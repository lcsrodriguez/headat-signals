"""

          _   _ _____    _    ____    _  _____
         | | | | ____|  / \  |  _ \  / \|_   _|
         | |_| |  _|   / _ \ | | | |/ _ \ | |
         |  _  | |___ / ___ \| |_| / ___ \| |
         |_| |_|_____/_/   \_\____/_/   \_\_|

            Developer           :   Lucas RODRIGUEZ
            Maintainer          :   Lucas RODRIGUEZ
            Development date    :   June 2022 - ...
            File description    :   HDView implementation
            Official Git repo   :   https://github.com/lcsrodriguez/headat-signals

"""
import math
import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import wfdb as wf
from wfdb.io.convert import wfdb_to_wav, wfdb_to_edf
import scipy.io
import pyspark
import tqdm
import requests
import validators
import wget
from pyspark.sql import SparkSession
from .lib.functions import *


if not os.path.exists(EXPORT_FOLDERS) or not os.path.isdir(EXPORT_FOLDERS):
    os.mkdir(EXPORT_FOLDERS)


class HDView:
    """
    Main class representing 1 HD View (1 WFDB record)
    """
    VIEWS_INITIALIZED_COUNTER = 0
    VIEWS_TITLES = []

    def __init__(self, record: str = "", title: str = "") -> None:
        """
        Constructor function initializing a new HDView object
        """

        # Declaring main variables
        self.sim_duration = None
        self.samples_foldername = None
        self.nb_observations = None
        self.columns = None
        self.spark_context = None
        self.record = None
        self.signals = None
        self.infos = None
        self.start_time = get_current_datetime()
        self.sim_start = None
        self.sim_end = None

        # Parsing the arguments of the c-tor
        if not isinstance(record, str) or not isinstance(title, str):
            raise TypeError("Record and title must be string values.")
        if record == "":
            #print(f"No record has been submitted.\nPlease consider adding one to the view by doing .add_record("
            #      f"record_name)")
            pass
        else:
            # Registering the record name
            if not self.add_record(record):
                raise Exception("The submitted record name is not valid. Please try it again")

        # Formatting HDView's title if title is not defined by the user
        if title == "":
            title = f"View #{HDView.VIEWS_INITIALIZED_COUNTER}"

        # Registering the HDView title
        self.title = title

        # Creation of the folder
        view_folder_name = make_view_directory()
        self.folder_name = view_folder_name
        self.start_clock()

    def start_clock(self):
        """ Function initiating the simulation clock """
        self.sim_start = time.time()

    def stop_clock(self):
        """ Function closing the simulation clock """
        self.sim_end = time.time()

    def compute_clock(self):
        """ Function computing the simulation total duration"""
        if self.sim_start is not None and self.sim_end is not None:
            self.sim_duration = math.fabs(self.sim_end - self.sim_start)

    def __str__(self) -> str:
        """
        Function representing as string the HDView object
        :return: Representation string
        """
        return f"HDView - [{self.title}] - #rec: {self.record}"

    def __del__(self) -> bool:
        """
        Function called when the Garbage Collector is summoned
        to kill a selected instance of HDView
        :return: bool
        """
        if self.spark_context is not None:
            print("Shutting down current SparkContext")
            self.spark_context.stop()
        #print("Instance killed")
        self.stop_clock()
        self.compute_clock()
        print(f"sim_dur: {self.sim_duration}")
        return True

    def __repr__(self) -> str:
        """
        Function representing as string the HDView object
        :return: Representation string
        """
        return f"HDView - [{self.title}] - #rec: {self.record}"

    def get_total_views_counter(self) -> int:
        """
        Function returning the total number of views initialized
        since the execution of the program
        """
        return HDView.VIEWS_INITIALIZED_COUNTER

    def download_sources(self, url_parent_folder: str = "") -> bool:
        """
        Function performing the complete download of remote files from
        https://physionet.org/ website resources
        :param url_parent_folder: String containing the URL from https://physionet.org
        :rtype: bool
        :return: Boolean showing if the full download has been performed with complete success
        """

        # Creation of a dedicated sub-folder named "samples/"
        path_filename = f"{self.folder_name}samples/"
        self.samples_foldername = path_filename
        if not os.path.isdir(path_filename) or not os.path.exists(path_filename):
            try:
                os.mkdir(path_filename)
            except Exception as e:
                raise Exception("An error has occured during the sub-folder creation process.\nError details: {e}")

        # Processing the URL
        # Checking if the record name is a URL
        if validators.url(url_parent_folder):
            try:
                url = urlparse(url_parent_folder)
                print(f"URL : {url}")

                # Restriction to the physionet.org webpages
                if url.scheme == "https":
                    if url.netloc == "physionet.org":
                        if url.path.split("/")[1] == "files":
                            # Download the files

                            # Getting the list of files from url
                            r = requests.get(url.geturl())
                            data = r.text
                            soup = BeautifulSoup(data, "html.parser")

                            # Formatting the relevant files
                            links = {
                                k.get("href"): url.geturl() + k.get("href") for k in soup.find_all("a")[1:] if
                                k.get("href").split(".")[-1] in ["hea", "dat"]
                            }

                            # Downloading the files
                            for file, link in tqdm.tqdm(links.items(), colour="blue"):
                                tqdm.tqdm.write(f"Processing link : {link}")
                                wget.download(url=link,
                                              out=f"{self.samples_foldername}{file}",
                                              bar=None)
                            print(f"Downloading from {url_parent_folder} completed successfully")
                            return True
                        else:
                            raise ValueError("You have to specify a files/ subfolder")
                    else:
                        raise ValueError("Headat only covers the 'physionet.org' web resources.")
                else:
                    raise ValueError("Headat only covers HTTPS protocol for web resources.")
            except Exception as e:
                raise Exception(f"An exception has occured during ")

        # If not, it's a local file and we simply read it using wfdb
        else:
            raise ValueError("The argument specified is not a valid URL.")

    def add_record(self, record: str = None) -> bool:
        """
        Function allowing user to add a record to the view
        :param record: Record name
        :rtype: bool
        :return: Boolean representing the success of the operation
        """
        if record is None:
            raise ValueError("record cannot be NoneType")

        try:
            # Increment the number of initialized views in order to get a count
            HDView.VIEWS_INITIALIZED_COUNTER += 1

            # Checking if the record name is a URL
            if validators.url(record):
                url = urlparse(record)
                print(f"URL : {url}")

                # We recover the parent folder:
                parent_folder = "/".join(url.geturl().split("/")[: -1]) + "/"
                print(parent_folder)
                self.download_sources(parent_folder)

                # Checking if the user has entered the URL to a file (.hea, .dat)
                # or just the name of the .hea without the extension
                if len(url.geturl().split(".hea")) > 1 or len(url.geturl().split(".dat")) > 1:
                    # We have the path to a .hea file
                    record = url.geturl().split("/")[-1].split(".")[0]
                else:
                    record = url.geturl().split("/")[-1]
                read_rec = wf.rdsamp(f"{self.samples_foldername}{record}")
            # If not, it's a local file and we simply read it using wfdb
            else:

                # Checking if the user has entered the URL to a file (.hea, .dat)
                # or just the name of the .hea without the extension
                if len(record.split(".hea")) > 1 or len(record.split(".dat")) > 1:
                    # We have the path to a .hea file
                    record = record.split(".")[0]

                # Reading the file
                read_rec = wf.rdsamp(record)

            # Filtering the signals and additional information from the signals using wfdb library
            self.signals = read_rec[0]
            self.infos = read_rec[1]
            self.columns = [k.lower().replace(" ", "_") for k in self.infos["sig_name"]]
            self.nb_observations = self.infos["sig_len"]

            # Registering the record on global scope
            self.record = record
            return True
        except Exception as e:
            raise Exception(f"Failure on the reading of the record: \nError details : {e}")

    def get_record_files(self, unique: bool = True) -> list:
        """
        Function returning the relative path of signal filenames
        :param unique: Boolean. If set to True, get_record_files(True) returns a list of unique (non-redundant items)
        filenames
        :rtype: list
        :return: List of signal filenames
        """
        try:
            record_hea_filename = self.record + ".hea"
            with open(record_hea_filename, "r") as f:
                files = f.readlines()[1 : ]
            if unique:
                return list(set([k.split(" ")[0] for k in files]))
            else:
                return [k.split(" ")[0] for k in files]
        except:
            raise Exception("Unable to find accurate signal files")

    def get_signals(self) -> np.ndarray:
        """
        Function returning the array of signals as Numpy ndarray
        :return: Numpy ndarray of signals where
            - 1 row = 1 record (1 observation)
            - 1 column = 1 signal
        """
        return self.signals

    def get_raw_signals(self) -> list:
        """
        Function returing a "pure" Python list of lists (kind of matrix)
        :return: List of lists Python representing the array of signals where
            - 1 row = 1 record (1 observation)
            - 1 column = 1 signal
        """
        return self.signals.tolist()

    def get_info(self) -> dict:
        """
        Function returning information about studied signals
        :return: Dictionary
        """
        return self.infos

    def get_spark_context(self) -> pyspark.sql.SparkSession:
        """
        Function initializing a SparkContext
        :rtype: pyspark.sql.SparkSession
        :return: SparkContext
        """
        if self.spark_context is None:
             self.spark_context = SparkSession.builder.master("local[1]")\
                 .appName('HEADAT RDD Converter')\
                .getOrCreate()
        return self.spark_context

    # ----------------------------------------------------------------
    #                     IN-PROGRAM CONVERSION METHODS

    def t_array(self) -> list:
        """
        Function returning a converted "pure" Python array of signals series
        :return: Python array
        """
        return self.get_raw_signals()

    def t_dict(self) -> dict:
        """
        Function returning a converted "pure" Python dict of signals series
        :return: Python dict
        """
        return self.t_frame().to_dict()

    def t_numpy(self) -> np.ndarray:
        """
        Function returning a converted Numpy ndarray of signals series
        :return: Numpy ndarrays
        """
        return self.get_signals()

    def t_numpy_records(self) -> np.record:
        """
        Function returning a converted Numpy records of signals series
        :rtype np.record:
        :return: Numpy records
        """
        return self.t_frame().to_records()

    def t_frame(self) -> pd.DataFrame:
        """
        Function returning a converted array as a Pandas DataFrame
        :return: Pandas DataFrame of the underlying signals
        """
        return pd.DataFrame(self.get_signals(), columns=self.columns)

    def t_rdd(self) -> pyspark.RDD:
        """
        Function returning a PySpark RDD
        :rtype: pyspark.RDD
        :return: PySpark RDD object
        """
        spark = self.get_spark_context()
        df_ps = spark.createDataFrame(self.t_frame())
        return df_ps.rdd

    # ----------------------------------------------------------------
    #                    EXPORT METHODS (GENERIC METHODS)

    def check_registered_record(self) -> bool:
        """
        Function returning whether a record has been registered to the view
        :return: Boolean
        """
        return (self.record is not None) and (self.signals is not None) and (self.infos is not None)

    def get_conversion_details(self, format: str = "csv") -> tuple:
        """
        Intermediary function converting the signals data into the desired/specified data type
        :param format: Format type (conversion output)
        :return: Tuple containing the original DataFrame, the extension and the method
        """

        # Checking if a record is registered
        if not self.check_registered_record():
            raise Exception("No record has been registered. Please call the .add_record() method before")

        # Filtering (security check)
        if not isinstance(format, str):
            raise TypeError("The format parameter needs to be represented as a non-empty string.")

        format = format.lower()
        if format not in get_export_types():
            raise ValueError("The format is not yet supported by the system. Please consider initiating a GitHub issue.")

        print(f"Conversion to format : {format}")
        df = self.t_frame()
        filename = self.folder_name + f"out_{self.start_time}.{formats[format]['extension']}"
        return df, formats[format]["method"], filename

    # ----------------------------------------------------------------
    #                    EXPORT METHODS (FORMAT METHODS)

    def t_txt(self, extension: str = "", separator: str = ",", **kwargs) -> bool:
        """
        Function converting the record to the textfile format (custom extension
        :param separator: Separator of the different columns items
        :param extension: Extension parameter
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, _, filename = self.get_conversion_details("text")
        filename += str(extension)
        try:
            df.to_csv(filename, sep=separator, index_label='id')
            return True
        except:
            return False

    def t_xlsx(self, **kwargs) -> bool:
        """
        Function converting the record to the XSLX format
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        if self.nb_observations > EXCEL_ROW_LIMIT:
            raise Exception("The record is too long for an .xlsx conversion.")
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("xlsx")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename, **kwargs)
            return True
        except:
            return False

    def t_csv(self, **kwargs) -> bool:
        """
        Function converting the record to the CSV format
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("csv")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename, index_label='id', **kwargs)
            return True
        except:
            return False

    def t_json(self, **kwargs) -> bool:
        """
        Function converting the record to the JSON format
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("json")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename, **kwargs)
            return True
        except:
            return False

    def t_xml(self, **kwargs) -> bool:
        """
        Function converting the record to the XML format
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("xml")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename, **kwargs)
            return True
        except:
            return False

    def t_md(self, **kwargs) -> bool:
        """
        Function converting the record to the MD (Markdown) format
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("markdown")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename, **kwargs)
            return True
        except:
            return False

    def t_html(self, **kwargs) -> bool:
        """
        Function converting the record to the HTML format
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("html")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename, **kwargs)
            return True
        except:
            return False

    def t_tex(self, **kwargs) -> bool:
        """
        Function converting the record to the .tex (TeX) format
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("latex")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename, **kwargs)
            return True
        except:
            return False

    def t_parquet(self, **kwargs) -> bool:
        """
        Function converting the record to the Apache Parquet format
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("parquet")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename, **kwargs)
            return True
        except:
            return False

    def t_pickle(self, **kwargs) -> bool:
        """
        Function converting the record to the Pickle (standard serialization) format
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("pickle")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename, **kwargs)
            return True
        except:
            return False

    def t_sql(self, **kwargs) -> bool:
        """
        Function converting the record to a database format supported by SQLAlchemy
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # TODO To be implemented
        pass

    def t_matlab(self, **kwargs) -> bool:
        """
        Function converting the record to a MATLAB file
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, _, filename = self.get_conversion_details("matlab")

        df.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
        try:
            scipy.io.savemat(file_name=filename,
                             mdict={
                                 'HEADAT': df.to_dict("list")
                             })
            return True
        except:
            return False

    def t_wav(self, **kwargs) -> bool:
        """
        Function converting the record to a .wav file
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, _, filename = self.get_conversion_details("wav")

        try:
            wfdb_to_wav(record_name=self.record,
                        output_filename=filename)
            return True
        except:
            return False

    def t_edf(self, **kwargs) -> bool:
        """
        Function converting the record to a .edf file
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, _, filename = self.get_conversion_details("edf")

        try:
            wfdb_to_edf(record_name=self.record,
                        output_filename=filename)
            return True
        except:
            return False

    def t_feather(self, **kwargs) -> bool:
        """
        Function converting the record to a .fea/.feather file
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("feather")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename, **kwargs)
            return True
        except:
            return False

    def t_stata(self, **kwargs) -> bool:
        """
        Function converting the record to a .dta file (STATA)
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("stata")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename, **kwargs)
            return True
        except:
            return False

    def t_hdf5(self, **kwargs) -> bool:
        """
        Function converting the record to a .hdf file (HDF5)
        :rtype: bool
        :return: Boolean set to True if conversion has been successfully performed
        """
        # Gathering the details concerning the specified format
        df, method, filename = self.get_conversion_details("hdf5")
        cl_m = eval(f"df.{method}")
        try:
            cl_m(filename,
                 key="df",
                 mode="w",
                 **kwargs
                 )
            return True
        except Exception as e:
            print(e)
            return False

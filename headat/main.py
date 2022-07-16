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
import numpy as np
import pandas as pd
import pyspark
import wfdb as wf
import scipy.io
import pyspark
from pyspark.sql import SparkSession
from .lib.functions import *

if os.path.exists(EXPORT_FOLDERS) and os.path.isdir(EXPORT_FOLDERS):
    pass
else:
    os.mkdir(EXPORT_FOLDERS)


class HDView:
    """
    Main class representing 1 HD View (1 WFDB record)
    """
    VIEWS_INITIALIZED_COUNTER = 0
    VIEWS_TITLES = []

    def __init__(self, record: str, title: str = "") -> None:
        """
        Constructor function initializing a new HDView object
        """

        # Declaring main variables
        self.spark_context = None
        self.record = None
        self.signals = None
        self.infos = None
        self.start_time = get_current_datetime()

        # Parsing the arguments of the c-tor
        if not isinstance(record, str) or not isinstance(title, str):
            raise TypeError("Record and title must be string values.")
        if record == "":
            raise ValueError("Record name must be a valid one : not empty")

        # Increment the number of initialized views in order to get a count
        HDView.VIEWS_INITIALIZED_COUNTER += 1

        # Formatting HDView's title if title is not defined by the user
        if title == "":
            title = f"View #{HDView.VIEWS_INITIALIZED_COUNTER}"

        # Registering the HDView title
        self.title = title

        # Creation of the folder
        view_folder_name = make_view_directory()
        self.folder_name = view_folder_name

        # Registering the record name
        if not self.add_record(record):
            raise Exception("The submitted record name is not valid. Please try it again")

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
        print("Instance killed")
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
            # Registering the record on global scope
            self.record = record

            # Reading the record
            read_rec = wf.rdsamp(record)

            # Filtering the signals and additional information from the signals using wfdb library
            self.signals = read_rec[0]
            self.infos = read_rec[1]
            self.columns = [k.lower().replace(" ", "_") for k in self.infos["sig_name"]]
            self.nb_observations = self.infos["sig_len"]
            print(self.columns)
            return True
        except Exception as e:
            raise Exception(f"Failure on the reading of the record: \nError details : {e}")

    def get_record_files(self, unique: bool = True) -> list:
        """
        Function returning the relative path of signal filenames
        :param unique: Boolean. If set to True, get_record_files(True) returns a list of unique (non-redundant items) filenames
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

    def get_infos(self) -> dict:
        """
        Function returning information about studied signals
        :return: Dictionary
        """
        return self.infos

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

        # TODO : Faire une fonction qui initie un Spark Context s'il n'en existe pas sinon utiliser l'actuel créé

        spark = SparkSession.builder.master("local[1]")\
            .appName('HEADAT RDD Converter')\
            .getOrCreate()
        self.spark_context = spark
        df_ps = spark.createDataFrame(self.t_frame())
        df_rdd = df_ps.rdd
        return df_rdd

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
        # TODO
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

        # TODO: Do the implementation

        pass

    # ----------------------------------------------------------------
    #                           GENERIC METHODS

    def get_records_hashes(self):
        """
        Function computing and returning the different hashes of the record files.
        :return:
        """
        import hashlib
        BLOCKSIZE = 65536
        hasher = hashlib.md5()
        # TODO : Complete function (check Twitter post)


"""
    1 record <-> 1 or more signals

    ------------------------------------------------
    1 record <-> 1 HDView 
        - useful for extracting entire or partial signals and entire records or selected signals from 1 record
        - importing them as numpy array or pandas DataFrame, series, dictionnary, Python list
        - exporting them to specific formats:
            - csv, xlsx, json, xml
            - text file with specific extension (.txt, .out, .dat, ...)
            - latex, markdown, html
            - pickle
            - parquet
            - hdfs
            - sqlite
            - matlab
            - wav
        - extracting useful information
    ------------------------------------------------
    1 or more records <-> 1 HDGroup ==> Goal: statistical comparison
        - do the same as with 1 HDView but concat the multiple records side-by-side 
"""

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
import wfdb as wf
from lib.functions import *

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
        self.record = None
        self.signals = None
        self.infos = None

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
    #                           EXPORT METHODS

    def check_registered_record(self) -> bool:
        """
        Function returning whether a record has been registered to the view
        :return: Boolean
        """
        return (self.record is not None) and (self.signals is not None) and (self.infos is not None)

    def convert(self, format: str = "csv") -> bool:
        """
        Intermediary function converting the signals data into the desired/specified data type
        :param format: Format type (conversion output)
        :return: Boolean indicating if the conversion and the
                 storage steps have been well-performed
        """

        # Checking if a record is registered
        if not self.check_registered_record():
            raise Exception("No record has been registered. Please call the .add_record() method before")

        # Filtering (security check)
        if not isinstance(format, str):
            raise TypeError("The format parameter needs to be represented as a non-empty string.")

        format = format.lower()
        # Filtering values
        print(format)
        if format not in get_export_extensions():
            raise ValueError("The format is not yet supported by the system. Please consider initiating a GitHub issue.")

        print(f"Asked format : {format}")

        df = self.t_frame()
        # Converting the view in the specified extension
        try:
            if formats[format]["method"] == "custom":
                print(f"Not yet supported for {format}")
                return False
            if format in ["json", "pickle"]:
                # Error with the JSON format: 'index=False' is only valid when 'orient' is 'split' or 'table'
                eval(f"df.{formats[format]['method']}(self.folder_name + f'out_{get_current_datetime()}.{formats[format]['extension']}')")
            elif format == "latex":
                eval(f"df.{formats[format]['method']}(self.folder_name + f'out_{get_current_datetime()}.{formats[format]['extension']}')")
            else:
                eval(f"df.{formats[format]['method']}(self.folder_name + f'out_{get_current_datetime()}.{formats[format]['extension']}', index=False)")
            print(f"Export finished for {format} format")
            return True
        except Exception as e:
            print(e)
            return False



    def t_frame(self) -> pd.DataFrame:
        """
        Function returning a converted array as a Pandas DataFrame
        :return: Pandas DataFrame of the underlying signals
        """
        return pd.DataFrame(self.get_signals())

    def t_numpy(self) -> np.ndarray:
        """
        Function returning a converted Numpy ndarray of signals series
        :return: Numpy ndarrays
        """
        return self.signals

    def t_csv(self) -> bool:
        """ Function converting the record to the CSV format """
        return self.convert("xlsx")

    def t_xlsx(self) -> bool:
        """ Function converting the record to the XLSX format """
        return self.convert("xlsx")

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


class HDGroup:
    """
    HDGroup class
    """
    pass


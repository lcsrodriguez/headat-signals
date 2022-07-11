"""

          _   _ _____    _    ____    _  _____
         | | | | ____|  / \  |  _ \  / \|_   _|
         | |_| |  _|   / _ \ | | | |/ _ \ | |
         |  _  | |___ / ___ \| |_| / ___ \| |
         |_| |_|_____/_/   \_\____/_/   \_\_|

            Developer: Lucas RODRIGUEZ (2022)
"""
import pandas as pd
import wfdb as wf
import logging
from .constants import *


class HDView:
    """
    Main class representing a HD View (1 WFDB record)
    """
    VIEWS_INITIALIZED_COUNTER = 0
    VIEWS_TITLES = []

    def __init__(self, record: str, title: str = "") -> None:
        """
        Constructor function initializing a new HDView object
        """

        # Parsing the arguments of the c-tor
        if not isinstance(record, str) or not isinstance(title, str):
            raise TypeError("Record and title must be string values.")
        if record == "":
            raise ValueError("Record name must be a valid one : not empty")

        # Increment the number of initialized views in order to get a count
        HDView.VIEWS_INITIALIZED_COUNTER += 1

        # Formatting HDView's title
        if title == "":
            title = f"View #{HDView.VIEWS_INITIALIZED_COUNTER}"

        self.record = record
        self.title = title

        # Registering the record name
        if not self.add_record(record):
            raise Exception("The submitted record name is not valid. Please try it again")

    def __str__(self) -> str:
        """
        Function representing as string the HDView object
        :return: Representation string
        """
        return f"HDView - [{self.title}] - #rec: {self.record}"

    def add_record(self, record: str = None) -> bool:
        """
        Function allowing user to add a record to the view
        :param record: Record name
        :rtype: bool
        :return: Boolean representing the success of the operation
        """

        """
        if self.source_record is not None:
            pass
            # TODO : Add folder check
            # TODO : Add if there is a .hea and a corresponding .dat file
        else:
            raise Exception("The record path to file is empty or not valid.")
        """

    def t_csv(self):
        """
        Function converting the record to the CSV format
        """
        pass

    def t_xlsx(self):
        """
        Function converting the record to the XLSX format
        """
        pass

    def get_total_views_counter(self) -> int:
        """
        Function returning the total number of views initialized 
        since the execution of the program
        """
        return HDView.VIEWS_INITIALIZED_COUNTER

    def get_export_extensions(self) -> list:
        """
        Function returning the array of the currently available
        extensions supported by the tool's exporter
        :return: list with specific types' extensions
        """
        return [AVAILABLE_EXPORT_TYPES[k]["ext"] for k in AVAILABLE_EXPORT_TYPES]

    def get_export_types(self) -> list:
        """
        Function returning the array of the currently available
        types supported by the tool's exporter
        :return: list with specific types
        """
        return [k for k in AVAILABLE_EXPORT_TYPES]

    def get_records_hashes(self):
        """
        Function computing and returning the different hashes of the record files.
        :return:
        """
        import hashlib
        BLOCKSIZE = 65536
        hasher = hashlib.md5()


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


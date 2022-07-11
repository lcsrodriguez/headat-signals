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
from .constants import *

class HDView:
    """
    Main class representing a HD View (1 WFDB record)
    """
    VIEWS_INITIALIZED_COUNTER = 0
    VIEWS_TITLES = []

    def __init__(self, source_record: str = None, title: str = None) -> None:
        """
        Constructor function initializing a new HDView object
        """

        # Parsing the arguments of the c-tor
        self.source_record = None
        self.title = title if title != None else f"HDView #{HDView.VIEWS_INITIALIZED_COUNTER}"

        # Adding a record
        self.add_record(source_record)

        # Increment the number of initialized views in order to get a count
        HDView.VIEWS_INITIALIZED_COUNTER += 1
        HDView.VIEWS_TITLES.append(self.title)

        print("Logging the creation of a new HDView")

    def add_record(self, source_record: str = None):
        """
        Function allowing user to add a record to the view
        """
        print("ADD")
        self.source_record = source_record
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

    def get_total_views_counter() -> int:
        """
        Function returning the total number of views initialized 
        since the execution of the program
        """
        return HDView.VIEWS_INITIALIZED_COUNTER


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


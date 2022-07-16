from .constants import *
import datetime
import os
import warnings
# Export routine to LaTeX generate a FutureWarning which has to be silenced
warnings.simplefilter(action='ignore', category=FutureWarning)

def get_current_datetime() -> str:
    """
    Function returning the current datetime in a string representation
    :return: String representation of the current datetime
    """
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S+%f")


def make_view_directory(out_folder: str = EXPORT_FOLDERS) -> str:
    """
    Function creating a dedicated directory for an HDView inside the out/ folder
    :param out_folder: If not default, specified parent folder
    :return: String of the folder pathname; Exception if error has occured
    """
    path_filename = f"{out_folder}/view_{get_current_datetime()}/"
    if not os.path.isdir(path_filename) or not os.path.exists(path_filename):
        try:
            os.mkdir(path_filename)
            return path_filename
        except Exception as e:
            raise Exception("An error has occured during the folder creation process.\nError details: {e}")


def get_export_types() -> list:
    """
    Function returning the array of the currently available
    types supported by the tool's exporter
    :return: list with specific types
    """
    return list(formats.keys())


def get_export_extensions() -> list:
    """
    Function returning the array of the currently available
    extensions supported by the tool's exporter
    :return: list with specific types' extensions
    """
    return [formats[k]["extension"] for k in formats]

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

"""
    --------------------------------------------------------------------------------
    This file is the official test document where you can test the main features
    Please clone the current repo and execute it by performing
    python3 test.py
    --------------------------------------------------------------------------------
"""

# Importing the main file from HEADAT
from headat.main import *

# Specify the record path
record_path = "samples/aami3a.hea"

# Initiating the HDView
v = HDView()

# Adding a local resource
v.add_record(record_path)

# OR

# Adding a remote resource from PhysioNet repo (WARNING : Heavy files (2.7GB))
#v.add_record("https://physionet.org/files/cebsdb/1.0.0/b001.hea")

# Getting information labels from the HDView
print(v.get_info())

# Getting raw signals (truncated by Python for human-friendly printing)
print(v.get_signals())

# Getting the underlying files from the HDView
print(v.get_record_files())

# Getting information on new folder :
print(f"The output folder is : {v.folder_name}\nThe export files are located inside.\nFor remote resources, a subfolder samples/ contains the "
      f"downloaded files.")

# Collecting signals in various types
print(v.t_frame()) # Pandas DataFrame
print(v.t_array()) # "Pure" Python array

# Converting the signals into readable data format for further statistical processing
v.t_csv()
v.t_xlsx()
v.t_json()
v.t_xml()

# Slow for heavy-sized files (due to the complexity of the standardized file format)
v.t_md()
v.t_tex()

# Fast for heavy-sized files (columnar-based, in-memory and serialization)
v.t_parquet()
v.t_pickle()
v.t_feather()

# (Check the README for the complete list)

# Getting the number of views initiated
print(HDView.VIEWS_INITIALIZED_COUNTER)

# Getting supported export formats information
print(get_export_types())
print(get_export_extensions())

# End of test file

# Lucas RODRIGUEZ - July 2022
from headat.main import *


file_folder = "data/apnea-ecg-database-1.0.0/"
file = "samples/aami3a"
#a = HDView(file_folder + "a01r")
a = HDView(file)
b = a.get_signals()
print(a.get_infos())
c = a.t_frame()
print(get_export_types())

"""
a.t_csv()
a.t_xlsx()
a.t_json()
a.t_xml()
a.t_md()
a.t_tex()
a.t_parquet()
a.t_pickle()
a.t_wav()
#a.t_edf()
a.t_csv()
a.t_feather()
"""
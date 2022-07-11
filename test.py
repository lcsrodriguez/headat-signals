import pandas as pd
from headat.main import *
import wfdb


file_folder = "data/apnea-ecg-database-1.0.0/"
rec = wfdb.rdsamp(file_folder + "a01r")

print(AVAILAB)
print(rec)
a = HDView()

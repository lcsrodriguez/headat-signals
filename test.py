from headat.main import *


file_folder = "data/apnea-ecg-database-1.0.0/"

a = HDView(file_folder + "a01r")
b = a.get_signals()



#print(a.convert("csv"))
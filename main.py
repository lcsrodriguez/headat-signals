import wfdb

file_folder = "data/apnea-ecg-database-1.0.0/"
rec = wfdb.rdsamp(file_folder + "a01r")
print(len(rec[0][1]))

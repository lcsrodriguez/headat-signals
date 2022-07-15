from headat.main import *

file_folder = "data/apnea-ecg-database-1.0.0/"

a = HDView(file_folder + "a01r")
b = a.get_signals()

print(len(b))
c = pd.DataFrame(b)
c.to_excel("test.xlsx")


for ext in get_export_extensions():
    a.convert(ext)
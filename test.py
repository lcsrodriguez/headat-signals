from headat.main import *

print(pd.__version__)
file_folder = "data/apnea-ecg-database-1.0.0/"

a = HDView(file_folder + "a01r")
b = a.get_signals()
print(a.get_infos())
c = a.t_frame()
#print(c.head(20))

#c.to_pickle("out/test.pickle")


print(pd.read_pickle("out/test.pickle"))
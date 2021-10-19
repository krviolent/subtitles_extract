EP = 31
import os
from os import listdir, getcwd, path
def listToString(s): 
    # initialize an empty string
    str1 = " "     
    # return string  
    return (str1.join(s))

filename = f"subs_file_{EP}.txt"
mypath = path.abspath(os.getcwd())
timestamps = list()
textonly = list()
subs_dir = mypath + f"/subs/EP.A.{EP}/"
print(subs_dir)
if not os.path.isdir(subs_dir):
    os.mkdir(subs_dir)
lines = list()
with open(filename) as f:
    lines = f.readlines()
print(len(lines))
for line in lines:
    line = line.split(" ")
    #print(line)
    with open(subs_dir  + "timestamps.txt", "a+") as ti:
        ti.write(line[0] + "\n")
        print(line[0])
    with open(subs_dir + "textonly.txt", "a+") as te:
        te.write(listToString(line[1:]) + "\n")

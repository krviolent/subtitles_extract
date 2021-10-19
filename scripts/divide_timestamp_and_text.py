import os, sys
from os import listdir, getcwd, path

EP = sys.argv[1]

def listToString(s): 
    # initialize an empty string
    str1 = " "     
    # return string  
    return (str1.join(s))

mypath = path.abspath(os.getcwd())
timestamps = list()
textonly = list()
subs_dir = mypath + f"/subs/EP.A.{EP}/"
filename = mypath + f"/subs/" + f"subs_file_{EP}.txt"
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
        #print(line[0])
    with open(subs_dir + "textonly.txt", "a+") as te:
        te.write(listToString(line[1:]))

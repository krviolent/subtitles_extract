# -*- coding: utf-8 -*-
import easyocr
import os
from os import listdir, getcwd, path
from os.path import isfile, join
import re, sys
import time

def cjk_detect(texts):
    # korean
    #if re.search("[\uac00-\ud7a3]", texts):
    #    return "ko"
    # japanese
    #if re.search("[\u3040-\u30ff]", texts):
    #    return "ja"
    # chinese
    if re.search("[\u4e00-\u9FFF]", texts):
        return 1
        #return "zh"
    return 0
def listToString(s): 
    # initialize an empty string
    str1 = " "     
    # return string  
    return (str1.join(s))

def gettime(x):
	import datetime
	n = ["0", str(datetime.timedelta(seconds=x)),".000"]
	return "".join(n)

def gettime_norm(x):
	import datetime
	n = ["0", str(datetime.timedelta(seconds=x)),".000"]
	return "".join(n)


def save_subs(tdict, filename):
    with open(filename, "a+") as f:
        for key,value in tdict.items():
            f.write(gettime(key) + " " + value + "\n")
    print(f"Saved subs in {filename}")

"""Удаление повторений в словаре субтитров"""
def remove_dups_in_dict(test_dict):
    # Remove duplicate values in dictionary
    # Using dictionary comprehension
    temp = {val : key for key, val in test_dict.items()}
    res = {val : key for key, val in temp.items()}
    return res
    
def replace_sym(text):
    for ch in ['\\','`','*','_','{','}','[',']','(',')','>','#','+','-','!','$','\'']:
        if ch in text:
            text = text.replace(ch,"")
    return text

def extract_subs():
# episode number
    EP = sys.argv[1]
    start_time = time.time()
    #Specify original subtitles language for recognition
    reader = easyocr.Reader(['ch_tra']) # this needs to run only once to load the model into memory

    mypath = path.abspath(os.getcwd()) + f"/frame_{EP}/"
    print(mypath)
    if not os.path.isdir(mypath):
        os.mkdir(mypath)
    print(mypath)
    subs = dict()
    onlyfiles = [f for f in listdir(mypath)]
    onlyfiles.sort()
    #print(onlyfiles)
    frame_number = 0
    try:
    	if isinstance(sys.argv[2], int):
        	frames_number = int(sys.argv[2])
    except:
    	frames_number = 2610 # 2582 - 43 минуты
    if frames_number > len(onlyfiles):
        frames_number = len(onlyfiles)

    for i in range(frames_number):
        result = reader.readtext(mypath + onlyfiles[i], detail=0)
        sub = listToString(result)
        #file_time = int((file.split(".")[-2]).split("-")[-1])
        #if len(result) > 1 and sub not in subs.values():
        # i - frame second
        if len(result)>0 and cjk_detect(sub) == 1: #decode("utf-8")
            #print(sub)
            subs[i] = sub
            print(i)
    print("done all: round 1")
    print("Starting round 2")
    #print("Filtering subs...")
    #subs_filtered = remove_dups_in_dict(subs)
    #print("Filtering done!")
    filename = f"subs_file{EP}.txt"
    print(f"Saving subs to {filename}")
    #save_subs(subs_filtered, filename)
    subs_dir = path.abspath(os.getcwd()) + f"/subs/EP.A.{EP}/"
    os.makedirs(subs_dir)
    save_subs(subs, os.getcwd() + "/subs/" + filename)
    # print programm running time
    print("--- %s seconds ---" % gettime_norm(int(time.time() - start_time)))
    lines = list()
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(" ")
        #print(line)
        with open(subs_dir  + "timestamps.txt", "a+") as ti:
            ti.write(line[0] + "\n")
            #print(line[0])
        with open(subs_dir + "textonly.txt", "a+") as te:
            te.write(listToString(line[1:]))
            
    import shutil
    print(f"Removing {mypath}...")
    shutil.rmtree(mypath)
    print("Done")

if __name__ == "__main__":
    extract_subs()

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
	n = ["0", str(datetime.timedelta(seconds=x)),",000"]
	return "".join(n)

def gettime_norm(x):
	import datetime
	n = ["0", str(datetime.timedelta(seconds=x)),",000"]
	return "".join(n)


def save_subs(tdict, filename):
    with open(filename, "w+") as f:
        for key,value in tdict.items():
            f.write(str(key) + " " + value.replace(" ","") + "\n")
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

def cut_right(text):
    return "".join(list(text)[2:])

def cut_left(text):
    return "".join(list(text)[:-2])

def do_srt_f(subs_dir, lines):
    EP = sys.argv[1]
    frame_rate = int(sys.argv[3])
    filename = os.getcwd() + "/subs/" + f"subs_file_{EP}.txt"
    subs_dir = path.abspath(os.getcwd()) + f"/subs/EP.A.{EP}/"
    lines = list()    
    
    with open(filename) as f:
        lines = f.readlines()
    
    i = 1
    k = 0
    print("lines len: ", len(lines))
    init_len = len(lines)
    # Check if duplicated subs are exist
    for i in range(len(lines)):
        line = lines[i].split(" ")
        timestamp = int(line[0])
        text = listToString(line[1:])
        while True:
            if i < len(lines)-1:
                next_text = listToString((lines[i+1].split(" "))[1:])
                print("current: ", text)
                print("next:    ", next_text)
                if text == next_text:
                    print("match!")
                    del lines[i+1]
                    i = i + 1
                    k = k + 1
                elif text == cut_left(next_text) or text == cut_right(next_text):
                    print("magic!")
                    lines[i] = lines[i+1]
                    del lines[i+1]
                else:
                    break
            else:
                break
        if i >= len(lines) - 1:
            break
    print("lines len: ", len(lines))
    line_code = 1
    for i in range(len(lines)):
        line_code = i + 1
        k = i
        line = lines[i].split(" ")
        timestamp = int(line[0])
        next_timestamp = 0
        if i+1 < len(lines):
            next_timestamp = int((lines[i+1].split(" "))[0])
        else:
            next_timestamp = timestamp

        frame_content = listToString(line[1:])
        duration = frame_rate
        #print(line)
        with open(subs_dir  + f"subs_{sys.argv[1]}.srt", "a+") as ti:
            if next_timestamp - timestamp > 2:
                duration = 3*frame_rate
            elif i+1 >= len(lines):
                duration = 2*frame_rate
            else:
                duration = next_timestamp - timestamp
            frame_start = gettime(timestamp/frame_rate)
            frame_end = gettime((timestamp + duration)/frame_rate)
            subtitle_line = f'{line_code}\n{frame_start} --> {frame_end}\n{frame_content}\n'
            ti.write(subtitle_line)
            
            
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
    	if isinstance(int(sys.argv[2]), int):
        	frames_number = int(sys.argv[2])
    except:
    	frames_number = 2610 # 2582 - 43 минуты
    if frames_number > len(onlyfiles):
        frames_number = len(onlyfiles)

    for i in range(frames_number):
        result = reader.readtext(mypath + onlyfiles[i], detail=0)
        #result = reader.readtextlang(mypath + onlyfiles[i])
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
    filename = os.getcwd() + "/subs/" + f"subs_file_{EP}.txt"
    print(f"Saving subs to {filename}")
    #save_subs(subs_filtered, filename)
    subs_dir = path.abspath(os.getcwd()) + f"/subs/EP.A.{EP}/"
    if not os.path.isdir(subs_dir):
        os.makedirs(subs_dir)
    save_subs(subs, filename)
    # print programm running time
    print("--- %s seconds ---" % gettime_norm(int(time.time() - start_time)))
    lines = list()    
    
    with open(filename) as f:
        lines = f.readlines()
    
    do_srt_f(subs_dir, lines)
    
    import shutil
    print(f"Removing {mypath}...")
    shutil.rmtree(mypath)
    print("Done")

if __name__ == "__main__":
    extract_subs()

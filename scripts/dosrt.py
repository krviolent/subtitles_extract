import os,sys
from os import path
from easyocr_test import gettime, listToString
def do_srt_f():
    EP = sys.argv[1]
    frame_rate = int(sys.argv[2])
    subs_dir = path.abspath(os.getcwd()) + f"/subs/EP.A.{EP}/"
    filename = os.getcwd() + "/subs/" + f"subs_file_{EP}.txt"
    if not os.path.isdir(subs_dir):
        os.makedirs(subs_dir)
    # print programm running time
    lines = list()    
    
    with open(filename) as f:
        lines = f.readlines()
    
    i = 1
    k = 0
    print("lines len: ", len(lines))
    init_len = len(lines)
    for i in range(len(lines)):
        line = lines[i].split(" ")
        timestamp = int(line[0])
        text = listToString(line[1:])
        print(i, " : ", len(lines))
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
                else:
                    break
            elif i >= len(lines) -1:
                break
            else:
                break
        if i >= len(lines) - 1:
            break
    print("lines len: ", len(lines))
    counter = 1
    for i in range(len(lines)):
        k = i
        line = lines[i].split(" ")
        timestamp = int(line[0])
        next_timestamp = 0
        if i+1 < len(lines):
            next_timestamp = int((lines[i+1].split(" "))[0])
        else:
            next_timestamp = timestamp

        text = listToString(line[1:])
        # Check if duplicated subs are exist
        duration = 1
        #print(line)
        with open(subs_dir  + f"subs_{sys.argv[1]}.srt", "a+") as ti:
            ti.write(str(counter) + "\n")
            if next_timestamp - timestamp > 2:
                duration = 3
            elif i+1 >= len(lines):
                duration = 2
            else:
                duration = next_timestamp - timestamp
            ti.write(gettime(timestamp/2.0) + " --> " + gettime(timestamp/2.0 + duration/2.0) + "\n")
            ti.write(text + "\n")
            counter = counter + 1


if __name__ == "__main__":
    do_srt_f()

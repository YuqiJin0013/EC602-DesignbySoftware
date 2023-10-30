#!/usr/bin/env python

import os
import sys
import stat
import pwd
import grp
import time
from lsfiles import printInCol
from lslong import get_file_details
from lsfiles import lscoltwo

def lsone():
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    files.sort()
    for file in files:
        print(file)

def lscol(path='.'):
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    files.sort()
    
    terminal_width = os.get_terminal_size().columns
    max_len = 0
    for file in files:
        if len(file) > max_len:
            max_len = len(file)
    num_cols = terminal_width // (max_len + 1)
    num_rows = (len(files) + num_cols - 1) // num_cols

    for row in range(num_rows):
        for col in range(num_cols):
            pointer = row + col * num_rows
            if pointer < len(files):
                file = files[pointer]
                print(file.ljust(max_len), end=" ")
        print()

def lsfiles(path='.'):
    # current_directory = os.getcwd()
    files = os.listdir(path)
    files.sort()
    # case 1: it is folder
    #   print folder name first then call the func lscoltwo() the files inside of folder
    # case 2: it is file
    # just print files  call the func printInCol()
    fileList = []
    folderList = []
    for entry in files:
        if os.path.isfile(entry):
            fileList.append(entry)
        else:
            folderList.append(entry)
    printInCol(fileList)
    print()
    for folder in folderList:
        print(folder + ":")
        lscoltwo("./" + folder)
        print()

def lslong(paths='.'):
    entries = []
    for path in paths:
        if os.path.exists(path):
            if os.path.isdir(path):
                for filename in os.listdir(path):
                    file_path = os.path.join(path, filename)
                    entries.append(file_path)
            else:
                entries.append(path)
        else:
            print(f"ls: cannot access '{path}': No such file or directory")
    # Sort the entries alphabetically
    entries.sort()
    for entry in entries:
        print(get_file_details(entry))


if len(sys.argv) > 1:
    input_arg = sys.argv[1]

    if input_arg == '-1':
        lsone()
    elif input_arg == '-C':
        lscol()
    elif input_arg == '*':
        lsfiles()
    elif input_arg == '-l':
        lslong()
    elif input_arg == '':
        lsfiles()
    else:
        lsfiles()
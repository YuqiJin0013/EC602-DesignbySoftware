#!/usr/bin/env python

import os
import sys

# Write an executable Python script lsfiles that works the same way as ls 
# when files and/or directories are specified on the command line.

def lsfiles(path='.'):
    # current_directory = os.getcwd()
    files = os.listdir(path)
    files.sort()
    # case 1: it is folder
    #   print folder name first then call the func lscol() the files inside of folder
    # case 2: it is file
    # just print files  call the func lscol()
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
        
def printInCol(files):
    max_len = 0
    for file in files:
        if len(file) > max_len:
            max_len = len(file)
    terminal_width = os.get_terminal_size().columns
    num_cols = terminal_width // (max_len + 1)
    num_rows = (len(files) + num_cols - 1) // num_cols

    for row in range(num_rows):
        for col in range(num_cols):
            pointer = row + col * num_rows
            if pointer < len(files):
                file = files[pointer]
                print(file.ljust(max_len), end=" ")
        print()       
    
def lscoltwo(path='.'):
    files = os.listdir(path)
    files.sort()
    
    terminal_width = os.get_terminal_size().columns
    
    max_len1 = 0
    for file in files:
        if len(file) > max_len1 : 
            max_len1 = len(file)
            
    num_cols = terminal_width // (max_len1 + 1)
    num_rows = (len(files) + num_cols - 1) // num_cols

    for row in range(num_rows):
        for col in range(num_cols):
            pointer = row + col * num_rows
            if pointer < len(files):
                file = files[pointer]
                print(file.ljust(max_len1), end=" ")
        print()

if __name__ == "__main__":
    lsfiles()




        






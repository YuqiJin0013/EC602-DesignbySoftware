#!/usr/bin/env python

import os

def lsone(path='.'):
    # current_directory = os.getcwd()
    files = os.listdir(path)
    files.sort()
    for file in files:
        print(file)
        
if __name__ == "__main__":
    lsone()
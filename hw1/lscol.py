#!/usr/bin/env python

import os

def lscol(path='.'):
    # current_directory = os.getcwd()
    files = os.listdir(path)
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

if __name__ == "__main__":
    lscol()

    









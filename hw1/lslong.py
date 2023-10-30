#!/usr/bin/env python

# Write an executable Python script lslong that works the same way as ls -l
import os
import sys
import stat
import pwd
import grp
import time

def get_file_details(file_path):
    stat_info = os.stat(file_path)
    permissions = stat.filemode(stat_info.st_mode)
    num_links = stat_info.st_nlink
    owner = pwd.getpwuid(stat_info.st_uid).pw_name
    group = grp.getgrgid(stat_info.st_gid).gr_name
    size = stat_info.st_size
    mod_time = time.strftime("%b %d %H:%M:%S", time.localtime(stat_info.st_mtime))
    file_name = os.path.basename(file_path)
    return f"{permissions:6} {num_links:2} {owner:6} {group:6} {size:6} {mod_time:10} {file_name}"

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

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        args = ["."]  
    lslong(args)




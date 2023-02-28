#!/usr/bin/env python3

import os
import subprocess

current_dir = os.path.dirname(os.path.realpath(__file__))
current_path = current_dir.split("/")
current_folder = current_path[-1]
parent_dir = '/'.join(current_path[:-1])

command_list = ["xgettext", "-k_tr", "-kN_tr", "--from-code", "utf-8", "-o", current_dir+"/system-monitoring-center.pot", "-f", current_dir+"/POTFILES.in", "-D", parent_dir]
process = subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
error_output = process.stderr.decode().strip()
if error_output != "":
    print(error_output)


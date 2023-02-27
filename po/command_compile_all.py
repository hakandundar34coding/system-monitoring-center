#!/usr/bin/env python3

import os
import subprocess

current_dir = os.path.dirname(os.path.realpath(__file__))

po_files = [file_name for file_name in os.listdir(current_dir) if file_name.endswith(".po")]

for po_file in po_files:
    file_name_only = po_file.rstrip(".po")
    target_dir = current_dir + "/locale/" + file_name_only + "/LC_MESSAGES"
    mo_file = target_dir + "/system-monitoring-center.mo"
    if os.path.isdir(target_dir) == False:
        try:
            os.makedirs(target_dir)
        except Exception:
            pass
    command_list = ["msgfmt", "-o", mo_file, po_file]
    process = subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_output = process.stderr.decode().strip()
    if error_output != "":
        print(error_output)


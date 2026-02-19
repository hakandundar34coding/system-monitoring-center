#!/usr/bin/env python3

import os
import sys

current_path = os.path.dirname(os.path.realpath(__file__)).split("/")
parent_dir = '/'.join(current_path[:-1])
current_folder = current_path[-1]
sys.path.append(parent_dir)

if current_folder == "src":
    from src import Main
if current_folder == "systemmonitoringcenter":
    from systemmonitoringcenter import Main
localedir = None
Main.main(localedir)


#!/usr/bin/env python3

def start_app():

    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/src/")
    import Main


#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

application_id="io.github.hakandundar34coding.system-monitoring-center"

localedir = None
def main(_localedir):
    global localedir
    localedir = _localedir

from .MainWindow import MainWindow
main_window = MainWindow.main_window
main_window.mainloop()


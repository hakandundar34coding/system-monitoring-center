#!/usr/bin/env python3

# ----------------------------------- Performance - Performance Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def performance_menus_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global Config, PerformanceGUI, Performance
    import Config, PerformanceGUI, Performance


# ----------------------------------- Performance - Performance Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Performance" tab menu/popover GUI objects and functions/signals) -----------------------------------
def performance_menus_gui_func():







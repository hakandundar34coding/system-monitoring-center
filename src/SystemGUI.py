#!/usr/bin/env python3

# ----------------------------------- System - System GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def system_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global MainGUI, System
    import MainGUI, System


# ----------------------------------- System - System GUI Function (the code of this module in order to avoid running them during module import and defines "System" tab GUI objects and functions/signals) -----------------------------------
def system_gui_func():

    global grid8101
    global label8101, label8102, label8103, label8104, label8105, label8106, label8107, label8108, label8109, label8110
    global label8111, label8112, label8113, label8114, label8115, label8116, label8117, label8118, label8119, label8120, label8121


    # System tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/SystemTab.ui")

    # System tab GUI objects - get
    grid8101 = builder.get_object('grid8101')
    label8101 = builder.get_object('label8101')
    label8102 = builder.get_object('label8102')
    label8103 = builder.get_object('label8103')
    label8104 = builder.get_object('label8104')
    label8105 = builder.get_object('label8105')
    label8106 = builder.get_object('label8106')
    label8107 = builder.get_object('label8107')
    label8108 = builder.get_object('label8108')
    label8109 = builder.get_object('label8109')
    label8110 = builder.get_object('label8110')
    label8111 = builder.get_object('label8111')
    label8112 = builder.get_object('label8112')
    label8113 = builder.get_object('label8113')
    label8114 = builder.get_object('label8114')
    label8115 = builder.get_object('label8115')
    label8116 = builder.get_object('label8116')
    label8117 = builder.get_object('label8117')
    label8118 = builder.get_object('label8118')
    label8119 = builder.get_object('label8119')
    label8120 = builder.get_object('label8120')
    label8121 = builder.get_object('label8121')

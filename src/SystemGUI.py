#!/usr/bin/env python3

# ----------------------------------- System - System GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def system_gui_import_func():

    global Gtk

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk


    global MainGUI, System
    import MainGUI, System


# ----------------------------------- System - System GUI Function (the code of this module in order to avoid running them during module import and defines "System" tab GUI objects and functions/signals) -----------------------------------
def system_gui_func():

    global label8101, label8102, label8103, label8104, label8105, label8106, label8107, label8108, label8109, label8110
    global label8111, label8112, label8113, label8114, label8115, label8116, label8117, label8118

    label8101 = MainGUI.builder.get_object('label8101')
    label8102 = MainGUI.builder.get_object('label8102')
    label8103 = MainGUI.builder.get_object('label8103')
    label8104 = MainGUI.builder.get_object('label8104')
    label8105 = MainGUI.builder.get_object('label8105')
    label8106 = MainGUI.builder.get_object('label8106')
    label8107 = MainGUI.builder.get_object('label8107')
    label8108 = MainGUI.builder.get_object('label8108')
    label8109 = MainGUI.builder.get_object('label8109')
    label8110 = MainGUI.builder.get_object('label8110')
    label8111 = MainGUI.builder.get_object('label8111')
    label8112 = MainGUI.builder.get_object('label8112')
    label8113 = MainGUI.builder.get_object('label8113')
    label8114 = MainGUI.builder.get_object('label8114')
    label8115 = MainGUI.builder.get_object('label8115')
    label8116 = MainGUI.builder.get_object('label8116')
    label8117 = MainGUI.builder.get_object('label8117')
    label8118 = MainGUI.builder.get_object('label8118')

#!/usr/bin/env python3

# ----------------------------------- Environment Variables - Environment Variables Right Click GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def environment_variables_menu_right_click_import_func():

    global Gtk, Gdk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os


    global EnvironmentVariables, Common
    import EnvironmentVariables, Common


# ----------------------------------- Environment Variables - Environment Variables Right Click Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Environment Variables" tab menu/popover GUI objects and functions/signals) -----------------------------------
def environment_variables_menu_right_click_gui_func():

    # Define builder and get all objects (Environment Variables tab right click menu) from GUI file.
    builder7101m = Gtk.Builder()
    builder7101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/EnvironmentVarMenuRightClick.ui")


    # ********************** Define object names for Environment Variables tab right click menu **********************
    global menu7101m
    global menuitem7104m, menuitem7105m

    # ********************** Get object names for Environment Variables tab right click menu **********************
    menu7101m = builder7101m.get_object('menu7101m')
    menuitem7104m = builder7101m.get_object('menuitem7104m')
    menuitem7105m = builder7101m.get_object('menuitem7105m')


    # ********************** Define object functions for Environment Variables tab right click menu **********************
    def on_menuitem7104m_activate(widget):                                                    # "Copy Variable" item on the right click menu
        selected_variable = Common.selected_variable_value.split("=")[0]
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(selected_variable, -1)
        clipboard.store()

    def on_menuitem7105m_activate(widget):                                                    # "Copy Value" item on the right click menu
        selected_value = '='.join(Common.selected_variable_value.split("=")[1:])              # There may be more than "=" in the VARIABLE=VALUE string. String later than first "=" is get as value.
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(selected_value, -1)
        clipboard.store()

    # ********************** Connect signals to GUI objects for Environment Variables tab right click menu **********************
    menuitem7104m.connect("activate", on_menuitem7104m_activate)
    menuitem7105m.connect("activate", on_menuitem7105m_activate)

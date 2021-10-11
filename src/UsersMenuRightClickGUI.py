#!/usr/bin/env python3

# ----------------------------------- Users - Users Right Click Menu GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def users_menu_right_click_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


# ----------------------------------- Users - Users Right Click Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab menu/popover GUI objects and functions/signals) -----------------------------------
def users_menu_right_click_gui_func():

    # Define builder and get all objects (Users tab right click menu) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersMenuRightClick.ui")

    # ********************** Define object names for Users tab right click menu **********************
    global menu3101m
    global menuitem3101m

    # ********************** Get object names for Users tab right click menu **********************
    menu3101m = builder.get_object('menu3101m')
    menuitem3101m = builder.get_object('menuitem3101m')

    # ********************** Define object functions for Users tab right click menu **********************
    def on_menuitem3101m_activate(widget):                                                    # "Details" item on the right click menu
        if 'UsersDetailsGUI' not in globals():                                                # Check if "UsersDetailsGUI" module is imported. Therefore it is not reimported for every click on "Details" menu item on right click menu if "UsersDetailsGUI" name is in globals().
            global UsersDetails, UsersDetailsGUI
            import UsersDetails, UsersDetailsGUI
            UsersDetailsGUI.users_details_gui_import_function()
            UsersDetailsGUI.users_details_gui_function()
            UsersDetails.users_details_import_func()
        UsersDetailsGUI.window3101w.show()
        UsersDetails.users_details_foreground_thread_run_func()

    # ********************** Connect signals to GUI objects for Users tab right click menu **********************
    menuitem3101m.connect("activate", on_menuitem3101m_activate)

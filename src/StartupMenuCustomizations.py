#!/usr/bin/env python3

# ----------------------------------- Startup - Startup Customizations Menu GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def startup_menu_customizations_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Startup
    import Config, Startup


    # Import gettext module for defining translation texts which will be recognized by gettext application. These lines of code are enough to define this variable if another values are defined in another module (MainGUI) before importing this module.
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    from locale import gettext as _tr


# ----------------------------------- Startup - Startup Customizations Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Startup" tab menu/popover GUI objects and functions/signals) -----------------------------------
def startup_menu_customizations_gui_func():

    # Define builder and get all objects (Startup tab customizations popover) from GUI file.
    builder5101m = Gtk.Builder()
    builder5101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/StartupMenuCustomizations.ui")


    # ********************** Define object names for Startup tab customizations popover **********************
    global popover5101p
    global checkbutton5101p, checkbutton5102p, checkbutton5103p
    global button5101p, button5102p

    # ********************** Get object names for Startup tab customizations popover **********************
    popover5101p = builder5101m.get_object('popover5101p')
    checkbutton5101p = builder5101m.get_object('checkbutton5101p')
    checkbutton5102p = builder5101m.get_object('checkbutton5102p')
    checkbutton5103p = builder5101m.get_object('checkbutton5103p')
    button5101p = builder5101m.get_object('button5101p')
    button5102p = builder5101m.get_object('button5102p')

    # ********************** Define object functions for Startup tab customizations popover Common GUI Objects **********************
    def on_button5101p_clicked(widget):                                                       # "Reset All" button
        Config.config_default_startup_func()
        Config.config_save_func()
        startup_tab_customization_popover_disconnect_signals_func()
        startup_tab_popover_set_gui()
        startup_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Startup tab customizations popover View Tab **********************
    def on_button5102p_clicked(widget):                                                       # "Reset" button
        Config.config_default_startup_row_sort_column_order_func()
        startup_tab_customization_popover_disconnect_signals_func()
        Config.config_save_func()
        startup_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Startup tab customizations popover Add/Remove Columns Tab **********************
    def on_checkbutton5101p_toggled(widget):                                                  # "Name" checkbutton
        startup_add_remove_columns_function()
    def on_checkbutton5102p_toggled(widget):                                                  # "Comment" checkbutton
        startup_add_remove_columns_function()
    def on_checkbutton5103p_toggled(widget):                                                  # "Command (Exec)" checkbutton
        startup_add_remove_columns_function()

    # ********************** Connect signals to GUI objects for Startup tab customizations popover Common GUI Objects **********************
    button5101p.connect("clicked", on_button5101p_clicked)
    button5102p.connect("clicked", on_button5102p_clicked)


    # ********************** Popover settings for Startup tab **********************
    popover5101p.set_relative_to(Startup.button5101)
    popover5101p.set_position(1)



    # ********************** Define function for connecting Startup tab customizations popover GUI signals **********************
    def startup_tab_customization_popover_connect_signals_func():
        # ********************** Connect signals to GUI objects for Startup tab customizations popover Add/Remove Columns Tab **********************
        checkbutton5101p.connect("toggled", on_checkbutton5101p_toggled)
        checkbutton5102p.connect("toggled", on_checkbutton5102p_toggled)
        checkbutton5103p.connect("toggled", on_checkbutton5103p_toggled)


    # ********************** Define function for disconnecting Startup tab customizations popover GUI signals **********************
    def startup_tab_customization_popover_disconnect_signals_func():
        # ********************** Disconnect signals of GUI objects for Startup tab customizations popover Add/Remove Columns Tab **********************
        checkbutton5101p.disconnect_by_func(on_checkbutton5101p_toggled)
        checkbutton5102p.disconnect_by_func(on_checkbutton5102p_toggled)
        checkbutton5103p.disconnect_by_func(on_checkbutton5103p_toggled)


    startup_tab_popover_set_gui()
    startup_tab_customization_popover_connect_signals_func()


# ********************** Set Startup tab customizations popover menu GUI object data/selections appropriate for settings **********************
def startup_tab_popover_set_gui():
    # Set Startup tab customizations popover menu Add/Remove Column tab GUI object data/selections appropriate for settings
    if 0 in Config.startup_treeview_columns_shown:
        checkbutton5101p.set_active(True)
    if 0 not in Config.startup_treeview_columns_shown:
        checkbutton5101p.set_active(False)
    if 1 in Config.startup_treeview_columns_shown:
        checkbutton5102p.set_active(True)
    if 1 not in Config.startup_treeview_columns_shown:
        checkbutton5102p.set_active(False)
    if 2 in Config.startup_treeview_columns_shown:
        checkbutton5103p.set_active(True)
    if 2 not in Config.startup_treeview_columns_shown:
        checkbutton5103p.set_active(False)


# ----------------------------------- Startup - Startup Add/Remove Columns Function (adds/removes storage treeview columns) -----------------------------------
def startup_add_remove_columns_function():

    Config.startup_treeview_columns_shown = []
    if checkbutton5101p.get_active() is True:
        Config.startup_treeview_columns_shown.append(0)
    if checkbutton5102p.get_active() is True:
        Config.startup_treeview_columns_shown.append(1)
    if checkbutton5103p.get_active() is True:
        Config.startup_treeview_columns_shown.append(2)

    Config.config_save_func()

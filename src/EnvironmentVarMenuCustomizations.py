#!/usr/bin/env python3

# ----------------------------------- Environment Variables - Environment Variables Customizations Menu GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def environment_variables_menu_customizations_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, EnvironmentVariables
    from . import Config, EnvironmentVariables


    # Import locale and gettext modules for defining translation texts which will be recognized by gettext application (will be run by programmer externally) and exported into a ".pot" file. 
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    import locale
    from locale import gettext as _tr

    # Define contstants for language translation support
    global application_name
    application_name = "system-monitoring-center"
    translation_files_path = "/usr/share/locale"
    system_current_language = os.environ.get("LANG")

    # Define functions for language translation support
    locale.bindtextdomain(application_name, translation_files_path)
    locale.textdomain(application_name)
    locale.setlocale(locale.LC_ALL, system_current_language)


# ----------------------------------- Environment Variables - Environment Variables Customizations Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Environment Variables" tab menu/popover GUI objects and functions/signals) -----------------------------------
def environment_variables_menu_customizations_gui_func():

    # Define builder and get all objects (Environment Variables tab customizations popover) from GUI file.
    builder7101m = Gtk.Builder()
    builder7101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/EnvironmentVarMenuCustomizations.ui")


    # ********************** Define object names for Environment Variables tab customizations popover **********************
    global popover7101p
    global checkbutton7101p, checkbutton7102p, checkbutton7103p
    global button7101p, button7102p

    # ********************** Get object names for Environment Variables tab customizations popover **********************
    popover7101p = builder7101m.get_object('popover7101p')
    checkbutton7101p = builder7101m.get_object('checkbutton7101p')
    checkbutton7102p = builder7101m.get_object('checkbutton7102p')
    checkbutton7103p = builder7101m.get_object('checkbutton7103p')
    button7101p = builder7101m.get_object('button7101p')
    button7102p = builder7101m.get_object('button7102p')

    # ********************** Define object functions for Environment Variables tab customizations popover Common GUI Objects **********************
    def on_button7101p_clicked(widget):                                                       # "Reset All" button
        Config.config_default_environment_variables_func()
        Config.config_save_func()
        environment_variables_tab_customization_popover_disconnect_signals_func()
        environment_variables_tab_popover_set_gui()
        environment_variables_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Environment Variables tab customizations popover View Tab **********************
    def on_button7102p_clicked(widget):                                                       # "Reset" button
        Config.config_default_environment_variables_row_sort_column_order_func()
        environment_variables_tab_customization_popover_disconnect_signals_func()
        Config.config_save_func()
        environment_variables_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Environment Variables tab customizations popover Add/Remove Columns Tab **********************
    def on_checkbutton7101p_toggled(widget):                                                 # "Variable" checkbutton
        environment_variables_add_remove_columns_function()
    def on_checkbutton7102p_toggled(widget):                                                 # "Value" checkbutton
        environment_variables_add_remove_columns_function()
    def on_checkbutton7103p_toggled(widget):                                                 # "Variable Type" checkbutton
        environment_variables_add_remove_columns_function()

    # ********************** Connect signals to GUI objects for Environment Variables tab customizations popover Common GUI Objects **********************
    button7101p.connect("clicked", on_button7101p_clicked)
    # ********************** Connect signals to GUI objects for Environment Variables tab customizations popover View Tab **********************
    button7102p.connect("clicked", on_button7102p_clicked)


    # ********************** Popover settings for Environment Variables tab **********************
    popover7101p.set_relative_to(EnvironmentVariables.button7101)
    popover7101p.set_position(1)


    # ********************** Define function for connecting Environment Variables tab customizations popover GUI signals **********************
    def environment_variables_tab_customization_popover_connect_signals_func():
        # ********************** Connect signals to GUI objects for Environment Variables tab customizations popover Add/Remove Columns Tab **********************
        checkbutton7101p.connect("toggled", on_checkbutton7101p_toggled)
        checkbutton7102p.connect("toggled", on_checkbutton7102p_toggled)
        checkbutton7103p.connect("toggled", on_checkbutton7103p_toggled)


    # ********************** Define function for disconnecting Environment Variables tab customizations popover GUI signals **********************
    def environment_variables_tab_customization_popover_disconnect_signals_func():
        # ********************** Connect signals to GUI objects for Environment Variables tab customizations popover Add/Remove Columns Tab **********************
        checkbutton7101p.disconnect_by_func(on_checkbutton7101p_toggled)
        checkbutton7102p.disconnect_by_func(on_checkbutton7102p_toggled)
        checkbutton7103p.disconnect_by_func(on_checkbutton7103p_toggled)


    environment_variables_tab_popover_set_gui()
    environment_variables_tab_customization_popover_connect_signals_func()


# ********************** Set Environment Variables tab customizations popover menu GUI object data/selections appropriate for settings **********************
def environment_variables_tab_popover_set_gui():
    # Set Environment Variables tab customizations popover menu Add/Remove Column tab GUI object data/selections appropriate for settings
    if 0 in Config.environment_variables_treeview_columns_shown:
        checkbutton7101p.set_active(True)
    if 0 not in Config.environment_variables_treeview_columns_shown:
        checkbutton7101p.set_active(False)
    if 1 in Config.environment_variables_treeview_columns_shown:
        checkbutton7102p.set_active(True)
    if 1 not in Config.environment_variables_treeview_columns_shown:
        checkbutton7102p.set_active(False)
    if 2 in Config.environment_variables_treeview_columns_shown:
        checkbutton7103p.set_active(True)
    if 2 not in Config.environment_variables_treeview_columns_shown:
        checkbutton7103p.set_active(False)


# ----------------------------------- Environment Variables - Environment Variables Add/Remove Columns Function (adds/removes environment variables treeview columns) -----------------------------------
def environment_variables_add_remove_columns_function():

    Config.environment_variables_treeview_columns_shown = []
    if checkbutton7101p.get_active() is True:
        Config.environment_variables_treeview_columns_shown.append(0)
    if checkbutton7102p.get_active() is True:
        Config.environment_variables_treeview_columns_shown.append(1)
    if checkbutton7103p.get_active() is True:
        Config.environment_variables_treeview_columns_shown.append(2)
    Config.config_save_func()

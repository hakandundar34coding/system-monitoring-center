#!/usr/bin/env python3

# ----------------------------------- Services - Services Customizations Menu GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def services_menu_customizations_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Services
    import Config, Services


# ----------------------------------- Services - Services Customizations Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Services" tab menu/popover GUI objects and functions/signals) -----------------------------------
def services_menu_customizations_gui_func():

    # Define builder and get all objects (Services tab customizations popover) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ServicesMenuCustomizations.ui")


    # ********************** Define object names for Services tab customizations popover **********************
    global popover6101p
    global checkbutton6101p, checkbutton6102p, checkbutton6103p, checkbutton6104p, checkbutton6105p, checkbutton6106p
    global checkbutton6107p, checkbutton6108p
    global button6101p, button6102p

    # ********************** Get object names for Services tab customizations popover **********************
    popover6101p = builder.get_object('popover6101p')
    checkbutton6101p = builder.get_object('checkbutton6101p')
    checkbutton6102p = builder.get_object('checkbutton6102p')
    checkbutton6103p = builder.get_object('checkbutton6103p')
    checkbutton6104p = builder.get_object('checkbutton6104p')
    checkbutton6105p = builder.get_object('checkbutton6105p')
    checkbutton6106p = builder.get_object('checkbutton6106p')
    checkbutton6107p = builder.get_object('checkbutton6107p')
    checkbutton6108p = builder.get_object('checkbutton6108p')
    button6101p = builder.get_object('button6101p')
    button6102p = builder.get_object('button6102p')

    # ********************** Define object functions for Services tab customizations popover Common GUI Objects **********************
    def on_button6101p_clicked(widget):                                                       # "Reset All" button
        Config.config_default_services_func()
        Config.config_save_func()
        services_tab_customization_popover_disconnect_signals_func()
        services_tab_popover_set_gui()
        services_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Services tab customizations popover View Tab **********************
    def on_button6102p_clicked(widget):                                                       # "Reset" button
        Config.config_default_services_row_sort_column_order_func()
        services_tab_customization_popover_disconnect_signals_func()
        Config.config_save_func()
        services_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Services tab customizations popover Add/Remove Columns Tab **********************
    def on_add_remove_checkbuttons_toggled(widget):                                           # "Service Name, State, Main PID, etc." checkbuttons
        services_add_remove_columns_function()

    # ********************** Connect signals to GUI objects for Services tab customizations popover Common GUI Objects **********************
    button6101p.connect("clicked", on_button6101p_clicked)
    # ********************** Connect signals to GUI objects for Services tab customizations popover View Tab **********************
    button6102p.connect("clicked", on_button6102p_clicked)


    # ********************** Popover settings for Services tab customizations menu **********************
    popover6101p.set_relative_to(Services.button6101)
    popover6101p.set_position(1)


    # ********************** Define function for connecting Services tab customizations popover GUI signals **********************
    def services_tab_customization_popover_connect_signals_func():
        # ********************** Connect signals to GUI objects for Services tab customizations popover Add/Remove Columns Tab **********************
        checkbutton6101p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton6102p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton6103p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton6104p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton6105p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton6106p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton6107p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton6108p.connect("toggled", on_add_remove_checkbuttons_toggled)


    # ********************** Define function for disconnecting Services tab customizations popover GUI signals **********************
    def services_tab_customization_popover_disconnect_signals_func():
        # ********************** Connect signals to GUI objects for Services tab customizations popover Add/Remove Columns Tab **********************
        checkbutton6101p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton6102p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton6103p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton6104p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton6105p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton6106p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton6107p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton6108p.disconnect_by_func(on_add_remove_checkbuttons_toggled)


    services_tab_popover_set_gui()
    services_tab_customization_popover_connect_signals_func()


# ********************** Set Services tab customizations popover menu GUI object data/selections appropriate for settings **********************
def services_tab_popover_set_gui():
    # Set Services tab customizations popover menu Add/Remove Column tab GUI object data/selections appropriate for settings
    if 0 in Config.services_treeview_columns_shown:
        checkbutton6101p.set_active(True)
    if 0 not in Config.services_treeview_columns_shown:
        checkbutton6101p.set_active(False)
    if 1 in Config.services_treeview_columns_shown:
        checkbutton6102p.set_active(True)
    if 1 not in Config.services_treeview_columns_shown:
        checkbutton6102p.set_active(False)
    if 2 in Config.services_treeview_columns_shown:
        checkbutton6103p.set_active(True)
    if 2 not in Config.services_treeview_columns_shown:
        checkbutton6103p.set_active(False)
    if 3 in Config.services_treeview_columns_shown:
        checkbutton6104p.set_active(True)
    if 3 not in Config.services_treeview_columns_shown:
        checkbutton6104p.set_active(False)
    if 4 in Config.services_treeview_columns_shown:
        checkbutton6105p.set_active(True)
    if 4 not in Config.services_treeview_columns_shown:
        checkbutton6105p.set_active(False)
    if 5 in Config.services_treeview_columns_shown:
        checkbutton6106p.set_active(True)
    if 5 not in Config.services_treeview_columns_shown:
        checkbutton6106p.set_active(False)
    if 6 in Config.services_treeview_columns_shown:
        checkbutton6107p.set_active(True)
    if 6 not in Config.services_treeview_columns_shown:
        checkbutton6107p.set_active(False)
    if 7 in Config.services_treeview_columns_shown:
        checkbutton6108p.set_active(True)
    if 7 not in Config.services_treeview_columns_shown:
        checkbutton6108p.set_active(False)


# ----------------------------------- Services - Services Add/Remove Columns Function (adds/removes services treeview columns) -----------------------------------
def services_add_remove_columns_function():

    Config.services_treeview_columns_shown = []
    if checkbutton6101p.get_active() is True:
        Config.services_treeview_columns_shown.append(0)
    if checkbutton6102p.get_active() is True:
        Config.services_treeview_columns_shown.append(1)
    if checkbutton6103p.get_active() is True:
        Config.services_treeview_columns_shown.append(2)
    if checkbutton6104p.get_active() is True:
        Config.services_treeview_columns_shown.append(3)
    if checkbutton6105p.get_active() is True:
        Config.services_treeview_columns_shown.append(4)
    if checkbutton6106p.get_active() is True:
        Config.services_treeview_columns_shown.append(5)
    if checkbutton6107p.get_active() is True:
        Config.services_treeview_columns_shown.append(6)
    if checkbutton6108p.get_active() is True:
        Config.services_treeview_columns_shown.append(7)
    Config.config_save_func()

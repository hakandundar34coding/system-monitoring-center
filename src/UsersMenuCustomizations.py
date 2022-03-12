#!/usr/bin/env python3

# ----------------------------------- Users - Users Customizations Menu GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def users_menu_customizations_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Users
    import Config, Users


# ----------------------------------- Users - Users Customizations Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab menu/popover GUI objects and functions/signals) -----------------------------------
def users_menu_customizations_gui_func():

    # Define builder and get all objects (Users tab customizations popover) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersMenuCustomizations.ui")


    # ********************** Define object names for Users tab customizations popover **********************
    global popover3101p
    global button3101p, button3102p
    global checkbutton3101p, checkbutton3102p, checkbutton3103p, checkbutton3104p, checkbutton3105p, checkbutton3106p, checkbutton3107p
    global checkbutton3108p, checkbutton3109p, checkbutton3110p, checkbutton3111p, checkbutton3112p

    # ********************** Get object names for Users tab customizations popover **********************
    popover3101p = builder.get_object('popover3101p')
    button3101p = builder.get_object('button3101p')
    button3102p = builder.get_object('button3102p')
    checkbutton3101p = builder.get_object('checkbutton3101p')
    checkbutton3102p = builder.get_object('checkbutton3102p')
    checkbutton3103p = builder.get_object('checkbutton3103p')
    checkbutton3104p = builder.get_object('checkbutton3104p')
    checkbutton3105p = builder.get_object('checkbutton3105p')
    checkbutton3106p = builder.get_object('checkbutton3106p')
    checkbutton3107p = builder.get_object('checkbutton3107p')
    checkbutton3108p = builder.get_object('checkbutton3108p')
    checkbutton3109p = builder.get_object('checkbutton3109p')
    checkbutton3110p = builder.get_object('checkbutton3110p')
    checkbutton3111p = builder.get_object('checkbutton3111p')
    checkbutton3112p = builder.get_object('checkbutton3112p')

    # ********************** Define object functions for Users tab customizations popover Common GUI Objects **********************
    def on_button3101p_clicked(widget):                                                       # "Reset All" button
        Config.config_default_users_func()
        Config.config_save_func()
        users_tab_customization_popover_disconnect_signals_func()
        users_tab_popover_set_gui()
        users_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Users tab customizations popover View Tab **********************
    def on_button3102p_clicked(widget):                                                       # "Reset" button
        Config.config_default_users_row_sort_column_order_func()
        users_tab_customization_popover_disconnect_signals_func()
        Config.config_save_func()
        users_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Users tab customizations popover Add/Remove Columns Tab **********************
    def on_add_remove_checkbuttons_toggled(widget):                                           # "User Name, Full Name, UID, etc." checkbuttons
        users_add_remove_columns_function()

    # ********************** Connect signals to GUI objects for Users tab customizations popover Common GUI Objects **********************
    button3101p.connect("clicked", on_button3101p_clicked)
    # ********************** Connect signals to GUI objects for Users tab customizations popover View Tab **********************
    button3102p.connect("clicked", on_button3102p_clicked)


    # ********************** Popover settings for Users tab **********************
    popover3101p.set_relative_to(Users.button3101)
    popover3101p.set_position(1)


    # ********************** Define function for connecting Users tab customizations popover GUI signals **********************
    def users_tab_customization_popover_connect_signals_func():
    # ********************** Connect signals to GUI objects for Users tab customizations popover Add/Remove Columns Tab **********************
        checkbutton3101p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton3102p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton3103p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton3104p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton3105p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton3106p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton3107p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton3108p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton3109p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton3110p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton3111p.connect("toggled", on_add_remove_checkbuttons_toggled)
        checkbutton3112p.connect("toggled", on_add_remove_checkbuttons_toggled)


    # ********************** Define function for disconnecting Users tab customizations popover GUI signals **********************
    def users_tab_customization_popover_disconnect_signals_func():
    # ********************** Disconnect signals of GUI objects for Users tab customizations popover Add/Remove Columns Tab **********************
        checkbutton3101p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton3102p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton3103p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton3104p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton3105p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton3106p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton3107p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton3108p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton3109p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton3110p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton3111p.disconnect_by_func(on_add_remove_checkbuttons_toggled)
        checkbutton3112p.disconnect_by_func(on_add_remove_checkbuttons_toggled)


    users_tab_popover_set_gui()
    users_tab_customization_popover_connect_signals_func()


# ********************** Set Users tab customizations popover menu GUI object data/selections appropriate for settings **********************
def users_tab_popover_set_gui():
    # Set Users tab customizations popover menu Add/Remove Column tab GUI object data/selections appropriate for settings
    if 0 in Config.users_treeview_columns_shown:
        checkbutton3101p.set_active(True)
    if 0 not in Config.users_treeview_columns_shown:
        checkbutton3101p.set_active(False)
    if 1 in Config.users_treeview_columns_shown:
        checkbutton3102p.set_active(True)
    if 1 not in Config.users_treeview_columns_shown:
        checkbutton3102p.set_active(False)
    if 2 in Config.users_treeview_columns_shown:
        checkbutton3103p.set_active(True)
    if 2 not in Config.users_treeview_columns_shown:
        checkbutton3103p.set_active(False)
    if 3 in Config.users_treeview_columns_shown:
        checkbutton3104p.set_active(True)
    if 3 not in Config.users_treeview_columns_shown:
        checkbutton3104p.set_active(False)
    if 4 in Config.users_treeview_columns_shown:
        checkbutton3105p.set_active(True)
    if 4 not in Config.users_treeview_columns_shown:
        checkbutton3105p.set_active(False)
    if 5 in Config.users_treeview_columns_shown:
        checkbutton3106p.set_active(True)
    if 5 not in Config.users_treeview_columns_shown:
        checkbutton3106p.set_active(False)
    if 6 in Config.users_treeview_columns_shown:
        checkbutton3107p.set_active(True)
    if 6 not in Config.users_treeview_columns_shown:
        checkbutton3107p.set_active(False)
    if 7 in Config.users_treeview_columns_shown:
        checkbutton3108p.set_active(True)
    if 7 not in Config.users_treeview_columns_shown:
        checkbutton3108p.set_active(False)
    if 8 in Config.users_treeview_columns_shown:
        checkbutton3109p.set_active(True)
    if 8 not in Config.users_treeview_columns_shown:
        checkbutton3109p.set_active(False)
    if 11 in Config.users_treeview_columns_shown:
        checkbutton3110p.set_active(True)
    if 11 not in Config.users_treeview_columns_shown:
        checkbutton3110p.set_active(False)
    if 12 in Config.users_treeview_columns_shown:
        checkbutton3111p.set_active(True)
    if 12 not in Config.users_treeview_columns_shown:
        checkbutton3111p.set_active(False)
    if 13 in Config.users_treeview_columns_shown:
        checkbutton3112p.set_active(True)
    if 13 not in Config.users_treeview_columns_shown:
        checkbutton3112p.set_active(False)


# ----------------------------------- Users - Users Add/Remove Columns Function (adds/removes users treeview columns) -----------------------------------
def users_add_remove_columns_function():

    # Add/Remove treeview columns
    Config.users_treeview_columns_shown = []
    if checkbutton3101p.get_active() is True:
        Config.users_treeview_columns_shown.append(0)
    if checkbutton3102p.get_active() is True:
        Config.users_treeview_columns_shown.append(1)
    if checkbutton3103p.get_active() is True:
        Config.users_treeview_columns_shown.append(2)
    if checkbutton3104p.get_active() is True:
        Config.users_treeview_columns_shown.append(3)
    if checkbutton3105p.get_active() is True:
        Config.users_treeview_columns_shown.append(4)
    if checkbutton3106p.get_active() is True:
        Config.users_treeview_columns_shown.append(5)
    if checkbutton3107p.get_active() is True:
        Config.users_treeview_columns_shown.append(6)
    if checkbutton3108p.get_active() is True:
        Config.users_treeview_columns_shown.append(7)
    if checkbutton3109p.get_active() is True:
        Config.users_treeview_columns_shown.append(8)
    if checkbutton3110p.get_active() is True:
        Config.users_treeview_columns_shown.append(11)
    if checkbutton3111p.get_active() is True:
        Config.users_treeview_columns_shown.append(12)
    if checkbutton3112p.get_active() is True:
        Config.users_treeview_columns_shown.append(13)
    Config.config_save_func()

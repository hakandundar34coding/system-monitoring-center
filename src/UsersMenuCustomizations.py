#!/usr/bin/env python3

# ----------------------------------- Users - Users Customizations Menu GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def users_menu_customizations_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Users
    from . import Config, Users


# ----------------------------------- Users - Users Customizations Menu GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab menu/popover GUI objects and functions/signals) -----------------------------------
def users_menu_customizations_gui_func():

    # Define builder and get all objects (Users tab customizations popover) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/ui/UsersMenuCustomizations.ui")


    # ********************** Define object names for Users tab customizations popover **********************
    global popover3101p
    global button3101p, button3102p
    global checkbutton3101p, checkbutton3102p, checkbutton3103p, checkbutton3104p, checkbutton3105p, checkbutton3106p, checkbutton3107p
    global checkbutton3108p, checkbutton3109p, checkbutton3110p, checkbutton3111p, checkbutton3112p, checkbutton3113p, checkbutton3114p
    global combobox3101p, combobox3102p, combobox3103p

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
    checkbutton3113p = builder.get_object('checkbutton3113p')
    checkbutton3114p = builder.get_object('checkbutton3114p')
    combobox3101p = builder.get_object('combobox3101p')
    combobox3102p = builder.get_object('combobox3102p')
    combobox3103p = builder.get_object('combobox3103p')

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
    def on_checkbutton3101p_toggled(widget):                                                  # "User Name" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3102p_toggled(widget):                                                  # "Full Name" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3103p_toggled(widget):                                                  # "Logged In" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3104p_toggled(widget):                                                  # "UID" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3105p_toggled(widget):                                                  # "GID" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3106p_toggled(widget):                                                  # "Processes" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3107p_toggled(widget):                                                  # "Home Dir." checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3108p_toggled(widget):                                                  # "Group" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3109p_toggled(widget):                                                  # "Terminal" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3110p_toggled(widget):                                                  # "Last Login" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3111p_toggled(widget):                                                  # "Last Failed Login" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3112p_toggled(widget):                                                  # "Started" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3113p_toggled(widget):                                                  # "CPU%" checkbutton
        users_add_remove_columns_function()
    def on_checkbutton3114p_toggled(widget):                                                  # "RAM (RSS)" checkbutton
        users_add_remove_columns_function()

    # ********************** Define object functions for Users tab customizations popover Precision/Data Tab **********************
    def on_combobox3101p_changed(widget):                                                     # "CPU Percent" combobox
        Config.users_cpu_usage_percent_precision = Config.number_precision_list[combobox3101p.get_active()][2]
        Config.config_save_func()

    def on_combobox3102p_changed(widget):                                                     # "RAM & Swap Usage" combobox for "precision"
        Config.users_ram_swap_data_precision = Config.number_precision_list[combobox1202p.get_active()][2]
        Config.config_save_func()

    def on_combobox3103p_changed(widget):                                                     # "RAM & Swap Usage" combobox for "data unit"
        Config.users_ram_swap_data_unit = Config.data_unit_list[combobox3103p.get_active()][2]
        Config.config_save_func()

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
        checkbutton3101p.connect("toggled", on_checkbutton3101p_toggled)
        checkbutton3102p.connect("toggled", on_checkbutton3102p_toggled)
        checkbutton3103p.connect("toggled", on_checkbutton3103p_toggled)
        checkbutton3104p.connect("toggled", on_checkbutton3104p_toggled)
        checkbutton3105p.connect("toggled", on_checkbutton3105p_toggled)
        checkbutton3106p.connect("toggled", on_checkbutton3106p_toggled)
        checkbutton3107p.connect("toggled", on_checkbutton3107p_toggled)
        checkbutton3108p.connect("toggled", on_checkbutton3108p_toggled)
        checkbutton3109p.connect("toggled", on_checkbutton3109p_toggled)
        checkbutton3110p.connect("toggled", on_checkbutton3110p_toggled)
        checkbutton3111p.connect("toggled", on_checkbutton3111p_toggled)
        checkbutton3112p.connect("toggled", on_checkbutton3112p_toggled)
        checkbutton3113p.connect("toggled", on_checkbutton3113p_toggled)
        checkbutton3114p.connect("toggled", on_checkbutton3114p_toggled)
        # ********************** Connect signals to GUI objects for Users tab customizations popover Precision/Data Units Tab **********************
        combobox3101p.connect("changed", on_combobox3101p_changed)
        combobox3102p.connect("changed", on_combobox3102p_changed)
        combobox3103p.connect("changed", on_combobox3103p_changed)


    # ********************** Define function for disconnecting Users tab customizations popover GUI signals **********************
    def users_tab_customization_popover_disconnect_signals_func():
    # ********************** Disconnect signals of GUI objects for Users tab customizations popover Add/Remove Columns Tab **********************
        checkbutton3101p.disconnect_by_func(on_checkbutton3101p_toggled)
        checkbutton3102p.disconnect_by_func(on_checkbutton3102p_toggled)
        checkbutton3103p.disconnect_by_func(on_checkbutton3103p_toggled)
        checkbutton3104p.disconnect_by_func(on_checkbutton3104p_toggled)
        checkbutton3105p.disconnect_by_func(on_checkbutton3105p_toggled)
        checkbutton3106p.disconnect_by_func(on_checkbutton3106p_toggled)
        checkbutton3107p.disconnect_by_func(on_checkbutton3107p_toggled)
        checkbutton3108p.disconnect_by_func(on_checkbutton3108p_toggled)
        checkbutton3109p.disconnect_by_func(on_checkbutton3109p_toggled)
        checkbutton3110p.disconnect_by_func(on_checkbutton3110p_toggled)
        checkbutton3111p.disconnect_by_func(on_checkbutton3111p_toggled)
        checkbutton3112p.disconnect_by_func(on_checkbutton3112p_toggled)
        checkbutton3113p.disconnect_by_func(on_checkbutton3113p_toggled)
        checkbutton3114p.disconnect_by_func(on_checkbutton3114p_toggled)
        # ********************** Disconnect signals of GUI objects for Users tab customizations popover Precision/Data Units Tab **********************
        combobox3101p.disconnect_by_func(on_combobox3101p_changed)
        combobox3102p.disconnect_by_func(on_combobox3102p_changed)
        combobox3103p.disconnect_by_func(on_combobox3103p_changed)


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
    if 9 in Config.users_treeview_columns_shown:
        checkbutton3110p.set_active(True)
    if 9 not in Config.users_treeview_columns_shown:
        checkbutton3110p.set_active(False)
    if 10 in Config.users_treeview_columns_shown:
        checkbutton3111p.set_active(True)
    if 10 not in Config.users_treeview_columns_shown:
        checkbutton3111p.set_active(False)
    if 11 in Config.users_treeview_columns_shown:
        checkbutton3112p.set_active(True)
    if 11 not in Config.users_treeview_columns_shown:
        checkbutton3112p.set_active(False)
    if 12 in Config.users_treeview_columns_shown:
        checkbutton3113p.set_active(True)
    if 12 not in Config.users_treeview_columns_shown:
        checkbutton3113p.set_active(False)
    if 13 in Config.users_treeview_columns_shown:
        checkbutton3114p.set_active(True)
    if 13 not in Config.users_treeview_columns_shown:
        checkbutton3114p.set_active(False)
    # Set Users tab customizations popover menu Precision/Data Units tab GUI object data/selections appropriate for settings
    # Add CPU usage percent data into combobox
    if "liststore3101p" not in globals():                                                 # Check if "liststore3101p" is in global variables list (Python's own list = globals()) in order to prevent readdition of items to the listbox and combobox.
        global liststore3101p
        liststore3101p = Gtk.ListStore()
        liststore3101p.set_column_types([str, int])
        combobox3101p.set_model(liststore3101p)
        renderer_text = Gtk.CellRendererText()
        combobox3101p.pack_start(renderer_text, True)
        combobox3101p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore3101p.append([data[1], data[2]])
    combobox3101p.set_active(Config.users_cpu_usage_percent_precision)
    # Add RAM usage data precision data into combobox
    if "liststore3102p" not in globals():
        global liststore3102p
        liststore3102p = Gtk.ListStore()
        liststore3102p.set_column_types([str, int])
        combobox3102p.set_model(liststore3102p)
        renderer_text = Gtk.CellRendererText()
        combobox3102p.pack_start(renderer_text, True)
        combobox3102p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore3102p.append([data[1], data[2]])
    combobox3102p.set_active(Config.users_ram_swap_data_precision)
    # Add RAM usage data unit data into combobox
    if "liststore3103p" not in globals():
        global liststore3103p
        liststore3103p = Gtk.ListStore()
        liststore3103p.set_column_types([str, int])
        combobox3103p.set_model(liststore3103p)
        renderer_text = Gtk.CellRendererText()
        combobox3103p.pack_start(renderer_text, True)
        combobox3103p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_unit_list:
            liststore3103p.append([data[1], data[2]])
    for data_list in Config.data_unit_list:
        if data_list[2] == Config.users_ram_swap_data_unit:      
            combobox3103p.set_active(data_list[0])


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
        Config.users_treeview_columns_shown.append(9)
    if checkbutton3111p.get_active() is True:
        Config.users_treeview_columns_shown.append(10)
    if checkbutton3112p.get_active() is True:
        Config.users_treeview_columns_shown.append(11)
    if checkbutton3113p.get_active() is True:
        Config.users_treeview_columns_shown.append(12)
    if checkbutton3114p.get_active() is True:
        Config.users_treeview_columns_shown.append(13)
    Config.config_save_func()

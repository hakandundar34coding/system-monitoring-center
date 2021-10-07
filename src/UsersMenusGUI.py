#!/usr/bin/env python3

# ----------------------------------- Users - Users Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def users_menus_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config, Users, UsersGUI
    import Config, Users, UsersGUI


# ----------------------------------- Users - Users Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab menu/popover GUI objects and functions/signals) -----------------------------------
def users_menus_gui_func():

    # Define builder and get all objects (Users tab customizations popover, Users tab search customizations popover) from GUI file.
    builder3101m = Gtk.Builder()
    builder3101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersMenus.ui")

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Users tab customizations popover
    # ********************** Define object names for Users tab right click menu **********************
    global menu3101m
    global menuitem3101m

    # ********************** Get object names for Users tab right click menu **********************
    menu3101m = builder3101m.get_object('menu3101m')
    menuitem3101m = builder3101m.get_object('menuitem3101m')

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
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Users tab customizations popover
    # ********************** Define object names for Users tab customizations popover **********************
    global popover3101p
    global button3101p, button3102p
    global checkbutton3101p, checkbutton3102p, checkbutton3103p, checkbutton3104p, checkbutton3105p, checkbutton3106p, checkbutton3107p
    global checkbutton3108p, checkbutton3109p, checkbutton3110p, checkbutton3111p, checkbutton3112p, checkbutton3113p, checkbutton3114p
    global combobox3101p, combobox3102p, combobox3103p

    # ********************** Get object names for Users tab customizations popover **********************
    popover3101p = builder3101m.get_object('popover3101p')
    button3101p = builder3101m.get_object('button3101p')
    button3102p = builder3101m.get_object('button3102p')
    checkbutton3101p = builder3101m.get_object('checkbutton3101p')
    checkbutton3102p = builder3101m.get_object('checkbutton3102p')
    checkbutton3103p = builder3101m.get_object('checkbutton3103p')
    checkbutton3104p = builder3101m.get_object('checkbutton3104p')
    checkbutton3105p = builder3101m.get_object('checkbutton3105p')
    checkbutton3106p = builder3101m.get_object('checkbutton3106p')
    checkbutton3107p = builder3101m.get_object('checkbutton3107p')
    checkbutton3108p = builder3101m.get_object('checkbutton3108p')
    checkbutton3109p = builder3101m.get_object('checkbutton3109p')
    checkbutton3110p = builder3101m.get_object('checkbutton3110p')
    checkbutton3111p = builder3101m.get_object('checkbutton3111p')
    checkbutton3112p = builder3101m.get_object('checkbutton3112p')
    checkbutton3113p = builder3101m.get_object('checkbutton3113p')
    checkbutton3114p = builder3101m.get_object('checkbutton3114p')
    combobox3101p = builder3101m.get_object('combobox3101p')
    combobox3102p = builder3101m.get_object('combobox3102p')
    combobox3103p = builder3101m.get_object('combobox3103p')

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
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Users tab search customizations popover
    # ********************** Define object names for Users tab search customizations popover **********************
    global popover3101p2
    global radiobutton3101p2, radiobutton3102p2, radiobutton3103p2, radiobutton3104p2, radiobutton3105p2
    global checkbutton3101p2, checkbutton3102p2, checkbutton3103p2

    # ********************** Get object names for Users tab search customizations popover **********************
    popover3101p2 = builder3101m.get_object('popover3101p2')
    radiobutton3101p2 = builder3101m.get_object('radiobutton3101p2')
    radiobutton3102p2 = builder3101m.get_object('radiobutton3102p2')
    radiobutton3103p2 = builder3101m.get_object('radiobutton3103p2')
    radiobutton3104p2 = builder3101m.get_object('radiobutton3104p2')
    radiobutton3105p2 = builder3101m.get_object('radiobutton3105p2')
    checkbutton3101p2 = builder3101m.get_object('checkbutton3101p2')
    checkbutton3102p2 = builder3101m.get_object('checkbutton3102p2')
    checkbutton3103p2 = builder3101m.get_object('checkbutton3103p2')

    # ********************** Define object functions for Users tab search customizations popover **********************
    def on_radiobutton3101p2_toggled(widget):                                                 # "Name" radiobutton
        if radiobutton3101p2.get_active() == True:
            Users.users_treeview_filter_search_func()

    def on_radiobutton3102p2_toggled(widget):                                                 # "Full Name" radiobutton
        if radiobutton3102p2.get_active() == True:
            Users.users_treeview_filter_search_func()

    def on_radiobutton3103p2_toggled(widget):                                                 # "Group" radiobutton
        if radiobutton3103p2.get_active() == True:
            Users.users_treeview_filter_search_func()

    def on_radiobutton3104p2_toggled(widget):                                                 # "UID" radiobutton
        if radiobutton3104p2.get_active() == True:
            Users.users_treeview_filter_search_func()

    def on_radiobutton3105p2_toggled(widget):                                                 # "GID" radiobutton
        if radiobutton3105p2.get_active() == True:
            Users.users_treeview_filter_search_func()

    def on_checkbutton3101p2_toggled(widget):                                                 # "All users" checkbutton
            users_popover_checkbutton_behavior_func(checkbutton3101p2)

    def on_checkbutton3102p2_toggled(widget):                                                 # "Users logged in" checkbutton
            users_popover_checkbutton_behavior_func(checkbutton3102p2)

    def on_checkbutton3103p2_toggled(widget):                                                 # "Users logged out" checkbutton
            users_popover_checkbutton_behavior_func(checkbutton3103p2)

    # ********************** Connect signals to GUI objects for Users tab search customizations popover **********************
    radiobutton3101p2.connect("toggled", on_radiobutton3101p2_toggled)
    radiobutton3102p2.connect("toggled", on_radiobutton3102p2_toggled)
    radiobutton3103p2.connect("toggled", on_radiobutton3103p2_toggled)
    radiobutton3104p2.connect("toggled", on_radiobutton3104p2_toggled)
    radiobutton3105p2.connect("toggled", on_radiobutton3105p2_toggled)
    global checkbutton3101p2_handler_id, checkbutton3102p2_handler_id, checkbutton3103p2_handler_id
    checkbutton3101p2_handler_id = checkbutton3101p2.connect("toggled", on_checkbutton3101p2_toggled)    # Handler ids are defined in order to block signals of the checkbuttons. Because activating and deactivating of this checkbuttons affects behaviors of each others and this would cause lock when active state of these are changed.
    checkbutton3102p2_handler_id = checkbutton3102p2.connect("toggled", on_checkbutton3102p2_toggled)
    checkbutton3103p2_handler_id = checkbutton3103p2.connect("toggled", on_checkbutton3103p2_toggled)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # ********************** Popover settings for Users tab **********************
    popover3101p.set_relative_to(UsersGUI.button3101)
    popover3101p.set_position(1)
    # ********************** Popover settings for Users tab search customizations **********************
    popover3101p2.set_relative_to(UsersGUI.button3102)
    popover3101p2.set_position(3)



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


# ----------------------------------- Users - User Popover Checkbuttons Behavior Function (sets a counter constant in order to avoid repetitive signal operations on checkbutton toggles) -----------------------------------
def users_popover_checkbutton_behavior_func(caller_checkbutton):

    checkbutton_list = [checkbutton3101p2, checkbutton3102p2, checkbutton3103p2]
    select_all_checkbutton = checkbutton_list[0]
    sub_checkbutton_list = checkbutton_list
    sub_checkbutton_list.remove(select_all_checkbutton)
    checkbutton_active_state_list = []
    for checkbutton in sub_checkbutton_list:
        if checkbutton != select_all_checkbutton:
            checkbutton_active_state_list.append(checkbutton.get_active())

    with checkbutton3101p2.handler_block(checkbutton3101p2_handler_id) as p1, checkbutton3102p2.handler_block(checkbutton3102p2_handler_id) as p2, checkbutton3103p2.handler_block(checkbutton3103p2_handler_id) as p3:
        if caller_checkbutton != select_all_checkbutton and caller_checkbutton.get_active() == False:
            if True not in checkbutton_active_state_list:
                caller_checkbutton.set_active(True)
                checkbutton_active_state_list[sub_checkbutton_list.index(caller_checkbutton)] = True
        if caller_checkbutton != select_all_checkbutton and False not in checkbutton_active_state_list:
            select_all_checkbutton.set_active(True)
            select_all_checkbutton.set_inconsistent(False)
        if caller_checkbutton != select_all_checkbutton and False in checkbutton_active_state_list:
            select_all_checkbutton.set_active(False)
            select_all_checkbutton.set_inconsistent(True)
        if select_all_checkbutton.get_active() == True:
            select_all_checkbutton.set_inconsistent(False)
            for i, checkbutton in enumerate(sub_checkbutton_list):
                checkbutton.set_active(True)
                checkbutton_active_state_list[i] = True
        if select_all_checkbutton.get_active() == False:
            if False not in checkbutton_active_state_list:
                select_all_checkbutton.set_active(True)

    if UsersGUI.searchentry3101.get_text() != "":                                             # Search filter updating is prevented, if any text is not inserted into searchentry. This is due to prevent user frustration because of the temperature/fan only buttons above the treeview.
        Users.users_treeview_filter_search_func()


# ----------------------------------- Users - Users Add/Remove Columns Function (adds/removes users treeview columns) -----------------------------------
def users_add_remove_columns_function():

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

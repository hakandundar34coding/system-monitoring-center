#!/usr/bin/env python3

# ----------------------------------- Environment Variables - Environment Variables Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def environment_variables_menus_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global Config, EnvironmentVariables, EnvironmentVariablesGUI
    import Config, EnvironmentVariables, EnvironmentVariablesGUI


# ----------------------------------- Environment Variables - Environment Variables Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Environment Variables" tab menu/popover GUI objects and functions/signals) -----------------------------------
def environment_variables_menus_gui_func():

    # Define builder and get all objects (Environment Variables tab right click menu, Environment Variables tab customizations popover, Environment Variables tab search customizations popover) from GUI file.
    builder7101m = Gtk.Builder()
    builder7101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/EnvironmentVariablesMenus.glade")


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Environment Variables tab right click menu
    # ********************** Define object names for Environment Variables tab right click menu **********************
    global menu7101m
    global menuitem7101m, menuitem7102m, menuitem7103m, menuitem7104m, menuitem7105m

    # ********************** Get object names for Environment Variables tab right click menu **********************
    menu7101m = builder7101m.get_object('menu7101m')
    menuitem7101m = builder7101m.get_object('menuitem7101m')
    menuitem7102m = builder7101m.get_object('menuitem7102m')
    menuitem7103m = builder7101m.get_object('menuitem7103m')
    menuitem7104m = builder7101m.get_object('menuitem7104m')
    menuitem7105m = builder7101m.get_object('menuitem7105m')

    # ********************** Define object functions for Environment Variables tab right click menu **********************
    def on_menu7101m_show(widget):
        pass

    def on_menuitem7101m_activate(widget):                                                    # "Edit" item on the right click menu
        return
        variable_name = EnvironmentVariablesGUI.selected_variable_name

    def on_menuitem7102m_activate(widget):                                                    # "Add Environment Variable For Current User" item on the right click menu
        return
        variable_name = EnvironmentVariablesGUI.selected_variable_name
        subprocess.check_output("echo 'export AA6=1' >> ~/.bashrc; source ~/.bashrc", shell=True, executable='/bin/bash').strip().decode()

    def on_menuitem7103m_activate(widget):                                                    # "Add Environment Variable For All Users" item on the right click menu
        return
        variable_name = EnvironmentVariablesGUI.selected_variable_name
        subprocess.check_output("echo 'export AA7=1' | pkexec tee -a /etc/profile.d/environment_variables_for_all_users.sh", shell=True, executable='/bin/bash').strip().decode()

    def on_menuitem7104m_activate(widget):                                                    # "Set Environment Variable For All Users" item on the right click menu
        return
        variable_name = EnvironmentVariablesGUI.selected_variable_name
        subprocess.check_output("sed -i '/export AA6=/d' ~/.bashrc", shell=True, executable='/bin/bash').strip().decode()

    def on_menuitem7105m_activate(widget):                                                    # "Set Environment Variable For Current User Only" item on the right click menu
        return
        variable_name = EnvironmentVariablesGUI.selected_variable_name
        subprocess.check_output("pkexec sed -i '/export AA7=/d' /etc/profile.d/environment_variables_for_all_users.sh", shell=True, executable='/bin/bash').strip().decode()

    # ********************** Connect signals to GUI objects for Environment Variables tab right click menu **********************
    menu7101m.connect("show", on_menu7101m_show)
    menuitem7101m.connect("activate", on_menuitem7101m_activate)
    menuitem7102m.connect("activate", on_menuitem7102m_activate)
    menuitem7103m.connect("activate", on_menuitem7103m_activate)
    menuitem7104m.connect("activate", on_menuitem7104m_activate)
    menuitem7105m.connect("activate", on_menuitem7105m_activate)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Environment Variables tab customizations popover
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
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Environment Variables tab search customizations popover
    # ********************** Define object names for Environment Variables tab search customizations popover **********************
    global popover7101p2
    global radiobutton7101p2, radiobutton7102p2
    global checkbutton7101p2, checkbutton7102p2, checkbutton7103p2

    # ********************** Get object names for Environment Variables tab search customizations popover **********************
    popover7101p2 = builder7101m.get_object('popover7101p2')
    radiobutton7101p2 = builder7101m.get_object('radiobutton7101p2')
    radiobutton7102p2 = builder7101m.get_object('radiobutton7102p2')
    checkbutton7101p2 = builder7101m.get_object('checkbutton7101p2')
    checkbutton7102p2 = builder7101m.get_object('checkbutton7102p2')
    checkbutton7103p2 = builder7101m.get_object('checkbutton7103p2')

    # ********************** Define object functions for Environment Variables tab search customizations popover **********************
    def on_radiobutton7101p2_toggled(widget):                                                 # "Variable" radiobutton
        if radiobutton7101p2.get_active() == True:
            EnvironmentVariables.environment_variables_treeview_filter_search_func()

    def on_radiobutton7102p2_toggled(widget):                                                 # "Value" radiobutton
        if radiobutton7102p2.get_active() == True:
            EnvironmentVariables.environment_variables_treeview_filter_search_func()

    def on_checkbutton7101p2_toggled(widget):                                                 # "All variables" checkbutton
        environment_variables_popovers_checkbutton_behavior_func(checkbutton7101p2)

    def on_checkbutton7102p2_toggled(widget):                                                 # "Environment variables" checkbutton
        environment_variables_popovers_checkbutton_behavior_func( checkbutton7102p2)

    def on_checkbutton7103p2_toggled(widget):                                                 # "Shell variables" checkbutton
        environment_variables_popovers_checkbutton_behavior_func(checkbutton7103p2)

    # ********************** Connect signals to GUI objects for Environment Variables tab search customizations popover **********************
    radiobutton7101p2.connect("toggled", on_radiobutton7101p2_toggled)
    radiobutton7102p2.connect("toggled", on_radiobutton7102p2_toggled)
    global checkbutton7101p2_handler_id, checkbutton7102p2_handler_id, checkbutton7103p2_handler_id
    checkbutton7101p2_handler_id = checkbutton7101p2.connect("toggled", on_checkbutton7101p2_toggled)    # Handler ids are defined in order to block signals of the checkbuttons. Because activating and deactivating of this checkbuttons affects behaviors of each others and this would cause lock when active state of these are changed.
    checkbutton7102p2_handler_id = checkbutton7102p2.connect("toggled", on_checkbutton7102p2_toggled)
    checkbutton7103p2_handler_id = checkbutton7103p2.connect("toggled", on_checkbutton7103p2_toggled)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # ********************** Popover settings for Environment Variables tab **********************
    popover7101p.set_relative_to(EnvironmentVariablesGUI.button7101)
    popover7101p.set_position(1)
    # ********************** Popover settings for Environment Variables tab search customizations **********************
    popover7101p2.set_relative_to(EnvironmentVariablesGUI.button7103)
    popover7101p2.set_position(3)                                                             # Search customizations popover menu is not very long. It will be shown at the lower edge of the caller button (set_position(3)).



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


# ----------------------------------- Environment Variables - Environment Variables Tab Popovers Checkbuttons Behavior Function (contains statements and blocking code in order to avoid repetitive signal operations on checkbutton toggles) -----------------------------------
def environment_variables_popovers_checkbutton_behavior_func(caller_checkbutton):

    checkbutton_list = [checkbutton7101p2, checkbutton7102p2, checkbutton7103p2]
    select_all_checkbutton = checkbutton_list[0]
    sub_checkbutton_list = checkbutton_list
    sub_checkbutton_list.remove(select_all_checkbutton)
    checkbutton_active_state_list = []
    for checkbutton in sub_checkbutton_list:
        if checkbutton != select_all_checkbutton:
            checkbutton_active_state_list.append(checkbutton.get_active())

    with checkbutton7101p2.handler_block(checkbutton7101p2_handler_id) as p1, checkbutton7102p2.handler_block(checkbutton7102p2_handler_id) as p2, checkbutton7103p2.handler_block(checkbutton7103p2_handler_id) as p3:
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

    if EnvironmentVariablesGUI.searchentry7101.get_text() != "":                                         # Search filter updating is prevented, if any text is not inserted into searchentry. This is due to prevent user frustration because of the "Show all ... variables" radiobuttons above the treeview.
        EnvironmentVariables.environment_variables_treeview_filter_search_func()


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

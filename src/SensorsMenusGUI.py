#!/usr/bin/env python3

# ----------------------------------- Sensors - Sensors Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def sensors_menus_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global Config, Sensors, SensorsGUI
    import Config, Sensors, SensorsGUI


# ----------------------------------- Sensors - Sensors Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab menu/popover GUI objects and functions/signals) -----------------------------------
def sensors_menus_gui_func():

    # Define builder and get all objects (Performance tab Sensors sub-tab customizations popover and search customizations popover) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/SensorsMenusGUI.ui")


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Performance tab Sensors sub-tab customizations popover
    # ********************** Define object names for Sensors tab popover **********************
    global popover1601p
    global button1602p#, button1601p

    # ********************** Get objects for Sensors tab customizations popover **********************
    popover1601p = builder.get_object('popover1601p')
#     button1601p = builder.get_object('button1601p')
    button1602p = builder.get_object('button1602p')

    # ********************** Define object functions for Sensors tab customizations popover **********************
#     def on_button1601p_clicked(widget):                                                     # "Reset" button
#         Config.config_default_performance_sensors_row_column_func()
#         Config.config_save_func()

    def on_button1602p_clicked(widget):                                                       # "Reset All" button
        Config.config_default_performance_sensors_row_column_func()
        Config.config_save_func()

    # ********************** Connect signals to GUI objects for Sensors tab customizations popover **********************
#     button1601p.connect("clicked", on_button1601p_clicked)
    button1602p.connect("clicked", on_button1602p_clicked)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # ********************** Popover settings for Sensors tab **********************
#     popover1601p.set_relative_to(SensorsGUI.button1601)
#     popover1601p.set_position(1)



    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Performance tab Sensors sub-tab search customizations popover
    # ********************** Define object names for Sensors tab search customizations popover **********************
    global popover1601p2
    global radiobutton1601p2, radiobutton1602p2
    global checkbutton1601p2, checkbutton1602p2, checkbutton1603p2

    # ********************** Get objects for Sensors tab search popover **********************
    popover1601p2 = builder.get_object('popover1601p2')
    radiobutton1601p2 = builder.get_object('radiobutton1601p2')
    radiobutton1602p2 = builder.get_object('radiobutton1602p2')
    checkbutton1601p2 = builder.get_object('checkbutton1601p2')
    checkbutton1602p2 = builder.get_object('checkbutton1602p2')
    checkbutton1603p2 = builder.get_object('checkbutton1603p2')

    # ********************** Define object functions for Sensors tab search customizations popover **********************
    def on_radiobutton1601p2_toggled(widget):
        if radiobutton1601p2.get_active() == True:
            Sensors.sensors_treeview_filter_search_func()

    def on_radiobutton1602p2_toggled(widget):
        if radiobutton1602p2.get_active() == True:
            Sensors.sensors_treeview_filter_search_func()

    def on_checkbutton1601p2_toggled(widget):
        sensors_popovers_checkbutton_behavior_func("sensors", checkbutton1601p2)

    def on_checkbutton1602p2_toggled(widget):
        sensors_popovers_checkbutton_behavior_func("sensors", checkbutton1602p2)

    def on_checkbutton1603p2_toggled(widget):
        sensors_popovers_checkbutton_behavior_func("sensors", checkbutton1603p2)

    # ********************** Connect signals to GUI objects for Sensors tab search customizations popover **********************
    radiobutton1601p2.connect("toggled", on_radiobutton1601p2_toggled)
    radiobutton1602p2.connect("toggled", on_radiobutton1602p2_toggled)
    global checkbutton1601p2_handler_id, checkbutton1602p2_handler_id, checkbutton1603p2_handler_id
    checkbutton1601p2_handler_id = checkbutton1601p2.connect("toggled", on_checkbutton1601p2_toggled)   # Handler ids are defined in order to block signals of the checkbuttons. Because activating and deactivating of this checkbuttons affects behaviors of each others and this would cause lock when active state of these are changed.
    checkbutton1602p2_handler_id = checkbutton1602p2.connect("toggled", on_checkbutton1602p2_toggled)
    checkbutton1603p2_handler_id = checkbutton1603p2.connect("toggled", on_checkbutton1603p2_toggled)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # ********************** Popover settings for Sensors tab search customizations **********************
    popover1601p2.set_relative_to(SensorsGUI.button1603)
    popover1601p2.set_position(3)                                                             # Search customizations popover menu is not very long. It will be shown at the lower edge of the caller button (set_position(3)).



# ----------------------------------- Sensors - Sensors Tab Popovers Checkbuttons Behavior Function (contains statements and blocking code in order to avoid repetitive signal operations on checkbutton toggles) -----------------------------------
def sensors_popovers_checkbutton_behavior_func(caller_tab, caller_checkbutton):

    if caller_tab == "sensors":
        checkbutton_list = [checkbutton1601p2, checkbutton1602p2, checkbutton1603p2]
        select_all_checkbutton = checkbutton_list[0]
        sub_checkbutton_list = checkbutton_list
        sub_checkbutton_list.remove(select_all_checkbutton)
        checkbutton_active_state_list = []
        for checkbutton in sub_checkbutton_list:
            if checkbutton != select_all_checkbutton:
                checkbutton_active_state_list.append(checkbutton.get_active())

    with checkbutton1601p2.handler_block(checkbutton1601p2_handler_id) as p1, checkbutton1602p2.handler_block(checkbutton1602p2_handler_id) as p2, checkbutton1603p2.handler_block(checkbutton1603p2_handler_id) as p3:
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

    if SensorsGUI.searchentry1601.get_text() != "":                                           # Search filter updating is prevented, if any text is not inserted into searchentry. This is due to prevent user frustration because of the temperature/fan only buttons above the treeview.
        Sensors.sensors_treeview_filter_search_func()

#!/usr/bin/env python3

# ----------------------------------- Services - Services Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def services_menus_import_func():

    global Gtk, Gdk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import subprocess


    global Config, Services, ServicesGUI, ServicesDetails, ServicesDetailsGUI
    import Config, Services, ServicesGUI, ServicesDetails, ServicesDetailsGUI


# ----------------------------------- Services - Services Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Services" tab menu/popover GUI objects and functions/signals) -----------------------------------
def services_menus_gui_func():

    # Define builder and get all objects (Services tab right click menu, Services tab customizations popover, Services tab search customizations popover) from GUI file.
    builder6101m = Gtk.Builder()
    builder6101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ServicesMenus.ui")


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Services tab right click menu
    # ********************** Define object names for Services tab right click menu **********************
    global menu6101m
    global menuitem6101m, menuitem6102m, menuitem6103m, menuitem6104m, menuitem6105m, menuitem6106m, checkmenuitem6107m, menuitem6108m
    global menuitem6109m

    # ********************** Get object names for Services tab right click menu **********************
    menu6101m = builder6101m.get_object('menu6101m')
    menuitem6101m = builder6101m.get_object('menuitem6101m')
    menuitem6102m = builder6101m.get_object('menuitem6102m')
    menuitem6103m = builder6101m.get_object('menuitem6103m')
    menuitem6104m = builder6101m.get_object('menuitem6104m')
    menuitem6105m = builder6101m.get_object('menuitem6105m')
    menuitem6106m = builder6101m.get_object('menuitem6106m')
    checkmenuitem6107m = builder6101m.get_object('checkmenuitem6107m')
    menuitem6108m = builder6101m.get_object('menuitem6108m')
    menuitem6109m = builder6101m.get_object('menuitem6109m')

    # ********************** Define object functions for Services tab right click menu **********************
    def on_menu6101m_show(widget):
        pass

    def on_menuitem6101m_activate(widget):                                                    # "Start" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl start " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6102m_activate(widget):                                                    # "Stop" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl stop " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6103m_activate(widget):                                                    # "Restart" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl restart " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6104m_activate(widget):                                                    # "Reload" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl reload " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6105m_activate(widget):                                                    # "Enable" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl enable " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6106m_activate(widget):                                                    # "Disable" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            (subprocess.check_output("systemctl disable " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_checkmenuitem6107m_toggled(widget):                                                # "Mask" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        try:
            if checkmenuitem6107m.get_active() == True:
                (subprocess.check_output("systemctl mask " + service_name, shell=True).strip()).decode()
            if checkmenuitem6107m.get_active() == False:
                (subprocess.check_output("systemctl unmask " + service_name, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            pass

    def on_menuitem6108m_activate(widget):                                                    # "Copy Name" item on the right click menu
        service_name = ServicesGUI.selected_service_name
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(service_name, -1)
        clipboard.store()                                                                     # Stores copied text in the clipboard. Therefore text stays in the clipboard after application has quit.

    def on_menuitem6109m_activate(widget):                                                    # "Details" item on the right click menu
        ServicesDetailsGUI.services_details_gui_function()
        ServicesDetailsGUI.window6101w.show()
        ServicesDetails.services_details_foreground_thread_run_func()

    # ********************** Connect signals to GUI objects for Services tab right click menu **********************
    menu6101m.connect("show", on_menu6101m_show)
    menuitem6101m.connect("activate", on_menuitem6101m_activate)
    menuitem6102m.connect("activate", on_menuitem6102m_activate)
    menuitem6103m.connect("activate", on_menuitem6103m_activate)
    menuitem6104m.connect("activate", on_menuitem6104m_activate)
    global checkmenuitem6107m_handler_id
    checkmenuitem6107m_handler_id = checkmenuitem6107m.connect("toggled", on_checkmenuitem6107m_toggled)    # Handler id is defined in order to block signals of the checkmenuitem. Because checkmenuitem is set as "activated/deactivated" appropriate with relevant service status when right click and mouse button release action is finished. This action triggers unwanted event signals.
    menuitem6108m.connect("activate", on_menuitem6108m_activate)
    menuitem6109m.connect("activate", on_menuitem6109m_activate)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Services tab customizations popover
    # ********************** Define object names for Services tab customizations popover **********************
    global popover6101p
    global checkbutton6101p, checkbutton6102p, checkbutton6103p, checkbutton6104p, checkbutton6105p, checkbutton6106p
    global checkbutton6107p, checkbutton6108p
    global button6101p, button6102p
    global combobox6101p, combobox6102p

    # ********************** Get object names for Services tab customizations popover **********************
    popover6101p = builder6101m.get_object('popover6101p')
    checkbutton6101p = builder6101m.get_object('checkbutton6101p')
    checkbutton6102p = builder6101m.get_object('checkbutton6102p')
    checkbutton6103p = builder6101m.get_object('checkbutton6103p')
    checkbutton6104p = builder6101m.get_object('checkbutton6104p')
    checkbutton6105p = builder6101m.get_object('checkbutton6105p')
    checkbutton6106p = builder6101m.get_object('checkbutton6106p')
    checkbutton6107p = builder6101m.get_object('checkbutton6107p')
    checkbutton6108p = builder6101m.get_object('checkbutton6108p')
    button6101p = builder6101m.get_object('button6101p')
    button6102p = builder6101m.get_object('button6102p')
    combobox6101p = builder6101m.get_object('combobox6101p')
    combobox6102p = builder6101m.get_object('combobox6102p')

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
    def on_checkbutton6101p_toggled(widget):                                                  # "Service Name" checkbutton
        services_add_remove_columns_function()
    def on_checkbutton6102p_toggled(widget):                                                  # "State" checkbutton
        services_add_remove_columns_function()
    def on_checkbutton6103p_toggled(widget):                                                  # "Main PID" checkbutton
        services_add_remove_columns_function()
    def on_checkbutton6104p_toggled(widget):                                                  # "Active State" checkbutton
        services_add_remove_columns_function()
    def on_checkbutton6105p_toggled(widget):                                                  # "Load State" checkbutton
        services_add_remove_columns_function()
    def on_checkbutton6106p_toggled(widget):                                                  # "Sub-State" checkbutton
        services_add_remove_columns_function()
    def on_checkbutton6107p_toggled(widget):                                                  # "Memory (RSS)" checkbutton
        services_add_remove_columns_function()
    def on_checkbutton6108p_toggled(widget):                                                  # "Description" checkbutton
        services_add_remove_columns_function()

    # ********************** Define object functions for Services tab customizations popover Precision/Data Tab **********************
    def on_combobox6101p_changed(widget):                                                     # "RAM Usage" combobox (precision)
        Config.services_ram_swap_data_precision = Config.number_precision_list[combobox6101p.get_active()][2]
        Config.config_save_func()

    def on_combobox6102p_changed(widget):                                                     # "RAM Usage" combobox (data unit)
        Config.services_ram_swap_data_unit = Config.data_unit_list[combobox6102p.get_active()][2]
        Config.config_save_func()

    # ********************** Connect signals to GUI objects for Services tab customizations popover Common GUI Objects **********************
    button6101p.connect("clicked", on_button6101p_clicked)
    # ********************** Connect signals to GUI objects for Services tab customizations popover View Tab **********************
    button6102p.connect("clicked", on_button6102p_clicked)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Services tab search customizations popover
    # ********************** Define object names for Services tab search customizations popover **********************
    global popover6101p2
    global radiobutton6101p2, radiobutton6102p2, radiobutton6103p2, radiobutton6104p2, radiobutton6105p2, radiobutton6106p2, radiobutton6107p2
    global checkbutton6101p2, checkbutton6102p2, checkbutton6103p2
    # ********************** Get object names for Services tab search customizations popover **********************
    popover6101p2 = builder6101m.get_object('popover6101p2')
    radiobutton6101p2 = builder6101m.get_object('radiobutton6101p2')
    radiobutton6102p2 = builder6101m.get_object('radiobutton6102p2')
    radiobutton6103p2 = builder6101m.get_object('radiobutton6103p2')
    radiobutton6104p2 = builder6101m.get_object('radiobutton6104p2')
    radiobutton6105p2 = builder6101m.get_object('radiobutton6105p2')
    radiobutton6106p2 = builder6101m.get_object('radiobutton6106p2')
    radiobutton6107p2 = builder6101m.get_object('radiobutton6107p2')
    checkbutton6101p2 = builder6101m.get_object('checkbutton6101p2')
    checkbutton6102p2 = builder6101m.get_object('checkbutton6102p2')
    checkbutton6103p2 = builder6101m.get_object('checkbutton6103p2')

    # ********************** Define object functions for Services tab search customizations popover **********************
    def on_radiobutton6101p2_toggled(widget):
        if radiobutton6101p2.get_active() == True:
            Services.services_treeview_filter_search_func()

    def on_radiobutton6102p2_toggled(widget):
        if radiobutton6102p2.get_active() == True:
            Services.services_treeview_filter_search_func()

    def on_radiobutton6103p2_toggled(widget):
        if radiobutton6103p2.get_active() == True:
            Services.services_treeview_filter_search_func()

    def on_radiobutton6104p2_toggled(widget):
        if radiobutton6104p2.get_active() == True:
            Services.services_treeview_filter_search_func()

    def on_radiobutton6105p2_toggled(widget):
        if radiobutton6105p2.get_active() == True:
            Services.services_treeview_filter_search_func()

    def on_radiobutton6106p2_toggled(widget):
        if radiobutton6106p2.get_active() == True:
            Services.services_treeview_filter_search_func()

    def on_radiobutton6107p2_toggled(widget):
        if radiobutton6107p2.get_active() == True:
            Services.services_treeview_filter_search_func()

    def on_checkbutton6101p2_toggled(widget):
        services_popovers_checkbutton_behavior_func(checkbutton6101p2)

    def on_checkbutton6102p2_toggled(widget):
        services_popovers_checkbutton_behavior_func( checkbutton6102p2)

    def on_checkbutton6103p2_toggled(widget):
        services_popovers_checkbutton_behavior_func(checkbutton6103p2)

    # ********************** Connect signals to GUI objects for Services tab search customizations popover **********************
    radiobutton6101p2.connect("toggled", on_radiobutton6101p2_toggled)
    radiobutton6102p2.connect("toggled", on_radiobutton6102p2_toggled)
    radiobutton6103p2.connect("toggled", on_radiobutton6103p2_toggled)
    radiobutton6104p2.connect("toggled", on_radiobutton6104p2_toggled)
    radiobutton6105p2.connect("toggled", on_radiobutton6105p2_toggled)
    radiobutton6106p2.connect("toggled", on_radiobutton6106p2_toggled)
    radiobutton6107p2.connect("toggled", on_radiobutton6107p2_toggled)
    global checkbutton6101p2_handler_id, checkbutton6102p2_handler_id, checkbutton6103p2_handler_id
    checkbutton6101p2_handler_id = checkbutton6101p2.connect("toggled", on_checkbutton6101p2_toggled)    # Handler ids are defined in order to block signals of the checkbuttons. Because activating and deactivating of this checkbuttons affects behaviors of each others and this would cause lock when active state of these are changed.
    checkbutton6102p2_handler_id = checkbutton6102p2.connect("toggled", on_checkbutton6102p2_toggled)
    checkbutton6103p2_handler_id = checkbutton6103p2.connect("toggled", on_checkbutton6103p2_toggled)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # ********************** Popover settings for Services tab **********************
    popover6101p.set_relative_to(ServicesGUI.button6101)
    popover6101p.set_position(1)
    # ********************** Popover settings for Services tab search customizations **********************
    popover6101p2.set_relative_to(ServicesGUI.button6102)
    popover6101p2.set_position(3)                                                             # Search customizations popover menu is not very long. It will be shown at the lower edge of the caller button (set_position(3)).



    # ********************** Define function for connecting Services tab customizations popover GUI signals **********************
    def services_tab_customization_popover_connect_signals_func():
        # ********************** Connect signals to GUI objects for Services tab customizations popover Add/Remove Columns Tab **********************
        checkbutton6101p.connect("toggled", on_checkbutton6101p_toggled)
        checkbutton6102p.connect("toggled", on_checkbutton6102p_toggled)
        checkbutton6103p.connect("toggled", on_checkbutton6103p_toggled)
        checkbutton6104p.connect("toggled", on_checkbutton6104p_toggled)
        checkbutton6105p.connect("toggled", on_checkbutton6105p_toggled)
        checkbutton6106p.connect("toggled", on_checkbutton6106p_toggled)
        checkbutton6107p.connect("toggled", on_checkbutton6107p_toggled)
        checkbutton6108p.connect("toggled", on_checkbutton6108p_toggled)
        # ********************** Connect signals to GUI objects for Services tab customizations popover Precision/Data Units Tab **********************
        combobox6101p.connect("changed", on_combobox6101p_changed)
        combobox6102p.connect("changed", on_combobox6102p_changed)


    # ********************** Define function for disconnecting Services tab customizations popover GUI signals **********************
    def services_tab_customization_popover_disconnect_signals_func():
        # ********************** Connect signals to GUI objects for Services tab customizations popover Add/Remove Columns Tab **********************
        checkbutton6101p.disconnect_by_func(on_checkbutton6101p_toggled)
        checkbutton6102p.disconnect_by_func(on_checkbutton6102p_toggled)
        checkbutton6103p.disconnect_by_func(on_checkbutton6103p_toggled)
        checkbutton6104p.disconnect_by_func(on_checkbutton6104p_toggled)
        checkbutton6105p.disconnect_by_func(on_checkbutton6105p_toggled)
        checkbutton6106p.disconnect_by_func(on_checkbutton6106p_toggled)
        checkbutton6107p.disconnect_by_func(on_checkbutton6107p_toggled)
        checkbutton6108p.disconnect_by_func(on_checkbutton6108p_toggled)
        # ********************** Connect signals to GUI objects for Services tab customizations popover Precision/Data Units Tab **********************
        combobox6101p.disconnect_by_func(on_combobox6101p_changed)
        combobox6102p.disconnect_by_func(on_combobox6102p_changed)


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
    # Set Services tab customizations popover menu Precision/Data Units tab GUI object data/selections appropriate for settings
    # Add RAM usage data precision data into combobox
    if "liststore6101p" not in globals():                                                 # Check if "liststore6101p" is in global variables list (Python's own list = globals()) in order to prevent readdition of items to the listbox and combobox.
        global liststore6101p
        liststore6101p = Gtk.ListStore()
        liststore6101p.set_column_types([str, int])
        combobox6101p.set_model(liststore6101p)
        renderer_text = Gtk.CellRendererText()
        combobox6101p.pack_start(renderer_text, True)
        combobox6101p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore6101p.append([data[1], data[2]])
    combobox6101p.set_active(Config.services_ram_swap_data_precision)
    # Add RAM usage data unit data into combobox
    if "liststore6102p" not in globals():
        global liststore6102p
        liststore6102p = Gtk.ListStore()
        liststore6102p.set_column_types([str, int])
        combobox6102p.set_model(liststore6102p)
        renderer_text = Gtk.CellRendererText()
        combobox6102p.pack_start(renderer_text, True)
        combobox6102p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_unit_list:
            liststore6102p.append([data[1], data[2]])
    for data_list in Config.data_unit_list:
        if data_list[2] == Config.services_ram_swap_data_unit:      
            combobox6102p.set_active(data_list[0])


# ----------------------------------- Services - Services Tab Popovers Checkbuttons Behavior Function (contains statements and blocking code in order to avoid repetitive signal operations on checkbutton toggles) -----------------------------------
def services_popovers_checkbutton_behavior_func(caller_checkbutton):

    checkbutton_list = [checkbutton6101p2, checkbutton6102p2, checkbutton6103p2]
    select_all_checkbutton = checkbutton_list[0]
    sub_checkbutton_list = checkbutton_list
    sub_checkbutton_list.remove(select_all_checkbutton)
    checkbutton_active_state_list = []
    for checkbutton in sub_checkbutton_list:
        if checkbutton != select_all_checkbutton:
            checkbutton_active_state_list.append(checkbutton.get_active())

    with checkbutton6101p2.handler_block(checkbutton6101p2_handler_id) as p1, checkbutton6102p2.handler_block(checkbutton6102p2_handler_id) as p2, checkbutton6103p2.handler_block(checkbutton6103p2_handler_id) as p3:
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

    if ServicesGUI.searchentry6101.get_text() != "":                                         # Search filter updating is prevented, if any text is not inserted into searchentry. This is due to prevent user frustration because of the "Show all ... services" radiobuttons above the treeview.
        Services.services_treeview_filter_search_func()


# ----------------------------------- Services - Set Checkmenuitems (acivates/deactivates checkmenuitem (Enable/Disable checkbox for service status (enabled/disabled, masked/unmasked)) on the popup menu when right click operation is performed on service row on the treeview) -----------------------------------
def services_set_checkmenuitem_func():

    service_name = ServicesGUI.selected_service_name
    service_status = subprocess.check_output("systemctl show " + service_name + " --property=UnitFileState", shell=True).decode().strip().split("=")[1]
    with checkmenuitem6107m.handler_block(checkmenuitem6107m_handler_id):
        if service_status == "masked":
            checkmenuitem6107m.set_active(True)
        if service_status != "masked":
            checkmenuitem6107m.set_active(False)


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

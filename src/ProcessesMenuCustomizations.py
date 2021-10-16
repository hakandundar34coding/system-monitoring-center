#!/usr/bin/env python3

# ----------------------------------- Processes - Processes Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def processes_menu_customizations_import_func():

    global Gtk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os
    import subprocess


    global Config, Processes
    import Config, Processes


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


# ----------------------------------- Processes - Processes Tab Customizations Popover GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab menu/popover GUI objects and functions/signals) -----------------------------------
def processes_menu_customizations_gui_func():

    # Define builder and get all objects (Processes tab customizations popover) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesMenuCustomizations.ui")


    # ********************** Define object names for Processes tab customizations popover **********************
    global popover2101p
    global checkbutton2101p, checkbutton2102p, checkbutton2103p
    global button2102p, button2103p
    global checkbutton2106p, checkbutton2107p, checkbutton2108p, checkbutton2109p, checkbutton2110p, checkbutton2111p, checkbutton2112p, checkbutton2113p
    global checkbutton2114p, checkbutton2115p, checkbutton2116p, checkbutton2117p, checkbutton2118p, checkbutton2119p, checkbutton2120p, checkbutton2121p
    global checkbutton2122p, checkbutton2123p
    global combobox2101p, combobox2102p, combobox2103p, combobox2104p, combobox2105p, combobox2106p, combobox2107p

    # ********************** Get object names for Processes tab customizations popover **********************
    popover2101p = builder.get_object('popover2101p')
    checkbutton2101p = builder.get_object('checkbutton2101p')
    checkbutton2102p = builder.get_object('checkbutton2102p')
    checkbutton2103p = builder.get_object('checkbutton2103p')
    button2102p = builder.get_object('button2102p')
    button2103p = builder.get_object('button2103p')
    checkbutton2106p = builder.get_object('checkbutton2106p')
    checkbutton2107p = builder.get_object('checkbutton2107p')
    checkbutton2108p = builder.get_object('checkbutton2108p')
    checkbutton2109p = builder.get_object('checkbutton2109p')
    checkbutton2110p = builder.get_object('checkbutton2110p')
    checkbutton2111p = builder.get_object('checkbutton2111p')
    checkbutton2112p = builder.get_object('checkbutton2112p')
    checkbutton2113p = builder.get_object('checkbutton2113p')
    checkbutton2114p = builder.get_object('checkbutton2114p')
    checkbutton2115p = builder.get_object('checkbutton2115p')
    checkbutton2116p = builder.get_object('checkbutton2116p')
    checkbutton2117p = builder.get_object('checkbutton2117p')
    checkbutton2118p = builder.get_object('checkbutton2118p')
    checkbutton2119p = builder.get_object('checkbutton2119p')
    checkbutton2120p = builder.get_object('checkbutton2120p')
    checkbutton2121p = builder.get_object('checkbutton2121p')
    checkbutton2122p = builder.get_object('checkbutton2122p')
    checkbutton2123p = builder.get_object('checkbutton2123p')
    combobox2101p = builder.get_object('combobox2101p')
    combobox2102p = builder.get_object('combobox2102p')
    combobox2103p = builder.get_object('combobox2103p')
    combobox2104p = builder.get_object('combobox2104p')
    combobox2105p = builder.get_object('combobox2105p')
    combobox2106p = builder.get_object('combobox2106p')
    combobox2107p = builder.get_object('combobox2107p')

    # ********************** Define object functions for Processes tab customizations popover Common GUI Objects **********************
    def on_button2102p_clicked(widget):                                                       # "Reset All" button
        Config.config_default_processes_func()
        Config.config_save_func()
        processes_tab_customization_popover_disconnect_signals_func()
        processes_tab_popover_set_gui()
        processes_tab_customization_popover_connect_signals_func()
        processes_expand_collapse_button_preferences_func()

    # ********************** Define object functions for Processes tab customizations popover View Tab **********************
    def on_checkbutton2101p_toggled(widget):                                                  # "Show processes of all users" checkbutton
        if checkbutton2101p.get_active() == True:
            Config.show_processes_of_all_users = 1
        if checkbutton2101p.get_active() == False:
            Config.show_processes_of_all_users = 0
        Processes.processes_loop_func()
        Processes.processes_initial_func()
        Config.config_save_func()

    def on_checkbutton2102p_toggled(widget):                                                  # "Show processes as tree" checkbutton
        if checkbutton2102p.get_active() == True:
            Config.show_processes_as_tree = 1
            checkbutton2103p.set_sensitive(True)
        if checkbutton2102p.get_active() == False:
            Config.show_processes_as_tree = 0
            checkbutton2103p.set_sensitive(False)
        Config.config_save_func()
        processes_expand_collapse_button_preferences_func()

    def on_checkbutton2103p_toggled(widget):                                                  # "Show tree lines" checkbutton
        if checkbutton2103p.get_active() == True:
            Config.show_tree_lines = 1
        if checkbutton2103p.get_active() == False:
            Config.show_tree_lines = 0
        Config.config_save_func()

    def on_button2103p_clicked(widget):                                                       # "Reset" button
        Config.config_default_processes_row_sort_column_order_func()
        processes_tab_customization_popover_disconnect_signals_func()
        Config.config_save_func()
        processes_tab_customization_popover_connect_signals_func()

    # ********************** Define object functions for Processes tab customizations popover Add/Remove Columns Tab **********************
    def on_checkbutton2106p_toggled(widget):                                                  # "Name" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2107p_toggled(widget):                                                  # "PID" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2108p_toggled(widget):                                                  # "User Name" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2109p_toggled(widget):                                                  # "Status" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2110p_toggled(widget):                                                  # "CPU Usage Percent" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2111p_toggled(widget):                                                  # "RAM (RSS)" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2112p_toggled(widget):                                                  # "RAM (VMS)" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2113p_toggled(widget):                                                  # "RAM (Shared)" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2114p_toggled(widget):                                                  # "Disk Read Data" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2115p_toggled(widget):                                                  # "Disk Write Data" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2116p_toggled(widget):                                                  # "Disk Read Speed" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2117p_toggled(widget):                                                  # "Disk Write Speed" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2118p_toggled(widget):                                                  # "Priority" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2119p_toggled(widget):                                                  # "Number of Threads" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2120p_toggled(widget):                                                  # "PPID" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2121p_toggled(widget):                                                  # "UID" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2122p_toggled(widget):                                                  # "GID" checkbutton
        processes_add_remove_columns_function()
    def on_checkbutton2123p_toggled(widget):                                                  # "Path" checkbutton
        processes_add_remove_columns_function()

    # ********************** Define object functions for Processes tab customizations popover Precision/Data Tab **********************
    def on_combobox2101p_changed(widget):                                                     # "CPU Percent" combobox
        Config.processes_cpu_usage_percent_precision = Config.number_precision_list[combobox2101p.get_active()][2]
        Config.config_save_func()

    def on_combobox2102p_changed(widget):                                                     # "RAM & Swap Usage" combobox
        Config.processes_ram_swap_data_precision = Config.number_precision_list[combobox2102p.get_active()][2]
        Config.config_save_func()

    def on_combobox2103p_changed(widget):                                                     # "Disk Speed" combobox
        Config.processes_disk_speed_data_precision = Config.number_precision_list[combobox2103p.get_active()][2]
        Config.config_save_func()

    def on_combobox2104p_changed(widget):                                                     # "Disk Usage" combobox
        Config.processes_disk_usage_data_precision = Config.number_precision_list[combobox2104p.get_active()][2]
        Config.config_save_func()

    def on_combobox2105p_changed(widget):                                                     # "RAM & Swap Usage" combobox
        Config.processes_ram_swap_data_unit = Config.data_unit_list[combobox2105p.get_active()][2]
        Config.config_save_func()

    def on_combobox2106p_changed(widget):                                                     # "Disk Speed" combobox
        Config.processes_disk_speed_data_unit = Config.data_speed_unit_list[combobox2106p.get_active()][2]
        Config.config_save_func()

    def on_combobox2107p_changed(widget):                                                     # "Disk Usage" combobox
        Config.processes_disk_usage_data_unit = Config.data_unit_list[combobox2107p.get_active()][2]
        Config.config_save_func()

    # ********************** Connect signals to GUI objects for Processes tab customizations popover Common GUI Objects **********************
    button2102p.connect("clicked", on_button2102p_clicked)
    # ********************** Connect signals to GUI objects for Processes tab customizations popover View Tab **********************
    button2103p.connect("clicked", on_button2103p_clicked)


    # ********************** Popover settings for Processes tab **********************
    popover2101p.set_relative_to(Processes.button2101)
    popover2101p.set_position(1)


    # ********************** Define function for connecting Processes tab customizations popover GUI signals **********************
    def processes_tab_customization_popover_connect_signals_func():
        # ********************** Connect signals to GUI objects for Processes tab customizations popover View Tab **********************
        checkbutton2101p.connect("toggled", on_checkbutton2101p_toggled)
        checkbutton2102p.connect("toggled", on_checkbutton2102p_toggled)
        checkbutton2103p.connect("toggled", on_checkbutton2103p_toggled)
        # ********************** Connect signals to GUI objects for Processes tab customizations popover Add/Remove Columns Tab **********************
        checkbutton2106p.connect("toggled", on_checkbutton2106p_toggled)
        checkbutton2107p.connect("toggled", on_checkbutton2107p_toggled)
        checkbutton2108p.connect("toggled", on_checkbutton2108p_toggled)
        checkbutton2109p.connect("toggled", on_checkbutton2109p_toggled)
        checkbutton2110p.connect("toggled", on_checkbutton2110p_toggled)
        checkbutton2111p.connect("toggled", on_checkbutton2111p_toggled)
        checkbutton2112p.connect("toggled", on_checkbutton2112p_toggled)
        checkbutton2113p.connect("toggled", on_checkbutton2113p_toggled)
        checkbutton2114p.connect("toggled", on_checkbutton2114p_toggled)
        checkbutton2115p.connect("toggled", on_checkbutton2115p_toggled)
        checkbutton2116p.connect("toggled", on_checkbutton2116p_toggled)
        checkbutton2117p.connect("toggled", on_checkbutton2117p_toggled)
        checkbutton2118p.connect("toggled", on_checkbutton2118p_toggled)
        checkbutton2119p.connect("toggled", on_checkbutton2119p_toggled)
        checkbutton2120p.connect("toggled", on_checkbutton2120p_toggled)
        checkbutton2121p.connect("toggled", on_checkbutton2121p_toggled)
        checkbutton2122p.connect("toggled", on_checkbutton2122p_toggled)
        checkbutton2123p.connect("toggled", on_checkbutton2123p_toggled)
        # ********************** Connect signals to GUI objects for Processes tab customizations popover Precision/Data Units Tab **********************
        combobox2101p.connect("changed", on_combobox2101p_changed)
        combobox2102p.connect("changed", on_combobox2102p_changed)
        combobox2103p.connect("changed", on_combobox2103p_changed)
        combobox2104p.connect("changed", on_combobox2104p_changed)
        combobox2105p.connect("changed", on_combobox2105p_changed)
        combobox2106p.connect("changed", on_combobox2106p_changed)
        combobox2107p.connect("changed", on_combobox2107p_changed)


    # ********************** Define function for disconnecting Processes tab customizations popover GUI signals **********************
    def processes_tab_customization_popover_disconnect_signals_func():
        # ********************** Disconnect signals of GUI objects for Processes tab customizations popover View Tab **********************
        checkbutton2101p.disconnect_by_func(on_checkbutton2101p_toggled)
        checkbutton2102p.disconnect_by_func(on_checkbutton2102p_toggled)
        checkbutton2103p.disconnect_by_func(on_checkbutton2103p_toggled)
        # ********************** Disconnect signals of GUI objects for Processes tab customizations popover Add/Remove Columns Tab **********************
        checkbutton2106p.disconnect_by_func(on_checkbutton2106p_toggled)
        checkbutton2107p.disconnect_by_func(on_checkbutton2107p_toggled)
        checkbutton2108p.disconnect_by_func(on_checkbutton2108p_toggled)
        checkbutton2109p.disconnect_by_func(on_checkbutton2109p_toggled)
        checkbutton2110p.disconnect_by_func(on_checkbutton2110p_toggled)
        checkbutton2111p.disconnect_by_func(on_checkbutton2111p_toggled)
        checkbutton2112p.disconnect_by_func(on_checkbutton2112p_toggled)
        checkbutton2113p.disconnect_by_func(on_checkbutton2113p_toggled)
        checkbutton2114p.disconnect_by_func(on_checkbutton2114p_toggled)
        checkbutton2115p.disconnect_by_func(on_checkbutton2115p_toggled)
        checkbutton2116p.disconnect_by_func(on_checkbutton2116p_toggled)
        checkbutton2117p.disconnect_by_func(on_checkbutton2117p_toggled)
        checkbutton2118p.disconnect_by_func(on_checkbutton2118p_toggled)
        checkbutton2119p.disconnect_by_func(on_checkbutton2119p_toggled)
        checkbutton2120p.disconnect_by_func(on_checkbutton2120p_toggled)
        checkbutton2121p.disconnect_by_func(on_checkbutton2121p_toggled)
        checkbutton2122p.disconnect_by_func(on_checkbutton2122p_toggled)
        checkbutton2123p.disconnect_by_func(on_checkbutton2123p_toggled)
        # ********************** Disconnect signals of GUI objects for Processes tab customizations popover Precision/Data Units Tab **********************
        combobox2101p.disconnect_by_func(on_combobox2101p_changed)
        combobox2102p.disconnect_by_func(on_combobox2102p_changed)
        combobox2103p.disconnect_by_func(on_combobox2103p_changed)
        combobox2104p.disconnect_by_func(on_combobox2104p_changed)
        combobox2105p.disconnect_by_func(on_combobox2105p_changed)
        combobox2106p.disconnect_by_func(on_combobox2106p_changed)
        combobox2107p.disconnect_by_func(on_combobox2107p_changed)


    processes_tab_popover_set_gui()
    processes_tab_customization_popover_connect_signals_func()


# ********************** Set Processes tab customizations popover menu GUI object data/selections appropriate for settings **********************
def processes_tab_popover_set_gui():
    # Set Processes tab customizations popover menu View tab GUI object data/selections appropriate for settings
    if Config.show_processes_of_all_users == 1:
        checkbutton2101p.set_active(True)
    if Config.show_processes_of_all_users == 0:
        checkbutton2101p.set_active(False)
    if Config.show_processes_as_tree == 1:
        checkbutton2102p.set_active(True)
        checkbutton2103p.set_sensitive(True)
    if Config.show_processes_as_tree == 0:
        checkbutton2102p.set_active(False)
        checkbutton2103p.set_sensitive(False)
    if Config.show_tree_lines == 1:
        checkbutton2103p.set_active(True)
    if Config.show_tree_lines == 0:
        checkbutton2103p.set_active(False)
    # Set Processes tab customizations popover menu Add/Remove Column tab GUI object data/selections appropriate for settings
    if 0 in Config.processes_treeview_columns_shown:
        checkbutton2106p.set_active(True)
    if 0 not in Config.processes_treeview_columns_shown:
        checkbutton2106p.set_active(False)
    if 1 in Config.processes_treeview_columns_shown:
        checkbutton2107p.set_active(True)
    if 1 not in Config.processes_treeview_columns_shown:
        checkbutton2107p.set_active(False)
    if 2 in Config.processes_treeview_columns_shown:
        checkbutton2108p.set_active(True)
    if 2 not in Config.processes_treeview_columns_shown:
        checkbutton2108p.set_active(False)
    if 3 in Config.processes_treeview_columns_shown:
        checkbutton2109p.set_active(True)
    if 3 not in Config.processes_treeview_columns_shown:
        checkbutton2109p.set_active(False)
    if 4 in Config.processes_treeview_columns_shown:
        checkbutton2110p.set_active(True)
    if 4 not in Config.processes_treeview_columns_shown:
        checkbutton2110p.set_active(False)
    if 5 in Config.processes_treeview_columns_shown:
        checkbutton2111p.set_active(True)
    if 5 not in Config.processes_treeview_columns_shown:
        checkbutton2111p.set_active(False)
    if 6 in Config.processes_treeview_columns_shown:
        checkbutton2112p.set_active(True)
    if 6 not in Config.processes_treeview_columns_shown:
        checkbutton2112p.set_active(False)
    if 7 in Config.processes_treeview_columns_shown:
        checkbutton2113p.set_active(True)
    if 7 not in Config.processes_treeview_columns_shown:
        checkbutton2113p.set_active(False)
    if 8 in Config.processes_treeview_columns_shown:
        checkbutton2114p.set_active(True)
    if 8 not in Config.processes_treeview_columns_shown:
        checkbutton2114p.set_active(False)
    if 9 in Config.processes_treeview_columns_shown:
        checkbutton2115p.set_active(True)
    if 9 not in Config.processes_treeview_columns_shown:
        checkbutton2115p.set_active(False)
    if 10 in Config.processes_treeview_columns_shown:
        checkbutton2116p.set_active(True)
    if 10 not in Config.processes_treeview_columns_shown:
        checkbutton2116p.set_active(False)
    if 11 in Config.processes_treeview_columns_shown:
        checkbutton2117p.set_active(True)
    if 11 not in Config.processes_treeview_columns_shown:
        checkbutton2117p.set_active(False)
    if 12 in Config.processes_treeview_columns_shown:
        checkbutton2118p.set_active(True)
    if 12 not in Config.processes_treeview_columns_shown:
        checkbutton2118p.set_active(False)
    if 13 in Config.processes_treeview_columns_shown:
        checkbutton2119p.set_active(True)
    if 13 not in Config.processes_treeview_columns_shown:
        checkbutton2119p.set_active(False)
    if 14 in Config.processes_treeview_columns_shown:
        checkbutton2120p.set_active(True)
    if 14 not in Config.processes_treeview_columns_shown:
        checkbutton2120p.set_active(False)
    if 15 in Config.processes_treeview_columns_shown:
        checkbutton2121p.set_active(True)
    if 15 not in Config.processes_treeview_columns_shown:
        checkbutton2121p.set_active(False)
    if 16 in Config.processes_treeview_columns_shown:
        checkbutton2122p.set_active(True)
    if 16 not in Config.processes_treeview_columns_shown:
        checkbutton2122p.set_active(False)
    if 17 in Config.processes_treeview_columns_shown:
        checkbutton2123p.set_active(True)
    if 17 not in Config.processes_treeview_columns_shown:
        checkbutton2123p.set_active(False)
    # Set Processes tab customizations popover menu Precision/Data Units tab GUI object data/selections appropriate for settings
    # Add CPU usage percent data into combobox
    if "liststore2101p" not in globals():                                                 # Check if "liststore2101p" is in global variables list (Python's own list = globals()) in order to prevent readdition of items to the listbox and combobox.
        global liststore2101p
        liststore2101p = Gtk.ListStore()
        liststore2101p.set_column_types([str, int])
        combobox2101p.set_model(liststore2101p)
        renderer_text = Gtk.CellRendererText()
        combobox2101p.pack_start(renderer_text, True)
        combobox2101p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore2101p.append([data[1], data[2]])
    combobox2101p.set_active(Config.processes_cpu_usage_percent_precision)
    # Add RAM usage data precision data into combobox
    if "liststore2102p" not in globals():
        global liststore2102p
        liststore2102p = Gtk.ListStore()
        liststore2102p.set_column_types([str, int])
        combobox2102p.set_model(liststore2102p)
        renderer_text = Gtk.CellRendererText()
        combobox2102p.pack_start(renderer_text, True)
        combobox2102p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore2102p.append([data[1], data[2]])
    combobox2102p.set_active(Config.processes_ram_swap_data_precision)
    # Add Disk speed data precision data into combobox
    if "liststore2103p" not in globals():
        global liststore2103p
        liststore2103p = Gtk.ListStore()
        liststore2103p.set_column_types([str, int])
        combobox2103p.set_model(liststore2103p)
        renderer_text = Gtk.CellRendererText()
        combobox2103p.pack_start(renderer_text, True)
        combobox2103p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore2103p.append([data[1], data[2]])
    combobox2103p.set_active(Config.processes_disk_speed_data_precision)
    # Add Disk usage data precision data into combobox
    if "liststore2104p" not in globals():
        global liststore2104p
        liststore2104p = Gtk.ListStore()
        liststore2104p.set_column_types([str, int])
        combobox2104p.set_model(liststore2104p)
        renderer_text = Gtk.CellRendererText()
        combobox2104p.pack_start(renderer_text, True)
        combobox2104p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore2104p.append([data[1], data[2]])
    combobox2104p.set_active(Config.processes_disk_usage_data_precision)
    # Add RAM usage data unit data into combobox
    if "liststore2105p" not in globals():
        global liststore2105p
        liststore2105p = Gtk.ListStore()
        liststore2105p.set_column_types([str, int])
        combobox2105p.set_model(liststore2105p)
        renderer_text = Gtk.CellRendererText()
        combobox2105p.pack_start(renderer_text, True)
        combobox2105p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_unit_list:
            liststore2105p.append([data[1], data[2]])
    for data_list in Config.data_unit_list:
        if data_list[2] == Config.processes_ram_swap_data_unit:      
            combobox2105p.set_active(data_list[0])
    # Add Disk speed data unit data into combobox
    if "liststore2106p" not in globals():
        global liststore2106p
        liststore2106p = Gtk.ListStore()
        liststore2106p.set_column_types([str, int])
        combobox2106p.set_model(liststore2106p)
        renderer_text = Gtk.CellRendererText()
        combobox2106p.pack_start(renderer_text, True)
        combobox2106p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_speed_unit_list:
            liststore2106p.append([data[1], data[2]])
    for data_list in Config.data_speed_unit_list:
        if data_list[2] == Config.processes_disk_speed_data_unit:      
            combobox2106p.set_active(data_list[0])
    # Add Disk usage data unit data into combobox
    if "liststore2107p" not in globals():
        global liststore2107p
        liststore2107p = Gtk.ListStore()
        liststore2107p.set_column_types([str, int])
        combobox2107p.set_model(liststore2107p)
        renderer_text = Gtk.CellRendererText()
        combobox2107p.pack_start(renderer_text, True)
        combobox2107p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_unit_list:
            liststore2107p.append([data[1], data[2]])
    for data_list in Config.data_unit_list:
        if data_list[2] == Config.processes_disk_usage_data_unit:      
            combobox2107p.set_active(data_list[0])


# ----------------------------------- Processes - Processes Add/Remove Columns Function (adds/removes processes treeview columns) -----------------------------------
def processes_add_remove_columns_function():

    # Add/Remove treeview columns
    Config.processes_treeview_columns_shown = []
    if checkbutton2106p.get_active() is True:
        Config.processes_treeview_columns_shown.append(0)
    if checkbutton2107p.get_active() is True:
        Config.processes_treeview_columns_shown.append(1)
    if checkbutton2108p.get_active() is True:
        Config.processes_treeview_columns_shown.append(2)
    if checkbutton2109p.get_active() is True:
        Config.processes_treeview_columns_shown.append(3)
    if checkbutton2110p.get_active() is True:
        Config.processes_treeview_columns_shown.append(4)
    if checkbutton2111p.get_active() is True:
        Config.processes_treeview_columns_shown.append(5)
    if checkbutton2112p.get_active() is True:
        Config.processes_treeview_columns_shown.append(6)
    if checkbutton2113p.get_active() is True:
        Config.processes_treeview_columns_shown.append(7)
    if checkbutton2114p.get_active() is True:
        Config.processes_treeview_columns_shown.append(8)
    if checkbutton2115p.get_active() is True:
        Config.processes_treeview_columns_shown.append(9)
    if checkbutton2116p.get_active() is True:
        Config.processes_treeview_columns_shown.append(10)
    if checkbutton2117p.get_active() is True:
        Config.processes_treeview_columns_shown.append(11)
    if checkbutton2118p.get_active() is True:
        Config.processes_treeview_columns_shown.append(12)
    if checkbutton2119p.get_active() is True:
        Config.processes_treeview_columns_shown.append(13)
    if checkbutton2120p.get_active() is True:
        Config.processes_treeview_columns_shown.append(14)
    if checkbutton2121p.get_active() is True:
        Config.processes_treeview_columns_shown.append(15)
    if checkbutton2122p.get_active() is True:
        Config.processes_treeview_columns_shown.append(16)
    if checkbutton2123p.get_active() is True:
        Config.processes_treeview_columns_shown.append(17)
    Config.config_save_func()


# ----------------------------------- Processes - Expand/Collapse Button Preference Function (sets "User defined expand, Expand all, Collapse all" buttons as sensitive/insensitive if "show_processes_as_tree" is enabled/disabled) -----------------------------------
def processes_expand_collapse_button_preferences_func():
    if checkbutton2102p.get_active() == True:
        # Set "User defined expand, Expand all, Collapse all" buttons as "sensitive" on the Processes tab if "show_processes_as_tree" option is enabled. Therefore, expanding/collapsing treeview rows functions will be available for using by the user. Also change widget tooltips for better understandability
        Processes.radiobutton2104.set_sensitive(True)
        Processes.radiobutton2105.set_sensitive(True)
        Processes.radiobutton2106.set_sensitive(True)
        Processes.radiobutton2104.set_tooltip_text(_tr("User defined expand"))
        Processes.radiobutton2105.set_tooltip_text(_tr("Expand all"))
        Processes.radiobutton2106.set_tooltip_text(_tr("Collapse all"))
    if checkbutton2102p.get_active() == False:
        # Set "User defined expand, Expand all, Collapse all" buttons as "insensitive" on the Processes tab if "show_processes_as_tree" option is disabled. Because expanding/collapsing treeview rows has no effects when treeview items are listed as "list". Also change widget tooltips for better understandability
        Processes.radiobutton2104.set_sensitive(False)
        Processes.radiobutton2105.set_sensitive(False)
        Processes.radiobutton2106.set_sensitive(False)
        Processes.radiobutton2104.set_tooltip_text(_tr("User defined expand\n(Usable if processes are listed as tree)"))
        Processes.radiobutton2105.set_tooltip_text(_tr("Expand all\n(Usable if processes are listed as tree)"))
        Processes.radiobutton2106.set_tooltip_text(_tr("Collapse all\n(Usable if processes are listed as tree)"))

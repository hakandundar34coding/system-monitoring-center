#! /usr/bin/python3

# ----------------------------------- Processes - Processes Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def processes_menus_import_func():

    global Gtk, Gdk, os, signal, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import signal
    import subprocess


    global Config, MainGUI, Processes, ProcessesGUI
    import Config, MainGUI, Processes, ProcessesGUI


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


# ----------------------------------- Processes - Processes Menus GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab menu/popover GUI objects and functions/signals) -----------------------------------
def processes_menus_gui_func():

    # Define builder and get all objects (Processes tab right click menu, Processes tab customizations popover, Processes tab search customizations popover) from GUI file.
    builder2101m = Gtk.Builder()
    builder2101m.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesMenus.ui")


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Processes tab right click menu
    # ********************** Define object names for Processes tab right click menu **********************
    global menu2101m
    global menuitem2101m, menuitem2102m, menuitem2103m, menuitem2104m, menuitem2106m, menuitem2107m, menuitem2108m
    global radiomenuitem2101m, radiomenuitem2102m, radiomenuitem2103m, radiomenuitem2104m, radiomenuitem2105m, normalmenuitem2101m

    # ********************** Get object names for Processes tab right click menu **********************
    menu2101m = builder2101m.get_object('menu2101m')
    menuitem2101m = builder2101m.get_object('menuitem2101m')
    menuitem2102m = builder2101m.get_object('menuitem2102m')
    menuitem2103m = builder2101m.get_object('menuitem2103m')
    menuitem2104m = builder2101m.get_object('menuitem2104m')
    menuitem2106m = builder2101m.get_object('menuitem2106m')
    menuitem2107m = builder2101m.get_object('menuitem2107m')
    menuitem2108m = builder2101m.get_object('menuitem2108m')
    radiomenuitem2101m = builder2101m.get_object('radiomenuitem2101m')
    radiomenuitem2102m = builder2101m.get_object('radiomenuitem2102m')
    radiomenuitem2103m = builder2101m.get_object('radiomenuitem2103m')
    radiomenuitem2104m = builder2101m.get_object('radiomenuitem2104m')
    radiomenuitem2105m = builder2101m.get_object('radiomenuitem2105m')
    normalmenuitem2101m = builder2101m.get_object('normalmenuitem2101m')

    # ********************** Define object functions for Processes tab right click menu **********************
    def on_menuitem2101m_activate(widget):                                                    # "Pause Process" item on the right click menu
        os.kill(ProcessesGUI.selected_process_pid, signal.SIGSTOP)

    def on_menuitem2102m_activate(widget):                                                    # "Resume Process" item on the right click menu
        os.kill(ProcessesGUI.selected_process_pid, signal.SIGCONT)

    def on_menuitem2103m_activate(widget):                                                    # "End Process" item on the right click menu
        process_pid = ProcessesGUI.selected_process_pid
        process_name = Processes.processes_data_rows[Processes.pid_list.index(process_pid)][2]
        if Config.warn_before_stopping_processes == 1:
            processes_end_process_warning_dialog(process_name, process_pid)
            if warning_dialog2101_response == Gtk.ResponseType.YES:
                os.kill(int(process_pid), signal.SIGTERM)
            if warning_dialog2101_response == Gtk.ResponseType.NO:
                pass                                                                          # Do nothing when "No" button is clicked. Dialog will be closed.
        if Config.warn_before_stopping_processes == 0:
            os.kill(process_pid, signal.SIGTERM)

    # Currently same as "End Process"
    def on_menuitem2104m_activate(widget):                                                    # "End Process Tree" item on the right click menu
        process_pid = ProcessesGUI.selected_process_pid
        process_name = Processes.processes_data_rows[Processes.pid_list.index(process_pid)][2]
        if Config.warn_before_stopping_processes == 1:
            processes_end_process_tree_warning_dialog(process_name, process_pid)
            if warning_dialog2102_response == Gtk.ResponseType.YES:
                os.kill(int(process_pid), signal.SIGTERM)
            if warning_dialog2102_response == Gtk.ResponseType.NO:
                pass                                                                          # Do nothing when "No" button is clicked. Dialog will be closed.
        if Config.warn_before_stopping_processes == 0:
            os.kill(int(process_pid), signal.SIGTERM)

    def on_menuitem2106m_activate(widget):                                                    # "Copy Name" item on the right click menu
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(Processes.processes_data_rows[Processes.pid_list.index(ProcessesGUI.selected_process_pid)][2], -1)
        clipboard.store()

    def on_menuitem2107m_activate(widget):                                                    # "Open Location" item on the right click menu
        try:                                                                                  # Executable path of some of the processes may not be get without root privileges or may not be get due to the reason of some of the processes may not have a exe file. "try-except" is used to be able to avoid errors due to these reasons.
            full_path = os.path.realpath("/proc/" + ProcessesGUI.selected_process_pid + "/exe")
        except:
            try:
                with open("/proc/" + ProcessesGUI.selected_process_pid + "/cmdline") as reader:
                    full_path = reader.read()
            except:
                full_path = "-"
        if full_path == "":
            full_path = "-"
        if full_path == "-":
            processes_no_path_error_dialog()
            return
        path_only, file_name_only = os.path.split(os.path.abspath(full_path))
        os.system('xdg-open "%s"' % path_only)

    def on_menuitem2108m_activate(widget):                                                    # "Details" item on the right click menu
        if 'ProcessesDetailsGUI' not in globals():                                            # Check if "ProcessesDetailsGUI" module is imported. Therefore it is not reimported for every click on "Details" menu item on the right click menu if "ProcessesDetailsGUI" name is in globals(). It is not recognized after tab switch if it is not imported as global.
            global ProcessesDetailsGUI, ProcessesDetails
            import ProcessesDetailsGUI, ProcessesDetails
            ProcessesDetailsGUI.processes_details_gui_import_function()
            ProcessesDetailsGUI.processes_details_gui_function()
            ProcessesDetails.processes_details_import_func()
        ProcessesDetailsGUI.window2101w.show()
        ProcessesDetails.process_details_foreground_thread_run_func()

    def on_radiomenuitem2101m_activate(widget):                                               # "Very High" item on the right click menu under "Change Priorty (Nice)" item
        processes_get_process_current_nice_func()
        if selected_process_current_nice <= -20:
            (subprocess.check_output("renice -n -20 -p " + ProcessesGUI.selected_process_pid, shell=True).strip()).decode()
        if selected_process_current_nice > -20:
            try:
                (subprocess.check_output("pkexec renice -n -20 -p " + ProcessesGUI.selected_process_pid, shell=True).strip()).decode()    # It gives "renice: failed to set priority for [PID] (process ID): Access denied" output if application is not run with root privileges.
            except subprocess.CalledProcessError:
                processes_nice_error_dialog()

    def on_radiomenuitem2102m_activate(widget):                                               # "High" item on the right click menu under "Change Priorty (Nice)" item
        processes_get_process_current_nice_func()
        if selected_process_current_nice <= -10:
            (subprocess.check_output("renice -n -10 -p " + ProcessesGUI.selected_process_pid, shell=True).strip()).decode()
        if selected_process_current_nice > -10:
            try:
                (subprocess.check_output("pkexec renice -n -10 -p " + ProcessesGUI.selected_process_pid, shell=True).strip()).decode()    # It gives "renice: failed to set priority for [PID] (process ID): Access denied" output if application is not run with root privileges.
            except subprocess.CalledProcessError:
                processes_nice_error_dialog()

    def on_radiomenuitem2103m_activate(widget):                                               # "Normal" item on the right click menu under "Change Priorty (Nice)" item
        processes_get_process_current_nice_func()
        if selected_process_current_nice <= 0:
            (subprocess.check_output("renice -n 0 -p " + ProcessesGUI.selected_process_pid, shell=True).strip()).decode()
        if selected_process_current_nice > 0:
            try:
                (subprocess.check_output("pkexec renice -n 0 -p " + ProcessesGUI.selected_process_pid, shell=True).strip()).decode()    # It gives "renice: failed to set priority for [PID] (process ID): Access denied" output if application is not run with root privileges.
            except subprocess.CalledProcessError:
                processes_nice_error_dialog()

    def on_radiomenuitem2104m_activate(widget):                                               # "Low" item on the right click menu under "Change Priorty (Nice)" item
        processes_get_process_current_nice_func()
        if selected_process_current_nice <= 10:
            (subprocess.check_output("renice -n 10 -p " + ProcessesGUI.selected_process_pid, shell=True).strip()).decode()
        if selected_process_current_nice > 10:
            try:
                (subprocess.check_output("pkexec renice -n 10 -p " + ProcessesGUI.selected_process_pid, shell=True).strip()).decode()    # It gives "renice: failed to set priority for [PID] (process ID): Access denied" output if application is not run with root privileges.
            except subprocess.CalledProcessError:
                processes_nice_error_dialog()

    def on_radiomenuitem2105m_activate(widget):                                               # "Very Low" item on the right click menu under "Change Priorty (Nice)" item
        (subprocess.check_output("renice -n 19 -p " + ProcessesGUI.selected_process_pid, shell=True).strip()).decode()

    def on_normalmenuitem2101m_activate(widget):                                              # "Custom Value..." item on the right click menu under "Change Priorty (Nice)" item
        if 'ProcessesCustomPriorityGUI' not in globals():                                     # Check if "ProcessesCustomPriorityGUI" module is imported. Therefore it is not reimported for every click on "Custom Value" sub-menu item on the rigth click menu if "ProcessesCustomPriorityGUI" name is in globals(). It is not recognized after tab switch if it is not imported as global.
            global ProcessesCustomPriorityGUI
            import ProcessesCustomPriorityGUI
            ProcessesCustomPriorityGUI.processes_custom_priority_import_func()
            ProcessesCustomPriorityGUI.processes_custom_priority_gui_func()
        ProcessesCustomPriorityGUI.window2101w2.show()



    # ********************** Connect signals to GUI objects for Processes tab right click menu **********************
    menuitem2101m.connect("activate", on_menuitem2101m_activate)
    menuitem2102m.connect("activate", on_menuitem2102m_activate)
    menuitem2103m.connect("activate", on_menuitem2103m_activate)
    menuitem2104m.connect("activate", on_menuitem2104m_activate)
    menuitem2106m.connect("activate", on_menuitem2106m_activate)
    menuitem2107m.connect("activate", on_menuitem2107m_activate)
    menuitem2108m.connect("activate", on_menuitem2108m_activate)
    normalmenuitem2101m.connect("activate", on_normalmenuitem2101m_activate)
    global radiomenuitem2101m_handler_id, radiomenuitem2102m_handler_id, radiomenuitem2103m_handler_id, radiomenuitem2104m_handler_id, radiomenuitem2105m_handler_id
    radiomenuitem2101m_handler_id = radiomenuitem2101m.connect("activate", on_radiomenuitem2101m_activate)
    radiomenuitem2102m_handler_id = radiomenuitem2102m.connect("activate", on_radiomenuitem2102m_activate)
    radiomenuitem2103m_handler_id = radiomenuitem2103m.connect("activate", on_radiomenuitem2103m_activate)
    radiomenuitem2104m_handler_id = radiomenuitem2104m.connect("activate", on_radiomenuitem2104m_activate)
    radiomenuitem2105m_handler_id = radiomenuitem2105m.connect("activate", on_radiomenuitem2105m_activate)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Processes tab customizations popover
    # ********************** Define object names for Processes tab customizations popover **********************
    global popover2101p
    global checkbutton2101p, checkbutton2102p, checkbutton2103p
    global button2101p, button2102p, button2103p
    global checkbutton2106p, checkbutton2107p, checkbutton2108p, checkbutton2109p, checkbutton2110p, checkbutton2111p, checkbutton2112p, checkbutton2113p
    global checkbutton2114p, checkbutton2115p, checkbutton2116p, checkbutton2117p, checkbutton2118p, checkbutton2119p, checkbutton2120p, checkbutton2121p
    global checkbutton2122p, checkbutton2123p
    global combobox2101p, combobox2102p, combobox2103p, combobox2104p, combobox2105p, combobox2106p, combobox2107p

    # ********************** Get object names for Processes tab customizations popover **********************
    popover2101p = builder2101m.get_object('popover2101p')
    checkbutton2101p = builder2101m.get_object('checkbutton2101p')
    checkbutton2102p = builder2101m.get_object('checkbutton2102p')
    checkbutton2103p = builder2101m.get_object('checkbutton2103p')
    button2101p = builder2101m.get_object('button2101p')
    button2102p = builder2101m.get_object('button2102p')
    button2103p = builder2101m.get_object('button2103p')
    checkbutton2106p = builder2101m.get_object('checkbutton2106p')
    checkbutton2107p = builder2101m.get_object('checkbutton2107p')
    checkbutton2108p = builder2101m.get_object('checkbutton2108p')
    checkbutton2109p = builder2101m.get_object('checkbutton2109p')
    checkbutton2110p = builder2101m.get_object('checkbutton2110p')
    checkbutton2111p = builder2101m.get_object('checkbutton2111p')
    checkbutton2112p = builder2101m.get_object('checkbutton2112p')
    checkbutton2113p = builder2101m.get_object('checkbutton2113p')
    checkbutton2114p = builder2101m.get_object('checkbutton2114p')
    checkbutton2115p = builder2101m.get_object('checkbutton2115p')
    checkbutton2116p = builder2101m.get_object('checkbutton2116p')
    checkbutton2117p = builder2101m.get_object('checkbutton2117p')
    checkbutton2118p = builder2101m.get_object('checkbutton2118p')
    checkbutton2119p = builder2101m.get_object('checkbutton2119p')
    checkbutton2120p = builder2101m.get_object('checkbutton2120p')
    checkbutton2121p = builder2101m.get_object('checkbutton2121p')
    checkbutton2122p = builder2101m.get_object('checkbutton2122p')
    checkbutton2123p = builder2101m.get_object('checkbutton2123p')
    combobox2101p = builder2101m.get_object('combobox2101p')
    combobox2102p = builder2101m.get_object('combobox2102p')
    combobox2103p = builder2101m.get_object('combobox2103p')
    combobox2104p = builder2101m.get_object('combobox2104p')
    combobox2105p = builder2101m.get_object('combobox2105p')
    combobox2106p = builder2101m.get_object('combobox2106p')
    combobox2107p = builder2101m.get_object('combobox2107p')

    # ********************** Define object functions for Processes tab customizations popover Common GUI Objects **********************
    def on_button2101p_clicked(widget):                                                       # "Process tree information from 'ps --forest -Ao pid,uid,ppid,cmd' command output" button
        process = subprocess.Popen("x-terminal-emulator -e /bin/bash -c \'ps --forest -Ao pid,uid,ppid,cmd; exec bash\'", stdout=subprocess.PIPE, stderr=None, shell=True)

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
    button2101p.connect("clicked", on_button2101p_clicked)
    button2102p.connect("clicked", on_button2102p_clicked)
    # ********************** Connect signals to GUI objects for Processes tab customizations popover View Tab **********************
    button2103p.connect("clicked", on_button2103p_clicked)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Define object names, get object names, define object functions and connect signals to GUI objects for Processes tab search customizations popover
    # ********************** Define object names for Processes tab search customizations popover **********************
    global popover2101p2
    global radiobutton2101p2, radiobutton2102p2, radiobutton2103p2, radiobutton2104p2, radiobutton2105p2, radiobutton2106p2
    global checkbutton2101p2, checkbutton2102p2, checkbutton2103p2

    # ********************** Get object names for Processes tab search customizations popover **********************
    popover2101p2 = builder2101m.get_object('popover2101p2')
    radiobutton2101p2 = builder2101m.get_object('radiobutton2101p2')
    radiobutton2102p2 = builder2101m.get_object('radiobutton2102p2')
    radiobutton2103p2 = builder2101m.get_object('radiobutton2103p2')
    radiobutton2104p2 = builder2101m.get_object('radiobutton2104p2')
    radiobutton2105p2 = builder2101m.get_object('radiobutton2105p2')
    radiobutton2106p2 = builder2101m.get_object('radiobutton2106p2')
    checkbutton2101p2 = builder2101m.get_object('checkbutton2101p2')
    checkbutton2102p2 = builder2101m.get_object('checkbutton2102p2')
    checkbutton2103p2 = builder2101m.get_object('checkbutton2103p2')

    # ********************** Define object functions for Processes tab search customizations popover **********************
    def on_radiobutton2101p2_toggled(widget):                                                 # "Name" radiobutton
        if radiobutton2101p2.get_active() == True:
            Processes.processes_treeview_filter_search_func()

    def on_radiobutton2102p2_toggled(widget):                                                 # "PID" radiobutton
        if radiobutton2102p2.get_active() == True:
            Processes.processes_treeview_filter_search_func()

    def on_radiobutton2103p2_toggled(widget):                                                 # "User Name" radiobutton
        if radiobutton2103p2.get_active() == True:
            Processes.processes_treeview_filter_search_func()

    def on_radiobutton2104p2_toggled(widget):                                                 # "Status" radiobutton
        if radiobutton2104p2.get_active() == True:
            Processes.processes_treeview_filter_search_func()

    def on_radiobutton2105p2_toggled(widget):                                                 # "PPID" radiobutton
        if radiobutton2105p2.get_active() == True:
            Processes.processes_treeview_filter_search_func()

    def on_radiobutton2106p2_toggled(widget):                                                 # "Path" radiobutton
        if radiobutton2106p2.get_active() == True:
            Processes.processes_treeview_filter_search_func()

    def on_checkbutton2101p2_toggled(widget):                                                 # "All users" checkbutton
        processes_popovers_checkbutton_behavior_func(checkbutton2101p2)

    def on_checkbutton2102p2_toggled(widget):                                                 # "This user" checkbutton
        processes_popovers_checkbutton_behavior_func( checkbutton2102p2)

    def on_checkbutton2103p2_toggled(widget):                                                 # "Other users" checkbutton
        processes_popovers_checkbutton_behavior_func(checkbutton2103p2)

    # ********************** Connect signals to GUI objects for Processes tab search customizations popover **********************
    radiobutton2101p2.connect("toggled", on_radiobutton2101p2_toggled)
    radiobutton2102p2.connect("toggled", on_radiobutton2102p2_toggled)
    radiobutton2103p2.connect("toggled", on_radiobutton2103p2_toggled)
    radiobutton2104p2.connect("toggled", on_radiobutton2104p2_toggled)
    radiobutton2105p2.connect("toggled", on_radiobutton2105p2_toggled)
    radiobutton2106p2.connect("toggled", on_radiobutton2106p2_toggled)
    global checkbutton2101p2_handler_id, checkbutton2102p2_handler_id, checkbutton2103p2_handler_id
    checkbutton2101p2_handler_id = checkbutton2101p2.connect("toggled", on_checkbutton2101p2_toggled)    # Handler ids are defined in order to block signals of the checkbuttons. Because activating and deactivating of this checkbuttons affects behaviors of each others and this would cause lock when active state of these are changed.
    checkbutton2102p2_handler_id = checkbutton2102p2.connect("toggled", on_checkbutton2102p2_toggled)
    checkbutton2103p2_handler_id = checkbutton2103p2.connect("toggled", on_checkbutton2103p2_toggled)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


    # ********************** Popover settings for Processes tab **********************
    popover2101p.set_relative_to(ProcessesGUI.button2101)
    popover2101p.set_position(1)
    # ********************** Popover settings for Processes tab search customizations **********************
    popover2101p2.set_relative_to(ProcessesGUI.button2104)
    popover2101p2.set_position(3)                                                             # Search customizations popover menu is not very long. It will be shown at the lower edge of the caller button (set_position(3)).



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


# ----------------------------------- Processes - Processes Tab Popovers Checkbuttons Behavior Function (contains statements and blocking code in order to avoid repetitive signal operations on checkbutton toggles) -----------------------------------
def processes_popovers_checkbutton_behavior_func(caller_checkbutton):

    checkbutton_list = [checkbutton2101p2, checkbutton2102p2, checkbutton2103p2]
    select_all_checkbutton = checkbutton_list[0]
    sub_checkbutton_list = checkbutton_list
    sub_checkbutton_list.remove(select_all_checkbutton)
    checkbutton_active_state_list = []
    for checkbutton in sub_checkbutton_list:
        if checkbutton != select_all_checkbutton:
            checkbutton_active_state_list.append(checkbutton.get_active())

    with checkbutton2101p2.handler_block(checkbutton2101p2_handler_id) as p1, checkbutton2102p2.handler_block(checkbutton2102p2_handler_id) as p2, checkbutton2103p2.handler_block(checkbutton2103p2_handler_id) as p3:
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

    if ProcessesGUI.searchentry2101.get_text() != "":                                         # Search filter updating is prevented, if any text is not inserted into searchentry. This is due to prevent user frustration because of the "Show processes from ..." radiobuttons above the treeview.
        Processes.processes_treeview_filter_search_func()


# ----------------------------------- Processes - Select Process Nice Option Function (selects process nice option on the popup menu when right click operation is performed on process row on the treeview) -----------------------------------
def processes_select_process_nice_option_func():

    try:                                                                                      # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
        with open("/proc/" + ProcessesGUI.selected_process_pid + "/stat") as reader:          # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
            proc_pid_stat_lines = reader.read()
    except FileNotFoundError:
        processes_no_such_process_error_dialog()
        return
    selected_process_nice = int(proc_pid_stat_lines.split()[-34])
    with radiomenuitem2101m.handler_block(radiomenuitem2101m_handler_id) as p1, radiomenuitem2102m.handler_block(radiomenuitem2102m_handler_id) as p2, radiomenuitem2103m.handler_block(radiomenuitem2103m_handler_id) as p3, radiomenuitem2104m.handler_block(radiomenuitem2104m_handler_id) as p4, radiomenuitem2105m.handler_block(radiomenuitem2105m_handler_id) as p5:    # Pause event signals while makiing changes on radiobutton selections.
        if selected_process_nice <= -11 and selected_process_nice >= -20:
            radiomenuitem2101m.set_active(True)
        if selected_process_nice < 0 and selected_process_nice > -11:
            radiomenuitem2102m.set_active(True)
        if selected_process_nice == 0:
            radiomenuitem2103m.set_active(True)
        if selected_process_nice < 11 and selected_process_nice > 0:
            radiomenuitem2104m.set_active(True)
        if selected_process_nice <= 19 and selected_process_nice >= 11:
            radiomenuitem2105m.set_active(True)


# ----------------------------------- Processes - Get Process Current Nice Function (get process current nice value in order to check if root privileges are needed for nice changing operation) -----------------------------------
def processes_get_process_current_nice_func():

    try:                                                                                      # Process may be ended just after right click on the process row is performed. "try-catch" is used for avoiding errors in this situation.
        with open("/proc/" + ProcessesGUI.selected_process_pid + "/stat") as reader:
            proc_pid_stat_lines_split = reader.read().split()
    except FileNotFoundError:
        return
    global selected_process_current_nice
    selected_process_current_nice = int(proc_pid_stat_lines_split[-34])                       # Get process nice value


# ----------------------------------- Processes - Processes Add/Remove Columns Function (adds/removes processes treeview columns) -----------------------------------
def processes_add_remove_columns_function():

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
        ProcessesGUI.radiobutton2104.set_sensitive(True)
        ProcessesGUI.radiobutton2105.set_sensitive(True)
        ProcessesGUI.radiobutton2106.set_sensitive(True)
        ProcessesGUI.radiobutton2104.set_tooltip_text(_tr("User defined expand"))
        ProcessesGUI.radiobutton2105.set_tooltip_text(_tr("Expand all"))
        ProcessesGUI.radiobutton2106.set_tooltip_text(_tr("Collapse all"))
    if checkbutton2102p.get_active() == False:
        # Set "User defined expand, Expand all, Collapse all" buttons as "insensitive" on the Processes tab if "show_processes_as_tree" option is disabled. Because expanding/collapsing treeview rows has no effects when treeview items are listed as "list". Also change widget tooltips for better understandability
        ProcessesGUI.radiobutton2104.set_sensitive(False)
        ProcessesGUI.radiobutton2105.set_sensitive(False)
        ProcessesGUI.radiobutton2106.set_sensitive(False)
        ProcessesGUI.radiobutton2104.set_tooltip_text(_tr("User defined expand\n(Usable if processes are listed as tree)"))
        ProcessesGUI.radiobutton2105.set_tooltip_text(_tr("Expand all\n(Usable if processes are listed as tree)"))
        ProcessesGUI.radiobutton2106.set_tooltip_text(_tr("Collapse all\n(Usable if processes are listed as tree)"))


# ----------------------------------- Processes - Processes Nice Error Dialog Function (shows an error dialog when nice is tried to increased (nice number decreased) for a process that owned by the user or nice is tried to increased/decreased for other users/system processes) -----------------------------------
def processes_nice_error_dialog():

    error_dialog2101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Access Denied"), )
    error_dialog2101.format_secondary_text(_tr("You have to have root privileges in order to:\n  1) Increase nice value of your processes\n  2) Increase/decrease nice value of other processes."))
    error_dialog2101.run()
    error_dialog2101.destroy()


# ----------------------------------- Processes - Processes End Process Warning Dialog Function (shows a warning dialog when a process is tried to be end) -----------------------------------
def processes_end_process_warning_dialog(process_name, process_pid):

    warning_dialog2101 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("End Process?"), )
    warning_dialog2101.format_secondary_text(_tr("Do you want to end the following process?\n ") + process_name + " (PID:" + str(process_pid) + ")")
    global warning_dialog2101_response
    warning_dialog2101_response = warning_dialog2101.run()
    warning_dialog2101.destroy()


# ----------------------------------- Processes - Processes End Process Tree Warning Dialog Function (shows a warning dialog when a process tree is tried to be end) -----------------------------------
def processes_end_process_tree_warning_dialog(process_name, process_pid):

    warning_dialog2102 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("End Process Tree?"), )
    warning_dialog2102.format_secondary_text(_tr("Do you want to end the following process and its child processes?\n ") + process_name + " (PID:" + str(process_pid) + ")")
    global warning_dialog2102_response
    warning_dialog2102_response = warning_dialog2102.run()
    warning_dialog2102.destroy()


# ----------------------------------- Processes - Processes No Path Error Dialog Function (shows an error dialog when process directory is tried to be opened and process directory could not be get) -----------------------------------
def processes_no_path_error_dialog():

    error_dialog2102 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Process Directory Could Not Be Get"), )
    error_dialog2102.format_secondary_text(_tr("Process directory could not be get.\nNo folder will be opened."))
    error_dialog2102.run()
    error_dialog2102.destroy()

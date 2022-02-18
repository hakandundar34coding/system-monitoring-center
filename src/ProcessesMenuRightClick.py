#!/usr/bin/env python3

# ----------------------------------- Processes - Processes Right Click Menu GUI Import Function -----------------------------------
def processes_menu_right_click_import_func():

    global Gtk, Gdk, os, signal, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import signal
    import subprocess


    global Config, Processes
    import Config, Processes


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Processes - Right Click Menu GUI Function -----------------------------------
def processes_menu_right_click_gui_func():

    # Define builder and get all objects (Processes Tab Right Click Menu) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesMenuRightClick.ui")


    # ********************** Define object names for Processes tab right click menu **********************
    global menu2101m
    global menuitem2101m, menuitem2102m, menuitem2103m, menuitem2104m, menuitem2106m
    global radiomenuitem2101m, radiomenuitem2102m, radiomenuitem2103m, radiomenuitem2104m, radiomenuitem2105m, normalmenuitem2101m

    # ********************** Get object names for Processes tab right click menu **********************
    menu2101m = builder.get_object('menu2101m')
    menuitem2101m = builder.get_object('menuitem2101m')
    menuitem2102m = builder.get_object('menuitem2102m')
    menuitem2103m = builder.get_object('menuitem2103m')
    menuitem2104m = builder.get_object('menuitem2104m')
    menuitem2106m = builder.get_object('menuitem2106m')
    radiomenuitem2101m = builder.get_object('radiomenuitem2101m')
    radiomenuitem2102m = builder.get_object('radiomenuitem2102m')
    radiomenuitem2103m = builder.get_object('radiomenuitem2103m')
    radiomenuitem2104m = builder.get_object('radiomenuitem2104m')
    radiomenuitem2105m = builder.get_object('radiomenuitem2105m')
    normalmenuitem2101m = builder.get_object('normalmenuitem2101m')

    # ********************** Define object functions for Processes tab right click menu **********************
    def on_menuitem2101m_activate(widget):                                                    # "Stop Process" item on the right click menu
        try:
            os.kill(int(Processes.selected_process_pid), signal.SIGSTOP)
        except PermissionError:
            try:
                (subprocess.check_output(["pkexec", "kill", "-19", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()    # Command output is not printed by using "stderr=subprocess.STDOUT".
            except subprocess.CalledProcessError:
                pass

    def on_menuitem2102m_activate(widget):                                                    # "Continue Process" item on the right click menu
        try:
            os.kill(int(Processes.selected_process_pid), signal.SIGCONT)
        except PermissionError:
            try:
                (subprocess.check_output(["pkexec", "kill", "-18", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()    # Command output is not printed by using "stderr=subprocess.STDOUT".
            except subprocess.CalledProcessError:
                pass

    def on_menuitem2103m_activate(widget):                                                    # "Terminate Process" item on the right click menu
        selected_process_pid = Processes.selected_process_pid
        selected_process_name = Processes.processes_data_rows[Processes.pid_list.index(selected_process_pid)][2]
        if Config.warn_before_stopping_processes == 1:
            processes_terminate_process_warning_dialog(selected_process_name, selected_process_pid)
            if warning_dialog2101_response == Gtk.ResponseType.YES:
                try:
                    os.kill(int(selected_process_pid), signal.SIGTERM)
                except PermissionError:
                    try:
                        (subprocess.check_output(["pkexec", "kill", "-15", selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()    # Command output is not printed by using "stderr=subprocess.STDOUT".
                    except subprocess.CalledProcessError:
                        pass
            if warning_dialog2101_response == Gtk.ResponseType.NO:
                pass                                                                          # Do nothing when "No" button is clicked. Dialog will be closed.
        if Config.warn_before_stopping_processes == 0:
            try:
                os.kill(selected_process_pid, signal.SIGTERM)
            except PermissionError:
                try:
                    (subprocess.check_output(["pkexec", "kill", "-15", selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()    # Command output is not printed by using "stderr=subprocess.STDOUT".
                except subprocess.CalledProcessError:
                    pass

    def on_menuitem2104m_activate(widget):                                                    # "Kill Process" item on the right click menu
        selected_process_pid = Processes.selected_process_pid
        selected_process_name = Processes.processes_data_rows[Processes.pid_list.index(selected_process_pid)][2]
        if Config.warn_before_stopping_processes == 1:
            processes_kill_process_warning_dialog(selected_process_name, selected_process_pid)
            if warning_dialog2102_response == Gtk.ResponseType.YES:
                try:
                    os.kill(int(selected_process_pid), signal.SIGKILL)
                except PermissionError:
                    try:
                        (subprocess.check_output(["pkexec", "kill", "-9", selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()    # Command output is not printed by using "stderr=subprocess.STDOUT".
                    except subprocess.CalledProcessError:
                        pass
            if warning_dialog2102_response == Gtk.ResponseType.NO:
                pass                                                                          # Do nothing when "No" button is clicked. Dialog will be closed.
        if Config.warn_before_stopping_processes == 0:
            try:
                os.kill(selected_process_pid, signal.SIGKILL)
            except PermissionError:
                try:
                    (subprocess.check_output(["pkexec", "kill", "-9", selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()    # Command output is not printed by using "stderr=subprocess.STDOUT".
                except subprocess.CalledProcessError:
                    pass

    def on_menuitem2106m_activate(widget):                                                    # "Details" item on the right click menu
        if 'ProcessesDetails' not in globals():
            global ProcessesDetails
            import ProcessesDetails
            ProcessesDetails.processes_details_import_func()
            ProcessesDetails.processes_details_gui_function()
        ProcessesDetails.window2101w.show()
        ProcessesDetails.process_details_run_func()

    def on_radiomenuitem2101m_activate(widget):                                               # "Very High" item on the right click menu under "Change Priorty (Nice)" item
        if radiomenuitem2101m.get_active() == True:
            try:
                (subprocess.check_output(["renice", "-n", "-20", "-p", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()    # Command output is not printed by using "stderr=subprocess.STDOUT".
            except subprocess.CalledProcessError:
                try:                                                                          # This "try-catch" is used in order to prevent errors if wrong password is used or polkit dialog is closed by user.
                    (subprocess.check_output(["pkexec", "renice", "-n", "-20", "-p", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
                except subprocess.CalledProcessError:
                    return

    def on_radiomenuitem2102m_activate(widget):                                               # "High" item on the right click menu under "Change Priorty (Nice)" item
        if radiomenuitem2102m.get_active() == True:
            try:
                (subprocess.check_output(["renice", "-n", "-10", "-p", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:
                try:
                    (subprocess.check_output(["pkexec", "renice", "-n", "-10", "-p", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
                except subprocess.CalledProcessError:
                    return

    def on_radiomenuitem2103m_activate(widget):                                               # "Normal" item on the right click menu under "Change Priorty (Nice)" item
        if radiomenuitem2103m.get_active() == True:
            try:
                (subprocess.check_output(["renice", "-n", "0", "-p", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:
                try:
                    (subprocess.check_output(["pkexec", "renice", "-n", "0", "-p", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
                except subprocess.CalledProcessError:
                    return

    def on_radiomenuitem2104m_activate(widget):                                               # "Low" item on the right click menu under "Change Priorty (Nice)" item
        if radiomenuitem2104m.get_active() == True:
            try:
                (subprocess.check_output(["renice", "-n", "10", "-p", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:
                try:
                    (subprocess.check_output(["pkexec", "renice", "-n", "10", "-p", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
                except subprocess.CalledProcessError:
                    return

    def on_radiomenuitem2105m_activate(widget):                                               # "Very Low" item on the right click menu under "Change Priorty (Nice)" item
        if radiomenuitem2105m.get_active() == True:
            try:
                (subprocess.check_output(["renice", "-n", "19", "-p", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:
                try:
                    (subprocess.check_output(["pkexec", "renice", "-n", "19", "-p", Processes.selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
                except subprocess.CalledProcessError:
                    return

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
    normalmenuitem2101m.connect("activate", on_normalmenuitem2101m_activate)
    global radiomenuitem2101m_handler_id, radiomenuitem2102m_handler_id, radiomenuitem2103m_handler_id, radiomenuitem2104m_handler_id, radiomenuitem2105m_handler_id
    radiomenuitem2101m_handler_id = radiomenuitem2101m.connect("activate", on_radiomenuitem2101m_activate)
    radiomenuitem2102m_handler_id = radiomenuitem2102m.connect("activate", on_radiomenuitem2102m_activate)
    radiomenuitem2103m_handler_id = radiomenuitem2103m.connect("activate", on_radiomenuitem2103m_activate)
    radiomenuitem2104m_handler_id = radiomenuitem2104m.connect("activate", on_radiomenuitem2104m_activate)
    radiomenuitem2105m_handler_id = radiomenuitem2105m.connect("activate", on_radiomenuitem2105m_activate)


# ----------------------------------- Processes - Select Process Nice Option Function (selects process nice option on the popup menu when right click operation is performed on process row on the treeview) -----------------------------------
def processes_select_process_nice_option_func():

    try:                                                                                      # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
        with open("/proc/" + Processes.selected_process_pid + "/stat") as reader:             # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
            proc_pid_stat_lines = reader.read()
    except FileNotFoundError:
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
        with open("/proc/" + Processes.selected_process_pid + "/stat") as reader:
            proc_pid_stat_lines_split = reader.read().split()
    except FileNotFoundError:
        return
    global selected_process_current_nice
    selected_process_current_nice = int(proc_pid_stat_lines_split[-34])                       # Get process nice value


# ----------------------------------- Processes - Processes Terminate Process Warning Dialog Function -----------------------------------
def processes_terminate_process_warning_dialog(process_name, process_pid):

    warning_dialog2101 = Gtk.MessageDialog(transient_for=Processes.grid2101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do you want to terminate this process?"), )
    warning_dialog2101.format_secondary_text(process_name + " (" + "PID" + ": " + str(process_pid) + ")")
    global warning_dialog2101_response
    warning_dialog2101_response = warning_dialog2101.run()
    warning_dialog2101.destroy()


# ----------------------------------- Processes - Processes Kill Process Warning Dialog Function -----------------------------------
def processes_kill_process_warning_dialog(process_name, process_pid):

    warning_dialog2102 = Gtk.MessageDialog(transient_for=Processes.grid2101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do you want to kill this process?"), )
    warning_dialog2102.format_secondary_text(process_name + " (" + "PID" + ": " + str(process_pid) + ")")
    global warning_dialog2102_response
    warning_dialog2102_response = warning_dialog2102.run()
    warning_dialog2102.destroy()

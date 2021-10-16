#!/usr/bin/env python3

# ----------------------------------- Processes - Processes Right Click Menu GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def processes_menu_right_click_import_func():

    global Gtk, Gdk, os, signal, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    import signal
    import subprocess


    global Config, MainGUI, Processes
    import Config, MainGUI, Processes


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


# ----------------------------------- Processes - Right Click Menu GUI Function (the code of this module in order to avoid running them during module import and defines menu GUI objects and functions/signals) -----------------------------------
def processes_menu_right_click_gui_func():

    # Define builder and get all objects (Processes Tab Right Click Menu) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesMenuRightClick.ui")


    # ********************** Define object names for Processes tab right click menu **********************
    global menu2101m
    global menuitem2101m, menuitem2102m, menuitem2103m, menuitem2104m, menuitem2106m, menuitem2107m, menuitem2108m
    global radiomenuitem2101m, radiomenuitem2102m, radiomenuitem2103m, radiomenuitem2104m, radiomenuitem2105m, normalmenuitem2101m

    # ********************** Get object names for Processes tab right click menu **********************
    menu2101m = builder.get_object('menu2101m')
    menuitem2101m = builder.get_object('menuitem2101m')
    menuitem2102m = builder.get_object('menuitem2102m')
    menuitem2103m = builder.get_object('menuitem2103m')
    menuitem2104m = builder.get_object('menuitem2104m')
    menuitem2106m = builder.get_object('menuitem2106m')
    menuitem2107m = builder.get_object('menuitem2107m')
    menuitem2108m = builder.get_object('menuitem2108m')
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
            os.system("pkexec kill -19 " + Processes.selected_process_pid)

    def on_menuitem2102m_activate(widget):                                                    # "Continue Process" item on the right click menu
        try:
            os.kill(int(Processes.selected_process_pid), signal.SIGCONT)
        except PermissionError:
            os.system("pkexec kill -18 " + Processes.selected_process_pid)

    def on_menuitem2103m_activate(widget):                                                    # "Terminate Process" item on the right click menu
        selected_process_pid = Processes.selected_process_pid
        selected_process_name = Processes.processes_data_rows[Processes.pid_list.index(selected_process_pid)][2]
        if Config.warn_before_stopping_processes == 1:
            processes_end_process_warning_dialog(selected_process_name, selected_process_pid)
            if warning_dialog2101_response == Gtk.ResponseType.YES:
                try:
                    os.kill(int(selected_process_pid), signal.SIGTERM)
                except PermissionError:
                    os.system("pkexec kill -15 " + selected_process_pid)
            if warning_dialog2101_response == Gtk.ResponseType.NO:
                pass                                                                          # Do nothing when "No" button is clicked. Dialog will be closed.
        if Config.warn_before_stopping_processes == 0:
            try:
                os.kill(selected_process_pid, signal.SIGTERM)
            except PermissionError:
                os.system("pkexec kill -15 " + selected_process_pid)

    def on_menuitem2104m_activate(widget):                                                    # "Kill Process" item on the right click menu
        selected_process_pid = Processes.selected_process_pid
        selected_process_name = Processes.processes_data_rows[Processes.pid_list.index(selected_process_pid)][2]
        if Config.warn_before_stopping_processes == 1:
            processes_end_process_warning_dialog(selected_process_name, selected_process_pid)
            if warning_dialog2101_response == Gtk.ResponseType.YES:
                try:
                    os.kill(int(selected_process_pid), signal.SIGKILL)
                except PermissionError:
                    os.system("pkexec kill -9 " + selected_process_pid)
            if warning_dialog2101_response == Gtk.ResponseType.NO:
                pass                                                                          # Do nothing when "No" button is clicked. Dialog will be closed.
        if Config.warn_before_stopping_processes == 0:
            try:
                os.kill(selected_process_pid, signal.SIGKILL)
            except PermissionError:
                os.system("pkexec kill -9 " + selected_process_pid)

    def on_menuitem2106m_activate(widget):                                                    # "Copy Name" item on the right click menu
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(Processes.processes_data_rows[Processes.pid_list.index(Processes.selected_process_pid)][2], -1)
        clipboard.store()

    def on_menuitem2107m_activate(widget):                                                    # "Open Location" item on the right click menu
        try:                                                                                  # Executable path of some of the processes may not be get without root privileges or may not be get due to the reason of some of the processes may not have a exe file. "try-except" is used to be able to avoid errors due to these reasons.
            full_path = os.path.realpath("/proc/" + Processes.selected_process_pid + "/exe")
        except:
            try:
                with open("/proc/" + Processes.selected_process_pid + "/cmdline") as reader:
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
        if 'ProcessesDetailsGUI' not in globals():                                            # Check if "ProcessesDetailsGUI" module is imported. Therefore it is not reimported for every click on "Details" menu item on the right click menu if "ProcessesDetailsGUI" name is in globals().
            global ProcessesDetailsGUI, ProcessesDetails
            import ProcessesDetailsGUI, ProcessesDetails
            ProcessesDetailsGUI.processes_details_gui_import_function()
            ProcessesDetailsGUI.processes_details_gui_function()
            ProcessesDetails.processes_details_import_func()
        ProcessesDetailsGUI.window2101w.show()
        ProcessesDetails.process_details_foreground_thread_run_func()

    def on_radiomenuitem2101m_activate(widget):                                               # "Very High" item on the right click menu under "Change Priorty (Nice)" item
        try:
            (subprocess.check_output("renice -n -20 -p " + Processes.selected_process_pid, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            (subprocess.check_output("pkexec renice -n -20 -p " + Processes.selected_process_pid, shell=True).strip()).decode()

    def on_radiomenuitem2102m_activate(widget):                                               # "High" item on the right click menu under "Change Priorty (Nice)" item
        try:
            (subprocess.check_output("renice -n -10 -p " + Processes.selected_process_pid, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            (subprocess.check_output("pkexec renice -n -10 -p " + Processes.selected_process_pid, shell=True).strip()).decode()

    def on_radiomenuitem2103m_activate(widget):                                               # "Normal" item on the right click menu under "Change Priorty (Nice)" item
        try:
            (subprocess.check_output("renice -n 0 -p " + Processes.selected_process_pid, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            (subprocess.check_output("pkexec renice -n 0 -p " + Processes.selected_process_pid, shell=True).strip()).decode()

    def on_radiomenuitem2104m_activate(widget):                                               # "Low" item on the right click menu under "Change Priorty (Nice)" item
        try:
            (subprocess.check_output("renice -n 10 -p " + Processes.selected_process_pid, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            (subprocess.check_output("pkexec renice -n 10 -p " + Processes.selected_process_pid, shell=True).strip()).decode()

    def on_radiomenuitem2105m_activate(widget):                                               # "Very Low" item on the right click menu under "Change Priorty (Nice)" item
        try:
            (subprocess.check_output("renice -n 19 -p " + Processes.selected_process_pid, shell=True).strip()).decode()
        except subprocess.CalledProcessError:
            (subprocess.check_output("pkexec renice -n 19 -p " + Processes.selected_process_pid, shell=True).strip()).decode()

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


# ----------------------------------- Processes - Select Process Nice Option Function (selects process nice option on the popup menu when right click operation is performed on process row on the treeview) -----------------------------------
def processes_select_process_nice_option_func():

    try:                                                                                      # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
        with open("/proc/" + Processes.selected_process_pid + "/stat") as reader:             # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
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
        with open("/proc/" + Processes.selected_process_pid + "/stat") as reader:
            proc_pid_stat_lines_split = reader.read().split()
    except FileNotFoundError:
        return
    global selected_process_current_nice
    selected_process_current_nice = int(proc_pid_stat_lines_split[-34])                       # Get process nice value


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

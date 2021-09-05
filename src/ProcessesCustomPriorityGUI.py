#!/usr/bin/env python3

# ----------------------------------- Processes - Processes Custom Priority Window GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def processes_custom_priority_import_func():

    global Gtk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os
    import subprocess


    global Processes, ProcessesGUI, ProcessesCustomPriorityGUI, MainGUI
    import Processes, ProcessesGUI, ProcessesCustomPriorityGUI, MainGUI


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


# ----------------------------------- Processes - Processes Custom Priority Window GUI Function (the code of this module in order to avoid running them during module import and defines "Processes" tab GUI objects and functions/signals) -----------------------------------
def processes_custom_priority_gui_func():

    global builder2101w2, window2101w2
    global scale2101w2, adjustment2101w2, label2101w2, button2101w2, button2102w2


    # Processes Custom Priority window GUI objects - get
    builder2101w2 = Gtk.Builder()
    builder2101w2.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesCustomPriorityWindow.glade")

    window2101w2 = builder2101w2.get_object('window2101w2')

    scale2101w2 = builder2101w2.get_object('scale2101w2')
    adjustment2101w2 = builder2101w2.get_object('adjustment2101w2')
    label2101w2 = builder2101w2.get_object('label2101w2')
    button2101w2 = builder2101w2.get_object('button2101w2')
    button2102w2 = builder2101w2.get_object('button2102w2')


    # Processes Custom Priority window GUI functions
    def on_window2101w2_delete_event(widget, event):
        window2101w2.hide()
        return True

    def on_window2101w2_show(widget):                                                         # Get process name and nice value (on window show) by using process PID.
        global selected_process_pid, selected_process_name, selected_process_nice
        selected_process_pid = ProcessesGUI.selected_process_pid
        try:                                                                                  # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
            with open("/proc/" + ProcessesGUI.selected_process_pid + "/stat") as reader:      # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
                proc_pid_stat_lines = reader.read()
        except FileNotFoundError:
            processes_no_such_process_error_dialog()
            return
        # Get process name and nice value
        proc_pid_stat_lines_split = proc_pid_stat_lines.split()
        first_parentheses = proc_pid_stat_lines.find("(")                                     # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
        second_parentheses = proc_pid_stat_lines.rfind(")")                                   # Last parantheses ")" index is get by using "find()".
        process_name_from_stat = proc_pid_stat_lines[first_parentheses+1:second_parentheses]  # Process name is get from string by using the indexes get previously.
        selected_process_name = process_name_from_stat
        if len(selected_process_name) >= 15:                                                  # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name. "=15" is enough but this limit may be increased in the next releases of the kernel. ">=15" is used in order to handle this possible change.
            with open("/proc/" + pid + "/cmdline") as reader:
                selected_process_name = ''.join(reader.read().split("/")[-1].split("\x00"))   # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()" and joined again without these characters.
            if selected_process_name.startswith(process_name_from_stat) == False:
                selected_process_name = process_name_from_stat                                # Root access is needed for reading "cmdline" file of the some processes. Otherwise it gives "" as output. Process name from "stat" file of the process is used is this situation. Also process name from "stat" file is used if name from "cmdline" does not start with name from "stat" file.
        selected_process_nice = int(proc_pid_stat_lines_split[-34])
        adjustment2101w2.configure(selected_process_nice, -20, 19, 1, 0, 0)
        label2101w2.set_text(f'{selected_process_name} - (PID: {selected_process_pid})')

    def on_button2101w2_clicked(widget):                                                      # "Cancel" button
        window2101w2.hide()                                                                   # Hide window without nice value change.

    def on_button2102w2_clicked(widget):                                                      # "Apply" button
        processes_get_process_current_nice_func()
        selected_process_nice = int(adjustment2101w2.get_value())
        if selected_process_current_nice <= selected_process_nice:
            (subprocess.check_output("renice -n " + str(selected_process_nice) + " -p " + selected_process_pid, shell=True).strip()).decode()    # It gives "renice: failed to set priority for [PID] (process ID): Access denied" output if application is not run with root privileges.
        if selected_process_current_nice > selected_process_nice:
            try:
                (subprocess.check_output("pkexec renice -n " + str(selected_process_nice) + " -p " + selected_process_pid, shell=True).strip()).decode()    # It gives "renice: failed to set priority for [PID] (process ID): Access denied" output if application is not run with root privileges.
            except subprocess.CalledProcessError:
                processes_nice_error_dialog()
        window2101w2.hide()



    # Processes Custom Priority window GUI functions - connect
    window2101w2.connect("delete-event", on_window2101w2_delete_event)
    window2101w2.connect("show", on_window2101w2_show)
    button2101w2.connect("clicked", on_button2101w2_clicked)
    button2102w2.connect("clicked", on_button2102w2_clicked)


# ----------------------------------- Processes - Get Process Current Nice Function (get process current nice value in order to check if root privileges are needed for nice changing operation) -----------------------------------
def processes_get_process_current_nice_func():

    try:                                                                                      # Process may be ended just after right click on the process row is performed. "try-catch" is used for avoiding errors in this situation.
        with open("/proc/" + ProcessesGUI.selected_process_pid + "/stat") as reader:
            proc_pid_stat_lines_split = reader.read().split()
    except FileNotFoundError:
        return
    global selected_process_current_nice
    selected_process_current_nice = int(proc_pid_stat_lines_split[-34])                       # Get process nice value


# ----------------------------------- Processes - Processes No Such Process Error Dialog Function (shows an error dialog and stops showing the "Set Process Custom Priority window" when the process is not alive anymore) -----------------------------------
def processes_no_such_process_error_dialog():

    error_dialog2101w2 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Process Is Not Running Anymore"), )
    error_dialog2101w2.format_secondary_text(_tr("Following process is not running anymore \nand process custom priority window is closed automatically:\n ") + selected_process_name + _tr(" (PID: ") + selected_process_pid)
    error_dialog2101w2.run()
    error_dialog2101w2.destroy()


# ----------------------------------- Processes - Processes Nice Error Dialog Function (shows an error dialog when nice is tried to increased (nice number decreased) for a process that owned by the user or nice is tried to increased/decreased for other users/system processes) -----------------------------------
def processes_nice_error_dialog():

    error_dialog2101w2 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Access Denied"), )
    error_dialog2101w2.format_secondary_text(_tr("You have to have root privileges in order to:\n  1) Increase nice value of your processes\n  2) Increase/decrease nice value of other processes."))
    error_dialog2101w2.run()
    error_dialog2101w2.destroy()

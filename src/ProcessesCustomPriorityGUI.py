#!/usr/bin/env python3

# ----------------------------------- Processes - Processes Custom Priority Window GUI Import Function -----------------------------------
def processes_custom_priority_import_func():

    global Gtk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os
    import subprocess


    global Processes, ProcessesMenuRightClick
    import Processes, ProcessesMenuRightClick


# ----------------------------------- Processes - Processes Custom Priority Window GUI Function -----------------------------------
def processes_custom_priority_gui_func():

    global builder2101w2, window2101w2
    global scale2101w2, adjustment2101w2, label2101w2, button2101w2, button2102w2


    # Processes Custom Priority window GUI objects - get
    builder2101w2 = Gtk.Builder()
    builder2101w2.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesCustomPriorityWindow.ui")

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
        selected_process_pid = Processes.selected_process_pid
        try:                                                                              # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
            with open(f'/proc/{Processes.selected_process_pid}/stat') as reader:          # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
                proc_pid_stat_lines = reader.read()
        except FileNotFoundError:
            window2101w2.hide()
            return
        # Get process name and nice value
        proc_pid_stat_lines_split = proc_pid_stat_lines.split()
        first_parentheses = proc_pid_stat_lines.find("(")                                     # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
        second_parentheses = proc_pid_stat_lines.rfind(")")                                   # Last parantheses ")" index is get by using "find()".
        process_name_from_stat = proc_pid_stat_lines[first_parentheses+1:second_parentheses]  # Process name is get from string by using the indexes get previously.
        selected_process_name = process_name_from_stat
        if len(selected_process_name) == 15:                                              # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name.
            try:
                with open(f'/proc/{selected_process_pid}/cmdline') as reader:
                    process_cmdline = reader.read()
                selected_process_name = process_cmdline.split("/")[-1].split("\x00")[0]       # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()".
            except FileNotFoundError:                                                         # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
                window2101w2.hide()
                return
            if selected_process_name.startswith(process_name_from_stat) == False:
                selected_process_name = process_cmdline.split(" ")[0].split("\x00")[0].strip()    # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()".
                if selected_process_name.startswith(process_name_from_stat) == False:
                    selected_process_name = process_cmdline.split("\x00")[0].split("/")[-1].strip()
                    if selected_process_name.startswith(process_name_from_stat) == False:
                        selected_process_name = process_name_from_stat                        # Root access is needed for reading "cmdline" file of the some processes. Otherwise it gives "" as output. Process name from "stat" file of the process is used is this situation. Also process name from "stat" file is used if name from "cmdline" does not start with name from "stat" file.
        selected_process_nice = int(proc_pid_stat_lines_split[-34])
        adjustment2101w2.configure(selected_process_nice, -20, 19, 1, 0, 0)
        label2101w2.set_text(f'{selected_process_name} - (PID: {selected_process_pid})')

    def on_button2101w2_clicked(widget):                                                      # "Cancel" button
        window2101w2.hide()                                                                   # Hide window without nice value change.

    def on_button2102w2_clicked(widget):                                                      # "Apply" button
        processes_get_process_current_nice_func()
        selected_process_nice = str(int(adjustment2101w2.get_value()))
        try:
            (subprocess.check_output(["renice", "-n", selected_process_nice, "-p", selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()    # Command output is not printed by using "stderr=subprocess.STDOUT".
        except subprocess.CalledProcessError:
            try:                                                                              # This "try-catch" is used in order to prevent errors if wrong password is used or polkit dialog is closed by user.
                (subprocess.check_output(["pkexec", "renice", "-n", selected_process_nice, "-p", selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:
                return
        window2101w2.hide()


    # Processes Custom Priority window GUI functions - connect
    window2101w2.connect("delete-event", on_window2101w2_delete_event)
    window2101w2.connect("show", on_window2101w2_show)
    button2101w2.connect("clicked", on_button2101w2_clicked)
    button2102w2.connect("clicked", on_button2102w2_clicked)


# ----------------------------------- Processes - Get Process Current Nice Function (get process current nice value in order to check if root privileges are needed for nice changing operation) -----------------------------------
def processes_get_process_current_nice_func():

    try:                                                                                  # Process may be ended just after right click on the process row is performed. "try-catch" is used for avoiding errors in this situation.
        with open(f'/proc/{Processes.selected_process_pid}/stat') as reader:
            proc_pid_stat_lines_split = reader.read().split()
    except FileNotFoundError:
        return
    global selected_process_current_nice
    selected_process_current_nice = int(proc_pid_stat_lines_split[-34])                       # Get process nice value

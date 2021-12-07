#!/usr/bin/env python3

# ----------------------------------- Processes - Processes Details Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def processes_details_import_func():

    global Gtk, GLib, os, Thread, time, datetime

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    import os
    from threading import Thread
    import time
    from datetime import datetime


    global Config, Processes, MainGUI
    import Config, Processes, MainGUI


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


# ----------------------------------- Processes - Processes Details Window GUI Function (the code of this module in order to avoid running them during module import and defines "Processes Details" window GUI objects and functions/signals) -----------------------------------
def processes_details_gui_function():

    # Processes Details window GUI objects
    global builder2101w, window2101w, notebook2101w
    global label2101w, label2102w, label2103w, label2104w, label2105w, label2106w, label2107w, label2108w, label2109w, label2110w
    global label2111w, label2112w, label2113w, label2114w, label2115w, label2116w, label2117w, label2118w, label2119w, label2120w
    global label2121w, label2122w, label2123w, label2124w, label2125w, label2126w, label2127w, label2128w, label2129w, label2130w
    global label2131w, label2132w, label2133w, label2134w, label2135w, label2136w, label2137w


    # Processes Details window GUI objects - get
    builder2101w = Gtk.Builder()
    builder2101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesDetailsWindow.ui")

    window2101w = builder2101w.get_object('window2101w')

    notebook2101w = builder2101w.get_object('notebook2101w')

    # Process Details window "Summary" tab GUI objects
    label2101w = builder2101w.get_object('label2101w')
    label2102w = builder2101w.get_object('label2102w')
    label2103w = builder2101w.get_object('label2103w')
    label2104w = builder2101w.get_object('label2104w')
    label2105w = builder2101w.get_object('label2105w')
    label2106w = builder2101w.get_object('label2106w')
    label2107w = builder2101w.get_object('label2107w')
    label2108w = builder2101w.get_object('label2108w')
    label2109w = builder2101w.get_object('label2109w')
    label2110w = builder2101w.get_object('label2110w')
    label2111w = builder2101w.get_object('label2111w')
    label2112w = builder2101w.get_object('label2112w')
    label2113w = builder2101w.get_object('label2113w')
    label2114w = builder2101w.get_object('label2114w')
    label2115w = builder2101w.get_object('label2115w')

    # Process Details window "CPU and RAM" tab GUI objects
    label2116w = builder2101w.get_object('label2116w')
    label2117w = builder2101w.get_object('label2117w')
    label2118w = builder2101w.get_object('label2118w')
    label2119w = builder2101w.get_object('label2119w')
    label2120w = builder2101w.get_object('label2120w')
    label2121w = builder2101w.get_object('label2121w')
    label2122w = builder2101w.get_object('label2122w')
    label2123w = builder2101w.get_object('label2123w')
    label2124w = builder2101w.get_object('label2124w')
    label2125w = builder2101w.get_object('label2125w')
    label2126w = builder2101w.get_object('label2126w')
    label2127w = builder2101w.get_object('label2127w')

    # Process Details window "Disk and Path" tab GUI objects
    label2128w = builder2101w.get_object('label2128w')
    label2129w = builder2101w.get_object('label2129w')
    label2130w = builder2101w.get_object('label2130w')
    label2131w = builder2101w.get_object('label2131w')
    label2132w = builder2101w.get_object('label2132w')
    label2133w = builder2101w.get_object('label2133w')
    label2134w = builder2101w.get_object('label2134w')
    label2135w = builder2101w.get_object('label2135w')
    label2136w = builder2101w.get_object('label2136w')
    label2137w = builder2101w.get_object('label2137w')


    # Processes Details window GUI functions
    def on_window2101w_delete_event(widget, event):
        window2101w.hide()
        return True

    def on_window2101w_show(widget):
        processes_details_gui_reset_function()                                                # Call this function in order to reset Processes Details window. Data from previous process remains visible (for a short time) until getting and showing new process data if window is closed and opened for an another process. Also last selected tab remains same because window is made hidden when close button is clicked.
        processes_details_tab_switch_control_func()


    # Processes Details window GUI functions - connect
    window2101w.connect("delete-event", on_window2101w_delete_event)
    window2101w.connect("show", on_window2101w_show)


# ----------------------------------- Processes - Processes Details Window GUI Reset Function (resets Processes Details window) -----------------------------------
def processes_details_gui_reset_function():

    notebook2101w.set_current_page(0)                                                         # Set fist page (Summary tab) of the notebook
    label2101w.set_text("--")
    label2102w.set_text("--")
    label2103w.set_text("--")
    label2104w.set_text("--")
    label2105w.set_text("--")
    label2106w.set_text("--")
    label2107w.set_text("--")
    label2108w.set_text("--")
    label2109w.set_text("--")
    label2110w.set_text("--")
    label2111w.set_text("--")
    label2112w.set_text("--")
    label2113w.set_text("--")
    label2114w.set_text("--")
    label2115w.set_text("--")
    label2116w.set_text("--")
    label2117w.set_text("--")
    label2118w.set_text("--")
    label2119w.set_text("--")
    label2120w.set_text("--")
    label2121w.set_text("--")
    label2122w.set_text("--")
    label2123w.set_text("--")
    label2124w.set_text("--")
    label2125w.set_text("--")
    label2126w.set_text("--")
    label2127w.set_text("--")
    label2128w.set_text("--")
    label2129w.set_text("--")
    label2130w.set_text("--")
    label2131w.set_text("--")
    label2132w.set_text("--")
    label2133w.set_text("--")
    label2134w.set_text("--")
    label2135w.set_text("--")
    label2136w.set_text("--")
    label2137w.set_text("--")


# ----------------------------------- Processes - Processes Details Tab Switch Control Function (controls if tab is switched and updates data on the last opened tab immediately without waiting end of the update interval. Signals of notebook for tab switching is not useful because it performs the action and after that it switches the tab. Data updating function does not recognizes tab switch due to this reason.) -----------------------------------
def processes_details_tab_switch_control_func():

    global previous_page
    if 'previous_page' not in globals():                                                      # For avoiding errors in the first loop of the control
        previous_page = None
        current_page = None
    current_page = notebook2101w.get_current_page()
    if current_page != previous_page and previous_page != None:                               # Check if tab is switched
        process_details_foreground_func()                                                     # Update the data on the tab
    previous_page = current_page
    if window2101w.get_visible() == True:
        GLib.timeout_add(200, processes_details_tab_switch_control_func)                      # Check is performed in every 200 ms which is small enough for immediate update and not very frequent for avoiding high CPU usages.


# ----------------------------------- Processes - Processes Details Function (the code of this module in order to avoid running them during module import and defines "Processes" tab GUI objects and functions/signals) -----------------------------------
def process_details_initial_func():

    processes_details_define_data_unit_converter_variables_func()                             # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    global process_status_list, global_process_cpu_times_prev, disk_read_write_data_prev, fd_mode_dict
    process_status_list = Processes.process_status_list
    global_process_cpu_times_prev = []
    disk_read_write_data_prev = []
    fd_mode_dict = {32768: "r", 32769: "w", 33793: "a", 32770: "w+", 33794: "a+"}

    # Get system boot time
    global system_boot_time
    with open("/proc/stat") as reader:
        stat_lines = reader.read().split("\n")
    for line in stat_lines:
        if "btime " in line:
            system_boot_time = int(line.split()[1].strip())


# ----------------------------------- Processes - Processes Details Foreground Function (updates the process data on the "Processes Details" window) -----------------------------------
def process_details_foreground_func():

    processes_cpu_usage_percent_precision = Config.processes_cpu_usage_percent_precision
    processes_ram_swap_data_precision = Config.processes_ram_swap_data_precision
    processes_ram_swap_data_unit = Config.processes_ram_swap_data_unit
    processes_disk_speed_data_precision = Config.processes_disk_speed_data_precision
    processes_disk_speed_data_unit = Config.processes_disk_speed_data_unit

    global global_process_cpu_times_prev, disk_read_write_data_prev
    global system_boot_time

    # Get human and root user usernames and UIDs only one time at the per loop in order to avoid running it per process loop (it is different than main loop = processes_loop_func) which increases CPU consumption.
    usernames_username_list = []
    usernames_uid_list = []
    with open("/etc/passwd") as reader:                                                       # "/etc/passwd" file (also knonw as Linux password database) contains all local user (system + human users) information.
        etc_passwd_lines = reader.read().strip().split("\n")                                  # "strip()" is used in order to prevent errors due to an empty line at the end of the list.
    for line in etc_passwd_lines:
        line_splitted = line.split(":")
        usernames_username_list.append(line_splitted[0])
        usernames_uid_list.append(line_splitted[2])

    global selected_process_pid
    selected_process_pid = Processes.selected_process_pid                                     # Get "selected_process_pid" from module "ProcessesGUI".

    number_of_clock_ticks = Processes.number_of_clock_ticks
    global_cpu_time_all = time.time() * number_of_clock_ticks                                 # global_cpu_time_all value is get just before "/proc/[PID]/stat file is read in order to measure global an process specific CPU times at the same time (nearly) for ensuring accurate process CPU usage percent. global_cpu_time_all value is get by using time module of Python instead of reading "/proc/stat" file for faster processing.
    try:                                                                                      # Process may be ended. "try-catch" is used for avoiding errors in this situation.
        with open("/proc/" + selected_process_pid + "/stat") as reader:                       # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
            proc_pid_stat_lines = reader.read()
    except FileNotFoundError:
        window2101w.hide()
        processes_no_such_process_error_dialog()
        return
    proc_pid_stat_lines_split = proc_pid_stat_lines.split()
    first_parentheses = proc_pid_stat_lines.find("(")                                         # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
    second_parentheses = proc_pid_stat_lines.rfind(")")                                       # Last parantheses ")" index is get by using "find()".
    process_name_from_stat = proc_pid_stat_lines[first_parentheses+1:second_parentheses]      # Process name is get from string by using the indexes get previously.
    selected_process_name = process_name_from_stat
    if len(selected_process_name) == 15:                                                      # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name.
        try:
            with open("/proc/" + selected_process_pid + "/cmdline") as reader:
                process_cmdline = reader.read()
            selected_process_name = process_cmdline.split("/")[-1].split("\x00")[0]           # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()".
        except FileNotFoundError:                                                             # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
            window2101w.hide()
            processes_no_such_process_error_dialog()
            return
        if selected_process_name.startswith(process_name_from_stat) == False:
            selected_process_name = process_cmdline.split(" ")[0].split("\x00")[0].strip()    # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()".
            if selected_process_name.startswith(process_name_from_stat) == False:
                selected_process_name = process_cmdline.split("\x00")[0].split("/")[-1].strip()
                if selected_process_name.startswith(process_name_from_stat) == False:
                    selected_process_name = process_name_from_stat                            # Root access is needed for reading "cmdline" file of the some processes. Otherwise it gives "" as output. Process name from "stat" file of the process is used is this situation. Also process name from "stat" file is used if name from "cmdline" does not start with name from "stat" file.
    selected_process_icon = "system-monitoring-center-process-symbolic"                       # Initial value of the "selected_process_icon". This icon will be shown for processes of which icon could not be found in default icon theme.
    if selected_process_name in Processes.application_exec_list:                              # Use process icon name from application file if process name is found in application exec list
        selected_process_icon = Processes.application_icon_list[Processes.application_exec_list.index(selected_process_name)]

    window2101w.set_title(_tr("Process Details: ") + selected_process_name + " - (" + "PID: " + selected_process_pid + ")")    # Set window title
    window2101w.set_icon_name(selected_process_icon)                                          # Set ProcessesDetails window icon


    # Show and update process details on the "Summary" tab
    if notebook2101w.get_current_page() == 0:
        # Get process status
        selected_process_status = process_status_list[proc_pid_stat_lines_split[-50]]         # Get process status
        # Get process user name
        try:                                                                                  # Process may be ended. "try-catch" is used for avoiding errors in this situation.
            with open("/proc/" + selected_process_pid + "/status") as reader:                 # User name of the process owner is get from "/proc/status" file because it is present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                proc_pid_status_lines = reader.read().split("\n")
        except FileNotFoundError:
            window2101w.hide()
            processes_no_such_process_error_dialog()
            return
        for line in proc_pid_status_lines:
            if "Uid:\t" in line:
                real_user_id = line.split(":")[1].split()[0].strip()                          # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                selected_process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
        # Get process nice
        selected_process_nice = int(proc_pid_stat_lines_split[-34])
        # Calculate CPU usage percent of the selected process
        process_cpu_time = int(proc_pid_stat_lines_split[-39]) + int(proc_pid_stat_lines_split[-38])   # Get process cpu time in user mode (utime + stime)
        global_process_cpu_times = [global_cpu_time_all, process_cpu_time]
        if global_process_cpu_times_prev == []:
            process_cpu_time_prev = process_cpu_time                                          # There is no "process_cpu_time_prev" value and get it from "process_cpu_time"  if this is first loop of the process
            global_cpu_time_all_prev = global_process_cpu_times[0] - 1                        # Subtract "1" CPU time (a negligible value) if this is first loop of the process
        if global_process_cpu_times_prev != []:
            global_cpu_time_all_prev, process_cpu_time_prev = global_process_cpu_times_prev
        process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
        global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
        selected_process_cpu_percent = process_cpu_time_difference / global_cpu_time_difference * 100 / Processes.number_of_logical_cores
        global_process_cpu_times_prev = global_process_cpu_times
        # Get RAM (RSS) data
        selected_process_memory_rss = int(proc_pid_stat_lines_split[-29]) * Processes.memory_page_size    # Get process RSS (resident set size) memory pages and multiply with memory_page_size in order to convert the value into bytes.
        # Get disk read data, disk write data
        try:                                                                                  # Root access is needed for reading "/proc/[PID]/io" file else it gives error. "try-except" is used in order to avoid this error if user has no root privileges.
            with open("/proc/" + selected_process_pid + "/io") as reader:
                proc_pid_io_lines = reader.read().split("\n")
            selected_process_read_bytes = int(proc_pid_io_lines[4].split(":")[1])
            selected_process_write_bytes = int(proc_pid_io_lines[5].split(":")[1])
        except PermissionError:
            selected_process_read_bytes = 0
            selected_process_write_bytes = 0
        # Get disk read speed, disk write speed
        disk_read_write_data = [selected_process_read_bytes, selected_process_write_bytes]
        if disk_read_write_data_prev == []:
            selected_process_read_bytes_prev = selected_process_read_bytes                    # Make process_read_bytes_prev equal to process_read_bytes for giving "0" disk read speed value if this is first loop of the process
        else:
            selected_process_read_bytes_prev = disk_read_write_data_prev[0]
        selected_process_read_speed = (selected_process_read_bytes - int(selected_process_read_bytes_prev)) / update_interval    # Append process_read_bytes which will be used as "process_read_bytes_prev" value in the next loop and also append disk read speed. 
        if disk_read_write_data_prev == []:
            selected_process_write_bytes_prev = selected_process_write_bytes                  # Make process_write_bytes_prev equal to process_write_bytes for giving "0" disk write speed value if this is first loop of the process
        else:
            selected_process_write_bytes_prev = disk_read_write_data_prev[1]
        selected_process_write_speed = (selected_process_write_bytes - int(selected_process_write_bytes_prev)) / update_interval    # Append process_read_bytes which will be used as "process_read_bytes_prev" value in the next loop and also append disk read speed. 
        disk_read_write_data_prev = disk_read_write_data
        # Get process start time
        try:
            with open("/proc/" + selected_process_pid + "/stat") as reader:
                proc_pid_stat_lines = int(reader.read().split()[-31])                         # Elapsed time between system boot and process start time (measured in clock ticks and need to be divided by sysconf(_SC_CLK_TCK) for converting into wall clock time)
        except Exception:
            window2101w.hide()
            processes_no_such_process_error_dialog()
            return
        selected_process_start_time = (proc_pid_stat_lines / number_of_clock_ticks) + system_boot_time
        # Get process ppid
        selected_process_ppid = int(proc_pid_stat_lines_split[-49])                           # Get process PPID
        # Get process exe
        try:                                                                                  # Executable path of some of the processes may not be get without root privileges or may not be get due to the reason of some of the processes may not have a exe file. "try-except" is used to be able to avoid errors due to these reasons.
            selected_process_exe = os.path.realpath("/proc/" + pid + "/exe")
        except Exception:
            selected_process_exe = "-"
        # Get parent processes name and PIDs
        parent_process_names_pids = []
        current_ppid = selected_process_pid                                                   # Define "current_ppid" as "selected_process_pid". They are not same thing for the initial value but it is defined as initial value for proper working of the ppid loop code.
        while current_ppid != 0:
            with open("/proc/" + str(current_ppid) + "/stat") as reader:
                current_ppid = int(reader.read().split()[-49])
            if current_ppid != 0:
                with open("/proc/" + str(current_ppid) + "/stat") as reader:
                    proc_pid_stat_lines = reader.read()
                first_parentheses = proc_pid_stat_lines.find("(")                             # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
                second_parentheses = proc_pid_stat_lines.rfind(")")                           # Last parantheses ")" index is get by using "find()".
                process_name_from_stat = proc_pid_stat_lines[first_parentheses+1:second_parentheses]    # Process name is get from string by using the indexes get previously.
                process_name = process_name_from_stat
                if len(process_name) >= 15:                                                   # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name. "=15" is enough but this limit may be increased in the next releases of the kernel. ">=15" is used in order to handle this possible change.
                    with open("/proc/" + str(current_ppid) + "/cmdline") as reader:
                        process_name = ''.join(reader.read().split("/")[-1].split("\x00"))    # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()" and joined again without these characters.
                    if process_name.startswith(process_name_from_stat) == False:
                        process_name = process_name_from_stat
                parent_process_names_pids.append(f'{process_name} (PID: {current_ppid})')
        # Get child process names and PIDs
        pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]
        ppid_list = []
        for pid in pid_list[:]:                                                               # "[:]" is used for iterating over copy of the list because element are removed during iteration. Otherwise incorrect operations (incorrect element removal) are performed on the list.
            try:                                                                              # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
                with open("/proc/" + pid + "/stat") as reader:                                # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
                    proc_pid_stat_lines = reader.read()
            except FileNotFoundError:                                                         # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
                pid_list.remove(pid)
                continue
            proc_pid_stat_lines_split = proc_pid_stat_lines.split()
            ppid_list.append(proc_pid_stat_lines_split[-49])
        selected_process_child_process_pids = []
        for i, ppid in enumerate(ppid_list):
            if ppid == selected_process_pid:
                selected_process_child_process_pids.append(pid_list[i])
        selected_process_child_process_names = []
        for pid in selected_process_child_process_pids:
            try:                                                                              # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
                with open("/proc/" + pid + "/stat") as reader:                                # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
                    proc_pid_stat_lines = reader.read()
            except FileNotFoundError:                                                         # Removed pid from "selected_process_child_process_pids" and skip to next loop (pid) if process is ended just after selected_process_child_process_pids is generated.
                selected_process_child_process_pids.remove(pid)
                continue
            first_parentheses = proc_pid_stat_lines.find("(")                                 # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
            second_parentheses = proc_pid_stat_lines.rfind(")")                               # Last parantheses ")" index is get by using "find()".
            process_name_from_stat = proc_pid_stat_lines[first_parentheses+1:second_parentheses]  # Process name is get from string by using the indexes get previously.
            process_name = process_name_from_stat
            if len(process_name) == 15:                                                       # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name.
                try:
                    with open("/proc/" + pid + "/cmdline") as reader:
                        process_name = reader.read().split("/")[-1].split("\x00")[0]          # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()".
                except FileNotFoundError:                                                     # Removed pid from "selected_process_child_process_pids" and skip to next loop (pid) if process is ended just after selected_process_child_process_pids is generated.
                    selected_process_child_process_pids.remove(pid)
                    continue
                if process_name.startswith(process_name_from_stat) == False:
                    process_name = process_name_from_stat                                     # Root access is needed for reading "cmdline" file of the some processes. Otherwise it gives "" as output. Process name from "stat" file of the process is used is this situation. Also process name from "stat" file is used if name from "cmdline" does not start with name from "stat" file.
            selected_process_child_process_names.append(process_name)
        child_process_names_pids = []
        for i, pid in enumerate(selected_process_child_process_pids):
            child_process_names_pids.append(f'{selected_process_child_process_names[i]} (PID: {pid})')
        # Get real, effective and saved UIDs
        for line in proc_pid_status_lines:
            if "Uid:\t" in line:
                line_split = line.split(":")[1].split()
                selected_process_uid_real = line_split[0].strip()                             # There are 4 values in the Uid line (real, effective, user, filesystem UIDs)
                selected_process_uid_effective = line_split[1].strip()
                selected_process_uid_saved = line_split[2].strip()
        # Get real, effective and saved GIDs
        for line in proc_pid_status_lines:
            if "Gid:\t" in line:
                line_split = line.split(":")[1].split()
                selected_process_gid_real = line_split[0].strip()                             # There are 4 values in the Gid line (real, effective, user, filesystem GIDs)
                selected_process_gid_effective = line_split[1].strip()
                selected_process_gid_saved = line_split[2].strip()
        # Set label text by using process data
        label2101w.set_text(selected_process_name)
        label2102w.set_text(f'{selected_process_pid}')
        label2103w.set_text(selected_process_status)
        label2104w.set_text(selected_process_username)
        label2105w.set_text(f'{selected_process_nice}')
        label2106w.set_text(f'{selected_process_cpu_percent:.{processes_cpu_usage_percent_precision}f} %')
        label2107w.set_text(f'{processes_details_data_unit_converter_func(selected_process_memory_rss, processes_ram_swap_data_unit, processes_ram_swap_data_precision)}')
        if selected_process_read_bytes != "-" and selected_process_write_bytes != "-":
            label2108w.set_text(f'{processes_details_data_unit_converter_func(selected_process_read_speed, processes_disk_speed_data_unit, processes_disk_speed_data_precision)} / {processes_details_data_unit_converter_func(selected_process_write_speed, processes_disk_speed_data_unit, processes_disk_speed_data_precision)}')
        if selected_process_read_bytes == "-" and selected_process_write_bytes == "-":
            label2108w.set_text("- / -")
        label2109w.set_text(datetime.fromtimestamp(selected_process_start_time).strftime("%d.%m.%Y %H:%M:%S"))
        label2110w.set_text(selected_process_exe)
        label2111w.set_text(f'{selected_process_ppid}')
        if parent_process_names_pids != []:
            label2112w.set_text(',\n'.join(parent_process_names_pids))
        if parent_process_names_pids == []:
            label2112w.set_text("-")
        if child_process_names_pids != []:
            label2113w.set_text(',\n'.join(child_process_names_pids))
        if child_process_names_pids == []:
            label2113w.set_text("-")
        label2114w.set_text(f'Real: {selected_process_uid_real}, Effective: {selected_process_uid_effective}, Saved: {selected_process_uid_saved}')
        label2115w.set_text(f'Real: {selected_process_gid_real}, Effective: {selected_process_gid_effective}, Saved: {selected_process_gid_saved}')


    # Show and update process details on the "CPU and Memory" tab
    if notebook2101w.get_current_page() == 1:
        # Calculate CPU usage percent of the selected process
        process_cpu_time = int(proc_pid_stat_lines_split[-39]) + int(proc_pid_stat_lines_split[-38])   # Get process cpu time in user mode (utime + stime)
        global_process_cpu_times = [global_cpu_time_all, process_cpu_time]
        if global_process_cpu_times_prev == []:
            process_cpu_time_prev = process_cpu_time                                          # There is no "process_cpu_time_prev" value and get it from "process_cpu_time"  if this is first loop of the process
            global_cpu_time_all_prev = global_process_cpu_times[0] - 1                        # Subtract "1" CPU time (a negligible value) if this is first loop of the process
        if global_process_cpu_times_prev != []:
            global_cpu_time_all_prev, process_cpu_time_prev = global_process_cpu_times_prev
        process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
        global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
        selected_process_cpu_percent = process_cpu_time_difference / global_cpu_time_difference * 100 / Processes.number_of_logical_cores
        global_process_cpu_times_prev = global_process_cpu_times
        # Get number of threads of the process
        selected_process_num_threads = proc_pid_stat_lines_split[-33]                         # Get process number of threads value
        # Get threads of the process
        selected_process_threads = [filename for filename in os.listdir("/proc/" + selected_process_pid + "/task/") if filename.isdigit()]    # Get process thread list (TIDs).
        # Get the last CPU core number which process executed on
        selected_process_cpu_num = proc_pid_stat_lines_split[-14]
        # Get CPU cores that process run allowed on
        try:                                                                                  # Process may be ended. "try-catch" is used for avoiding errors in this situation.
            with open("/proc/" + selected_process_pid + "/status") as reader:
                proc_pid_status_lines = reader.read().split("\n")
        except FileNotFoundError:
            window2101w.hide()
            processes_no_such_process_error_dialog()
            return
        for line in proc_pid_status_lines:
            if "Cpus_allowed_list:" in line:
                selected_process_cpus_allowed = line.split(":")[1].strip()
        # Get CPU times of the process
        selected_process_cpu_times_user = proc_pid_stat_lines_split[-39]
        selected_process_cpu_times_kernel = proc_pid_stat_lines_split[-38]
        selected_process_cpu_times_children_user = proc_pid_stat_lines_split[-37]
        selected_process_cpu_times_children_kernel = proc_pid_stat_lines_split[-36]
        selected_process_cpu_times_io_wait = proc_pid_stat_lines_split[-11]
        for line in proc_pid_status_lines:
            if "voluntary_ctxt_switches:" in line:
                selected_process_num_ctx_switches_voluntary = line.split(":")[1].strip()
        for line in proc_pid_status_lines:
            if "nonvoluntary_ctxt_switches:" in line:
                selected_process_num_ctx_switches_nonvoluntary = line.split(":")[1].strip()
        # Get RAM (RSS) data
        selected_process_memory_rss = int(proc_pid_stat_lines_split[-29]) * Processes.memory_page_size    # Get process RSS (resident set size) memory pages and multiply with memory_page_size in order to convert the value into bytes.
        # Get RAM (VMS) data
        selected_process_memory_vms = int(proc_pid_stat_lines_split[-30])                     # Get process VMS (virtual memory size) memory (this value is in bytes unit).
        # Get RAM (Shared) data
        with open("/proc/" + selected_process_pid + "/statm") as reader:                                   
            selected_process_memory_shared = int(reader.read().split()[2]) * Processes.memory_page_size    # Get shared memory pages and multiply with memory_page_size in order to convert the value into bytes.
        # Get USS (Unique Set Size) and swap memory data of the pprocess
        try:
            private_clean = 0
            private_dirty = 0
            memory_swap = 0
            with open("/proc/" + selected_process_pid + "/smaps") as reader:
                proc_pid_smaps_lines = reader.read().split("\n")
            for line in proc_pid_smaps_lines:
                if "Private_Clean:" in line:
                    private_clean = private_clean + int(line.split(":")[1].split()[0].strip())
                if "Private_Dirty:" in line:
                    private_dirty = private_dirty + int(line.split(":")[1].split()[0].strip())
                if line.startswith("Swap:"):
                    memory_swap = memory_swap + int(line.split(":")[1].split()[0].strip())
            selected_process_memory_uss = (private_clean + private_dirty) * 1024              # Kilobytes value converted into bytes value (there is a negligible deviation in bytes unit)
            selected_process_memory_swap = memory_swap * 1024                                 # Kilobytes value converted into bytes value (there is a negligible deviation in bytes unit)
        except Exception:
            selected_process_memory_uss = "-"
            selected_process_memory_swap = "-"
        # Set label text by using process data
        label2116w.set_text(f'{selected_process_cpu_percent:.{processes_cpu_usage_percent_precision}f} %')
        label2117w.set_text(f'{selected_process_num_threads}')
        label2118w.set_text(',\n'.join(selected_process_threads))
        label2119w.set_text(f'{selected_process_cpu_num}')
        label2120w.set_text(selected_process_cpus_allowed)
        label2121w.set_text(f'User: {selected_process_cpu_times_user}, System: {selected_process_cpu_times_kernel}, Children User: {selected_process_cpu_times_children_user}, Children System: {selected_process_cpu_times_children_kernel}, IO Wait: {selected_process_cpu_times_io_wait}')
        label2122w.set_text(f'Voluntary: {selected_process_num_ctx_switches_voluntary}, Involuntary: {selected_process_num_ctx_switches_nonvoluntary}')
        label2123w.set_text(f'{processes_details_data_unit_converter_func(selected_process_memory_rss, processes_ram_swap_data_unit, processes_ram_swap_data_precision)}')
        label2124w.set_text(f'{processes_details_data_unit_converter_func(selected_process_memory_vms, processes_ram_swap_data_unit, processes_ram_swap_data_precision)}')
        label2125w.set_text(f'{processes_details_data_unit_converter_func(selected_process_memory_shared, processes_ram_swap_data_unit, processes_ram_swap_data_precision)}')
        if selected_process_memory_uss != "-" and selected_process_memory_swap != "-":
            label2126w.set_text(f'{processes_details_data_unit_converter_func(selected_process_memory_uss, processes_ram_swap_data_unit, processes_ram_swap_data_precision)}')
            label2127w.set_text(f'{processes_details_data_unit_converter_func(selected_process_memory_swap, processes_ram_swap_data_unit, processes_ram_swap_data_precision)}')
        if selected_process_memory_uss == "-" and selected_process_memory_swap == "-":
            label2126w.set_text(selected_process_memory_uss)
            label2127w.set_text(selected_process_memory_swap)


    # Show and update process details on the "Disk and Path" tab
    if notebook2101w.get_current_page() == 2:
        # Get disk read data, disk write data, read count, write count of the process
        try:                                                                                  # Root access is needed for reading "/proc/[PID]/io" file else it gives error. "try-except" is used in order to avoid this error if user has no root privileges.
            with open("/proc/" + selected_process_pid + "/io") as reader:
                proc_pid_io_lines = reader.read().split("\n")
            selected_process_read_bytes = int(proc_pid_io_lines[4].split(":")[1])
            selected_process_write_bytes = int(proc_pid_io_lines[5].split(":")[1])
            selected_process_read_count = int(proc_pid_io_lines[2].split(":")[1])
            selected_process_write_count = int(proc_pid_io_lines[3].split(":")[1])
        except PermissionError:
            selected_process_read_bytes = 0
            selected_process_write_bytes = 0
            selected_process_read_count = 0
            selected_process_write_count = 0
        # Get disk read speed, disk write speed
        disk_read_write_data = [selected_process_read_bytes, selected_process_write_bytes]
        if disk_read_write_data_prev == []:
            selected_process_read_bytes_prev = selected_process_read_bytes                    # Make process_read_bytes_prev equal to process_read_bytes for giving "0" disk read speed value if this is first loop of the process
        else:
            selected_process_read_bytes_prev = disk_read_write_data_prev[0]
        selected_process_read_speed = (selected_process_read_bytes - int(selected_process_read_bytes_prev)) / update_interval    # Append process_read_bytes which will be used as "process_read_bytes_prev" value in the next loop and also append disk read speed. 
        if disk_read_write_data_prev == []:
            selected_process_write_bytes_prev = selected_process_write_bytes                  # Make process_write_bytes_prev equal to process_write_bytes for giving "0" disk write speed value if this is first loop of the process
        else:
            selected_process_write_bytes_prev = disk_read_write_data_prev[1]
        selected_process_write_speed = (selected_process_write_bytes - int(selected_process_write_bytes_prev)) / update_interval    # Append process_read_bytes which will be used as "process_read_bytes_prev" value in the next loop and also append disk read speed. 
        disk_read_write_data_prev = disk_read_write_data
        # Get process exe
        try:                                                                                  # Executable path of some of the processes may not be get without root privileges or may not be get due to the reason of some of the processes may not have a exe file. "try-except" is used to be able to avoid errors due to these reasons.
            selected_process_exe = os.path.realpath("/proc/" + selected_process_pid + "/exe")
        except Exception:
            selected_process_exe = "-"
        # Get process cwd
        try:
            selected_process_cwd = os.readlink("/proc/" + selected_process_pid + "/cwd")
        except (PermissionError, FileNotFoundError) as multiple_exception:                    # "PermissionError" is used for processes that require root privileges for "cwd data". "FileNotFoundError" is used for zombie processes which do not have a readable "cwd" file (it has the file but it is a broken link).
            selected_process_cwd = "-"
        # Get process cmdline
        with open("/proc/" + selected_process_pid + "/cmdline") as reader:
            selected_process_cmdline = reader.read().split("\x00")
        if selected_process_cmdline == [""]:
            selected_process_cmdline = "-"
        # Get open files of the process
        selected_process_open_files = []
        try:
            files_in_fd = [filename for filename in os.listdir("/proc/" + selected_process_pid + "/fd")]
            for file in files_in_fd:
                try:
                    path = os.readlink("/proc/" + selected_process_pid + "/fd/" + file)
                    if os.path.isfile(path) == True:
                        selected_process_open_files_path = path
                        selected_process_open_files_fd = file
                        with open("/proc/" + selected_process_pid + "/fdinfo/" + file) as reader:
                            proc_pid_fdinfo_lines = reader.read().split("\n")
                        for fdinfo in proc_pid_fdinfo_lines:
                            if "pos:" in fdinfo:
                                selected_process_open_files_position = fdinfo.split(":")[1].strip()            # File offset (for more information, see: https://man7.org/linux/man-pages/man5/proc.5.html)
                            if "flags:" in fdinfo:
                                selected_process_open_files_flags = int(fdinfo.split(":")[1].strip(), 8)       # Convert octal value into decimal integer. Flags is file access mode and file status mode  (for more information, see: https://man7.org/linux/man-pages/man5/proc.5.html).
                                try:
                                    selected_process_open_files_mode = fd_mode_dict[selected_process_open_files_flags]
                                except KeyError:
                                    selected_process_open_files_mode = selected_process_open_files_flags       # It gives error for Python process with "557057" file decriptor mode. No information is found for "557057" file descriptor mode integer value so far. Integer value is shown in this situation.
                        selected_process_open_files.append(f'Path: {selected_process_open_files_path}, File Descriptor: {selected_process_open_files_fd}, Position: {selected_process_open_files_position}, Mode: {selected_process_open_files_mode}, Flags: {selected_process_open_files_flags}')
                except FileNotFoundError:
                    continue
        except PermissionError:
            pass
        if selected_process_open_files == []:
            selected_process_open_files = "-"
        # Set label text by using process data
        if selected_process_read_bytes != "-" and selected_process_write_bytes != "-":
            label2128w.set_text(f'{processes_details_data_unit_converter_func(selected_process_read_speed, processes_disk_speed_data_unit, processes_disk_speed_data_precision)}')
            label2129w.set_text(f'{processes_details_data_unit_converter_func(selected_process_write_speed, processes_disk_speed_data_unit, processes_disk_speed_data_precision)}')
            label2130w.set_text(f'{processes_details_data_unit_converter_func(selected_process_read_bytes, processes_disk_speed_data_unit, processes_disk_speed_data_precision)}')
            label2131w.set_text(f'{processes_details_data_unit_converter_func(selected_process_write_bytes, processes_disk_speed_data_unit, processes_disk_speed_data_precision)}')
            label2132w.set_text(f'{selected_process_read_count}')
            label2133w.set_text(f'{selected_process_write_count}')
        if selected_process_read_bytes == "-" and selected_process_write_bytes == "-":
            label2128w.set_text("-")
            label2129w.set_text("-")
            label2130w.set_text("-")
            label2131w.set_text("-")
            label2132w.set_text("-")
            label2133w.set_text("-")
        label2134w.set_text(selected_process_exe)
        label2135w.set_text(selected_process_cwd)
        label2136w.set_text(',\n'.join(selected_process_cmdline))
        if selected_process_open_files != "-":
            label2137w.set_text(',\n'.join(selected_process_open_files))
        if selected_process_open_files == "-":
            label2137w.set_text("-")


# ----------------------------------- Processes - Processes Details Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def process_details_loop_func():

    if window2101w.get_visible() is True:
        GLib.idle_add(process_details_foreground_func)
        global update_interval
        update_interval = Config.update_interval
        GLib.timeout_add(update_interval * 1000, process_details_loop_func)


# ----------------------------------- Processes Details Foreground Thread Run Function (starts execution of the threads) -----------------------------------
def process_details_foreground_thread_run_func():

    processes_details_initial_thread = Thread(target=process_details_initial_func, daemon=True)
    processes_details_initial_thread.start()
    processes_details_initial_thread.join()
    processes_details_loop_thread = Thread(target=process_details_loop_func, daemon=True)
    processes_details_loop_thread.start()


# ----------------------------------- Processes - Processes Details Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def processes_details_define_data_unit_converter_variables_func():

    global data_unit_list

    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently.

    # Unit Name    Abbreviation    bytes   
    # byte         B               1
    # kilobyte     KB              1024
    # megabyte     MB              1.04858E+06
    # gigabyte     GB              1.07374E+09
    # terabyte     TB              1.09951E+12
    # petabyte     PB              1.12590E+15
    # exabyte      EB              1.15292E+18

    # Unit Name    Abbreviation    bytes    
    # bit          b               8
    # kilobit      Kb              8192
    # megabit      Mb              8,38861E+06
    # gigabit      Gb              8,58993E+09
    # terabit      Tb              8,79609E+12
    # petabit      Pb              9,00720E+15
    # exabit       Eb              9,22337E+18

    data_unit_list = [[0, 0, _tr("Auto-Byte")], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, _tr("Auto-bit")], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Processes - Processes Details Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def processes_details_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if unit >= 8:
        data = data * 8                                                                       # Source data is byte and a convertion is made by multiplicating with 8 if preferenced unit is bit.
    if unit == 0 or unit == 8:
        unit_counter = unit + 1
        while data > 1024:
            unit_counter = unit_counter + 1
            data = data/1024
        unit = data_unit_list[unit_counter][2]
        if data == 0:
            precision = 0
        return f'{data:.{precision}f} {unit}'

    data = data / data_unit_list[unit][1]
    unit = data_unit_list[unit][2]
    if data == 0:
        precision = 0
    return f'{data:.{precision}f} {unit}'


# ----------------------------------- Processes - Processes No Such Process Error Dialog Function (shows an error dialog and stops updating the "Process Details window" when the process is not alive anymore) -----------------------------------
def processes_no_such_process_error_dialog():

    error_dialog2101w = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Process Is Not Running Anymore"), )
    error_dialog2101w.format_secondary_text(_tr("Following process is not running anymore \nand process details window is closed automatically:\n  ") + selected_process_name + _tr(" (PID: ") + selected_process_pid + _tr(")"), )
    error_dialog2101w.run()
    error_dialog2101w.destroy()

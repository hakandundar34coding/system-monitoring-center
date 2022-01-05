#!/usr/bin/env python3

# ----------------------------------- Users - Users Details Import Function -----------------------------------
def users_details_import_func():

    global Gtk, GLib, GdkPixbuf, os, subprocess, datetime, time

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib, GdkPixbuf
    import os
    import subprocess
    from datetime import datetime
    import time


    global Config, Users, MainGUI
    import Config, Users, MainGUI


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Users - Users Details Window GUI Function -----------------------------------
def users_details_gui_function():

    # Users Details window GUI objects
    global builder3101w, window3101w
    global label3101w, label3102w, label3103w, label3104w, label3105w, label3106w, label3107w, label3108w, label3109w, label3110w
    global label3111w, label3112w, label3113w, label3114w


    # Users Details window GUI objects - get
    builder3101w = Gtk.Builder()
    builder3101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersDetailsWindow.ui")

    window3101w = builder3101w.get_object('window3101w')


    # Users Details window GUI objects
    label3101w = builder3101w.get_object('label3101w')
    label3102w = builder3101w.get_object('label3102w')
    label3103w = builder3101w.get_object('label3103w')
    label3104w = builder3101w.get_object('label3104w')
    label3105w = builder3101w.get_object('label3105w')
    label3106w = builder3101w.get_object('label3106w')
    label3107w = builder3101w.get_object('label3107w')
    label3108w = builder3101w.get_object('label3108w')
    label3109w = builder3101w.get_object('label3109w')
    label3110w = builder3101w.get_object('label3110w')
    label3111w = builder3101w.get_object('label3111w')
    label3112w = builder3101w.get_object('label3112w')
    label3113w = builder3101w.get_object('label3113w')
    label3114w = builder3101w.get_object('label3114w')


    # Users Details window GUI functions
    def on_window3101w_delete_event(widget, event):
        window3101w.hide()
        return True

    def on_window3101w_show(widget):
        try:
            global update_interval
            del update_interval                                                               # Delete "update_interval" variable in order to let the code to run initial function. Otherwise, data from previous process (if it was viewed) will be used.
        except NameError:
            pass
        users_details_gui_reset_function()                                                    # Call this function in order to reset Users Details window. Data from previous user remains visible (for a short time) until getting and showing new user data if window is closed and opened for an another user because window is made hidden when close button is clicked.


    # Users Details window GUI functions - connect
    window3101w.connect("delete-event", on_window3101w_delete_event)
    window3101w.connect("show", on_window3101w_show)


# ----------------------------------- Users - Users Details Window GUI Reset Function -----------------------------------
def users_details_gui_reset_function():
    window3101w.set_title(_tr("User Details"))                                                # Reset window title
    window3101w.set_icon_name("system-monitoring-center-user-symbolic")                       # Reset window icon
    label3101w.set_text("--")
    label3102w.set_text("--")
    label3103w.set_text("--")
    label3104w.set_text("--")
    label3105w.set_text("--")
    label3106w.set_text("--")
    label3107w.set_text("--")
    label3108w.set_text("--")
    label3109w.set_text("--")
    label3110w.set_text("--")
    label3111w.set_text("--")
    label3112w.set_text("--")
    label3113w.set_text("--")
    label3114w.set_text("--")


# # ----------------------------------- Users - Users Details Tab Switch Control Function (controls if tab is switched and updates data on the last opened tab immediately without waiting end of the update interval. Signals of notebook for tab switching is not useful because it performs the action and after that it switches the tab. Data updating function does not recognizes tab switch due to this reason.) -----------------------------------
# def users_details_tab_switch_control_func():
# 
#     global previous_page
#     if 'previous_page' not in globals():                                                      # For avoiding errors in the first loop of the control
#         previous_page = None
#         current_page = None
#     current_page = notebook3101w.get_current_page()
#     if current_page != previous_page and previous_page != None:                               # Check if tab is switched
#         UsersDetails.user_details_foreground_func()                                           # Update the data on the tab
#     previous_page = current_page
#     if window3101w.get_visible() == True:
#         GLib.timeout_add(200, users_details_tab_switch_control_func)                          # Check is performed in every 200 ms which is small enough for immediate update and not very frequent for avoiding high CPU usages.


# ----------------------------------- Users - Users Details Function -----------------------------------
def users_details_initial_func():

    users_define_data_unit_converter_variables_func()                                         # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    global pid_list_prev, global_process_cpu_times_prev
    pid_list_prev = []
    global_process_cpu_times_prev = []

    global number_of_clock_ticks, memory_page_size, system_boot_time, user_image_unset_pixbuf

    number_of_clock_ticks = os.sysconf("SC_CLK_TCK")                                          # For many systems CPU ticks 100 times in a second. Wall clock time could be get if CPU times are multiplied with this value or vice versa.
    memory_page_size = os.sysconf("SC_PAGE_SIZE")                                             # This value is used for converting memory page values into byte values. This value depends on architecture (also sometimes depends on machine model). Default value is 4096 Bytes (4 KiB) for most processors.

    # Get system boot time which will be used for obtaining user process start time
    with open("/proc/stat") as reader:
        stat_lines = reader.read().split("\n")
    for line in stat_lines:
        if "btime " in line:
            system_boot_time = int(line.split()[1].strip())

    user_image_unset_pixbuf = Gtk.IconTheme.get_default().load_icon("system-monitoring-center-user-symbolic", 24, 0)

    date_month_names_list = [_tr("Jan"), _tr("Feb"), _tr("Mar"), _tr("Apr"), _tr("May"), _tr("Jun"), _tr("Jul"), _tr("Aug"), _tr("Sep"), _tr("Oct"), _tr("Nov"), _tr("Dec")]    # This list is defined in order to make English month names (get from /var/log/auth.log file) to be translated into other languages.
    date_day_names_list = [_tr("Mon"), _tr("Tue"), _tr("Wed"), _tr("Thu"), _tr("Fri"), _tr("Sat"), _tr("Sun")]    # This list is defined in order to make English day names (get from "lslogins") to be translated into other languages.


# ----------------------------------- Users - Users Details Foreground Function -----------------------------------
def users_details_loop_func():

    global selected_user_uid, selected_username
    selected_user_uid = str(Users.selected_user_uid)                                          # Get right clicked user UID
    selected_username = Users.selected_username

    # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
    global users_cpu_usage_percent_precision
    global users_ram_swap_data_precision, users_ram_swap_data_unit
    users_cpu_usage_percent_precision = Config.users_cpu_usage_percent_precision
    users_ram_swap_data_precision = Config.users_ram_swap_data_precision
    users_ram_swap_data_unit = Config.users_ram_swap_data_unit

    # Define global variables and empty lists for the current loop
    global global_process_cpu_times_prev, pid_list, pid_list_prev
    global_process_cpu_times = []

    # Get number of online logical CPU cores (this operation is repeated in every loop because number of online CPU cores may be changed by user and this may cause wrong calculation of CPU usage percent data of the processes even if this is a very rare situation.)
    global number_of_logical_cores
    try:
        number_of_logical_cores = os.sysconf("SC_NPROCESSORS_ONLN")                           # To be able to get number of online logical CPU cores first try  a faster way: using "SC_NPROCESSORS_ONLN" variable.
    except:
        with open("/proc/cpuinfo") as reader:                                                 # As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
            proc_cpuinfo_lines = reader.read().split("\n")
        number_of_logical_cores = 0
        for line in proc_cpuinfo_lines:
            if line.startswith("processor"):
                number_of_logical_cores = number_of_logical_cores + 1

    # Get all users
    with open("/etc/passwd") as reader:
        etc_passwd_output = reader.read().strip()                                             # "strip()" is used for removing empty (last) line in the text
    etc_passwd_lines = etc_passwd_output.split("\n")
    if ":" + selected_user_uid + ":" not in etc_passwd_output:
        window3101w.hide()
        return
    # Get all user groups
    with open("/etc/group") as reader:
        etc_group_lines = reader.read().strip().split("\n")
    user_group_names = []
    user_group_ids = []
    for line in etc_group_lines:
        line_split = line.split(":")
        user_group_names.append(line_split[0])
        user_group_ids.append(line_split[2])
    # Get all process PIDs to be able to search "systemd" process (user account process) and check username of it if it is correct "systemd" file. User logged in information and start time (first log in time since system boot) will be get by using this process.
    pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]
    # Get process names (will be used for checking "systemd" named processes to be able to get user process, user first log in time since system boot), usernames (will be used for determining number of processes of the users), CPU% and memory usage of all processes
    all_process_names = []
    all_process_user_ids = []
    all_process_cpu_usages = []
    all_process_memory_usages = []
    for pid in pid_list[:]:                                                                   # "[:]" is used for iterating over copy of the list because element are removed during iteration. Otherwise incorrect operations (incorrect element removal) are performed on the list.
        try:
            with open("/proc/" + pid + "/status") as reader:
                proc_pid_status_lines = reader.read().split("\n")
            with open("/proc/" + pid + "/stat") as reader:
                global_cpu_time_all = time.time() * number_of_clock_ticks                     # global_cpu_time_all value is get just before "/proc/[PID]/stat file is read in order to measure global an process specific CPU times at the same time (nearly) for ensuring accurate process CPU usage percent.
                proc_pid_stat_lines = reader.read().split()
        except FileNotFoundError:                                                             # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
            pid_list.remove(pid)
            continue
        for line in proc_pid_status_lines:
            # Get names of all processes
            if "Name:\t" in line:
                all_process_names.append(line.split(":")[1].strip())
            # Get user UIDs of all processes
            if "Uid:\t" in line:
                all_process_user_ids.append(line.split(":")[1].split()[0].strip())            # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
        # Get CPU usage percent of all processes
        process_cpu_time = int(proc_pid_stat_lines[-39]) + int(proc_pid_stat_lines[-38])      # Get process cpu time in user mode (utime + stime)
        global_process_cpu_times.append((global_cpu_time_all, process_cpu_time))              # While appending multiple elements into a list "append((value1, value2))" is faster than "append([value1, value2])".
        try:                                                                                  # It gives various errors (ValueError, IndexError, UnboundLocalError) if a new process is started, a new column is shown on the treeview, etc because previous CPU time values are not present in these situations. Following CPU time values are use in these situations.
            global_cpu_time_all_prev, process_cpu_time_prev = global_process_cpu_times_prev[pid_list_prev.index(pid)]
        except (ValueError, IndexError, UnboundLocalError) as me:
            process_cpu_time_prev = process_cpu_time                                          # There is no "process_cpu_time_prev" value and get it from "process_cpu_time"  if this is first loop of the process
            global_cpu_time_all_prev = global_process_cpu_times[-1][0] - 1                    # Subtract "1" CPU time (a negligible value) if this is first loop of the process
        process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
        global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
        all_process_cpu_usages.append(process_cpu_time_difference / global_cpu_time_difference * 100 / number_of_logical_cores)
        # Get RAM memory (RSS) usage percent of all processes
        all_process_memory_usages.append(int(proc_pid_stat_lines[-29]) * memory_page_size)    # Get process RSS (resident set size) memory pages and multiply with memory_page_size in order to convert the value into bytes.
    # Get all users last log in and last failed log in times
    lslogins_command_lines = (subprocess.check_output(["lslogins", "--notruncate", "-e", "--newline", "--time-format=full", "-u", "-o", "=USER,LAST-LOGIN,FAILED-LOGIN"], shell=False)).decode().strip().split("\n")

    for line in etc_passwd_lines:
        line_split = line.split(":")
        if line_split[2] == selected_user_uid:
            selected_user_username = line_split[0]
            selected_user_gid = line_split[3]
            selected_user_full_name = line_split[4]                                           # Get user full name
            selected_user_home_dir = line_split[5]
            selected_user_terminal = line_split[6]
            break

    # Get user PID and logged in data (PID data is required for obtaining user logged in data. User PID and user logged in data will be appended later)
    user_process_pid = 0                                                                      # Initial value of "user_PID" value. This value will be left as "0" if user is not logged in.
    for i, process_name in enumerate(all_process_names):
        if process_name == "systemd":                                                         # "systemd" process per user is checked here (by checking real UID of the process). It is not system-wide "systemd" process which is owned by "root" user. User session process is specific to desktop session (for example xfce4-session for XFCE desktop environment) and checking "systemd" process of the user is easier and gives very similar start time.
            real_user_id = all_process_user_ids[i]
            if real_user_id == selected_user_uid:
                user_process_pid = pid_list[i]
                break                                                                         # Exit this loop if real_user_id" is found in order to obtain faster code execution.
    if user_process_pid != 0:                                                                 # User is not logged in if "user_process_pid" is not get from "systemd" process of the user.
        selected_user_logged_in = _tr("Yes")
    if user_process_pid == 0:                                                                 # User is logged in if "user_process_pid" is get from "systemd" process of the user.
        selected_user_logged_in = _tr("No")

    # Get user account image
    user_image_path = "/var/lib/AccountsService/icons/" + selected_user_username
    if os.path.isfile(user_image_path) == True:
        selected_user_account_image = GdkPixbuf.Pixbuf.new_from_file_at_size(user_image_path, 24, 24)
    if os.path.isfile(user_image_path) == False:
        selected_user_account_image = user_image_unset_pixbuf

    # Get user process count
    selected_user_process_count = all_process_user_ids.count(selected_user_uid)

    # Get user group
    selected_user_group_name = user_group_names[user_group_ids.index(selected_user_gid)]

    # Get user last log in time
    for i, line in enumerate(lslogins_command_lines):                                         # Search for username of current loop (user data row). Finally, data is split by using "empty space" and joined again for translating English month and day names into other languages. Strings which will be translated are defined in lists (date_month_names_list, date_day_names_list) and are exported by "gettext".
        if line.split("=")[1].strip('"') == selected_user_username:
            selected_user_last_log_in_time_split = lslogins_command_lines[i+1].split("=")[1].strip('"').split()    # For using translated strings (day and month names)
            for i, string in enumerate(selected_user_last_log_in_time_split):
                selected_user_last_log_in_time_split[i] = _tr(string)
            selected_user_last_log_in_time = " ".join(selected_user_last_log_in_time_split)
            break
    if selected_user_last_log_in_time == "":
        selected_user_last_log_in_time = "-"

    # Get user last failed log in time
    for i, line in enumerate(lslogins_command_lines):
        if line.split("=")[1].strip('"') == selected_user_username:                           # Search for username of current loop (user data row). Finally, data is split by using "empty space" and joined again for translating English month and day names into other languages. Strings which will be translated are defined in lists (date_month_names_list, date_day_names_list) and are exported by "gettext".
            selected_user_last_failed_log_in_time_split = lslogins_command_lines[i+2].split("=")[1].strip('"').split()    # For using translated strings (day and month names)
            for i, string in enumerate(selected_user_last_failed_log_in_time_split):
                selected_user_last_failed_log_in_time_split[i] = _tr(string)
            selected_user_last_failed_log_in_time = " ".join(selected_user_last_failed_log_in_time_split)
            break
    if selected_user_last_failed_log_in_time == "":
        selected_user_last_failed_log_in_time = "-"

    # Get user process start time
    if user_process_pid == 0:
        selected_user_process_start_time = 0                                                  # User process start time is "0" if it is not alive (if user is not logged in)
    if user_process_pid != 0:                                                                 # User process start time is get if it is alive (if user is logged in)
        try:
            with open("/proc/" + str(user_process_pid) + "/stat") as reader:
                proc_pid_stat_lines = int(reader.read().split()[-31])                         # Elapsed time between system boot and process start time (measured in clock ticks and need to be divided by sysconf(_SC_CLK_TCK) for converting into wall clock time)
            selected_user_process_start_time = (proc_pid_stat_lines / number_of_clock_ticks) + system_boot_time
        except:
            selected_user_process_start_time = 0

    # Get user processes CPU usage percent and RAM memory (RSS) usage percent
    selected_user_cpu_percent = 0
    for pid in pid_list:
        if all_process_user_ids[pid_list.index(pid)] == selected_user_uid:
            selected_user_cpu_percent = selected_user_cpu_percent + all_process_cpu_usages[pid_list.index(pid)]
    selected_user_ram_percent = 0
    for pid in pid_list:
        if all_process_user_ids[pid_list.index(pid)] == selected_user_uid:
            selected_user_ram_percent = selected_user_ram_percent + all_process_memory_usages[pid_list.index(pid)]

    pid_list_prev = pid_list                                                                  # For using values in the next loop
    global_process_cpu_times_prev = global_process_cpu_times                                  # For using values in the next loop


    # Set Users Details window title and window icon image
    window3101w.set_title(_tr("User Details") + ": " + selected_user_username)                     # Set window title
    window3101w.set_icon(selected_user_account_image)                                         # Set UsersDetails window icon

    # Set label text by using storage/disk data
    label3101w.set_text(selected_user_username)
    label3102w.set_text(selected_user_full_name)
    label3103w.set_text(selected_user_logged_in)
    label3104w.set_text(selected_user_uid)
    label3105w.set_text(selected_user_gid)
    label3106w.set_text(f'{selected_user_process_count}')
    label3107w.set_text(selected_user_home_dir)
    label3108w.set_text(selected_user_group_name)
    label3109w.set_text(selected_user_terminal)
    label3110w.set_text(selected_user_last_log_in_time)
    label3111w.set_text(selected_user_last_failed_log_in_time)
    if selected_user_process_start_time != 0:
        label3112w.set_text(datetime.fromtimestamp(selected_user_process_start_time).strftime("%H:%M:%S %d.%m.%Y"))
    if selected_user_process_start_time == 0:
        label3112w.set_text("-")
    label3113w.set_text(f'{selected_user_cpu_percent:.{users_cpu_usage_percent_precision}f} %')
    label3114w.set_text(f'{users_data_unit_converter_func(selected_user_ram_percent, users_ram_swap_data_unit, users_ram_swap_data_precision)}')


# ----------------------------------- Users Details Run Function -----------------------------------
def users_details_run_func():

    if "update_interval" not in globals():
        GLib.idle_add(users_details_initial_func)
    if window3101w.get_visible() is True:
        GLib.idle_add(users_details_loop_func)
        global update_interval
        update_interval = Config.update_interval
        GLib.timeout_add(update_interval * 1000, users_details_run_func)


# ----------------------------------- Users - Define Data Unit Converter Variables Function -----------------------------------
def users_define_data_unit_converter_variables_func():

    global data_unit_list
    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently. [[index, calculated byte value, unit abbreviation], ...]
    data_unit_list = [[0, 0, "Auto-Byte"], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, "Auto-bit"], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Users - Data Details Unit Converter Function -----------------------------------
def users_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if unit >= 8:
        data = data * 8
    if unit in [0, 8]:
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

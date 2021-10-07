#! /usr/bin/python3

# ----------------------------------- Users - Users Details Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def users_details_import_func():

    global Gtk, GLib, GdkPixbuf, os, Thread, subprocess, datetime, time

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib, GdkPixbuf
    import os
    from threading import Thread
    import subprocess
    from datetime import datetime
    import time


    global Config, Users, UsersGUI, UsersDetailsGUI, MainGUI
    import Config, Users, UsersGUI, UsersDetailsGUI, MainGUI


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


# ----------------------------------- Users - Users Details Function (the code of this module in order to avoid running them during module import and defines "Users" tab GUI objects and functions/signals) -----------------------------------
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


# ----------------------------------- Users - Users Details Foreground Function (updates the process data on the "Users Details" window) -----------------------------------
def users_details_foreground_func():

    global selected_user_uid
    selected_user_uid = str(UsersGUI.selected_user_uid)                                       # Get right clicked disk name

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
        etc_passwd_lines = reader.read().strip().split("\n")                                  # "strip()" is used for removing empty (last) line in the text
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
    lslogins_command_lines = subprocess.check_output("lslogins --notruncate -e --newline --time-format=full -u -o =USER,LAST-LOGIN,FAILED-LOGIN", shell=True).decode().strip().split("\n")

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
    UsersDetailsGUI.window3101w.set_title(_tr("User Details: ") + selected_user_username)     # Set window title
    UsersDetailsGUI.window3101w.set_icon(selected_user_account_image)                         # Set UsersDetails window icon

    # Set label text by using storage/disk data
    UsersDetailsGUI.label3101w.set_text(selected_user_username)
    UsersDetailsGUI.label3102w.set_text(selected_user_full_name)
    UsersDetailsGUI.label3103w.set_text(selected_user_logged_in)
    UsersDetailsGUI.label3104w.set_text(selected_user_uid)
    UsersDetailsGUI.label3105w.set_text(selected_user_gid)
    UsersDetailsGUI.label3106w.set_text(f'{selected_user_process_count}')
    UsersDetailsGUI.label3107w.set_text(selected_user_home_dir)
    UsersDetailsGUI.label3108w.set_text(selected_user_group_name)
    UsersDetailsGUI.label3109w.set_text(selected_user_terminal)
    UsersDetailsGUI.label3110w.set_text(selected_user_last_log_in_time)
    UsersDetailsGUI.label3111w.set_text(selected_user_last_failed_log_in_time)
    if selected_user_process_start_time != 0:
        UsersDetailsGUI.label3112w.set_text(datetime.fromtimestamp(selected_user_process_start_time).strftime("%H:%M:%S %d.%m.%Y"))
    if selected_user_process_start_time == 0:
        UsersDetailsGUI.label3112w.set_text("-")
    UsersDetailsGUI.label3113w.set_text(f'{selected_user_cpu_percent:.{users_cpu_usage_percent_precision}f} %')
    UsersDetailsGUI.label3114w.set_text(f'{users_data_unit_converter_func(selected_user_ram_percent, users_ram_swap_data_unit, users_ram_swap_data_precision)}')



# ----------------------------------- Users - Users Details Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def users_details_loop_func():

    if UsersDetailsGUI.window3101w.get_visible() is True:
        GLib.idle_add(users_details_foreground_func)
        GLib.timeout_add(Config.update_interval * 1000, users_details_loop_func)


# ----------------------------------- Users Details Foreground Thread Run Function (starts execution of the threads) -----------------------------------
def users_details_foreground_thread_run_func():

    users_details_initial_thread = Thread(target=users_details_initial_func, daemon=True)
    users_details_initial_thread.start()
    users_details_initial_thread.join()
    users_details_loop_thread = Thread(target=users_details_loop_func, daemon=True)
    users_details_loop_thread.start()


# ----------------------------------- Users - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def users_define_data_unit_converter_variables_func():

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


# ----------------------------------- Users - Data Details Unit Converter Function (converts byte and bit data units) -----------------------------------
def users_data_unit_converter_func(data, unit, precision):

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


# ----------------------------------- Users - Users Details No Such Users Error Dialog Function (shows an error dialog and stops updating the "Users Details window" when the storage/disk is not connected anymore) -----------------------------------
def users_no_such_user_error_dialog():

    error_dialog3101w = Gtk.MessageDialog(transient_for=MainGUI.window1, title="Error", flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text="Disk Is Not Connected Anymore", )
    error_dialog3101w.format_secondary_text(_tr("Following disk is not connected anymore \nand storage details window is closed automatically:\n  ") + disk)
    error_dialog3101w.run()
    error_dialog3101w.destroy()

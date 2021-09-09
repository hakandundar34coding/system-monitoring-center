#!/usr/bin/env python3

# ----------------------------------- Processes - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def processes_import_func():

    global Gtk, Gdk, GLib, GObject, Wnck, Thread, os, time

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib, GObject
    gi.require_version('Wnck', '3.0')
    from gi.repository import Wnck
    from threading import Thread
    import os
    import time


    global Config, MainGUI, ProcessesGUI, ProcessesMenusGUI
    import Config, MainGUI, ProcessesGUI, ProcessesMenusGUI


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


# ----------------------------------- Processes - Initial Function (contains initial code which defines some variables and gets data which is not wanted to be run in every loop) -----------------------------------
def processes_initial_func():

    # data list explanation:
    # processes_data_list = [
    #                       [treeview column number, treeview column title, internal column count, cell renderer count, treeview column sort column id, [data type 1, data type 2, ...], [cell renderer type 1, cell renderer type 2, ...], [cell attribute 1, cell attribute 2, ...], [cell renderer data 1, cell renderer data 2, ...], [cell left/right alignment 1, cell left/right alignment 2, ...], [set expand 1 {if cell will allocate unused space} cell expand 2, ...], [cell function 1, cell function 2, ...]]
    #                       .
    #                       .
    #                       ]
    global processes_data_list
    processes_data_list = [
                          [0, _tr('Process Name'), 3, 2, 3, [bool, str, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'icon_name', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
                          [1, _tr('PID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [2, _tr('User Name'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                          [3, _tr('Status'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                          [4, _tr('CPU %'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_cpu_usage_percent]],
                          [5, _tr('RAM (RSS)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_ram_swap]],
                          [6, _tr('RAM (VMS)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_ram_swap]],
                          [7, _tr('RAM (Shared)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_ram_swap]],
                          [8, _tr('Disk Read Data'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_usage]],
                          [9, _tr('Disk Write Data'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_usage]],
                          [10, _tr('Disk Read Speed'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_speed]],
                          [11, _tr('Disk Write Speed'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_speed]],
                          [12, _tr('Priority'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [13, _tr('# of Threads'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [14, _tr('PPID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [15, _tr('UID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [16, _tr('GID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [17, _tr('Path'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']]
                          ]

    processes_define_data_unit_converter_variables_func()                                     # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    global processes_data_rows_prev, pid_list_prev, piter_list, global_process_cpu_times_prev, disk_read_write_data_prev, show_processes_as_tree_prev, processes_treeview_columns_shown_prev, processes_data_row_sorting_column_prev, processes_data_row_sorting_order_prev, processes_data_column_order_prev, processes_data_column_widths_prev
    processes_data_rows_prev = []
    pid_list_prev = []
    piter_list = []
    global_process_cpu_times_prev = []
    disk_read_write_data_prev = []
    show_processes_as_tree_prev = Config.show_processes_as_tree
    processes_treeview_columns_shown_prev = []
    processes_data_row_sorting_column_prev = ""
    processes_data_row_sorting_order_prev = ""
    processes_data_column_order_prev = []
    processes_data_column_widths_prev = []

    global process_status_list, number_of_clock_ticks, memory_page_size
    process_status_list = {"R": _tr("Running"), "S": _tr("Sleeping"), "D": _tr("Waiting"), "I": _tr("Idle"), "Z": _tr("Zombie"), "T": _tr("Stopped"), "t": _tr("Tracing Stop"), "X": _tr("Dead")}    # This list is used in order to show full status of the process. For more information, see: "https://man7.org/linux/man-pages/man5/proc.5.html".
    number_of_clock_ticks = os.sysconf("SC_CLK_TCK")                                          # For many systems CPU ticks 100 times in a second. Wall clock time could be get if CPU times are multiplied with this value or vice versa.
    memory_page_size = os.sysconf("SC_PAGE_SIZE")                                             # This value is used for converting memory page values into byte values. This value depends on architecture (also sometimes depends on machine model). Default value is 4096 Bytes (4 KiB) for most processors.

    global application_exec_list, application_icon_list                                       # Process names will be checked if they are in these lists. If process names cold not be found in these lists, "application" icon will be shown.
    application_exec_list = []
    application_icon_list = []
    application_file_list = [file for file in os.listdir("/usr/share/applications/") if file.endswith(".desktop")]    # Get  ".desktop" file name
    for application in application_file_list:
        try:
            with open("/usr/share/applications/" + application) as reader:
                application_file_content = reader.read()
            appliation_exec = application_file_content.split("Exec=")[1].split("\n")[0].split("/")[-1].split(" ")[0]    # Get application exec data
            if appliation_exec != "sh":                                                       # Splitting operation above may give "sh" as application name and this may cause confusion between "sh" process and splitted application exec (for example: sh -c "gdebi-gtk %f"sh -c "gdebi-gtk %f"). This statement is used to avoid from this confusion.
                application_exec_list.append(appliation_exec)
            else:
                application_exec_list.append(application_file_content.split("Exec=")[1].split("\n")[0])
            application_icon_list.append(application_file_content.split("Icon=")[1].split("\n")[0])    # Get application icon name data
        except:
            application_icon_list.append("_no_icon_")                                         # Append "_no_icon_" into the list if no icon name data is found in the ".desktop" file in order to keep list length same as "application_exec_list" list. Because index matching of these list is used in order to get application icon names by using application exec data.


# ----------------------------------- Processes - Get Process Data Function (gets processes data, adds into treeview and updates it) -----------------------------------
def processes_loop_func():

    # Get configrations one time per floop instead of getting them multiple times (hundreds of times for many of them) in every loop which causes high CPU usage.
    global processes_cpu_usage_percent_precision
    global processes_ram_swap_data_precision, processes_ram_swap_data_unit
    global processes_disk_usage_data_precision, processes_disk_usage_data_unit, processes_disk_speed_data_precision, processes_disk_speed_data_unit
    processes_cpu_usage_percent_precision = Config.processes_cpu_usage_percent_precision
    processes_ram_swap_data_precision = Config.processes_ram_swap_data_precision
    processes_ram_swap_data_unit = Config.processes_ram_swap_data_unit
    processes_disk_usage_data_precision = Config.processes_disk_usage_data_precision
    processes_disk_usage_data_unit = Config.processes_disk_usage_data_unit
    processes_disk_speed_data_precision = Config.processes_disk_speed_data_precision
    processes_disk_speed_data_unit = Config.processes_disk_speed_data_unit

    # Define global variables and get treeview columns, sort column/order, column widths, etc.
    global processes_treeview_columns_shown, show_processes_of_all_users
    global processes_treeview_columns_shown_prev, processes_data_row_sorting_column_prev, processes_data_row_sorting_order_prev, processes_data_column_order_prev, processes_data_column_widths_prev
    processes_treeview_columns_shown = Config.processes_treeview_columns_shown
    processes_data_row_sorting_column = Config.processes_data_row_sorting_column
    processes_data_row_sorting_order = Config.processes_data_row_sorting_order
    processes_data_column_order = Config.processes_data_column_order
    processes_data_column_widths = Config.processes_data_column_widths
    show_processes_of_all_users = Config.show_processes_of_all_users

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

    # Get human and root user usernames and UIDs only one time at the per loop in order to avoid running it per process loop (it is different than main loop = processes_loop_func) which increases CPU consumption.
    usernames_username_list = []
    usernames_uid_list = []
    with open("/etc/passwd") as reader:                                                       # "/etc/passwd" file (also knonw as Linux password database) contains all local user (system + human users) information.
        etc_passwd_lines = reader.read().strip().split("\n")                                  # "strip()" is used in order to prevent errors due to an empty line at the end of the list.
    for line in etc_passwd_lines:
        line_splitted = line.split(":")
        usernames_username_list.append(line_splitted[0])
        usernames_uid_list.append(line_splitted[2])

    # Get current username which will be used for determining processes from only this user or other users.
    global current_user_name
    current_user_name = os.environ.get('SUDO_USER')                                           # Get user name that gets root privileges. Othervise, username is get as "root" when root access is get.
    if current_user_name is None:                                                             # Get username in the following way if current application has not been run by root privileges.
        current_user_name = os.environ.get('USER')
    pkexec_uid = os.environ.get('PKEXEC_UID')
    if current_user_name == "root" and pkexec_uid != None:                                    # current_user_name is get as "None" if application is run with "pkexec" command. In this case, "os.environ.get('PKEXEC_UID')" is used to be able to get username of which user has run the application with "pkexec" command.
        current_user_name = usernames_username_list[usernames_uid_list.index(os.environ.get('PKEXEC_UID'))]

    # Get process PIDs and define global variables and empty lists for the current loop
    global processes_data_rows, processes_data_rows_prev, global_process_cpu_times_prev, disk_read_write_data_prev, pid_list, pid_list_prev, username_list
    processes_data_rows = []
    ppid_list = []
    username_list = []
    global_process_cpu_times = []
    disk_read_write_data = []
    pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]          # Get process PID list. PID values are appended as string values because they are used as string values in various places in the code and this ensures lower CPU usage by avoiding hundreds/thousands of times integer to string conversion.

    # Get user names of the processes (this data is get outside and before the "getting process data" loop in which process pseudo files are read because this data also will be used for "show_processes_of_all_users" preference)
    for pid in pid_list[:]:                                                                   # "[:]" is used for iterating over copy of the list because elements are removed during iteration. Otherwise incorrect operations (incorrect element removals) are performed on the list.
        try:                                                                                  # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
            with open("/proc/" + pid + "/status") as reader:                                  # User name of the process owner is get from "/proc/status" file because it is present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                proc_pid_status_lines = reader.read().split("\n")
        except FileNotFoundError:                                                             # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
            pid_list.remove(pid)
            continue
        for line in proc_pid_status_lines:
            if "Uid:\t" in line:
                real_user_id = line.split(":")[1].split()[0].strip()                          # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                username = usernames_username_list[usernames_uid_list.index(real_user_id)]
        username_list.append(username)
        # Remove PIDs of processes from other than current user (show processes only from this user) if it is preferred by user
        if show_processes_of_all_users == 0:
            if username != current_user_name:
                pid_list.remove(pid)
                del username_list[-1]                                                         # Remove last username which has been appended in this loop. It is removed because its process PID has been removed (because it is not owned by current user).
                continue

    # Get process data
    for pid in pid_list[:]:                                                                   # "[:]" is used for iterating over copy of the list because element are removed during iteration. Otherwise incorrect operations (incorrect element removal) are performed on the list.
        global_cpu_time_all = time.time() * number_of_clock_ticks                             # global_cpu_time_all value is get just before "/proc/[PID]/stat file is read in order to measure global an process specific CPU times at the same time (nearly) for ensuring accurate process CPU usage percent. global_cpu_time_all value is get by using time module of Python instead of reading "/proc/stat" file for faster processing.
        try:                                                                                  # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
            with open("/proc/" + pid + "/stat") as reader:                                    # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
                proc_pid_stat_lines = reader.read()
        except FileNotFoundError:                                                             # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
            pid_list.remove(pid)
            continue
        proc_pid_stat_lines_split = proc_pid_stat_lines.split()
        processes_data_row = []
        processes_data_row.append(True)                                                       # Process visibility data (on treeview) which is used for showing/hiding process when processes of specific user is preferred to be shown or process search feature is used from the GUI.
        ppid_list.append(proc_pid_stat_lines_split[-49])                                      # Process data is get by negative indexes because file content is split by " " (empty space) character and also process name could contain empty space character which may result confusion getting correct process data. In other words empty space character count may not be same for all process "stat" files and process name it at the second place in the file. Reading process data of which turn is later than process name by using negative index is a reliable method.
        first_parentheses = proc_pid_stat_lines.find("(")                                     # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
        second_parentheses = proc_pid_stat_lines.rfind(")")                                   # Last parantheses ")" index is get by using "find()".
        process_name_from_stat = proc_pid_stat_lines[first_parentheses+1:second_parentheses]  # Process name is get from string by using the indexes get previously.
        process_name = process_name_from_stat
        if len(process_name) >= 15:                                                           # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name. "=15" is enough but this limit may be increased in the next releases of the kernel. ">=15" is used in order to handle this possible change.
            try:
                with open("/proc/" + pid + "/cmdline") as reader:
                    process_name = ''.join(reader.read().split("/")[-1].split("\x00"))        # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()" and joined again without these characters.
            except FileNotFoundError:                                                         # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
                pid_list.remove(pid)
                continue
            if process_name.startswith(process_name_from_stat) == False:
                process_name = process_name_from_stat                                         # Root access is needed for reading "cmdline" file of the some processes. Otherwise it gives "" as output. Process name from "stat" file of the process is used is this situation. Also process name from "stat" file is used if name from "cmdline" does not start with name from "stat" file.
        if process_name in application_icon_list:                                             # Use process name as process icon name if process name is found in application icons list
            process_icon = process_name
        elif process_name in application_exec_list:                                           # Use process icon name from application file if process name is found in application exec list
            process_icon = application_icon_list[application_exec_list.index(process_name)]
        else:
            process_icon = "system-monitoring-center-process-symbolic"                        # This icon will be shown for processes of which icon could not be found in default icon theme.
        processes_data_row.extend((process_icon, process_name))
        if 1 in processes_treeview_columns_shown:
            processes_data_row.append(int(proc_pid_stat_lines_split[0]))                      # Get process PID. Value is appended as integer for ensuring correct "PID" column sorting such as 1,2,10,101... Otherwise it would sort such as 1,10,101,2...
        if 2 in processes_treeview_columns_shown:
            processes_data_row.append(username_list[pid_list.index(pid)])                     # Append process username
        if 3 in processes_treeview_columns_shown:
            processes_data_row.append(process_status_list[proc_pid_stat_lines_split[-50]])    # Get process status
        if 4 in processes_treeview_columns_shown:
            process_cpu_time = int(proc_pid_stat_lines_split[-39]) + int(proc_pid_stat_lines_split[-38])   # Get process cpu time in user mode (utime + stime)
            global_process_cpu_times.append((global_cpu_time_all, process_cpu_time))          # While appending multiple elements into a list "append((value1, value2))" is faster than "append([value1, value2])".
            try:                                                                              # It gives various errors (ValueError, IndexError, UnboundLocalError) if a new process is started, a new column is shown on the treeview, etc because previous CPU time values are not present in these situations. Following CPU time values are use in these situations.
                global_cpu_time_all_prev, process_cpu_time_prev = global_process_cpu_times_prev[pid_list_prev.index(pid)]
            except (ValueError, IndexError, UnboundLocalError) as me:
                process_cpu_time_prev = process_cpu_time                                      # There is no "process_cpu_time_prev" value and get it from "process_cpu_time"  if this is first loop of the process
                global_cpu_time_all_prev = global_process_cpu_times[-1][0] - 1                # Subtract "1" CPU time (a negligible value) if this is first loop of the process
            process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
            global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
            processes_data_row.append(process_cpu_time_difference / global_cpu_time_difference * 100 / number_of_logical_cores)
        if 5 in processes_treeview_columns_shown:
            processes_data_row.append(int(proc_pid_stat_lines_split[-29]) * memory_page_size) # Get process RSS (resident set size) memory pages and multiply with memory_page_size in order to convert the value into bytes.
        if 6 in processes_treeview_columns_shown:
            processes_data_row.append(int(proc_pid_stat_lines_split[-30]))                    # Get process VMS (virtual memory size) memory (this value is in bytes unit).
        if 7 in processes_treeview_columns_shown:
            try:
                with open("/proc/" + pid + "/statm") as reader:                                   
                    processes_data_row.append(int(reader.read().split()[2]) * memory_page_size)   # Get shared memory pages and multiply with memory_page_size in order to convert the value into bytes.
            except FileNotFoundError:                                                         # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
                pid_list.remove(pid)
                continue
        if 8 in processes_treeview_columns_shown or 9 in processes_treeview_columns_shown or 10 in processes_treeview_columns_shown or 11 in processes_treeview_columns_shown:
            try:                                                                              # Root access is needed for reading "/proc/[PID]/io" file else it gives error. "try-except" is used in order to avoid this error if user has no root privileges.
                with open("/proc/" + pid + "/io") as reader:
                    proc_pid_io_lines = reader.read().split("\n")
                process_read_bytes = int(proc_pid_io_lines[4].split(":")[1])
                process_write_bytes = int(proc_pid_io_lines[5].split(":")[1])
            except PermissionError:
                process_read_bytes = 0
                process_write_bytes = 0
            disk_read_write_data.append((process_read_bytes, process_write_bytes))
            if pid not in pid_list_prev and disk_read_write_data_prev != []:
                disk_read_write_data_prev.append((process_read_bytes, process_write_bytes))
            if 8 in processes_treeview_columns_shown:
                processes_data_row.append(process_read_bytes)
            if 9 in processes_treeview_columns_shown:
                processes_data_row.append(process_write_bytes)
            if 10 in processes_treeview_columns_shown:
                if disk_read_write_data_prev == []:
                    process_read_bytes_prev = process_read_bytes                              # Make process_read_bytes_prev equal to process_read_bytes for giving "0" disk read speed value if this is first loop of the process
                else:
                    process_read_bytes_prev = disk_read_write_data_prev[pid_list.index(pid)][0]
                processes_data_row.append((process_read_bytes - int(process_read_bytes_prev)) / update_interval)    # Append process_read_bytes which will be used as "process_read_bytes_prev" value in the next loop and also append disk read speed. 
            if 11 in processes_treeview_columns_shown:
                if disk_read_write_data_prev == []:
                    process_write_bytes_prev = process_write_bytes                            # Make process_write_bytes_prev equal to process_write_bytes for giving "0" disk write speed value if this is first loop of the process
                else:
                    process_write_bytes_prev = disk_read_write_data_prev[pid_list.index(pid)][1]
                processes_data_row.append((process_write_bytes - int(process_write_bytes_prev)) / update_interval)    # Append process_write_bytes which will be used as "process_write_bytes_prev" value in the next loop and also append disk write speed. 
        if 12 in processes_treeview_columns_shown:
            processes_data_row.append(int(proc_pid_stat_lines_split[-34]))                    # Get process nice value
        if 13 in processes_treeview_columns_shown:
            processes_data_row.append(int(proc_pid_stat_lines_split[-33]))                    # Get process number of threads value
        if 14 in processes_treeview_columns_shown:
            processes_data_row.append(int(proc_pid_stat_lines_split[-49]))                    # Get process PPID
        if 15 in processes_treeview_columns_shown:
            processes_data_row.append(int(real_user_id))                                      # Append process UID value
        if 16 in processes_treeview_columns_shown:
            for line in proc_pid_status_lines:
                if "Gid:\t" in line:
                    processes_data_row.append(int(line.split(":")[1].split()[0].strip()))     # There are 4 values in the Gid line and first one (real GID) is get from this file.
        if 17 in processes_treeview_columns_shown:
            try:                                                                              # Executable path of some of the processes may not be get without root privileges or may not be get due to the reason of some of the processes may not have a exe file. "try-except" is used to be able to avoid errors due to these reasons.
                process_executable_path = os.path.realpath("/proc/" + pid + "/exe")
            except:
                process_executable_path = "-"
            processes_data_row.append(process_executable_path)                                # Append process executable path
        # Append process data into a list (processes_data_rows)
        processes_data_rows.append(processes_data_row)
    global_process_cpu_times_prev = global_process_cpu_times                                  # For using values in the next loop
    disk_read_write_data_prev = disk_read_write_data                                          # For using values in the next loop

    # Add/Remove treeview columns appropriate for user preferences
    ProcessesGUI.treeview2101.freeze_child_notify()                                           # For lower CPU consumption by preventing treeview updates on content changes/updates.
    if processes_treeview_columns_shown != processes_treeview_columns_shown_prev:             # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        for column in ProcessesGUI.treeview2101.get_columns():                                # Remove all columns in the treeview.
            ProcessesGUI.treeview2101.remove_column(column)
        for i, column in enumerate(processes_treeview_columns_shown):
            if processes_data_list[column][0] in processes_treeview_columns_shown:
                cumulative_sort_column_id = cumulative_sort_column_id + processes_data_list[column][2]
            processes_treeview_column = Gtk.TreeViewColumn(processes_data_list[column][1])    # Define column (also column title is defined)
            for i, cell_renderer_type in enumerate(processes_data_list[column][6]):
                cumulative_internal_data_id = cumulative_internal_data_id + 1
                if cell_renderer_type == "internal_column":                                   # Continue to next loop to avoid generating a cell renderer for internal column (internal columns are not shon on the treeview and they do not have cell renderers).
                    continue
                if cell_renderer_type == "CellRendererPixbuf":                                # Define cell renderer
                    cell_renderer = Gtk.CellRendererPixbuf()
                if cell_renderer_type == "CellRendererText":                                  # Define cell renderer
                    cell_renderer = Gtk.CellRendererText()
                cell_renderer.set_alignment(processes_data_list[column][9][i], 0.5)           # Vertical alignment is set 0.5 in order to leave it as unchanged.
                processes_treeview_column.pack_start(cell_renderer, processes_data_list[column][10][i])    # Set if column will allocate unused space
                processes_treeview_column.add_attribute(cell_renderer, processes_data_list[column][7][i], cumulative_internal_data_id)
                if processes_data_list[column][11][i] != "no_cell_function":
                    processes_treeview_column.set_cell_data_func(cell_renderer, processes_data_list[column][11][i], func_data=cumulative_internal_data_id)    # Define cell function which sets cell data precision and/or data unit
            processes_treeview_column.set_sizing(2)                                           # Set column sizing (2 = auto sizing which is required for "treeview2101.set_fixed_height_mode(True)" command that is used for lower treeview CPU consumption because row heights are not calculated for every row).
            processes_treeview_column.set_sort_column_id(cumulative_sort_column_id)           # Be careful with lists contain same element more than one.
            processes_treeview_column.set_resizable(True)                                     # Set columns resizable by the user when column title button edge handles are dragged.
            processes_treeview_column.set_reorderable(True)                                   # Set columns reorderable by the user when column title buttons are dragged.
            processes_treeview_column.set_min_width(40)                                       # Set minimum column widths as "40 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            processes_treeview_column.connect("clicked", on_column_title_clicked)             # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
            ProcessesGUI.treeview2101.append_column(processes_treeview_column)                # Append column into treeview

        # Get column data types for appending processes data into treestore
        processes_data_column_types = []
        for column in sorted(processes_treeview_columns_shown):
            internal_column_count = len(processes_data_list[column][5])
            for internal_column_number in range(internal_column_count):
                processes_data_column_types.append(processes_data_list[column][5][internal_column_number])    # Get column types (int, bool, float, str, etc.)

        # Define a treestore (for storing treeview data in it), a treemodelfilter (for search filtering), treemodelsort (for row sorting when column title buttons are clicked)
        global treestore2101                                                                  # Define as global variable because treestore is generated in statement and will not be defined in every loop and it will be used outside the statement.
        treestore2101 = Gtk.TreeStore()
        treestore2101.set_column_types(processes_data_column_types)                           # Set column types of the columns which will be appended into treestore
        treemodelfilter2101 = treestore2101.filter_new()
        treemodelfilter2101.set_visible_column(0)                                             # Column "0" of the treestore will be used for column visibility information (True or False)
        #ProcessesGUI.treeview2101.set_model(treemodelfilter2101)                             # If sorting will not be used, this command could be used instead of "ProcessesGUI.treeview3101.set_model(Gtk.TreeModelSort(model=treemodelfilter3101))".
        #treemodelsort2101 = Gtk.TreeModelSort.new_with_model(treemodelfilter2101)
        #ProcessesGUI.treeview2101.set_model(treemodelsort2101)                               # If one model is added, previous one is removed. In order to avoid from this behavior, treemodelfilter is added instead of standalone treestore. A treestore also is added into a treemodelfilter. This command is used instead of "PerformanceGUI.treeview2101.set_model(treemodelfilter2101)" in order to prevent "Gtk-CRITICAL **: ... gtk_tree_sortable_set_sort_column_id: assertion 'GTK_IS_TREE_SORTABLE (sortable)' failed" warnings.
        #ProcessesGUI.treeview2101.set_model(treestore2101)
        treemodelsort2101 = Gtk.TreeModelSort(treemodelfilter2101)
        ProcessesGUI.treeview2101.set_model(treemodelsort2101)
        pid_list_prev = []                                                                    # Redefine (clear) "pid_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
        global piter_list
        piter_list = []
    ProcessesGUI.treeview2101.thaw_child_notify()                                             # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
    if processes_treeview_columns_shown_prev != processes_treeview_columns_shown or processes_data_column_order_prev != processes_data_column_order:
        processes_treeview_columns = ProcessesGUI.treeview2101.get_columns()                  # Get shown columns on the treeview in order to use this data for reordering the columns.
        processes_treeview_columns_modified = ProcessesGUI.treeview2101.get_columns()
        treeview_column_titles = []
        for column in processes_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for order in reversed(sorted(processes_data_column_order)):                           # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
            if processes_data_column_order.index(order) <= len(processes_treeview_columns) - 1 and processes_data_column_order.index(order) in processes_treeview_columns_shown:
                column_number_to_move = processes_data_column_order.index(order)
                column_title_to_move = processes_data_list[column_number_to_move][1]
                column_to_move = processes_treeview_columns[treeview_column_titles.index(column_title_to_move)]
                column_title_to_move = column_to_move.get_title()
                for data in processes_data_list:
                    if data[1] == column_title_to_move:
                        ProcessesGUI.treeview2101.move_column_after(column_to_move, None)     # Column is moved at the beginning of the treeview if "None" is used.

    # Sort process rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
    if processes_treeview_columns_shown_prev != processes_treeview_columns_shown or processes_data_row_sorting_column_prev != processes_data_row_sorting_column or processes_data_row_sorting_order != processes_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
        processes_treeview_columns = ProcessesGUI.treeview2101.get_columns()                  # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_column_titles = []
        for column in processes_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i in range(10):
            if processes_data_row_sorting_column in processes_treeview_columns_shown:
                for data in processes_data_list:
                    if data[0] == processes_data_row_sorting_column:
                        column_title_for_sorting = data[1]
            if processes_data_row_sorting_column not in processes_treeview_columns_shown:
                column_title_for_sorting = processes_data_list[0][1]
            column_for_sorting = processes_treeview_columns[treeview_column_titles.index(column_title_for_sorting)]
            column_for_sorting.clicked()                                                  # For row sorting.
            if processes_data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                break

    # Set column widths if there are changes since last loop.
    if processes_treeview_columns_shown_prev != processes_treeview_columns_shown or processes_data_column_widths_prev != processes_data_column_widths:
        processes_treeview_columns = ProcessesGUI.treeview2101.get_columns()
        treeview_column_titles = []
        for column in processes_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i, processes_data in enumerate(processes_data_list):
            for j, column_title in enumerate(treeview_column_titles):
                if column_title == processes_data[1]:
                   column_width = processes_data_column_widths[i]
                   processes_treeview_columns[j].set_fixed_width(column_width)                # Set column width in pixels. Fixed width is unset if value is "-1".

    # Append treestore items (rows) as tree or list structure depending on user preferences.
    global show_processes_as_tree_prev
    show_processes_as_tree = Config.show_processes_as_tree
    if show_processes_as_tree != show_processes_as_tree_prev:                                 # Check if "show_processes_as_tree" setting has been changed since last loop and redefine "piter_list" in order to prevent resetting it in every loop which will cause high CPU consumption because piter_list and treestore content would have been appended/builded from zero.
        pid_list_prev = []                                                                    # Redefine (clear) "pid_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
        treestore2101.clear()                                                                 # Clear treestore because items will be appended from zero (in tree or list structure).
        piter_list = []

    # Get new/deleted(ended) processes for updating treestore/treeview
    pid_list_prev_set = set(pid_list_prev)
    pid_list_set = set(pid_list)
    deleted_processes = sorted(list(pid_list_prev_set - pid_list_set), key=int)               # "sorted(list, key=int)" is used for sorting string list (like "'1', '2', '10', '100'") as integer list without converting the list into integer list. Otherwise it is sorted like "'1', '10', '100', '2'".
    new_processes = sorted(list(pid_list_set - pid_list_prev_set), key=int)
    existing_processes = sorted(list(pid_list_set.intersection(pid_list_prev)), key=int)
    updated_existing_proc_index = [[pid_list.index(i), pid_list_prev.index(i)] for i in existing_processes]    # "c = set(a).intersection(b)" is about 19% faster than "c = set(a).intersection(set(b))"
    processes_data_rows_row_length = len(processes_data_rows[0])
    # Append/Remove/Update processes data into treestore
    ProcessesGUI.treeview2101.freeze_child_notify()                                           # For lower CPU consumption by preventing treeview updates on content changes/updates.
    global process_search_text, filter_process_type, filter_column
    if len(piter_list) > 0:
        for i, j in updated_existing_proc_index:
            if processes_data_rows[i] != processes_data_rows_prev[j]:
                for k in range(1, processes_data_rows_row_length):                            # Start from "1" in order to set first element (treeview row visibility data) as "True" in every loop.
                    if processes_data_rows_prev[j][k] != processes_data_rows[i][k]:
                        treestore2101.set_value(piter_list[j], k, processes_data_rows[i][k])
    if len(deleted_processes) > 0:
        for process in reversed(sorted(list(deleted_processes), key=int)):
            treestore2101.remove(piter_list[pid_list_prev.index(process)])
            piter_list.remove(piter_list[pid_list_prev.index(process)])
    if len(new_processes) > 0:
        for process in new_processes:
            # /// Start /// This block of code is used for determining if the newly added process will be shown on the treeview (user search actions and/or search customizations and/or "Show processes from this user/other users ..." preference affect process visibility).
            if ProcessesGUI.radiobutton2102.get_active() == True and username_list[pid_list.index(process)] != current_user_name:    # Hide process (set the visibility value as "False") if "Show processes from this user" option is selected on the GUI and process username is not same as name of current user.
                processes_data_rows[pid_list.index(process)][0] = False
            if ProcessesGUI.radiobutton2103.get_active() == True and username_list[pid_list.index(process)] == current_user_name:    # Hide process (set the visibility value as "False") if "Show processes from other users" option is selected on the GUI and process username is same as name of current user.
                processes_data_rows[pid_list.index(process)][0] = False
            if ProcessesGUI.searchentry2101.get_text() != "":
                process_data_text_in_model = processes_data_rows[pid_list.index(process)][filter_column]
                username_in_model = username_list[pid_list.index(process)]
                if process_search_text not in str(process_data_text_in_model).lower():        # Hide process (set the visibility value as "False") if search text (typed into the search entry) is not in the appropriate column of the process data.
                    processes_data_rows[pid_list.index(process)][0] = False
                if username_in_model not in filter_process_type:                              # Hide process (set the visibility value as "False") if username of the process is not in the filter_process_type (this list is constructed by using user preferred options on the "Processes Search Customizations" tab).
                    processes_data_rows[pid_list.index(process)][0] = False
            # \\\ End \\\ This block of code is used for determining if the newly added process will be shown on the treeview (user search actions and/or search customizations and/or "Show processes from this user/other users ..." preference affect process visibility).
            if show_processes_as_tree == 1:
                if ppid_list[pid_list.index(process)] == "0":                                 # Process ppid was set as "0" if it has no parent process. Process is set as tree root (this root has no relationship between root user) process if it has no ppid (parent process). Treeview tree indentation is first level for the tree root proceess.
                    piter_list.append(treestore2101.append(None, processes_data_rows[pid_list.index(process)]))
                if ppid_list[pid_list.index(process)] != "0":
                    if show_processes_of_all_users == 1:                                      # Process appended under tree root process or another process if "Show processes as tree" option is preferred.
                        piter_list.append(treestore2101.append(piter_list[pid_list.index(ppid_list[pid_list.index(process)])], processes_data_rows[pid_list.index(process)]))
                    parent_process = ppid_list[pid_list.index(process)]                       # Define parent process of the process in order to avoid calculating it multiple times for faster processing.
                    if show_processes_of_all_users == 0 and parent_process not in pid_list:   # Process is appended into treeview as tree root process if "Show processes of all users" is not preferred and process ppid not in pid_list.
                        piter_list.append(treestore2101.append(None, processes_data_rows[pid_list.index(process)]))
                    if show_processes_of_all_users == 0 and parent_process in pid_list:       # Process is appended into treeview under tree root process or another process if "Show processes of all users" is preferred and process ppid is in pid_list.
                        piter_list.append(treestore2101.append(piter_list[pid_list.index(ppid_list[pid_list.index(process)])], processes_data_rows[pid_list.index(process)]))
            if show_processes_as_tree == 0:                                                   # All processes are appended into treeview as tree root process if "Show processes as tree" is not preferred. Thus processes are listed as list structure instead of tree structure.
                piter_list.insert(pid_list.index(process), treestore2101.insert(None, pid_list.index(process), processes_data_rows[pid_list.index(process)]))
    ProcessesGUI.treeview2101.thaw_child_notify()                                             # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    if pid_list_prev == []:                                                                   # Expand all treeview rows (if treeview items are in tree structured, not list) if this is the first loop of the Processes tab. It expands treeview rows (and children) in all loops if this control is not made. "First loop" control is made by checking if pid_list_prev is empty.
        ProcessesGUI.treeview2101.expand_all()

    pid_list_prev = pid_list
    processes_data_rows_prev = processes_data_rows
    show_processes_as_tree_prev = show_processes_as_tree
    processes_treeview_columns_shown_prev = processes_treeview_columns_shown
    processes_data_row_sorting_column_prev = processes_data_row_sorting_column
    processes_data_row_sorting_order_prev = processes_data_row_sorting_order
    processes_data_column_order_prev = processes_data_column_order
    processes_data_column_widths_prev = processes_data_column_widths

    # Get number of processes from current user and number of all processses and show these information on the GUI label
    current_user_process_count = username_list.count(current_user_name)
    number_of_all_processes = len(username_list)
    ProcessesGUI.label2101.set_text(_tr("Total: ") + str(number_of_all_processes) + _tr(" processes (") + str(current_user_process_count) + _tr(" from this user, ") + str(number_of_all_processes-current_user_process_count) + _tr(" from other users/system)"))    # f strings have lower CPU usage than joining method but strings are joinied by by this method because gettext could not be worked with Python f strings.

    # Show/Hide treeview expander arrows
    if show_processes_as_tree == 1:
        ProcessesGUI.treeview2101.set_show_expanders(True)                                    # Show expander arrows (default is True) if "Show processes as tree" option is preferred. If "child rows" are not used and there is no need for these expanders (they would be shown as empty spaces in this situation).
    if show_processes_as_tree == 0:
        ProcessesGUI.treeview2101.set_show_expanders(False)                                   # Hide expander arrows (default is True) if "Show processes as tree" option is not preferred.

    # Show/Hide treeview tree lines
    if Config.show_tree_lines == 1:
        ProcessesGUI.treeview2101.set_enable_tree_lines(True)                                 # Show tree lines for tree view of processes (default is False).
    if Config.show_tree_lines == 0:
        ProcessesGUI.treeview2101.set_enable_tree_lines(False)                                # Hide tree lines for tree view of processes. There is no need for showing tree lines for list view of processes.


# ----------------------------------- Processes - Treeview Cell Functions (defines functions for treeview cell for setting data precisions and/or data units) -----------------------------------
def cell_data_function_cpu_usage_percent(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{tree_model.get(iter, data)[0]:.{processes_cpu_usage_percent_precision}f} %')

def cell_data_function_ram_swap(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{processes_data_unit_converter_func(tree_model.get(iter, data)[0], processes_ram_swap_data_unit, processes_ram_swap_data_precision)}')

def cell_data_function_disk_usage(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{processes_data_unit_converter_func(tree_model.get(iter, data)[0], processes_disk_usage_data_unit, processes_disk_usage_data_precision)}')

def cell_data_function_disk_speed(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{processes_data_unit_converter_func(tree_model.get(iter, data)[0], processes_disk_speed_data_unit, processes_disk_speed_data_precision)}/s')


# ----------------------------------- Processes Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def processes_initial_thread_func():

    GLib.idle_add(processes_initial_func)


# ----------------------------------- Processes Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def processes_loop_thread_func():

    GLib.idle_add(processes_loop_func)
    if MainGUI.radiobutton2.get_active() is True:                                             # "is/is not" is about 15% faster than "==/!="
        global update_interval
        update_interval = Config.update_interval
        GLib.timeout_add(update_interval * 1000, processes_loop_thread_func)


# ----------------------------------- Processes Thread Run Function (starts execution of the threads) -----------------------------------
def processes_thread_run_func():

    if "number_of_logical_cores" not in globals():                                            # To be able to run initial thread for only one time
        processes_initial_thread = Thread(target=processes_initial_thread_func, daemon=True)
        processes_initial_thread.start()
        processes_initial_thread.join()
    processes_loop_thread = Thread(target=processes_loop_thread_func, daemon=True)
    processes_loop_thread.start()


# ----------------------------------- Processes - Treeview Filter Show All Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def processes_treeview_filter_show_all_func():

    for piter in piter_list:
        treestore2101.set_value(piter, 0, True)
    ProcessesGUI.treeview2101.expand_all()


# ----------------------------------- Processes - Treeview Filter This User Only Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def processes_treeview_filter_this_user_only_func():

    for piter in piter_list:
        if username_list[piter_list.index(piter)] != current_user_name:
            treestore2101.set_value(piter, 0, False)
    ProcessesGUI.treeview2101.expand_all()


# ----------------------------------- Processes - Treeview Filter Other Users Only Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def processes_treeview_filter_other_users_only_func():

    for piter in piter_list:
        if username_list[piter_list.index(piter)] == current_user_name:
            treestore2101.set_value(piter, 0, False)
    ProcessesGUI.treeview2101.expand_all()


# ----------------------------------- Processes - Treeview Filter Search Function (updates treeview shown rows when text typed into entry) -----------------------------------
def processes_treeview_filter_search_func():

    # Determine filtering column (name, username, PID, etc) for hiding/showing processes by using search text typed into search entry.
    global process_search_text, filter_process_type, filter_column
    if ProcessesMenusGUI.radiobutton2101p2.get_active() == True:
        if 0 in processes_treeview_columns_shown:                                             # "0" is treeview column number
            filter_column = 2                                                                 # Append internal column number (2) of "process name" for filtering
    if ProcessesMenusGUI.radiobutton2102p2.get_active() == True:
        if 1 in processes_treeview_columns_shown:                                             # "1" is treeview column number
            filter_column = 3                                                                 # Append internal column number (3) of "PID" for filtering
    if ProcessesMenusGUI.radiobutton2103p2.get_active() == True:
        if 2 in processes_treeview_columns_shown:                                             # "2" is treeview column number
            filter_column = 4                                                                 # Append internal column number (4) of "user name" for filtering
    if ProcessesMenusGUI.radiobutton2104p2.get_active() == True:
        if 3 in processes_treeview_columns_shown:                                             # "3" is treeview column number
            filter_column = 5                                                                 # Append internal column number (5) of "status" for filtering
    if ProcessesMenusGUI.radiobutton2105p2.get_active() == True:
        if 14 in processes_treeview_columns_shown:                                            # "14" is treeview column number
            filter_column = 16                                                                # Append internal column number (16) of "UID" for filtering
    if ProcessesMenusGUI.radiobutton2106p2.get_active() == True:
        if 17 in processes_treeview_columns_shown:                                            # "17" is treeview column number
            filter_column = 19                                                                # Append internal column number (19) of "path" for filtering
    # Processes could be shown/hidden for specific user names. Preferred user names are determined here.
    filter_process_type = []
    if ProcessesMenusGUI.checkbutton2102p2.get_active() == True:
        filter_process_type.append(current_user_name)
    if ProcessesMenusGUI.checkbutton2103p2.get_active() == True:
        username_list_unique = list(set(username_list))
        for username in username_list_unique:
            if username != current_user_name:
                filter_process_type.append(username)

    process_search_text = ProcessesGUI.searchentry2101.get_text().lower()
    # Set visible/hidden processes
    for piter in piter_list:
        treestore2101.set_value(piter, 0, False)
        process_data_text_in_model = treestore2101.get_value(piter, filter_column)
        if process_search_text in str(process_data_text_in_model).lower():
            treestore2101.set_value(piter, 0, True)
            username_in_model = username_list[piter_list.index(piter)]
            if username_in_model not in filter_process_type:
                treestore2101.set_value(piter, 0, False)
            if treestore2101.get_value(piter, 0) == True:                                     # Make parent processes visible if one of its children is visible.
                piter_parent = treestore2101.iter_parent(piter)
                while piter_parent != None:
                    treestore2101.set_value(piter_parent, 0, True)
                    piter_parent = treestore2101.iter_parent(piter_parent)

    ProcessesGUI.treeview2101.expand_all()                                                    # Expand all treeview rows (if tree view is preferred) after filtering is applied (after any text is typed into search entry).


# ----------------------------------- Processes - Column Title Clicked Function (gets treeview column number (id) and row sorting order by being triggered by Gtk signals) -----------------------------------
def on_column_title_clicked(widget):

    processes_data_row_sorting_column_title = widget.get_title()                              # Get column title which will be used for getting column number
    for data in processes_data_list:
        if data[1] == processes_data_row_sorting_column_title:
            Config.processes_data_row_sorting_column = data[0]                                # Get column number
    Config.processes_data_row_sorting_order = int(widget.get_sort_order())                    # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    Config.config_save_func()


# ----------------------------------- Processes - Treeview Column Order-Width Row Sorting Function (gets treeview column order/widths and row sorting) -----------------------------------
def processes_treeview_column_order_width_row_sorting_func():
    # Columns in the treeview are get one by one and appended into "processes_data_column_order". "processes_data_column_widths" list elements are modified for widths of every columns in the treeview. Length of these list are always same even if columns are removed, appended and column widths are changed. Only values of the elements (element indexes are always same with "processes_data") are changed if column order/widths are changed.
    processes_treeview_columns = ProcessesGUI.treeview2101.get_columns()
    treeview_column_titles = []
    for column in processes_treeview_columns:
        treeview_column_titles.append(column.get_title())
    for i, processes_data in enumerate(processes_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == processes_data[1]:
                Config.processes_data_column_order[i] = j
                Config.processes_data_column_widths[i] = processes_treeview_columns[j].get_width()
                break
    Config.config_save_func()


# ----------------------------------- Processes - Define Window Function (defines a window by a user mouse click and highlights process of the defined window process on the proces list (on treeview)) -----------------------------------
def processes_define_window_func():

    global processes_define_window_stop_loop
    processes_define_window_stop_loop = 0                                                     # This is a variable to check if defining window is completed and to stop loop for watching active window PIDs.
    changed_cursor = Gdk.Cursor(Gdk.CursorType.CROSSHAIR)                                     # Define "cross hair" cursor type to be used after clicking "Define Window" button in order to inform user that defining function is ready.
    MainGUI.window1.get_window().set_cursor(changed_cursor)                                   # Set "cross hair" cursor type

    def processes_define_window_initial_func():                                               # Initial function that will be run once after "Define Window" button is clicked.
        global current_process_pid
        current_process_pid = os.getpid()                                                     # Get current application window (system monitor window) PID to check if it is changed. It means user clicked on a window if it is changed. Therefore loop function is not run anymore.

    def processes_define_window_func():                                                       # Loop function that will be run repeatedly in order to watch for active window PIDs.
        global processes_define_window_stop_loop
        default_screen = Wnck.Screen.get_default()                                            # Get default screen
        default_screen.force_update()                                                         # Force update "wnck". "wnck" has an internal updating mechanism and it will give same output in some situations if this "force update" is not used.
        active_window = default_screen.get_active_window()                                    # Get active window (top most window). Because window will be topmost window when user clicks on it.
        active_window_pid = active_window.get_pid()                                           # Get PID of active window
        active_window = None                                                                  # Set active window as None in order to save memory resources
        default_screen = None                                                                 # Set default screen as None in order to save memory resources
        Wnck.shutdown()                                                                       # Use this command in order to save memory resources
        if active_window_pid == 0 or active_window_pid == None:                               # Some window managers give window PID as "0" or "None". This is not fault of "wnck". In this case, this statement is used in order to avoid errors.
            changed_cursor = Gdk.Cursor(Gdk.CursorType.ARROW)                                 # Define default cursor (ARROW) if window PID is get as "0" or "None".
            MainGUI.window1.get_window().set_cursor(changed_cursor)                           # Set default cursor (ARROW) if window PID is get as "0" or "None".
            processes_define_window_stop_loop = 1                                             # Set the variable a "1" in order to prevent running loop function since clicking on a window is done even window PID is get as "0" or "None".
            return                                                                            # Stop running function
        if active_window_pid > 0 and active_window_pid != current_process_pid:                # If active window PID is not get as "0" or "None" run the following code (scroll to treeview row of the active window process).
            model = ProcessesGUI.treeview2101.get_model()                                     # Get model (in this case treemodelsort is get.) connected to the treeview.
            child_path = treestore2101.get_path(piter_list[pid_list.index(str(active_window_pid))])    # "child_path" is the path in the child model. Treeview model has treestore, treemodelfilter and treemodelsort. There is a child/parent model relationship due to this structure. Therefore, path and child path are different. It selects incorrect row (as if row sorting is not applied) if wrong path is used.
            path = model.convert_child_path_to_path(child_path)                               # Get path by using child_path.
            get_iter = model.get_iter(path)                                                   # Get iter by using path.
            ProcessesGUI.treeview2101.get_selection().select_iter(get_iter)                   # Select row on the treeview by using iter.
            column = ProcessesGUI.treeview2101.get_column(0)                                  # Get first column on the treeview (This is required to scroll to a treeview row. Column "0" is used because column number is not necessary in this situation and using the first one is safer.)
            ProcessesGUI.treeview2101.scroll_to_cell(path, column, False)                     # Scroll to a cell (therefore  scroll to its row) of the active window process
            changed_cursor = Gdk.Cursor(Gdk.CursorType.ARROW)                                 # Define default cursor (ARROW) if window PID is get as "0" or "None".
            MainGUI.window1.get_window().set_cursor(changed_cursor)                           # Set default cursor (ARROW) if window PID is get as "0" or "None".
            processes_define_window_stop_loop = 1                                             # Set the variable a "1" in order to prevent running loop function since clicking on a window is done.
            return                                                                            # Stop running function

    def processes_define_window_initial_thread_func():                                        # A function to run initial function as threaded and prevent blocking Gtk signals/events.
        GLib.idle_add(processes_define_window_initial_func)

    def processes_define_window_loop_thread_func():                                           # A function to run loop function as threaded and prevent blocking Gtk signals/events.
        GLib.idle_add(processes_define_window_func)
        if processes_define_window_stop_loop != 1 and MainGUI.window1.get_visible() == True:    # Also check if main window is visible. If window is closed, this function is not repeated and thread is ended. Therefore, there is no working process is left after window closed. "is/is not" is about 15% faster than "==/!="
            GLib.timeout_add(200, processes_define_window_loop_thread_func)                   # 200 milliseconds value is used for waiting before rerunning the loop function

    def processes_define_window_thread_run_func():                                            # A funciton to run threads for initial and loop functions
        processes_define_window_initial_thread = Thread(target=processes_define_window_initial_thread_func, daemon=True)
        processes_define_window_initial_thread.start()
        processes_define_window_initial_thread.join()
        processes_define_window_loop_thread = Thread(target=processes_define_window_loop_thread_func, daemon=True)
        processes_define_window_loop_thread.start()
    processes_define_window_thread_run_func()                                                 # Run the function in order to start threads


# ----------------------------------- Processes - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def processes_define_data_unit_converter_variables_func():

    global data_unit_list

    # Calculated values are used in order to obtain faster code run, because this function will be called very frequently. For the details of the calculation, see "Data_unit_conversion.ods." document.

    data_unit_list = [[0, 0, _tr("Auto-Byte")], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, _tr("Auto-bit")], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Processes - Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def processes_data_unit_converter_func(data, unit, precision):

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

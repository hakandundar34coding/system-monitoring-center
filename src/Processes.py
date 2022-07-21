#!/usr/bin/env python3

# ----------------------------------- Processes - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def processes_import_func():

    global Gtk, Gdk, GLib, GObject, os, time

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GLib', '2.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('GObject', '2.0')
    from gi.repository import Gtk, Gdk, GLib, GObject
    import os
    import time


    global Config, Performance
    from Config import Config
    from Performance import Performance

    # Import gettext module for defining translation texts which will be recognized by gettext application. These lines of code are enough to define this variable if another values are defined in another module (Main GUI module) before importing this module.
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    from locale import gettext as _tr


# ----------------------------------- Processes - Processes GUI Function (the code of this module in order to avoid running them during module import and defines "Processes" tab GUI objects and functions/signals) -----------------------------------
def processes_gui_func():

    # Processes tab GUI objects
    global grid2101, treeview2101, searchentry2101, button2101

    # Processes tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesTab.ui")

    # Processes tab GUI objects - get
    grid2101 = builder.get_object('grid2101')
    treeview2101 = builder.get_object('treeview2101')
    searchentry2101 = builder.get_object('searchentry2101')
    button2101 = builder.get_object('button2101')

    # Processes tab GUI functions - connect
    treeview2101.connect("button-press-event", on_treeview2101_button_press_event)
    treeview2101.connect("button-release-event", on_treeview2101_button_release_event)
    treeview2101.connect("key-press-event", on_treeview2101_key_press_event)
    searchentry2101.connect("changed", on_searchentry2101_changed)
    button2101.connect("clicked", on_button2101_clicked)

    # Processes Tab - Treeview Properties
    treeview2101.set_activate_on_single_click(True)                                           # This command used for activating rows and column header buttons on single click. Column headers have to clicked twice (or clicked() command have to be used twice) for the first sorting operation if this is not used.
    treeview2101.set_fixed_height_mode(True)                                                  # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview2101.set_headers_clickable(True)
    treeview2101.set_enable_search(True)                                                      # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview2101.set_search_column(2)                                                         # This command used for searching by using entry.
    treeview2101.set_tooltip_column(2)

    global initial_already_run
    initial_already_run = 0


# --------------------------------- Called for running code/functions when button is pressed on the treeview ---------------------------------
def on_treeview2101_button_press_event(widget, event):

    # Get right/double clicked row data
    try:                                                                                  # "try-except" is used in order to prevent errors when right clicked on an empty area on the treeview.
        path, _, _, _ = treeview2101.get_path_at_pos(int(event.x), int(event.y))
    except TypeError:
        return
    model = treeview2101.get_model()
    treeiter = model.get_iter(path)

    # Get right/double clicked process PID
    if treeiter == None:
        return
    global selected_process_pid
    try:
        selected_process_pid = pid_list[processes_data_rows.index(model[treeiter][:])]
    # It gives error such as "ValueError: [True, 'system-monitoring-center-process-symbolic', 'python3', 2411, 'asush', 'Running', 1.6633495783351964, 98824192, 548507648, 45764608, 0, 16384, 0, 5461, 0, 4, 1727, 1000, 1000, '/usr/bin/python3.9'] is not in list" rarely. It is handled in this situation.
    except ValueError:
        return

    # Open right click menu if right clicked on a row
    if event.button == 3:
        from ProcessesMenuRightClick import ProcessesMenuRightClick
        ProcessesMenuRightClick.processes_add_remove_expand_collapse_menuitems_func()
        ProcessesMenuRightClick.processes_select_process_nice_option_func()
        ProcessesMenuRightClick.menu2101m.popup_at_pointer()

    # Open details window if double clicked on a row
    if event.type == Gdk.EventType._2BUTTON_PRESS:
        from ProcessesDetails import ProcessesDetails
        ProcessesDetails.window2101w.show()


# --------------------------------- Called for running code/functions when button is released on the treeview ---------------------------------
def on_treeview2101_button_release_event(widget, event):

    # Check if left mouse button is used
    if event.button == 1:
        processes_treeview_column_order_width_row_sorting_func()


# --------------------------------- Called for running code/functions when keyboard buttons (shortcuts such as Ctrl+C) is pressed on the treeview ---------------------------------
def on_treeview2101_key_press_event(widget, event):

    # Get selected row data.
    selection = treeview2101.get_selection()
    model, treeiter = selection.get_selected()

    # Get selected process PID
    if treeiter == None:
        return
    global selected_process_pid
    try:
        selected_process_pid = pid_list[processes_data_rows.index(model[treeiter][:])]
    # It gives error such as "ValueError: [True, 'system-monitoring-center-process-symbolic', 'python3', 2411, 'asush', 'Running', 1.6633495783351964, 98824192, 548507648, 45764608, 0, 16384, 0, 5461, 0, 4, 1727, 1000, 1000, '/usr/bin/python3.9'] is not in list" rarely. It is handled in this situation.
    except ValueError:
        return

    from ProcessesMenuRightClick import ProcessesMenuRightClick

    # Check if Ctrl and S keys are pressed at the same time.
    if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_s:
        ProcessesMenuRightClick.on_process_manage_menuitems_activate(ProcessesMenuRightClick.menuitem2101m)
        return

    # Check if Ctrl and C keys are pressed at the same time.
    if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_c:
        ProcessesMenuRightClick.on_process_manage_menuitems_activate(ProcessesMenuRightClick.menuitem2102m)
        return

    # Check if Ctrl and T keys are pressed at the same time.
    if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_t:
        ProcessesMenuRightClick.on_process_manage_menuitems_activate(ProcessesMenuRightClick.menuitem2103m)
        return

    # Check if Ctrl and K keys are pressed at the same time.
    if event.state & Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_k:
        ProcessesMenuRightClick.on_process_manage_menuitems_activate(ProcessesMenuRightClick.menuitem2104m)
        return


# --------------------------------- Called for searching items when searchentry text is changed ---------------------------------
def on_searchentry2101_changed(widget):

    global filter_column
    process_search_text = searchentry2101.get_text().lower()
    # Set visible/hidden processes
    for piter in piter_list:
        treestore2101.set_value(piter, 0, False)
        process_data_text_in_model = treestore2101.get_value(piter, filter_column)
        if process_search_text in str(process_data_text_in_model).lower():
            treestore2101.set_value(piter, 0, True)
            # Make parent processes visible if one of its children is visible.
            piter_parent = treestore2101.iter_parent(piter)
            while piter_parent != None:
                treestore2101.set_value(piter_parent, 0, True)
                piter_parent = treestore2101.iter_parent(piter_parent)
    # Expand all treeview rows (if tree view is preferred) after filtering is applied (after any text is typed into search entry).
    treeview2101.expand_all()


# --------------------------------- Called for showing Processes tab customization menu when button is clicked ---------------------------------
def on_button2101_clicked(widget):

    from ProcessesMenuCustomizations import ProcessesMenuCustomizations
    # Set widget that popover menu will display at the edge of it, define popover position and show popover.
    ProcessesMenuCustomizations.popover2101p.set_relative_to(button2101)
    ProcessesMenuCustomizations.popover2101p.set_position(1)
    ProcessesMenuCustomizations.popover2101p.popup()


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
                          [0, _tr('Name'), 3, 2, 3, [bool, str, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'icon_name', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
                          [1, _tr('PID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [2, _tr('User'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                          [3, _tr('Status'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                          [4, _tr('CPU'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_cpu_usage_percent]],
                          [5, _tr('Memory (RSS)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_ram_swap]],
                          [6, _tr('Memory (VMS)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_ram_swap]],
                          [7, _tr('Memory (Shared)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_ram_swap]],
                          [8, _tr('Read Data'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_usage]],
                          [9, _tr('Write Data'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_usage]],
                          [10, _tr('Read Speed'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_speed]],
                          [11, _tr('Write Speed'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_speed]],
                          [12, _tr('Priority'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [13, _tr('Threads'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [14, _tr('PPID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [15, _tr('UID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [16, _tr('GID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [17, _tr('Path'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                          [18, _tr('Command Line'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']]
                          ]

    # Define data unit conversion function objects in for lower CPU usage.
    global performance_define_data_unit_converter_variables_func, performance_define_data_unit_converter_variables_func, performance_data_unit_converter_func
    performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
    performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

    # Define data unit conversion variables before they are used.
    performance_define_data_unit_converter_variables_func()


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
    process_status_list = {"R": _tr("Running"), "S": _tr("Sleeping"), "D": _tr("Waiting"), "I": _tr("Idle"), "Z": _tr("Zombie"), "T": _tr("Stopped"), "t": "Tracing Stop", "X": "Dead"}    # This list is used in order to show full status of the process. For more information, see: "https://man7.org/linux/man-pages/man5/proc.5.html".
    number_of_clock_ticks = os.sysconf("SC_CLK_TCK")                                          # For many systems CPU ticks 100 times in a second. Wall clock time could be get if CPU times are multiplied with this value or vice versa.
    memory_page_size = os.sysconf("SC_PAGE_SIZE")                                             # This value is used for converting memory page values into byte values. This value depends on architecture (also sometimes depends on machine model). Default value is 4096 Bytes (4 KiB) for most processors.

    global application_exec_list, application_icon_list                                       # Process names will be checked if they are in these lists. If process names cold not be found in these lists, "application" icon will be shown.
    application_exec_list = []
    application_icon_list = []
    application_file_list = [file for file in os.listdir("/usr/share/applications/") if file.endswith(".desktop")]    # Get  ".desktop" file name
    for application in application_file_list:
        with open("/usr/share/applications/" + application) as reader:
            application_file_content = reader.read()
        if "Exec=" not in application_file_content or "Icon=" not in application_file_content:    # Do not include application name or icon name if any of them is not found in the .desktop file.
            continue
        application_exec = application_file_content.split("Exec=", 1)[1].split("\n", 1)[0].split("/")[-1].split(" ")[0]    # Get application exec data
        if application_exec != "sh":                                                          # Splitting operation above may give "sh" as application name and this may cause confusion between "sh" process and splitted application exec (for example: sh -c "gdebi-gtk %f"sh -c "gdebi-gtk %f"). This statement is used to avoid from this confusion.
            application_exec_list.append(application_exec)
        else:
            application_exec_list.append(application_file_content.split("Exec=", 1)[1].split("\n", 1)[0])
        application_icon_list.append(application_file_content.split("Icon=", 1)[1].split("\n", 1)[0])    # Get application icon name data

    global filter_column
    filter_column = processes_data_list[0][2] - 1                                             # Search filter is "Process Name". "-1" is used because "processes_data_list" has internal column count and it has to be converted to Python index. For example, if there are 3 internal columns but index is 2 for the last internal column number for the relevant treeview column.

    global initial_already_run
    initial_already_run = 1


# ----------------------------------- Processes - Get Process Data Function (gets processes data, adds into treeview and updates it) -----------------------------------
def processes_loop_func():

    update_interval = Config.update_interval

    # Get GUI obejcts one time per floop instead of getting them multiple times
    global treeview2101

    # Get configrations one time per floop instead of getting them multiple times (hundreds of times for many of them) in every loop which causes high CPU usage.
    global processes_cpu_precision
    global processes_memory_data_precision, processes_memory_data_unit
    global processes_disk_data_precision, processes_disk_data_unit, processes_disk_speed_bit
    processes_cpu_precision = Config.processes_cpu_precision
    processes_memory_data_precision = Config.processes_memory_data_precision
    processes_memory_data_unit = Config.processes_memory_data_unit
    processes_disk_data_precision = Config.processes_disk_data_precision
    processes_disk_data_unit = Config.processes_disk_data_unit
    processes_disk_speed_bit = Config.processes_disk_speed_bit

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
    except ValueError:
        with open("/proc/cpuinfo") as reader:                                                 # As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
            proc_cpuinfo_lines = reader.read().split("\n")
        number_of_logical_cores = 0
        for line in proc_cpuinfo_lines:
            if line.startswith("processor"):
                number_of_logical_cores = number_of_logical_cores + 1

    # Get human and root user usernames and UIDs only one time at the per loop in order to avoid running it per process loop (it is different than main loop = processes_loop_func) which increases CPU consumption.
    usernames_username_list = []
    usernames_uid_list = []
    with open("/etc/passwd") as reader:
        etc_passwd_lines = reader.read().strip().split("\n")
    for line in etc_passwd_lines:
        line_splitted = line.split(":", 3)
        usernames_username_list.append(line_splitted[0])
        usernames_uid_list.append(line_splitted[2])

    # Get current username which will be used for determining processes from only this user or other users.
    global current_user_name
    current_user_name = os.environ.get('USER')

    # Get process PIDs and define global variables and empty lists for the current loop
    global processes_data_rows, processes_data_rows_prev, global_process_cpu_times_prev, disk_read_write_data_prev, pid_list, pid_list_prev, username_list
    processes_data_rows = []
    ppid_list = []
    username_list = []
    global_process_cpu_times = []
    disk_read_write_data = []
    pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]          # Get process PID list. PID values are appended as string values because they are used as string values in various places in the code and this ensures lower CPU usage by avoiding hundreds/thousands of times integer to string conversion.

    processes_treeview_columns_shown = set(processes_treeview_columns_shown)                  # For obtaining lower CPU usage (because "if [number] in processes_treeview_columns_shown:" check is repeated thousand of times).

    # Get user names of the processes
    for pid in pid_list[:]:                                                                   # "[:]" is used for iterating over copy of the list because elements are removed during iteration. Otherwise incorrect operations (incorrect element removals) are performed on the list.
        try:                                                                                  # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
            with open(f'/proc/{pid}/status') as reader:                                       # User name of the process owner is get from "/proc/status" file because it is not present in "/proc/stat" file.
                proc_pid_status_output = reader.read()
        except FileNotFoundError:                                                             # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
            pid_list.remove(pid)
            continue
        real_user_id = proc_pid_status_output.split("\nUid:\t", 1)[1].split("\n", 1)[0].split("\t", 1)[0]    # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
        try:
            username = usernames_username_list[usernames_uid_list.index(real_user_id)]
        except ValueError:
            username = real_user_id
        username_list.append(username)
        # Remove PIDs of processes from other than current user (show processes only from this user) if it is preferred by user
        if show_processes_of_all_users == 0:
            if username != current_user_name:
                pid_list.remove(pid)
                del username_list[-1]                                                         # Remove last username which has been appended in this loop. It is removed because its process PID has been removed (because it is not owned by current user).
                continue

        # Get process data
        global_cpu_time_all = time.time() * number_of_clock_ticks                             # global_cpu_time_all value is get just before "/proc/[PID]/stat file is read in order to measure global an process specific CPU times at the same time (nearly) for ensuring accurate process CPU usage percent. global_cpu_time_all value is get by using time module of Python instead of reading "/proc/stat" file for faster processing.
        try:                                                                                  # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
            with open(f'/proc/{pid}/stat') as reader:                                         # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
                proc_pid_stat_lines = reader.read()
        except (FileNotFoundError, ProcessLookupError) as me:
            pid_list.remove(pid)
            continue
        proc_pid_stat_lines_split = proc_pid_stat_lines.split()
        ppid_list.append(proc_pid_stat_lines_split[-49])                                      # Process data is get by negative indexes because file content is split by " " (empty space) character and also process name could contain empty space character which may result confusion getting correct process data. In other words empty space character count may not be same for all process "stat" files and process name it at the second place in the file. Reading process data of which turn is later than process name by using negative index is a reliable method.
        process_name_from_stat = proc_pid_stat_lines.split("(", 1)[1].rsplit(")", 1)[0]
        process_name = process_name_from_stat
        if len(process_name) == 15:                                                           # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name.
            try:
                with open(f'/proc/{pid}/cmdline') as reader:
                    process_cmdline = reader.read().replace("\x00", " ")                      # Some process names which are obtained from "cmdline" contain "\x00" and these are replaced by " ".
            except FileNotFoundError:
                pid_list.remove(pid)
                continue
            process_name = process_cmdline.split("/")[-1].split(" ")[0]
            if process_name.startswith(process_name_from_stat) == False:
                process_name = process_cmdline.split(" ")[0].split("/")[-1]
                if process_name.startswith(process_name_from_stat) == False:
                    process_name = process_name_from_stat
        process_icon = "system-monitoring-center-process-symbolic"                            # Initial value of "process_icon". This icon will be shown for processes of which icon could not be found in default icon theme.
        if process_name in application_exec_list:                                             # Use process icon name from application file if process name is found in application exec list.
            process_icon = application_icon_list[application_exec_list.index(process_name)]
        processes_data_row = [True, process_icon, process_name]                               # Process row visibility data (True/False) which is used for showing/hiding process when processes of specific user is preferred to be shown or process search feature is used from the GUI.
        if 1 in processes_treeview_columns_shown:
            processes_data_row.append(int(pid))                                               # Append process PID. Value is appended as integer for ensuring correct "PID" column sorting such as 1,2,10,101... Otherwise it would sort such as 1,10,101,2...
        if 2 in processes_treeview_columns_shown:
            processes_data_row.append(username)                                               # Append process username (this value is get before).
        if 3 in processes_treeview_columns_shown:
            processes_data_row.append(process_status_list[proc_pid_stat_lines_split[-50]])    # Get process status
        if 4 in processes_treeview_columns_shown:
            process_cpu_time = int(proc_pid_stat_lines_split[-39]) + int(proc_pid_stat_lines_split[-38])   # Get process cpu time in user mode (utime + stime)
            global_process_cpu_times.append((global_cpu_time_all, process_cpu_time))          # While appending multiple elements into a list "append((value1, value2))" is faster than "append([value1, value2])".
            try:                                                                              # It gives various errors (ValueError, IndexError, UnboundLocalError) if a new process is started, a new column is shown on the treeview, etc because previous CPU time values are not present in these situations. Following CPU time values are used in these situations.
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
                with open(f'/proc/{pid}/statm') as reader:                                   
                    processes_data_row.append(int(reader.read().split()[2]) * memory_page_size)   # Get shared memory pages and multiply with memory_page_size in order to convert the value into bytes.
            except FileNotFoundError:
                pid_list.remove(pid)
                continue
        if 8 in processes_treeview_columns_shown or 9 in processes_treeview_columns_shown or 10 in processes_treeview_columns_shown or 11 in processes_treeview_columns_shown:
            try:                                                                              # Root access is needed for reading "/proc/[PID]/io" file else it gives error. "try-except" is used in order to avoid this error if user has no root privileges.
                with open(f'/proc/{pid}/io') as reader:
                    proc_pid_io_lines = reader.read().split("\n")
                process_read_bytes = int(proc_pid_io_lines[4].split(":")[1])
                process_write_bytes = int(proc_pid_io_lines[5].split(":")[1])
            except (PermissionError, ProcessLookupError) as me:
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
            processes_data_row.append(int(proc_pid_status_output.split("\nGid:\t", 1)[1].split("\n", 1)[0].split("\t", 1)[0]))    # There are 4 values in the Gid line and first one (real GID) is get from this file.
        if 17 in processes_treeview_columns_shown:
            try:                                                                              # Executable path of some of the processes may not be get without root privileges or may not be get due to the reason of some of the processes may not have a exe file. "try-except" is used to be able to avoid errors due to these reasons.
                process_executable_path = os.path.realpath(f'/proc/{pid}/exe')
            except Exception:
                process_executable_path = "-"
            processes_data_row.append(process_executable_path)                                # Append process executable path
        if 18 in processes_treeview_columns_shown:
            try:
                with open(f'/proc/{pid}/cmdline') as reader:
                    process_commandline = ' '.join(reader.read().split("\x00"))
            except Exception:
                process_commandline = "-"
            processes_data_row.append(process_commandline)                                    # Append process command line
        # Append process data into a list (processes_data_rows)
        processes_data_rows.append(processes_data_row)
    global_process_cpu_times_prev = global_process_cpu_times                                  # For using values in the next loop
    disk_read_write_data_prev = disk_read_write_data

    processes_treeview_columns_shown = sorted(list(processes_treeview_columns_shown))         # Convert set to list (it was set before getting process information)

    # Add/Remove treeview columns appropriate for user preferences
    treeview2101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    if processes_treeview_columns_shown != processes_treeview_columns_shown_prev:             # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        for column in treeview2101.get_columns():                                             # Remove all columns in the treeview.
            treeview2101.remove_column(column)
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
                if cell_renderer_type == "CellRendererText":
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
            processes_treeview_column.set_min_width(50)                                       # Set minimum column widths as "50 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            processes_treeview_column.connect("clicked", on_column_title_clicked)             # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
            treeview2101.append_column(processes_treeview_column)                             # Append column into treeview

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
        treemodelsort2101 = Gtk.TreeModelSort(treemodelfilter2101)
        treeview2101.set_model(treemodelsort2101)
        pid_list_prev = []                                                                    # Redefine (clear) "pid_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
        global piter_list
        piter_list = []
    treeview2101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
    if processes_treeview_columns_shown_prev != processes_treeview_columns_shown or processes_data_column_order_prev != processes_data_column_order:
        processes_treeview_columns = treeview2101.get_columns()                               # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_column_titles = []
        for column in processes_treeview_columns:
            treeview_column_titles.append(column.get_title())
        processes_data_column_order_scratch = []
        for column_order in processes_data_column_order:
            if column_order != -1:
                processes_data_column_order_scratch.append(column_order)
        for order in reversed(sorted(processes_data_column_order_scratch)):                   # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
            if processes_data_column_order.index(order) in processes_treeview_columns_shown:
                column_number_to_move = processes_data_column_order.index(order)
                column_title_to_move = processes_data_list[column_number_to_move][1]
                column_to_move = processes_treeview_columns[treeview_column_titles.index(column_title_to_move)]
                treeview2101.move_column_after(column_to_move, None)                          # Column is moved at the beginning of the treeview if "None" is used.

    # Sort process rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
    if processes_treeview_columns_shown_prev != processes_treeview_columns_shown or processes_data_row_sorting_column_prev != processes_data_row_sorting_column or processes_data_row_sorting_order != processes_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
        processes_treeview_columns = treeview2101.get_columns()                               # Get shown columns on the treeview in order to use this data for reordering the columns.
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
            column_for_sorting.clicked()                                                      # For row sorting.
            if processes_data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                break

    # Set column widths if there are changes since last loop.
    if processes_treeview_columns_shown_prev != processes_treeview_columns_shown or processes_data_column_widths_prev != processes_data_column_widths:
        processes_treeview_columns = treeview2101.get_columns()
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
    treeview2101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    global process_search_text, filter_column
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
        on_searchentry2101_changed(searchentry2101)                                           # Update search results.
    if len(new_processes) > 0:
        for process in new_processes:
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
        on_searchentry2101_changed(searchentry2101)                                           # Update search results.
    treeview2101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    if pid_list_prev == []:                                                                   # Expand all treeview rows (if treeview items are in tree structured, not list) if this is the first loop of the Processes tab. It expands treeview rows (and children) in all loops if this control is not made. "First loop" control is made by checking if pid_list_prev is empty.
        treeview2101.expand_all()

    pid_list_prev = pid_list
    processes_data_rows_prev = processes_data_rows
    show_processes_as_tree_prev = show_processes_as_tree
    processes_treeview_columns_shown_prev = processes_treeview_columns_shown
    processes_data_row_sorting_column_prev = processes_data_row_sorting_column
    processes_data_row_sorting_order_prev = processes_data_row_sorting_order
    processes_data_column_order_prev = processes_data_column_order
    processes_data_column_widths_prev = processes_data_column_widths

    # Show number of processes on the searchentry as placeholder text
    searchentry2101.set_placeholder_text(_tr("Search...") + "                    " + "(" + _tr("Processes") + ": " + str(len(username_list)) + ")")

    # Show/Hide treeview expander arrows. If "child rows" are not used and there is no need for these expanders (they would be shown as empty spaces in this situation).
    if show_processes_as_tree == 1:
        treeview2101.set_show_expanders(True)
    if show_processes_as_tree == 0:
        treeview2101.set_show_expanders(False)

    # Show/Hide treeview tree lines
    if Config.show_tree_lines == 1:
        treeview2101.set_enable_tree_lines(True)
    if Config.show_tree_lines == 0:
        treeview2101.set_enable_tree_lines(False)


# ----------------------------------- Processes - Treeview Cell Functions (defines functions for treeview cell for setting data precisions and/or data units) -----------------------------------
def cell_data_function_cpu_usage_percent(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{tree_model.get(iter, data)[0]:.{processes_cpu_precision}f} %')

def cell_data_function_ram_swap(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_memory_data_unit, processes_memory_data_precision))

def cell_data_function_disk_usage(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_disk_data_unit, processes_disk_data_precision))

def cell_data_function_disk_speed(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{performance_data_unit_converter_func("speed", processes_disk_speed_bit, tree_model.get(iter, data)[0], processes_disk_data_unit, processes_disk_data_precision)}/s')


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
    processes_treeview_columns = treeview2101.get_columns()
    treeview_column_titles = []
    for column in processes_treeview_columns:
        treeview_column_titles.append(column.get_title())

    processes_data_column_order = [-1] * len(processes_data_list)
    processes_data_column_widths = [-1] * len(processes_data_list)

    processes_treeview_columns_last_index = len(processes_treeview_columns)-1

    for i, processes_data in enumerate(processes_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == processes_data[1]:
                column_index = treeview_column_titles.index(processes_data[1])
                processes_data_column_order[i] = column_index
                if j != processes_treeview_columns_last_index:
                    processes_data_column_widths[i] = processes_treeview_columns[column_index].get_width()

    Config.processes_data_column_order = list(processes_data_column_order)
    Config.processes_data_column_widths = list(processes_data_column_widths)
    Config.config_save_func()


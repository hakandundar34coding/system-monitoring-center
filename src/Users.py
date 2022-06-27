#!/usr/bin/env python3

# ----------------------------------- Users - Import Function -----------------------------------
def users_import_func():

    global Gtk, Gdk, GLib, GObject, GdkPixbuf, os, datetime, time

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GLib', '2.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('GObject', '2.0')
    gi.require_version('GdkPixbuf', '2.0')
    from gi.repository import Gtk, Gdk, GLib, GObject, GdkPixbuf
    import os
    from datetime import datetime
    import time


    global Config
    from Config import Config


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Users - Users GUI Function -----------------------------------
def users_gui_func():

    global grid3101, treeview3101, searchentry3101, button3101

    # Users tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersTab.ui")

    # Users tab GUI objects - get
    grid3101 = builder.get_object('grid3101')
    treeview3101 = builder.get_object('treeview3101')
    searchentry3101 = builder.get_object('searchentry3101')
    button3101 = builder.get_object('button3101')

    # Users tab GUI functions - connect
    treeview3101.connect("button-press-event", on_treeview3101_button_press_event)
    treeview3101.connect("button-release-event", on_treeview3101_button_release_event)
    searchentry3101.connect("changed", on_searchentry3101_changed)
    button3101.connect("clicked", on_button3101_clicked)

    # Users Tab - Treeview Properties
    treeview3101.set_activate_on_single_click(True)
    treeview3101.set_fixed_height_mode(True)
    treeview3101.set_headers_clickable(True)
    treeview3101.set_show_expanders(False)
    treeview3101.set_enable_search(True)
    treeview3101.set_search_column(2)
    treeview3101.set_tooltip_column(2)

    global initial_already_run
    initial_already_run = 0


# --------------------------------- Called for running code/functions when button is pressed on the treeview ---------------------------------
def on_treeview3101_button_press_event(widget, event):

    # Get right/double clicked row data
    try:                                                                                  # "try-except" is used in order to prevent errors when right clicked on an empty area on the treeview.
        path, _, _, _ = treeview3101.get_path_at_pos(int(event.x), int(event.y))
    except TypeError:
        return
    model = treeview3101.get_model()
    treeiter = model.get_iter(path)

    # Get right/double clicked user UID and user name
    if treeiter == None:
        return
    global selected_user_uid, selected_username
    try:
        selected_user_uid = uid_username_list[users_data_rows.index(model[treeiter][:])][0]
        selected_username = uid_username_list[users_data_rows.index(model[treeiter][:])][1]
    except ValueError:
        return

    # Open right click menu if right clicked on a row
    if event.button == 3:
        from UsersMenuRightClick import UsersMenuRightClick
        UsersMenuRightClick.menu3101m.popup_at_pointer()

    # Open details window if double clicked on a row
    if event.type == Gdk.EventType._2BUTTON_PRESS:
        from UsersDetails import UsersDetails
        UsersDetails.window3101w.show()


# --------------------------------- Called for running code/functions when button is released on the treeview ---------------------------------
def on_treeview3101_button_release_event(widget, event):

    # Check if left mouse button is used
    if event.button == 1:
        users_treeview_column_order_width_row_sorting_func()


# --------------------------------- Called for searching items when searchentry text is changed ---------------------------------
def on_searchentry3101_changed(widget):

    global filter_column
    user_search_text = searchentry3101.get_text().lower()
    # Set visible/hidden users
    for piter in piter_list:
        treestore3101.set_value(piter, 0, False)
        user_data_text_in_model = treestore3101.get_value(piter, filter_column)
        if user_search_text in str(user_data_text_in_model).lower():
            treestore3101.set_value(piter, 0, True)


# --------------------------------- Called for showing Users tab customization menu when button is clicked ---------------------------------
def on_button3101_clicked(widget):

    from UsersMenuCustomizations import UsersMenuCustomizations
    UsersMenuCustomizations.popover3101p.set_relative_to(button3101)
    UsersMenuCustomizations.popover3101p.set_position(1)
    UsersMenuCustomizations.popover3101p.popup()


# ----------------------------------- Users - Initial Function -----------------------------------
def users_initial_func():

    global users_data_list
    users_data_list = [
                      [0, _tr('User'), 3, 2, 3, [bool, GdkPixbuf.Pixbuf, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'pixbuf', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
                      [1, _tr('Full Name'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                      [2, _tr('Logged In'), 1, 1, 1, [bool], ['CellRendererToggle'], ['active'], [0], [0.5], [False], ['no_cell_function']],
                      [3, _tr('UID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                      [4, _tr('GID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                      [5, _tr('Processes'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                      [6, _tr('Home Directory'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                      [7, _tr('Group'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                      [8, _tr('Terminal'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                      [9, _tr('Start Time'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_started]],
                      [10, _tr('CPU'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_cpu_usage_percent]],
                      ]

    global users_data_rows_prev, users_treeview_columns_shown_prev, users_data_row_sorting_column_prev, users_data_row_sorting_order_prev, users_data_column_order_prev, users_data_column_widths_prev
    global pid_list_prev, global_process_cpu_times_prev, uid_username_list_prev
    users_data_rows_prev = []
    pid_list_prev = []
    global_process_cpu_times_prev = []
    uid_username_list_prev = []                                                               # For tracking new/removed (from treeview) user data rows
    users_treeview_columns_shown_prev = []
    users_data_row_sorting_column_prev = ""
    users_data_row_sorting_order_prev = ""
    users_data_column_order_prev = []
    users_data_column_widths_prev = []


    global number_of_clock_ticks, system_boot_time, user_image_unset_pixbuf

    number_of_clock_ticks = os.sysconf("SC_CLK_TCK")                                          # For many systems CPU ticks 100 times in a second. Wall clock time could be get if CPU times are multiplied with this value or vice versa.

    # Get system boot time which will be used for obtaining user process start time
    with open("/proc/stat") as reader:
        stat_lines = reader.read().split("\n")
    for line in stat_lines:
        if "btime " in line:
            system_boot_time = int(line.split()[1].strip())

    try:
        user_image_unset_pixbuf = Gtk.IconTheme.get_default().load_icon("system-monitoring-center-user-symbolic", 16, 0)
    # Prevent "gi.repository.GLib.Error" if image is not found (occurs if the application is run from source code without installation). It gives this error because this image is set in the code.
    except:
        user_image_unset_pixbuf = Gtk.IconTheme.get_default().load_icon("image-missing", 16, 0)

    global filter_column
    filter_column = users_data_list[0][2] - 1                                                 # Search filter is "Process Name". "-1" is used because "processes_data_list" has internal column count and it has to be converted to Python index. For example, if there are 3 internal columns but index is 2 for the last internal column number for the relevant treeview column.

    global initial_already_run
    initial_already_run = 1


# ----------------------------------- Users - Get User Data Function (gets user data, adds into treeview and updates it) -----------------------------------
def users_loop_func():

    update_interval = Config.update_interval

    # Get GUI obejcts one time per floop instead of getting them multiple times
    global treeview3101

    # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
    global users_cpu_precision
    users_cpu_precision = Config.users_cpu_precision

    # Define global variables and get treeview columns, sort column/order, column widths, etc.
    global users_treeview_columns_shown
    global users_treeview_columns_shown_prev, users_data_row_sorting_column_prev, users_data_row_sorting_order_prev, users_data_column_order_prev, users_data_column_widths_prev
    users_treeview_columns_shown = Config.users_treeview_columns_shown
    users_data_row_sorting_column = Config.users_data_row_sorting_column
    users_data_row_sorting_order = Config.users_data_row_sorting_order
    users_data_column_order = Config.users_data_column_order
    users_data_column_widths = Config.users_data_column_widths

    # Define global variables and empty lists for the current loop
    global users_data_rows, users_data_rows_prev, global_process_cpu_times_prev, pid_list, pid_list_prev, uid_username_list_prev, uid_username_list, user_logged_in_list
    users_data_rows = []
    global_process_cpu_times = []
    uid_username_list = []                                                                    # For tracking new/removed user data rows. User UID and username information is appended per user. Because tracking only user UID and username may cause confusions. User UID may be given another user after a time if a user is deleted.
    user_logged_in_list = []

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
    # Get process names (will be used for checking "systemd" named processes to be able to get user process, user first log in time since system boot), usernames (will be used for determining number of processes of the users), CPU% usage of all processes
    all_process_names = []
    all_process_user_ids = []
    all_process_cpu_usages = []
    for pid in pid_list[:]:                                                                   # "[:]" is used for iterating over copy of the list because element are removed during iteration. Otherwise incorrect operations (incorrect element removal) are performed on the list.
        try:
            with open("/proc/" + pid + "/status") as reader:
                proc_pid_status_lines = reader.read().split("\n")
            if 9 in users_treeview_columns_shown or 10 in users_treeview_columns_shown:
                with open("/proc/" + pid + "/stat") as reader:
                    global_cpu_time_all = time.time() * number_of_clock_ticks                 # global_cpu_time_all value is get just before "/proc/[PID]/stat file is read in order to measure global an process specific CPU times at the same time (nearly) for ensuring accurate process CPU usage percent.
                    proc_pid_stat_lines = reader.read().split()
        except (FileNotFoundError, ProcessLookupError) as me:                                 # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
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
        if 10 in users_treeview_columns_shown:
            process_cpu_time = int(proc_pid_stat_lines[-39]) + int(proc_pid_stat_lines[-38])  # Get process cpu time in user mode (utime + stime)
            global_process_cpu_times.append((global_cpu_time_all, process_cpu_time))          # While appending multiple elements into a list "append((value1, value2))" is faster than "append([value1, value2])".
            try:                                                                              # It gives various errors (ValueError, IndexError, UnboundLocalError) if a new process is started, a new column is shown on the treeview, etc because previous CPU time values are not present in these situations. Following CPU time values are use in these situations.
                global_cpu_time_all_prev, process_cpu_time_prev = global_process_cpu_times_prev[pid_list_prev.index(pid)]
            except (ValueError, IndexError, UnboundLocalError) as me:
                process_cpu_time_prev = process_cpu_time                                      # There is no "process_cpu_time_prev" value and get it from "process_cpu_time"  if this is first loop of the process
                global_cpu_time_all_prev = global_process_cpu_times[-1][0] - 1                # Subtract "1" CPU time (a negligible value) if this is first loop of the process
            process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
            global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
            all_process_cpu_usages.append(process_cpu_time_difference / global_cpu_time_difference * 100 / number_of_logical_cores)

    # Get and append data per user
    for line in etc_passwd_lines:
        line_split = line.split(":")
        username = line_split[0]
        user_uid = line_split[2]
        user_gid = line_split[3]
        user_uid_int = int(user_uid)                                                          # For lower CPU usage because it is repeated two times in the following line
        if user_uid_int >= 1000 and user_uid_int != 65534:                                    # Human users have UID bigger than 999 (1000 =< UID) and lower than 65534. 
            uid_username_list.append([int(user_uid), username])                               # "user_uid" have to be appended as integer because sorting list of multiple elemented sub-list operation will be performed. "sorted(a_list, key=int)" could not be used in this situation.
            # Get user PID and logged in data (PID data is required for obtaining user logged in data. User PID and user logged in data will be appended later)
            user_process_pid = 0                                                              # Initial value of "user_PID" value. This value will be left as "0" if user is not logged in.
            for i, process_name in enumerate(all_process_names):
                if process_name == "systemd":                                                 # "systemd" process per user is checked here (by checking real UID of the process). It is not system-wide "systemd" process which is owned by "root" user. User session process is specific to desktop session (for example xfce4-session for XFCE desktop environment) and checking "systemd" process of the user is easier and gives very similar start time.
                    real_user_id = all_process_user_ids[i]
                    if real_user_id == user_uid:
                        user_process_pid = pid_list[i]
                        break                                                                 # Exit this loop if real_user_id" is found in order to obtain faster code execution.
            if user_process_pid != 0:                                                         # User is not logged in if "user_process_pid" is not get from "systemd" process of the user.
                user_logged_in = True
            if user_process_pid == 0:                                                         # User is logged in if "user_process_pid" is get from "systemd" process of the user.
                user_logged_in = False
            user_logged_in_list.append(user_logged_in)
            # Append row visibility data, username (username has been get previously) and get user account image
            user_image_path = "/var/lib/AccountsService/icons/" + username
            if os.path.isfile(user_image_path) == True:
                user_account_image = GdkPixbuf.Pixbuf.new_from_file_at_size(user_image_path, 16, 16)
            if os.path.isfile(user_image_path) == False:
                user_account_image = user_image_unset_pixbuf
            users_data_row = [True, user_account_image, username]                             # User data row visibility data (True/False) is always appended into the list. True is an initial value and it is modified later.
            # Get user full name
            if 1 in users_treeview_columns_shown:
                user_full_name = line_split[4]
                users_data_row.append(user_full_name)
            # Get user logged in data (User logged in data has been get previously)
            if 2 in users_treeview_columns_shown:
                users_data_row.append(user_logged_in)
            # Get user UID (UID value has been get previously)
            if 3 in users_treeview_columns_shown:
                users_data_row.append(int(user_uid))
            # Get user GID
            if 4 in users_treeview_columns_shown:
                users_data_row.append(int(user_gid))
            # Get user process count
            if 5 in users_treeview_columns_shown:
                user_process_count = all_process_user_ids.count(user_uid)
                users_data_row.append(user_process_count)
            # Get user home directory
            if 6 in users_treeview_columns_shown:
                user_home_dir = line_split[5]
                users_data_row.append(user_home_dir)
            # Get user group
            if 7 in users_treeview_columns_shown:
                user_group_name = user_group_names[user_group_ids.index(user_gid)]
                users_data_row.append(user_group_name)
            # Get user terminal
            if 8 in users_treeview_columns_shown:
                user_terminal = line_split[6]
                users_data_row.append(user_terminal)
            # Get user process start time
            if 9 in users_treeview_columns_shown:
                if user_process_pid == 0:
                    user_process_start_time = 0                                               # User process start time is "0" if it is not alive (if user is not logged in)
                if user_process_pid != 0:                                                     # User process start time is get if it is alive (if user is logged in)
                    try:
                        with open("/proc/" + str(user_process_pid) + "/stat") as reader:
                            proc_pid_stat_lines = int(reader.read().split()[-31])             # Elapsed time between system boot and process start time (measured in clock ticks and need to be divided by sysconf(_SC_CLK_TCK) for converting into wall clock time)
                        user_process_start_time = (proc_pid_stat_lines / number_of_clock_ticks) + system_boot_time
                    except Exception:
                        user_process_start_time = 0
                users_data_row.append(user_process_start_time)
            # Get user processes CPU usage percentages
            if 10 in users_treeview_columns_shown:
                user_users_cpu_percent = 0
                for pid in pid_list:
                    if all_process_user_ids[pid_list.index(pid)] == user_uid:
                        user_users_cpu_percent = user_users_cpu_percent + all_process_cpu_usages[pid_list.index(pid)]
                users_data_row.append(user_users_cpu_percent)
            # Append all data of the users into a list which will be appended into a treestore for showing the data on a treeview.
            users_data_rows.append(users_data_row)
    pid_list_prev = pid_list                                                                  # For using values in the next loop
    global_process_cpu_times_prev = global_process_cpu_times                                  # For using values in the next loop

    # Add/Remove treeview columns appropriate for user preferences
    treeview3101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    if users_treeview_columns_shown != users_treeview_columns_shown_prev:                     # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        for column in treeview3101.get_columns():                                             # Remove all columns in the treeview.
            treeview3101.remove_column(column)
        for i, column in enumerate(users_treeview_columns_shown):
            if users_data_list[column][0] in users_treeview_columns_shown:
                cumulative_sort_column_id = cumulative_sort_column_id + users_data_list[column][2]
            users_treeview_column = Gtk.TreeViewColumn(users_data_list[column][1])            # Define column (also column title is defined)
            for i, cell_renderer_type in enumerate(users_data_list[column][6]):
                cumulative_internal_data_id = cumulative_internal_data_id + 1
                if cell_renderer_type == "internal_column":                                   # Continue to next loop to avoid generating a cell renderer for internal column (internal columns are not shon on the treeview and they do not have cell renderers).
                    continue
                if cell_renderer_type == "CellRendererPixbuf":                                # Define cell renderer
                    cell_renderer = Gtk.CellRendererPixbuf()
                if cell_renderer_type == "CellRendererText":                                  # Define cell renderer
                    cell_renderer = Gtk.CellRendererText()
                if cell_renderer_type == "CellRendererToggle":                                # Define cell renderer
                    cell_renderer = Gtk.CellRendererToggle()
                cell_renderer.set_alignment(users_data_list[column][9][i], 0.5)               # Vertical alignment is set 0.5 in order to leave it as unchanged.
                users_treeview_column.pack_start(cell_renderer, users_data_list[column][10][i])    # Set if column will allocate unused space
                users_treeview_column.add_attribute(cell_renderer, users_data_list[column][7][i], cumulative_internal_data_id)
                if users_data_list[column][11][i] != "no_cell_function":
                    users_treeview_column.set_cell_data_func(cell_renderer, users_data_list[column][11][i], func_data=cumulative_internal_data_id)    # Define cell function which sets cell data precision and/or data unit
            users_treeview_column.set_sizing(2)                                               # Set column sizing (2 = auto sizing which is required for "treeview3101.set_fixed_height_mode(True)" command that is used for lower treeview CPU consumption because row heights are not calculated for every row).
            users_treeview_column.set_sort_column_id(cumulative_sort_column_id)               # Be careful with lists contain same element more than one.
            users_treeview_column.set_resizable(True)                                         # Set columns resizable by the user when column title button edge handles are dragged.
            users_treeview_column.set_reorderable(True)                                       # Set columns reorderable by the user when column title buttons are dragged.
            users_treeview_column.set_min_width(50)                                           # Set minimum column widths as "50 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            users_treeview_column.connect("clicked", on_column_title_clicked)                 # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
            treeview3101.append_column(users_treeview_column)                                 # Append column into treeview

        # Get column data types for appending users data into treestore
        users_data_column_types = []
        for column in sorted(users_treeview_columns_shown):
            internal_column_count = len(users_data_list[column][5])
            for internal_column_number in range(internal_column_count):
                users_data_column_types.append(users_data_list[column][5][internal_column_number])    # Get column types (int, bool, float, str, etc.)

        # Define a treestore (for storing treeview data in it), a treemodelfilter (for search filtering), treemodelsort (for row sorting when column title buttons are clicked)
        global treestore3101                                                                  # Define as global variable because treestore is generated in statement and will not be defined in every loop and it will be used outside the statement.
        treestore3101 = Gtk.TreeStore()
        treestore3101.set_column_types(users_data_column_types)                               # Set column types of the columns which will be appended into treestore
        treemodelfilter3101 = treestore3101.filter_new()
        treemodelfilter3101.set_visible_column(0)                                             # Column "0" of the treestore will be used for column visibility information (True or False)
        treemodelsort3101 = Gtk.TreeModelSort(treemodelfilter3101)
        treeview3101.set_model(treemodelsort3101)
        pid_list_prev = []                                                                    # Redefine (clear) "pid_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
        uid_username_list_prev = []                                                           # Redefine (clear) "uid_username_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
        global piter_list
        piter_list = []
    treeview3101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
    if users_treeview_columns_shown_prev != users_treeview_columns_shown or users_data_column_order_prev != users_data_column_order:
        users_treeview_columns = treeview3101.get_columns()                                   # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_column_titles = []
        for column in users_treeview_columns:
            treeview_column_titles.append(column.get_title())
        users_data_column_order_scratch = []
        for column_order in users_data_column_order:
            if column_order != -1:
                users_data_column_order_scratch.append(column_order)
        for order in reversed(sorted(users_data_column_order_scratch)):                       # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
            if users_data_column_order.index(order) in users_treeview_columns_shown:
                column_number_to_move = users_data_column_order.index(order)
                column_title_to_move = users_data_list[column_number_to_move][1]
                column_to_move = users_treeview_columns[treeview_column_titles.index(column_title_to_move)]
                treeview3101.move_column_after(column_to_move, None)                          # Column is moved at the beginning of the treeview if "None" is used.

    # Sort user rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
    if users_treeview_columns_shown_prev != users_treeview_columns_shown or users_data_row_sorting_column_prev != users_data_row_sorting_column or users_data_row_sorting_order != users_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
        users_treeview_columns = treeview3101.get_columns()                                   # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_column_titles = []
        for column in users_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i in range(10):
            if users_data_row_sorting_column in users_treeview_columns_shown:
                for data in users_data_list:
                    if data[0] == users_data_row_sorting_column:
                        column_title_for_sorting = data[1]
            if users_data_row_sorting_column not in users_treeview_columns_shown:
                column_title_for_sorting = users_data_list[0][1]
            column_for_sorting = users_treeview_columns[treeview_column_titles.index(column_title_for_sorting)]
            column_for_sorting.clicked()                                                      # For row sorting.
            if users_data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                break

    # Set column widths if there are changes since last loop.
    if users_treeview_columns_shown_prev != users_treeview_columns_shown or users_data_column_widths_prev != users_data_column_widths:
        users_treeview_columns = treeview3101.get_columns()
        treeview_column_titles = []
        for column in users_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i, users_data in enumerate(users_data_list):
            for j, column_title in enumerate(treeview_column_titles):
                if column_title == users_data[1]:
                   column_width = users_data_column_widths[i]
                   users_treeview_columns[j].set_fixed_width(column_width)                    # Set column width in pixels. Fixed width is unset if value is "-1".

    # Get new/deleted(ended) users for updating treestore/treeview
    uid_username_list_prev_set = set(tuple(i) for i in uid_username_list_prev)                # "set(a_list)" could not be used here because this list is a list of sub-lists. 
    uid_username_list_set = set(tuple(i) for i in uid_username_list)                          # "set(a_list)" could not be used here because this list is a list of sub-lists. 
    deleted_users = sorted(list(uid_username_list_prev_set - uid_username_list_set))          # For list of multiple elemented sub-lists, sorting is performed by using first elements of the sub-lists (For example: output of an sorted list = [[1, "b"], [2, "a"], [3, "c"]]).
    new_users = sorted(list(uid_username_list_set - uid_username_list_prev_set))
    existing_users = sorted(list(uid_username_list_set.intersection(uid_username_list_prev_set)))
    updated_existing_user_index = [[uid_username_list.index(list(i)), uid_username_list_prev.index(list(i))] for i in existing_users]    # "c = set(a).intersection(b)" is about 19% faster than "c = set(a).intersection(set(b))"
    try:
        users_data_rows_row_length = len(users_data_rows[0])
    # Prevent errors if there is no user account on the system. An user account may not be found on an OS if the OS is run from the installation disk without installation.
    except IndexError:
        return
    # Append/Remove/Update users data into treestore
    treeview3101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    global user_search_text, filter_column
    if len(piter_list) > 0:
        for i, j in updated_existing_user_index:
            if users_data_rows[i] != users_data_rows_prev[j]:
                for k in range(1, users_data_rows_row_length):                                # Start from "1" in order to set first element (treeview row visibility data) as "True" in every loop.
                    if users_data_rows_prev[j][k] != users_data_rows[i][k]:
                        treestore3101.set_value(piter_list[j], k, users_data_rows[i][k])
    if len(deleted_users) > 0:
        for user in reversed(sorted(list(deleted_users))):
            treestore3101.remove(piter_list[uid_username_list_prev.index(list(user))])        # ".index(list(user))" have to used with "list()" because it was converted into "set". This behavior is valid for list of multiple elemented sub-lists.
            piter_list.remove(piter_list[uid_username_list_prev.index(list(user))])
        on_searchentry3101_changed(searchentry3101)                                           # Update search results.
    if len(new_users) > 0:
        for i, user in enumerate(new_users):
            piter_list.append(treestore3101.append(None, users_data_rows[uid_username_list.index(list(user))]))
        on_searchentry3101_changed(searchentry3101)                                           # Update search results.
    treeview3101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    uid_username_list_prev = uid_username_list
    users_data_rows_prev = users_data_rows
    users_treeview_columns_shown_prev = users_treeview_columns_shown
    users_data_row_sorting_column_prev = users_data_row_sorting_column
    users_data_row_sorting_order_prev = users_data_row_sorting_order
    users_data_column_order_prev = users_data_column_order
    users_data_column_widths_prev = users_data_column_widths

    # Show number of users on the searchentry as placeholder text
    searchentry3101.set_placeholder_text(_tr("Search...") + "                    " + "(" + _tr("Users") + ": " + str(len(user_logged_in_list)) + ")")


# ----------------------------------- Users - Treeview Cell Functions (defines functions for treeview cell for setting data precisions and/or data units) -----------------------------------
def cell_data_function_cpu_usage_percent(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{tree_model.get(iter, data)[0]:.{users_cpu_precision}f} %')

def cell_data_function_started(tree_column, cell, tree_model, iter, data):
    cell_data = tree_model.get(iter, data)[0]
    if cell_data != 0:
        cell.set_property('text', datetime.fromtimestamp(tree_model.get(iter, data)[0]).strftime("%H:%M:%S %d.%m.%Y"))
    if cell_data == 0:
        cell.set_property('text', "-")


# ----------------------------------- Users - Column Title Clicked Function -----------------------------------
def on_column_title_clicked(widget):

    users_data_row_sorting_column_title = widget.get_title()                                  # Get column title which will be used for getting column number
    for data in users_data_list:
        if data[1] == users_data_row_sorting_column_title:
            Config.users_data_row_sorting_column = data[0]                                    # Get column number
    Config.users_data_row_sorting_order = int(widget.get_sort_order())                        # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    Config.config_save_func()


# ----------------------------------- Users - Treeview Column Order-Width Row Sorting Function -----------------------------------
def users_treeview_column_order_width_row_sorting_func():

    users_treeview_columns = treeview3101.get_columns()
    treeview_column_titles = []
    for column in users_treeview_columns:
        treeview_column_titles.append(column.get_title())

    users_data_column_order = [-1] * len(users_data_list)
    users_data_column_widths = [-1] * len(users_data_list)

    users_treeview_columns_last_index = len(users_treeview_columns)-1

    for i, users_data in enumerate(users_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == users_data[1]:
                column_index = treeview_column_titles.index(users_data[1])
                users_data_column_order[i] = column_index
                if j != users_treeview_columns_last_index:
                    users_data_column_widths[i] = users_treeview_columns[column_index].get_width()

    Config.users_data_column_order = list(users_data_column_order)
    Config.users_data_column_widths = list(users_data_column_widths)
    Config.config_save_func()


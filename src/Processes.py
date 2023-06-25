#!/usr/bin/env python3

# ----------------------------------- Processes - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def processes_import_func():

    global Gtk, Gdk, GLib, GObject, os, time, subprocess, datetime

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GLib', '2.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('GObject', '2.0')
    from gi.repository import Gtk, Gdk, GLib, GObject
    import os
    import time
    import subprocess
    from datetime import datetime


    global Config, Performance
    from Config import Config
    from Performance import Performance

    # Import gettext module for defining translation texts which will be recognized by gettext application. These lines of code are enough to define this variable if another values are defined in another module (Main GUI module) before importing this module.
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    from locale import gettext as _tr


# ----------------------------------- Processes - Processes GUI Function (the code of this module in order to avoid running them during module import and defines "Processes" tab GUI objects and functions/signals) -----------------------------------
def processes_gui_func():

    # Processes tab GUI objects
    global grid2101, treeview2101, searchentry2101

    # Processes tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesTab.ui")

    # Processes tab GUI objects - get
    grid2101 = builder.get_object('grid2101')
    treeview2101 = builder.get_object('treeview2101')
    searchentry2101 = builder.get_object('searchentry2101')

    # Processes tab GUI functions - connect
    treeview2101.connect("columns-changed", on_columns_changed, treeview2101)
    treeview2101.connect("button-press-event", on_treeview2101_button_press_event)
    treeview2101.connect("button-release-event", on_treeview2101_button_release_event)
    treeview2101.connect("key-press-event", on_treeview2101_key_press_event)
    searchentry2101.connect("changed", on_searchentry2101_changed)

    # Processes Tab - Treeview Properties
    treeview2101.set_activate_on_single_click(True)                                           # This command used for activating rows and column header buttons on single click. Column headers have to clicked twice (or clicked() command have to be used twice) for the first sorting operation if this is not used.
    treeview2101.set_fixed_height_mode(True)                                                  # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview2101.set_headers_clickable(True)
    treeview2101.set_enable_search(True)                                                      # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview2101.set_search_column(2)                                                         # This command used for searching by using entry.
    treeview2101.set_tooltip_column(2)

    if Config.show_processes_as_tree == 1:
        Config.temporary_show_processes_as_tree = 1
    elif Config.show_processes_as_tree == 0:
        Config.temporary_show_processes_as_tree = 0

    # Add PID column (1) to shown columns in order to prevent errors during process search if PID column is hidden in
    # previous versions (<=v1.43.4) of the application.
    treeview_columns_shown = Config.processes_treeview_columns_shown
    if 1 not in treeview_columns_shown:
        treeview_columns_shown.append(1)
    Config.processes_treeview_columns_shown = sorted(treeview_columns_shown)

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
        selected_process_pid = model[treeiter][:][4]
        #selected_process_pid = pid_list[processes_data_rows.index(model[treeiter][:])]
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
        """from ProcessesDetails import ProcessesDetails
        ProcessesDetails.window2101w.show()"""

        import ProcessesDetails
        ProcessesDetails.processes_details_show_process_details()


# --------------------------------- Called for running code/functions when button is released on the treeview ---------------------------------
def on_treeview2101_button_release_event(widget, event):

    pass


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
        selected_process_pid = model[treeiter][:][4]
        #selected_process_pid = pid_list[processes_data_rows.index(model[treeiter][:])]
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

    # Check if Enter key is pressed.
    if event.keyval == Gdk.KEY_Return or event.keyval == Gdk.KEY_KP_Enter:
        ProcessesMenuRightClick.on_menuitem2106m_activate(ProcessesMenuRightClick.menuitem2106m)
        return


# --------------------------------- Called for searching items when searchentry text is changed ---------------------------------
def on_searchentry2101_changed(widget):

    global filter_column
    process_search_text = searchentry2101.get_text().lower()

    if process_search_text != "":
        if Config.show_processes_as_tree == 1 and Config.temporary_show_processes_as_tree == 1:
            Config.temporary_show_processes_as_tree = 0
            processes_initial_func()
            processes_loop_func()
    elif process_search_text == "":
        if Config.show_processes_as_tree == 1 and Config.temporary_show_processes_as_tree == 0:
            Config.temporary_show_processes_as_tree = 1
            processes_initial_func()
            processes_loop_func()

    # Set visible/hidden processes
    for piter in piter_list:
        process_data_text_in_model = treestore.get_value(piter, filter_column)
        if process_search_text in str(process_data_text_in_model).lower():
            treestore.set_value(piter, 0, True)
        else:
            treestore.set_value(piter, 0, False)


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
                          [1, _tr('PID'), 2, 1, 2, [str, int], ['internal_column', 'CellRendererText'], ['no_cell_attribute', 'text'], [0, 1], ['no_cell_alignment', 1.0], [False, False], ['no_cell_function', 'no_cell_function']],
                          [2, _tr('User'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                          [3, _tr('Status'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                          [4, _tr('CPU'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_cpu_usage_percent]],
                          [5, _tr('Memory (RSS)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_memory_rss]],
                          [6, _tr('Memory (VMS)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_memory_vms]],
                          [7, _tr('Memory (Shared)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_memory_shared]],
                          [8, _tr('Read Data'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_read_data]],
                          [9, _tr('Written Data'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_write_data]],
                          [10, _tr('Read Speed'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_read_speed]],
                          [11, _tr('Write Speed'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_write_speed]],
                          [12, _tr('Priority'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [13, _tr('Threads'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [14, _tr('PPID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [15, _tr('UID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [16, _tr('GID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                          [17, _tr('Start Time'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [0.0], [False], [cell_data_function_start_time]],
                          [18, _tr('Command Line'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']]
                          ]

    # Define data unit conversion function objects in for lower CPU usage.
    global performance_define_data_unit_converter_variables_func, performance_define_data_unit_converter_variables_func, performance_data_unit_converter_func
    performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
    performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

    # Define data unit conversion variables before they are used.
    performance_define_data_unit_converter_variables_func()


    global processes_data_rows_prev, pid_list_prev, piter_list, global_process_cpu_times_prev, disk_read_write_data_prev, show_processes_as_tree_prev, temporary_show_processes_as_tree_prev, processes_treeview_columns_shown_prev, processes_data_row_sorting_column_prev, processes_data_row_sorting_order_prev, processes_data_column_order_prev, processes_data_column_widths_prev, rows_data_dict_prev
    processes_data_rows_prev = []
    pid_list_prev = []
    piter_list = []
    show_processes_as_tree_prev = Config.show_processes_as_tree
    global_process_cpu_times_prev = []
    disk_read_write_data_prev = []
    show_processes_as_tree_prev = Config.show_processes_as_tree
    temporary_show_processes_as_tree_prev = Config.temporary_show_processes_as_tree
    processes_treeview_columns_shown_prev = []
    processes_data_row_sorting_column_prev = ""
    processes_data_row_sorting_order_prev = ""
    processes_data_column_order_prev = []
    processes_data_column_widths_prev = []
    rows_data_dict_prev = {}

    global process_status_dict, number_of_clock_ticks, memory_page_size, application_image_dict, system_boot_time, username_uid_dict
    # For more information, see: "https://man7.org/linux/man-pages/man5/proc.5.html".
    process_status_dict = {"R": "Running", "S": "Sleeping", "D": "Waiting", "I": "Idle",
                           "Z": "Zombie", "T": "Stopped", "t": "Tracing Stop", "X": "Dead"}
    number_of_clock_ticks = os.sysconf("SC_CLK_TCK")
    memory_page_size = os.sysconf("SC_PAGE_SIZE")
    system_boot_time = get_system_boot_time()
    username_uid_dict = get_username_uid_dict()
    application_image_dict = get_application_name_image_dict()

    process_status_list = [_tr("Running"), _tr("Sleeping"), _tr("Waiting"), _tr("Idle"), _tr("Zombie"), _tr("Stopped")]

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
    global processes_treeview_columns_shown, show_processes_of_all_users, show_processes_as_tree, show_processes_as_tree_prev
    global processes_treeview_columns_shown_prev, processes_data_row_sorting_column_prev, processes_data_row_sorting_order_prev, processes_data_column_order_prev, processes_data_column_widths_prev
    processes_treeview_columns_shown = Config.processes_treeview_columns_shown
    processes_data_row_sorting_column = Config.processes_data_row_sorting_column
    processes_data_row_sorting_order = Config.processes_data_row_sorting_order
    processes_data_column_order = Config.processes_data_column_order
    processes_data_column_widths = Config.processes_data_column_widths
    show_processes_of_all_users = Config.show_processes_of_all_users
    show_processes_as_tree = Config.show_processes_as_tree

    global processes_data_rows_prev, pid_list_prev

    # For obtaining lower CPU usage
    processes_treeview_columns_shown = set(processes_treeview_columns_shown)

    # Define lists for appending some performance data for calculating max values to determine cell background color.
    cpu_usage_list = []
    memory_rss_list = []
    memory_vms_list = []
    memory_shared_list = []
    disk_read_data_list = []
    disk_write_data_list = []
    disk_read_speed_list = []
    disk_write_speed_list = []

    # Get process information
    global rows_data_dict_prev, system_boot_time, username_uid_dict
    global cmdline_list, application_image_dict, pid_list
    process_list = []
    if show_processes_of_all_users == 1:
        processes_of_user = "all"
    else:
        processes_of_user = "current"
    cpu_usage_divide_by_cores = "yes"
    detail_level = "medium"
    rows_data_dict = get_processes_information(process_list, processes_of_user, cpu_usage_divide_by_cores, detail_level, rows_data_dict_prev, system_boot_time, username_uid_dict)
    rows_data_dict_prev = dict(rows_data_dict)
    pid_list = rows_data_dict["pid_list"]
    ppid_list = rows_data_dict["ppid_list"]
    username_list = rows_data_dict["username_list"]
    cmdline_list = rows_data_dict["cmdline_list"]

    # Get and append process data
    global processes_data_rows
    processes_data_rows = []
    for pid in pid_list:
        row_data_dict = rows_data_dict[pid]
        process_name = row_data_dict["name"]
        ppid = row_data_dict["ppid"]
        # Get process image
        if ppid == 2 or pid == 2:
            process_image = "system-monitoring-center-process-symbolic"
        else:
            process_image = "application-x-executable"
            if process_name in application_image_dict:
                process_image = application_image_dict[process_name]
        process_commandline = row_data_dict["command_line"]
        tab_data_row = [True, process_image, process_name, process_commandline]
        if 1 in processes_treeview_columns_shown:
            tab_data_row.append(pid)
        if 2 in processes_treeview_columns_shown:
            tab_data_row.append(row_data_dict["username"])
        if 3 in processes_treeview_columns_shown:
            tab_data_row.append(_tr(row_data_dict["status"]))
        if 4 in processes_treeview_columns_shown:
            cpu_usage = row_data_dict["cpu_usage"]
            cpu_usage_list.append(cpu_usage)
            tab_data_row.append(cpu_usage)
        if 5 in processes_treeview_columns_shown:
            memory_rss = row_data_dict["memory_rss"]
            memory_rss_list.append(memory_rss)
            tab_data_row.append(memory_rss)
        if 6 in processes_treeview_columns_shown:
            memory_vms = row_data_dict["memory_vms"]
            tab_data_row.append(memory_vms)
            memory_vms_list.append(memory_vms)
        if 7 in processes_treeview_columns_shown:
            memory_shared = row_data_dict["memory_shared"]
            memory_shared_list.append(memory_shared)
            tab_data_row.append(memory_shared)
        if 8 in processes_treeview_columns_shown:
            process_read_bytes = row_data_dict["read_data"]
            tab_data_row.append(process_read_bytes)
            disk_read_data_list.append(process_read_bytes)
        if 9 in processes_treeview_columns_shown:
            process_write_bytes = row_data_dict["written_data"]
            tab_data_row.append(process_write_bytes)
            disk_write_data_list.append(process_write_bytes)
        if 10 in processes_treeview_columns_shown:
            disk_read_speed = row_data_dict["read_speed"]
            tab_data_row.append(disk_read_speed)
            disk_read_speed_list.append(disk_read_speed)
        if 11 in processes_treeview_columns_shown:
            disk_write_speed = row_data_dict["write_speed"]
            tab_data_row.append(disk_write_speed)
            disk_write_speed_list.append(disk_write_speed)
        if 12 in processes_treeview_columns_shown:
            tab_data_row.append(row_data_dict["nice"])
        if 13 in processes_treeview_columns_shown:
            tab_data_row.append(row_data_dict["number_of_threads"])
        if 14 in processes_treeview_columns_shown:
            tab_data_row.append(ppid)
        if 15 in processes_treeview_columns_shown:
            tab_data_row.append(row_data_dict["uid"])
        if 16 in processes_treeview_columns_shown:
            tab_data_row.append(row_data_dict["gid"])
        if 17 in processes_treeview_columns_shown:
            tab_data_row.append(row_data_dict["start_time"])
        if 18 in processes_treeview_columns_shown:
            tab_data_row.append(process_commandline)

        # Append process data into a list
        processes_data_rows.append(tab_data_row)

    # Convert set to list (it was set before getting process information)
    processes_treeview_columns_shown = sorted(list(processes_treeview_columns_shown))

    TabObject_data = [treeview2101, processes_data_list, processes_treeview_columns_shown, processes_data_column_order,
                     processes_data_row_sorting_column, processes_data_row_sorting_order, processes_data_column_widths,
                     processes_treeview_columns_shown_prev, processes_data_column_order_prev, processes_data_row_sorting_column_prev,
                     processes_data_row_sorting_order_prev, processes_data_column_widths_prev,
                     processes_data_rows, processes_data_rows_prev]

    reset_row_unique_data_list_prev = treeview_add_remove_columns(TabObject_data)
    if reset_row_unique_data_list_prev == "yes":
        pid_list_prev = []
    treeview_reorder_columns_sort_rows_set_column_widths(TabObject_data)

    # Append treestore items (rows) as tree or list structure depending on user preferences.
    global treestore, piter_list
    if show_processes_as_tree != show_processes_as_tree_prev:                            # Check if "show_processes_as_tree" setting has been changed since last loop and redefine "piter_list" in order to prevent resetting it in every loop which will cause high CPU consumption because piter_list and treestore content would have been appended/builded from zero.
        pid_list_prev = []                                                               # Redefine (clear) "pid_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
        treestore.clear()                                                            # Clear treestore because items will be appended from zero (in tree or list structure).
        piter_list = []


    global temporary_show_processes_as_tree_prev
    temporary_show_processes_as_tree = Config.temporary_show_processes_as_tree
    if temporary_show_processes_as_tree != temporary_show_processes_as_tree_prev:
        pid_list_prev = []
        treestore.clear()
        piter_list = []

    # Prevent errors if no rows are found.
    if len(processes_data_rows[0]) == 0:
        return

    deleted_rows, new_rows, updated_existing_row_index = get_new_deleted_updated_rows(pid_list, pid_list_prev)
    update_treestore_rows(TabObject_data, rows_data_dict, deleted_rows, new_rows, updated_existing_row_index, pid_list, pid_list_prev, show_processes_as_tree, temporary_show_processes_as_tree)

    # Expand all treeview rows (if treeview items are in tree structured, not list) if this is the first loop
    # of the Processes tab. It expands treeview rows (and children) in all loops if this control is not made.
    # "First loop" control is made by checking if pid_list_prev is empty.
    if pid_list_prev == []:
        treeview2101.expand_all()

    pid_list_prev = pid_list
    processes_data_rows_prev = processes_data_rows
    show_processes_as_tree_prev = show_processes_as_tree
    temporary_show_processes_as_tree_prev = temporary_show_processes_as_tree
    processes_treeview_columns_shown_prev = processes_treeview_columns_shown
    processes_data_row_sorting_column_prev = processes_data_row_sorting_column
    processes_data_row_sorting_order_prev = processes_data_row_sorting_order
    processes_data_column_order_prev = processes_data_column_order
    processes_data_column_widths_prev = processes_data_column_widths

    # Get max values of some performance data for setting cell background colors depending on relative performance data.
    global max_value_cpu_usage_list, max_value_memory_rss_list, max_value_memory_vms_list, max_value_memory_shared_list
    global max_value_disk_read_data_list, max_value_disk_write_data_list, max_value_disk_read_speed_list, max_value_disk_write_speed_list
    try:
        max_value_cpu_usage_list = max(cpu_usage_list)
    except ValueError:
        max_value_cpu_usage_list = 0
    try:
        max_value_memory_rss_list = max(memory_rss_list)
    except ValueError:
        max_value_memory_rss_list = 0
    try:
        max_value_memory_vms_list = max(memory_vms_list)
    except ValueError:
        max_value_memory_vms_list = 0
    try:
        max_value_memory_shared_list = max(memory_shared_list)
    except ValueError:
        max_value_memory_shared_list = 0
    try:
        max_value_disk_read_data_list = max(disk_read_data_list)
    except ValueError:
        max_value_disk_read_data_list = 0
    try:
        max_value_disk_write_data_list = max(disk_write_data_list)
    except ValueError:
        max_value_disk_write_data_list = 0
    try:
        max_value_disk_read_speed_list = max(disk_read_speed_list)
    except ValueError:
        max_value_disk_read_speed_list = 0
    try:
        max_value_disk_write_speed_list = max(disk_write_speed_list)
    except ValueError:
        max_value_disk_write_speed_list = 0

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


def treeview_add_remove_columns(TabObject_data):
    """
    Add/Remove treeview columns appropriate for user preferences.
    Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if
    column numbers are changed. Because once treestore data types (str, int, etc) are defined, they
    can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal
    can not be performed.
    """

    treeview = TabObject_data[0]
    row_data_list = TabObject_data[1]
    treeview_columns_shown_prev = TabObject_data[7]
    #piter_list = TabObject_data[13]

    # Get treeview columns shown
    treeview_columns_shown = Config.processes_treeview_columns_shown

    # Add/Remove treeview columns if they are changed since the last loop.
    treeview.freeze_child_notify()
    reset_row_unique_data_list_prev = "no"
    if treeview_columns_shown != treeview_columns_shown_prev:
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        # Remove all columns in the treeview.
        for column in treeview.get_columns():
            treeview.remove_column(column)
        for i, column in enumerate(treeview_columns_shown):
            if row_data_list[column][0] in treeview_columns_shown:
                cumulative_sort_column_id = cumulative_sort_column_id + row_data_list[column][2]
            # Define column (also column title is defined)
            treeview_column = Gtk.TreeViewColumn(row_data_list[column][1])
            for i, cell_renderer_type in enumerate(row_data_list[column][6]):
                cumulative_internal_data_id = cumulative_internal_data_id + 1
                # Continue to next loop to avoid generating a cell renderer for internal column
                # (internal columns are not shown on the treeview and they do not have cell renderers).
                if cell_renderer_type == "internal_column":
                    continue
                # Define cell renderer
                if cell_renderer_type == "CellRendererPixbuf":
                    cell_renderer = Gtk.CellRendererPixbuf()
                if cell_renderer_type == "CellRendererText":
                    cell_renderer = Gtk.CellRendererText()
                if cell_renderer_type == "CellRendererToggle":
                    cell_renderer = Gtk.CellRendererToggle()
                # Vertical alignment is set 0.5 in order to leave it as unchanged.
                cell_renderer.set_alignment(row_data_list[column][9][i], 0.5)
                # Set if column will allocate unused space
                treeview_column.pack_start(cell_renderer, row_data_list[column][10][i])
                treeview_column.add_attribute(cell_renderer, row_data_list[column][7][i], cumulative_internal_data_id)
                if row_data_list[column][11][i] != "no_cell_function":
                    treeview_column.set_cell_data_func(cell_renderer, row_data_list[column][11][i], func_data=cumulative_internal_data_id)    # Define cell function which sets cell data precision and/or data unit
            treeview_column.set_sizing(2)                                           # Set column sizing (2 = auto sizing which is required for "treeview.set_fixed_height_mode(True)" command that is used for lower treeview CPU consumption because row heights are not calculated for every row).
            treeview_column.set_sort_column_id(cumulative_sort_column_id)           # Be careful with lists contain same element more than one.
            treeview_column.set_resizable(True)                                     # Set columns resizable by the user when column title button edge handles are dragged.
            treeview_column.set_reorderable(True)                                   # Set columns reorderable by the user when column title buttons are dragged.
            treeview_column.set_min_width(50)                                       # Set minimum column widths as "50 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            treeview_column.connect("clicked", on_column_title_clicked, TabObject_data)  # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
            treeview_column.connect("notify::width", treeview_column_order_width_row_sorting)
            treeview.append_column(treeview_column)                                 # Append column into treeview

        # Get column data types for appending row data into treestore
        data_column_types = []
        for column in sorted(treeview_columns_shown):
            internal_column_count = len(row_data_list[column][5])
            for internal_column_number in range(internal_column_count):
                data_column_types.append(row_data_list[column][5][internal_column_number])    # Get column types (int, bool, float, str, etc.)

        # Define a treestore (for storing treeview data in it), a treemodelfilter (for search filtering),
        # treemodelsort (for row sorting when column title buttons are clicked)
        global treestore
        treestore = Gtk.TreeStore()
        treestore.set_column_types(data_column_types)                     # Set column types of the columns which will be appended into treestore
        treemodelfilter = treestore.filter_new()
        treemodelfilter.set_visible_column(0)                                       # Column "0" of the treestore will be used for column visibility information (True or False)
        treemodelsort = Gtk.TreeModelSort().new_with_model(treemodelfilter)
        treeview.set_model(treemodelsort)
        global piter_list
        piter_list = []
        reset_row_unique_data_list_prev = "yes"                                     # For redefining (clear) "pid_list_prev, human_user_uid_list_prev, service_list_prev" lists. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
    treeview.thaw_child_notify()

    return reset_row_unique_data_list_prev


def get_new_deleted_updated_rows(row_id_list, row_id_list_prev):
    """
    Get new/deleted/updated rows for updating treestore/treeview.
    """

    row_id_list_prev_set = set(row_id_list_prev)
    row_id_list_set = set(row_id_list)
    deleted_rows = sorted(list(row_id_list_prev_set - row_id_list_set))
    new_rows = sorted(list(row_id_list_set - row_id_list_prev_set))
    existing_rows = sorted(list(row_id_list_set.intersection(row_id_list_prev)))
    # "c = set(a).intersection(b)" is about 19% faster than "c = set(a).intersection(set(b))"
    updated_existing_row_index = [[row_id_list.index(i), row_id_list_prev.index(i)] for i in existing_rows]

    return deleted_rows, new_rows, updated_existing_row_index


def update_treestore_rows(TabObject_data, rows_data_dict, deleted_rows, new_rows, updated_existing_row_index, row_id_list, row_id_list_prev, show_rows_as_tree=0, temporary_show_processes_as_tree=0):
    """
    Add/Remove/Update treestore rows.
    """

    treeview = TabObject_data[0]
    row_data_list = TabObject_data[1]
    treeview_columns_shown_prev = TabObject_data[7]
    tab_data_rows = TabObject_data[12]
    tab_data_rows_prev = TabObject_data[13]

    global searchentry, on_searchentry_changed, show_processes_of_all_users, treestore, piter_list
    searchentry = searchentry2101
    on_searchentry_changed = on_searchentry2101_changed

    treeview.freeze_child_notify()
    tab_data_rows_row_length = len(tab_data_rows[0])
    if len(piter_list) > 0:
        for i, j in updated_existing_row_index:
            if tab_data_rows[i] != tab_data_rows_prev[j]:
                # Start from "1" in order to set first element (treeview row visibility data) as "True" in every loop.
                for k in range(1, tab_data_rows_row_length):
                    if tab_data_rows_prev[j][k] != tab_data_rows[i][k]:
                        treestore.set_value(piter_list[j], k, tab_data_rows[i][k])
    if len(deleted_rows) > 0:
        for row in reversed(sorted(list(deleted_rows))):
            treestore.remove(piter_list[row_id_list_prev.index(row)])
            piter_list.remove(piter_list[row_id_list_prev.index(row)])
        # Update search results
        on_searchentry_changed(searchentry)
    if len(new_rows) > 0:
        for row in new_rows:
            pid_index = row_id_list.index(row)
            if show_rows_as_tree == 1 and temporary_show_processes_as_tree == 1:
                row_data_dict = rows_data_dict[row]
                parent_row = row_data_dict["ppid"]
                if parent_row == 0:                                                           # Row ppid was set as "0" if it has no parent row. Row is set as tree root (this root has no relationship between root user) row if it has no ppid (parent row). Treeview tree indentation is first level for the tree root row.
                    piter_list.append(treestore.append(None, tab_data_rows[pid_index]))
                else:
                    if show_processes_of_all_users == 1:                                      # Row appended under tree root row or another row if "Show [ROWS] as tree" option is preferred.
                        piter_list.append(treestore.append(piter_list[row_id_list.index(parent_row)], tab_data_rows[pid_index]))
                    if show_processes_of_all_users == 0 and parent_row not in row_id_list:    # Row is appended into treeview as tree root row if "Show [ROWS] of all users" is not preferred and row ppid not in row_id_list.
                        piter_list.append(treestore.append(None, tab_data_rows[pid_index]))
                    if show_processes_of_all_users == 0 and parent_row in row_id_list:        # Row is appended into treeview under tree root row or another row if "Show [ROWS] of all users" is preferred and row ppid is in row_id_list.
                        piter_list.append(treestore.append(piter_list[row_id_list.index(parent_row)], tab_data_rows[pid_index]))
            else:                                                                             # All rows are appended into treeview as tree root row if "Show [ROWS] as tree" is not preferred. Thus rows are listed as list structure instead of tree structure.
                piter_list.insert(pid_index, treestore.insert(None, pid_index, tab_data_rows[pid_index]))
        # Update search results
        on_searchentry_changed(searchentry)
    treeview.thaw_child_notify()


def treeview_reorder_columns_sort_rows_set_column_widths(TabObject_data):
    """
    Reorder TreeView columns, sort TreeView rows and set TreeView columns.
    """

    treeview = TabObject_data[0]
    row_data_list = TabObject_data[1]
    treeview_columns_shown = TabObject_data[2]
    tab_data_rows = TabObject_data[12]
    tab_data_rows_prev = TabObject_data[13]
    data_column_order = TabObject_data[3]
    data_row_sorting_column = TabObject_data[4]
    data_row_sorting_order = TabObject_data[5]
    data_column_widths = TabObject_data[6]
    treeview_columns_shown_prev = TabObject_data[7]
    data_column_order_prev = TabObject_data[8]
    data_row_sorting_column_prev = TabObject_data[9]
    data_row_sorting_order_prev = TabObject_data[10]
    data_column_widths_prev = TabObject_data[11]

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or
    # user has reset column order from customizations.
    if treeview_columns_shown_prev != treeview_columns_shown or data_column_order_prev != data_column_order:
        # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_columns = treeview.get_columns()
        treeview_column_titles = []
        for column in treeview_columns:
            treeview_column_titles.append(column.get_title())
        data_column_order_scratch = []
        for column_order in data_column_order:
            if column_order != -1:
                data_column_order_scratch.append(column_order)
        # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
        for order in reversed(sorted(data_column_order_scratch)):
            if data_column_order.index(order) in treeview_columns_shown:
                column_number_to_move = data_column_order.index(order)
                column_title_to_move = row_data_list[column_number_to_move][1]
                column_to_move = treeview_columns[treeview_column_titles.index(column_title_to_move)]
                # Column is moved at the beginning of the treeview if "None" is used.
                treeview.move_column_after(column_to_move, None)

    # Sort rows if user has changed row sorting column and sorting order (ascending/descending) by clicking
    # on any column title button on the GUI.
    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid
    # reordering/sorting in every loop.
    if treeview_columns_shown_prev != treeview_columns_shown or \
       data_row_sorting_column_prev != data_row_sorting_column or \
       data_row_sorting_order != data_row_sorting_order_prev:
        # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_columns = treeview.get_columns()
        treeview_column_titles = []
        for column in treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i in range(10):
            if data_row_sorting_column in treeview_columns_shown:
                for data in row_data_list:
                    if data[0] == data_row_sorting_column:
                        column_title_for_sorting = data[1]
            if data_row_sorting_column not in treeview_columns_shown:
                column_title_for_sorting = row_data_list[0][1]
            column_for_sorting = treeview_columns[treeview_column_titles.index(column_title_for_sorting)]
            column_for_sorting.clicked()                                                      # For row sorting.
            if data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                break

    # Set column widths if there are changes since last loop.
    if treeview_columns_shown_prev != treeview_columns_shown or data_column_widths_prev != data_column_widths:
        treeview_columns = treeview.get_columns()
        treeview_column_titles = []
        for column in treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i, row_data in enumerate(row_data_list):
            for j, column_title in enumerate(treeview_column_titles):
                if column_title == row_data[1]:
                   column_width = data_column_widths[i]
                   # Set column width in pixels. Fixed width is unset if value is "-1".
                   treeview_columns[j].set_fixed_width(column_width)


def treeview_column_order_width_row_sorting(widget, parameter):
    """
    Get and save column order/width, row sorting.
    Columns in the treeview are get one by one and appended into "data_column_order".
    "data_column_widths" list elements are modified for widths of every columns in the treeview.
    Length of these list are always same even if columns are removed, appended and column widths are changed.
    Only values of the elements (element indexes are always same with "row_data_list") are changed if column order/widths are changed.
    """

    global treeview2101, processes_data_list
    treeview = treeview2101
    row_data_list = processes_data_list

    # Get previous column order and widths
    data_column_order_prev = Config.processes_data_column_order
    data_column_widths_prev = Config.processes_data_column_widths

    # Get new column order and widths
    treeview_columns = treeview.get_columns()
    treeview_column_titles = []
    for column in treeview_columns:
        treeview_column_titles.append(column.get_title())

    data_column_order = [-1] * len(row_data_list)
    data_column_widths = [-1] * len(row_data_list)

    treeview_columns_last_index = len(treeview_columns)-1

    for i, row_data in enumerate(row_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == row_data[1]:
                column_index = treeview_column_titles.index(row_data[1])
                data_column_order[i] = column_index
                if j != treeview_columns_last_index:
                    data_column_widths[i] = treeview_columns[column_index].get_width()

    # Prevent saving settings if column order and widths are not changed.
    if data_column_order == data_column_order_prev and data_column_widths == data_column_widths_prev:
        return

    # Save new column order and widths
    Config.processes_data_column_order = list(data_column_order)
    Config.processes_data_column_widths = list(data_column_widths)

    Config.config_save_func()


def on_column_title_clicked(widget, TabObject_data):
    """
    Get and save column sorting order.
    """

    row_data_list = TabObject_data[1]

    # Get column title which will be used for getting column number
    data_row_sorting_column_title = widget.get_title()
    for data in row_data_list:
        if data[1] == data_row_sorting_column_title:
            # Get column number
            data_row_sorting_column = data[0]

    # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    data_row_sorting_order = int(widget.get_sort_order())

    # Save new column order and widths
    Config.processes_data_row_sorting_column = data_row_sorting_column
    Config.processes_data_row_sorting_order = data_row_sorting_order

    Config.config_save_func()


def on_columns_changed(widget, treeview):
    """
    Called if number of columns changed.
    """

    # Get treeview columns shown
    treeview_columns_shown = Config.processes_treeview_columns_shown

    treeview_columns = treeview.get_columns()
    if len(treeview_columns_shown) != len(treeview_columns):
        return
    if treeview_columns[0].get_width() == 0:
        return
    treeview_column_order_width_row_sorting(widget, None)


# ----------------------------------- Processes - Treeview Cell Functions (defines functions for treeview cell for setting data precisions and/or data units) -----------------------------------
def cell_data_function_cpu_usage_percent(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{tree_model.get(iter, data)[0]:.{processes_cpu_precision}f} %')
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_cpu_usage_list)

def cell_data_function_memory_rss(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_memory_data_unit, processes_memory_data_precision))
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_memory_rss_list)

def cell_data_function_memory_vms(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_memory_data_unit, processes_memory_data_precision))
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_memory_vms_list)

def cell_data_function_memory_shared(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_memory_data_unit, processes_memory_data_precision))
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_memory_shared_list)

def cell_data_function_disk_read_data(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_disk_data_unit, processes_disk_data_precision))
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_disk_read_data_list)

def cell_data_function_disk_write_data(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_disk_data_unit, processes_disk_data_precision))
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_disk_write_data_list)

def cell_data_function_disk_read_speed(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{performance_data_unit_converter_func("speed", processes_disk_speed_bit, tree_model.get(iter, data)[0], processes_disk_data_unit, processes_disk_data_precision)}/s')
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_disk_read_speed_list)

def cell_data_function_disk_write_speed(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{performance_data_unit_converter_func("speed", processes_disk_speed_bit, tree_model.get(iter, data)[0], processes_disk_data_unit, processes_disk_data_precision)}/s')
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_disk_write_speed_list)

def cell_data_function_start_time(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', datetime.fromtimestamp(tree_model.get(iter, data)[0]).strftime("%d.%m.%Y %H:%M:%S"))

def cell_backround_color(cell, value, max_value):
    if value > 0.7 * max_value:
        color = Gdk.RGBA(0.7, 0.35, 0.05, 0.45)
    elif value <= 0.7 * max_value and value > 0.4 * max_value:
        color = Gdk.RGBA(0.7, 0.35, 0.05, 0.35)
    elif value <= 0.4 * max_value and value > 0.2 * max_value:
        color = Gdk.RGBA(0.7, 0.35, 0.05, 0.25)
    elif value <= 0.2 * max_value and value > 0.1 * max_value:
        color = Gdk.RGBA(0.7, 0.35, 0.05, 0.15)
    elif value <= 0.1 * max_value:
        color = Gdk.RGBA(0.7, 0.35, 0.05, 0.0)
    cell.set_property('background-rgba', color)


def get_system_boot_time():
    """
    Get system boot time.
    """

    with open("/proc/stat") as reader:
        stat_lines = reader.read().split("\n")

    for line in stat_lines:
        if "btime " in line:
            system_boot_time = int(line.split()[1].strip())

    return system_boot_time


def get_username_uid_dict():
    """
    Get usernames and UIDs.
    """

    environment_type = get_environment_type()

    if environment_type == "flatpak":
        with open("/var/run/host/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")
    else:
        with open("/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")

    username_uid_dict = {}
    for line in etc_passwd_lines:
        line_splitted = line.split(":", 3)
        username_uid_dict[int(line_splitted[2])] = line_splitted[0]

    return username_uid_dict


def get_application_name_image_dict():
    """
    Get application names and images. Process name will be searched in "application_image_dict" list.
    """

    application_image_dict = {}

    # Get ".desktop" file names
    application_file_list = [file for file in os.listdir("/usr/share/applications/") if file.endswith(".desktop")]

    # Get application name and image information
    for application in application_file_list:

        # "encoding="utf-8"" is used for preventing "UnicodeDecodeError" errors during reading the file content if "C" locale is used.
        try:
            with open("/usr/share/applications/" + application, encoding="utf-8") as reader:
                application_file_content = reader.read()
        except PermissionError:
            continue

        # Do not include application name or icon name if any of them is not found in the .desktop file.
        if "Exec=" not in application_file_content or "Icon=" not in application_file_content:
            continue

        # Get application exec data
        application_exec = application_file_content.split("Exec=", 1)[1].split("\n", 1)[0].split("/")[-1].split(" ")[0]
        # Splitting operation above may give "sh" as application name and this may cause confusion between "sh" process
        # and splitted application exec (for example: sh -c "gdebi-gtk %f"sh -c "gdebi-gtk %f").
        # This statement is used to avoid from this confusion.
        if application_exec == "sh":
            application_exec = application_file_content.split("Exec=", 1)[1].split("\n", 1)[0]

        # Get application image name data
        application_image = application_file_content.split("Icon=", 1)[1].split("\n", 1)[0]

        application_image_dict[application_exec] = application_image

    return application_image_dict


def get_number_of_logical_cores():
    """
    Get number of online logical cores.
    """

    try:
        # First try a faster way: using "SC_NPROCESSORS_ONLN" variable.
        number_of_logical_cores = os.sysconf("SC_NPROCESSORS_ONLN")
    except ValueError:
        # As a second try, count by reading from "/proc/cpuinfo" file.
        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_lines = reader.read().split("\n")
        number_of_logical_cores = 0
        for line in proc_cpuinfo_lines:
            if line.startswith("processor"):
                number_of_logical_cores = number_of_logical_cores + 1

    return number_of_logical_cores


def get_environment_type():
    """
    Detect environment type (Flatpak or native).
    It will be used for accessing host OS commands if the application is run in Flatpak environment.
    """

    application_flatpak_id = os.getenv('FLATPAK_ID')

    if application_flatpak_id != None:
        environment_type = "flatpak"
    else:
        environment_type = "native"

    return environment_type


def get_processes_information(process_list=[], processes_of_user="all", cpu_usage_divide_by_cores="yes", detail_level="medium", processes_data_dict_prev={}, system_boot_time=0, username_uid_dict={}):
    """
    Get process information of all/specified processes.
    """

    global number_of_clock_ticks, memory_page_size, process_status_dict

    # Get usernames and UIDs
    if username_uid_dict == {}:
        username_uid_dict = get_username_uid_dict()

    # Get current username which will be used for determining processes from only this user or other users.
    current_user_name = os.environ.get('USER')

    # Redefine core count division number if "Divide CPU usage by core count" option is disabled.
    if cpu_usage_divide_by_cores == "yes":
        core_count_division_number = get_number_of_logical_cores()
    else:
        core_count_division_number = 1

    # Get system boot time
    if system_boot_time == 0:
        system_boot_time = get_system_boot_time()

    # Read information from procfs files. "/proc/[PID]/smaps" file is not read for all processes. Because reading and
    # processing "/proc/[PID]/smaps" file data for all processes (about 250 processes) requires nearly 1 second on a 4 core CPU (i7-2630QM).
    cat_output_split, global_time, global_cpu_time_all = read_process_information(process_list, detail_level)

    # Define lists for getting process information from command output.
    processes_data_dict = {}
    if processes_data_dict_prev != {}:
        pid_list_prev = processes_data_dict_prev["pid_list"]
        ppid_list_prev = processes_data_dict_prev["ppid_list"]
        process_cpu_times_prev = processes_data_dict_prev["process_cpu_times"]
        disk_read_write_data_prev = processes_data_dict_prev["disk_read_write_data"]
        global_cpu_time_all_prev = processes_data_dict_prev["global_cpu_time_all"]
        global_time_prev = processes_data_dict_prev["global_time"]
    else:
        pid_list_prev = []
        ppid_list_prev = []
        process_cpu_times_prev = {}
        disk_read_write_data_prev = {}
    pid_list = []
    ppid_list = []
    username_list = []
    cmdline_list = []
    process_cpu_times = {}
    disk_read_write_data = {}

    # Get process information from command output.
    cat_output_split_iter = iter(cat_output_split)
    for process_data_stat_statm_status in cat_output_split_iter:
        # Also get second part of the data of the current process.
        if detail_level == "medium":
            process_data_io_cmdline = next(cat_output_split_iter)
        # Also get second and third part of the data of the current process.
        elif detail_level == "high":
            process_data_io_cmdline = next(cat_output_split_iter)
            process_data_smaps = next(cat_output_split_iter)

        # Get process information from "/proc/[PID]/stat" file
        # Skip to next loop if one of the stat, statm, status files is not read.
        try:
            stat_file, statm_file, status_file = process_data_stat_statm_status.split("\n", 2)
        except ValueError:
            continue
        if status_file.startswith("Name:") == False or "" in (stat_file, statm_file, status_file):
            continue
        stat_file_split = stat_file.split()

        # Get PID
        try:
            pid = int(stat_file_split[0])
        except IndexError:
            break

        ppid = int(stat_file_split[-49])
        status = process_status_dict[stat_file_split[-50]]
        # Get process CPU time in user mode (utime + stime)
        cpu_time_user = int(stat_file_split[-39])
        cpu_time_kernel = int(stat_file_split[-38])
        cpu_time = cpu_time_user + cpu_time_kernel
        # Get process RSS (resident set size) memory pages and multiply with memory_page_size in order to convert the value into bytes.
        memory_rss = int(stat_file_split[-29]) * memory_page_size
        # Get process VMS (virtual memory size) memory (this value is in bytes unit).
        memory_vms = int(stat_file_split[-30])
        # Elapsed time between system boot and process start time (measured in clock ticks and need to be divided by sysconf(_SC_CLK_TCK) for converting to wall clock time)
        start_time = (int(stat_file_split[-31]) / number_of_clock_ticks) + system_boot_time
        nice = int(stat_file_split[-34])
        number_of_threads = int(stat_file_split[-33])

        # Get process information from "/proc/[PID]/status" file
        name = status_file.split("Name:\t", 1)[1].split("\n", 1)[0]
        # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
        uid = int(status_file.split("\nUid:\t", 1)[1].split("\n", 1)[0].split("\t", 1)[0])
        # There are 4 values in the Gid line and first one (real GID) is get from this file.
        gid = int(status_file.split("\nGid:\t", 1)[1].split("\n", 1)[0].split("\t", 1)[0])

        # Get username
        try:
            username = username_uid_dict[uid]
        except KeyError:
            username = str(uid)

        # Skip to next process information if process information of current user is wanted.
        if processes_of_user == "current" and username != current_user_name:
            continue

        # Get process information from "/proc/[PID]/statm" file
        statm_file_split = statm_file.split()
        # Get shared memory pages and multiply with memory_page_size in order to convert the value into bytes.
        memory_shared = int(statm_file_split[2]) * memory_page_size
        # Get memory
        memory = memory_rss - memory_shared

        # Get process information from "/proc/[PID]/io" and "/proc/[PID]/cmdline" files
        if detail_level == "medium" or detail_level == "high":
            if process_data_io_cmdline.startswith("rchar") == True:
                try:
                    io_cmdline_files_split = process_data_io_cmdline.split("\n", 7)
                    cmdline_file = io_cmdline_files_split[-1]
                except ValueError:
                    io_cmdline_files_split = process_data_io_cmdline.split("\n")
                    cmdline_file = ""
                read_data = int(io_cmdline_files_split[4].split(":")[1])
                written_data = int(io_cmdline_files_split[5].split(":")[1])
            else:
                read_data = 0
                written_data = 0
                cmdline_file = process_data_io_cmdline
                io_cmdline_files_split = "-"

            # "cmdline" content may contain "\x00". They are replaced with " ". Otherwise, file content may be get as "".
            command_line = cmdline_file.replace("\x00", " ")
            if command_line == "":
                command_line = "-"

        # Get process information from "/proc/[PID]/smaps" file and other files that are processed previously.
        if detail_level == "high":
            # Get process USS (unique set size) memory and swap memory and convert them to bytes
            process_data_smaps_split = process_data_smaps.split("\n")
            private_clean = 0
            private_dirty = 0
            memory_swap = 0
            for line in process_data_smaps_split:
                if "Private_Clean:" in line:
                    private_clean = private_clean + int(line.split(":")[1].split()[0].strip())
                elif "Private_Dirty:" in line:
                    private_dirty = private_dirty + int(line.split(":")[1].split()[0].strip())
                elif line.startswith("Swap:"):
                    memory_swap = memory_swap + int(line.split(":")[1].split()[0].strip())
            memory_uss = (private_clean + private_dirty) * 1024
            memory_swap = memory_swap * 1024

            # Get other CPU time information (children_user, children_kernel, io_wait)
            cpu_time_children_user = int(stat_file_split[-37])
            cpu_time_children_kernel = int(stat_file_split[-36])
            cpu_time_io_wait = int(stat_file_split[-11])

            # Get numbers of CPU cores that process is run on.
            cpu_numbers = int(stat_file_split[-14])

            # Get UIDs (real, effective, saved)
            uids = status_file.split("\nUid:\t", 1)[1].split("\n", 1)[0].split("\t")
            uid_real, uid_effective, uid_saved = int(uids[0]), int(uids[1]), int(uids[2])

            # Get GIDs (real, effective, saved)
            gids = status_file.split("\nGid:\t", 1)[1].split("\n", 1)[0].split("\t")
            gid_real, gid_effective, gid_saved = int(gids[0]), int(gids[1]), int(gids[2])

            # Get number of context switches (voluntary and nonvoluntary)
            ctx_switches_voluntary = int(status_file.split("\nvoluntary_ctxt_switches:\t", 1)[1].split("\n", 1)[0])
            ctx_switches_nonvoluntary = int(status_file.split("\nnonvoluntary_ctxt_switches:\t", 1)[1].split("\n", 1)[0])

            # Get read count and write count
            if io_cmdline_files_split != "-":
                read_count = int(io_cmdline_files_split[2].split(":")[1])
                write_count = int(io_cmdline_files_split[3].split(":")[1])
            else:
                read_count = 0
                write_count = 0

        # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters
        # (it is counted as 15). "/proc/[PID]/cmdline" file is read and it is split by the last "/" character 
        # (not all process cmdlines have this) in order to obtain full process name.
        if detail_level == "medium" or detail_level == "high":
            process_name_from_status = name
            if len(name) == 15:
                name = command_line.split("/")[-1].split(" ")[0]
                if name.startswith(process_name_from_status) == False:
                    name = command_line.split(" ")[0].split("/")[-1]
                    if name.startswith(process_name_from_status) == False:
                        name = process_name_from_status

        # Get CPU usage by using CPU times
        process_cpu_time = cpu_time
        process_cpu_times[pid] = process_cpu_time
        try:
            process_cpu_time_prev = process_cpu_times_prev[pid]
        except KeyError:
            # There is no "process_cpu_time_prev" value and get it from "process_cpu_time" if this is first loop of the process.
            process_cpu_time_prev = process_cpu_time
            # Subtract "1" CPU time (a negligible value) if this is first loop of the process.
            global_cpu_time_all_prev = global_cpu_time_all - 1
        cpu_usage = (process_cpu_time - process_cpu_time_prev) / (global_cpu_time_all - global_cpu_time_all_prev) * 100 / core_count_division_number

        # Get disk read speed and disk write speed
        if detail_level == "medium" or detail_level == "high":
            disk_read_write_data[pid] = (read_data, written_data)
            try:
                read_data_prev, written_data_prev = disk_read_write_data_prev[pid]
                update_interval = global_time - global_time_prev
            except (KeyError, NameError) as e:
                # Make read_data_prev and written_data_prev equal to read_data for giving "0" disk read/write speed values
                # if this is first loop of the process
                read_data_prev = read_data
                written_data_prev = written_data
                update_interval = 1
            read_speed = (read_data - read_data_prev) / update_interval
            write_speed = (written_data - written_data_prev) / update_interval

        pid_list.append(pid)
        ppid_list.append(ppid)
        if detail_level == "medium" or detail_level == "high":
            cmdline_list.append(command_line)
        username_list.append(username)

        # Add process data to a sub-dictionary
        if detail_level == "low":
            process_data_dict = {
                                "name" : name,
                                "username" : username,
                                "status" : status,
                                "cpu_time" : cpu_time,
                                "cpu_usage" : cpu_usage,
                                "memory_rss" : memory_rss,
                                "memory_vms" : memory_vms,
                                "memory_shared" : memory_shared,
                                "memory" : memory,
                                "nice" : nice,
                                "number_of_threads" : number_of_threads,
                                "ppid" : ppid,
                                "uid" : uid,
                                "gid" : gid,
                                "start_time" : start_time,
                                }
        elif detail_level == "medium":
            process_data_dict = {
                                "name" : name,
                                "username" : username,
                                "status" : status,
                                "cpu_time" : cpu_time,
                                "cpu_usage" : cpu_usage,
                                "memory_rss" : memory_rss,
                                "memory_vms" : memory_vms,
                                "memory_shared" : memory_shared,
                                "memory" : memory,
                                "read_data" : read_data,
                                "written_data" : written_data,
                                "read_speed" : read_speed,
                                "write_speed" : write_speed,
                                "nice" : nice,
                                "number_of_threads" : number_of_threads,
                                "ppid" : ppid,
                                "uid" : uid,
                                "gid" : gid,
                                "start_time" : start_time,
                                "command_line" : command_line
                                }
        elif detail_level == "high":
            process_data_dict = {
                                "name" : name,
                                "username" : username,
                                "status" : status,
                                "cpu_time" : cpu_time,
                                "cpu_usage" : cpu_usage,
                                "memory_rss" : memory_rss,
                                "memory_vms" : memory_vms,
                                "memory_shared" : memory_shared,
                                "memory" : memory,
                                "memory_uss" : memory_uss,
                                "memory_swap" : memory_swap,
                                "read_data" : read_data,
                                "written_data" : written_data,
                                "read_speed" : read_speed,
                                "write_speed" : write_speed,
                                "nice" : nice,
                                "number_of_threads" : number_of_threads,
                                "ppid" : ppid,
                                "uid" : uid,
                                "gid" : gid,
                                "start_time" : start_time,
                                "command_line" : command_line,
                                "memory_uss": memory_uss,
                                "memory_swap": memory_swap,
                                "cpu_time_user": cpu_time_user,
                                "cpu_time_kernel": cpu_time_kernel,
                                "cpu_time_children_user": cpu_time_children_user,
                                "cpu_time_children_kernel": cpu_time_children_kernel,
                                "cpu_time_io_wait": cpu_time_io_wait,
                                "cpu_numbers": cpu_numbers,
                                "uid_real" : uid_real,
                                "uid_effective" : uid_effective,
                                "uid_saved" : uid_saved,
                                "gid_real" : gid_real,
                                "gid_effective" : gid_effective,
                                "gid_saved" : gid_saved,
                                "ctx_switches_voluntary": ctx_switches_voluntary,
                                "ctx_switches_nonvoluntary": ctx_switches_nonvoluntary,
                                "read_count": read_count,
                                "write_count": write_count
                                }

        # Add process sub-dictionary to dictionary
        processes_data_dict[pid] = process_data_dict

    # Add process related lists and variables for returning them for using them (for using some them as previous data in the next loop).
    processes_data_dict["pid_list"] = pid_list
    processes_data_dict["ppid_list"] = ppid_list
    processes_data_dict["username_list"] = username_list
    processes_data_dict["cmdline_list"] = cmdline_list
    processes_data_dict["process_cpu_times"] = process_cpu_times
    processes_data_dict["disk_read_write_data"] = disk_read_write_data
    processes_data_dict["global_cpu_time_all"] = global_cpu_time_all
    processes_data_dict["global_time"] = global_time

    return processes_data_dict


def read_process_information(process_list, detail_level="medium"):
    """
    Read information from procfs files.
    """

    # Get environment type
    environment_type = get_environment_type()

    # Get process PIDs
    if process_list == []:
        command_list = ["ls", "/proc/"]
        if environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        ls_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()
        pid_list = []
        for pid in ls_output.split():
            if pid.isdigit() == True:
                pid_list.append(pid)
        pid_list = sorted(pid_list, key=int)
    else:
        pid_list = process_list

    # Get process information from procfs files. "/proc/version" file content is used as separator text.
    command_list = ["env", "LANG=C", "cat"]
    command_list.append('/proc/version')
    if environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    if detail_level == "low":
        for pid in pid_list:
            command_list.extend((
                                f'/proc/{pid}/stat',
                                f'/proc/{pid}/statm',
                                f'/proc/{pid}/status',
                                '/proc/version'
                                ))
    elif detail_level == "medium":
        for pid in pid_list:
            command_list.extend((
                                f'/proc/{pid}/stat',
                                f'/proc/{pid}/statm',
                                f'/proc/{pid}/status',
                                '/proc/version',
                                f'/proc/{pid}/io',
                                f'/proc/{pid}/cmdline',
                                '/proc/version'
                                ))
    elif detail_level == "high":
        for pid in pid_list:
            command_list.extend((
                                f'/proc/{pid}/stat',
                                f'/proc/{pid}/statm',
                                f'/proc/{pid}/status',
                                '/proc/version',
                                f'/proc/{pid}/io',
                                f'/proc/{pid}/cmdline',
                                '/proc/version',
                                f'/proc/{pid}/smaps',
                                '/proc/version'
                                ))
    # Get time just before "/proc/[PID]/stat" file is read in order to calculate an average value.
    time_before = time.time()
    #cat_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)).stdout.strip()
    cat_output = subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    # Get time just after "/proc/[PID]/stat" file is read in order to calculate an average value.
    time_after = time.time()
    # Calculate average values of "global_time" and "global_cpu_time_all".
    global_time = (time_before + time_after) / 2
    global_cpu_time_all = global_time * number_of_clock_ticks
    try:
        cat_output = cat_output.decode().strip()
    # Prevent errors if "cmdline" file contains characters that can not be decoded.
    except UnicodeDecodeError:
        cat_output = cat_output.decode("utf-8", "ignore").strip()

    # Get separator text
    separator_text = cat_output.split("\n", 1)[0]

    cat_output_split = cat_output.split(separator_text + "\n")
    # Delete first empty element
    del cat_output_split[0]

    return cat_output_split, global_time, global_cpu_time_all


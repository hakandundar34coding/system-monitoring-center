#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Gio', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, GLib, GObject, Gio, Pango

import os
import time
import subprocess
from datetime import datetime

from locale import gettext as _tr

from Config import Config
from MainWindow import MainWindow
import Common


class Users:

    def __init__(self):

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_grid = Common.tab_grid()

        self.tab_title_grid()

        self.tab_info_grid()

        self.gui_signals()

        self.right_click_menu()


    def tab_title_grid(self):
        """
        Generate tab name label, searchentry.
        """

        # Grid (tab title)
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.tab_grid.attach(grid, 0, 0, 1, 1)

        # Label (Users)
        label = Common.tab_title_label(_tr("Users"))
        grid.attach(label, 0, 0, 1, 1)

        # SearchEntry
        self.searchentry = Common.scrolledwindow_searchentry(self.on_searchentry_changed)
        grid.attach(self.searchentry, 1, 0, 1, 1)


    def tab_info_grid(self):
        """
        Generate information GUI objects.
        """

        # ScrolledWindow
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.tab_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # TreeView
        self.treeview = Gtk.TreeView()
        self.treeview.set_activate_on_single_click(True)
        self.treeview.set_show_expanders(False)
        self.treeview.set_fixed_height_mode(True)
        self.treeview.set_headers_clickable(True)
        self.treeview.set_enable_search(True)
        self.treeview.set_search_column(2)
        self.treeview.set_tooltip_column(2)
        scrolledwindow.set_child(self.treeview)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # Treeview mouse events.
        treeview_mouse_event = Gtk.GestureClick()
        treeview_mouse_event.connect("pressed", self.on_treeview_pressed)
        treeview_mouse_event.connect("released", self.on_treeview_released)
        self.treeview.add_controller(treeview_mouse_event)

        treeview_mouse_event_right_click = Gtk.GestureClick()
        treeview_mouse_event_right_click.set_button(3)
        treeview_mouse_event_right_click.connect("pressed", self.on_treeview_pressed)
        self.treeview.add_controller(treeview_mouse_event_right_click)

        # Right click menu actions
        # "Details" action
        action = Gio.SimpleAction.new("users_details", None)
        action.connect("activate", self.on_details_item_clicked)
        MainWindow.main_window.add_action(action)


    def right_click_menu(self):
        """
        Generate right click menu GUI.
        """

        # Menu models
        right_click_menu_model = Gio.Menu.new()
        right_click_menu_model.append(_tr("Details"), "win.users_details")

        # Popover menu
        self.right_click_menu_po = Gtk.PopoverMenu()
        self.right_click_menu_po.set_menu_model(right_click_menu_model)
        #self.right_click_menu_po.set_parent(self.treeview)
        self.right_click_menu_po.set_parent(MainWindow.main_window)
        self.right_click_menu_po.set_position(Gtk.PositionType.BOTTOM)
        self.right_click_menu_po.set_has_arrow(False)


    def on_details_item_clicked(self, action, parameter):
        """
        Show process details window.
        """

        from UsersDetails import UsersDetails
        UsersDetails.user_details_window.show()


    def on_searchentry_changed(self, widget):
        """
        Called by searchentry when text is changed.
        """

        user_search_text = self.searchentry.get_text().lower()

        # Set visible/hidden users
        for piter in self.piter_list:
            self.treestore.set_value(piter, 0, False)
            user_data_text_in_model = self.treestore.get_value(piter, self.filter_column)
            if user_search_text in str(user_data_text_in_model).lower():
                self.treestore.set_value(piter, 0, True)


    def on_treeview_pressed(self, event, count, x, y):
        """
        Mouse single right click and double left click events (button press).
        Right click menu is opened when right clicked. Details window is shown when double clicked.
        """

        # Convert coordinates for getting path.
        x_bin, y_bin = self.treeview.convert_widget_to_bin_window_coords(x,y)

        # Get right/double clicked row data
        try:
            path, _, _, _ = self.treeview.get_path_at_pos(int(x_bin), int(y_bin))
        # Prevent errors when right clicked on an empty area on the treeview.
        except TypeError:
            return
        model = self.treeview.get_model()
        treeiter = model.get_iter(path)

        # Get right/double clicked user UID and user name
        if treeiter == None:
            return
        global selected_user_uid, selected_username
        try:
            selected_uid_username = self.uid_username_list[self.users_data_rows.index(model[treeiter][:])]
            self.selected_user_uid = selected_uid_username[0]
            self.selected_username = selected_uid_username[1]
        except ValueError:
            return

        # Show right click menu if right clicked on a row
        if int(event.get_button()) == 3:
            rectangle = Gdk.Rectangle()
            rectangle.x = int(x)
            rectangle.y = int(y)
            rectangle.width = 1
            rectangle.height = 1
            # Convert teeview coordinates to window coordinates. Because popovermenu is set for window instead of treeview.
            treeview_x_coord, treeview_y_coord = self.treeview.translate_coordinates(MainWindow.main_window,0,0)
            rectangle.x = rectangle.x + treeview_x_coord
            rectangle.y = rectangle.y + treeview_y_coord

            # New coordinates have to be set for popovermenu on every popup.
            self.right_click_menu_po.set_pointing_to(rectangle)
            self.right_click_menu_po.popup()

        # Show details window if double clicked on a row
        if int(event.get_button()) == 1 and int(count) == 2:
            from UsersDetails import UsersDetails
            UsersDetails.user_details_window.show()


    def on_treeview_released(self, event, count, x, y):
        """
        Mouse single left click event (button release).
        Update teeview column/row width/sorting/order.
        """

        # Check if left mouse button is used
        if int(event.get_button()) == 1:
            self.treeview_column_order_width_row_sorting()


    def users_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        global users_data_list
        users_data_list = [
                          [0, _tr('User'), 3, 2, 3, [bool, str, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'icon_name', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
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


        global number_of_clock_ticks, system_boot_time

        number_of_clock_ticks = os.sysconf("SC_CLK_TCK")                                          # For many systems CPU ticks 100 times in a second. Wall clock time could be get if CPU times are multiplied with this value or vice versa.

        # Get system boot time which will be used for obtaining user process start time
        with open("/proc/stat") as reader:
            stat_lines = reader.read().split("\n")
        for line in stat_lines:
            if "btime " in line:
                system_boot_time = int(line.split()[1].strip())

        self.filter_column = users_data_list[0][2] - 1                                                 # Search filter is "Process Name". "-1" is used because "processes_data_list" has internal column count and it has to be converted to Python index. For example, if there are 3 internal columns but index is 2 for the last internal column number for the relevant treeview column.

        self.number_of_clock_ticks = number_of_clock_ticks
        self.system_boot_time = system_boot_time

        self.initial_already_run = 1


    def users_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        # Get GUI obejcts one time per floop instead of getting them multiple times
        global users_treeview

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
        global users_data_rows, users_data_rows_prev, global_process_cpu_times_prev, pid_list, pid_list_prev, uid_username_list_prev, uid_username_list
        users_data_rows = []
        global_process_cpu_times = []
        uid_username_list = []                                                                    # For tracking new/removed user data rows. User UID and username information is appended per user. Because tracking only user UID and username may cause confusions. User UID may be given another user after a time if a user is deleted.

        # Get number of online logical CPU cores (this operation is repeated in every loop because number of online CPU cores may be changed by user and this may cause wrong calculation of CPU usage percent data of the processes even if this is a very rare situation.)
        number_of_logical_cores = Common.number_of_logical_cores()

        # Get all users and user groups.
        etc_passwd_lines, user_group_names, user_group_ids = self.users_groups_func()

        # Get all user process PIDs and elapsed times (seconds) since they are started.
        command_list = ["ps", "--no-headers", "-eo", "pid,etimes,user"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        ps_output_lines = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")

        # Get user process PIDs, logged in users and user start times.
        pid_list = []
        user_processes_start_times = []
        logged_in_users_list = []
        for line in ps_output_lines:
            line_split = line.split()
            pid_list.append(line_split[0])
            user_processes_start_times.append(int(line_split[1]))
            logged_in_users_list.append(line_split[-1])

        # Get CPU usage percent of all processes
        if 10 in users_treeview_columns_shown:
            command_list = ["cat"]
            if Config.environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list
            for pid in pid_list:
                command_list.append("/proc/" + pid + "/stat")
            cat_output_lines = (subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)).stdout.decode().strip().split("\n")
            global_cpu_time_all = time.time() * number_of_clock_ticks                             # global_cpu_time_all value is get just after "/proc/[PID]/stat file is get in order to measure global an process specific CPU times at the same time (nearly) for ensuring accurate process CPU usage percent.
            all_process_cpu_usages = []
            pid_list_from_stat = []
            for line in cat_output_lines:
                line_split = line.split()
                process_pid = line_split[0]
                pid_list_from_stat.append(process_pid)
                process_cpu_time = int(line_split[-39]) + int(line_split[-38])                    # Get process cpu time in user mode (utime + stime)
                global_process_cpu_times.append((global_cpu_time_all, process_cpu_time))          # While appending multiple elements into a list "append((value1, value2))" is faster than "append([value1, value2])".
                try:                                                                              # It gives various errors (ValueError, IndexError, UnboundLocalError) if a new process is started, a new column is shown on the treeview, etc because previous CPU time values are not present in these situations. Following CPU time values are use in these situations.
                    global_cpu_time_all_prev, process_cpu_time_prev = global_process_cpu_times_prev[pid_list_prev.index(process_pid)]
                except (ValueError, IndexError, UnboundLocalError) as me:
                    process_cpu_time_prev = process_cpu_time                                      # There is no "process_cpu_time_prev" value and get it from "process_cpu_time"  if this is first loop of the process
                    global_cpu_time_all_prev = global_process_cpu_times[-1][0] - 1                # Subtract "1" CPU time (a negligible value) if this is first loop of the process
                process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
                global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
                all_process_cpu_usages.append(process_cpu_time_difference / global_cpu_time_difference * 100 / number_of_logical_cores)
            for pid in pid_list[:]:
                index_to_remove = pid_list.index(pid)
                if pid not in pid_list_from_stat:
                    del pid_list[index_to_remove]
                    del user_processes_start_times[index_to_remove]
                    del logged_in_users_list[index_to_remove]
                continue

        # Get only logged in human user list.
        user_logged_in_list = []
        for line in etc_passwd_lines:
            line_split = line.split(":")
            username = line_split[0]
            user_uid = line_split[2]
            user_uid_int = int(user_uid)
            if user_uid_int >= 1000 and user_uid_int != 65534:
                if username in logged_in_users_list:
                    user_logged_in_list.append(username)

        # Get and append data per user.
        for line in etc_passwd_lines:
            line_split = line.split(":")
            username = line_split[0]
            user_uid = line_split[2]
            user_gid = line_split[3]
            user_uid_int = int(user_uid)
            if user_uid_int >= 1000 and user_uid_int != 65534:                                    # Human users have UID bigger than 999 (1000 =< UID) and lower than 65534. 
                uid_username_list.append([int(user_uid), username])                               # "user_uid" have to be appended as integer because sorting list of multiple elemented sub-list operation will be performed. "sorted(a_list, key=int)" could not be used in this situation.            
                # Append row visibility data, username (username has been get previously) and image
                users_data_row = [True, "system-monitoring-center-user-symbolic", username]                             # User data row visibility data (True/False) is always appended into the list. True is an initial value and it is modified later.
                # Get user full name
                if 1 in users_treeview_columns_shown:
                    user_full_name = line_split[4]
                    users_data_row.append(user_full_name)
                # Get user logged in data (User logged in data has been get previously)
                if 2 in users_treeview_columns_shown:
                    if username in user_logged_in_list:
                        users_data_row.append(True)
                    else:
                        users_data_row.append(False)
                # Get user UID (UID value has been get previously)
                if 3 in users_treeview_columns_shown:
                    users_data_row.append(int(user_uid))
                # Get user GID
                if 4 in users_treeview_columns_shown:
                    users_data_row.append(int(user_gid))
                # Get user process count
                if 5 in users_treeview_columns_shown:
                    user_process_count = logged_in_users_list.count(username)
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
                    curent_user_process_start_time_list = []
                    for pid in pid_list:
                        if logged_in_users_list[pid_list.index(pid)] == username:
                            curent_user_process_start_time_list.append(user_processes_start_times[pid_list.index(pid)])
                    if curent_user_process_start_time_list == []:
                        user_process_start_time = 0
                    else:
                        user_process_start_time = time.time() - max(curent_user_process_start_time_list)
                    users_data_row.append(user_process_start_time)
                # Get user processes CPU usage percentages
                if 10 in users_treeview_columns_shown:
                    user_users_cpu_percent = 0
                    for pid in pid_list:
                        if logged_in_users_list[pid_list.index(pid)] == username:
                            user_users_cpu_percent = user_users_cpu_percent + all_process_cpu_usages[pid_list.index(pid)]
                    users_data_row.append(user_users_cpu_percent)
                # Append all data of the users into a list which will be appended into a treestore for showing the data on a treeview.
                users_data_rows.append(users_data_row)
        pid_list_prev = pid_list                                                                  # For using values in the next loop
        global_process_cpu_times_prev = global_process_cpu_times                                  # For using values in the next loop

        # Add/Remove treeview columns appropriate for user preferences
        if users_treeview_columns_shown != users_treeview_columns_shown_prev:                     # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
            cumulative_sort_column_id = -1
            cumulative_internal_data_id = -1
            for column in self.treeview.get_columns():                                           # Remove all columns in the treeview.
                self.treeview.remove_column(column)
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
                users_treeview_column.set_sizing(2)                                               # Set column sizing (2 = auto sizing which is required for "self.treeview.set_fixed_height_mode(True)" command that is used for lower treeview CPU consumption because row heights are not calculated for every row).
                users_treeview_column.set_sort_column_id(cumulative_sort_column_id)               # Be careful with lists contain same element more than one.
                users_treeview_column.set_resizable(True)                                         # Set columns resizable by the user when column title button edge handles are dragged.
                users_treeview_column.set_reorderable(True)                                       # Set columns reorderable by the user when column title buttons are dragged.
                users_treeview_column.set_min_width(50)                                           # Set minimum column widths as "50 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
                users_treeview_column.connect("clicked", self.on_column_title_clicked)            # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
                self.treeview.append_column(users_treeview_column)                                # Append column into treeview

            # Get column data types for appending users data into treestore
            users_data_column_types = []
            for column in sorted(users_treeview_columns_shown):
                internal_column_count = len(users_data_list[column][5])
                for internal_column_number in range(internal_column_count):
                    users_data_column_types.append(users_data_list[column][5][internal_column_number])    # Get column types (int, bool, float, str, etc.)

            # Define a treestore (for storing treeview data in it), a treemodelfilter (for search filtering), treemodelsort (for row sorting when column title buttons are clicked)
            self.treestore = Gtk.TreeStore()
            self.treestore.set_column_types(users_data_column_types)                               # Set column types of the columns which will be appended into treestore
            treemodelfilter3101 = self.treestore.filter_new()
            treemodelfilter3101.set_visible_column(0)                                             # Column "0" of the treestore will be used for column visibility information (True or False)
            treemodelsort3101 = Gtk.TreeModelSort().new_with_model(treemodelfilter3101)
            self.treeview.set_model(treemodelsort3101)
            pid_list_prev = []                                                                    # Redefine (clear) "pid_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
            uid_username_list_prev = []                                                           # Redefine (clear) "uid_username_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
            self.piter_list = []

        # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
        if users_treeview_columns_shown_prev != users_treeview_columns_shown or users_data_column_order_prev != users_data_column_order:
            users_treeview_columns = self.treeview.get_columns()                                   # Get shown columns on the treeview in order to use this data for reordering the columns.
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
                    self.treeview.move_column_after(column_to_move, None)                          # Column is moved at the beginning of the treeview if "None" is used.

        # Sort user rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
        if users_treeview_columns_shown_prev != users_treeview_columns_shown or users_data_row_sorting_column_prev != users_data_row_sorting_column or users_data_row_sorting_order != users_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
            users_treeview_columns = self.treeview.get_columns()                                   # Get shown columns on the treeview in order to use this data for reordering the columns.
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
            users_treeview_columns = self.treeview.get_columns()
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
        global user_search_text
        if len(self.piter_list) > 0:
            for i, j in updated_existing_user_index:
                if users_data_rows[i] != users_data_rows_prev[j]:
                    for k in range(1, users_data_rows_row_length):                                 # Start from "1" in order to set first element (treeview row visibility data) as "True" in every loop.
                        if users_data_rows_prev[j][k] != users_data_rows[i][k]:
                            self.treestore.set_value(self.piter_list[j], k, users_data_rows[i][k])
        if len(deleted_users) > 0:
            for user in reversed(sorted(list(deleted_users))):
                self.treestore.remove(self.piter_list[uid_username_list_prev.index(list(user))])        # ".index(list(user))" have to used with "list()" because it was converted into "set". This behavior is valid for list of multiple elemented sub-lists.
                self.piter_list.remove(self.piter_list[uid_username_list_prev.index(list(user))])
            self.on_searchentry_changed(self.searchentry)                                          # Update search results.
        if len(new_users) > 0:
            for i, user in enumerate(new_users):
                self.piter_list.append(self.treestore.append(None, users_data_rows[uid_username_list.index(list(user))]))
            self.on_searchentry_changed(self.searchentry)                                          # Update search results.

        uid_username_list_prev = uid_username_list
        users_data_rows_prev = users_data_rows
        users_treeview_columns_shown_prev = users_treeview_columns_shown
        users_data_row_sorting_column_prev = users_data_row_sorting_column
        users_data_row_sorting_order_prev = users_data_row_sorting_order
        users_data_column_order_prev = users_data_column_order
        users_data_column_widths_prev = users_data_column_widths

        self.users_data_rows = users_data_rows
        self.uid_username_list = uid_username_list
        self.number_of_logical_cores = number_of_logical_cores

        # Show number of users on the searchentry as placeholder text
        self.searchentry.props.placeholder_text = _tr("Search...") + "                    " + "(" + _tr("Users") + ": " + str(len(uid_username_list)) + ")"


    def on_column_title_clicked(self, widget):
        """
        Get and save column sorting order.
        """

        users_data_row_sorting_column_title = widget.get_title()                                  # Get column title which will be used for getting column number
        for data in users_data_list:
            if data[1] == users_data_row_sorting_column_title:
                Config.users_data_row_sorting_column = data[0]                                    # Get column number
        Config.users_data_row_sorting_order = int(widget.get_sort_order())                        # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
        Config.config_save_func()


    def treeview_column_order_width_row_sorting(self):
        """
        Get and save column order/width, row sorting.
        """

        users_treeview_columns = self.treeview.get_columns()
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


    def users_groups_func(self):
        """
        Get users and user groups.
        """
        
        # Read all users
        if Config.environment_type == "flatpak":
            with open("/var/run/host/etc/passwd") as reader:
                etc_passwd_lines = reader.read().strip().split("\n")
        else:
            with open("/etc/passwd") as reader:
                etc_passwd_lines = reader.read().strip().split("\n")

        # Read all user groups
        if Config.environment_type == "flatpak":
            with open("/var/run/host/etc/group") as reader:
                etc_group_lines = reader.read().strip().split("\n")
        else:
            with open("/etc/group") as reader:
                etc_group_lines = reader.read().strip().split("\n")

        user_group_names = []
        user_group_ids = []
        for line in etc_group_lines:
            line_split = line.split(":")
            user_group_names.append(line_split[0])
            user_group_ids.append(line_split[2])

        return etc_passwd_lines, user_group_names, user_group_ids


# ----------------------------------- Users - Treeview Cell Functions (defines functions for treeview cell for setting data precisions and/or data units) -----------------------------------
def cell_data_function_cpu_usage_percent(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{tree_model.get(iter, data)[0]:.{users_cpu_precision}f} %')

def cell_data_function_started(tree_column, cell, tree_model, iter, data):
    cell_data = tree_model.get(iter, data)[0]
    if cell_data != 0:
        cell.set_property('text', datetime.fromtimestamp(tree_model.get(iter, data)[0]).strftime("%H:%M:%S %d.%m.%Y"))
    if cell_data == 0:
        cell.set_property('text', "-")


Users = Users()


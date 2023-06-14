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

from .Config import Config
from .MainWindow import MainWindow
from . import Common


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
        self.searchentry = Common.searchentry(self.on_searchentry_changed)
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

        # Treeview signals
        self.treeview.connect("columns-changed", Common.on_columns_changed)

        # Treeview mouse events.
        treeview_mouse_event = Gtk.GestureClick()
        treeview_mouse_event.connect("pressed", self.on_treeview_pressed)
        treeview_mouse_event.connect("released", self.on_treeview_released)
        self.treeview.add_controller(treeview_mouse_event)

        treeview_mouse_event_right_click = Gtk.GestureClick()
        treeview_mouse_event_right_click.set_button(3)
        treeview_mouse_event_right_click.connect("pressed", self.on_treeview_pressed)
        self.treeview.add_controller(treeview_mouse_event_right_click)

        # SeachEntry focus action and accelerator
        Common.searchentry_focus_action_and_accelerator(MainWindow)

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

        from .UsersDetails import UsersDetails
        UsersDetails.user_details_window.set_visible(True)


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
        try:
            row_index = self.users_data_rows.index(model[treeiter][:])
            self.selected_user_uid = self.human_user_uid_list[row_index]
            self.selected_username = self.users_data_rows[row_index][2]
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
            from .UsersDetails import UsersDetails
            UsersDetails.user_details_window.set_visible(True)


    def on_treeview_released(self, event, count, x, y):
        """
        Mouse single left click event (button release).
        Update teeview column/row width/sorting/order.
        """

        # Check if left mouse button is used
        if int(event.get_button()) == 1:
            pass


    def users_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        global row_data_list
        row_data_list = [
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

        self.row_data_list = row_data_list

        global users_data_rows_prev
        global human_user_uid_list_prev
        users_data_rows_prev = []
        human_user_uid_list_prev = []
        self.treeview_columns_shown_prev = []
        self.data_row_sorting_column_prev = ""
        self.data_row_sorting_order_prev = ""
        self.data_column_order_prev = []
        self.data_column_widths_prev = []

        self.users_data_dict_prev = {}

        self.system_boot_time = Common.get_system_boot_time()

        self.filter_column = row_data_list[0][2] - 1

        self.initial_already_run = 1


    def users_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        global users_cpu_precision
        users_cpu_precision = Config.users_cpu_precision

        # Define global variables and get treeview columns, sort column/order, column widths, etc.
        global treeview_columns_shown
        treeview_columns_shown = Config.users_treeview_columns_shown
        self.data_row_sorting_column = Config.users_data_row_sorting_column
        self.data_row_sorting_order = Config.users_data_row_sorting_order
        self.data_column_order = Config.users_data_column_order
        self.data_column_widths = Config.users_data_column_widths
        self.treeview_columns_shown = treeview_columns_shown

        # Define global variables and empty lists for the current loop
        global users_data_rows, users_data_rows_prev, human_user_uid_list_prev, human_user_uid_list
        users_data_rows = []

        # Get user information
        users_data_dict = Common.users_information(self.users_data_dict_prev, self.system_boot_time)
        self.users_data_dict_prev = dict(users_data_dict)
        human_user_uid_list = users_data_dict["human_user_uid_list"]

        # Get and append user data
        for uid in human_user_uid_list:
            user_data_dict = users_data_dict[uid]
            username = user_data_dict["username"]
            users_data_row = [True, "system-monitoring-center-user-symbolic", username]
            if 1 in treeview_columns_shown:
                users_data_row.append(user_data_dict["full_name"])
            if 2 in treeview_columns_shown:
                users_data_row.append(user_data_dict["logged_in"])
            if 3 in treeview_columns_shown:
                users_data_row.append(uid)
            if 4 in treeview_columns_shown:
                users_data_row.append(user_data_dict["gid"])
            if 5 in treeview_columns_shown:
                users_data_row.append(user_data_dict["process_count"])
            if 6 in treeview_columns_shown:
                users_data_row.append(user_data_dict["home_dir"])
            if 7 in treeview_columns_shown:
                users_data_row.append(user_data_dict["group_name"])
            if 8 in treeview_columns_shown:
                users_data_row.append(user_data_dict["terminal"])
            if 9 in treeview_columns_shown:
                users_data_row.append(user_data_dict["log_in_time"])
            if 10 in treeview_columns_shown:
                users_data_row.append(user_data_dict["total_cpu_usage"])

            # Append user data into a list
            users_data_rows.append(users_data_row)

        reset_row_unique_data_list_prev = Common.treeview_add_remove_columns()
        if reset_row_unique_data_list_prev == "yes":
            human_user_uid_list_prev = []
        Common.treeview_reorder_columns_sort_rows_set_column_widths()

        # Get new/deleted(ended) users for updating treestore/treeview
        human_user_uid_list_prev_set = set(human_user_uid_list_prev)
        human_user_uid_list_set = set(human_user_uid_list)
        deleted_users = sorted(list(human_user_uid_list_prev_set - human_user_uid_list_set))
        new_users = sorted(list(human_user_uid_list_set - human_user_uid_list_prev_set))
        existing_users = sorted(list(human_user_uid_list_set.intersection(human_user_uid_list_prev_set)))
        updated_existing_user_index = [[human_user_uid_list.index(i), human_user_uid_list_prev.index(i)] for i in existing_users]
        try:
            users_data_rows_row_length = len(users_data_rows[0])
        # Prevent errors if there is no user account on the system. An user account may not be found on an OS if the OS is run without installation.
        except IndexError:
            return
        # Append/Remove/Update users data to treestore
        global user_search_text
        if len(self.piter_list) > 0:
            for i, j in updated_existing_user_index:
                if users_data_rows[i] != users_data_rows_prev[j]:
                    for k in range(1, users_data_rows_row_length):                                 # Start from "1" in order to set first element (treeview row visibility data) as "True" in every loop.
                        if users_data_rows_prev[j][k] != users_data_rows[i][k]:
                            self.treestore.set_value(self.piter_list[j], k, users_data_rows[i][k])
        if len(deleted_users) > 0:
            for user in reversed(sorted(list(deleted_users))):
                self.treestore.remove(self.piter_list[human_user_uid_list_prev.index(user)])
                self.piter_list.remove(self.piter_list[human_user_uid_list_prev.index(user)])
            self.on_searchentry_changed(self.searchentry)                                          # Update search results.
        if len(new_users) > 0:
            for i, user in enumerate(new_users):
                self.piter_list.append(self.treestore.append(None, users_data_rows[human_user_uid_list.index(user)]))
            self.on_searchentry_changed(self.searchentry)                                          # Update search results.

        human_user_uid_list_prev = human_user_uid_list
        users_data_rows_prev = users_data_rows
        self.treeview_columns_shown_prev = treeview_columns_shown
        self.data_row_sorting_column_prev = self.data_row_sorting_column
        self.data_row_sorting_order_prev = self.data_row_sorting_order
        self.data_column_order_prev = self.data_column_order
        self.data_column_widths_prev = self.data_column_widths

        self.users_data_rows = users_data_rows
        self.human_user_uid_list = human_user_uid_list

        # Show number of users on the searchentry as placeholder text
        self.searchentry.props.placeholder_text = _tr("Search...") + "                    " + "(" + _tr("Users") + ": " + str(len(human_user_uid_list)) + ")"


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


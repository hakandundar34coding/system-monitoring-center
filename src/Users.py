import tkinter as tk
from tkinter import ttk

import os
import time
import subprocess
from datetime import datetime

from .Config import Config
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class Users:

    def __init__(self):

        self.name = "Users"

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_frame = ttk.Frame(MainWindow.users_tab_main_frame)
        self.tab_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.tab_frame.columnconfigure(0, weight=1)
        self.tab_frame.rowconfigure(1, weight=1)

        self.tab_title_frame()

        self.information_frame()

        self.gui_signals()

        self.right_click_menu_gui()


    def tab_title_frame(self):
        """
        Generate tab name label, searchentry.
        """

        # Grid (tab title)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=0, column=0, sticky="new", padx=0, pady=(0, 10))
        frame.columnconfigure(1, weight=1)

        # Label (Users)
        label = Common.tab_title_label(frame, _tr("Users"))

        # Grid (search widgets)
        search_frame = ttk.Frame(frame)
        search_frame.columnconfigure(0, weight=1)
        search_frame.grid(row=0, column=1, sticky="ew", padx=0, pady=0)

        # SearchEntry
        self.searchentry, self.searchentry_text_var = Common.searchentry(search_frame, self)
        self.searchentry.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)


    def information_frame(self):
        """
        Generate information GUI objects.
        """

        # TreeView
        self.treeview, frame = Common.treeview(self.tab_frame, self)


    def gui_signals(self):
        """
        Connect GUI signals.
        """
        return


    def right_click_menu_gui(self):
        """
        Generate right click menu GUI.
        """

        self.right_click_menu = tk.Menu(self.treeview, tearoff=False, bd=3, activebackground="gray")
        self.right_click_menu.add_command(label=_tr("Details"), accelerator="(Enter)", command=self.on_details_item_activate)

        self.right_click_menu.bind("<FocusOut>", self.right_click_menu_close)

        self.treeview.bind("<Button-3>", self.on_right_click)
        self.treeview.bind("<Double-1>", self.treeview_double_click_event)
        # Treeview "FocusOut" signal may not close right click menu if certain areas of the GUI is clicked. The following signal is used for fixing this issue.
        self.treeview.winfo_toplevel().bind("<Button-1>", self.right_click_menu_close)


    def get_selection(self, event):

        self.selected_row_id = self.treeview.identify_row(event.y)
        # Get right clicked row id.
        if self.selected_row_id:
            # Select the row visually if right clicked on a row.
            self.treeview.selection_set(self.selected_row_id)
            # Get data of the selected row.
            self.selected_row_name = self.treeview.item(self.selected_row_id, "text")

        return self.selected_row_name


    def on_right_click(self, event):

        self.get_selection(event)
        # Show menu on mouse coordinates
        self.right_click_menu.post(event.x_root, event.y_root)
        self.right_click_menu.focus_set()


    def right_click_menu_close(self, event):
        """
        Close right click menu if clicked another part of the GUI.
        """

        self.right_click_menu.unpost()


    def on_details_item_activate(self):
        """
        Show process details window.
        """

        from .UsersDetails import UsersDetails
        UsersDetails.window_gui()


    def treeview_double_click_event(self, event):

        region = self.treeview.identify_region(event.x, event.y)
        # Prevent running code if rows are not clicked.
        if region in ["cell", "tree"]:
            self.selected_row_name = self.get_selection(event)
            from .UsersDetails import UsersDetails
            UsersDetails.window_gui()


    def on_searchentry_changed(self, widget):
        """
        Called by searchentry when text is changed.
        """

        self.filter.changed(Gtk.FilterChange.DIFFERENT)


    def search_function(self, item, user_data):
        search_text = self.searchentry.get_text().lower()
        if not search_text:
            return True
        return search_text in item.user_name.lower()


    def on_sorter_changed(self, sorter, change):
        """
        Save sorting column and sorting order if they are changed.
        """

        # Prevent error if sorting column is removed from ColumnView.
        if sorter.get_primary_sort_column() != None:
            Config.users_row_sorting_column = sorter.get_primary_sort_column().get_id()
            Config.users_row_sorting_order = int(sorter.get_primary_sort_order())
            Config.config_save_func()


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.column_dict = {"user_name": {"column_title": _tr("User"), "column_type": str, "converted_data": "no"},
                            "full_name": {"column_title": _tr("Full Name"), "column_type": str, "converted_data": "no"},
                            "logged_in": {"column_title": _tr("Logged In"), "column_type": str, "converted_data": "no"},
                            "uid": {"column_title": _tr("UID"), "column_type": int, "converted_data": "no"},
                            "gid": {"column_title": _tr("GID"), "column_type": int, "converted_data": "no"},
                            "process_count": {"column_title": _tr("Processes"), "column_type": int, "converted_data": "no"},
                            "home_directory": {"column_title": _tr("Home Directory"), "column_type": str, "converted_data": "no"},
                            "group_name": {"column_title": _tr("Group"), "column_type": str, "converted_data": "no"},
                            "terminal": {"column_title": _tr("Terminal"), "column_type": str, "converted_data": "no"},
                            "log_in_time": {"column_title": _tr("Start Time"), "column_type": float, "converted_data": "yes"},
                            "cpu_usage": {"column_title": _tr("CPU"), "column_type": int, "converted_data": "yes"},
                            }

        self.piter_dict = {}
        self.selected_data_rows_prev = {}
        self.rows_data_dict_prev = {}
        self.row_id_list_prev = []
        self.image_dict = {}
        self.treeview_columns_shown_prev = []
        self.system_boot_time = Libsysmon.get_system_boot_time()
        self.rows_additional_data_dict_prev = {}

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        global users_cpu_precision
        users_cpu_precision = Config.users_cpu_precision

        try:
            self.treeview_columns_shown_prev = list(self.treeview_columns_shown)
            self.row_sorting_column_prev = self.row_sorting_column
            self.row_sorting_order_prev = self.row_sorting_order
        except AttributeError:
            self.treeview_columns_shown_prev = []
            self.row_sorting_column_prev = 0
            self.row_sorting_order_prev = 0

        # Define global variables and get treeview columns, sort column/order, column widths, etc.
        self.treeview_columns_shown = Config.users_columns_shown
        self.row_sorting_column = Config.users_row_sorting_column
        self.row_sorting_order = Config.users_row_sorting_order

        username_uid_dict = {}
        rows_data_dict, rows_additional_data_dict = Libsysmon.get_users_information(self.rows_data_dict_prev, self.system_boot_time, username_uid_dict, self.rows_additional_data_dict_prev)
        self.row_id_list = list(rows_data_dict.keys())

        Common.add_columns_and_reset_rows_and_columns(self)

        user_image = tk.PhotoImage(file=MainWindow.image_path + "smc-user.png").subsample(3, 3)

        selected_data_rows_raw = {}
        selected_data_rows = {}
        for user_name in self.row_id_list:
            row_data_dict = rows_data_dict[user_name]
            if user_name not in self.image_dict:
                self.image_dict[user_name] = user_image
            selected_data_row_raw = []
            selected_data_row = []
            for column_shown in self.treeview_columns_shown:
                if column_shown == "user_name":
                    selected_data_row.append(row_data_dict["user_name"])
                    selected_data_row_raw.append(row_data_dict["user_name"])
                if column_shown == "full_name":
                    selected_data_row.append(row_data_dict["full_name"])
                    selected_data_row_raw.append(row_data_dict["full_name"])
                if column_shown == "logged_in":
                    selected_data_row.append(row_data_dict["logged_in"])
                    selected_data_row_raw.append(row_data_dict["logged_in"])
                if column_shown == "uid":
                    selected_data_row.append(row_data_dict["uid"])
                    selected_data_row_raw.append(row_data_dict["uid"])
                if column_shown == "gid":
                    selected_data_row.append(row_data_dict["gid"])
                    selected_data_row_raw.append(row_data_dict["gid"])
                if column_shown == "process_count":
                    selected_data_row.append(row_data_dict["process_count"])
                    selected_data_row_raw.append(row_data_dict["process_count"])
                if column_shown == "home_directory":
                    selected_data_row.append(row_data_dict["home_directory"])
                    selected_data_row_raw.append(row_data_dict["home_directory"])
                if column_shown == "group_name":
                    selected_data_row.append(row_data_dict["group_name"])
                    selected_data_row_raw.append(row_data_dict["group_name"])
                if column_shown == "terminal":
                    selected_data_row.append(row_data_dict["terminal"])
                    selected_data_row_raw.append(row_data_dict["terminal"])
                if column_shown == "log_in_time":
                    if row_data_dict["log_in_time"] != 0:
                        converted_data = datetime.fromtimestamp(row_data_dict["log_in_time"]).strftime("%H:%M:%S %d.%m.%Y")
                    if row_data_dict["log_in_time"] == 0:
                        converted_data = "-"
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["log_in_time"])
                if column_shown == "cpu_usage":
                    selected_data_row.append(f'{row_data_dict["cpu_usage"]:.{users_cpu_precision}f} %')
                    selected_data_row_raw.append(row_data_dict["cpu_usage"])

            selected_data_rows[user_name] = selected_data_row
            selected_data_rows_raw[user_name] = selected_data_row_raw

        new_rows, deleted_rows, existing_rows = Common.get_new_removed_updated_rows(self.row_id_list, self.row_id_list_prev)

        self.piter_dict = Common.add_remove_update_treeview_rows(self.treeview, self.piter_dict, self.selected_data_rows_prev, self.image_dict, selected_data_rows, selected_data_rows_raw, new_rows, deleted_rows, existing_rows)

        self.row_count = len(self.row_id_list)
        self.row_information = _tr("Users")
        self.selected_data_rows = selected_data_rows
        Common.searchentry_placeholder_text(self)

        self.rows_data_dict_prev = dict(rows_data_dict)
        self.row_id_list_prev = self.row_id_list
        self.selected_data_rows_prev = self.selected_data_rows

        self.rows_additional_data_dict_prev = dict(rows_additional_data_dict)

        Common.sort_columns_on_every_loop(self)


Users = Users()


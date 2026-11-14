import tkinter as tk
from tkinter import ttk

import os
import time
import subprocess
from datetime import datetime

from .Config import Config
from .Users import Users
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class UsersDetails:

    def __init__(self):

        #self.window_gui()
        pass


    def window_gui(self):
        """
        Generate window GUI.
        """

        # Window (User Details)
        self.user_details_window, frame = Common.window(MainWindow.main_window, _tr("User Details"))

        # Frame (main)
        self.main_frame = ttk.Frame(frame)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.main_tab_gui()

        self.gui_signals()


    def main_tab_gui(self):
        """
        Generate labels on the main (single) tab.
        """

        # Label (User)
        label = Common.static_information_label(self.main_frame, text=_tr("User"))
        label.grid(row=0, column=0, sticky="nsew", padx=0, pady=4)
        # Label (User)
        label = Common.static_information_label(self.main_frame, text=":")
        label.grid(row=0, column=1, sticky="nsew", padx=5, pady=4)
        # Label (User)
        self.user_label = Common.dynamic_information_label(self.main_frame)
        self.user_label.grid(row=0, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Full Name)
        label = Common.static_information_label(self.main_frame, text=_tr("Full Name"))
        label.grid(row=1, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Full Name)
        label = Common.static_information_label(self.main_frame, text=":")
        label.grid(row=1, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Full Name)
        self.full_name_label = Common.dynamic_information_label(self.main_frame)
        self.full_name_label.grid(row=1, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Logged In)
        label = Common.static_information_label(self.main_frame, text=_tr("Logged In"))
        label.grid(row=2, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Logged In)
        label = Common.static_information_label(self.main_frame, text=":")
        label.grid(row=2, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Logged In)
        self.logged_in_label = Common.dynamic_information_label(self.main_frame)
        self.logged_in_label.grid(row=2, column=2, sticky="nsew", padx=0, pady=4)

        # Label (UID)
        label = Common.static_information_label(self.main_frame, text=_tr("UID"))
        label.grid(row=3, column=0, sticky="nsew", padx=0, pady=4)
        # Label (UID)
        label = Common.static_information_label(self.main_frame, text=":")
        label.grid(row=3, column=1, sticky="nsew", padx=5, pady=4)
        # Label (UID)
        self.uid_label = Common.dynamic_information_label(self.main_frame)
        self.uid_label.grid(row=3, column=2, sticky="nsew", padx=0, pady=4)

        # Label (GID)
        label = Common.static_information_label(self.main_frame, text=_tr("GID"))
        label.grid(row=4, column=0, sticky="nsew", padx=0, pady=4)
        # Label (GID)
        label = Common.static_information_label(self.main_frame, text=":")
        label.grid(row=4, column=1, sticky="nsew", padx=5, pady=4)
        # Label (GID)
        self.gid_label = Common.dynamic_information_label(self.main_frame)
        self.gid_label.grid(row=4, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Processes)
        label = Common.static_information_label(self.main_frame, text=_tr("Processes"))
        label.grid(row=5, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Processes)
        label = Common.static_information_label(self.main_frame, text=":")
        label.grid(row=5, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Processes)
        self.processes_label = Common.dynamic_information_label(self.main_frame)
        self.processes_label.grid(row=5, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Home Directory)
        label = Common.static_information_label(self.main_frame, text=_tr("Home Directory"))
        label.grid(row=6, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Home Directory)
        label = Common.static_information_label(self.main_frame, text=":")
        label.grid(row=6, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Home Directory)
        self.home_directory_label = Common.dynamic_information_label(self.main_frame)
        self.home_directory_label.grid(row=6, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Group)
        label = Common.static_information_label(self.main_frame, text=_tr("Group"))
        label.grid(row=7, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Group)
        label = Common.static_information_label(self.main_frame, text=":")
        label.grid(row=7, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Group)
        self.group_label = Common.dynamic_information_label(self.main_frame)
        self.group_label.grid(row=7, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Terminal)
        label = Common.static_information_label(self.main_frame, text=_tr("Terminal"))
        label.grid(row=8, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Terminal)
        label = Common.static_information_label(self.main_frame, text=":")
        label.grid(row=8, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Terminal)
        self.terminal_label = Common.dynamic_information_label(self.main_frame)
        self.terminal_label.grid(row=8, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Start Time)
        label = Common.static_information_label(self.main_frame, text=_tr("Start Time"))
        label.grid(row=9, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Start Time)
        label = Common.static_information_label(self.main_frame, text=":")
        label.grid(row=9, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Start Time)
        self.start_time_label = Common.dynamic_information_label(self.main_frame)
        self.start_time_label.grid(row=9, column=2, sticky="nsew", padx=0, pady=4)

        # Label (CPU)
        label = Common.static_information_label(self.main_frame, text=_tr("CPU"))
        label.grid(row=10, column=0, sticky="nsew", padx=0, pady=4)
        # Label (CPU)
        label = Common.static_information_label(self.main_frame, text=":")
        label.grid(row=10, column=1, sticky="nsew", padx=5, pady=4)
        # Label (CPU)
        self.cpu_label = Common.dynamic_information_label(self.main_frame)
        self.cpu_label.grid(row=10, column=2, sticky="nsew", padx=0, pady=4)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        self.user_details_window.after(1, self.on_details_window_show)


    def on_details_window_delete_event(self, widget):
        """
        Called when window is closed.
        """

        self.update_window_value = 0
        self.user_details_window.set_visible(False)
        return True


    def on_details_window_show(self):
        """
        Run code after window is shown.
        """

        try:
            # Delete "update_interval" variable in order to let the code to run initial function.
            # Otherwise, data from previous user (if it was viewed) will be used.
            del self.update_interval
        except AttributeError:
            pass

        # This value is checked for repeating the function for getting the user data.
        self.update_window_value = 1

        self.details_run_func()


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.update_interval = Config.update_interval

        self.rows_data_dict_prev = {}
        self.rows_additional_data_dict_prev = {}

        self.system_boot_time = Libsysmon.get_system_boot_time()

        self.uid_list_prev = []
        self.human_user_uid_list_prev = []
        self.processes_data_dict_prev = {}


    def details_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        # Get right clicked user user name
        selected_user_name = Users.selected_row_name

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        users_cpu_precision = Config.users_cpu_precision

        # Get user information
        username_uid_dict = {}
        rows_data_dict, rows_additional_data_dict = Libsysmon.get_users_information(self.rows_data_dict_prev, self.system_boot_time, username_uid_dict, self.rows_additional_data_dict_prev)
        #rows_data_dict, uid_list, human_user_uid_list, processes_data_dict = Libsysmon.get_users_information(self.rows_data_dict_prev, self.system_boot_time, username_uid_dict, self.uid_list_prev, self.human_user_uid_list_prev, self.processes_data_dict_prev)

        #row_data_dict = rows_data_dict[selected_user_name]

        uid_list = rows_additional_data_dict["uid_list"]
        human_user_uid_list = rows_additional_data_dict["human_user_uid_list"]
        processes_data_dict_prev = rows_additional_data_dict["processes_data_dict_prev"]
        processes_additional_data_dict_prev = rows_additional_data_dict["processes_additional_data_dict_prev"]

        try:
            row_data_dict = rows_data_dict[selected_user_name]
        # Prevent error if user account is deleted while its detail window is open.
        except KeyError:
            self.update_window_value = 0
            self.user_details_window.destroy()
            return

        # Set label text
        self.user_label.config(text=row_data_dict["user_name"])
        self.full_name_label.config(text=row_data_dict["full_name"])
        if row_data_dict["logged_in"] == True:
            selected_user_logged_in = _tr("Yes")
        else:
            selected_user_logged_in = _tr("No")
        self.logged_in_label.config(text=selected_user_logged_in)
        self.uid_label.config(text=str(row_data_dict["uid"]))
        self.gid_label.config(text=str(row_data_dict["gid"]))
        self.processes_label.config(text=str(row_data_dict["process_count"]))
        self.home_directory_label.config(text=row_data_dict["home_directory"])
        self.group_label.config(text=row_data_dict["group_name"])
        self.terminal_label.config(text=row_data_dict["terminal"])
        selected_user_process_start_time = row_data_dict["log_in_time"]
        if selected_user_process_start_time != 0:
            self.start_time_label.config(text=datetime.fromtimestamp(selected_user_process_start_time).strftime("%H:%M:%S %d.%m.%Y"))
        if selected_user_process_start_time == 0:
            self.start_time_label.config(text="-")
        self.cpu_label.config(text=f'{row_data_dict["cpu_usage"]:.{users_cpu_precision}f} %')

        self.rows_additional_data_dict_prev = dict(rows_additional_data_dict)
        self.rows_data_dict_prev = dict(rows_data_dict)
        self.uid_list_prev = list(uid_list)
        self.human_user_uid_list_prev = list(human_user_uid_list)
        #self.processes_data_dict_prev = dict(processes_data_dict)


    def details_run_func(self):
        """
        Run initial and loop functions of service details window.
        """

        if hasattr(UsersDetails, "update_interval") == False:
            self.initial_func()

        self.details_loop_func()

        self.user_details_window.after(int(Config.update_interval*1000), self.details_run_func)


UsersDetails = UsersDetails()


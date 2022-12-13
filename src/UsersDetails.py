#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

import os
import time
import subprocess
from datetime import datetime

from locale import gettext as _tr

from Config import Config
from Users import Users
from Performance import Performance
from MainWindow import MainWindow
import Common


class UsersDetails:

    def __init__(self):

        self.window_gui()


    def window_gui(self):
        """
        Generate window GUI.
        """

        # Window
        self.user_details_window = Gtk.Window()
        self.user_details_window.set_default_size(350, 330)
        self.user_details_window.set_title(_tr("User"))
        self.user_details_window.set_icon_name("system-monitoring-center")
        self.user_details_window.set_transient_for(MainWindow.main_window)
        self.user_details_window.set_modal(True)
        self.user_details_window.set_hide_on_close(True)

        self.main_tab_gui()

        self.gui_signals()


    def main_tab_gui(self):
        """
        Generate labels on the main (single) tab.
        """

        # ScrolledWindow
        scrolledwindow = Common.window_main_scrolledwindow()
        self.user_details_window.set_child(scrolledwindow)

        # Viewport
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Grid
        grid = Common.window_main_grid()
        scrolledwindow.set_child(grid)

        # Label (User)
        label = Common.static_information_label(_tr("User"))
        grid.attach(label, 0, 0, 1, 1)
        # Label (User)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 0, 1, 1)
        # Label (User)
        self.user_label = Common.dynamic_information_label()
        grid.attach(self.user_label, 2, 0, 1, 1)

        # Label (Full Name)
        label = Common.static_information_label(_tr("Full Name"))
        grid.attach(label, 0, 1, 1, 1)
        # Label (Full Name)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 1, 1, 1)
        # Label (Full Name)
        self.full_name_label = Common.dynamic_information_label()
        grid.attach(self.full_name_label, 2, 1, 1, 1)

        # Label (Logged In)
        label = Common.static_information_label(_tr("Logged In"))
        grid.attach(label, 0, 2, 1, 1)
        # Label (Logged In)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 2, 1, 1)
        # Label (Logged In)
        self.logged_in_label = Common.dynamic_information_label()
        grid.attach(self.logged_in_label, 2, 2, 1, 1)

        # Label (UID)
        label = Common.static_information_label(_tr("UID"))
        grid.attach(label, 0, 3, 1, 1)
        # Label (UID)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 3, 1, 1)
        # Label (UID)
        self.uid_label = Common.dynamic_information_label()
        grid.attach(self.uid_label, 2, 3, 1, 1)

        # Label (GID)
        label = Common.static_information_label(_tr("GID"))
        grid.attach(label, 0, 4, 1, 1)
        # Label (GID)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 4, 1, 1)
        # Label (GID)
        self.gid_label = Common.dynamic_information_label()
        grid.attach(self.gid_label, 2, 4, 1, 1)

        # Label (Processes)
        label = Common.static_information_label(_tr("Processes"))
        grid.attach(label, 0, 5, 1, 1)
        # Label (Processes)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 5, 1, 1)
        # Label (Processes)
        self.processes_label = Common.dynamic_information_label()
        grid.attach(self.processes_label, 2, 5, 1, 1)

        # Label (Home Directory)
        label = Common.static_information_label(_tr("Home Directory"))
        grid.attach(label, 0, 6, 1, 1)
        # Label (Home Directory)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 6, 1, 1)
        # Label (Home Directory)
        self.home_directory_label = Common.dynamic_information_label()
        grid.attach(self.home_directory_label, 2, 6, 1, 1)

        # Label (Group)
        label = Common.static_information_label(_tr("Group"))
        grid.attach(label, 0, 7, 1, 1)
        # Label (Group)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 7, 1, 1)
        # Label (Group)
        self.group_label = Common.dynamic_information_label()
        grid.attach(self.group_label, 2, 7, 1, 1)

        # Label (Terminal)
        label = Common.static_information_label(_tr("Terminal"))
        grid.attach(label, 0, 8, 1, 1)
        # Label (Terminal)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 8, 1, 1)
        # Label (Terminal)
        self.terminal_label = Common.dynamic_information_label()
        grid.attach(self.terminal_label, 2, 8, 1, 1)

        # Label (Start Time)
        label = Common.static_information_label(_tr("Start Time"))
        grid.attach(label, 0, 9, 1, 1)
        # Label (Start Time)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 9, 1, 1)
        # Label (Start Time)
        self.start_time_label = Common.dynamic_information_label()
        grid.attach(self.start_time_label, 2, 9, 1, 1)

        # Label (CPU)
        label = Common.static_information_label(_tr("CPU"))
        grid.attach(label, 0, 10, 1, 1)
        # Label (CPU)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 10, 1, 1)
        # Label (CPU)
        self.cpu_label = Common.dynamic_information_label()
        grid.attach(self.cpu_label, 2, 10, 1, 1)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # Window signals
        self.user_details_window.connect("close-request", self.on_user_details_window_delete_event)
        self.user_details_window.connect("show", self.on_user_details_window_show)


    def on_user_details_window_delete_event(self, widget):
        """
        Called when window is closed.
        """

        self.update_window_value = 0
        self.user_details_window.hide()
        return True


    def on_user_details_window_show(self, widget):
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

        self.users_details_run_func()


    def users_details_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.pid_list_prev = []
        self.global_process_cpu_times_prev = []

        self.system_boot_time = Users.system_boot_time
        self.number_of_clock_ticks = Users.number_of_clock_ticks


    def users_details_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        # Get right clicked user UID and username
        selected_user_uid = str(Users.selected_user_uid)
        selected_username = Users.selected_username

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        users_cpu_precision = Config.users_cpu_precision

        # Set window title
        self.user_details_window.set_title(_tr("User") + ": " + selected_username)

        # Define empty lists for the current loop
        global_process_cpu_times = []

        # Get all users and user groups.
        etc_passwd_lines, user_group_names, user_group_ids = Users.users_groups_func()

        # Get all user process PIDs and elapsed times (seconds) since they are started.
        command_list = ["ps", "--no-headers", "-eo", "pid,etimes,user"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        ps_output_lines = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split("\n")

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
        command_list = ["cat"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        for pid in pid_list:
            command_list.append("/proc/" + pid + "/stat")
        cat_output_lines = (subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)).stdout.decode().strip().split("\n")
        global_cpu_time_all = time.time() * self.number_of_clock_ticks                             # global_cpu_time_all value is get just after "/proc/[PID]/stat file is get in order to measure global an process specific CPU times at the same time (nearly) for ensuring accurate process CPU usage percent.
        all_process_cpu_usages = []
        pid_list_from_stat = []
        for line in cat_output_lines:
            line_split = line.split()
            process_pid = line_split[0]
            pid_list_from_stat.append(process_pid)
            process_cpu_time = int(line_split[-39]) + int(line_split[-38])                    # Get process cpu time in user mode (utime + stime)
            global_process_cpu_times.append((global_cpu_time_all, process_cpu_time))          # While appending multiple elements into a list "append((value1, value2))" is faster than "append([value1, value2])".
            try:                                                                              # It gives various errors (ValueError, IndexError, UnboundLocalError) if a new process is started, a new column is shown on the treeview, etc because previous CPU time values are not present in these situations. Following CPU time values are use in these situations.
                global_cpu_time_all_prev, process_cpu_time_prev = self.global_process_cpu_times_prev[self.pid_list_prev.index(process_pid)]
            except (ValueError, IndexError, UnboundLocalError) as me:
                process_cpu_time_prev = process_cpu_time                                      # There is no "process_cpu_time_prev" value and get it from "process_cpu_time"  if this is first loop of the process
                global_cpu_time_all_prev = global_process_cpu_times[-1][0] - 1                # Subtract "1" CPU time (a negligible value) if this is first loop of the process
            process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
            global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
            all_process_cpu_usages.append(process_cpu_time_difference / global_cpu_time_difference * 100 / Common.number_of_logical_cores())
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
            if user_uid == selected_user_uid:                                                     # Human users have UID bigger than 999 (1000 =< UID) and lower than 65534.

                # Get username.
                selected_user_username = username

                # Get user full name
                selected_user_full_name = line_split[4]

                # Get user logged in data (User logged in data has been get previously)
                if username in user_logged_in_list:
                    selected_user_logged_in = _tr("Yes")
                else:
                    selected_user_logged_in = _tr("No")

                # Get user UID (UID value has been get previously)
                selected_user_uid = user_uid

                # Get user GID
                selected_user_gid = user_gid

                # Get user process count
                selected_user_process_count = logged_in_users_list.count(username)

                # Get user home directory
                selected_user_home_dir = line_split[5]

                # Get user group
                selected_user_group_name = user_group_names[user_group_ids.index(user_gid)]

                # Get user terminal
                selected_user_terminal = line_split[6]

                # Get user process start time
                curent_user_process_start_time_list = []
                for pid in pid_list:
                    if logged_in_users_list[pid_list.index(pid)] == username:
                        curent_user_process_start_time_list.append(user_processes_start_times[pid_list.index(pid)])
                if curent_user_process_start_time_list == []:
                    selected_user_process_start_time = 0
                else:
                    selected_user_process_start_time = time.time() - max(curent_user_process_start_time_list)

                # Get user processes CPU usage percentages
                selected_user_cpu_percent = 0
                for pid in pid_list:
                    if logged_in_users_list[pid_list.index(pid)] == username:
                        selected_user_cpu_percent = selected_user_cpu_percent + all_process_cpu_usages[pid_list.index(pid)]

        # For using values in the next loop
        self.pid_list_prev = pid_list
        self.global_process_cpu_times_prev = global_process_cpu_times

        # It gives "UnboundLocalError" error if "User Details" window is closed. The value is checked and window is closed in order to avoid errors.
        try:
            check_value = selected_user_username
        except UnboundLocalError:
            self.update_window_value = 0
            self.user_details_window.hide()
            return

        # Set label text
        self.user_label.set_label(selected_user_username)
        self.full_name_label.set_label(selected_user_full_name)
        self.logged_in_label.set_label(selected_user_logged_in)
        self.uid_label.set_label(selected_user_uid)
        self.gid_label.set_label(selected_user_gid)
        self.processes_label.set_label(f'{selected_user_process_count}')
        self.home_directory_label.set_label(selected_user_home_dir)
        self.group_label.set_label(selected_user_group_name)
        self.terminal_label.set_label(selected_user_terminal)
        if selected_user_process_start_time != 0:
            self.start_time_label.set_label(datetime.fromtimestamp(selected_user_process_start_time).strftime("%H:%M:%S %d.%m.%Y"))
        if selected_user_process_start_time == 0:
            self.start_time_label.set_label("-")
        self.cpu_label.set_label(f'{selected_user_cpu_percent:.{users_cpu_precision}f} %')


    def users_details_run_func(self, *args):
        """
        Run initial and loop functions of user details window.
        "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()".
        "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to change the update interval and
        run the loop again without waiting ending the previous update interval.
        """

        if hasattr(UsersDetails, "update_interval") == False:
            GLib.idle_add(self.users_details_initial_func)

        # Destroy GLib source for preventing it repeating the function.
        try:
            self.main_glib_source.destroy()
        # "try-except" is used in order to prevent errors if this is first run of the function.
        except AttributeError:
            pass
        self.update_interval = Config.update_interval
        self.main_glib_source = GLib.timeout_source_new(self.update_interval * 1000)

        if self.update_window_value == 1:
            GLib.idle_add(self.users_details_loop_func)
            self.main_glib_source.set_callback(self.users_details_run_func)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


UsersDetails = UsersDetails()


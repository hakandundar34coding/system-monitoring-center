#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GLib, GdkPixbuf
import os
from datetime import datetime
import time
import subprocess

from locale import gettext as _tr

from Config import Config
import Users
from Performance import Performance
from MainGUI import MainGUI


class UsersDetails:

    def __init__(self):

        # Get GUI objects from file
        builder3101w = Gtk.Builder()
        builder3101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersDetailsWindow.ui")

        # Get GUI objects
        self.window3101w = builder3101w.get_object('window3101w')
        self.label3101w = builder3101w.get_object('label3101w')
        self.label3102w = builder3101w.get_object('label3102w')
        self.label3103w = builder3101w.get_object('label3103w')
        self.label3104w = builder3101w.get_object('label3104w')
        self.label3105w = builder3101w.get_object('label3105w')
        self.label3106w = builder3101w.get_object('label3106w')
        self.label3107w = builder3101w.get_object('label3107w')
        self.label3108w = builder3101w.get_object('label3108w')
        self.label3109w = builder3101w.get_object('label3109w')
        self.label3110w = builder3101w.get_object('label3110w')
        self.label3111w = builder3101w.get_object('label3111w')

        # Set window properties
        self.window3101w.set_transient_for(MainGUI.window1)
        self.window3101w.set_modal(True)

        # Connect GUI signals
        self.window3101w.connect("delete-event", self.on_window3101w_delete_event)
        self.window3101w.connect("show", self.on_window3101w_show)


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window3101w_delete_event(self, widget, event):

        self.update_window_value = 0
        self.window3101w.hide()
        return True


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window3101w_show(self, widget):

        try:
            # Delete "update_interval" variable in order to let the code to run initial function. Otherwise, data from previous user (if it was viewed) will be used.
            del self.update_interval
        except AttributeError:
            pass

        # This value is checked for repeating the function for getting the user data.
        self.update_window_value = 1

        # Call this function in order to reset Users Details window GUI.
        self.users_details_gui_reset_function()
        self.users_details_run_func()


    # ----------------------- Called for resetting window GUI -----------------------
    def users_details_gui_reset_function(self):

        self.label3101w.set_text("--")
        self.label3102w.set_text("--")
        self.label3103w.set_text("--")
        self.label3104w.set_text("--")
        self.label3105w.set_text("--")
        self.label3106w.set_text("--")
        self.label3107w.set_text("--")
        self.label3108w.set_text("--")
        self.label3109w.set_text("--")
        self.label3110w.set_text("--")
        self.label3111w.set_text("--")


    # ----------------------------------- Users - Users Details Function -----------------------------------
    def users_details_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

        self.pid_list_prev = []
        self.global_process_cpu_times_prev = []

        self.system_boot_time = Users.system_boot_time
        self.number_of_clock_ticks = Users.number_of_clock_ticks


    # ----------------------------------- Users - Users Details Foreground Function -----------------------------------
    def users_details_loop_func(self):

        # Get right clicked user UID and username
        selected_user_uid = str(Users.selected_user_uid)
        selected_username = Users.selected_username

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        users_cpu_precision = Config.users_cpu_precision


        self.window3101w.set_title(_tr("User") + ":  " + selected_username)

        # Define empty lists for the current loop
        global_process_cpu_times = []
        number_of_logical_cores = Users.users_number_of_logical_cores_func()

        # Get all users and user groups.
        etc_passwd_lines, user_group_names, user_group_ids = Users.users_groups_func()

        # Get all user process PIDs and elapsed times (seconds) since they are started.
        if Config.environment_type == "flatpak":
            ps_output_lines = (subprocess.check_output(["flatpak-spawn", "--host", "ps", "--no-headers", "-eo", "pid,etimes,user"], shell=False)).decode().strip().split("\n")
        else:
            ps_output_lines = (subprocess.check_output(["ps", "--no-headers", "-eo", "pid,etimes,user"], shell=False)).decode().strip().split("\n")

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
            self.window3101w.hide()
            return

        # Set label text
        self.label3101w.set_text(selected_user_username)
        self.label3102w.set_text(selected_user_full_name)
        self.label3103w.set_text(selected_user_logged_in)
        self.label3104w.set_text(selected_user_uid)
        self.label3105w.set_text(selected_user_gid)
        self.label3106w.set_text(f'{selected_user_process_count}')
        self.label3107w.set_text(selected_user_home_dir)
        self.label3108w.set_text(selected_user_group_name)
        self.label3109w.set_text(selected_user_terminal)
        if selected_user_process_start_time != 0:
            self.label3110w.set_text(datetime.fromtimestamp(selected_user_process_start_time).strftime("%H:%M:%S %d.%m.%Y"))
        if selected_user_process_start_time == 0:
            self.label3110w.set_text("-")
        self.label3111w.set_text(f'{selected_user_cpu_percent:.{users_cpu_precision}f} %')


    # ----------------------------------- Users Details - Run Function -----------------------------------
    # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to change the update interval and run the loop again without waiting ending the previous update interval.
    def users_details_run_func(self, *args):

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


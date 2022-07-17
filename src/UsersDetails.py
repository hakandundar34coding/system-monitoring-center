#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GLib, GdkPixbuf
import os
import subprocess
from datetime import datetime
import time

from locale import gettext as _tr

from Config import Config
import Users
from Performance import Performance


# Define class
class UsersDetails:

    # ----------------------- Always called when object is generated -----------------------
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

        # For many systems CPU ticks 100 times in a second. Wall clock time could be get if CPU times are multiplied with this value or vice versa.
        self.number_of_clock_ticks = os.sysconf("SC_CLK_TCK")

        # Get system boot time which will be used for obtaining user process start time
        with open("/proc/stat") as reader:
            stat_lines = reader.read().split("\n")
        for line in stat_lines:
            if "btime " in line:
                self.system_boot_time = int(line.split()[1].strip())


    # ----------------------------------- Users - Users Details Foreground Function -----------------------------------
    def users_details_loop_func(self):

        # Get right clicked user UID and username
        selected_user_uid = str(Users.selected_user_uid)
        selected_username = Users.selected_username

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        users_cpu_precision = Config.users_cpu_precision


        self.window3101w.set_title(_tr("User") + ": " + selected_username)

        # Define empty lists for the current loop
        global_process_cpu_times = []

        # Get number of online logical CPU cores (this operation is repeated in every loop because number of online CPU cores may be changed by user and this may cause wrong calculation of CPU usage percent data of the processes even if this is a very rare situation.)
        try:
            # To be able to get number of online logical CPU cores first try  a faster way: using "SC_NPROCESSORS_ONLN" variable.
            number_of_logical_cores = os.sysconf("SC_NPROCESSORS_ONLN")
        except ValueError:
            # As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
            with open("/proc/cpuinfo") as reader:
                proc_cpuinfo_lines = reader.read().split("\n")
            number_of_logical_cores = 0
            for line in proc_cpuinfo_lines:
                if line.startswith("processor"):
                    number_of_logical_cores = number_of_logical_cores + 1

        # Get all users
        with open("/etc/passwd") as reader:
            etc_passwd_output = reader.read().strip()
        etc_passwd_lines = etc_passwd_output.split("\n")
        if ":" + selected_user_uid + ":" not in etc_passwd_output:
            self.update_window_value = 0
            self.window3101w.hide()
            return

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
        for pid in pid_list[:]:                                                               # "[:]" is used for iterating over copy of the list because element are removed during iteration. Otherwise incorrect operations (incorrect element removal) are performed on the list.
            try:
                with open("/proc/" + pid + "/status") as reader:
                    proc_pid_status_lines = reader.read().split("\n")
                with open("/proc/" + pid + "/stat") as reader:
                    global_cpu_time_all = time.time() * self.number_of_clock_ticks            # global_cpu_time_all value is get just before "/proc/[PID]/stat file is read in order to measure global an process specific CPU times at the same time (nearly) for ensuring accurate process CPU usage percent.
                    proc_pid_stat_lines = reader.read().split()
            except FileNotFoundError:                                                         # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
                pid_list.remove(pid)
                continue
            for line in proc_pid_status_lines:
                # Get names of all processes
                if "Name:\t" in line:
                    all_process_names.append(line.split(":")[1].strip())
                # Get user UIDs of all processes
                if "Uid:\t" in line:
                    all_process_user_ids.append(line.split(":")[1].split()[0].strip())        # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.

            # Get CPU usage percent of all processes
            process_cpu_time = int(proc_pid_stat_lines[-39]) + int(proc_pid_stat_lines[-38])    # Get process cpu time in user mode (utime + stime)
            global_process_cpu_times.append((global_cpu_time_all, process_cpu_time))          # While appending multiple elements into a list "append((value1, value2))" is faster than "append([value1, value2])".
            try:                                                                              # It gives various errors (ValueError, IndexError, UnboundLocalError) if a new process is started, a new column is shown on the treeview, etc because previous CPU time values are not present in these situations. Following CPU time values are use in these situations.
                global_cpu_time_all_prev, process_cpu_time_prev = self.global_process_cpu_times_prev[self.pid_list_prev.index(pid)]
            except (ValueError, IndexError, UnboundLocalError) as me:
                process_cpu_time_prev = process_cpu_time                                      # There is no "process_cpu_time_prev" value and get it from "process_cpu_time"  if this is first loop of the process
                global_cpu_time_all_prev = global_process_cpu_times[-1][0] - 1                # Subtract "1" CPU time (a negligible value) if this is first loop of the process
            process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
            global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
            all_process_cpu_usages.append(process_cpu_time_difference / global_cpu_time_difference * 100 / number_of_logical_cores)

        # Get all users last log in and last failed log in times
        lslogins_command_lines = (subprocess.check_output(["lslogins", "--notruncate", "-e", "--newline", "--time-format=iso", "-u", "-o", "=USER,LAST-LOGIN,FAILED-LOGIN"], shell=False)).decode().strip().split("\n")

        for line in etc_passwd_lines:
            line_split = line.split(":")
            if line_split[2] == selected_user_uid:
                selected_user_username = line_split[0]
                selected_user_gid = line_split[3]
                selected_user_full_name = line_split[4]                                       # Get user full name
                selected_user_home_dir = line_split[5]
                selected_user_terminal = line_split[6]
                break

        # Get user PID and logged in data (PID data is required for obtaining user logged in data. User PID and user logged in data will be appended later)
        user_process_pid = 0                                                                  # Initial value of "user_PID" value. This value will be left as "0" if user is not logged in.
        for i, process_name in enumerate(all_process_names):
            if process_name == "systemd":                                                     # "systemd" process per user is checked here (by checking real UID of the process). It is not system-wide "systemd" process which is owned by "root" user. User session process is specific to desktop session (for example xfce4-session for XFCE desktop environment) and checking "systemd" process of the user is easier and gives very similar start time.
                real_user_id = all_process_user_ids[i]
                if real_user_id == selected_user_uid:
                    user_process_pid = pid_list[i]
                    break                                                                     # Exit this loop if real_user_id" is found in order to obtain faster code execution.
        if user_process_pid != 0:                                                             # User is not logged in if "user_process_pid" is not get from "systemd" process of the user.
            selected_user_logged_in = _tr("Yes")
        if user_process_pid == 0:                                                             # User is logged in if "user_process_pid" is get from "systemd" process of the user.
            selected_user_logged_in = _tr("No")

        # Get user process count
        selected_user_process_count = all_process_user_ids.count(selected_user_uid)

        # Get user group
        selected_user_group_name = user_group_names[user_group_ids.index(selected_user_gid)]

        # Get user process start time
        if user_process_pid == 0:
            selected_user_process_start_time = 0                                              # User process start time is "0" if it is not alive (if user is not logged in)
        if user_process_pid != 0:                                                             # User process start time is get if it is alive (if user is logged in)
            try:
                with open("/proc/" + str(user_process_pid) + "/stat") as reader:
                    proc_pid_stat_lines = int(reader.read().split()[-31])                     # Elapsed time between system boot and process start time (measured in clock ticks and need to be divided by sysconf(_SC_CLK_TCK) for converting into wall clock time)
                selected_user_process_start_time = (proc_pid_stat_lines / self.number_of_clock_ticks) + self.system_boot_time
            except Exception:
                selected_user_process_start_time = 0

        # Get user processes CPU usage percent
        selected_user_cpu_percent = 0
        for pid in pid_list:
            if all_process_user_ids[pid_list.index(pid)] == selected_user_uid:
                selected_user_cpu_percent = selected_user_cpu_percent + all_process_cpu_usages[pid_list.index(pid)]

        # For using values in the next loop
        self.pid_list_prev = pid_list
        self.global_process_cpu_times_prev = global_process_cpu_times


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


# Generate object
UsersDetails = UsersDetails()


#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib
import os
import time
from datetime import datetime

from locale import gettext as _tr

from Config import Config
import Processes
from Performance import Performance


# Define class
class ProcessesDetails:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder2101w = Gtk.Builder()
        builder2101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesDetailsWindow.ui")

        # Get GUI objects
        self.window2101w = builder2101w.get_object('window2101w')
        self.notebook2101w = builder2101w.get_object('notebook2101w')
        # Get "Summary" tab GUI objects
        self.label2101w = builder2101w.get_object('label2101w')
        self.label2102w = builder2101w.get_object('label2102w')
        self.label2103w = builder2101w.get_object('label2103w')
        self.label2104w = builder2101w.get_object('label2104w')
        self.label2105w = builder2101w.get_object('label2105w')
        self.label2106w = builder2101w.get_object('label2106w')
        self.label2107w = builder2101w.get_object('label2107w')
        self.label2108w = builder2101w.get_object('label2108w')
        self.label2109w = builder2101w.get_object('label2109w')
        self.label2110w = builder2101w.get_object('label2110w')
        self.label2111w = builder2101w.get_object('label2111w')
        self.label2112w = builder2101w.get_object('label2112w')
        self.label2113w = builder2101w.get_object('label2113w')
        self.label2114w = builder2101w.get_object('label2114w')
        self.label2115w = builder2101w.get_object('label2115w')
        self.label2138w = builder2101w.get_object('label2138w')
        # Get "CPU and RAM" tab GUI objects
        self.label2116w = builder2101w.get_object('label2116w')
        self.label2117w = builder2101w.get_object('label2117w')
        self.label2118w = builder2101w.get_object('label2118w')
        self.label2119w = builder2101w.get_object('label2119w')
        self.label2120w = builder2101w.get_object('label2120w')
        self.label2121w = builder2101w.get_object('label2121w')
        self.label2122w = builder2101w.get_object('label2122w')
        self.label2123w = builder2101w.get_object('label2123w')
        self.label2124w = builder2101w.get_object('label2124w')
        self.label2125w = builder2101w.get_object('label2125w')
        self.label2126w = builder2101w.get_object('label2126w')
        self.label2127w = builder2101w.get_object('label2127w')
        # Get "Disk and Path" tab GUI objects
        self.label2128w = builder2101w.get_object('label2128w')
        self.label2129w = builder2101w.get_object('label2129w')
        self.label2130w = builder2101w.get_object('label2130w')
        self.label2131w = builder2101w.get_object('label2131w')
        self.label2132w = builder2101w.get_object('label2132w')
        self.label2133w = builder2101w.get_object('label2133w')
        self.label2134w = builder2101w.get_object('label2134w')
        self.label2135w = builder2101w.get_object('label2135w')
        self.label2136w = builder2101w.get_object('label2136w')
        self.label2137w = builder2101w.get_object('label2137w')

        # Connect GUI signals
        self.window2101w.connect("delete-event", self.on_window2101w_delete_event)
        self.window2101w.connect("show", self.on_window2101w_show)


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window2101w_delete_event(self, widget, event):

        self.window2101w.hide()
        return True


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window2101w_show(self, widget):

        try:
            # Delete "update_interval" variable in order to let the code to run initial function. Otherwise, data from previous process (if it was viewed) will be used.
            del self.update_interval
        except AttributeError:
            pass

        # Call this function in order to reset Processes Details window GUI.
        self.processes_details_gui_reset_function()
        self.processes_details_tab_switch_control_func()
        self.process_details_run_func()


    # ----------------------- Called for resetting window GUI -----------------------
    def processes_details_gui_reset_function(self):

        # Set fist page (Summary tab) of the notebook
        self.notebook2101w.set_current_page(0)

        self.label2101w.set_text("--")
        self.label2102w.set_text("--")
        self.label2103w.set_text("--")
        self.label2104w.set_text("--")
        self.label2105w.set_text("--")
        self.label2106w.set_text("--")
        self.label2107w.set_text("--")
        self.label2108w.set_text("--")
        self.label2109w.set_text("--")
        self.label2110w.set_text("--")
        self.label2111w.set_text("--")
        self.label2112w.set_text("--")
        self.label2113w.set_text("--")
        self.label2114w.set_text("--")
        self.label2115w.set_text("--")
        self.label2116w.set_text("--")
        self.label2117w.set_text("--")
        self.label2118w.set_text("--")
        self.label2119w.set_text("--")
        self.label2120w.set_text("--")
        self.label2121w.set_text("--")
        self.label2122w.set_text("--")
        self.label2123w.set_text("--")
        self.label2124w.set_text("--")
        self.label2125w.set_text("--")
        self.label2126w.set_text("--")
        self.label2127w.set_text("--")
        self.label2128w.set_text("--")
        self.label2129w.set_text("--")
        self.label2130w.set_text("--")
        self.label2131w.set_text("--")
        self.label2132w.set_text("--")
        self.label2133w.set_text("--")
        self.label2134w.set_text("--")
        self.label2135w.set_text("--")
        self.label2136w.set_text("--")
        self.label2137w.set_text("--")
        self.label2138w.set_text("--")


    # ----------------------- Called for checking if noteobok tabs are switched and updating the data on the last opened tab immediately without waiting end of the update interval. Signals of notebook for tab switching is not useful because it performs the action and after that it switches the tab. Data updating function does not recognizes tab switch due to this reason. -----------------------
    def processes_details_tab_switch_control_func(self):

        # For avoiding errors in the first loop of the control
        if hasattr(ProcessesDetails, "previous_page") == False:
            self.previous_page = None
        current_page = self.notebook2101w.get_current_page()

        # Check if tab is switched and run loop function to get process information immediately.
        if current_page != self.previous_page and self.previous_page != None:
            # This definiton is made here because this value may be deleted if a process details window is opened after closing a previous one and this causes "NameError: name 'update_interval' is not defined" error.
            self.update_interval = Config.update_interval
            # Update the data on the tab
            self.process_details_loop_func()
        self.previous_page = current_page

        # Check is performed in every 200 ms which is small enough for immediate update and not very frequent for avoiding high CPU usages.
        if self.window2101w.get_visible() == True:
            GLib.timeout_add(200, self.processes_details_tab_switch_control_func)


    # ----------------------------------- Processes - Processes Details Function -----------------------------------
    def process_details_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

        self.process_status_list = Processes.process_status_list
        self.global_process_cpu_times_prev = []
        self.disk_read_write_data_prev = []

        # Get system boot time
        with open("/proc/stat") as reader:
            stat_lines = reader.read().split("\n")
        for line in stat_lines:
            if "btime " in line:
                self.system_boot_time = int(line.split()[1].strip())


    # ----------------------------------- Processes - Processes Details Foreground Function -----------------------------------
    def process_details_loop_func(self):

        processes_cpu_precision = Config.processes_cpu_precision
        processes_memory_data_precision = Config.processes_memory_data_precision
        processes_memory_data_unit = Config.processes_memory_data_unit
        processes_disk_data_precision = Config.processes_disk_data_precision
        processes_disk_data_unit = Config.processes_disk_data_unit
        processes_disk_speed_bit = Config.processes_disk_speed_bit

        # Get usernames and UIDs.
        usernames_username_list = []
        usernames_uid_list = []
        with open("/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")
        for line in etc_passwd_lines:
            line_splitted = line.split(":")
            usernames_username_list.append(line_splitted[0])
            usernames_uid_list.append(line_splitted[2])

        # Get "selected_process_pid".
        selected_process_pid = Processes.selected_process_pid

        number_of_clock_ticks = Processes.number_of_clock_ticks
        # global_cpu_time_all value is get just before "/proc/[PID]/stat file is read in order to measure global an process specific CPU times at the same time (nearly) for ensuring accurate process CPU usage percent. global_cpu_time_all value is get by using time module of Python instead of reading "/proc/stat" file for faster processing.
        global_cpu_time_all = time.time() * number_of_clock_ticks
        try:
            # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
            with open("/proc/" + selected_process_pid + "/stat") as reader:
                proc_pid_stat_lines = reader.read()
        # Process may be ended. "try-catch" is used for avoiding errors in this situation.
        except FileNotFoundError:
            self.window2101w.hide()
            self.processes_no_such_process_error_dialog(selected_process_name, selected_process_pid)
            return

        # Get process name            
        proc_pid_stat_lines_split = proc_pid_stat_lines.split()
        first_parentheses = proc_pid_stat_lines.find("(")                                     # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
        second_parentheses = proc_pid_stat_lines.rfind(")")                                   # Last parantheses ")" index is get by using "find()".
        process_name_from_stat = proc_pid_stat_lines[first_parentheses+1:second_parentheses]    # Process name is get from string by using the indexes get previously.
        selected_process_name = process_name_from_stat
        if len(selected_process_name) == 15:                                                  # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name.
            try:
                with open("/proc/" + selected_process_pid + "/cmdline") as reader:
                    process_cmdline = reader.read().replace("\x00", " ")                      # Some process names which are obtained from "cmdline" contain "\x00" and these are replaced by " ".
                selected_process_name = process_cmdline.split("/")[-1].split("\x00")[0]       # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()".
            # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
            except FileNotFoundError:
                self.window2101w.hide()
                self.processes_no_such_process_error_dialog(selected_process_name, selected_process_pid)
                return
            selected_process_name = process_cmdline.split("/")[-1].split(" ")[0]
            if selected_process_name.startswith(process_name_from_stat) == False:
                selected_process_name = process_cmdline.split(" ")[0].split("/")[-1]
                if selected_process_name.startswith(process_name_from_stat) == False:
                    selected_process_name = process_name_from_stat                            # Root access is needed for reading "cmdline" file of the some processes. Otherwise it gives "" as output. Process name from "stat" file of the process is used is this situation. Also process name from "stat" file is used if name from "cmdline" does not start with name from "stat" file.

        # Get process icon
        selected_process_icon = "system-monitoring-center-process-symbolic"                   # Initial value of the "selected_process_icon". This icon will be shown for processes of which icon could not be found in default icon theme.
        if selected_process_name in Processes.application_exec_list:                          # Use process icon name from application file if process name is found in application exec list
            selected_process_icon = Processes.application_icon_list[Processes.application_exec_list.index(selected_process_name)]

        # Set ProcessesDetails window title and icon
        self.window2101w.set_title(_tr("Process Details") + ": " + selected_process_name + " - (" + _tr("PID") + ": " + selected_process_pid + ")")
        self.window2101w.set_icon_name(selected_process_icon)


        # Show and update process details on the "Summary" tab
        if self.notebook2101w.get_current_page() == 0:
        
            # Get process status
            selected_process_status = self.process_status_list[proc_pid_stat_lines_split[-50]]

            # Get process user name
            try:
                # User name of the process owner is get from "/proc/status" file because it is present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                with open("/proc/" + selected_process_pid + "/status") as reader:
                    proc_pid_status_lines = reader.read().split("\n")
            # Process may be ended. "try-catch" is used for avoiding errors in this situation.
            except FileNotFoundError:
                self.window2101w.hide()
                self.processes_no_such_process_error_dialog(selected_process_name, selected_process_pid)
                return
            for line in proc_pid_status_lines:
                if "Uid:\t" in line:
                    # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                    real_user_id = line.split(":")[1].split()[0].strip()
                    try:
                        selected_process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
                    except ValueError:
                        selected_process_username = real_user_id

            # Get process nice
            selected_process_nice = int(proc_pid_stat_lines_split[-34])

            # Calculate CPU usage percent of the selected process
            process_cpu_time = int(proc_pid_stat_lines_split[-39]) + int(proc_pid_stat_lines_split[-38])   # Get process cpu time in user mode (utime + stime)
            global_process_cpu_times = [global_cpu_time_all, process_cpu_time]
            try:
                global_cpu_time_all_prev, process_cpu_time_prev = self.global_process_cpu_times_prev
            # It gives various errors (ValueError, IndexError, UnboundLocalError) if a new process is started, a new column is shown on the treeview, etc because previous CPU time values are not present in these situations. Following CPU time values are used in these situations.
            except (ValueError, IndexError, UnboundLocalError) as me:
                process_cpu_time_prev = process_cpu_time                                      # There is no "process_cpu_time_prev" value and get it from "process_cpu_time"  if this is first loop of the process
                global_cpu_time_all_prev = global_process_cpu_times[0] - 1                    # Subtract "1" CPU time (a negligible value) if this is first loop of the process
            process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
            global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
            selected_process_cpu_percent = process_cpu_time_difference / global_cpu_time_difference * 100 / Processes.number_of_logical_cores
            self.global_process_cpu_times_prev = global_process_cpu_times

            # Get RAM (RSS) data
            selected_process_memory_rss = int(proc_pid_stat_lines_split[-29]) * Processes.memory_page_size    # Get process RSS (resident set size) memory pages and multiply with memory_page_size in order to convert the value into bytes.

            # Get disk read data, disk write data
            try:
                with open("/proc/" + selected_process_pid + "/io") as reader:
                    proc_pid_io_lines = reader.read().split("\n")
                selected_process_read_bytes = int(proc_pid_io_lines[4].split(":")[1])
                selected_process_write_bytes = int(proc_pid_io_lines[5].split(":")[1])
            # Root access is needed for reading "/proc/[PID]/io" file else it gives error. "try-except" is used in order to avoid this error if user has no root privileges.
            except PermissionError:
                selected_process_read_bytes = 0
                selected_process_write_bytes = 0

            # Get disk read speed, disk write speed
            disk_read_write_data = [selected_process_read_bytes, selected_process_write_bytes]
            if self.disk_read_write_data_prev == []:
                selected_process_read_bytes_prev = selected_process_read_bytes                # Make process_read_bytes_prev equal to process_read_bytes for giving "0" disk read speed value if this is first loop of the process
            else:
                selected_process_read_bytes_prev = self.disk_read_write_data_prev[0]
            selected_process_read_speed = (selected_process_read_bytes - int(selected_process_read_bytes_prev)) / self.update_interval    # Append process_read_bytes which will be used as "process_read_bytes_prev" value in the next loop and also append disk read speed. 
            if self.disk_read_write_data_prev == []:
                selected_process_write_bytes_prev = selected_process_write_bytes              # Make process_write_bytes_prev equal to process_write_bytes for giving "0" disk write speed value if this is first loop of the process
            else:
                selected_process_write_bytes_prev = self.disk_read_write_data_prev[1]
            selected_process_write_speed = (selected_process_write_bytes - int(selected_process_write_bytes_prev)) / self.update_interval    # Append process_read_bytes which will be used as "process_read_bytes_prev" value in the next loop and also append disk read speed. 
            self.disk_read_write_data_prev = disk_read_write_data

            # Get process start time
            try:
                with open("/proc/" + selected_process_pid + "/stat") as reader:
                    proc_pid_stat_lines = int(reader.read().split()[-31])                     # Elapsed time between system boot and process start time (measured in clock ticks and need to be divided by sysconf(_SC_CLK_TCK) for converting into wall clock time)
            except Exception:
                self.window2101w.hide()
                self.processes_no_such_process_error_dialog(selected_process_name, selected_process_pid)
                return
            selected_process_start_time = (proc_pid_stat_lines / number_of_clock_ticks) + self.system_boot_time

            # Get process ppid
            selected_process_ppid = int(proc_pid_stat_lines_split[-49])

            # Get process exe
            try:
                selected_process_exe = os.path.realpath("/proc/" + pid + "/exe")
            # Executable path of some of the processes may not be get without root privileges or may not be get due to the reason of some of the processes may not have a exe file. "try-except" is used to be able to avoid errors due to these reasons.
            except Exception:
                selected_process_exe = "-"

            # Get parent processes name and PIDs
            parent_process_names_pids = []
            # Define "current_ppid" as "selected_process_pid". They are not same thing for the initial value but it is defined as initial value for proper working of the ppid loop code.
            current_ppid = selected_process_pid
            while current_ppid != 0:
                with open("/proc/" + str(current_ppid) + "/stat") as reader:
                    current_ppid = int(reader.read().split()[-49])
                if current_ppid != 0:
                    with open("/proc/" + str(current_ppid) + "/stat") as reader:
                        proc_pid_stat_lines = reader.read()
                    first_parentheses = proc_pid_stat_lines.find("(")                         # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
                    second_parentheses = proc_pid_stat_lines.rfind(")")                       # Last parantheses ")" index is get by using "find()".
                    process_name_from_stat = proc_pid_stat_lines[first_parentheses+1:second_parentheses]    # Process name is get from string by using the indexes get previously.
                    process_name = process_name_from_stat
                    if len(process_name) >= 15:                                               # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name. "=15" is enough but this limit may be increased in the next releases of the kernel. ">=15" is used in order to handle this possible change.
                        with open("/proc/" + str(current_ppid) + "/cmdline") as reader:
                            process_name = ''.join(reader.read().split("/")[-1].split("\x00"))    # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()" and joined again without these characters.
                        if process_name.startswith(process_name_from_stat) == False:
                            process_name = process_name_from_stat
                    parent_process_names_pids.append(f'{process_name} (PID: {current_ppid})')

            # Get child process names and PIDs
            pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]
            ppid_list = []
            for pid in pid_list[:]:                                                           # "[:]" is used for iterating over copy of the list because element are removed during iteration. Otherwise incorrect operations (incorrect element removal) are performed on the list.
                try:                                                                          # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
                    with open("/proc/" + pid + "/stat") as reader:                            # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
                        proc_pid_stat_lines = reader.read()
                # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
                except FileNotFoundError:
                    pid_list.remove(pid)
                    continue
                proc_pid_stat_lines_split = proc_pid_stat_lines.split()
                ppid_list.append(proc_pid_stat_lines_split[-49])
            selected_process_child_process_pids = []
            for i, ppid in enumerate(ppid_list):
                if ppid == selected_process_pid:
                    selected_process_child_process_pids.append(pid_list[i])
            selected_process_child_process_names = []
            for pid in selected_process_child_process_pids:
                try:
                    with open("/proc/" + pid + "/stat") as reader:                            # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
                        proc_pid_stat_lines = reader.read()
                # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
                # Removed pid from "selected_process_child_process_pids" and skip to next loop (pid) if process is ended just after selected_process_child_process_pids is generated.
                except FileNotFoundError:
                    selected_process_child_process_pids.remove(pid)
                    continue
                first_parentheses = proc_pid_stat_lines.find("(")                             # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
                second_parentheses = proc_pid_stat_lines.rfind(")")                           # Last parantheses ")" index is get by using "find()".
                process_name_from_stat = proc_pid_stat_lines[first_parentheses+1:second_parentheses]  # Process name is get from string by using the indexes get previously.
                process_name = process_name_from_stat
                if len(process_name) == 15:                                                   # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name.
                    try:
                        with open("/proc/" + pid + "/cmdline") as reader:
                            process_name = reader.read().split("/")[-1].split("\x00")[0]      # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()".
                    except FileNotFoundError:                                                 # Removed pid from "selected_process_child_process_pids" and skip to next loop (pid) if process is ended just after selected_process_child_process_pids is generated.
                        selected_process_child_process_pids.remove(pid)
                        continue
                    if process_name.startswith(process_name_from_stat) == False:
                        process_name = process_name_from_stat                                 # Root access is needed for reading "cmdline" file of the some processes. Otherwise it gives "" as output. Process name from "stat" file of the process is used is this situation. Also process name from "stat" file is used if name from "cmdline" does not start with name from "stat" file.
                selected_process_child_process_names.append(process_name)
            child_process_names_pids = []
            for i, pid in enumerate(selected_process_child_process_pids):
                child_process_names_pids.append(f'{selected_process_child_process_names[i]} (PID: {pid})')

            # Get real, effective and saved UIDs
            for line in proc_pid_status_lines:
                if "Uid:\t" in line:
                    line_split = line.split(":")[1].split()
                    # There are 4 values in the Uid line (real, effective, user, filesystem UIDs)
                    selected_process_uid_real = line_split[0].strip()
                    selected_process_uid_effective = line_split[1].strip()
                    selected_process_uid_saved = line_split[2].strip()

            # Get real, effective and saved GIDs
            for line in proc_pid_status_lines:
                if "Gid:\t" in line:
                    line_split = line.split(":")[1].split()
                    # There are 4 values in the Gid line (real, effective, user, filesystem GIDs)
                    selected_process_gid_real = line_split[0].strip()
                    selected_process_gid_effective = line_split[1].strip()
                    selected_process_gid_saved = line_split[2].strip()

            # Set label text by using process data
            self.label2101w.set_text(selected_process_name)
            self.label2102w.set_text(f'{selected_process_pid}')
            self.label2103w.set_text(selected_process_status)
            self.label2104w.set_text(selected_process_username)
            self.label2105w.set_text(f'{selected_process_nice}')
            self.label2106w.set_text(f'{selected_process_cpu_percent:.{processes_cpu_precision}f} %')
            self.label2107w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_rss, processes_memory_data_unit, processes_memory_data_precision)}')
            if selected_process_read_bytes != "-":
                self.label2108w.set_text(f'{self.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_read_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
            if selected_process_read_bytes == "-":
                self.label2108w.set_text("-")
            if selected_process_write_bytes != "-":
                self.label2138w.set_text(f'{self.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_write_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
            if selected_process_write_bytes == "-":
                self.label2138w.set_text("-")
            self.label2109w.set_text(datetime.fromtimestamp(selected_process_start_time).strftime("%d.%m.%Y %H:%M:%S"))
            self.label2110w.set_text(selected_process_exe)
            self.label2111w.set_text(f'{selected_process_ppid}')
            if parent_process_names_pids != []:
                self.label2112w.set_text(',\n'.join(parent_process_names_pids))
            if parent_process_names_pids == []:
                self.label2112w.set_text("-")
            if child_process_names_pids != []:
                self.label2113w.set_text(',\n'.join(child_process_names_pids))
            if child_process_names_pids == []:
                self.label2113w.set_text("-")
            self.label2114w.set_text(f'Real: {selected_process_uid_real}, Effective: {selected_process_uid_effective}, Saved: {selected_process_uid_saved}')
            self.label2115w.set_text(f'Real: {selected_process_gid_real}, Effective: {selected_process_gid_effective}, Saved: {selected_process_gid_saved}')


        # Show and update process details on the "CPU and Memory" tab
        if self.notebook2101w.get_current_page() == 1:

            # Calculate CPU usage percent of the selected process
            process_cpu_time = int(proc_pid_stat_lines_split[-39]) + int(proc_pid_stat_lines_split[-38])   # Get process cpu time in user mode (utime + stime)
            global_process_cpu_times = [global_cpu_time_all, process_cpu_time]
            try:
                global_cpu_time_all_prev, process_cpu_time_prev = self.global_process_cpu_times_prev
            # It gives various errors (ValueError, IndexError, UnboundLocalError) if a new process is started, a new column is shown on the treeview, etc because previous CPU time values are not present in these situations. Following CPU time values are used in these situations.
            except (ValueError, IndexError, UnboundLocalError) as me:
                process_cpu_time_prev = process_cpu_time                                      # There is no "process_cpu_time_prev" value and get it from "process_cpu_time"  if this is first loop of the process
                global_cpu_time_all_prev = global_process_cpu_times[0] - 1                    # Subtract "1" CPU time (a negligible value) if this is first loop of the process
            process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
            global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
            selected_process_cpu_percent = process_cpu_time_difference / global_cpu_time_difference * 100 / Processes.number_of_logical_cores
            self.global_process_cpu_times_prev = global_process_cpu_times

            # Get number of threads of the process
            selected_process_num_threads = proc_pid_stat_lines_split[-33]

            # Get threads (TIDs) of the process
            selected_process_threads = [filename for filename in os.listdir("/proc/" + selected_process_pid + "/task/") if filename.isdigit()]

            # Get the last CPU core number which process executed on
            selected_process_cpu_num = proc_pid_stat_lines_split[-14]

            # Get CPU cores that process run allowed on
            try:
                with open("/proc/" + selected_process_pid + "/status") as reader:
                    proc_pid_status_lines = reader.read().split("\n")
            # Process may be ended. "try-catch" is used for avoiding errors in this situation.
            except FileNotFoundError:
                self.window2101w.hide()
                self.processes_no_such_process_error_dialog(selected_process_name, selected_process_pid)
                return
            for line in proc_pid_status_lines:
                if "Cpus_allowed_list:" in line:
                    selected_process_cpus_allowed = line.split(":")[1].strip()

            # Get CPU times of the process
            selected_process_cpu_times_user = proc_pid_stat_lines_split[-39]
            selected_process_cpu_times_kernel = proc_pid_stat_lines_split[-38]
            selected_process_cpu_times_children_user = proc_pid_stat_lines_split[-37]
            selected_process_cpu_times_children_kernel = proc_pid_stat_lines_split[-36]
            selected_process_cpu_times_io_wait = proc_pid_stat_lines_split[-11]
            for line in proc_pid_status_lines:
                if "voluntary_ctxt_switches:" in line:
                    selected_process_num_ctx_switches_voluntary = line.split(":")[1].strip()
            for line in proc_pid_status_lines:
                if "nonvoluntary_ctxt_switches:" in line:
                    selected_process_num_ctx_switches_nonvoluntary = line.split(":")[1].strip()

            # Get RAM (RSS) data and multiply with memory_page_size in order to convert the value into bytes.
            selected_process_memory_rss = int(proc_pid_stat_lines_split[-29]) * Processes.memory_page_size

            # Get RAM (VMS) data (this value is in bytes unit).
            selected_process_memory_vms = int(proc_pid_stat_lines_split[-30])

            # Get RAM (Shared) data and multiply with memory_page_size in order to convert the value into bytes.
            with open("/proc/" + selected_process_pid + "/statm") as reader:                                   
                selected_process_memory_shared = int(reader.read().split()[2]) * Processes.memory_page_size

            # Get USS (Unique Set Size) and swap memory data of the pprocess
            try:
                private_clean = 0
                private_dirty = 0
                memory_swap = 0
                with open("/proc/" + selected_process_pid + "/smaps") as reader:
                    proc_pid_smaps_lines = reader.read().split("\n")
                for line in proc_pid_smaps_lines:
                    if "Private_Clean:" in line:
                        private_clean = private_clean + int(line.split(":")[1].split()[0].strip())
                    if "Private_Dirty:" in line:
                        private_dirty = private_dirty + int(line.split(":")[1].split()[0].strip())
                    if line.startswith("Swap:"):
                        memory_swap = memory_swap + int(line.split(":")[1].split()[0].strip())
                # Kilobytes value converted into bytes value (there is a negligible deviation in bytes unit)
                selected_process_memory_uss = (private_clean + private_dirty) * 1024
                selected_process_memory_swap = memory_swap * 1024
            except Exception:
                selected_process_memory_uss = "-"
                selected_process_memory_swap = "-"

            # Set label text by using process data
            self.label2116w.set_text(f'{selected_process_cpu_percent:.{processes_cpu_precision}f} %')
            self.label2117w.set_text(f'{selected_process_num_threads}')
            self.label2118w.set_text(',\n'.join(selected_process_threads))
            self.label2119w.set_text(f'{selected_process_cpu_num}')
            self.label2120w.set_text(selected_process_cpus_allowed)
            self.label2121w.set_text(f'User: {selected_process_cpu_times_user}, System: {selected_process_cpu_times_kernel}, Children User: {selected_process_cpu_times_children_user}, Children System: {selected_process_cpu_times_children_kernel}, IO Wait: {selected_process_cpu_times_io_wait}')
            self.label2122w.set_text(f'Voluntary: {selected_process_num_ctx_switches_voluntary}, Involuntary: {selected_process_num_ctx_switches_nonvoluntary}')
            self.label2123w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_rss, processes_memory_data_unit, processes_memory_data_precision)}')
            self.label2124w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_vms, processes_memory_data_unit, processes_memory_data_precision)}')
            self.label2125w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_shared, processes_memory_data_unit, processes_memory_data_precision)}')
            if selected_process_memory_uss != "-" and selected_process_memory_swap != "-":
                self.label2126w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_uss, processes_memory_data_unit, processes_memory_data_precision)}')
                self.label2127w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_memory_swap, processes_memory_data_unit, processes_memory_data_precision)}')
            if selected_process_memory_uss == "-" and selected_process_memory_swap == "-":
                self.label2126w.set_text(selected_process_memory_uss)
                self.label2127w.set_text(selected_process_memory_swap)


        # Show and update process details on the "Disk and Path" tab
        if self.notebook2101w.get_current_page() == 2:

            # Get disk read data, disk write data, read count, write count of the process
            try:
                with open("/proc/" + selected_process_pid + "/io") as reader:
                    proc_pid_io_lines = reader.read().split("\n")
                selected_process_read_bytes = int(proc_pid_io_lines[4].split(":")[1])
                selected_process_write_bytes = int(proc_pid_io_lines[5].split(":")[1])
                selected_process_read_count = int(proc_pid_io_lines[2].split(":")[1])
                selected_process_write_count = int(proc_pid_io_lines[3].split(":")[1])
            # Root access is needed for reading "/proc/[PID]/io" file else it gives error. "try-except" is used in order to avoid this error if user has no root privileges.
            except PermissionError:
                selected_process_read_bytes = 0
                selected_process_write_bytes = 0
                selected_process_read_count = 0
                selected_process_write_count = 0

            # Get disk read speed, disk write speed
            disk_read_write_data = [selected_process_read_bytes, selected_process_write_bytes]
            if self.disk_read_write_data_prev == []:
                # Make process_read_bytes_prev equal to process_read_bytes for giving "0" disk read speed value if this is first loop of the process
                selected_process_read_bytes_prev = selected_process_read_bytes
            else:
                selected_process_read_bytes_prev = self.disk_read_write_data_prev[0]
            selected_process_read_speed = (selected_process_read_bytes - int(selected_process_read_bytes_prev)) / self.update_interval    # Append process_read_bytes which will be used as "process_read_bytes_prev" value in the next loop and also append disk read speed. 
            if self.disk_read_write_data_prev == []:
                # Make process_write_bytes_prev equal to process_write_bytes for giving "0" disk write speed value if this is first loop of the process 
                selected_process_write_bytes_prev = selected_process_write_bytes
            else:
                selected_process_write_bytes_prev = self.disk_read_write_data_prev[1]
            selected_process_write_speed = (selected_process_write_bytes - int(selected_process_write_bytes_prev)) / self.update_interval    # Append process_read_bytes which will be used as "process_read_bytes_prev" value in the next loop and also append disk read speed. 
            self.disk_read_write_data_prev = disk_read_write_data

            # Get process exe
            try:
                selected_process_exe = os.path.realpath("/proc/" + selected_process_pid + "/exe")
            # Executable path of some of the processes may not be get without root privileges or may not be get due to the reason of some of the processes may not have a exe file. "try-except" is used to be able to avoid errors due to these reasons.
            except Exception:
                selected_process_exe = "-"

            # Get process cwd
            try:
                selected_process_cwd = os.readlink("/proc/" + selected_process_pid + "/cwd")
            # "PermissionError" is used for processes that require root privileges for "cwd data". "FileNotFoundError" is used for zombie processes which do not have a readable "cwd" file (it has the file but it is a broken link).
            except (PermissionError, FileNotFoundError) as multiple_exception:
                selected_process_cwd = "-"

            # Get process cmdline
            with open("/proc/" + selected_process_pid + "/cmdline") as reader:
                selected_process_cmdline = reader.read().split("\x00")
            if selected_process_cmdline == [""]:
                selected_process_cmdline = "-"

            # Get open files of the process
            selected_process_open_files = []
            try:
                files_in_fd = [filename for filename in os.listdir("/proc/" + selected_process_pid + "/fd")]
                for file in files_in_fd:
                    try:
                        path = os.readlink("/proc/" + selected_process_pid + "/fd/" + file)
                        if os.path.isfile(path) == True:
                            selected_process_open_files.append(path)
                    except FileNotFoundError:
                        continue
            except PermissionError:
                pass
            if selected_process_open_files == []:
                selected_process_open_files = "-"

            # Set label text by using process data
            if selected_process_read_bytes != "-" and selected_process_write_bytes != "-":
                self.label2128w.set_text(f'{self.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_read_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
                self.label2129w.set_text(f'{self.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_write_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
                self.label2130w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_read_bytes, processes_disk_data_unit, processes_disk_data_precision)}')
                self.label2131w.set_text(f'{self.performance_data_unit_converter_func("data", "none", selected_process_write_bytes, processes_disk_data_unit, processes_disk_data_precision)}')
                self.label2132w.set_text(f'{selected_process_read_count}')
                self.label2133w.set_text(f'{selected_process_write_count}')
            if selected_process_read_bytes == "-" and selected_process_write_bytes == "-":
                self.label2128w.set_text("-")
                self.label2129w.set_text("-")
                self.label2130w.set_text("-")
                self.label2131w.set_text("-")
                self.label2132w.set_text("-")
                self.label2133w.set_text("-")
            self.label2134w.set_text(selected_process_exe)
            self.label2135w.set_text(selected_process_cwd)
            self.label2136w.set_text(' '.join(selected_process_cmdline))
            if selected_process_open_files != "-":
                self.label2137w.set_text(',\n'.join(selected_process_open_files))
            if selected_process_open_files == "-":
                self.label2137w.set_text("-")


    # ----------------------------------- Processes Details - Run Function -----------------------------------
    def process_details_run_func(self):

        if hasattr(ProcessesDetails, "update_interval") == False:
            GLib.idle_add(self.process_details_initial_func)
        if self.window2101w.get_visible() == True:
            self.update_interval = Config.update_interval
            GLib.idle_add(self.process_details_loop_func)
            GLib.timeout_add(self.update_interval * 1000, self.process_details_run_func)


    # ----------------------------------- Processes - Processes No Such Process Error Dialog Function -----------------------------------
    def processes_no_such_process_error_dialog(self, selected_process_name, selected_process_pid):

        error_dialog2101w = Gtk.MessageDialog(transient_for=Processes.grid2101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.ERROR,
        buttons=Gtk.ButtonsType.CLOSE, text=_tr("This process is not running anymore:"))
        error_dialog2101w.format_secondary_text(selected_process_name + " (" + _tr("PID") + ": " + selected_process_pid + ")")
        error_dialog2101w.run()
        error_dialog2101w.destroy()


# Generate object
ProcessesDetails = ProcessesDetails()


#!/usr/bin/env python3

# ----------------------------------- System - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def system_import_func():

    global Gtk, GLib, Thread, subprocess, os, time

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import subprocess
    import os
    import time


    global Config, MainGUI, SystemGUI
    import Config, MainGUI, SystemGUI


    # Import locale and gettext modules for defining translation texts which will be recognized by gettext application (will be run by programmer externally) and exported into a ".pot" file. 
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    import locale
    from locale import gettext as _tr

    # Define contstants for language translation support
    global application_name
    application_name = "system-monitoring-center"
    translation_files_path = "/usr/share/locale"
    system_current_language = os.environ.get("LANG")

    # Define functions for language translation support
    locale.bindtextdomain(application_name, translation_files_path)
    locale.textdomain(application_name)
    locale.setlocale(locale.LC_ALL, system_current_language)


# ----------------------------------- System - Loop Function (updates the system data and labels on the GUI) -----------------------------------
def system_loop_func():

    with open("/etc/os-release") as reader:
        os_release_output_lines = reader.read().strip().split("\n")
    for line in os_release_output_lines:
        if line.startswith("ID="):
            os_name = line.split("ID=")[1].strip().capitalize()
        if line.startswith("VERSION_ID="):
            os_version = line.split("VERSION_ID=")[1].strip(' "')
        if line.startswith("VERSION_CODENAME="):
            os_version_code_name = line.split("VERSION_CODENAME=")[1].strip()
        if line.startswith("ID_LIKE="):
            os_based_on = line.split("ID_LIKE=")[1].strip().capitalize()
            if os_based_on == "Debian":
                with open("/etc/debian_version") as reader:
                    debian_version = reader.read().strip()
                os_based_on = os_based_on + " (" + debian_version + ")"

    uname_output_lines = (subprocess.check_output("uname -o; uname -r", shell=True).strip()).decode().split("\n")
    kernel_release = uname_output_lines[1]

    id_output = (subprocess.check_output("id -u", shell=True).strip()).decode()
    if id_output != "0":
        current_dektop_environment = (subprocess.check_output("echo $XDG_CURRENT_DESKTOP", shell=True).strip()).decode()
    if id_output == "0":                                                                      # Code below this statement could be used without "is or is not '0'" check after further testing
        current_desktop_session = ""                                                          # Set an initial string in order to avoid errors in case of undetected current desktop session.
        pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]      # Get process PID list. PID values are appended as string values because they are used as string values in various places in the code and this ensures lower CPU usage by avoiding hundreds/thousands of times integer to string conversion.
        for pid in pid_list[:]:                                                               # "[:]" is used for iterating over copy of the list because element are removed during iteration. Otherwise incorrect operations (incorrect element removal) are performed on the list.
            try:                                                                              # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
                with open("/proc/" + pid + "/stat") as reader:                                # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
                    proc_pid_stat_lines = reader.read()
            except FileNotFoundError:                                                         # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
                pid_list.remove(pid)
                continue
            proc_pid_stat_lines_split = proc_pid_stat_lines.split()
            first_parentheses = proc_pid_stat_lines.find("(")                                 # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
            second_parentheses = proc_pid_stat_lines.rfind(")")                               # Last parantheses ")" index is get by using "find()".
            process_name_from_stat = proc_pid_stat_lines[first_parentheses+1:second_parentheses]    # Process name is get from string by using the indexes get previously.
            process_name = process_name_from_stat
            if len(process_name) >= 15:                                                       # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name. "=15" is enough but this limit may be increased in the next releases of the kernel. ">=15" is used in order to handle this possible change.
                with open("/proc/" + pid + "/cmdline") as reader:
                    process_commandline = reader.read()
                    process_name = ''.join(reader.read().split("/")[-1].split("\x00"))        # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()" and joined again without these characters.
                if process_name.startswith(process_name_from_stat) == False:
                    process_name = process_name_from_stat                                     # Root access is needed for reading "cmdline" file of the some processes. Otherwise it gives "" as output. Process name from "stat" file of the process is used is this situation. Also process name from "stat" file is used if name from "cmdline" does not start with name from "stat" file.
            if process_name == "ssh-agent":
                with open("/proc/" + pid + "/cmdline") as reader:                             # Read process commandline because it may not be read previously if process name is shorter than 15 characters.
                    process_commandline = reader.read()
                if "x-session-manager" in process_commandline.lower():
                    current_desktop_session = "XFCE"
                    break
                if "gnome-session" in process_commandline.lower():
                    current_desktop_session = "GNOME"
                    break
        current_dektop_environment = current_desktop_session
    if current_dektop_environment == "XFCE":
        current_dektop_environment_version_lines = (subprocess.check_output("xfce4-panel --version", shell=True).strip()).decode().split("\n")
        for line in current_dektop_environment_version_lines:
            if "xfce4-panel" in line:
                current_dektop_environment_version = line.split(" ")[1]
                break
    if current_dektop_environment == "GNOME":
        current_dektop_environment_version_lines = (subprocess.check_output("gnome-shell --version", shell=True).strip()).decode().split("\n")
        for line in current_dektop_environment_version_lines:
            if "GNOME Shell" in line:
                current_dektop_environment_version = line.split(" ")[2]
                break
    if current_dektop_environment != "XFCE" and current_dektop_environment != "GNOME":
            current_dektop_environment_version = _tr("Unknown")
        

    with open("/etc/X11/default-display-manager") as reader:
        current_window_manager = reader.read().strip()
        if current_window_manager.startswith("/"):                                            # Split current_window_manager with "/" if it starts with "/" character which means it is a directory.
            current_window_manager = current_window_manager.split("/")[-1]

    with open("/proc/sys/kernel/hostname") as reader:
        host_name = reader.read().strip()

    current_screen = MainGUI.window1.get_screen()
    number_of_monitors = current_screen.get_n_monitors()
    current_monitor = current_screen.get_monitor_at_window(current_screen.get_active_window())    # Get the monitor number that most of the gtk.gdk.Window is in.

    with open("/proc/uptime") as reader:
        sut_read = float(reader.read().split(" ")[0].strip())
    sut_days = sut_read/60/60/24
    sut_days_int = int(sut_days)
    sut_hours = (sut_days -sut_days_int) * 24
    sut_hours_int = int(sut_hours)
    sut_minutes = (sut_hours - sut_hours_int) * 60
    sut_minutes_int = int(sut_minutes)
    sut_seconds = (sut_minutes - sut_minutes_int) * 60
    sut_seconds_int = int(sut_seconds)

    number_of_installed_packages = len((subprocess.check_output("dpkg --list", shell=True)).decode().split("\n"))

    # Get human and root user usernames and UIDs which will be used for determining username when "pkexec_uid" is get.
    usernames_username_list = []
    usernames_uid_list = []
    with open("/etc/passwd") as reader:                                                       # "/etc/passwd" file (also knonw as Linux password database) contains all local user (system + human users) information.
        etc_passwd_lines = reader.read().strip().split("\n")                                  # "strip()" is used in order to prevent errors due to an empty line at the end of the list.
    for line in etc_passwd_lines:
        line_splitted = line.split(":")
        usernames_username_list.append(line_splitted[0])
        usernames_uid_list.append(line_splitted[2])
    # Get current username which will be used for determining configration file directory.
    global current_user_name
    current_user_name = os.environ.get('SUDO_USER')                                           # Get user name that gets root privileges. Othervise, username is get as "root" when root access is get.
    if current_user_name is None:                                                             # Get username in the following way if current application has not been run by root privileges.
        current_user_name = os.environ.get('USER')
    pkexec_uid = os.environ.get('PKEXEC_UID')
    if current_user_name == "root" and pkexec_uid != None:                                    # current_user_name is get as "None" if application is run with "pkexec" command. In this case, "os.environ.get('PKEXEC_UID')" is used to be able to get username of which user has run the application with "pkexec" command.
        current_user_name = usernames_username_list[usernames_uid_list.index(os.environ.get('PKEXEC_UID'))]

    if id_output == "0":
        have_root_access = _tr("(Yes)")
    else:
        have_root_access = _tr("(No)")


    SystemGUI.label8101.set_text(f'{os_name} {os_version}')
    SystemGUI.label8103.set_text(os_name)
    SystemGUI.label8104.set_text(f'{os_version} - {os_version_code_name}')
    SystemGUI.label8106.set_text(os_based_on)
    SystemGUI.label8107.set_text(kernel_release)
    SystemGUI.label8108.set_text(f'{current_dektop_environment} ({current_dektop_environment_version})')
    SystemGUI.label8110.set_text(current_window_manager)
    SystemGUI.label8114.set_text(host_name)
    SystemGUI.label8115.set_text(f'{number_of_monitors} - {current_monitor}')
    SystemGUI.label8116.set_text(f'{sut_days_int:02}:{sut_hours_int:02}:{sut_minutes_int:02}:{sut_seconds_int:02}')
    SystemGUI.label8117.set_text(f'{number_of_installed_packages}')
    SystemGUI.label8118.set_text(f'{current_user_name} - {have_root_access}')

# ----------------------------------- System - Initial Function (gets data and adds into labels) -----------------------------------
def system_initial_func():

    uname_output_lines = (subprocess.check_output("uname -o; uname -r", shell=True).strip()).decode().split("\n")
    os_family = uname_output_lines[0]

    id_output = (subprocess.check_output("id -u", shell=True).strip()).decode()
    if id_output != "0":
        windowing_system = (subprocess.check_output("echo $XDG_SESSION_TYPE", shell=True).strip()).decode()
    if id_output == "0":
        pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]      # Get process PID list. PID values are appended as string values because they are used as string values in various places in the code and this ensures lower CPU usage by avoiding hundreds/thousands of times integer to string conversion.
        for pid in pid_list[:]:                                                               # "[:]" is used for iterating over copy of the list because element are removed during iteration. Otherwise incorrect operations (incorrect element removal) are performed on the list.
            try:                                                                              # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
                with open("/proc/" + pid + "/stat") as reader:                                # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
                    proc_pid_stat_lines = reader.read()
            except FileNotFoundError:                                                         # Removed pid from "pid_list" and skip to next loop (pid) if process is ended just after pid_list is generated.
                pid_list.remove(pid)
                continue
            proc_pid_stat_lines_split = proc_pid_stat_lines.split()
            first_parentheses = proc_pid_stat_lines.find("(")                                 # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
            second_parentheses = proc_pid_stat_lines.rfind(")")                               # Last parantheses ")" index is get by using "find()".
            process_name_from_stat = proc_pid_stat_lines[first_parentheses+1:second_parentheses]    # Process name is get from string by using the indexes get previously.
            process_name = process_name_from_stat
            if len(process_name) >= 15:                                                       # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name. "=15" is enough but this limit may be increased in the next releases of the kernel. ">=15" is used in order to handle this possible change.
                with open("/proc/" + pid + "/cmdline") as reader:
                    process_commandline = reader.read()
                    process_name = ''.join(reader.read().split("/")[-1].split("\x00"))        # Some process names which are obtained from "cmdline" contain "\x00" and these are trimmed by using "split()" and joined again without these characters.
                if process_name.startswith(process_name_from_stat) == False:
                    process_name = process_name_from_stat                                     # Root access is needed for reading "cmdline" file of the some processes. Otherwise it gives "" as output. Process name from "stat" file of the process is used is this situation. Also process name from "stat" file is used if name from "cmdline" does not start with name from "stat" file.
            if "xorg" in process_name.lower():
                windowing_system = "x11"
                break
            else:
                windowing_system = _tr("Unknown")

    sys_devices_virtual_dmi_id_output_lines = (subprocess.check_output("cat /sys/devices/virtual/dmi/id/sys_vendor; cat /sys/devices/virtual/dmi/id/product_name; cat /sys/devices/virtual/dmi/id/chassis_type", shell=True).strip()).decode().split("\n")
    computer_vendor = sys_devices_virtual_dmi_id_output_lines[0]
    computer_model = sys_devices_virtual_dmi_id_output_lines[1]
    computer_chassis_type_value = sys_devices_virtual_dmi_id_output_lines[2]

    # For more information about computer chassis types, see: "https://docs.microsoft.com/en-us/previous-versions/tn-archive/ee156537(v=technet.10)"
    # "https://superuser.com/questions/877677/programatically-determine-if-an-script-is-being-executed-on-laptop-or-desktop"
    computer_chassis_types_dict = {1: "Other", 2: "Unknown", 3: "Desktop", 4: "Low Profile Desktop", 5: "Pizza Box", 6: "Mini Tower", 7: "Tower", 8: "Portable", 9: "Laptop",
                                   10: "Notebook", 11: "Hand Held", 12: "Docking Station", 13: "All in One", 14: "Sub Notebook", 15: "Space-Saving", 16: "Lunch Box",
                                   17: "Main System Chassis", 18: "Expansion Chassis", 19: "Sub Chassis", 20: "Bus Expansion Chassis", 21: "Peripheral Chassis",
                                   22: "Storage Chassis", 23: "Rack Mount Chassis", 24: "Sealed-Case PC"}

    computer_chassis_type = computer_chassis_types_dict[int(computer_chassis_type_value)]


    SystemGUI.label8102.set_text(f'{computer_vendor} {computer_model}')
    SystemGUI.label8105.set_text(os_family)
    SystemGUI.label8109.set_text(windowing_system)
    SystemGUI.label8111.set_text(computer_vendor)
    SystemGUI.label8112.set_text(computer_model)
    SystemGUI.label8113.set_text(computer_chassis_type)


# ----------------------------------- System Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def system_initial_thread_func():

    GLib.idle_add(system_initial_func)


# ----------------------------------- System Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def system_loop_thread_func():

    GLib.idle_add(system_loop_func)
    if MainGUI.radiobutton8.get_active() is True and MainGUI.window1.get_visible() is True:
        GLib.timeout_add(Config.update_interval * 1000, system_loop_thread_func)


# ----------------------------------- System Thread Run Function (starts execution of the threads) -----------------------------------
def system_thread_run_func():

    system_initial_thread = Thread(target=system_initial_thread_func, daemon=True)
    system_initial_thread.start()
    system_initial_thread.join()
    system_loop_thread = Thread(target=system_loop_thread_func, daemon=True)
    system_loop_thread.start()

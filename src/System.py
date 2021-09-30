#!/usr/bin/env python3

# ----------------------------------- System - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def system_import_func():

    global Gtk, GLib, Thread, subprocess, os, platform, time

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import subprocess
    import os
    import platform
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


# ----------------------------------- System - Initial Function (gets data and adds into labels) -----------------------------------
def system_initial_func():

    # Get human and root user usernames and UIDs which will be used for determining username when "pkexec_uid" is get.
    usernames_username_list = []
    usernames_uid_list = []
    with open("/etc/passwd") as reader:                                                       # "/etc/passwd" file (also knonw as Linux password database) contains all local user (system + human users) information.
        etc_passwd_lines = reader.read().strip().split("\n")                                  # "strip()" is used in order to prevent errors due to an empty line at the end of the list.
    for line in etc_passwd_lines:
        line_splitted = line.split(":")
        usernames_username_list.append(line_splitted[0])
        usernames_uid_list.append(line_splitted[2])
    # Get current username
    global current_user_name
    current_user_name = os.environ.get('SUDO_USER')                                           # Get user name that gets root privileges. Othervise, username is get as "root" when root access is get.
    if current_user_name is None:                                                             # Get username in the following way if current application has not been run by root privileges.
        current_user_name = os.environ.get('USER')
    pkexec_uid = os.environ.get('PKEXEC_UID')
    if current_user_name == "root" and pkexec_uid != None:                                    # current_user_name is get as "None" if application is run with "pkexec" command. In this case, "os.environ.get('PKEXEC_UID')" is used to be able to get username of which user has run the application with "pkexec" command.
        current_user_name = usernames_username_list[usernames_uid_list.index(os.environ.get('PKEXEC_UID'))]

    # Get os family
    os_family = platform.system()
    if os_family == "":
        os_family = "-"

    # Get kernel release (base version of kernel)
    kernel_release = platform.release()
    if kernel_release == "":
        kernel_release = "-"

    # Get kernel version (package version of kernel))
    kernel_version = platform.version()
    if kernel_version == "":
        kernel_version = "-"

    # Get windowing system
    global windowing_system
    windowing_system = os.environ.get('XDG_SESSION_TYPE')
    if windowing_system != None:
        windowing_system = windowing_system.capitalize()
    if windowing_system == None:
        windowing_system = _tr("Unknown")                                                     # Initial value of "windowing_system" variable. This value will be used if "windowing_system" could not be detected.
        pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]      # Get process PID list. PID values are appended as string values because they are used as string values in various places in the code and this ensures lower CPU usage by avoiding hundreds/thousands of times integer to string conversion.
        for pid in pid_list:
            try:                                                                              # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
                with open("/proc/" + pid + "/comm") as reader:
                    process_name = reader.read().strip()
            except FileNotFoundError:
                continue
            if process_name.lower() == "xorg":
                windowing_system = "X11"
                break
            if process_name.lower() == "xwayland":
                windowing_system = "Wayland"
                break

    # Get window manager
    supported_window_managers_list = ["xfwm4", "mutter", "kwin", "kwin_x11", "cinnamon", "openbox", "metacity", "marco", "compiz", "englightenment", "fvwm2", "icewm", "sawfish", "awesome"]
    global window_manager
    window_manager = "-"                                                                      # Set an initial string in order to avoid errors in case of undetected current desktop session.
    if 'pid_list' not in locals():
        pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]      # Get process PID list. PID values are appended as string values because they are used as string values in various places in the code and this ensures lower CPU usage by avoiding hundreds/thousands of times integer to string conversion.
    for pid in pid_list:
        try:                                                                                  # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
            with open("/proc/" + pid + "/comm") as reader:
                process_name = reader.read().strip()
        except FileNotFoundError:
            continue
        if process_name.lower() in supported_window_managers_list:
            try:
                with open("/proc/" + pid + "/status") as reader:                              # User name of the process owner is get from "/proc/status" file because it is not present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                    proc_pid_status_lines = reader.read().split("\n")
            except FileNotFoundError:
                continue
            for line in proc_pid_status_lines:
                if "Uid:\t" in line:
                    real_user_id = line.split(":")[1].split()[0].strip()                      # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                    process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
            if process_username == current_user_name:
                window_manager = process_name.lower()
                break

    # Get current desktop environment
    current_desktop_environment = os.environ.get('XDG_CURRENT_DESKTOP')
    if current_desktop_environment == None:
        current_desktop_session = "-"                                                         # Set an initial string in order to avoid errors in case of undetected current desktop session.
        for pid in pid_list:
            try:                                                                              # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
                with open("/proc/" + pid + "/comm") as reader:
                    process_name = reader.read().strip()
                with open("/proc/" + pid + "/status") as reader:                              # User name of the process owner is get from "/proc/status" file because it is not present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                    proc_pid_status_lines = reader.read().split("\n")
            except FileNotFoundError:
                continue
            for line in proc_pid_status_lines:
                if "Uid:\t" in line:
                    real_user_id = line.split(":")[1].split()[0].strip()                      # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                    process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
            if process_username == current_user_name:
                if process_name == "xfce4-session":
                    current_desktop_session = "XFCE"
                if process_name == "gnome-session-b":
                    current_desktop_session = "GNOME"
                if process_name == "cinnamon-session":
                    current_desktop_session = "X-Cinnamon"                                    # Cinnamon dektop environment accepts both "X-Cinnamon" and "CINNAMON" names in the .desktop files.
                if process_name == "mate-session":
                    current_desktop_session = "MATE"
                if process_name == "plasmashell":
                    current_desktop_session = "KDE"
                if process_name == "lxqt-session":
                    current_desktop_session = "LXQt"
                if process_name == "lxsession":
                    current_desktop_session = "LXDE"
        current_desktop_environment = current_desktop_session

    # Get current desktop environment version
    supported_desktop_environments_list = ["XFCE", "GNOME", "X-Cinnamon", "CINNAMON", "MATE", "KDE", "LXQt", "LXDE"]    # Cinnamon dektop environment accepts both "X-Cinnamon" and "CINNAMON" names in the .desktop files.
    current_desktop_environment_version = _tr("Unknown")                                                                # Set initial value of the "current_desktop_environment_version". This value will be used if it could not be detected.
    if current_desktop_environment == "XFCE":
        current_desktop_environment_version_lines = (subprocess.check_output("xfce4-panel --version", shell=True).strip()).decode().split("\n")
        for line in current_desktop_environment_version_lines:
            if "xfce4-panel" in line:
                current_desktop_environment_version = line.split(" ")[1]
    if current_desktop_environment == "GNOME":
        current_desktop_environment_version_lines = (subprocess.check_output("gnome-shell --version", shell=True).strip()).decode().split("\n")
        for line in current_desktop_environment_version_lines:
            if "GNOME Shell" in line:
                current_desktop_environment_version = line.split(" ")[2]
    if current_desktop_environment == "X-Cinnamon" or current_desktop_environment == "CINNAMON":
        current_desktop_environment_version = (subprocess.check_output("cinnamon --version", shell=True).strip()).decode().split(" ")[-1]
    if current_desktop_environment == "MATE":
        current_desktop_environment_version = (subprocess.check_output("mate-about --version", shell=True).strip()).decode().split(" ")[-1]
    if current_desktop_environment == "KDE":
        current_desktop_environment_version = (subprocess.check_output("plasmashell --version", shell=True).strip()).decode()
    if current_desktop_environment == "LXQt":
        current_desktop_environment_version_lines = (subprocess.check_output("lxqt-about --version", shell=True).strip()).decode()
        for line in current_desktop_environment_version_lines:
            if "liblxqt" in line:
                current_desktop_environment_version = line.split()[1].strip()

    # Get current display manager
    with open("/etc/X11/default-display-manager") as reader:
        current_display_manager = reader.read().strip()
        if current_display_manager.startswith("/"):                                           # Split current_display_manager with "/" if it starts with "/" character which means it is a directory.
            current_display_manager = current_display_manager.split("/")[-1]

    # Get computer vendor, model, chassis information
    with open("/sys/devices/virtual/dmi/id/sys_vendor") as reader:
        computer_vendor = reader.read().strip()
    with open("/sys/devices/virtual/dmi/id/product_name") as reader:
        computer_model = reader.read().strip()
    with open("/sys/devices/virtual/dmi/id/chassis_type") as reader:
        computer_chassis_type_value = reader.read().strip()

    # For more information about computer chassis types, see: "https://docs.microsoft.com/en-us/previous-versions/tn-archive/ee156537(v=technet.10)"
    # "https://superuser.com/questions/877677/programatically-determine-if-an-script-is-being-executed-on-laptop-or-desktop"
    computer_chassis_types_dict = {1: "Other", 2: "Unknown", 3: "Desktop", 4: "Low Profile Desktop", 5: "Pizza Box", 6: "Mini Tower", 7: "Tower", 8: "Portable", 9: "Laptop",
                                   10: "Notebook", 11: "Hand Held", 12: "Docking Station", 13: "All in One", 14: "Sub Notebook", 15: "Space-Saving", 16: "Lunch Box",
                                   17: "Main System Chassis", 18: "Expansion Chassis", 19: "Sub Chassis", 20: "Bus Expansion Chassis", 21: "Peripheral Chassis",
                                   22: "Storage Chassis", 23: "Rack Mount Chassis", 24: "Sealed-Case PC"}
    computer_chassis_type = computer_chassis_types_dict[int(computer_chassis_type_value)]


    # Set label texts to show information
    SystemGUI.label8102.set_text(f'{computer_vendor} {computer_model}')
    SystemGUI.label8105.set_text(os_family)
    SystemGUI.label8107.set_text(kernel_release)
    SystemGUI.label8108.set_text(kernel_version)
    SystemGUI.label8109.set_text(f'{current_desktop_environment} ({current_desktop_environment_version})')
    SystemGUI.label8110.set_text(windowing_system)
    SystemGUI.label8111.set_text(window_manager)
    SystemGUI.label8112.set_text(current_display_manager)
    SystemGUI.label8113.set_text(computer_vendor)
    SystemGUI.label8114.set_text(computer_model)
    SystemGUI.label8115.set_text(computer_chassis_type)


# ----------------------------------- System - Loop Function (updates the system data and labels on the GUI) -----------------------------------
def system_loop_func():

    # Get OS name, version, version code name and OS based on information
    with open("/etc/os-release") as reader:
        os_release_output_lines = reader.read().strip().split("\n")
    os_based_on = "-"                                                                         # Initial value of "os_based_on" variable. This value will be used if "os_based_on" could not be detected (For example, "ID_LIKE" value is not present in "/etc/os-release" file if OS is "Debian").
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

    with open("/proc/sys/kernel/hostname") as reader:
        host_name = reader.read().strip()

    # Get number of monitors and current monitor
    current_monitor = "-"                                                                             # Initial value of "current_monitor" variable. This value will be used if "current_monitor" could not be detected ("current_screen" could not be get on system which run Wayland. But could be detected on systems which run X11.)..
    current_screen = MainGUI.window1.get_screen()
    number_of_monitors = current_screen.get_n_monitors()
    if windowing_system.lower() == "x11":
        current_monitor = current_screen.get_monitor_at_window(current_screen.get_active_window())    # Get the monitor number that most of the gtk.gdk.Window is in.

    # Get system up time
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

    # Get number of installed packages
    number_of_installed_packages = len((subprocess.check_output("dpkg --list", shell=True)).decode().split("\n"))

    # Get if current user has root privileges
    if os.geteuid() == 0:
        have_root_access = _tr("(Yes)")
    else:
        have_root_access = _tr("(No)")


    # Set label texts to show information
    SystemGUI.label8101.set_text(f'{os_name} {os_version}')
    SystemGUI.label8103.set_text(os_name)
    SystemGUI.label8104.set_text(f'{os_version} - {os_version_code_name}')
    SystemGUI.label8106.set_text(os_based_on)
    SystemGUI.label8116.set_text(host_name)
    SystemGUI.label8117.set_text(f'{number_of_monitors}')
    SystemGUI.label8118.set_text(f'{current_monitor}')
    SystemGUI.label8119.set_text(f'{sut_days_int:02}:{sut_hours_int:02}:{sut_minutes_int:02}:{sut_seconds_int:02}')
    SystemGUI.label8120.set_text(f'{number_of_installed_packages}')
    SystemGUI.label8121.set_text(f'{current_user_name} - {have_root_access}')


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

#!/usr/bin/env python3

# ----------------------------------- System - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def system_import_func():

    global Gtk, GLib, Thread, subprocess, os, platform, time, pkg_resources

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import subprocess
    import os
    import platform
    import time
    import pkg_resources


    global Config, MainGUI
    from . import Config, MainGUI


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


# ----------------------------------- System - System GUI Function (the code of this module in order to avoid running them during module import and defines "System" tab GUI objects and functions/signals) -----------------------------------
def system_gui_func():

    # System tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/SystemTab.ui")

    # System tab GUI objects
    global grid8101
    global button8101
    global label8101, label8102, label8103, label8104, label8105, label8106, label8107, label8108, label8109, label8110
    global label8111, label8112, label8113, label8114, label8115, label8116, label8117, label8118, label8119, label8120
    global label8121, label8122

    # System tab GUI objects - get
    grid8101 = builder.get_object('grid8101')
    button8101 = builder.get_object('button8101')
    label8101 = builder.get_object('label8101')
    label8102 = builder.get_object('label8102')
    label8103 = builder.get_object('label8103')
    label8104 = builder.get_object('label8104')
    label8105 = builder.get_object('label8105')
    label8106 = builder.get_object('label8106')
    label8107 = builder.get_object('label8107')
    label8108 = builder.get_object('label8108')
    label8109 = builder.get_object('label8109')
    label8110 = builder.get_object('label8110')
    label8111 = builder.get_object('label8111')
    label8112 = builder.get_object('label8112')
    label8113 = builder.get_object('label8113')
    label8114 = builder.get_object('label8114')
    label8115 = builder.get_object('label8115')
    label8116 = builder.get_object('label8116')
    label8117 = builder.get_object('label8117')
    label8118 = builder.get_object('label8118')
    label8119 = builder.get_object('label8119')
    label8120 = builder.get_object('label8120')
    label8121 = builder.get_object('label8121')
    label8122 = builder.get_object('label8122')


    # System tab GUI functions
    def on_button8101_clicked(widget):                                                        # "Refresh" button
        system_initial_func()
        system_loop_func()


    # System tab GUI functions - connect
    button8101.connect("clicked", on_button8101_clicked)


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
        windowing_system = "-"                                                                # Initial value of "windowing_system" variable. This value will be used if "windowing_system" could not be detected.
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
    supported_window_managers_list = ["xfwm4", "mutter", "kwin", "kwin_x11", "cinnamon", "budgie-wm", "openbox", "metacity", "marco", "compiz", "englightenment", "fvwm2", "icewm", "sawfish", "awesome"]
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
    current_desktop_environment = os.environ.get('XDG_CURRENT_DESKTOP')                       # This command may give Budgie desktop environment as "Budgie:GNOME".
    supported_desktop_environments_process_list = ["xfce4-session", "gnome-session-b", "cinnamon-session", "mate-session", "plasmashell", "lxqt-session", "lxsession", "budgie-panel"]
    supported_desktop_environments_list = ["XFCE", "GNOME", "X-Cinnamon", "CINNAMON", "MATE", "KDE", "LXQt", "LXDE", "Budgie", "Deepin"]    # Cinnamon dektop environment accepts both "X-Cinnamon" and "CINNAMON" names in the .desktop files.
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
            if process_name in supported_desktop_environments_process_list:
                for line in proc_pid_status_lines:
                    if "Uid:\t" in line:
                        real_user_id = line.split(":")[1].split()[0].strip()                  # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                        process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
                if process_username == current_user_name:
                    if process_name == "xfce4-session":
                        current_desktop_session = "XFCE"
                        break
                    if process_name == "gnome-session-b":
                        current_desktop_session = "GNOME"
                        break
                    if process_name == "cinnamon-session":
                        current_desktop_session = "X-Cinnamon"                                # Cinnamon dektop environment accepts both "X-Cinnamon" and "CINNAMON" names in the .desktop files.
                        break
                    if process_name == "mate-session":
                        current_desktop_session = "MATE"
                        break
                    if process_name == "plasmashell":
                        current_desktop_session = "KDE"
                        break
                    if process_name == "lxqt-session":
                        current_desktop_session = "LXQt"
                        break
                    if process_name == "lxsession":
                        current_desktop_session = "LXDE"
                        break
                    if process_name == "budgie-panel":                                        # This control for Budgie desktop have to be made after contrl of "gnome-session-b" process. Because "budgie-panel" process is child process of "gnome-session-b" process.
                        current_desktop_session = "Budgie"
                        break
                    if process_name == "dde-desktop":
                        current_desktop_session = "Deepin"
                        break
                current_desktop_environment = current_desktop_session

    # Get current desktop environment version
    current_desktop_environment_version = "-"                                                 # Set initial value of the "current_desktop_environment_version". This value will be used if it could not be detected.
    if current_desktop_environment == "XFCE":
        current_desktop_environment_version_lines = (subprocess.check_output(["xfce4-panel", "--version"], shell=False)).decode().strip().split("\n")
        for line in current_desktop_environment_version_lines:
            if "xfce4-panel" in line:
                current_desktop_environment_version = line.split(" ")[1]
    if current_desktop_environment == "GNOME" or current_desktop_environment == "zorin:GNOME" or current_desktop_environment == "ubuntu:GNOME":
        current_desktop_environment_version_lines = (subprocess.check_output(["gnome-shell", "--version"], shell=False)).decode().strip().split("\n")
        for line in current_desktop_environment_version_lines:
            if "GNOME Shell" in line:
                current_desktop_environment_version = line.split(" ")[-1]
    if current_desktop_environment == "X-Cinnamon" or current_desktop_environment == "CINNAMON":
        current_desktop_environment_version = (subprocess.check_output(["cinnamon", "--version"], shell=False)).decode().strip().split(" ")[-1]
    if current_desktop_environment == "MATE":
        current_desktop_environment_version = (subprocess.check_output(["mate-about", "--version"], shell=False)).decode().strip().split(" ")[-1]
    if current_desktop_environment == "KDE":
        current_desktop_environment_version = (subprocess.check_output(["plasmashell", "--version"], shell=False)).decode().strip()
    if current_desktop_environment == "LXQt":
        current_desktop_environment_version_lines = (subprocess.check_output(["lxqt-about", "--version"], shell=False)).decode().strip()
        for line in current_desktop_environment_version_lines:
            if "liblxqt" in line:
                current_desktop_environment_version = line.split()[1].strip()
    if current_desktop_environment == "Budgie" or current_desktop_environment == "Budgie:GNOME":
        current_desktop_environment_version = (subprocess.check_output(["budgie-desktop", "--version"], shell=False)).decode().strip().split("\n")[0].strip().split(" ")[-1]

    # Get current display manager
    supported_display_managers_list = ["lightdm", "gdm", "gdm3", "sddm", "xdm", "lxdm"]
    supported_display_managers_process_list = ["lightdm", "gdm", "gdm3", "sddm", "xdm", "lxdm-binary"]
    current_display_manager = "-"                                                             # Set an initial string in order to avoid errors in case of undetected current display manager.
    for pid in pid_list:
        try:                                                                                  # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
            with open("/proc/" + pid + "/comm") as reader:
                process_name = reader.read().strip()
            with open("/proc/" + pid + "/status") as reader:                                  # User name of the process owner is get from "/proc/status" file because it is not present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                proc_pid_status_lines = reader.read().split("\n")
        except FileNotFoundError:
            continue
        if process_name in supported_display_managers_process_list:
            for line in proc_pid_status_lines:
                if "Uid:\t" in line:
                    real_user_id = line.split(":")[1].split()[0].strip()                      # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                    process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
            if process_username == "root":                                                    # Display manager processes are owned by root user.
                if process_name == "lightdm":
                    current_display_manager = "lightdm"
                    break
                if process_name == "gdm":
                    current_display_manager = "gdm"
                    break
                if process_name == "gdm3":
                    current_display_manager = "gdm3"
                    break
                if process_name == "sddm":
                    current_display_manager = "sddm"
                    break
                if process_name == "xdm":
                    current_display_manager = "xdm"
                    break
                if process_name == "lxdm-binary":
                    current_display_manager = "lxdm"
                    break

    # Get computer vendor, model, chassis information
    try:                                                                                      # This information may not be available on some systems such as ARM CPU used motherboards.
        with open("/sys/devices/virtual/dmi/id/sys_vendor") as reader:
            computer_vendor = reader.read().strip()
    except FileNotFoundError:
        computer_vendor = "-"
    try:                                                                                      # This information may not be available on some systems such as ARM CPU used motherboards.
        with open("/sys/devices/virtual/dmi/id/product_name") as reader:
            computer_model = reader.read().strip()
    except FileNotFoundError:
        computer_model = "-"
    try:                                                                                      # This information may not be available on some systems such as ARM CPU used motherboards.
        with open("/sys/devices/virtual/dmi/id/chassis_type") as reader:
            computer_chassis_type_value = reader.read().strip()
    except FileNotFoundError:
        computer_chassis_type_value = 2

    # For more information about computer chassis types, see: "https://docs.microsoft.com/en-us/previous-versions/tn-archive/ee156537(v=technet.10)"
    # "https://superuser.com/questions/877677/programatically-determine-if-an-script-is-being-executed-on-laptop-or-desktop"
    computer_chassis_types_dict = {1: "Other", 2: "Unknown", 3: "Desktop", 4: "Low Profile Desktop", 5: "Pizza Box", 6: "Mini Tower", 7: "Tower", 8: "Portable", 9: "Laptop",
                                   10: "Notebook", 11: "Hand Held", 12: "Docking Station", 13: "All in One", 14: "Sub Notebook", 15: "Space-Saving", 16: "Lunch Box",
                                   17: "Main System Chassis", 18: "Expansion Chassis", 19: "Sub Chassis", 20: "Bus Expansion Chassis", 21: "Peripheral Chassis",
                                   22: "Storage Chassis", 23: "Rack Mount Chassis", 24: "Sealed-Case PC"}
    computer_chassis_type = computer_chassis_types_dict[int(computer_chassis_type_value)]

    # Determine package types used on the system. This information will be used for getting number of installed packages on the system.
    global apt_packages_available, rpm_packages_available, pacman_packages_available, flatpak_packages_available
    apt_packages_available = "-"                                                              # Initial value of the variable.
    rpm_packages_available = "-"
    pacman_packages_available = "-"
    flatpak_packages_available = "-"
    try:
        apt_packages_available = (subprocess.check_output(["dpkg", "--list"], shell=False)).decode().strip().count("\nii  ")
        if apt_packages_available > 0:
            apt_packages_available = "yes"
    except FileNotFoundError:                                                                 # It gives "FileNotFoundError" if first element of the command (program name) can not be found on the system. It gives "subprocess.CalledProcessError" if there are any errors relevant with the parameters (commands later than the first one).
        apt_packages_available = "no"
    try:
        rpm_packages_available = (subprocess.check_output(["rpm", "-qa"], shell=False)).decode().strip().split("\n")
        rpm_packages_available = len(rpm_packages_available) - rpm_packages_available.count("")    # Differentiate empty line count
        if rpm_packages_available > 0:
            rpm_packages_available = "yes"
    except FileNotFoundError:
        rpm_packages_available = "no"
    try:
        pacman_packages_available = (subprocess.check_output(["pacman", "-Qq"], shell=False)).decode().strip().split("\n")
        pacman_packages_available = len(pacman_packages_available) - pacman_packages_available.count("")    # Differentiate empty line count
        if pacman_packages_available > 0:
            pacman_packages_available = "yes"
    except FileNotFoundError:
        pacman_packages_available = "no"
    try:
        flatpak_packages_available = (subprocess.check_output(["flatpak", "list"], shell=False)).decode().strip().split("\n")
        flatpak_packages_available = len(flatpak_packages_available) - flatpak_packages_available.count("")    # Differentiate empty line count
        if flatpak_packages_available > 0:
            flatpak_packages_available = "yes"
    except FileNotFoundError:
        flatpak_packages_available = "no"

    # Delete global "number_of_installed_rpm_packages" variable before loop function.
    try:
        global number_of_installed_rpm_packages
        del number_of_installed_rpm_packages                                                  # Global "number_of_installed_rpm_packages" variable is deleted in order to get its value if user clicks on "Refresh" button on System tab. Because presence of this variable in "globals()" is contolled on every loop in order to avoid getting its value in every loop (for avoiding very high CPU usage).
    except NameError:
        pass


    # Set label texts to show information
    label8102.set_text(f'{computer_vendor} - {computer_model}')
    label8105.set_text(os_family)
    label8107.set_text(kernel_release)
    label8108.set_text(kernel_version)
    label8109.set_text(f'{current_desktop_environment} ({current_desktop_environment_version})')
    label8110.set_text(windowing_system)
    label8111.set_text(window_manager)
    label8112.set_text(current_display_manager)
    label8113.set_text(computer_vendor)
    label8114.set_text(computer_model)
    label8115.set_text(computer_chassis_type)


# ----------------------------------- System - Loop Function (updates the system data and labels on the GUI) -----------------------------------
def system_loop_func():

    # Get OS name, version, version code name and OS based on information
    with open("/etc/os-release") as reader:
        os_release_output_lines = reader.read().strip().split("\n")
    for line in os_release_output_lines:
        if line.startswith("ID="):
            os_name = line.split("ID=")[1].strip().title()                                    # ".title()" capitalizes each word in the string.
        if line.startswith("VERSION_ID="):
            os_version = line.split("VERSION_ID=")[1].strip(' "')
        if line.startswith("VERSION_CODENAME="):
            os_version_code_name = line.split("VERSION_CODENAME=")[1].strip(' "')
        if line.startswith("ID_LIKE="):
            os_based_on = line.split("ID_LIKE=")[1].strip().title()                           # ".title()" capitalizes each word in the string.
    if 'os_based_on' not in locals() or os_based_on == "-":                                   # Set variable value as "-" in case of its value is not get so far.
        os_based_on = "-"
    if 'os_version' not in locals() or os_version == "-":
        os_version = "-"
    if 'os_version_code_name' not in locals() or os_version_code_name == "-":
        os_version_code_name = "-"
    if 'os_based_on' in locals() and os_based_on == "Debian":
        with open("/etc/debian_version") as reader:
            debian_version = reader.read().strip()
        os_based_on = os_based_on + " (" + debian_version + ")"

    with open("/proc/sys/kernel/hostname") as reader:
        host_name = reader.read().strip()

    # Get number of monitors and current monitor
    current_monitor = "-"                                                                     # Initial value of "current_monitor" variable. This value will be used if "current_monitor" could not be detected ("current_screen" could not be get on system which run Wayland. But could be detected on systems which run X11.)..
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

    global apt_packages_available, rpm_packages_available, pacman_packages_available, flatpak_packages_available
    number_of_installed_apt_or_rpm_or_pacman_packages = "-"
    # Get number of installed APT packages
    if apt_packages_available == "yes":
        number_of_installed_apt_packages = (subprocess.check_output(["dpkg", "--list"], shell=False)).decode().strip().count("\nii  ")
        number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_apt_packages} (APT)'

    # Get number of installed RPM packages
    if rpm_packages_available == "yes":
        if 'number_of_installed_rpm_packages' not in globals():                               # Number of installed RPM packages is not updated on every loop. Getting number of installed RPM packages consumes very high CPU usage because of the "rpm -qa" command and there is no any other solution for getting this information with low CPU usage.
            global number_of_installed_rpm_packages
            number_of_installed_rpm_packages = (subprocess.check_output(["rpm", "-qa"], shell=False)).decode().strip().split("\n")
            number_of_installed_rpm_packages = len(number_of_installed_rpm_packages) - number_of_installed_rpm_packages.count("")    # Differentiate empty line count
        number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_rpm_packages} (RPM)'

    # Get number of installed pacman packages
    if pacman_packages_available == "yes":
        number_of_installed_pacman_packages = (subprocess.check_output(["pacman", "-Qq"], shell=False)).decode().strip().split("\n")
        number_of_installed_pacman_packages = len(number_of_installed_pacman_packages) - number_of_installed_pacman_packages.count("")    # Differentiate empty line count
        number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_pacman_packages} (pacman)'

    # Get number of installed Python packages (including built-in packages)
    number_of_installed_python_packages = len([d.project_name for d in pkg_resources.working_set])

    # Get number of installed Flatpak packages
    number_of_installed_flatpak_packages = "-"                                                # Initial value of "number_of_installed_flatpak_packages" variable. This value will be used if "number_of_installed_flatpak_packages" could not be detected.
    if flatpak_packages_available == "yes":
        try:
            number_of_installed_flatpak_packages = (subprocess.check_output(["flatpak", "list"], shell=False)).decode().strip().split("\n")
            number_of_installed_flatpak_packages = len(number_of_installed_flatpak_packages) - number_of_installed_flatpak_packages.count("")    # Differentiate empty line count
        except FileNotFoundError:                                                             # "try-except" is used in order to prevent errors if Flatpak is uninstalled during run-time of this application.
            number_of_installed_flatpak_packages = "-"

    # Get if current user has root privileges
    if os.geteuid() == 0:
        have_root_access = _tr("(Yes)")
    else:
        have_root_access = _tr("(No)")


    # Set label texts to show information
    label8101.set_text(f'{os_name} - {os_version}')
    label8103.set_text(os_name)
    label8104.set_text(f'{os_version} - {os_version_code_name}')
    label8106.set_text(os_based_on)
    label8116.set_text(host_name)
    label8117.set_text(f'{number_of_monitors}')
    label8118.set_text(f'{current_monitor}')
    label8119.set_text(f'{sut_days_int:02}:{sut_hours_int:02}:{sut_minutes_int:02}:{sut_seconds_int:02}')
    label8120.set_text(f'{number_of_installed_apt_or_rpm_or_pacman_packages}')
    label8121.set_text(f'{number_of_installed_python_packages} (Py) - {number_of_installed_flatpak_packages} (Fp)')
    label8122.set_text(f'{current_user_name} - {have_root_access}')


# ----------------------------------- System Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def system_initial_thread_func():

    GLib.idle_add(system_initial_func)


# ----------------------------------- System Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def system_loop_thread_func(*args):                                                           # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when a tab is switched off and on again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

    if MainGUI.radiobutton8.get_active() == True:
        global system_glib_source, update_interval                                            # GLib source variable name is defined as global to be able to destroy it if tab is switched back in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            system_glib_source.destroy()                                                      # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        system_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(system_loop_func)
        system_glib_source.set_callback(system_loop_thread_func)
        system_glib_source.attach(GLib.MainContext.default())                                 # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.


# ----------------------------------- System Thread Run Function (starts execution of the threads) -----------------------------------
def system_thread_run_func():

    if "current_user_name" not in globals():                                                  # To be able to run initial thread for only one time
        system_initial_thread = Thread(target=system_initial_thread_func, daemon=True)
        system_initial_thread.start()
        system_initial_thread.join()
    system_loop_thread = Thread(target=system_loop_thread_func(), daemon=True)
    system_loop_thread.start()

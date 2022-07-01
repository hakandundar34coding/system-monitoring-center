#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib
import subprocess
import os
import platform
import threading


# Define class
class System:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/SystemTab.ui")

        # Get GUI objects
        self.grid8101 = builder.get_object('grid8101')
        self.button8101 = builder.get_object('button8101')
        self.label8101 = builder.get_object('label8101')
        self.label8102 = builder.get_object('label8102')
        self.label8103 = builder.get_object('label8103')
        self.label8104 = builder.get_object('label8104')
        self.label8105 = builder.get_object('label8105')
        self.label8106 = builder.get_object('label8106')
        self.label8107 = builder.get_object('label8107')
        self.label8108 = builder.get_object('label8108')
        self.label8109 = builder.get_object('label8109')
        self.label8110 = builder.get_object('label8110')
        self.label8111 = builder.get_object('label8111')
        self.label8112 = builder.get_object('label8112')
        self.label8113 = builder.get_object('label8113')
        self.label8114 = builder.get_object('label8114')
        self.label8115 = builder.get_object('label8115')
        self.label8116 = builder.get_object('label8116')
        self.label8117 = builder.get_object('label8117')
        self.label8118 = builder.get_object('label8118')
        self.label8119 = builder.get_object('label8119')
        self.label8120 = builder.get_object('label8120')
        self.label8121 = builder.get_object('label8121')
        self.label8122 = builder.get_object('label8122')
        self.spinner8101 = builder.get_object('spinner8101')

        # Connect GUI signals
        self.button8101.connect("clicked", self.on_button8101_clicked)

        # "0" value of "initial_already_run" variable means that initial function is not run before or tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    # ----------------------- "Refresh" Button -----------------------
    def on_button8101_clicked(self, widget):

        # Start spinner animation and show it before running the function for getting information.
        self.spinner8101.start()
        self.spinner8101.show()
        GLib.idle_add(self.system_initial_func)


    # ----------------------- System - Initial Function -----------------------
    def system_initial_func(self):

        # Get information.
        os_name, os_version, os_based_on = self.system_os_name_version_codename_based_on_func()
        os_family = self.system_os_family_func()
        kernel_release, kernel_version = self.system_kernel_release_kernel_version_func()
        cpu_architecture = self.system_cpu_architecture_func()
        computer_vendor, computer_model, computer_chassis_type = self.system_computer_vendor_model_chassis_type_func()
        host_name = self.system_host_name_func()
        number_of_monitors = self.system_number_of_monitors_func()
        number_of_installed_flatpak_packages = self.system_installed_flatpak_packages_func()
        current_python_version, current_gtk_version = self.system_current_python_version_gtk_version_func()
        current_desktop_environment, current_desktop_environment_version, windowing_system, window_manager, current_display_manager = self.system_desktop_environment_and_version_windowing_system_window_manager_display_manager_func()
        # Run this function in a separate thread because it may take a long time (2-3 seconds) to get the information on some systems (such as rpm based systems) and it blocks the GUI during this process if a separate thread is not used.
        threading.Thread(target=self.system_installed_apt_rpm_pacman_packages_func, daemon=True).start()


        # Set label texts to show information
        self.label8101.set_text(f'{os_name} - {os_version}')
        self.label8102.set_text(f'{computer_vendor} - {computer_model}')
        self.label8103.set_text(os_name)
        self.label8104.set_text(os_version)
        self.label8105.set_text(os_family)
        self.label8106.set_text(os_based_on)
        self.label8107.set_text(kernel_release)
        self.label8108.set_text(kernel_version)
        self.label8109.set_text(f'{current_desktop_environment} ({current_desktop_environment_version})')
        self.label8110.set_text(windowing_system)
        self.label8111.set_text(window_manager)
        self.label8112.set_text(current_display_manager)
        self.label8113.set_text(computer_vendor)
        self.label8114.set_text(computer_model)
        self.label8115.set_text(computer_chassis_type)
        self.label8116.set_text(host_name)
        self.label8117.set_text(cpu_architecture)
        self.label8118.set_text(f'{number_of_monitors}')
        #self.label8119.set_text(f'{number_of_installed_apt_or_rpm_or_pacman_packages}')
        self.label8120.set_text(f'{number_of_installed_flatpak_packages}')
        self.label8121.set_text(current_gtk_version)
        self.label8122.set_text(f'{current_python_version}')

        self.initial_already_run = 1


    # ----------------------- Set spinner properties and show "number_of_installed_apt_or_rpm_or_pacman_packages" information on the label -----------------------
    def system_set_number_of_installed_apt_or_rpm_or_pacman_packages_label_func(self, number_of_installed_apt_or_rpm_or_pacman_packages):

        # Stop spinner animation and hide it after running the function for getting information.
        self.spinner8101.stop()
        self.spinner8101.hide()
        self.label8119.set_text(f'{number_of_installed_apt_or_rpm_or_pacman_packages}')


    # ----------------------- Get OS name, version, version code name and OS based on information -----------------------
    def system_os_name_version_codename_based_on_func(self):

        # Initial value of "os_name" variable. This value will be used if "os_name" could not be detected.
        os_name = "-"
        os_based_on = "-"
        os_version = "-"

        # Get OS name, version and based on information.
        with open("/etc/os-release") as reader:
            os_release_output_lines = reader.read().strip().split("\n")

        for line in os_release_output_lines:
            if line.startswith("NAME="):
                os_name = line.split("NAME=")[1].strip(' "')
                continue
            if line.startswith("VERSION="):
                os_version = line.split("VERSION=")[1].strip(' "')
                continue
            if line.startswith("ID_LIKE="):
                os_based_on = line.split("ID_LIKE=")[1].strip(' "').title()
                continue

        # Append Debian version to the based on information if OS is based on Debian.
        if os_based_on == "Debian":
            debian_version = "-"
            with open("/etc/debian_version") as reader:
                debian_version = reader.read().strip()
            os_based_on = os_based_on + " (" + debian_version + ")"

        # Append Ubuntu version to the based on information if OS is based on Ubuntu.
        if os_based_on == "Ubuntu":
            ubuntu_version = "-"
            for line in os_release_output_lines:
                if line.startswith("UBUNTU_CODENAME="):
                    ubuntu_version = line.split("UBUNTU_CODENAME=")[1].strip(' "')
                    break
            os_based_on = os_based_on + " (" + ubuntu_version + ")"

        # Get Image version and use it as OS version for ArchLinux.
        if os_name.lower() == "arch linux":
            for line in os_release_output_lines:
                if line.startswith("IMAGE_VERSION="):
                    os_version = "Image Version: " + line.split("IMAGE_VERSION=")[1].strip(' "')
                    break

        return os_name, os_version, os_based_on


    # ----------------------- Get OS family -----------------------
    def system_os_family_func(self):

        # Get os family
        os_family = platform.system()
        if os_family == "":
            os_family = "-"

        return os_family


    # ----------------------- Get kernel release (base version of kernel) and kernel version (package version of kernel) -----------------------
    def system_kernel_release_kernel_version_func(self):

        # Get kernel release (base version of kernel)
        kernel_release = platform.release()
        if kernel_release == "":
            kernel_release = "-"

        # Get kernel version (package version of kernel)
        kernel_version = platform.version()
        if kernel_version == "":
            kernel_version = "-"

        return kernel_release, kernel_version


    # ----------------------- Get CPU architecture -----------------------
    def system_cpu_architecture_func(self):

        cpu_architecture = platform.processor()
        if cpu_architecture == "":
            cpu_architecture = platform.machine()
            if cpu_architecture == "":
                cpu_architecture = "-"

        return cpu_architecture


    # ----------------------- Get computer vendor, model and chassis type -----------------------
    def system_computer_vendor_model_chassis_type_func(self):

        # Get computer vendor ("/sys/devices/virtual/dmi" is used for UEFI/ACPI systems and not found on ARM systems)
        #, model, chassis information (These informations may not be available on some systems such as ARM CPU used motherboards).
        try:
            with open("/sys/devices/virtual/dmi/id/sys_vendor") as reader:
                computer_vendor = reader.read().strip()
        except FileNotFoundError:
            computer_vendor = "-"

        # Get computer model ("/sys/devices/virtual/dmi" is used for UEFI/ACPI systems and not found on ARM systems)
        try:
            with open("/sys/devices/virtual/dmi/id/product_name") as reader:
                computer_model = reader.read().strip()
        except FileNotFoundError:
            # Try to get computer model for ARM systems.
            try:
                # "/proc/device-tree/model" is a symlink to "/sys/firmware/devicetree/base/model" and using it is safer. For details: https://github.com/torvalds/linux/blob/v5.9/Documentation/ABI/testing/sysfs-firmware-ofw
                with open("/proc/device-tree/model") as reader:
                    computer_model = reader.read().strip()
            except FileNotFoundError:
                computer_model = "-"

        # Get computer chassis ("/sys/devices/virtual/dmi" is used for UEFI/ACPI systems and not found on ARM systems)
        try:
            with open("/sys/devices/virtual/dmi/id/chassis_type") as reader:
                computer_chassis_type_value = reader.read().strip()
        except FileNotFoundError:
            computer_chassis_type_value = 2

        # For more information about computer chassis types, see: "https://www.dmtf.org/standards/SMBIOS"
        # "https://superuser.com/questions/877677/programatically-determine-if-an-script-is-being-executed-on-laptop-or-desktop"
        computer_chassis_types_dict = {1: "Other", 2: "Unknown", 3: "Desktop", 4: "Low Profile Desktop", 5: "Pizza Box", 6: "Mini Tower", 7: "Tower", 8: "Portable", 9: "Laptop",
                                       10: "Notebook", 11: "Hand Held", 12: "Docking Station", 13: "All in One", 14: "Sub Notebook", 15: "Space-Saving", 16: "Lunch Box",
                                       17: "Main System Chassis", 18: "Expansion Chassis", 19: "Sub Chassis", 20: "Bus Expansion Chassis", 21: "Peripheral Chassis",
                                       22: "Storage Chassis", 23: "Rack Mount Chassis", 24: "Sealed-Case PC", 25: "Multi-system chassis", 26: "Compact PCI", 27: "Advanced TCA",
                                       28: "Blade", 29: "Blade Enclosure", 30: "Tablet", 31: "Convertible", 32: "Detachable", 33: "IoT Gateway", 34: "Embedded PC",
                                       35: "Mini PC", 36: "Stick PC"}
        computer_chassis_type = computer_chassis_types_dict[int(computer_chassis_type_value)]

        return computer_vendor, computer_model, computer_chassis_type


    # ----------------------- Get host name -----------------------
    def system_host_name_func(self):

        with open("/proc/sys/kernel/hostname") as reader:
            host_name = reader.read().strip()

        return host_name


    # ----------------------- Get number of monitors -----------------------
    def system_number_of_monitors_func(self):

        current_screen = self.label8101.get_toplevel().get_screen()
        number_of_monitors = current_screen.get_n_monitors()

        return number_of_monitors


    # ----------------------- Get number of installed Flatpak packages (and runtimes) -----------------------
    def system_installed_flatpak_packages_func(self):

        number_of_installed_flatpak_packages = "-"
        try:
            flatpak_packages_available = (subprocess.check_output(["flatpak", "list"], shell=False)).decode().strip().split("\n")
            # Differentiate empty line count
            number_of_installed_flatpak_packages = len(flatpak_packages_available) - flatpak_packages_available.count("")
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            number_of_installed_flatpak_packages = "-"

        return number_of_installed_flatpak_packages


    # ----------------------- Get current Python version and GTK version -----------------------
    def system_current_python_version_gtk_version_func(self):

        # Get current Python version (Python which is running this code)
        current_python_version = platform.python_version()

        # Get Gtk version which is used for this application.
        current_gtk_version = f'{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}'

        return current_python_version, current_gtk_version


    # ----------------------- Get number of installed APT, RPM or pacman packages -----------------------
    def system_installed_apt_rpm_pacman_packages_func(self):

        # Initial value of the variables.
        apt_packages_available = "-"
        rpm_packages_available = "-"
        pacman_packages_available = "-"
        number_of_installed_apt_or_rpm_or_pacman_packages = "-"

        try:
            # Check if "python3" is installed in order to determine package type of the system.
            apt_packages_available = (subprocess.check_output(["dpkg", "-s", "python3"], shell=False)).decode().strip()
            if "Package: python3" in apt_packages_available:
                number_of_installed_apt_packages = (subprocess.check_output(["dpkg", "--list"], shell=False)).decode().strip().count("\nii  ")
                number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_apt_packages} (APT)'
        # It gives "FileNotFoundError" if first element of the command (program name) can not be found on the system. It gives "subprocess.CalledProcessError" if there are any errors relevant with the parameters (commands later than the first one).
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            apt_packages_available = "-"

        if apt_packages_available == "-":
            try:
                rpm_packages_available = (subprocess.check_output(["rpm", "-q", "python3"], shell=False)).decode().strip()
                if rpm_packages_available.startswith("python3-3."):
                    number_of_installed_rpm_packages = (subprocess.check_output(["rpm", "-qa"], shell=False)).decode().strip().split("\n")
                    # Differentiate empty line count
                    number_of_installed_rpm_packages = len(number_of_installed_rpm_packages) - number_of_installed_rpm_packages.count("")
                    number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_rpm_packages} (RPM)'
            except (FileNotFoundError, subprocess.CalledProcessError) as me:
                rpm_packages_available = "-"

        if apt_packages_available == "-" and rpm_packages_available == "-":
            try:
                pacman_packages_available = (subprocess.check_output(["pacman", "-Q", "python3"], shell=False)).decode().strip()
                if pacman_packages_available.startswith("python 3."):
                    number_of_installed_pacman_packages = (subprocess.check_output(["pacman", "-Qq"], shell=False)).decode().strip().split("\n")
                    # Differentiate empty line count
                    number_of_installed_pacman_packages = len(number_of_installed_pacman_packages) - number_of_installed_pacman_packages.count("")
                    number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_pacman_packages} (pacman)'
            except (FileNotFoundError, subprocess.CalledProcessError) as me:
                pacman_packages_available = "-"

        # Show the information on the label by using "GLib.idle_add" in order to avoid problems (bugs, data corruption, etc.) because of threading (GTK is not thread-safe).
        GLib.idle_add(self.system_set_number_of_installed_apt_or_rpm_or_pacman_packages_label_func, number_of_installed_apt_or_rpm_or_pacman_packages)

        return number_of_installed_apt_or_rpm_or_pacman_packages


    # ----------------------- Get current desktop environment, windowing_system, window_manager, current_display_manager -----------------------
    def system_desktop_environment_and_version_windowing_system_window_manager_display_manager_func(self):

        # Get human and root user usernames and UIDs which will be used for determining username when "pkexec_uid" is get.
        usernames_username_list = []
        usernames_uid_list = []
        with open("/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")
        for line in etc_passwd_lines:
            line_splitted = line.split(":", 3)
            usernames_username_list.append(line_splitted[0])
            usernames_uid_list.append(line_splitted[2])
        # Get current username
        # Get user name that gets root privileges. Othervise, username is get as "root" when root access is get.
        current_user_name = os.environ.get('SUDO_USER')
        # Get username in the following way if current application has not been run by root privileges.
        if current_user_name is None:
            current_user_name = os.environ.get('USER')
        pkexec_uid = os.environ.get('PKEXEC_UID')
        # current_user_name is get as "None" if application is run with "pkexec" command. In this case, "os.environ.get('PKEXEC_UID')" is used to be able to get username of which user has run the application with "pkexec" command.
        if current_user_name == "root" and pkexec_uid != None:
            current_user_name = usernames_username_list[usernames_uid_list.index(os.environ.get('PKEXEC_UID'))]

        # Try to get windowing system. This value may be get as "None" if the application is run with root privileges. This value will be get by reading information of processes if it is get as "None".
        windowing_system = os.environ.get('XDG_SESSION_TYPE')
        # "windowing_system" is get as "None" if application is run with root privileges.
        if windowing_system != None:
            windowing_system = windowing_system.capitalize()

        # Try to get current desktop environment. This value may be get as "None" if the application is run with root privileges. This value will be get by reading information of processes if it is get as "None".
        # This command may give Gnome DE based DEs as "[DE_name]:GNOME". For example, "Budgie:GNOME" value is get on Budgie DE.
        current_desktop_environment = os.environ.get('XDG_CURRENT_DESKTOP')
        if current_desktop_environment == None:
            # Set an initial string in order to avoid errors in case of undetected current desktop environment (DE).
            current_desktop_environment = "-"

        # Define initial value of "windowing_system"
        if windowing_system == None:
            windowing_system = "-"

        # First values are process names of the DEs, second values are names of the DEs. Cinnamon dektop environment accepts both "X-Cinnamon" and "CINNAMON" names in the .desktop files.
        supported_desktop_environments_dict = {"xfce4-session":"XFCE", "gnome-session-b":"GNOME", "cinnamon-session":"X-Cinnamon",
                                               "mate-session":"MATE", "plasmashell":"KDE", "lxqt-session":"LXQt", "lxsession":"LXDE",
                                               "budgie-panel":"Budgie", "dde-desktop":"Deepin"}

        # Define initial value of "window_manager"
        window_manager = "-"
        supported_window_managers_list = ["xfwm4", "mutter", "kwin", "kwin_x11", "cinnamon", "budgie-wm", "openbox", "metacity", "marco", "compiz", "englightenment", "fvwm2", "icewm", "sawfish", "awesome"]

        # Define initial value of "current_display_manager"
        # First values are process names of the display managers, second values are names of the display managers.
        supported_display_managers_dict = {"lightdm":"lightdm", "gdm":"gdm", "gdm3":"gdm3", "sddm":"sddm", "xdm":"xdm", "lxdm-binary":"lxdm"}
        # Set an initial string in order to avoid errors in case of undetected current display manager.
        current_display_manager = "-"                                                             

        # Try to detect windowing system, window manager, current desktop environment and current display manager by reading process names and other details.
        pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]
        for pid in pid_list:
            # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
            try:
                with open("/proc/" + pid + "/comm") as reader:
                    process_name = reader.read().strip()
            except FileNotFoundError:
                continue
            # Get windowing system information. Windowing system may be get as "tty" (which is for non-graphical system) when "os.environ.get('XDG_SESSION_TYPE')" is used on Arch Linux.if environment variables are not set after installing a windowing system.
            if windowing_system in ["-", "Tty"]:
                if process_name.lower() == "xorg":
                    windowing_system = "X11"
                if process_name.lower() == "xwayland":
                    windowing_system = "Wayland"
            # Get window manager information
            if window_manager == "-":
                if process_name.lower() in supported_window_managers_list:
                    try:
                        # User name of the process owner is get from "/proc/status" file because it is not present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                        with open("/proc/" + pid + "/status") as reader:
                            proc_pid_status_lines = reader.read()
                    except FileNotFoundError:
                        continue
                    # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                    real_user_id = proc_pid_status_lines.split("\nUid:", 1)[1].split("\n", 1)[0].strip().split()[0].strip()
                    process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
                    if process_username == current_user_name:
                        window_manager = process_name.lower()
            # Get current display manager information
            if current_display_manager == "-":
                if process_name in supported_display_managers_dict:
                    try:
                        # User name of the process owner is get from "/proc/status" file because it is not present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                        with open("/proc/" + pid + "/status") as reader:
                            proc_pid_status_lines = reader.read()
                    except FileNotFoundError:
                        continue
                    # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                    real_user_id = proc_pid_status_lines.split("\nUid:", 1)[1].split("\n", 1)[0].strip().split()[0].strip()
                    process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
                    # Display manager processes are owned by root user.
                    if process_username == "root":
                        current_display_manager = supported_display_managers_dict[process_name]
            # Get current desktop environment information
            # "current_desktop_environment == "GNOME"" check is performed in order to detect if current DE is "Budgie DE". Because "budgie-panel" process is child process of "gnome-session-b" process.
            if current_desktop_environment == "-" or current_desktop_environment == "GNOME":
                if process_name in supported_desktop_environments_dict:
                    try:
                        # User name of the process owner is get from "/proc/status" file because it is not present in "/proc/stat" file. As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
                        with open("/proc/" + pid + "/status") as reader:
                            proc_pid_status_lines = reader.read()
                    except FileNotFoundError:
                        continue
                    # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                    real_user_id = proc_pid_status_lines.split("\nUid:", 1)[1].split("\n", 1)[0].strip().split()[0].strip()
                    process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
                    if process_username == current_user_name:
                        current_desktop_environment = supported_desktop_environments_dict[process_name]

        # Get current desktop environment version
        # Set initial value of the "current_desktop_environment_version". This value will be used if it could not be detected.
        current_desktop_environment_version = "-"
        if current_desktop_environment == "XFCE":
            try:
                current_desktop_environment_version_lines = (subprocess.check_output(["xfce4-panel", "--version"], shell=False)).decode().strip().split("\n")
                for line in current_desktop_environment_version_lines:
                    if "xfce4-panel" in line:
                        current_desktop_environment_version = line.split(" ")[1]
            except FileNotFoundError:
                pass
        if current_desktop_environment == "GNOME" or current_desktop_environment == "zorin:GNOME" or current_desktop_environment == "ubuntu:GNOME":
            try:
                current_desktop_environment_version_lines = (subprocess.check_output(["gnome-shell", "--version"], shell=False)).decode().strip().split("\n")
                for line in current_desktop_environment_version_lines:
                    if "GNOME Shell" in line:
                        current_desktop_environment_version = line.split(" ")[-1]
            except FileNotFoundError:
                pass
        if current_desktop_environment == "X-Cinnamon" or current_desktop_environment == "CINNAMON":
            try:
                current_desktop_environment_version = (subprocess.check_output(["cinnamon", "--version"], shell=False)).decode().strip().split(" ")[-1]
            except FileNotFoundError:
                pass
        if current_desktop_environment == "MATE":
            try:
                current_desktop_environment_version = (subprocess.check_output(["mate-about", "--version"], shell=False)).decode().strip().split(" ")[-1]
            except FileNotFoundError:
                pass
        if current_desktop_environment == "KDE":
            try:
                current_desktop_environment_version = (subprocess.check_output(["plasmashell", "--version"], shell=False)).decode().strip()
            except FileNotFoundError:
                pass
        if current_desktop_environment == "LXQt":
            try:
                current_desktop_environment_version_lines = (subprocess.check_output(["lxqt-about", "--version"], shell=False)).decode().strip()
                for line in current_desktop_environment_version_lines:
                    if "liblxqt" in line:
                        current_desktop_environment_version = line.split()[1].strip()
            except FileNotFoundError:
                pass
        if current_desktop_environment == "Budgie" or current_desktop_environment == "Budgie:GNOME":
            try:
                current_desktop_environment_version = (subprocess.check_output(["budgie-desktop", "--version"], shell=False)).decode().strip().split("\n")[0].strip().split(" ")[-1]
            except FileNotFoundError:
                pass

        # Get window manager for GNOME DE (GNOME DE uses mutter window manager and it not detected because it has no separate package or process.).
        if window_manager == "-":
            if current_desktop_environment.upper() == "GNOME":
                if current_desktop_environment_version.split(".")[0] in ["3", "40", "41", "42"]:
                    window_manager = "mutter"

        return current_desktop_environment, current_desktop_environment_version, windowing_system, window_manager, current_display_manager


# Generate object
System = System()


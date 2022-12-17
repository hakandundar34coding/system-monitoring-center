#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, Gdk, GLib

import subprocess
import os
import platform
import threading

from locale import gettext as _tr

from Config import Config
from MainWindow import MainWindow
import Common


class System:

    def __init__(self):

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_grid = Common.tab_grid()

        self.tab_title_grid()

        self.information_grid()


    def tab_title_grid(self):
        """
        Generate tab name, os name-version, computer vendor-model labels and refresh button.
        """

        # Grid (tab title)
        grid = Gtk.Grid()
        self.tab_grid.attach(grid, 0, 0, 1, 1)

        # Label (System)
        label = Common.tab_title_label(_tr("System"))
        grid.attach(label, 0, 0, 1, 2)

        # Label (OS name-version)
        self.os_name_version_label = Common.device_vendor_model_label()
        self.os_name_version_label.set_tooltip_text(_tr("Operating System (OS)"))
        grid.attach(self.os_name_version_label, 1, 0, 1, 1)

        # Label (computer vendor-model)
        self.computer_vendor_model_label = Common.device_kernel_name_label()
        self.computer_vendor_model_label.set_tooltip_text(_tr("Computer"))
        grid.attach(self.computer_vendor_model_label, 1, 1, 1, 1)

        # Button (tab refresh)
        self.refresh_button = Common.refresh_button(self.on_refresh_button_clicked)
        grid.attach(self.refresh_button, 2, 0, 1, 2)


    def information_grid(self):
        """
        Generate performance/information labels.
        """

        # Add viewports for showing borders around some the performance data.
        css = b"grid {border-style: solid; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
        style_provider_grid = Gtk.CssProvider()
        style_provider_grid.load_from_data(css)

        # Grid (performance/information labels)
        performance_info_grid = Gtk.Grid()
        performance_info_grid.set_column_homogeneous(True)
        performance_info_grid.set_row_homogeneous(True)
        performance_info_grid.set_column_spacing(12)
        performance_info_grid.set_row_spacing(10)
        performance_info_grid.set_margin_top(5)
        performance_info_grid.get_style_context().add_provider(style_provider_grid, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.tab_grid.attach(performance_info_grid, 0, 1, 1, 1)

        # Grid (information labels inner grid)
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_column_spacing(12)
        grid.set_row_spacing(10)
        grid.set_margin_top(6)
        grid.set_margin_bottom(6)
        grid.set_margin_start(6)
        grid.set_margin_end(6)
        performance_info_grid.attach(grid, 0, 0, 1, 1)

        # Performance information labels
        # Label - Title (Operating System (OS))
        label = Common.title_label(_tr("Operating System (OS)"))
        grid.attach(label, 0, 0, 2, 1)

        # Label (Name)
        label = Common.static_information_label(_tr("Name") + ":")
        grid.attach(label, 0, 1, 1, 1)
        # Label (Name)
        self.os_name_label = Common.dynamic_information_label()
        grid.attach(self.os_name_label, 1, 1, 1, 1)

        # Label (Version - Code Name)
        label = Common.static_information_label(_tr("Version - Code Name") + ":")
        grid.attach(label, 0, 2, 1, 1)
        # Label (Version - Code Name)
        self.version_codename_label = Common.dynamic_information_label()
        grid.attach(self.version_codename_label, 1, 2, 1, 1)

        # Label (OS Family)
        label = Common.static_information_label(_tr("OS Family") + ":")
        grid.attach(label, 0, 3, 1, 1)
        # Label (OS Family)
        self.os_family_label = Common.dynamic_information_label()
        grid.attach(self.os_family_label, 1, 3, 1, 1)

        # Label (Based On)
        label = Common.static_information_label(_tr("Based On") + ":")
        grid.attach(label, 0, 4, 1, 1)
        # Label (Based On)
        self.based_on_label = Common.dynamic_information_label()
        grid.attach(self.based_on_label, 1, 4, 1, 1)

        # Label (Kernel Release)
        label = Common.static_information_label(_tr("Kernel Release") + ":")
        grid.attach(label, 0, 5, 1, 1)
        # Label (Kernel Release)
        self.kernel_release_label = Common.dynamic_information_label()
        grid.attach(self.kernel_release_label, 1, 5, 1, 1)

        # Label (Kernel Version)
        label = Common.static_information_label(_tr("Kernel Version") + ":")
        grid.attach(label, 0, 6, 1, 1)
        # Label (Kernel Version)
        self.kernel_version_label = Common.dynamic_information_label()
        grid.attach(self.kernel_version_label, 1, 6, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        separator.set_valign(Gtk.Align.CENTER)
        grid.attach(separator, 0, 7, 4, 1)

        # Label - Title (Graphical User Interface (GUI))
        label = Common.title_label(_tr("Graphical User Interface (GUI)"))
        grid.attach(label, 0, 8, 2, 1)

        # Label (Desktop Environment)
        label = Common.static_information_label(_tr("Desktop Environment") + ":")
        grid.attach(label, 0, 9, 1, 1)
        # Label (Desktop Environment)
        self.desktop_environment_label = Common.dynamic_information_label()
        grid.attach(self.desktop_environment_label, 1, 9, 1, 1)

        # Label (Windowing System)
        label = Common.static_information_label(_tr("Windowing System") + ":")
        grid.attach(label, 0, 10, 1, 1)
        # Label (Windowing System)
        self.windowing_system_label = Common.dynamic_information_label()
        grid.attach(self.windowing_system_label, 1, 10, 1, 1)

        # Label (Window Manager)
        label = Common.static_information_label(_tr("Window Manager") + ":")
        grid.attach(label, 0, 11, 1, 1)
        # Label (Window Manager)
        self.window_manager_label = Common.dynamic_information_label()
        grid.attach(self.window_manager_label, 1, 11, 1, 1)

        # Label (Display Manager)
        label = Common.static_information_label(_tr("Display Manager") + ":")
        grid.attach(label, 0, 12, 1, 1)
        # Label (Display Manager)
        self.display_manager_label = Common.dynamic_information_label()
        grid.attach(self.display_manager_label, 1, 12, 1, 1)

        # Label - Title (Computer)
        label = Common.title_label(_tr("Computer"))
        grid.attach(label, 2, 0, 2, 1)

        # Label (Vendor)
        label = Common.static_information_label(_tr("Vendor") + ":")
        grid.attach(label, 2, 1, 1, 1)
        # Label (Vendor)
        self.vendor_label = Common.dynamic_information_label()
        grid.attach(self.vendor_label, 3, 1, 1, 1)

        # Label (Model)
        label = Common.static_information_label(_tr("Model") + ":")
        grid.attach(label, 2, 2, 1, 1)
        # Label (Model)
        self.model_label = Common.dynamic_information_label()
        grid.attach(self.model_label, 3, 2, 1, 1)

        # Label (Computer Type)
        label = Common.static_information_label(_tr("Computer Type") + ":")
        grid.attach(label, 2, 3, 1, 1)
        # Label (Computer Type)
        self.computer_type_label = Common.dynamic_information_label()
        grid.attach(self.computer_type_label, 3, 3, 1, 1)

        # Label (Name)
        label = Common.static_information_label(_tr("Name") + ":")
        grid.attach(label, 2, 4, 1, 1)
        # Label (Name)
        self.computer_name_label = Common.dynamic_information_label()
        grid.attach(self.computer_name_label, 3, 4, 1, 1)

        # Label (Architecture)
        label = Common.static_information_label(_tr("Architecture") + ":")
        grid.attach(label, 2, 5, 1, 1)
        # Label (Architecture)
        self.architecture_label = Common.dynamic_information_label()
        grid.attach(self.architecture_label, 3, 5, 1, 1)

        # Label (Number Of Monitors)
        label = Common.static_information_label(_tr("Number Of Monitors") + ":")
        grid.attach(label, 2, 6, 1, 1)
        # Label (Number Of Monitors)
        self.number_of_monitors_label = Common.dynamic_information_label()
        grid.attach(self.number_of_monitors_label, 3, 6, 1, 1)

        # There is a separator between rows 6 and 7.

        # Label - Title (Packages)
        label = Common.title_label(_tr("Packages"))
        grid.attach(label, 2, 8, 2, 1)

        # Label (System)
        label = Common.static_information_label(_tr("System") + ":")
        grid.attach(label, 2, 9, 1, 1)
        # Grid (System)
        grid_system_packages = Gtk.Grid()
        grid_system_packages.set_column_spacing(2)
        grid.attach(grid_system_packages, 3, 9, 1, 1)
        # Label (System)
        self.system_label = Common.dynamic_information_label()
        grid_system_packages.attach(self.system_label, 0, 0, 1, 1)
        # Spinner (System)
        self.spinner_system = Gtk.Spinner()
        self.spinner_system.start()
        grid_system_packages.attach(self.spinner_system, 1, 0, 1, 1)

        # Label (Flatpak)
        label = Common.static_information_label(_tr("Flatpak") + ":")
        label.set_tooltip_text(_tr("Number of installed Flatpak applications and runtimes"))
        grid.attach(label, 2, 10, 1, 1)
        # Label (Flatpak)
        self.flatpak_label = Common.dynamic_information_label()
        grid.attach(self.flatpak_label, 3, 10, 1, 1)

        # Label (GTK Version)
        label = Common.static_information_label(_tr("GTK Version") + ":")
        label.set_tooltip_text(_tr("Version for the currently running software"))
        grid.attach(label, 2, 11, 1, 1)
        # Label (GTK Version)
        self.gtk_version_label = Common.dynamic_information_label()
        grid.attach(self.gtk_version_label, 3, 11, 1, 1)

        # Label (Python Version)
        label = Common.static_information_label(_tr("Python Version") + ":")
        label.set_tooltip_text(_tr("Version for the currently running software"))
        grid.attach(label, 2, 12, 1, 1)
        # Label (Python Version)
        self.python_version_label = Common.dynamic_information_label()
        grid.attach(self.python_version_label, 3, 12, 1, 1)


    def on_refresh_button_clicked(self, widget):
        """
        Refresh data on the tab.
        """

        # Start spinner animation and show it before running the function for getting information.
        self.spinner_system.start()
        self.spinner_system.show()
        GLib.idle_add(self.system_initial_func)


    def system_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        # Get information.
        os_name, os_version, os_based_on = self.os_name_version_codename_based_on_func()
        os_family = self.os_family_func()
        kernel_release, kernel_version = self.kernel_release_kernel_version_func()
        cpu_architecture = self.cpu_architecture_func()
        computer_vendor, computer_model, computer_chassis_type = self.computer_vendor_model_chassis_type_func()
        host_name = self.host_name_func()
        number_of_monitors = self.number_of_monitors_func()
        number_of_installed_flatpak_packages = self.installed_flatpak_packages_func()
        current_python_version, current_gtk_version = self.current_python_version_gtk_version_func()
        current_desktop_environment, current_desktop_environment_version, windowing_system, window_manager, current_display_manager = self.desktop_environment_and_version_windowing_system_window_manager_display_manager_func()
        # Run this function in a separate thread because it may take a long time (2-3 seconds) to get the information on some systems (such as rpm based systems) and it blocks the GUI during this process if a separate thread is not used.
        threading.Thread(target=self.installed_apt_rpm_pacman_packages_func, daemon=True).start()


        # Set label texts to show information
        self.os_name_version_label.set_label(f'{os_name} - {os_version}')
        self.computer_vendor_model_label.set_label(f'{computer_vendor} - {computer_model}')
        self.os_name_label.set_label(os_name)
        self.version_codename_label.set_label(os_version)
        self.os_family_label.set_label(os_family)
        self.based_on_label.set_label(os_based_on)
        self.kernel_release_label.set_label(kernel_release)
        self.kernel_version_label.set_label(kernel_version)
        self.desktop_environment_label.set_label(f'{current_desktop_environment} ({current_desktop_environment_version})')
        self.windowing_system_label.set_label(windowing_system)
        self.window_manager_label.set_label(window_manager)
        self.display_manager_label.set_label(current_display_manager)
        self.vendor_label.set_label(computer_vendor)
        self.model_label.set_label(computer_model)
        self.computer_type_label.set_label(computer_chassis_type)
        self.computer_name_label.set_label(host_name)
        self.architecture_label.set_label(cpu_architecture)
        self.number_of_monitors_label.set_label(f'{number_of_monitors}')
        #self.system_label.set_label(f'{number_of_installed_apt_or_rpm_or_pacman_packages}')
        self.flatpak_label.set_label(f'{number_of_installed_flatpak_packages}')
        self.gtk_version_label.set_label(current_gtk_version)
        self.python_version_label.set_label(f'{current_python_version}')

        self.initial_already_run = 1


    def set_number_of_installed_apt_or_rpm_or_pacman_packages_label_func(self, number_of_installed_apt_or_rpm_or_pacman_packages):
        """
        Stop and hide spinner properties and show "number_of_installed_apt_or_rpm_or_pacman_packages" information on the label.
        """

        self.spinner_system.stop()
        self.spinner_system.hide()
        self.system_label.set_label(f'{number_of_installed_apt_or_rpm_or_pacman_packages}')


    def os_name_version_codename_based_on_func(self):
        """
        Get OS name, version, version code name and OS based on information.
        """

        # Read "/etc/os-release" file for getting OS name, version and based on information.
        if Config.environment_type == "flatpak":
            with open("/var/run/host/etc/os-release") as reader:
                os_release_output_lines = reader.read().strip().split("\n")
        else:
            with open("/etc/os-release") as reader:
                os_release_output_lines = reader.read().strip().split("\n")

        os_name = "-"
        os_based_on = "-"
        os_version = "-"
        build_id = "-"

        # Get OS name, version and based on information.
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
            if line.startswith("BUILD_ID="):
                build_id = line.split("BUILD_ID=")[1].strip(' "').title()
                continue

        # Some Arch Linux based distributions may have "BUILD_ID" instead of "VERSION". For example: Endeavour OS.
        if os_version == "-":
            os_version = build_id

        # Append Debian version to the based on information if OS is based on Debian.
        if os_based_on == "Debian":
            debian_version = "-"
            if Config.environment_type == "flatpak":
                with open("/var/run/host/etc/debian_version") as reader:
                    debian_version = reader.read().strip()
            else:
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


    def os_family_func(self):
        """
        Get OS family.
        """

        os_family = platform.system()
        if os_family == "":
            os_family = "-"

        return os_family


    def kernel_release_kernel_version_func(self):
        """
        Get kernel release (base version of kernel) and kernel version (package version of kernel).
        """

        # Get kernel release (base version of kernel)
        kernel_release = platform.release()
        if kernel_release == "":
            kernel_release = "-"

        # Get kernel version (package version of kernel)
        kernel_version = platform.version()
        if kernel_version == "":
            kernel_version = "-"

        return kernel_release, kernel_version


    def cpu_architecture_func(self):
        """
        Get CPU architecture
        """

        cpu_architecture = platform.processor()
        if cpu_architecture == "":
            cpu_architecture = platform.machine()
            if cpu_architecture == "":
                cpu_architecture = "-"

        return cpu_architecture


    def computer_vendor_model_chassis_type_func(self):
        """
        Get computer vendor, model and chassis type
        """

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


    def host_name_func(self):
        """
        Get host name.
        """

        with open("/proc/sys/kernel/hostname") as reader:
            host_name = reader.read().strip()

        return host_name


    def number_of_monitors_func(self):
        """
        Get number of monitors.
        """

        try:
            monitor_list = Gdk.Display().get_default().get_monitors()
            number_of_monitors = len(monitor_list)
        except Exception:
            number_of_monitors = "-"

        return number_of_monitors


    def installed_flatpak_packages_func(self):
        """
        Get number of installed Flatpak packages (and runtimes).
        """

        number_of_installed_flatpak_packages = "-"

        try:
            if Config.environment_type == "flatpak":
                flatpak_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "flatpak", "list"], shell=False)).decode().strip().split("\n")
            else:
                flatpak_packages_available = (subprocess.check_output(["flatpak", "list"], shell=False)).decode().strip().split("\n")
            # Differentiate empty line count
            number_of_installed_flatpak_packages = len(flatpak_packages_available) - flatpak_packages_available.count("")
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            number_of_installed_flatpak_packages = "-"

        return number_of_installed_flatpak_packages


    def current_python_version_gtk_version_func(self):
        """
        Get current Python version and GTK version.
        """

        # Get current Python version (Python which is running this code)
        current_python_version = platform.python_version()

        # Get Gtk version which is used for this application.
        current_gtk_version = f'{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}'

        return current_python_version, current_gtk_version


    def installed_apt_rpm_pacman_packages_func(self):
        """
        Get number of installed APT, RPM or pacman packages.
        """

        # Initial value of the variables.
        apt_packages_available = "-"
        rpm_packages_available = "-"
        pacman_packages_available = "-"
        number_of_installed_apt_or_rpm_or_pacman_packages = "-"

        # Get number of APT (deb) packages if available.
        try:
            # Check if "python3" is installed in order to determine package type of the system.
            if Config.environment_type == "flatpak":
                apt_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "dpkg", "-s", "python3"], shell=False)).decode().strip()
            else:
                apt_packages_available = (subprocess.check_output(["dpkg", "-s", "python3"], shell=False)).decode().strip()
            if "Package: python3" in apt_packages_available:
                if Config.environment_type == "flatpak":
                    number_of_installed_apt_packages = (subprocess.check_output(["flatpak-spawn", "--host", "dpkg", "--list"], shell=False)).decode().strip().count("\nii  ")
                else:
                    number_of_installed_apt_packages = (subprocess.check_output(["dpkg", "--list"], shell=False)).decode().strip().count("\nii  ")
                number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_apt_packages} (APT)'
        # It gives "FileNotFoundError" if first element of the command (program name) can not be found on the system. It gives "subprocess.CalledProcessError" if there are any errors relevant with the parameters (commands later than the first one).
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            apt_packages_available = "-"

        # Get number of RPM packages if available.
        if apt_packages_available == "-":
            try:
                if Config.environment_type == "flatpak":
                    rpm_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "rpm", "-q", "python3"], shell=False)).decode().strip()
                else:
                    rpm_packages_available = (subprocess.check_output(["rpm", "-q", "python3"], shell=False)).decode().strip()
                if rpm_packages_available.startswith("python3-3."):
                    if Config.environment_type == "flatpak":
                        number_of_installed_rpm_packages = (subprocess.check_output(["flatpak-spawn", "--host", "rpm", "-qa"], shell=False)).decode().strip().split("\n")
                    else:
                        number_of_installed_rpm_packages = (subprocess.check_output(["rpm", "-qa"], shell=False)).decode().strip().split("\n")
                    # Differentiate empty line count
                    number_of_installed_rpm_packages = len(number_of_installed_rpm_packages) - number_of_installed_rpm_packages.count("")
                    number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_rpm_packages} (RPM)'
            except (FileNotFoundError, subprocess.CalledProcessError) as me:
                rpm_packages_available = "-"

        # Get number of pacman (Arch Linux) packages if available.
        if apt_packages_available == "-" and rpm_packages_available == "-":
            try:
                if Config.environment_type == "flatpak":
                    pacman_packages_available = (subprocess.check_output(["flatpak-spawn", "--host", "pacman", "-Q", "python3"], shell=False)).decode().strip()
                else:
                    pacman_packages_available = (subprocess.check_output(["pacman", "-Q", "python3"], shell=False)).decode().strip()
                if pacman_packages_available.startswith("python 3."):
                    if Config.environment_type == "flatpak":
                        number_of_installed_pacman_packages = (subprocess.check_output(["flatpak-spawn", "--host", "pacman", "-Qq"], shell=False)).decode().strip().split("\n")
                    else:
                        number_of_installed_pacman_packages = (subprocess.check_output(["pacman", "-Qq"], shell=False)).decode().strip().split("\n")
                    # Differentiate empty line count
                    number_of_installed_pacman_packages = len(number_of_installed_pacman_packages) - number_of_installed_pacman_packages.count("")
                    number_of_installed_apt_or_rpm_or_pacman_packages = f'{number_of_installed_pacman_packages} (pacman)'
            except (FileNotFoundError, subprocess.CalledProcessError) as me:
                pacman_packages_available = "-"

        # Show the information on the label by using "GLib.idle_add" in order to avoid problems (bugs, data corruption, etc.) because of threading (GTK is not thread-safe).
        GLib.idle_add(self.set_number_of_installed_apt_or_rpm_or_pacman_packages_label_func, number_of_installed_apt_or_rpm_or_pacman_packages)

        return number_of_installed_apt_or_rpm_or_pacman_packages


    def desktop_environment_and_version_windowing_system_window_manager_display_manager_func(self):
        """
        Get current desktop environment, windowing_system, window_manager, current_display_manager.
        """

        # Get current username
        # Get user name that gets root privileges.
        # Othervise, username is get as "root" when root access is get.
        current_user_name = os.environ.get('SUDO_USER')
        # Get username in the following way if current application has not
        # been run by root privileges.
        if current_user_name is None:
            current_user_name = os.environ.get('USER')

        # Try to get windowing system. This value may be get as "None" if the
        # application is run with root privileges. This value will be get by
        # reading information of processes if it is get as "None".
        windowing_system = os.environ.get('XDG_SESSION_TYPE')
        # "windowing_system" is get as "None" if application is run with root privileges.
        if windowing_system != None:
            windowing_system = windowing_system.capitalize()

        # Try to get current desktop environment. This value may be get as
        # "None" if the application is run with root privileges. This value
        # will be get by reading information of processes if it is get as "None".
        # This command may give Gnome DE based DEs as "[DE_name]:GNOME".
        # For example, "Budgie:GNOME" value is get on Budgie DE.
        current_desktop_environment = os.environ.get('XDG_CURRENT_DESKTOP')
        if current_desktop_environment == None:
            # Define initial value of "desktop environment".
            current_desktop_environment = "-"

        # Define initial value of "windowing_system".
        if windowing_system == None:
            windowing_system = "-"

        # Define initial value of "window_manager".
        window_manager = "-"

        # Define initial value of "current_display_manager".
        current_display_manager = "-"

        # First values are process names of the DEs, second values are names of
        # the DEs. Cinnamon dektop environment accepts both "X-Cinnamon" and
        # "CINNAMON" names in the .desktop files.
        supported_desktop_environments_dict = {"xfce4-session":"XFCE", "gnome-session-b":"GNOME", "cinnamon-session":"X-Cinnamon",
                                               "mate-session":"MATE", "plasmashell":"KDE", "lxqt-session":"LXQt", "lxsession":"LXDE",
                                               "budgie-panel":"Budgie", "dde-desktop":"Deepin"}
        supported_window_managers_list = ["xfwm4", "mutter", "kwin", "kwin_x11", "cinnamon", "budgie-wm", "openbox", "metacity", 
                                          "marco", "compiz", "englightenment", "fvwm2", "icewm", "sawfish", "awesome", "muffin"]
        # First values are process names of the display managers, second values
        # are names of the display managers.
        supported_display_managers_dict = {"lightdm":"lightdm", "gdm":"gdm", "gdm3":"gdm3", "sddm":"sddm", "xdm":"xdm", "lxdm-binary":"lxdm"}                                                       

        # Try to detect windowing system, window manager, current desktop 
        # environment and current display manager by reading process names and
        # other details.
        command_list = ["ps", "--no-headers", "-eo", "comm,user"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        ps_output_lines = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split("\n")

        process_name_list = []
        username_list = []

        for line in ps_output_lines:
            line_split = line.split()
            process_name_list.append(line_split[0])
            username_list.append(line_split[1])

        # Get current desktop environment information
        # "current_desktop_environment == "GNOME"" check is performed in order to
        # detect if current DE is "Budgie DE". Because "budgie-panel" process is child
        # process of "gnome-session-b" process.
        for process_name in process_name_list:
            if current_desktop_environment == "-" or current_desktop_environment == "GNOME":
                if process_name in supported_desktop_environments_dict:
                    process_username = username_list[process_name_list.index(process_name)]
                    if process_username == current_user_name:
                        current_desktop_environment = supported_desktop_environments_dict[process_name]
                        break

        # Get current desktop environment version
        current_desktop_environment_version = self.desktop_environment_version_func(current_desktop_environment)

        # Get windowing system information.
        # Windowing system may be get as "tty" (which is for non-graphical system) when
        # "os.environ.get('XDG_SESSION_TYPE')" is used on Arch Linux if environment
        # variables are not set after installing a windowing system.
        for process_name in process_name_list:
            if windowing_system in ["-", "Tty"]:
                process_name = process_name.lower()
                if process_name == "xorg":
                    windowing_system = "X11"
                    break
                if process_name == "xwayland":
                    windowing_system = "Wayland"
                    break

        # Get window manager information
        for process_name in process_name_list:
            if window_manager == "-":
                if process_name.lower() in supported_window_managers_list:
                    process_username = username_list[process_name_list.index(process_name)]
                    if process_username == current_user_name:
                        window_manager = process_name.lower()
                        break

        # Get window manager for GNOME DE (GNOME DE uses mutter window manager and
        # it not detected because it has no separate package or process.).
        if window_manager == "-":
            if current_desktop_environment.upper() == "GNOME":
                if current_desktop_environment_version.split(".")[0] in ["3", "40", "41", "42", "43"]:
                    window_manager = "mutter"

        # Get current display manager information
        for process_name in process_name_list:
            if current_display_manager == "-":
                if process_name in supported_display_managers_dict:
                    process_username = username_list[process_name_list.index(process_name)]
                    # Display manager processes are owned by root user.
                    if process_username == "root":
                        current_display_manager = supported_display_managers_dict[process_name]
                        break

        return current_desktop_environment, current_desktop_environment_version, windowing_system, window_manager, current_display_manager


    def desktop_environment_version_func(self, current_desktop_environment):
        """
        Get current desktop environment version.
        """

        desktop_environment_version_command_dict = {
                                                    "XFCE":["xfce4-panel", "--version"],
                                                    "GNOME":["gnome-shell", "--version"],
                                                    "zorin:GNOME":["gnome-shell", "--version"],
                                                    "ubuntu:GNOME":["gnome-shell", "--version"],
                                                    "X-Cinnamon":["cinnamon", "--version"],
                                                    "CINNAMON":["cinnamon", "--version"],
                                                    "MATE":["mate-about", "--version"],
                                                    "KDE":["plasmashell", "--version"],
                                                    "LXQt":["lxqt-about", "--version"],
                                                    "Budgie":["budgie-desktop", "--version"],
                                                    "Budgie:GNOME":["budgie-desktop", "--version"]
                                                    }

        current_desktop_environment_version = "-"

        if current_desktop_environment in desktop_environment_version_command_dict:
            command_list = desktop_environment_version_command_dict[current_desktop_environment]
            if Config.environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list

            try:
                desktop_environment_version_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()
            except Exception:
                desktop_environment_version_output = "-"
        else:
            desktop_environment_version_output = "-"

        if current_desktop_environment == "XFCE":
            for line in desktop_environment_version_output.split("\n"):
                if "xfce4-panel" in line:
                    current_desktop_environment_version = line.split(" ")[1]

        if current_desktop_environment in ["GNOME", "zorin:GNOME", "ubuntu:GNOME"]:
            for line in desktop_environment_version_output.split("\n"):
                if "GNOME Shell" in line:
                    current_desktop_environment_version = line.split(" ")[-1]

        if current_desktop_environment in ["X-Cinnamon", "CINNAMON"]:
            current_desktop_environment_version = desktop_environment_version_output.split(" ")[-1]

        if current_desktop_environment == "MATE":
            current_desktop_environment_version = desktop_environment_version_output.split(" ")[-1]

        if current_desktop_environment == "KDE":
            current_desktop_environment_version = desktop_environment_version_output

        if current_desktop_environment == "LXQt":
            for line in desktop_environment_version_output:
                if "liblxqt" in line:
                    current_desktop_environment_version = line.split()[1].strip()

        if current_desktop_environment in ["Budgie", "Budgie:GNOME"]:
            current_desktop_environment_version = desktop_environment_version_output.split("\n")[0].strip().split(" ")[-1]

        return current_desktop_environment_version


System = System()


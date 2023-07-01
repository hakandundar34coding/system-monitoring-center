import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

import threading

from .Config import Config
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class System:

    def __init__(self):

        self.name = "System"

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
        style_provider_grid = Gtk.CssProvider()
        try:
            css = b"grid {border-style: solid; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
            style_provider_grid.load_from_data(css)
        except Exception:
            css = "grid {border-style: solid; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
            style_provider_grid.load_from_data(css, len(css))

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
        label = Common.static_information_label(_tr("Version") + " - " + _tr("Code Name") + ":")
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
        system_packages_grid = Gtk.Grid()
        system_packages_grid.set_column_spacing(2)
        grid.attach(system_packages_grid, 3, 9, 1, 1)
        # Label (System)
        self.system_packages_label = Common.dynamic_information_label()
        system_packages_grid.attach(self.system_packages_label, 0, 0, 1, 1)
        # Spinner (System)
        self.system_packages_spinner = Gtk.Spinner()
        self.system_packages_spinner.start()
        system_packages_grid.attach(self.system_packages_spinner, 1, 0, 1, 1)

        # Label (Flatpak)
        label = Common.static_information_label(_tr("Flatpak") + ":")
        label.set_tooltip_text(_tr("Number of installed Flatpak applications and runtimes"))
        grid.attach(label, 2, 10, 1, 1)
        # Grid (Flatpak)
        flatpak_packages_grid = Gtk.Grid()
        flatpak_packages_grid.set_column_spacing(2)
        grid.attach(flatpak_packages_grid, 3, 10, 1, 1)
        # Label (Flatpak)
        self.flatpak_packages_label = Common.dynamic_information_label()
        flatpak_packages_grid.attach(self.flatpak_packages_label, 0, 0, 1, 1)
        # Spinner (Flatpak)
        self.flatpak_packages_spinner = Gtk.Spinner()
        self.flatpak_packages_spinner.start()
        flatpak_packages_grid.attach(self.flatpak_packages_spinner, 1, 0, 1, 1)

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

        # Show and start spinner animation before running the function for getting information.
        self.system_packages_spinner.set_visible(True)
        self.system_packages_spinner.start()

        self.flatpak_packages_spinner.set_visible(True)
        self.flatpak_packages_spinner.start()

        self.loop_func()


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        # Get information.
        os_name, os_version, os_based_on = Libsysmon.get_os_name_version_codename_based_on()
        os_family = Libsysmon.get_os_family()
        kernel_release = Libsysmon.get_kernel_release()
        kernel_version = Libsysmon.get_kernel_version()
        cpu_architecture = Libsysmon.get_cpu_architecture()
        computer_vendor, computer_model, computer_chassis_type = Libsysmon.get_computer_vendor_model_chassis_type()
        host_name = Libsysmon.get_host_name()
        number_of_monitors = Libsysmon.get_number_of_monitors()
        current_python_version = Libsysmon.get_current_python_version()
        current_gtk_version = Libsysmon.get_current_gtk_version()
        current_desktop_environment, current_desktop_environment_version, windowing_system, window_manager, current_display_manager = Libsysmon.get_desktop_environment_and_version_windowing_system_window_manager_display_manager()
        # Run this function in a separate thread because it may take a long time (2-3 seconds) to get the information on some systems (such as rpm based systems) and it blocks the GUI during this process if a separate thread is not used.
        threading.Thread(target=self.apt_or_rpm_or_pacman_packages_count_func, daemon=True).start()
        threading.Thread(target=self.flatpak_packages_count_func, daemon=True).start()


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
        #self.system_packages_label.set_label(f'{apt_or_rpm_or_pacman_packages_count}')
        #self.flatpak_packages_label.set_label(f'{flatpak_packages_count}')
        self.gtk_version_label.set_label(current_gtk_version)
        self.python_version_label.set_label(f'{current_python_version}')

        self.initial_already_run = 1


    def apt_or_rpm_or_pacman_packages_count_func(self):
        apt_or_rpm_or_pacman_packages_count = Libsysmon.get_installed_apt_rpm_pacman_packages()
        # Stop and hide spinner and set label text.
        GLib.idle_add(Common.set_label_spinner, self.system_packages_label, self.system_packages_spinner, apt_or_rpm_or_pacman_packages_count)


    def flatpak_packages_count_func(self):
        flatpak_packages_count = Libsysmon.get_installed_flatpak_packages()
        # Stop and hide spinner and set label text.
        GLib.idle_add(Common.set_label_spinner, self.flatpak_packages_label, self.flatpak_packages_spinner, flatpak_packages_count)


System = System()


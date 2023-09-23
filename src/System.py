import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

import threading

from .Config import Config
from .Performance import Performance
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

        # ScrolledWindow
        scrolledwindow = Gtk.ScrolledWindow()
        performance_info_grid.attach(scrolledwindow, 0, 0, 1, 1)
        # Viewport
        viewport = Gtk.Viewport()
        viewport.set_hexpand(True)
        viewport.set_vexpand(True)
        scrolledwindow.set_child(viewport)

        # Grid (information labels inner grid)
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        #grid.set_row_homogeneous(True)
        grid.set_column_spacing(12)
        grid.set_row_spacing(2)
        grid.set_margin_top(6)
        grid.set_margin_bottom(6)
        grid.set_margin_start(6)
        grid.set_margin_end(6)
        viewport.set_child(grid)

        # Grid (Hardware)
        self.grid_hardware = Gtk.Grid()
        self.grid_hardware.set_column_homogeneous(True)
        self.grid_hardware.set_row_homogeneous(True)
        self.grid_hardware.set_column_spacing(12)
        self.grid_hardware.set_row_spacing(2)
        grid.attach(self.grid_hardware, 0, 0, 2, 1)

        # Grid Upper (Computer - Packages)
        grid_computer_packages = Gtk.Grid()
        grid_computer_packages.set_column_homogeneous(True)
        #grid_computer_packages.set_row_homogeneous(True)
        grid_computer_packages.set_column_spacing(12)
        grid_computer_packages.set_row_spacing(2)
        grid.attach(grid_computer_packages, 0, 1, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(4)
        separator.set_margin_bottom(4)
        separator.set_valign(Gtk.Align.CENTER)
        grid_computer_packages.attach(separator, 0, 0, 1, 1)

        # Grid (Computer)
        grid_computer = Gtk.Grid()
        grid_computer.set_column_homogeneous(True)
        grid_computer.set_row_homogeneous(True)
        grid_computer.set_column_spacing(12)
        grid_computer.set_row_spacing(2)
        grid_computer_packages.attach(grid_computer, 0, 1, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(4)
        separator.set_margin_bottom(4)
        separator.set_valign(Gtk.Align.CENTER)
        grid_computer_packages.attach(separator, 0, 2, 1, 1)

        # Grid (Packages)
        grid_packages = Gtk.Grid()
        grid_packages.set_column_homogeneous(True)
        grid_packages.set_row_homogeneous(True)
        grid_packages.set_column_spacing(12)
        grid_packages.set_row_spacing(2)
        grid_computer_packages.attach(grid_packages, 0, 3, 1, 1)

        # Grid Upper ((Operating System (OS) - Graphical User Interface (GUI))
        grid_os_gui = Gtk.Grid()
        grid_os_gui.set_column_homogeneous(True)
        #grid_os_gui.set_row_homogeneous(True)
        grid_os_gui.set_column_spacing(12)
        grid_os_gui.set_row_spacing(2)
        grid.attach(grid_os_gui, 1, 1, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(4)
        separator.set_margin_bottom(4)
        separator.set_valign(Gtk.Align.CENTER)
        grid_os_gui.attach(separator, 0, 0, 1, 1)

        # Grid (Operating System (OS))
        grid_operating_system = Gtk.Grid()
        grid_operating_system.set_column_homogeneous(True)
        grid_operating_system.set_row_homogeneous(True)
        grid_operating_system.set_column_spacing(12)
        grid_operating_system.set_row_spacing(2)
        grid_os_gui.attach(grid_operating_system, 0, 1, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(4)
        separator.set_margin_bottom(4)
        separator.set_valign(Gtk.Align.CENTER)
        grid_os_gui.attach(separator, 0, 2, 1, 1)

        # Grid (Graphical User Interface (GUI))
        grid_graphical_user_interface = Gtk.Grid()
        grid_graphical_user_interface.set_column_homogeneous(True)
        grid_graphical_user_interface.set_row_homogeneous(True)
        grid_graphical_user_interface.set_column_spacing(12)
        grid_graphical_user_interface.set_row_spacing(2)
        grid_os_gui.attach(grid_graphical_user_interface, 0, 3, 1, 1)


        # Performance information labels
        """# Label - Title (Hardware)
        label = Common.title_label(_tr("Hardware"))
        self.grid_hardware.attach(label, 0, 0, 2, 1)"""

        # Label (CPU)
        label = Common.static_information_label(_tr("CPU") + ":")
        self.grid_hardware.attach(label, 0, 0, 1, 1)
        # Label (CPU)
        self.cpu_vendor_model_label = Common.dynamic_information_label()
        self.grid_hardware.attach(self.cpu_vendor_model_label, 1, 0, 3, 1)

        # Label (Memory)
        label = Common.static_information_label(_tr("Memory") + ":")
        self.grid_hardware.attach(label, 0, 1, 1, 1)
        # Label (Memory)
        self.memory_capacity_label = Common.dynamic_information_label()
        self.grid_hardware.attach(self.memory_capacity_label, 1, 1, 3, 1)

        # Label (GPU)
        label = Common.static_information_label(_tr("GPU") + ":")
        self.grid_hardware.attach(label, 0, 2, 1, 1)
        # Label (GPU)
        self.gpu_vendor_model_label = Common.dynamic_information_label()
        self.grid_hardware.attach(self.gpu_vendor_model_label, 1, 2, 3, 1)

        # Label (GPU (2))
        self.gpu2_label = Common.static_information_label(_tr("GPU") + " (2)" + ":")
        # Label (GPU (2))
        self.gpu_vendor_model_label2 = Common.dynamic_information_label()

        # Label (Monitors)
        label = Common.static_information_label(_tr("Resolution") + ":")
        self.grid_hardware.attach(label, 0, 3, 1, 1)
        # Label (Monitors)
        self.monitors_label = Common.dynamic_information_label()
        self.grid_hardware.attach(self.monitors_label, 1, 3, 3, 1)

        # Label - Title (Computer)
        label = Common.title_label(_tr("Computer"))
        grid_computer.attach(label, 0, 0, 2, 1)

        # Label (Vendor)
        label = Common.static_information_label(_tr("Vendor") + ":")
        grid_computer.attach(label, 0, 1, 1, 1)
        # Label (Vendor)
        self.vendor_label = Common.dynamic_information_label()
        grid_computer.attach(self.vendor_label, 1, 1, 1, 1)

        # Label (Model)
        label = Common.static_information_label(_tr("Model") + ":")
        grid_computer.attach(label, 0, 2, 1, 1)
        # Label (Model)
        self.model_label = Common.dynamic_information_label()
        grid_computer.attach(self.model_label, 1, 2, 1, 1)

        # Label (Computer Type)
        label = Common.static_information_label(_tr("Computer Type") + ":")
        grid_computer.attach(label, 0, 3, 1, 1)
        # Label (Computer Type)
        self.computer_type_label = Common.dynamic_information_label()
        grid_computer.attach(self.computer_type_label, 1, 3, 1, 1)

        # Label (Name)
        label = Common.static_information_label(_tr("Name") + ":")
        grid_computer.attach(label, 0, 4, 1, 1)
        # Label (Name)
        self.computer_name_label = Common.dynamic_information_label()
        grid_computer.attach(self.computer_name_label, 1, 4, 1, 1)

        # Label (Architecture)
        label = Common.static_information_label(_tr("Architecture") + ":")
        grid_computer.attach(label, 0, 5, 1, 1)
        # Label (Architecture)
        self.architecture_label = Common.dynamic_information_label()
        grid_computer.attach(self.architecture_label, 1, 5, 1, 1)

        # Label (Number Of Monitors)
        label = Common.static_information_label(_tr("Number Of Monitors") + ":")
        grid_computer.attach(label, 0, 6, 1, 1)
        # Label (Number Of Monitors)
        self.number_of_monitors_label = Common.dynamic_information_label()
        grid_computer.attach(self.number_of_monitors_label, 1, 6, 1, 1)

        # Label - Title (Operating System (OS))
        label = Common.title_label(_tr("Operating System (OS)"))
        grid_operating_system.attach(label, 0, 0, 2, 1)

        # Label (Name)
        label = Common.static_information_label(_tr("Name") + ":")
        grid_operating_system.attach(label, 0, 1, 1, 1)
        # Label (Name)
        self.os_name_label = Common.dynamic_information_label()
        grid_operating_system.attach(self.os_name_label, 1, 1, 1, 1)

        # Label (Version - Code Name)
        label = Common.static_information_label(_tr("Version") + " - " + _tr("Code Name") + ":")
        grid_operating_system.attach(label, 0, 2, 1, 1)
        # Label (Version - Code Name)
        self.version_codename_label = Common.dynamic_information_label()
        grid_operating_system.attach(self.version_codename_label, 1, 2, 1, 1)

        # Label (OS Family)
        label = Common.static_information_label(_tr("OS Family") + ":")
        grid_operating_system.attach(label, 0, 3, 1, 1)
        # Label (OS Family)
        self.os_family_label = Common.dynamic_information_label()
        grid_operating_system.attach(self.os_family_label, 1, 3, 1, 1)

        # Label (Based On)
        label = Common.static_information_label(_tr("Based On") + ":")
        grid_operating_system.attach(label, 0, 4, 1, 1)
        # Label (Based On)
        self.based_on_label = Common.dynamic_information_label()
        grid_operating_system.attach(self.based_on_label, 1, 4, 1, 1)

        # Label (Kernel Release)
        label = Common.static_information_label(_tr("Kernel Release") + ":")
        grid_operating_system.attach(label, 0, 5, 1, 1)
        # Label (Kernel Release)
        self.kernel_release_label = Common.dynamic_information_label()
        grid_operating_system.attach(self.kernel_release_label, 1, 5, 1, 1)

        # Label (Kernel Version)
        label = Common.static_information_label(_tr("Kernel Version") + ":")
        grid_operating_system.attach(label, 0, 6, 1, 1)
        # Label (Kernel Version)
        self.kernel_version_label = Common.dynamic_information_label()
        grid_operating_system.attach(self.kernel_version_label, 1, 6, 1, 1)

        # Label - Title (Graphical User Interface (GUI))
        label = Common.title_label(_tr("Graphical User Interface (GUI)"))
        grid_graphical_user_interface.attach(label, 0, 0, 2, 1)

        # Label (Desktop Environment)
        label = Common.static_information_label(_tr("Desktop Environment") + ":")
        grid_graphical_user_interface.attach(label, 0, 1, 1, 1)
        # Label (Desktop Environment)
        self.desktop_environment_label = Common.dynamic_information_label()
        grid_graphical_user_interface.attach(self.desktop_environment_label, 1, 1, 1, 1)

        # Label (Windowing System)
        label = Common.static_information_label(_tr("Windowing System") + ":")
        grid_graphical_user_interface.attach(label, 0, 2, 1, 1)
        # Label (Windowing System)
        self.windowing_system_label = Common.dynamic_information_label()
        grid_graphical_user_interface.attach(self.windowing_system_label, 1, 2, 1, 1)

        # Label (Window Manager)
        label = Common.static_information_label(_tr("Window Manager") + ":")
        grid_graphical_user_interface.attach(label, 0, 3, 1, 1)
        # Label (Window Manager)
        self.window_manager_label = Common.dynamic_information_label()
        grid_graphical_user_interface.attach(self.window_manager_label, 1, 3, 1, 1)

        # Label (Display Manager)
        label = Common.static_information_label(_tr("Display Manager") + ":")
        grid_graphical_user_interface.attach(label, 0, 4, 1, 1)
        # Label (Display Manager)
        self.display_manager_label = Common.dynamic_information_label()
        grid_graphical_user_interface.attach(self.display_manager_label, 1, 4, 1, 1)

        # Label - Title (Packages)
        label = Common.title_label(_tr("Packages"))
        grid_packages.attach(label, 0, 0, 2, 1)

        # Label (System)
        label = Common.static_information_label(_tr("System") + ":")
        grid_packages.attach(label, 0, 1, 1, 1)
        # Grid (System)
        system_packages_grid = Gtk.Grid()
        system_packages_grid.set_column_spacing(2)
        grid_packages.attach(system_packages_grid, 1, 1, 1, 1)
        # Label (System)
        self.system_packages_label = Common.dynamic_information_label()
        system_packages_grid.attach(self.system_packages_label, 0, 0, 1, 1)
        # Spinner (System)
        self.system_packages_spinner_label = Common.static_information_label(_tr("Processing") + "...")
        self.system_packages_spinner_label.set_margin_start(10)
        #self.system_packages_spinner.start()
        system_packages_grid.attach(self.system_packages_spinner_label, 1, 0, 1, 1)

        # Label (Flatpak)
        label = Common.static_information_label(_tr("Flatpak") + ":")
        label.set_tooltip_text(_tr("Number of installed Flatpak applications and runtimes"))
        grid_packages.attach(label, 0, 2, 1, 1)
        # Grid (Flatpak)
        flatpak_packages_grid = Gtk.Grid()
        flatpak_packages_grid.set_column_spacing(2)
        grid_packages.attach(flatpak_packages_grid, 1, 2, 1, 1)
        # Label (Flatpak)
        self.flatpak_packages_label = Common.dynamic_information_label()
        flatpak_packages_grid.attach(self.flatpak_packages_label, 0, 0, 1, 1)
        # Spinner (Flatpak)
        self.flatpak_packages_spinner_label = Gtk.Spinner()
        # Rest of the code is not run and infomation is not shown if Spinner is started on some systems with XFCE DE.
        #self.flatpak_packages_spinner_label.start()
        flatpak_packages_grid.attach(self.flatpak_packages_spinner_label, 1, 0, 1, 1)

        # Label (GTK Version)
        label = Common.static_information_label(_tr("GTK Version") + ":")
        label.set_tooltip_text(_tr("Version for the currently running software"))
        grid_packages.attach(label, 0, 3, 1, 1)
        # Label (GTK Version)
        self.gtk_version_label = Common.dynamic_information_label()
        grid_packages.attach(self.gtk_version_label, 1, 3, 1, 1)

        # Label (Python Version)
        label = Common.static_information_label(_tr("Python Version") + ":")
        label.set_tooltip_text(_tr("Version for the currently running software"))
        grid_packages.attach(label, 0, 4, 1, 1)
        # Label (Python Version)
        self.python_version_label = Common.dynamic_information_label()
        grid_packages.attach(self.python_version_label, 1, 4, 1, 1)


    def on_refresh_button_clicked(self, widget):
        """
        Refresh data on the tab.
        """

        # Show and start spinner animation before running the function for getting information.
        self.system_packages_spinner_label.set_visible(True)
        #self.system_packages_spinner_label.start()

        self.flatpak_packages_spinner_label.set_visible(True)
        #self.flatpak_packages_spinner_label.start()

        self.loop_already_run = 0

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

        # Prevent running rest of the code if System tab is opened again.
        try:
            if self.loop_already_run == 1:
                return
        except AttributeError:
            pass
        self.loop_already_run = 1

        # Get information.
        os_name, os_version, os_based_on = Libsysmon.get_os_name_version_codename_based_on()
        os_family = Libsysmon.get_os_family()
        kernel_release = Libsysmon.get_kernel_release()
        kernel_version = Libsysmon.get_kernel_version()
        # Run this function in a separate thread for a more responsive GUI.
        threading.Thread(target=self.get_computer_hardware_information, daemon=True).start()
        cpu_architecture = Libsysmon.get_cpu_architecture()
        computer_vendor, computer_model, computer_chassis_type = Libsysmon.get_computer_vendor_model_chassis_type()
        host_name = Libsysmon.get_host_name()
        number_of_monitors = Libsysmon.get_number_of_monitors()
        current_python_version = Libsysmon.get_current_python_version()
        current_gtk_version = Libsysmon.get_current_gtk_version()
        current_desktop_environment, current_desktop_environment_version, windowing_system, window_manager, current_display_manager = Libsysmon.get_desktop_environment_and_version_windowing_system_window_manager_display_manager()
        # Run this function in a separate thread because it may take a long time (2-3 seconds) to get the information on some systems (such as rpm based systems) and it blocks the GUI during this process if a separate thread is not used.
        threading.Thread(target=self.apt_or_rpm_or_pacman_or_apk_packages_count_func, daemon=True).start()
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
        """self.cpu_vendor_model_label.set_label(cpu_model_name)
        self.memory_capacity_label.set_label(Libsysmon.data_unit_converter("data", "none", ram_total, performance_memory_data_unit, performance_memory_data_precision))
        self.gpu_vendor_model_label.set_label(',\n'.join(gpu_device_model_name.split(" - ", 1)))
        self.monitors_label.set_label(current_resolution_refresh_rate)"""
        self.vendor_label.set_label(computer_vendor)
        self.model_label.set_label(computer_model)
        self.computer_type_label.set_label(computer_chassis_type)
        self.computer_name_label.set_label(host_name)
        self.architecture_label.set_label(cpu_architecture)
        self.number_of_monitors_label.set_label(f'{number_of_monitors}')
        #self.system_packages_label.set_label(f'{apt_or_rpm_or_pacman_or_apk_packages_count}')
        #self.flatpak_packages_label.set_label(f'{flatpak_packages_count}')
        self.gtk_version_label.set_label(current_gtk_version)
        self.python_version_label.set_label(f'{current_python_version}')

        self.initial_already_run = 1


    def set_multiple_label_text(self, label_list, label_data_list):
        """
        Set multiple label text.
        """

        for i, label in enumerate(label_list):
            label.set_label(label_data_list[i])


    def get_computer_hardware_information(self):
        """
        Get some of computer hardware information.
        """

        # Get CPU vendor-model
        selected_cpu_core = "cpu0"
        number_of_logical_cores = Libsysmon.get_number_of_logical_cores()
        number_of_physical_cores, number_of_cpu_sockets, cpu_model_name = Libsysmon.get_number_of_physical_cores_sockets_cpu_name(selected_cpu_core, number_of_logical_cores)

        # Get RAM and swap memory capacity values
        performance_memory_data_precision = Config.performance_memory_data_precision
        performance_memory_data_unit = Config.performance_memory_data_unit
        memory_info = Libsysmon.get_memory_info()
        ram_total = memory_info["ram_total"]
        swap_total = memory_info["swap_total"]
        ram_capacity_text = Libsysmon.data_unit_converter("data", "none", ram_total, performance_memory_data_unit, performance_memory_data_precision)
        swap_capacity_text = Libsysmon.data_unit_converter("data", "none", swap_total, 0, 1)
        memory_capacity_text = ram_capacity_text + " (" + _tr("RAM") + ")  -  " + swap_capacity_text + " (" + _tr("Swap Memory") + ")"

        # Get GPU (boot VGA) vendor-model
        try:
            gpu_list, gpu_device_path_list, gpu_device_sub_path_list, default_gpu = Libsysmon.get_gpu_list_and_boot_vga()
            config_selected_gpu = default_gpu
            selected_gpu_number, selected_gpu = Libsysmon.gpu_set_selected_gpu(config_selected_gpu, gpu_list, default_gpu)
            gpu_device_model_name, device_vendor_id = Libsysmon.get_device_model_name_vendor_id(selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)
        except Exception:
            gpu_device_model_name = "-"
        current_resolution, current_refresh_rate = Libsysmon.get_resolution_refresh_rate()
        current_resolution_refresh_rate = Libsysmon.monitor_resolution_refresh_rate_multiple_text(current_resolution, current_refresh_rate)

        # Set multiple label text
        label_list = [self.cpu_vendor_model_label,
                      self.memory_capacity_label,
                      self.gpu_vendor_model_label,
                      self.monitors_label]

        label_data_list = [cpu_model_name,
                           memory_capacity_text,
                           gpu_device_model_name,
                           current_resolution_refresh_rate]

        # Remove labels and Grid row of GPU (2) if they are added before.
        widget_at_gpu2_label_position = self.grid_hardware.get_child_at(1, 3)
        if widget_at_gpu2_label_position == self.gpu_vendor_model_label2:
            self.grid_hardware.remove(self.gpu2_label)
            self.grid_hardware.remove(self.gpu_vendor_model_label2)
            self.grid_hardware.remove_row(3)

        # Add labels, Grid row and get GPU vendor-model information for GPU (2).
        if len(gpu_list) > 1:
            self.grid_hardware.insert_row(3)
            self.grid_hardware.attach(self.gpu2_label, 0, 3, 1, 1)
            self.grid_hardware.attach(self.gpu_vendor_model_label2, 1, 3, 3, 1)
            try:
                # Get vendor-model information of another GPU (not boot VGA).
                for i, gpu in enumerate(gpu_list):
                    if i != selected_gpu_number:
                        selected_gpu_number2 = i
                # Get GPU vendor-model information
                gpu_device_model_name2, device_vendor_id2 = Libsysmon.get_device_model_name_vendor_id(selected_gpu_number2, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)
            except Exception:
                gpu_device_model_name2 = "-"
            # Add label and label data into lists for showing information
            label_list.insert(3, self.gpu_vendor_model_label2)
            label_data_list.insert(3, gpu_device_model_name2)

        GLib.idle_add(self.set_multiple_label_text, label_list, label_data_list)


    def apt_or_rpm_or_pacman_or_apk_packages_count_func(self):
        apt_or_rpm_or_pacman_or_apk_packages_count = Libsysmon.get_installed_apt_rpm_pacman_apk_packages()
        # Stop and hide spinner and set label text.
        GLib.idle_add(Common.set_label_spinner, self.system_packages_label, self.system_packages_spinner_label, apt_or_rpm_or_pacman_or_apk_packages_count)


    def flatpak_packages_count_func(self):
        flatpak_packages_count = Libsysmon.get_installed_flatpak_packages()
        # Stop and hide spinner and set label text.
        GLib.idle_add(Common.set_label_spinner, self.flatpak_packages_label, self.flatpak_packages_spinner_label, flatpak_packages_count)


System = System()


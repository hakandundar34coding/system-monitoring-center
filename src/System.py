import tkinter as tk
from tkinter import ttk

import subprocess
import os
import platform
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

        self.tab_frame = ttk.Frame(MainWindow.system_tab_main_frame)
        self.tab_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.tab_frame.columnconfigure(0, weight=1)
        self.tab_frame.rowconfigure(1, weight=1)

        self.tab_title_frame()

        self.information_frame()


    def tab_title_frame(self):
        """
        Generate tab name, os name-version, computer vendor-model labels and refresh button.
        """

        # Frame (tab title)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=0, column=0, sticky="new", padx=0, pady=(0, 10))
        frame.columnconfigure(2, weight=1)

        # Label (System)
        label = Common.tab_title_label(frame, _tr("System"))

        # Label (OS name-version)
        self.os_name_version_label = Common.device_vendor_model_label(frame)
        tooltip = Common.tooltip(self.os_name_version_label, _tr("Operating System (OS)"))

        # Label (computer vendor-model)
        self.computer_vendor_model_label = Common.device_kernel_name_label(frame)
        tooltip = Common.tooltip(self.computer_vendor_model_label, _tr("Computer"))


    def information_frame(self):
        """
        Generate performance/information labels.
        """

        # Frame (performance/information labels)
        performance_info_frame = ttk.Frame(self.tab_frame)
        performance_info_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=6)
        performance_info_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="equal")
        #performance_info_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), uniform="equal")

        # Label (CPU)
        label = Common.static_information_label(performance_info_frame, _tr("CPU") + ":")
        label.grid(row=0, column=0, sticky="w", padx=0, pady=1)
        # Label (CPU)
        self.cpu_label = Common.dynamic_information_label(performance_info_frame)
        self.cpu_label.grid(row=0, column=1, columnspan=3, sticky="w", padx=(12, 0), pady=1)

        # Label (Memory)
        label = Common.static_information_label(performance_info_frame, _tr("Memory") + ":")
        label.grid(row=1, column=0, sticky="w", padx=0, pady=1)
        # Label (Memory)
        self.memory_label = Common.dynamic_information_label(performance_info_frame)
        self.memory_label.grid(row=1, column=1, columnspan=3, sticky="w", padx=(12, 0), pady=1)

        # Label (GPU)
        label = Common.static_information_label(performance_info_frame, _tr("GPU") + ":")
        label.grid(row=2, column=0, sticky="w", padx=0, pady=1)
        # Label (GPU)
        self.gpu_label = Common.dynamic_information_label(performance_info_frame)
        self.gpu_label.grid(row=2, column=1, columnspan=3, sticky="w", padx=(12, 0), pady=1)

        # Label (GPU (2))
        label = Common.static_information_label(performance_info_frame, _tr("GPU") + " (2)" + ":")
        label.grid(row=3, column=0, sticky="w", padx=0, pady=1)
        # Label (GPU (2))
        self.gpu2_label = Common.dynamic_information_label(performance_info_frame)
        self.gpu2_label.grid(row=3, column=1, columnspan=3, sticky="w", padx=(12, 0), pady=1)

        # Label (Resolution)
        label = Common.static_information_label(performance_info_frame, _tr("Resolution") + ":")
        label.grid(row=4, column=0, sticky="w", padx=0, pady=1)
        # Label (Resolution)
        self.resolution_label = Common.dynamic_information_label(performance_info_frame)
        self.resolution_label.grid(row=4, column=1, columnspan=3, sticky="w", padx=(12, 0), pady=1)

        # Separator
        separator = ttk.Separator(performance_info_frame, orient="horizontal")
        separator.grid(row=5, column=0, columnspan=4, sticky="ew", padx=0, pady=6)


        # Performance information labels
        # Label - Title (Computer)
        label = Common.bold_label(performance_info_frame, _tr("Computer"))
        label.grid(row=6, column=0, columnspan=2, sticky="w", padx=0, pady=5)

        # Label (Vendor)
        label = Common.static_information_label(performance_info_frame, _tr("Vendor") + ":")
        label.grid(row=7, column=0, sticky="w", padx=0, pady=1)
        # Label (Vendor)
        self.vendor_label = Common.dynamic_information_label(performance_info_frame)
        self.vendor_label.grid(row=7, column=1, sticky="w", padx=(12, 0), pady=1)

        # Label (Model)
        label = Common.static_information_label(performance_info_frame, _tr("Model") + ":")
        label.grid(row=8, column=0, sticky="w", padx=0, pady=1)
        # Label (Model)
        self.model_label = Common.dynamic_information_label(performance_info_frame)
        self.model_label.grid(row=8, column=1, sticky="w", padx=(12, 0), pady=1)

        # Label (Computer Type)
        label = Common.static_information_label(performance_info_frame, _tr("Computer Type") + ":")
        label.grid(row=9, column=0, sticky="w", padx=0, pady=1)
        # Label (Computer Type)
        self.computer_type_label = Common.dynamic_information_label(performance_info_frame)
        self.computer_type_label.grid(row=9, column=1, sticky="w", padx=(12, 0), pady=1)

        # Label (Name)
        label = Common.static_information_label(performance_info_frame, _tr("Name") + ":")
        label.grid(row=10, column=0, sticky="w", padx=0, pady=1)
        # Label (Name)
        self.computer_name_label = Common.dynamic_information_label(performance_info_frame)
        self.computer_name_label.grid(row=10, column=1, sticky="w", padx=(12, 0), pady=1)

        # Label (Architecture)
        label = Common.static_information_label(performance_info_frame, _tr("Architecture") + ":")
        label.grid(row=11, column=0, sticky="w", padx=0, pady=1)
        # Label (Architecture)
        self.architecture_label = Common.dynamic_information_label(performance_info_frame)
        self.architecture_label.grid(row=11, column=1, sticky="w", padx=(12, 0), pady=1)

        # Label (Number Of Monitors)
        label = Common.static_information_label(performance_info_frame, _tr("Number Of Monitors") + ":")
        label.grid(row=12, column=0, sticky="w", padx=0, pady=1)
        # Label (Number Of Monitors)
        self.number_of_monitors_label = Common.dynamic_information_label(performance_info_frame)
        self.number_of_monitors_label.grid(row=12, column=1, sticky="w", padx=(12, 0), pady=1)


        # Label - Title (Operating System (OS))
        label = Common.bold_label(performance_info_frame, _tr("Operating System (OS)"))
        label.grid(row=6, column=2, columnspan=2, sticky="w", padx=0, pady=5)

        # Label (Name)
        label = Common.static_information_label(performance_info_frame, _tr("Name") + ":")
        label.grid(row=7, column=2, sticky="w", padx=0, pady=1)
        # Label (Name)
        self.os_name_label = Common.dynamic_information_label(performance_info_frame)
        self.os_name_label.grid(row=7, column=3, sticky="w", padx=(12, 0), pady=1)

        # Label (Version - Code Name)
        label = Common.static_information_label(performance_info_frame, _tr("Version - Code Name") + ":")
        label.grid(row=8, column=2, sticky="w", padx=0, pady=1)
        # Label (Version - Code Name)
        self.version_codename_label = Common.dynamic_information_label(performance_info_frame)
        self.version_codename_label.grid(row=8, column=3, sticky="w", padx=(12, 0), pady=1)

        # Label (OS Family)
        label = Common.static_information_label(performance_info_frame, _tr("OS Family") + ":")
        label.grid(row=9, column=2, sticky="w", padx=0, pady=1)
        # Label (OS Family)
        self.os_family_label = Common.dynamic_information_label(performance_info_frame)
        self.os_family_label.grid(row=9, column=3, sticky="w", padx=(12, 0), pady=1)

        # Label (Based On)
        label = Common.static_information_label(performance_info_frame, _tr("Based On") + ":")
        label.grid(row=10, column=2, sticky="w", padx=0, pady=1)
        # Label (Based On)
        self.based_on_label = Common.dynamic_information_label(performance_info_frame)
        self.based_on_label.grid(row=10, column=3, sticky="w", padx=(12, 0), pady=1)

        # Label (Kernel Release)
        label = Common.static_information_label(performance_info_frame, _tr("Kernel Release") + ":")
        label.grid(row=11, column=2, sticky="w", padx=0, pady=1)
        # Label (Kernel Release)
        self.kernel_release_label = Common.dynamic_information_label(performance_info_frame)
        self.kernel_release_label.grid(row=11, column=3, sticky="w", padx=(12, 0), pady=1)

        # Label (Kernel Version)
        label = Common.static_information_label(performance_info_frame, _tr("Kernel Version") + ":")
        label.grid(row=12, column=2, sticky="w", padx=0, pady=1)
        # Label (Kernel Version)
        self.kernel_version_label = Common.dynamic_information_label(performance_info_frame)
        self.kernel_version_label.grid(row=12, column=3, sticky="w", padx=(12, 0), pady=1)

        # Separator
        separator = ttk.Separator(performance_info_frame, orient="horizontal")
        separator.grid(row=13, column=0, columnspan=4, sticky="ew", padx=0, pady=6)

         # Label - Title (Packages)
        label = Common.bold_label(performance_info_frame, _tr("Packages"))
        label.grid(row=14, column=0, columnspan=2, sticky="w", padx=0, pady=5)

        # Label (System)
        label = Common.static_information_label(performance_info_frame, _tr("System") + ":")
        label.grid(row=15, column=0, sticky="w", padx=0, pady=1)
        # Label (System)
        self.system_packages_label = Common.dynamic_information_label(performance_info_frame)
        self.system_packages_label.grid(row=15, column=1, sticky="w", padx=(12, 0), pady=1)

        # Label (Flatpak)
        label = Common.static_information_label(performance_info_frame, _tr("Flatpak") + ":")
        label.grid(row=16, column=0, sticky="w", padx=0, pady=1)
        tooltip = Common.tooltip(label, _tr("Number of installed Flatpak applications and runtimes"))
        # Label (Flatpak)
        self.flatpak_packages_label = Common.dynamic_information_label(performance_info_frame)
        self.flatpak_packages_label.grid(row=16, column=1, sticky="w", padx=(12, 0), pady=1)

        # Label (Tkinter Version)
        label = Common.static_information_label(performance_info_frame, _tr("Tkinter Version") + ":")
        label.grid(row=17, column=0, sticky="w", padx=0, pady=1)
        tooltip = Common.tooltip(label, _tr("Version for the currently running software"))
        # Label (Tkinter Version)
        self.tk_version_label = Common.dynamic_information_label(performance_info_frame)
        self.tk_version_label.grid(row=17, column=1, sticky="w", padx=(12, 0), pady=1)

        # Label (Python Version)
        label = Common.static_information_label(performance_info_frame, _tr("Python Version") + ":")
        label.grid(row=18, column=0, sticky="w", padx=0, pady=1)
        tooltip = Common.tooltip(label, _tr("Version for the currently running software"))
        # Label (Python Version)
        self.python_version_label = Common.dynamic_information_label(performance_info_frame)
        self.python_version_label.grid(row=18, column=1, sticky="w", padx=(12, 0), pady=1)

        # There is a separator between rows 6 and 8.


       # Label - Title (Graphical User Interface (GUI))
        label = Common.bold_label(performance_info_frame, _tr("Graphical User Interface (GUI)"))
        label.grid(row=14, column=2, columnspan=2, sticky="w", padx=0, pady=5)

        # Label (Desktop Environment)
        label = Common.static_information_label(performance_info_frame, _tr("Desktop Environment") + ":")
        label.grid(row=15, column=2, sticky="w", padx=0, pady=1)
        # Label (Desktop Environment)
        self.desktop_environment_label = Common.dynamic_information_label(performance_info_frame)
        self.desktop_environment_label.grid(row=15, column=3, sticky="w", padx=(12, 0), pady=1)

        # Label (Windowing System)
        label = Common.static_information_label(performance_info_frame, _tr("Windowing System") + ":")
        label.grid(row=16, column=2, sticky="w", padx=0, pady=1)
        # Label (Windowing System)
        self.windowing_system_label = Common.dynamic_information_label(performance_info_frame)
        self.windowing_system_label.grid(row=16, column=3, sticky="w", padx=(12, 0), pady=1)

        # Label (Window Manager)
        label = Common.static_information_label(performance_info_frame, _tr("Window Manager") + ":")
        label.grid(row=17, column=2, sticky="w", padx=0, pady=1)
        # Label (Window Manager)
        self.window_manager_label = Common.dynamic_information_label(performance_info_frame)
        self.window_manager_label.grid(row=17, column=3, sticky="w", padx=(12, 0), pady=1)

        # Label (Display Manager)
        label = Common.static_information_label(performance_info_frame, _tr("Display Manager") + ":")
        label.grid(row=18, column=2, sticky="w", padx=0, pady=1)
        # Label (Display Manager)
        self.display_manager_label = Common.dynamic_information_label(performance_info_frame)
        self.display_manager_label.grid(row=18, column=3, sticky="w", padx=(12, 0), pady=1)


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
        #threading.Thread(target=self.get_computer_hardware_information, daemon=True).start()
        cpu_architecture = Libsysmon.get_cpu_architecture()
        computer_vendor, computer_model, computer_chassis_type = Libsysmon.get_computer_vendor_model_chassis_type()
        host_name = Libsysmon.get_host_name()
        number_of_monitors = Libsysmon.get_number_of_monitors()
        current_python_version = Libsysmon.get_current_python_version()
        current_tk_version = Libsysmon.get_current_tk_version()
        windowing_system = Libsysmon.get_windowing_system()
        current_desktop_environment, current_desktop_environment_version, window_manager, current_display_manager = Libsysmon.get_desktop_environment_and_version_window_manager_display_manager()
        # Run this function in a separate thread because it may take a long time (2-3 seconds) to get the information on some systems (such as rpm based systems) and it blocks the GUI during this process if a separate thread is not used.
        threading.Thread(target=self.system_packages_count_func, daemon=True).start()
        threading.Thread(target=self.flatpak_packages_count_func, daemon=True).start()
        self.get_computer_hardware_information()

        # Set label texts to show information
        self.os_name_version_label.config(text=f'{os_name} - {os_version}')
        self.computer_vendor_model_label.config(text=f'{computer_vendor} - {computer_model}')
        self.os_name_label.config(text=os_name)
        self.version_codename_label.config(text=os_version)
        self.os_family_label.config(text=os_family)
        self.based_on_label.config(text=os_based_on)
        self.kernel_release_label.config(text=kernel_release)
        self.kernel_version_label.config(text=kernel_version)
        self.desktop_environment_label.config(text=f'{current_desktop_environment} ({current_desktop_environment_version})')
        self.windowing_system_label.config(text=windowing_system)
        self.window_manager_label.config(text=window_manager)
        self.display_manager_label.config(text=current_display_manager)
        self.vendor_label.config(text=computer_vendor)
        self.model_label.config(text=computer_model)
        self.computer_type_label.config(text=computer_chassis_type)
        self.computer_name_label.config(text=host_name)
        self.architecture_label.config(text=cpu_architecture)
        self.number_of_monitors_label.config(text=f'{number_of_monitors}')
        #self.system_packages_label.config(text=f'{apt_or_rpm_or_pacman_packages_count}')
        #self.flatpak_packages_label.config(text=f'{flatpak_packages_count}')
        self.tk_version_label.config(text=current_tk_version)
        self.python_version_label.config(text=f'{current_python_version}')

        self.initial_already_run = 1


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
        #current_resolution, current_refresh_rate = Libsysmon.get_resolution_refresh_rate()
        current_resolution_refresh_rate = Libsysmon.monitor_resolution_refresh_rate_multiple_text(MainWindow.main_window)

        if len(gpu_list) > 1:
            try:
                # Get vendor-model information of another GPU (not boot VGA).
                for i, gpu in enumerate(gpu_list):
                    if i != selected_gpu_number:
                        selected_gpu_number2 = i
                # Get GPU vendor-model information
                gpu_device_model_name2, device_vendor_id2 = Libsysmon.get_device_model_name_vendor_id(selected_gpu_number2, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)
            except Exception:
                gpu_device_model_name2 = "-"
        else:
            gpu_device_model_name2 = "-"

        self.cpu_label.config(text=cpu_model_name)
        self.memory_label.config(text=memory_capacity_text)
        self.gpu_label.config(text=gpu_device_model_name)
        self.gpu2_label.config(text=gpu_device_model_name2)
        self.resolution_label.config(text=current_resolution_refresh_rate)


    def system_packages_count_func(self):
        system_packages_count = Libsysmon.get_installed_system_packages()
        # Stop and hide spinner and set label text.
        MainWindow.main_window.after(0, lambda: self.system_packages_label.config(text=system_packages_count))


    def flatpak_packages_count_func(self):
        flatpak_packages_count = Libsysmon.get_installed_flatpak_packages()
        # Stop and hide spinner and set label text.
        MainWindow.main_window.after(0, lambda: self.flatpak_packages_label.config(text=flatpak_packages_count))

System = System()


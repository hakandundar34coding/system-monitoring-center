import tkinter as tk
from tkinter import ttk

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class Cpu:

    def __init__(self):

        self.name = "Cpu"

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_frame = ttk.Frame(MainWindow.cpu_tab_main_frame)
        self.tab_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.tab_frame.columnconfigure(0, weight=1)
        self.tab_frame.rowconfigure(1, weight=1)

        self.tab_title_frame()

        self.da_frame()

        self.information_frame()


    def tab_title_frame(self):
        """
        Generate tab name, device name labels.
        """

        # Grid (tab title)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=0, column=0, sticky="new", padx=0, pady=(0, 10))
        """frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)"""

        # Label (CPU)
        label = Common.tab_title_label(frame, _tr("CPU"))

        # Label (device vendor-model label)
        self.device_vendor_model_label = Common.device_vendor_model_label(frame)
        tooltip = Common.tooltip(self.device_vendor_model_label, _tr("Vendor - Model"))

        # Label (device kernel name)
        self.device_kernel_name_label = Common.device_kernel_name_label(frame)
        tooltip = Common.tooltip(self.device_kernel_name_label, _tr("Device Name In Kernel"))


    def da_frame(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Frame (drawingarea)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(0, 10))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Label (drawingarea upper-left)
        self.da_upper_left_label = Common.da_upper_lower_label(frame, _tr("CPU Usage (Average)"))
        self.da_upper_left_label.grid(row=0, column=0, sticky="w")

        # Label (drawingarea upper-right)
        label = Common.da_upper_lower_label(frame, "100%")
        label.grid(row=0, column=1, sticky="e")

        # Label (for showing graphics)
        self.da_cpu_usage = Common.drawingarea(frame, "da_cpu_usage")
        self.da_cpu_usage.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label(frame, "0")
        label.grid(row=2, column=1, sticky="e")


    def information_frame(self):
        """
        Generate performance/information labels.
        """

        # Frame (performance/information labels)
        performance_info_grid = ttk.Frame(self.tab_frame)
        performance_info_grid.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        performance_info_grid.columnconfigure((0, 1), weight=1, uniform="equal")
        performance_info_grid.rowconfigure((0, 1), weight=1, uniform="equal")
        #performance_info_grid.rowconfigure(0, weight=1)

        # Styled information widgets (Average Usage and Frequency)
        # Frame (Average Usage and Frequency)
        _frame, self.average_usage_label, self.frequency_label = Common.styled_information_scrolledwindow(performance_info_grid, _tr("Average Usage"), _tr("Average CPU usage of all cores"), _tr("Frequency"), None)
        _frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=(0, 5))

        # Styled information widgets (Processes-Threads and Up Time)
        # Frame (Processes-Threads and Up Time)
        _frame, self.processes_threads_label, self.up_time_label = Common.styled_information_scrolledwindow(performance_info_grid, _tr("Processes-Threads"), None, _tr("Up Time"), None)
        _frame.grid(row=1, column=0, sticky="nsew", padx=(0, 15), pady=(5, 0))

        # Frame - Right information labels
        performance_info_right_frame = ttk.Frame(performance_info_grid)
        performance_info_right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=0, pady=0)
        performance_info_right_frame.columnconfigure((0, 1), weight=1, uniform="equal")

        # Labels - Right information labels
        # Label (Min-Max Frequency)
        label = Common.static_information_label(performance_info_right_frame, _tr("Min-Max Frequency") + ":")
        label.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Min-Max Frequency)
        self.min_max_frequency_label = Common.dynamic_information_label(performance_info_right_frame)
        self.min_max_frequency_label.grid(row=0, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Cache (L1d-L1i))
        label = Common.static_information_label(performance_info_right_frame, _tr("Cache (L1d-L1i)") + ":")
        label.grid(row=1, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Cache (L1d-L1i))
        self.cache_l1d_l1i_label = Common.dynamic_information_label(performance_info_right_frame)
        self.cache_l1d_l1i_label.grid(row=1, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Cache (L2-L3))
        label = Common.static_information_label(performance_info_right_frame, _tr("Cache (L2-L3)") + ":")
        label.grid(row=2, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Cache (L2-L3))
        self.cache_l2_l3_label = Common.dynamic_information_label(performance_info_right_frame)
        self.cache_l2_l3_label.grid(row=2, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (CPU Sockets)
        label = Common.static_information_label(performance_info_right_frame, _tr("CPU Sockets") + ":")
        label.grid(row=3, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (CPU Sockets)
        self.cpu_sockets_label = Common.dynamic_information_label(performance_info_right_frame)
        self.cpu_sockets_label.grid(row=3, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Cores (Physical-Logical))
        label = Common.static_information_label(performance_info_right_frame, _tr("Cores (Physical-Logical)") + ":")
        label.grid(row=4, column=0, sticky="w", padx=0, pady=(0, 4))
        tooltip = Common.tooltip(label, _tr("Number of online physical and logical CPU cores"))
        # Label (Cores (Physical-Logical))
        self.cores_phy_log_label = Common.dynamic_information_label(performance_info_right_frame)
        self.cores_phy_log_label.grid(row=4, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Architecture)
        label = Common.static_information_label(performance_info_right_frame, _tr("Architecture") + ":")
        label.grid(row=5, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Architecture)
        self.architecture_label = Common.dynamic_information_label(performance_info_right_frame)
        self.architecture_label.grid(row=5, column=1, sticky="w", padx=(4, 0), pady=(0, 4))


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        selected_cpu_core = Performance.selected_cpu_core
        self.selected_cpu_core_prev = selected_cpu_core
        self.logical_core_list_prev = list(Performance.logical_core_list)

        # Get information
        cpu_core_min_frequency, cpu_core_max_frequency = Libsysmon.get_cpu_core_min_max_frequency(selected_cpu_core)
        if Config.show_cpu_cache_type == "socket":
            cpu_l1d_cache, cpu_l1i_cache, cpu_l2_cache, cpu_l3_cache = Libsysmon.get_cpu_socket_l1_l2_l3_cache(selected_cpu_core)
        elif Config.show_cpu_cache_type == "core":
            cpu_l1d_cache, cpu_l1i_cache, cpu_l2_cache, cpu_l3_cache = Libsysmon.get_cpu_core_l1_l2_l3_cache(selected_cpu_core)
        cpu_architecture = Libsysmon.get_cpu_architecture()

        # Show information on labels
        show_cpu_usage_per_core = Config.show_cpu_usage_per_core
        if show_cpu_usage_per_core == 0:
            self.da_upper_left_label.config(text=_tr("CPU Usage (Average)"))
        elif show_cpu_usage_per_core == 1:
            self.da_upper_left_label.config(text=_tr("CPU Usage (Per Core)"))
        if isinstance(cpu_core_max_frequency, str) is False:
            self.min_max_frequency_label.config(text=f'{cpu_core_min_frequency:.2f} - {cpu_core_max_frequency:.2f} GHz')
        else:
            self.min_max_frequency_label.config(text=f'{cpu_core_min_frequency} - {cpu_core_max_frequency}')
        self.architecture_label.config(text=cpu_architecture)
        self.cache_l1d_l1i_label.config(text=f'{cpu_l1d_cache} - {cpu_l1i_cache}')
        self.cache_l2_l3_label.config(text=f'{cpu_l2_cache} - {cpu_l3_cache}')

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        number_of_logical_cores = Libsysmon.get_number_of_logical_cores()
        cpu_usage_percent_ave = Performance.cpu_usage_percent_ave
        selected_cpu_core = Performance.selected_cpu_core
        # Run "initial_func" if selected CPU core is changed since the last loop.
        if self.selected_cpu_core_prev != selected_cpu_core:
            self.initial_func()
        self.selected_cpu_core_prev = selected_cpu_core

        # Run "main_gui_device_selection_list" if selected device list is changed since the last loop.
        if self.logical_core_list_prev != Performance.logical_core_list:
            MainWindow.main_gui_device_selection_list()
        self.logical_core_list_prev = list(Performance.logical_core_list)

        Performance.performance_line_charts_draw(self.da_cpu_usage, "da_cpu_usage")

        # Get information
        number_of_physical_cores, number_of_cpu_sockets, cpu_model_name = Libsysmon.get_number_of_physical_cores_sockets_cpu_name(selected_cpu_core, number_of_logical_cores)
        cpu_core_current_frequency = Libsysmon.get_cpu_core_current_frequency(selected_cpu_core)
        number_of_total_processes, number_of_total_threads = Libsysmon.get_processes_threads()
        system_up_time = Libsysmon.get_system_up_time()


        # Show information on labels
        self.device_vendor_model_label.config(text=cpu_model_name)
        self.device_kernel_name_label.config(text=selected_cpu_core)
        self.processes_threads_label.config(text=f'{number_of_total_processes} - {number_of_total_threads}')
        self.up_time_label.config(text=system_up_time)
        self.average_usage_label.config(text=f'{cpu_usage_percent_ave[-1]:.{Config.performance_cpu_usage_percent_precision}f} %')
        self.frequency_label.config(text=f'{cpu_core_current_frequency:.2f} GHz')
        self.cpu_sockets_label.config(text=f'{number_of_cpu_sockets}')
        self.cores_phy_log_label.config(text=f'{number_of_physical_cores} - {number_of_logical_cores}')


Cpu = Cpu()


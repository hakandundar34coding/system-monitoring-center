import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

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

        self.tab_grid = Common.tab_grid()

        self.tab_title_grid()

        self.da_grid()

        self.information_grid()


    def tab_title_grid(self):
        """
        Generate tab name, device name labels.
        """

        # Grid (tab title)
        grid = Gtk.Grid()
        self.tab_grid.attach(grid, 0, 0, 1, 1)

        # Label (CPU)
        label = Common.tab_title_label(_tr("CPU"))
        grid.attach(label, 0, 0, 1, 2)

        # Label (device vendor-model label)
        self.device_vendor_model_label = Common.device_vendor_model_label()
        self.device_vendor_model_label.set_tooltip_text(_tr("Vendor-Model"))
        grid.attach(self.device_vendor_model_label, 1, 0, 1, 1)

        # Label (device kernel name)
        self.device_kernel_name_label = Common.device_kernel_name_label()
        self.device_kernel_name_label.set_tooltip_text(_tr("Device Name In Kernel"))
        grid.attach(self.device_kernel_name_label, 1, 1, 1, 1)


    def da_grid(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Grid (drawingarea)
        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.tab_grid.attach(grid, 0, 1, 1, 1)

        # Label (drawingarea upper-left)
        self.da_upper_left_label = Common.da_upper_lower_label(_tr("CPU Usage (Average)"), Gtk.Align.START)
        grid.attach(self.da_upper_left_label, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        label = Common.da_upper_lower_label("100%", Gtk.Align.END)
        grid.attach(label, 1, 0, 1, 1)

        # DrawingArea (CPU usage)
        self.da_cpu_usage = Common.drawingarea(Performance.performance_line_charts_draw, "da_cpu_usage")
        grid.attach(self.da_cpu_usage, 0, 2, 2, 1)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label("0", Gtk.Align.END)
        grid.attach(label, 0, 3, 2, 1)


    def information_grid(self):
        """
        Generate performance/information labels.
        """

        # Grid (performance/information labels)
        performance_info_grid = Common.performance_info_grid()
        self.tab_grid.attach(performance_info_grid, 0, 2, 1, 1)

        # Styled information widgets (Average Usage and Frequency)
        # ScrolledWindow (Average Usage and Frequency)
        scrolledwindow, self.average_usage_label, self.frequency_label = Common.styled_information_scrolledwindow(_tr("Average Usage"), _tr("Average CPU usage of all cores"), _tr("Frequency"), None)
        performance_info_grid.attach(scrolledwindow, 0, 0, 1, 1)

        # Styled information widgets (Processes-Threads and Up Time)
        # ScrolledWindow (Processes-Threads and Up Time)
        scrolledwindow, self.processes_threads_label, self.up_time_label = Common.styled_information_scrolledwindow(_tr("Processes-Threads"), None, _tr("Up Time"), None)
        performance_info_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # Grid - Right information labels
        performance_info_right_grid = Common.performance_info_right_grid()
        performance_info_grid.attach(performance_info_right_grid, 1, 0, 1, 2)

        # Labels - Right information labels
        # Label (Min-Max Frequency)
        label = Common.static_information_label(_tr("Min-Max Frequency") + ":")
        performance_info_right_grid.attach(label, 0, 0, 1, 1)
        # Label (Min-Max Frequency)
        self.min_max_frequency_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.min_max_frequency_label, 1, 0, 1, 1)

        # Label (Cache (L1d-L1i))
        label = Common.static_information_label(_tr("Cache (L1d-L1i)") + ":")
        performance_info_right_grid.attach(label, 0, 1, 1, 1)
        # Label (Cache (L1d-L1i))
        self.cache_l1d_l1i_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.cache_l1d_l1i_label, 1, 1, 1, 1)

        # Label (Cache (L2-L3))
        label = Common.static_information_label(_tr("Cache (L2-L3)") + ":")
        performance_info_right_grid.attach(label, 0, 2, 1, 1)
        # Label (Cache (L2-L3))
        self.cache_l2_l3_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.cache_l2_l3_label, 1, 2, 1, 1)

        # Label (CPU Sockets)
        label = Common.static_information_label(_tr("CPU Sockets") + ":")
        performance_info_right_grid.attach(label, 0, 3, 1, 1)
        # Label (CPU Sockets)
        self.cpu_sockets_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.cpu_sockets_label, 1, 3, 1, 1)

        # Label (Cores (Physical-Logical))
        label = Common.static_information_label(_tr("Cores (Physical-Logical)") + ":")
        label.set_tooltip_text(_tr("Number of online physical and logical CPU cores"))
        performance_info_right_grid.attach(label, 0, 4, 1, 1)
        # Label (Cores (Physical-Logical))
        self.cores_phy_log_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.cores_phy_log_label, 1, 4, 1, 1)

        # Label (Architecture)
        label = Common.static_information_label(_tr("Architecture") + ":")
        performance_info_right_grid.attach(label, 0, 5, 1, 1)
        # Label (Architecture)
        self.architecture_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.architecture_label, 1, 5, 1, 1)


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        selected_cpu_core = Performance.selected_cpu_core
        self.selected_cpu_core_prev = selected_cpu_core
        self.logical_core_list_prev = list(Performance.logical_core_list)

        # Get information
        cpu_core_min_frequency, cpu_core_max_frequency = Libsysmon.get_cpu_core_min_max_frequency(selected_cpu_core)
        cpu_core_l1d_cache, cpu_core_l1i_cache, cpu_core_l2_cache, cpu_core_l3_cache = Libsysmon.get_cpu_core_l1_l2_l3_cache(selected_cpu_core)
        cpu_architecture = Libsysmon.get_cpu_architecture()


        # Show information on labels
        show_cpu_usage_per_core = Config.show_cpu_usage_per_core
        if show_cpu_usage_per_core == 0:
            self.da_upper_left_label.set_label(_tr("CPU Usage (Average)"))
        if show_cpu_usage_per_core == 1:
            self.da_upper_left_label.set_label(_tr("CPU Usage (Per Core)"))
        if isinstance(cpu_core_max_frequency, str) is False:
            self.min_max_frequency_label.set_label(f'{cpu_core_min_frequency:.2f} - {cpu_core_max_frequency:.2f} GHz')
        else:
            self.min_max_frequency_label.set_label(f'{cpu_core_min_frequency} - {cpu_core_max_frequency}')
        self.architecture_label.set_label(cpu_architecture)
        self.cache_l1d_l1i_label.set_label(f'{cpu_core_l1d_cache} - {cpu_core_l1i_cache}')
        self.cache_l2_l3_label.set_label(f'{cpu_core_l2_cache} - {cpu_core_l3_cache}')

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

        self.da_cpu_usage.queue_draw()

        # Get information
        number_of_physical_cores, number_of_cpu_sockets, cpu_model_name = Libsysmon.get_number_of_physical_cores_sockets_cpu_name(selected_cpu_core, number_of_logical_cores)
        cpu_core_current_frequency = Libsysmon.get_cpu_core_current_frequency(selected_cpu_core)
        number_of_total_processes, number_of_total_threads = Libsysmon.get_processes_threads()
        system_up_time = Libsysmon.get_system_up_time()


        # Show information on labels
        self.device_vendor_model_label.set_label(cpu_model_name)
        self.device_kernel_name_label.set_label(selected_cpu_core)
        self.processes_threads_label.set_label(f'{number_of_total_processes} - {number_of_total_threads}')
        self.up_time_label.set_label(system_up_time)
        self.average_usage_label.set_label(f'{cpu_usage_percent_ave[-1]:.{Config.performance_cpu_usage_percent_precision}f} %')
        self.frequency_label.set_label(f'{cpu_core_current_frequency:.2f} GHz')
        self.cpu_sockets_label.set_label(f'{number_of_cpu_sockets}')
        self.cores_phy_log_label.set_label(f'{number_of_physical_cores} - {number_of_logical_cores}')


Cpu = Cpu()


import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import os
import platform

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from MainWindow import MainWindow
import Common


class Cpu:

    def __init__(self):

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


    def cpu_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        selected_cpu_core = Performance.selected_cpu_core
        self.selected_cpu_core_prev = selected_cpu_core
        self.logical_core_list_prev = list(Performance.logical_core_list)

        # Get information.
        cpu_core_min_frequency, cpu_core_max_frequency = self.cpu_core_min_max_frequency_func(selected_cpu_core)
        cpu_core_l1d_cache, cpu_core_l1i_cache, cpu_core_l2_cache, cpu_core_l3_cache = self.cpu_core_l1_l2_l3_cache_func(selected_cpu_core)
        cpu_architecture = self.architecture_func()


        # Show information on labels.
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


    def cpu_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        number_of_logical_cores = Performance.number_of_logical_cores
        cpu_usage_percent_ave = Performance.cpu_usage_percent_ave
        selected_cpu_core = Performance.selected_cpu_core
        # Run "cpu_initial_func" if selected CPU core is changed since the last loop.
        if self.selected_cpu_core_prev != selected_cpu_core:
            self.cpu_initial_func()
        self.selected_cpu_core_prev = selected_cpu_core

        # Run "main_gui_device_selection_list" if selected device list is changed since the last loop.
        if self.logical_core_list_prev != Performance.logical_core_list:
            MainWindow.main_gui_device_selection_list()
        self.logical_core_list_prev = list(Performance.logical_core_list)

        self.da_cpu_usage.queue_draw()

        # Get information.
        number_of_physical_cores, number_of_cpu_sockets, cpu_model_name = self.number_of_physical_cores_sockets_cpu_name_func(selected_cpu_core, number_of_logical_cores)
        cpu_core_current_frequency = self.cpu_core_current_frequency_func(selected_cpu_core)
        number_of_total_processes, number_of_total_threads = self.processes_threads_func()
        system_up_time = self.system_up_time_func()


        # Show information on labels.
        self.device_vendor_model_label.set_label(cpu_model_name)
        self.device_kernel_name_label.set_label(selected_cpu_core)
        self.processes_threads_label.set_label(f'{number_of_total_processes} - {number_of_total_threads}')
        self.up_time_label.set_label(system_up_time)
        self.average_usage_label.set_label(f'{cpu_usage_percent_ave[-1]:.{Config.performance_cpu_usage_percent_precision}f} %')
        self.frequency_label.set_label(f'{cpu_core_current_frequency:.2f} GHz')
        self.cpu_sockets_label.set_label(f'{number_of_cpu_sockets}')
        self.cores_phy_log_label.set_label(f'{number_of_physical_cores} - {number_of_logical_cores}')


    def cpu_core_min_max_frequency_func(self, selected_cpu_core):
        """
        Get minimum and maximum frequencies of the CPU core.
        """

        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cpufreq/scaling_max_freq") as reader:
                cpu_core_max_frequency = float(reader.read().strip()) / 1000000
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cpufreq/scaling_min_freq") as reader:
                cpu_core_min_frequency = float(reader.read().strip()) / 1000000
        except FileNotFoundError:
            cpu_core_max_frequency = "-"
            cpu_core_min_frequency = "-"

        return cpu_core_min_frequency, cpu_core_max_frequency


    def cpu_core_l1_l2_l3_cache_func(self, selected_cpu_core):
        """
        Get L1i, L1d, L2, L3 cache memory values of the CPU core.
        """

        # Get l1d cache
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/type") as reader:
                cache_type = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index0/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "1" and cache_type == "Data":
                cpu_core_l1d_cache = cache_size
        except FileNotFoundError:
            cpu_core_l1d_cache = "-"

        # Get li cache
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/type") as reader:
                cache_type = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index1/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "1" and cache_type == "Instruction":
                cpu_core_l1i_cache = cache_size
        except FileNotFoundError:
            cpu_core_l1i_cache = "-"

        # Get l2 cache
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index2/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "2":
                cpu_core_l2_cache = cache_size
        except FileNotFoundError:
            cpu_core_l2_cache = "-"

        # Get l3 cache
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/level") as reader:
                cache_level = reader.read().strip()
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cache/index3/size") as reader:
                cache_size = reader.read().strip()
            if cache_level == "3":
                cpu_core_l3_cache = cache_size
        except FileNotFoundError:
            cpu_core_l3_cache = "-"

        return cpu_core_l1d_cache, cpu_core_l1i_cache, cpu_core_l2_cache, cpu_core_l3_cache


    def architecture_func(self):
        """
        Get CPU architecture.
        """

        cpu_architecture = platform.processor()
        if cpu_architecture == "":
            cpu_architecture = platform.machine()
            if cpu_architecture == "":
                cpu_architecture = "-"

        return cpu_architecture


    def number_of_physical_cores_sockets_cpu_name_func(self, selected_cpu_core, number_of_logical_cores):
        """
        Get number of physical cores, number of cpu sockets, cpu_model_names.
        """

        selected_cpu_core_number = Performance.logical_core_list.index(selected_cpu_core)

        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_output = reader.read()
        proc_cpuinfo_output_lines = proc_cpuinfo_output.split("\n")

        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "x86_64" architecture.
        # Physical and logical cores and model name per core information are tracked easily on this platform.
        if "physical id" in proc_cpuinfo_output:
            cpu_model_names = []
            number_of_physical_cores = 0
            physical_id = 0
            physical_id_prev = 0
            for line in proc_cpuinfo_output_lines:
                if line.startswith("physical id"):
                    physical_id_prev = physical_id
                    physical_id = line.split(":")[1].strip()
                if physical_id != physical_id_prev and line.startswith("cpu cores"):
                    number_of_physical_cores = number_of_physical_cores + int(line.split(":")[1].strip())
                if line.startswith("model name"):
                    cpu_model_names.append(line.split(":")[1].strip())
            number_of_cpu_sockets = int(physical_id) + 1
            cpu_model_name = cpu_model_names[selected_cpu_core_number]

        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "ARM" architecture.
        #xPhysical and logical cores and model name per core information are not tracked easily on this platform.
        # Different ARM processors (v6, v7, v8 or models of same ARM vX processors) may have different information in "/proc/cpuinfo" file.
        else:
            cpu_model_names = []
            number_of_physical_cores = number_of_logical_cores
            number_of_cpu_sockets = 1

            cpu_implementer_list = []
            cpu_architecture_list = []
            cpu_part_list = []

            # Get register values to get required information.
            for line in proc_cpuinfo_output_lines:
                # "CPU implementer" is used for getting vendor.
                if line.startswith("CPU implementer"):
                    cpu_implementer_list.append(line.split(":")[-1].strip())
                # "CPU architecture" is used for getting architecture.
                elif line.startswith("CPU architecture"):
                    cpu_architecture_list.append(line.split(":")[-1].strip())
                # "CPU part" is used for getting core model such as Cortex-A57.
                elif line.startswith("CPU part"):
                    cpu_part_list.append(line.split(":")[-1].strip())

            # Redefine "selected_cpu_core_number" in order to get information of the selected CPU core.
            if len(cpu_implementer_list) == number_of_logical_cores:
                selected_cpu_core_number = selected_cpu_core_number
            # There may be only one instance of register values even if CPU has multiple cores.
            else:
                selected_cpu_core_number = 0

            # Get CPU model information by using register values.
            cpu_implementer = "-"
            cpu_architecture = "-"
            cpu_part = "-"
            # Read database file for ARM CPU register values.
            with open(os.path.dirname(os.path.realpath(__file__)) + "/../database/arm.ids") as reader:
                ids_file_output = reader.read().strip()
            # Define ARM architecture dictionary.
            arm_architecture_dict = {"5TE": "ARMv5", "6TEJ": "ARMv6", "7": "ARMv7", "8": "ARMv8"}
            # Get device vendor, model names from device ID file content.
            search_text1 = cpu_implementer_list[selected_cpu_core_number].split("0x", 1)[-1]
            search_text2 = "\t" + cpu_part_list[selected_cpu_core_number].split("0x", 1)[-1]
            if search_text1 in ids_file_output:
                rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
                cpu_implementer = rest_of_the_ids_file_output.split("\n", 1)[0].strip()
                if search_text2 in ids_file_output:
                    cpu_part = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0].strip()
                else:
                    cpu_part = "-"
            else:
                cpu_implementer = "-"
                cpu_part = "-"
            try:
                cpu_architecture = arm_architecture_dict[cpu_architecture_list[selected_cpu_core_number]]
            except KeyError:
                cpu_architecture = "-"
            cpu_model_name = f'{cpu_implementer} {cpu_part} ({cpu_architecture})'
            # Get CPU model information by using "/proc/cpuinfo" file if CPU implementer or CPU part is not detected.
            if cpu_implementer == "-" or cpu_part == "-":
                cpu_model_name = "-"
                for line in proc_cpuinfo_output_lines:
                    if line.startswith("model name"):
                        cpu_model_name = line.split(":")[-1].strip()
                if cpu_model_name == "-":
                    for line in proc_cpuinfo_output_lines:
                        if line.startswith("Processor"):
                            cpu_model_name = line.split(":")[-1].strip()
                if cpu_model_name == "-":
                    cpu_model_name = "[" + _tr("Unknown") + "]"

        return number_of_physical_cores, number_of_cpu_sockets, cpu_model_name


    def cpu_core_current_frequency_func(self, selected_cpu_core):
        """
        Get current frequency of the CPU core.
        '/sys/devices/system/cpu/cpu[NUMBER]/cpufreq' is used instead of '/sys/devices/system/cpu/cpufreq/policy[NUMBER]'.
        Because CPU core current frequencies may be same for all cores on RB-Pi devices and "scaling_cur_freq" file may be available
        # for only 0th core of the relevant CPU group (little cores , big cores).
        """

        cpu_core_current_frequency = "-"

        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cpufreq/scaling_cur_freq") as reader:
                cpu_core_current_frequency = float(reader.read().strip()) / 1000000
        # CPU core current frequency may not be available in "/sys/devices/system/cpu/cpufreq/policy..." folders on virtual machines (x86_64).
        # Get it by reading "/proc/cpuinfo" file.
        except FileNotFoundError:
            with open("/proc/cpuinfo") as reader:
                proc_cpuinfo_all_cores = reader.read().strip().split("\n\n")
            proc_cpuinfo_all_cores_lines = proc_cpuinfo_all_cores[int(selected_cpu_core.split("cpu")[1])].split("\n")
            for line in proc_cpuinfo_all_cores_lines:
                if line.startswith("cpu MHz"):
                    cpu_core_current_frequency = float(line.split(":")[1].strip()) / 1000
                    break

        return cpu_core_current_frequency


    def processes_threads_func(self):
        """
        Get number of threads and number of processes.
        """

        if Config.environment_type == "flatpak":
            import subprocess
            ps_output_lines = (subprocess.check_output(["flatpak-spawn", "--host", "ps", "--no-headers", "-eo", "thcount"], shell=False)).decode().strip().split("\n")
            number_of_total_processes = len(ps_output_lines)
            number_of_total_threads = 0
            for line in ps_output_lines:
                number_of_total_threads = number_of_total_threads + int(line.strip())

        else:
            pid_list = [filename for filename in os.listdir("/proc/") if filename.isdigit()]

            thread_count_list = []
            for pid in pid_list:
                try:
                    with open("/proc/" + pid + "/status") as reader:
                        proc_status_output = reader.read()
                # Skip to the next loop without application error if a "FileNotFoundError" error is encountered
                # when process is ended after process list is get.
                except (FileNotFoundError, ProcessLookupError) as me:
                    continue
                # Append number of threads of the process
                thread_count_list.append(int(proc_status_output.split("\nThreads:", 1)[1].split("\n", 1)[0].strip()))

            number_of_total_processes = len(thread_count_list)
            number_of_total_threads = sum(thread_count_list)

        return number_of_total_processes, number_of_total_threads


    def system_up_time_func(self):
        """
        Get system up time.
        """

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

        system_up_time = f'{sut_days_int:02}:{sut_hours_int:02}:{sut_minutes_int:02}:{sut_seconds_int:02}'

        return system_up_time


Cpu = Cpu()


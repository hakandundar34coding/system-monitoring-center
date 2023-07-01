import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

import os
import subprocess
from threading import Thread

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class Gpu:

    def __init__(self):

        self.name = "Gpu"

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

        # Label (GPU)
        label = Common.tab_title_label(_tr("GPU"))
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
        self.da_upper_left_label = Common.da_upper_lower_label(_tr("GPU Usage"), Gtk.Align.START)
        grid.attach(self.da_upper_left_label, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        label = Common.da_upper_lower_label("100%", Gtk.Align.END)
        grid.attach(label, 1, 0, 1, 1)

        # DrawingArea
        self.da_gpu_usage = Common.drawingarea(Performance.performance_line_charts_draw, "da_gpu_usage")
        grid.attach(self.da_gpu_usage, 0, 2, 2, 1)

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

        # Styled information widgets (GPU Usage and Video Memory)
        # ScrolledWindow (GPU Usage and Video Memory)
        scrolledwindow, self.gpu_usage_label, self.video_memory_label = Common.styled_information_scrolledwindow(_tr("GPU Usage"), None, _tr("Video Memory"), None)
        performance_info_grid.attach(scrolledwindow, 0, 0, 1, 1)

        # Styled information widgets (Frequency and Temperature)
        # ScrolledWindow (Frequency and Temperature)
        scrolledwindow, self.frequency_label, self.temperature_label = Common.styled_information_scrolledwindow(_tr("Frequency"), None, _tr("Temperature"), None)
        performance_info_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # Grid - Right information labels
        performance_info_right_grid = Common.performance_info_right_grid()
        performance_info_grid.attach(performance_info_right_grid, 1, 0, 1, 2)

        # Label (Min-Max Frequency)
        label = Common.static_information_label(_tr("Min-Max Frequency") + ":")
        performance_info_right_grid.attach(label, 0, 0, 1, 1)
        # Label (Min-Max Frequency)
        self.min_max_frequency_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.min_max_frequency_label, 1, 0, 1, 1)

        # Label (Boot VGA)
        label = Common.static_information_label(_tr("Boot VGA") + ":")
        performance_info_right_grid.attach(label, 0, 1, 1, 1)
        # Label (Boot VGA)
        self.boot_vga_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.boot_vga_label, 1, 1, 1, 1)

        # Label (Power Usage)
        label = Common.static_information_label(_tr("Power Usage") + ":")
        performance_info_right_grid.attach(label, 0, 2, 1, 1)
        # Label (Power Usage)
        self.power_usage_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.power_usage_label, 1, 2, 1, 1)

        # Label (Driver)
        label = Common.static_information_label(_tr("Driver") + ":")
        performance_info_right_grid.attach(label, 0, 3, 1, 1)
        # Label (Driver)
        self.driver_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.driver_label, 1, 3, 1, 1)

        # Label (Refresh Rate)
        label = Common.static_information_label(_tr("Refresh Rate") + ":")
        performance_info_right_grid.attach(label, 0, 4, 1, 1)
        # Label (Refresh Rate)
        self.refresh_rate_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.refresh_rate_label, 1, 4, 1, 1)

        # Label (Resolution)
        label = Common.static_information_label(_tr("Resolution") + ":")
        performance_info_right_grid.attach(label, 0, 5, 1, 1)
        # Label (Resolution)
        self.resolution_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.resolution_label, 1, 5, 1, 1)


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        # Define initial values
        self.chart_data_history = Config.chart_data_history
        self.gpu_load_list = [0] * self.chart_data_history
        # Currently highest monitor refresh rate is 360. 365 is used in order to get GPU load for AMD GPUs precisely.
        self.amd_gpu_load_list = [0] * 365


        # Get information.
        gpu_list, gpu_device_path_list, gpu_device_sub_path_list, default_gpu = Libsysmon.get_gpu_list_and_boot_vga()
        selected_gpu_number, selected_gpu = Libsysmon.gpu_set_selected_gpu(Config.selected_gpu, gpu_list, default_gpu)
        if_default_gpu = Libsysmon.get_default_gpu(selected_gpu_number, gpu_list, default_gpu)
        gpu_device_model_name, device_vendor_id = Libsysmon.get_device_model_name_vendor_id(selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)
        gpu_driver_name = Libsysmon.get_driver_name(selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)

        self.default_gpu = default_gpu
        self.selected_gpu_number = selected_gpu_number
        self.selected_gpu = selected_gpu
        self.gpu_list = gpu_list
        self.gpu_device_path_list = gpu_device_path_list
        self.gpu_device_sub_path_list = gpu_device_sub_path_list
        self.device_vendor_id = device_vendor_id


        # Set GPU tab label texts by using information get
        self.device_vendor_model_label.set_label(gpu_device_model_name)
        self.device_kernel_name_label.set_label(f'{self.gpu_list[self.selected_gpu_number]}')
        self.boot_vga_label.set_label(if_default_gpu)
        self.driver_label.set_label(gpu_driver_name)

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        default_gpu = self.default_gpu
        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.selected_gpu
        gpu_list = self.gpu_list
        gpu_device_path_list = self.gpu_device_path_list
        gpu_device_sub_path_list = self.gpu_device_sub_path_list
        device_vendor_id = self.device_vendor_id

        # Run "initial_func" if "initial_already_run variable is "0" which means all settings
        # of the application is reset and initial function has to be run in order to avoid errors.
        # This check is required only for GPU tab (not required for other Performance tab sub-tabs).
        if self.initial_already_run == 0:
            self.initial_func()

        # Get information.
        current_resolution, current_refresh_rate = Libsysmon.get_resolution_refresh_rate()
        gpu_pci_address = Libsysmon.get_gpu_pci_address(selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)
        gpu_load, gpu_memory_used, gpu_memory_capacity, gpu_current_frequency, gpu_min_frequency, gpu_max_frequency, gpu_temperature, gpu_power = self.get_gpu_load_memory_frequency_power(gpu_pci_address, device_vendor_id, selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)

        gpu_load = gpu_load.split()[0]
        if gpu_load == "-":
            self.gpu_load_list.append(0)
            gpu_load = "-"
        else:
            self.gpu_load_list.append(float(gpu_load))
            gpu_load = f'{gpu_load} %'
        del self.gpu_load_list[0]

        try:
            gpu_temperature = float(gpu_temperature)
            gpu_temperature = f'{gpu_temperature:.0f} °C'
        except ValueError:
            pass

        self.da_gpu_usage.queue_draw()

        # Run "main_gui_device_selection_list" if selected device list is changed since the last loop.
        gpu_list = self.gpu_list
        try:                                                                                      
            if self.gpu_list_prev != gpu_list:
                MainWindow.main_gui_device_selection_list()
        # Avoid error if this is first loop of the function.
        except AttributeError:
            MainWindow.main_gui_device_selection_list()
        self.gpu_list_prev = list(gpu_list)


        # Set and update GPU tab label texts by using information get
        self.gpu_usage_label.set_label(gpu_load)
        self.video_memory_label.set_label(f'{gpu_memory_used} / {gpu_memory_capacity}')
        self.frequency_label.set_label(gpu_current_frequency)
        self.temperature_label.set_label(gpu_temperature)
        self.min_max_frequency_label.set_label(f'{gpu_min_frequency} - {gpu_max_frequency}')
        self.power_usage_label.set_label(gpu_power)
        self.refresh_rate_label.set_label(current_refresh_rate)
        self.resolution_label.set_label(f'{current_resolution}')


    def get_gpu_load_memory_frequency_power(self, gpu_pci_address, device_vendor_id, selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list):
        """
        Get GPU load, memory, frequencies, power.
        """

        gpu_device_path = gpu_device_path_list[selected_gpu_number]

        environment_type = Libsysmon.get_environment_type()

        # Define initial values for unknown GPU vendors such as vritual devices.
        gpu_load = "-"
        gpu_memory_used = "-"
        gpu_memory_capacity = "-"
        gpu_current_frequency = "-"
        gpu_min_frequency = "-"
        gpu_max_frequency = "-"
        gpu_temperature = "-"
        gpu_power = "-"

        # If selected GPU vendor is Intel
        if device_vendor_id == "v00008086":
            gpu_load_memory_frequency_power_dict = Libsysmon.get_gpu_load_memory_frequency_power_intel(gpu_device_path)

        # If selected GPU vendor is AMD
        if device_vendor_id in ["v00001022", "v00001002"]:
            gpu_load_memory_frequency_power_dict = Libsysmon.get_gpu_load_memory_frequency_power_amd(gpu_device_path)

            # Get GPU load average. There is no "%" character in "gpu_busy_percent" file. This file contains GPU load for a very small time.
            try:
                self.gpu_load_amd_func()
                gpu_load = f'{(sum(self.amd_gpu_load_list) / len(self.amd_gpu_load_list)):.0f} %'
            except Exception:
                gpu_load = "-"

            # Update the GPU load value. Because it is not get in "get_gpu_load_memory_frequency_power_amd" function.
            gpu_load_memory_frequency_power_dict["gpu_load"] = gpu_load

        # If selected GPU vendor is Broadcom (for RB-Pi ARM devices).
        if device_vendor_id in ["Brcm"]:
            gpu_load_memory_frequency_power_dict = Libsysmon.get_gpu_load_memory_frequency_power_broadcom_arm()

        # If selected GPU vendor is NVIDIA and selected GPU is used on a PCI used system.
        if device_vendor_id == "v000010DE" and gpu_device_path.startswith("/sys/class/drm/") == True:
            # Try to get GPU usage information in a separate thread in order to prevent this function from blocking
            # the main thread and GUI for a very small time which stops the GUI for a very small time.
            gpu_tool_output = "-"
            Thread(target=self.gpu_load_nvidia_func, daemon=True).start()

            try:
                gpu_tool_output = self.gpu_tool_output
            # Prevent error if thread is not finished before using the output variable "gpu_tool_output".
            except AttributeError:
                pass
            gpu_load_memory_frequency_power_dict = Libsysmon.process_gpu_tool_output_nvidia(gpu_pci_address, gpu_tool_output)

        # If selected GPU vendor is NVIDIA and selected GPU is used on an ARM system.
        if device_vendor_id in ["v000010DE", "Nvidia"] and gpu_device_path.startswith("/sys/devices/") == True:
            gpu_load_memory_frequency_power_dict = Libsysmon.get_gpu_load_memory_frequency_power_nvidia_arm(gpu_device_path)

        if device_vendor_id in ["v00008086", "v00001022", "v00001002", "Brcm", "v000010DE", "Nvidia"]:
            gpu_load = gpu_load_memory_frequency_power_dict["gpu_load"]
            gpu_memory_used = gpu_load_memory_frequency_power_dict["gpu_memory_used"]
            gpu_memory_capacity = gpu_load_memory_frequency_power_dict["gpu_memory_capacity"]
            gpu_current_frequency = gpu_load_memory_frequency_power_dict["gpu_current_frequency"]
            gpu_min_frequency = gpu_load_memory_frequency_power_dict["gpu_min_frequency"]
            gpu_max_frequency = gpu_load_memory_frequency_power_dict["gpu_max_frequency"]
            gpu_temperature = gpu_load_memory_frequency_power_dict["gpu_temperature"]
            gpu_power = gpu_load_memory_frequency_power_dict["gpu_power"]

        return gpu_load, gpu_memory_used, gpu_memory_capacity, gpu_current_frequency, gpu_min_frequency, gpu_max_frequency, gpu_temperature, gpu_power


    def gpu_load_nvidia_func(self):
        """
        Get GPU load average for NVIDIA (PCI) GPUs.
        """

        command_list = ["nvidia-smi", "--query-gpu=gpu_name,gpu_bus_id,driver_version,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used,temperature.gpu,clocks.current.graphics,clocks.max.graphics,power.draw", "--format=csv"]
        if Libsysmon.get_environment_type() == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list

        try:
            self.gpu_tool_output = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
        # Prevent errors because nvidia-smi may not be installed on some devices (such as N.Switch with NVIDIA Tegra GPU).
        except FileNotFoundError:
            pass


    def gpu_load_amd_func(self, *args):
        """
        Get GPU load average for AMD GPUs.
        """

        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.gpu_list[selected_gpu_number]
        gpu_device_path = self.gpu_device_path_list[selected_gpu_number]
        gpu_device_sub_path = self.gpu_device_sub_path_list[selected_gpu_number]

        # Destroy GLib source for preventing it repeating the function.
        try:
            self.gpu_glib_source.destroy()
        # Prevent errors if this is first run of the function.
        except AttributeError:
            pass
        self.gpu_glib_source = GLib.timeout_source_new(1000 / 365)

        # Read file to get GPU load information. This information is calculated for a very small
        # time (screen refresh rate or content (game, etc.) refresh rate?) and directly plotting this data gives spikes.
        with open(gpu_device_path + "device/gpu_busy_percent") as reader:
            gpu_load = reader.read().strip()

        # Add GPU load data into a list in order to calculate average of the list.
        self.amd_gpu_load_list.append(float(gpu_load))
        del self.amd_gpu_load_list[0]

        # Prevent running the function again if tab is GPU switched off.
        if Config.current_main_tab != 0 or Config.performance_tab_current_sub_tab != 5:
            return

        self.gpu_glib_source.set_callback(self.gpu_load_amd_func)
        # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed.
        # A function may be attached to the MainContext multiple times.
        self.gpu_glib_source.attach(GLib.MainContext.default())


Gpu = Gpu()


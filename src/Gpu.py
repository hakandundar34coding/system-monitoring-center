import tkinter as tk
from tkinter import ttk

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

        self.tab_frame = ttk.Frame(MainWindow.gpu_tab_main_frame)
        self.tab_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.tab_frame.columnconfigure(0, weight=1)
        self.tab_frame.rowconfigure((1, 2), weight=1, uniform="equal")

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

        # Label (GPU)
        label = Common.tab_title_label(frame, _tr("GPU"))

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
        self.da_upper_left_label = Common.da_upper_lower_label(frame, _tr("GPU Usage"))
        self.da_upper_left_label.grid(row=0, column=0, sticky="w")

        # Label (drawingarea upper-right)
        label = Common.da_upper_lower_label(frame, "100%")
        label.grid(row=0, column=1, sticky="e")

        # Label (for showing graphics)
        self.da_gpu_usage = Common.drawingarea(frame, "da_gpu_usage")
        self.da_gpu_usage.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label(frame, "0")
        label.grid(row=2, column=1, sticky="e")


        # Frame (drawingarea)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=2, column=0, sticky="nsew", padx=0, pady=(0, 10))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Label (drawingarea upper-left)
        self.da_upper_left_label = Common.da_upper_lower_label(frame, _tr("GPU Memory"))
        self.da_upper_left_label.grid(row=0, column=0, sticky="w")

        # Label (drawingarea upper-right)
        label = Common.da_upper_lower_label(frame, "100%")
        label.grid(row=0, column=1, sticky="e")

        # Label (for showing graphics)
        self.da_gpu_memory_usage = Common.drawingarea(frame, "da_gpu_memory_usage")
        self.da_gpu_memory_usage.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label(frame, "0")
        label.grid(row=2, column=1, sticky="e")


    def information_frame(self):
        """
        Generate performance/information labels.
        """

        # Frame (performance/information labels)
        performance_info_grid = ttk.Frame(self.tab_frame)
        performance_info_grid.grid(row=3, column=0, sticky="nsew", padx=0, pady=0)
        performance_info_grid.columnconfigure((0, 1), weight=1, uniform="equal")
        performance_info_grid.rowconfigure((0, 1), weight=1, uniform="equal")
        #performance_info_grid.rowconfigure(0, weight=1)

        # Styled information widgets (GPU Usage and Video Memory)
        # Frame (GPU Usage and Video Memory)
        _frame, self.gpu_usage_label, self.video_memory_label = Common.styled_information_scrolledwindow(performance_info_grid, _tr("GPU Usage"), None, _tr("Video Memory"), None)
        _frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=(0, 5))

        # Styled information widgets (Frequency and Temperature)
        # Frame (Frequency and Temperature)
        _frame, self.frequency_label, self.temperature_label = Common.styled_information_scrolledwindow(performance_info_grid, _tr("Frequency"), None, _tr("Temperature"), None)
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

        # Label (Memory Frequency)
        label = Common.static_information_label(performance_info_right_frame, _tr("Memory Frequency") + ":")
        label.grid(row=1, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Memory Frequency)
        self.memory_frequency_label = Common.dynamic_information_label(performance_info_right_frame)
        self.memory_frequency_label.grid(row=1, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Power Usage)
        label = Common.static_information_label(performance_info_right_frame, _tr("Power Usage") + ":")
        label.grid(row=2, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Power Usage)
        self.power_usage_label = Common.dynamic_information_label(performance_info_right_frame)
        self.power_usage_label.grid(row=2, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Boot VGA)
        label = Common.static_information_label(performance_info_right_frame, _tr("Boot VGA") + ":")
        label.grid(row=3, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Driver)
        self.boot_vga_label = Common.dynamic_information_label(performance_info_right_frame)
        self.boot_vga_label.grid(row=3, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Driver)
        label = Common.static_information_label(performance_info_right_frame, _tr("Driver") + ":")
        label.grid(row=4, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Driver)
        self.driver_label = Common.dynamic_information_label(performance_info_right_frame)
        self.driver_label.grid(row=4, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Details...)
        label = Common.static_information_label(performance_info_right_frame, _tr("Details") + ":")
        label.grid(row=5, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Show...)
        self.details_label = Common.clickable_label(performance_info_right_frame, self.on_details_label_released)
        self.details_label.grid(row=5, column=1, sticky="w", padx=(4, 0), pady=(0, 4))


    def on_details_label_released(self, event):
        """
        Show GPU details window.
        """

        widget = event.widget

        self.gpu_details_window_gui()
        self.gpu_details_info_get()
        self.gpu_details_update()


    def gpu_details_window_gui(self):
        """
        GPU details window GUI.
        """

        # Window
        self.gpu_details_window, frame = Common.window(MainWindow.main_window, _tr("GPU"))

        # Information labels
        # Label (Vendor - Model)
        label = Common.static_information_label(frame, _tr("Vendor - Model"))
        label.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Vendor - Model)
        label = Common.static_information_label(frame, ":")
        label.grid(row=0, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Vendor - Model)
        self.gpu_details_vendor_model_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_vendor_model_label.grid(row=0, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (GPU)
        label = Common.static_information_label(frame, _tr("GPU"))
        label.grid(row=1, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (GPU)
        label = Common.static_information_label(frame, ":")
        label.grid(row=1, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (GPU)
        self.gpu_details_gpu_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_gpu_label.grid(row=1, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (PCIe Address)
        label = Common.static_information_label(frame, _tr("PCIe Address"))
        label.grid(row=2, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (PCIe Address)
        label = Common.static_information_label(frame, ":")
        label.grid(row=2, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (PCIe Address)
        self.gpu_details_pcie_address_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_pcie_address_label.grid(row=2, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (GPU Interface)
        label = Common.static_information_label(frame, _tr("GPU Interface"))
        label.grid(row=3, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (GPU Interface)
        label = Common.static_information_label(frame, ":")
        label.grid(row=3, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (GPU Interface)
        self.gpu_details_gpu_interface_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_gpu_interface_label.grid(row=3, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Connection Speed)
        label = Common.static_information_label(frame, _tr("Connection Speed"))
        label.grid(row=4, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Connection Speed)
        label = Common.static_information_label(frame, ":")
        label.grid(row=4, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Connection Speed)
        self.gpu_details_link_speed_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_link_speed_label.grid(row=4, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (GPU Usage)
        label = Common.static_information_label(frame, _tr("GPU Usage"))
        label.grid(row=5, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (GPU Usage)
        label = Common.static_information_label(frame, ":")
        label.grid(row=5, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (GPU Usage)
        self.gpu_details_gpu_usage_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_gpu_usage_label.grid(row=5, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (GPU Memory)
        label = Common.static_information_label(frame, _tr("GPU Memory"))
        label.grid(row=6, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (GPU Memory)
        label = Common.static_information_label(frame, ":")
        label.grid(row=6, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (GPU Memory)
        self.gpu_details_gpu_memory_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_gpu_memory_label.grid(row=6, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Frequency)
        label = Common.static_information_label(frame, _tr("Frequency"))
        label.grid(row=7, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Frequency)
        label = Common.static_information_label(frame, ":")
        label.grid(row=7, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Frequency)
        self.gpu_details_frequency_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_frequency_label.grid(row=7, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Min-Max Frequency)
        label = Common.static_information_label(frame, _tr("Min-Max Frequency"))
        label.grid(row=8, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Min-Max Frequency)
        label = Common.static_information_label(frame, ":")
        label.grid(row=8, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Min-Max Frequency)
        self.gpu_details_min_max_frequency_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_min_max_frequency_label.grid(row=8, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Memory Frequency)
        label = Common.static_information_label(frame, _tr("Memory Frequency"))
        label.grid(row=9, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Memory Frequency)
        label = Common.static_information_label(frame, ":")
        label.grid(row=9, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Memory Frequency)
        self.gpu_details_memory_frequency_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_memory_frequency_label.grid(row=9, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Temperature)
        label = Common.static_information_label(frame, _tr("Temperature"))
        label.grid(row=10, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Temperature)
        label = Common.static_information_label(frame, ":")
        label.grid(row=10, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Temperature)
        self.gpu_details_temperature_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_temperature_label.grid(row=10, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Power Usage)
        label = Common.static_information_label(frame, _tr("Power Usage"))
        label.grid(row=11, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Power Usage)
        label = Common.static_information_label(frame, ":")
        label.grid(row=11, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Power Usage)
        self.gpu_details_power_usage_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_power_usage_label.grid(row=11, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Boot VGA)
        label = Common.static_information_label(frame, _tr("Boot VGA"))
        label.grid(row=12, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Boot VGA)
        label = Common.static_information_label(frame, ":")
        label.grid(row=12, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Boot VGA)
        self.gpu_details_boot_vga_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_boot_vga_label.grid(row=12, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Driver)
        label = Common.static_information_label(frame, _tr("Driver"))
        label.grid(row=13, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Driver)
        label = Common.static_information_label(frame, ":")
        label.grid(row=13, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Driver)
        self.gpu_details_driver_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_driver_label.grid(row=13, column=2, sticky="w", padx=0, pady=(0, 4))

        # Label (Connections)
        label = Common.static_information_label(frame, _tr("Connections"))
        label.grid(row=14, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Connections)
        label = Common.static_information_label(frame, ":")
        label.grid(row=14, column=1, sticky="w", padx=4, pady=(0, 4))
        # Label (Connections)
        self.gpu_details_connections_label = Common.dynamic_information_label_wrap(frame)
        self.gpu_details_connections_label.grid(row=14, column=2, sticky="w", padx=0, pady=(0, 4))


    def gpu_details_info_get(self):
        """
        Get GPU details information.
        """

        # Get information
        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.selected_gpu
        gpu_list = self.gpu_list
        gpu_device_path_list = self.gpu_device_path_list
        gpu_device_sub_path_list = self.gpu_device_sub_path_list
        gpu_device_path = gpu_device_path_list[selected_gpu_number]

        gpu_pci_address = Libsysmon.get_gpu_pci_address(selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)
        gpu_current_link_speed = Libsysmon.get_gpu_current_link_speed(gpu_device_path)
        gpu_max_link_speed = Libsysmon.get_gpu_max_link_speed(gpu_device_path)
        gpu_interface = Libsysmon.get_gpu_interface(gpu_device_path)
        gpu_connections = Libsysmon.get_gpu_connections(gpu_device_path, selected_gpu)

        # Set GPU Details window title
        self.gpu_details_window.title(_tr("GPU") + ": " + selected_gpu)

        # Set label text by using GPU data
        self.gpu_details_vendor_model_label.config(text=self.gpu_information_share_dict["gpu_device_model_name"])
        self.gpu_details_gpu_label.config(text=selected_gpu)
        self.gpu_details_pcie_address_label.config(text=gpu_pci_address)
        self.gpu_details_gpu_interface_label.config(text=gpu_interface)
        self.gpu_details_link_speed_label.config(text=gpu_current_link_speed + " / " + gpu_max_link_speed)
        self.gpu_details_gpu_usage_label.config(text=self.gpu_information_share_dict2["gpu_load"])
        self.gpu_details_gpu_memory_label.config(text=self.gpu_information_share_dict2["gpu_memory_used"] + " / " + self.gpu_information_share_dict2["gpu_memory_capacity"])
        self.gpu_details_frequency_label.config(text=self.gpu_information_share_dict2["gpu_current_frequency"])
        self.gpu_details_min_max_frequency_label.config(text=self.gpu_information_share_dict2["gpu_min_frequency"] + " - " + self.gpu_information_share_dict2["gpu_max_frequency"])
        self.gpu_details_memory_frequency_label.config(text=self.gpu_information_share_dict2["gpu_memory_current_frequency"] + " / " + self.gpu_information_share_dict2["gpu_memory_max_frequency"])
        self.gpu_details_temperature_label.config(text=self.gpu_information_share_dict2["gpu_temperature"])
        self.gpu_details_power_usage_label.config(text=self.gpu_information_share_dict2["gpu_power_current"] + " / " + self.gpu_information_share_dict2["gpu_power_max"])
        self.gpu_details_boot_vga_label.config(text=self.gpu_information_share_dict["if_default_gpu"])
        self.gpu_details_driver_label.config(text=self.gpu_information_share_dict["gpu_driver_name"])
        self.gpu_details_connections_label.config(text=gpu_connections)


    def gpu_details_update(self, *args):
        """
        Update GPU information on the GPU details window.
        """

        if self.gpu_details_window.state() == "normal":
            self.gpu_details_info_get()
            self.gpu_details_window.after(int(Config.update_interval*1000), self.gpu_details_update)


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        # Define initial values
        self.chart_data_history = Config.chart_data_history
        self.gpu_load_list = [0] * self.chart_data_history
        self.gpu_memory_list = [0] * self.chart_data_history

        # Get information
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

        self.gpu_information_share_dict = {
                                           "gpu_device_model_name" : gpu_device_model_name,
                                           "if_default_gpu" : if_default_gpu,
                                           "gpu_driver_name" : gpu_driver_name,
                                           }

        # Set GPU tab label texts by using information get
        self.device_vendor_model_label.config(text=gpu_device_model_name)
        self.device_kernel_name_label.config(text=f'{self.gpu_list[self.selected_gpu_number]}')
        self.boot_vga_label.config(text=if_default_gpu)
        self.driver_label.config(text=gpu_driver_name)

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
        gpu_pci_address = Libsysmon.get_gpu_pci_address(selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)
        gpu_load_memory_frequency_power_dict = Libsysmon.get_gpu_load_memory_frequency_power(gpu_pci_address, device_vendor_id, selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)

        gpu_load = gpu_load_memory_frequency_power_dict["gpu_load"]
        gpu_memory_used = gpu_load_memory_frequency_power_dict["gpu_memory_used"]
        gpu_memory_capacity = gpu_load_memory_frequency_power_dict["gpu_memory_capacity"]
        gpu_current_frequency = gpu_load_memory_frequency_power_dict["gpu_current_frequency"]
        gpu_min_frequency = gpu_load_memory_frequency_power_dict["gpu_min_frequency"]
        gpu_max_frequency = gpu_load_memory_frequency_power_dict["gpu_max_frequency"]
        gpu_memory_current_frequency = gpu_load_memory_frequency_power_dict["gpu_memory_current_frequency"]
        gpu_memory_min_frequency = gpu_load_memory_frequency_power_dict["gpu_memory_min_frequency"]
        gpu_memory_max_frequency = gpu_load_memory_frequency_power_dict["gpu_memory_max_frequency"]
        gpu_temperature = gpu_load_memory_frequency_power_dict["gpu_temperature"]
        gpu_power_current = gpu_load_memory_frequency_power_dict["gpu_power_current"]
        gpu_power_max = gpu_load_memory_frequency_power_dict["gpu_power_max"]

        gpu_load = gpu_load.split()[0]
        if gpu_load == "-":
            self.gpu_load_list.append(0)
        else:
            self.gpu_load_list.append(float(gpu_load))
            gpu_load = f'{gpu_load} %'
        del self.gpu_load_list[0]

        gpu_memory_usage_percentage = Libsysmon.get_gpu_memory_usage_percentage(gpu_memory_used, gpu_memory_capacity)
        self.gpu_memory_list.append(gpu_memory_usage_percentage)
        del self.gpu_memory_list[0]

        try:
            gpu_temperature = float(gpu_temperature)
            gpu_temperature = f'{gpu_temperature:.0f} °C'
        except ValueError:
            pass

        Performance.performance_line_charts_draw(self.da_gpu_usage, "da_gpu_usage")
        Performance.performance_line_charts_draw(self.da_gpu_memory_usage, "da_gpu_memory_usage")

        self.gpu_information_share_dict2 = dict(gpu_load_memory_frequency_power_dict)

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
        self.gpu_usage_label.config(text=gpu_load)
        self.video_memory_label.config(text=f'{gpu_memory_used} / {gpu_memory_capacity}')
        self.frequency_label.config(text=gpu_current_frequency)
        self.temperature_label.config(text=gpu_temperature)
        self.min_max_frequency_label.config(text=f'{gpu_min_frequency} - {gpu_max_frequency}')
        self.power_usage_label.config(text=gpu_power_current + " / " + gpu_power_max)
        #self.memory_frequency_label.config(text=f'{gpu_memory_current_frequency} / {gpu_memory_max_frequency}')


Gpu = Gpu()


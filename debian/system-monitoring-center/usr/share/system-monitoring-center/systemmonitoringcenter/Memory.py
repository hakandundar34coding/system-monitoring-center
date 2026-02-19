import tkinter as tk
from tkinter import ttk

import os
import subprocess

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class Memory:

    def __init__(self):

        self.name = "Memory"

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_frame = ttk.Frame(MainWindow.memory_tab_main_frame)
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

        # Label (Memory)
        label = Common.tab_title_label(frame, _tr("Memory"))

        # Label (device vendor-model label)
        self.device_vendor_model_label = Common.device_vendor_model_label(frame)

        # Label (device kernel name)
        self.device_kernel_name_label = Common.device_kernel_name_label(frame)


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
        self.da_upper_left_label = Common.da_upper_lower_label(frame, _tr("RAM Usage"))
        self.da_upper_left_label.grid(row=0, column=0, sticky="w")

        # Label (drawingarea upper-right)
        label = Common.da_upper_lower_label(frame, "100%")
        label.grid(row=0, column=1, sticky="e")

        # Label (for showing graphics)
        self.da_memory_usage = Common.drawingarea(frame, "da_memory_usage")
        self.da_memory_usage.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

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
        #performance_info_grid.rowconfigure((0, 1, 2), weight=1, uniform="equal")
        #performance_info_grid.rowconfigure(0, weight=1)

        # Label - Title (RAM)
        label = Common.bold_label(performance_info_grid, _tr("RAM"))
        label.grid(row=0, column=0, sticky="w", padx=(0, 15), pady=5)

        # Styled information widgets (Used and Available)
        # Frame (Used and Available)
        _frame, self.ram_used_label, self.ram_available_label = Common.styled_information_scrolledwindow(performance_info_grid, _tr("Used"), None, _tr("Available"), None)
        _frame.grid(row=1, column=0, sticky="nsew", padx=(0, 15), pady=(0, 5))

        # Frame (lower left information labels)
        frame = ttk.Frame(performance_info_grid)
        frame.grid(row=2, column=0, sticky="nsew", padx=(0, 15), pady=0)
        frame.columnconfigure((0, 1), weight=1, uniform="equal")
        frame.rowconfigure((0, 1, 2), weight=1, uniform="equal")

        # Label (Capacity)
        label = Common.static_information_label(frame, _tr("Capacity") + ":")
        label.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Capacity)
        self.ram_capacity_label = Common.dynamic_information_label(frame)
        self.ram_capacity_label.grid(row=0, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Free)
        label = Common.static_information_label(frame, _tr("Free") + ":")
        label.grid(row=1, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Free)
        self.ram_free_label = Common.dynamic_information_label(frame)
        self.ram_free_label.grid(row=1, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Cached)
        label = Common.static_information_label(frame, _tr("Cached") + ":")
        label.grid(row=2, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Cached)
        self.ram_cached_label = Common.dynamic_information_label(frame)
        self.ram_cached_label.grid(row=2, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Hardware)
        label = Common.static_information_label(frame, _tr("Hardware") + ":")
        label.grid(row=3, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Show...)
        self.ram_hardware_label = Common.clickable_label(frame, self.on_details_label_released)
        self.ram_hardware_label.grid(row=3, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label - Title (Swap)
        label = Common.bold_label(performance_info_grid, _tr("Swap"))
        label.grid(row=0, column=1, sticky="w", padx=(15, 0), pady=5)

        # Styled information widgets (Used and Free)
        # Frame (Used and Free)
        _frame, self.swap_used_label, self.swap_free_label = Common.styled_information_scrolledwindow(performance_info_grid, _tr("Used"), None, _tr("Free"), None)
        _frame.grid(row=1, column=1, sticky="nsew", padx=(15, 0), pady=(0, 5))

        # Frame (lower right information labels)
        frame = ttk.Frame(performance_info_grid)
        frame.grid(row=2, column=1, sticky="nsew", padx=(15, 0), pady=0)
        frame.columnconfigure((0, 1), weight=1, uniform="equal")
        frame.rowconfigure((0, 1, 2), weight=1, uniform="equal")

        # Label (Used (swap percent))
        label = Common.static_information_label(frame, _tr("Used") + ":")
        label.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label and DrawingArea (Used (swap percent))
        frame_label_and_da = ttk.Frame(frame)
        frame_label_and_da.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        # Moving widgets problem is fixed by using the following configurations.
        frame_label_and_da.columnconfigure((0,1), weight=2, uniform="equal")
        frame_label_and_da.columnconfigure(1, weight=1)
        # DrawingArea (Used (swap percent))
        self.da_swap_usage = ttk.Label(frame_label_and_da)
        self.da_swap_usage.grid(row=0, column=0, sticky="nsew", padx=0, pady=2)
        # Label (Used (swap percent))
        self.swap_used_percent_label = Common.dynamic_information_label(frame_label_and_da)
        self.swap_used_percent_label.grid(row=0, column=1, sticky="e", padx=(4, 0), pady=(0, 4))

        # Label (Capacity (swap))
        label = Common.static_information_label(frame, _tr("Capacity") + ":")
        label.grid(row=1, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Capacity (swap))
        self.swap_capacity_label = Common.dynamic_information_label(frame)
        self.swap_capacity_label.grid(row=1, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Cached (swap))
        label = Common.static_information_label(frame, _tr("Cached") + ":")
        label.grid(row=2, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Cached (swap))
        self.swap_cached_label = Common.dynamic_information_label(frame)
        self.swap_cached_label.grid(row=2, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Details (swap))
        label = Common.static_information_label(frame, _tr("Details") + ":")
        label.grid(row=3, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Show... (swap))
        self.swap_details_label = Common.clickable_label(frame, self.on_details_label_released)
        self.swap_details_label.grid(row=3, column=1, sticky="w", padx=(4, 0), pady=(0, 4))


    def on_details_label_released(self, event):
        """
        Show RAM hardware window or swap details window.
        """

        widget = event.widget

        # Show RAM hardware window
        if widget == self.ram_hardware_label:
            memory_ram_hardware_info = Libsysmon.get_ram_hardware_info()
            self.ram_hardware_window_gui()
            self.ram_hardware_win_label.configure(state="normal")
            self.ram_hardware_win_label.delete(1.0, "end")
            self.ram_hardware_win_label.insert(1.0, memory_ram_hardware_info)
            self.ram_hardware_win_label.configure(state="disabled")

        # Show swap details window
        if widget == self.swap_details_label:
            memory_swap_details_info = Libsysmon.get_swap_details_info(Config.performance_memory_data_precision, Config.performance_memory_data_unit)
            self.swap_details_window_gui()
            self.swap_details_win_label.configure(state="normal")
            #self.swap_details_info_get()
            self.swap_details_update()


    def ram_hardware_window_gui(self):
        """
        RAM hardware window GUI.
        """

        # Window
        self.ram_hardware_window, frame = Common.window(MainWindow.main_window, _tr("Physical RAM"))

        # Text
        self.ram_hardware_win_label = tk.Text(frame, font=Common.font_system)
        self.ram_hardware_win_label.delete(1.0, "end")
        self.ram_hardware_win_label.insert(1.0, "--")
        self.ram_hardware_win_label.configure(relief="flat")
        self.ram_hardware_win_label.configure(state="disabled")
        self.ram_hardware_win_label.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        # Scrollbar (Text)
        scrollbar_vertical = ttk.Scrollbar(frame, orient="vertical", command=self.ram_hardware_win_label.yview)
        scrollbar_vertical.grid(row=0, column=1, sticky="ns", padx=0, pady=0)
        scrollbar_horizontal = ttk.Scrollbar(frame, orient="horizontal", command=self.ram_hardware_win_label.xview)
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        self.ram_hardware_win_label['yscrollcommand'] = scrollbar_vertical.set
        self.ram_hardware_win_label['xscrollcommand'] = scrollbar_horizontal.set


    def swap_details_window_gui(self):
        """
        Swap details window GUI.
        """

        # Window
        self.swap_details_window, frame = Common.window(MainWindow.main_window, _tr("Swap Memory"))

        # Text
        self.swap_details_win_label = tk.Text(frame, font=Common.font_system)
        self.swap_details_win_label.delete(1.0, "end")
        self.swap_details_win_label.insert(1.0, "--")
        self.swap_details_win_label.configure(relief="flat")
        self.swap_details_win_label.configure(state="disabled")
        self.swap_details_win_label.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        # Scrollbar (Text)
        scrollbar_vertical = ttk.Scrollbar(frame, orient="vertical", command=self.swap_details_win_label.yview)
        scrollbar_vertical.grid(row=0, column=1, sticky="ns", padx=0, pady=0)
        scrollbar_horizontal = ttk.Scrollbar(frame, orient="horizontal", command=self.swap_details_win_label.xview)
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
        self.swap_details_win_label['yscrollcommand'] = scrollbar_vertical.set
        self.swap_details_win_label['xscrollcommand'] = scrollbar_horizontal.set


    def swap_details_update(self, *args):
        """
        Update swap memory information on the swap details window.
        """

        memory_swap_details_info = Libsysmon.get_swap_details_info(Config.performance_memory_data_precision, Config.performance_memory_data_unit)
        if memory_swap_details_info.strip() == "":
            memory_swap_details_info = "-"

        self.swap_details_win_label.configure(state="normal")
        self.swap_details_win_label.delete(1.0, "end")
        self.swap_details_win_label.insert(1.0, memory_swap_details_info)
        self.swap_details_win_label.configure(state="disabled")

        self.swap_details_window.after(int(Config.update_interval*1000), self.swap_details_update)


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        # List for language translation
        memory_swap_details_text_list = [_tr("Partition"), _tr("File")]

        total_physical_ram = Libsysmon.get_physical_ram()

        # Set Memory tab label texts by using information get
        if total_physical_ram != "-":
            self.device_vendor_model_label.config(text=_tr("Physical RAM") + ": " + str(Libsysmon.data_unit_converter("data", "none", total_physical_ram, 0, 1)))
        else:
            self.device_vendor_model_label.config(text=_tr("RAM") + " - " + _tr("Capacity") + ": " + str(Libsysmon.data_unit_converter("data", "none", ram_total, 0, 1)))

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        memory_info = Libsysmon.get_memory_info()

        ram_used = memory_info["ram_used"]
        ram_usage_percent = Performance.ram_usage_percent
        ram_available = memory_info["ram_available"]
        ram_free = memory_info["ram_free"]
        ram_total = memory_info["ram_total"]
        ram_cached = memory_info["ram_cached"]

        self.swap_usage_percent = Performance.swap_usage_percent
        swap_used = memory_info["swap_used"]
        swap_free = memory_info["swap_free"]
        swap_total = memory_info["swap_total"]
        swap_cached = memory_info["swap_cached"]


        performance_memory_data_precision = Config.performance_memory_data_precision
        performance_memory_data_unit = Config.performance_memory_data_unit

        Performance.performance_line_charts_draw(self.da_memory_usage, "da_memory_usage")
        Performance.performance_bar_charts_draw(self.da_swap_usage, "da_swap_usage")


        # Set and update Memory tab label texts by using information get
        self.device_kernel_name_label.config(text=_tr("Swap Memory") + ": " + str(Libsysmon.data_unit_converter("data", "none", swap_total, 0, 1)))
        self.ram_used_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", ram_used, performance_memory_data_unit, performance_memory_data_precision)}  ( {ram_usage_percent[-1]:.0f}% )')
        self.ram_available_label.config(text=Libsysmon.data_unit_converter("data", "none", ram_available, performance_memory_data_unit, performance_memory_data_precision))
        self.ram_capacity_label.config(text=Libsysmon.data_unit_converter("data", "none", ram_total, performance_memory_data_unit, performance_memory_data_precision))
        self.ram_free_label.config(text=Libsysmon.data_unit_converter("data", "none", ram_free, performance_memory_data_unit, performance_memory_data_precision))
        self.ram_cached_label.config(text=Libsysmon.data_unit_converter("data", "none", ram_cached, performance_memory_data_unit, performance_memory_data_precision))
        self.swap_used_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", swap_used, performance_memory_data_unit, performance_memory_data_precision)}  ( {self.swap_usage_percent[-1]:.0f}% )')
        self.swap_used_percent_label.config(text=f'{self.swap_usage_percent[-1]:.0f}%')
        self.swap_free_label.config(text=Libsysmon.data_unit_converter("data", "none", swap_free, performance_memory_data_unit, performance_memory_data_precision))
        self.swap_capacity_label.config(text=Libsysmon.data_unit_converter("data", "none", swap_total, performance_memory_data_unit, performance_memory_data_precision))
        self.swap_cached_label.config(text=Libsysmon.data_unit_converter("data", "none", swap_cached, performance_memory_data_unit, performance_memory_data_precision))


Memory = Memory()


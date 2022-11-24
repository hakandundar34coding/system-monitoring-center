#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, Pango

import os
import platform

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from MainWindow import MainWindow


class Cpu:

    def __init__(self):

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        # Grid (tab)
        self.tab_grid = Gtk.Grid()
        self.tab_grid.set_row_spacing(10)
        self.tab_grid.set_margin_top(2)
        self.tab_grid.set_margin_bottom(2)
        self.tab_grid.set_margin_start(2)
        self.tab_grid.set_margin_end(2)

        # Bold label atributes
        self.attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold.insert(attribute)

        self.tab_title_grid()

        self.da_grid()

        self.information_grid()

        self.connect_signals()


    def tab_title_grid(self):
        """
        Generate tab name, device name labels.
        """

        # Grid (tab title)
        grid = Gtk.Grid()
        self.tab_grid.attach(grid, 0, 0, 1, 1)

        # Bold and 2x label atributes
        attribute_list_bold_2x = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        attribute_list_bold_2x.insert(attribute)
        attribute = Pango.attr_scale_new(2.0)
        attribute_list_bold_2x.insert(attribute)

        # Label (CPU)
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(60)
        label.set_attributes(attribute_list_bold_2x)
        label.set_label(_tr("CPU"))
        grid.attach(label, 0, 0, 1, 2)

        # Label (device vendor-model label)
        self.device_vendor_model_label = Gtk.Label()
        self.device_vendor_model_label.set_halign(Gtk.Align.START)
        self.device_vendor_model_label.set_selectable(True)
        self.device_vendor_model_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.device_vendor_model_label.set_attributes(self.attribute_list_bold)
        self.device_vendor_model_label.set_label("--")
        self.device_vendor_model_label.set_tooltip_text(_tr("Vendor-Model"))
        grid.attach(self.device_vendor_model_label, 1, 0, 1, 1)

        # Label (device kernel name)
        self.device_kernel_name_label = Gtk.Label()
        self.device_kernel_name_label.set_halign(Gtk.Align.START)
        self.device_kernel_name_label.set_selectable(True)
        self.device_kernel_name_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.device_kernel_name_label.set_label("--")
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
        self.da_upper_left_label = Gtk.Label()
        self.da_upper_left_label.set_halign(Gtk.Align.START)
        self.da_upper_left_label.set_label(_tr("CPU Usage (Average)"))
        grid.attach(self.da_upper_left_label, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        label = Gtk.Label()
        label.set_halign(Gtk.Align.END)
        label.set_label("100%")
        grid.attach(label, 1, 0, 1, 1)

        # DrawingArea (CPU usage)
        self.da_cpu_usage = Gtk.DrawingArea()
        self.da_cpu_usage.set_hexpand(True)
        self.da_cpu_usage.set_vexpand(True)
        grid.attach(self.da_cpu_usage, 0, 2, 2, 1)

        # Label (drawingarea lower-right)
        label = Gtk.Label()
        label.set_halign(Gtk.Align.END)
        label.set_label("0")
        grid.attach(label, 0, 3, 2, 1)


    def information_grid(self):
        """
        Generate performance/information labels.
        """

        # Grid (performance/information labels)
        performance_info_grid = Gtk.Grid()
        performance_info_grid.set_column_homogeneous(True)
        performance_info_grid.set_row_homogeneous(True)
        performance_info_grid.set_column_spacing(12)
        performance_info_grid.set_row_spacing(10)
        self.tab_grid.attach(performance_info_grid, 0, 2, 1, 1)

        # Define style provider for scrolledwindow for border radius.
        css = b"scrolledwindow {border-radius: 8px 8px 8px 8px;}"
        style_provider_scrolledwindow = Gtk.CssProvider()
        style_provider_scrolledwindow.load_from_data(css)

        # Add separators for showing lines with contrast colors between some the performance data and set color of the separators.
        css = b"separator {background: rgba(50%,50%,50%,0.6);}"
        style_provider_separator = Gtk.CssProvider()
        style_provider_separator.load_from_data(css)

        # Styled information widgets (Average Usage and Frequency)
        # ScrolledWindow (Average Usage and Frequency)
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_has_frame(True)
        scrolledwindow.get_style_context().add_provider(style_provider_scrolledwindow, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        performance_info_grid.attach(scrolledwindow, 0, 0, 1, 1)
        # Grid (Average Usage and Frequency)
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(3)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)
        grid.set_margin_start(5)
        grid.set_margin_end(5)
        grid.set_valign(Gtk.Align.CENTER)
        scrolledwindow.set_child(grid)
        # Label (Average Usage)
        label = Gtk.Label()
        label.set_label(_tr("Average Usage"))
        label.set_tooltip_text(_tr("Average CPU usage of all cores"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Label (Frequency)
        label = Gtk.Label()
        label.set_label(_tr("Frequency"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 1, 0, 1, 1)
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_halign(Gtk.Align.CENTER)
        separator.set_valign(Gtk.Align.CENTER)
        separator.set_size_request(60, -1)
        separator.get_style_context().add_provider(style_provider_separator, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        grid.attach(separator, 0, 1, 1, 1)
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_halign(Gtk.Align.CENTER)
        separator.set_valign(Gtk.Align.CENTER)
        separator.set_size_request(60, -1)
        separator.get_style_context().add_provider(style_provider_separator, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        grid.attach(separator, 1, 1, 1, 1)
        # Label (Average Usage)
        self.average_usage_label = Gtk.Label()
        self.average_usage_label.set_selectable(True)
        self.average_usage_label.set_attributes(self.attribute_list_bold)
        self.average_usage_label.set_label("--")
        self.average_usage_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.average_usage_label, 0, 2, 1, 1)
        # Label (Frequency)
        self.frequency_label = Gtk.Label()
        self.frequency_label.set_selectable(True)
        self.frequency_label.set_attributes(self.attribute_list_bold)
        self.frequency_label.set_label("--")
        self.frequency_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.frequency_label, 1, 2, 1, 1)

        # Styled information widgets (Processes-Threads and Up Time)
        # ScrolledWindow (Processes-Threads and Up Time)
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_has_frame(True)
        scrolledwindow.get_style_context().add_provider(style_provider_scrolledwindow, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        performance_info_grid.attach(scrolledwindow, 0, 1, 1, 1)
        # Grid (Processes-Threads and Up Time)
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(3)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)
        grid.set_margin_start(5)
        grid.set_margin_end(5)
        grid.set_valign(Gtk.Align.CENTER)
        scrolledwindow.set_child(grid)
        # Label (Processes-Threads)
        label = Gtk.Label()
        label.set_label(_tr("Processes-Threads"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Label (Up Time)
        label = Gtk.Label()
        label.set_label(_tr("Up Time"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 1, 0, 1, 1)
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_halign(Gtk.Align.CENTER)
        separator.set_valign(Gtk.Align.CENTER)
        separator.set_size_request(60, -1)
        separator.get_style_context().add_provider(style_provider_separator, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        grid.attach(separator, 0, 1, 1, 1)
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_halign(Gtk.Align.CENTER)
        separator.set_valign(Gtk.Align.CENTER)
        separator.set_size_request(60, -1)
        separator.get_style_context().add_provider(style_provider_separator, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        grid.attach(separator, 1, 1, 1, 1)
        # Label (Processes-Threads)
        self.processes_threads_label = Gtk.Label()
        self.processes_threads_label.set_selectable(True)
        self.processes_threads_label.set_attributes(self.attribute_list_bold)
        self.processes_threads_label.set_label("--")
        self.processes_threads_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.processes_threads_label, 0, 2, 1, 1)
        # Label (Up Time)
        self.up_time_label = Gtk.Label()
        self.up_time_label.set_selectable(True)
        self.up_time_label.set_attributes(self.attribute_list_bold)
        self.up_time_label.set_label("--")
        self.up_time_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.up_time_label, 1, 2, 1, 1)

        # Grid - Right information labels
        performance_info_right_grid = Gtk.Grid()
        performance_info_right_grid.set_column_homogeneous(True)
        performance_info_right_grid.set_row_homogeneous(True)
        performance_info_right_grid.set_column_spacing(2)
        performance_info_right_grid.set_row_spacing(4)
        performance_info_grid.attach(performance_info_right_grid, 1, 0, 1, 2)

        # Labels - Right information labels
        # Label (Min-Max Frequency)
        label = Gtk.Label()
        label.set_label(_tr("Min-Max Frequency") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 0, 1, 1)
        # Label (Min-Max Frequency)
        self.min_max_frequency_label = Gtk.Label()
        self.min_max_frequency_label.set_selectable(True)
        self.min_max_frequency_label.set_attributes(self.attribute_list_bold)
        self.min_max_frequency_label.set_label("--")
        self.min_max_frequency_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.min_max_frequency_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.min_max_frequency_label, 1, 0, 1, 1)

        # Label (Cache (L1d-L1i))
        label = Gtk.Label()
        label.set_label(_tr("Cache (L1d-L1i)") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 1, 1, 1)
        # Label (Cache (L1d-L1i))
        self.cache_l1d_l1i_label = Gtk.Label()
        self.cache_l1d_l1i_label.set_selectable(True)
        self.cache_l1d_l1i_label.set_attributes(self.attribute_list_bold)
        self.cache_l1d_l1i_label.set_label("--")
        self.cache_l1d_l1i_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cache_l1d_l1i_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.cache_l1d_l1i_label, 1, 1, 1, 1)

        # Label (Cache (L2-L3))
        label = Gtk.Label()
        label.set_label(_tr("Cache (L2-L3)") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 2, 1, 1)
        # Label (Cache (L2-L3))
        self.cache_l2_l3_label = Gtk.Label()
        self.cache_l2_l3_label.set_selectable(True)
        self.cache_l2_l3_label.set_attributes(self.attribute_list_bold)
        self.cache_l2_l3_label.set_label("--")
        self.cache_l2_l3_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cache_l2_l3_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.cache_l2_l3_label, 1, 2, 1, 1)

        # Label (CPU Sockets)
        label = Gtk.Label()
        label.set_label(_tr("CPU Sockets") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 3, 1, 1)
        # Label (CPU Sockets)
        self.cpu_sockets_label = Gtk.Label()
        self.cpu_sockets_label.set_selectable(True)
        self.cpu_sockets_label.set_attributes(self.attribute_list_bold)
        self.cpu_sockets_label.set_label("--")
        self.cpu_sockets_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cpu_sockets_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.cpu_sockets_label, 1, 3, 1, 1)

        # Label (Cores (Physical-Logical))
        label = Gtk.Label()
        label.set_label(_tr("Cores (Physical-Logical)") + ":")
        label.set_tooltip_text(_tr("Number of online physical and logical CPU cores"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 4, 1, 1)
        # Label (Cores (Physical-Logical))
        self.cores_phy_log_label = Gtk.Label()
        self.cores_phy_log_label.set_selectable(True)
        self.cores_phy_log_label.set_attributes(self.attribute_list_bold)
        self.cores_phy_log_label.set_label("--")
        self.cores_phy_log_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cores_phy_log_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.cores_phy_log_label, 1, 4, 1, 1)

        # Label (Architecture)
        label = Gtk.Label()
        label.set_label(_tr("Architecture") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 5, 1, 1)
        # Label (Architecture)
        self.architecture_label = Gtk.Label()
        self.architecture_label.set_selectable(True)
        self.architecture_label.set_attributes(self.attribute_list_bold)
        self.architecture_label.set_label("--")
        self.architecture_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.architecture_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.architecture_label, 1, 5, 1, 1)


    def connect_signals(self):
        """
        Connect GUI signals.
        """

        self.da_cpu_usage.set_draw_func(Performance.performance_line_charts_draw_func, "da_cpu_usage")

        # Drawingarea mouse events
        drawingarea_mouse_event = Gtk.EventControllerMotion()
        drawingarea_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawingarea_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawingarea_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        self.da_cpu_usage.add_controller(drawingarea_mouse_event)


    def cpu_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        logical_core_list_system_ordered = Performance.logical_core_list_system_ordered
        selected_cpu_core = Performance.selected_cpu_core
        selected_cpu_core_number_only = selected_cpu_core.split("cpu")[1]


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
        selected_cpu_core_number = Performance.selected_cpu_core_number
        selected_cpu_core = Performance.selected_cpu_core
        selected_cpu_core_number_only = selected_cpu_core.split("cpu")[1]
        # Run "cpu_initial_func" if selected CPU core is changed since the last loop.
        try:                                                                                      
            if self.selected_cpu_core_prev != selected_cpu_core:
                self.cpu_initial_func()
        # try-except is used in order to avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.selected_cpu_core_prev = selected_cpu_core

        self.da_cpu_usage.queue_draw()

        # Run "main_gui_device_selection_list_func" if selected device list is changed since the last loop.
        logical_core_list_system_ordered = Performance.logical_core_list_system_ordered
        try:                                                                                      
            if self.logical_core_list_system_ordered_prev != logical_core_list_system_ordered:
                MainWindow.main_gui_device_selection_list_func()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list_func" if this is first loop of the function.
        except AttributeError:
            pass
        self.logical_core_list_system_ordered_prev = logical_core_list_system_ordered


        # Get information.
        number_of_physical_cores, number_of_cpu_sockets, cpu_model_name = self.number_of_physical_cores_sockets_cpu_name_func(selected_cpu_core_number, number_of_logical_cores)
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
        Get minimum and maximum frequencies of the selected CPU core.
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
        Get L1i, L1d, L2, L3 cache memory values of the selected CPU core.
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


    def number_of_physical_cores_sockets_cpu_name_func(self, selected_cpu_core_number, number_of_logical_cores):
        """
        Get number of physical cores, number of cpu sockets, cpu_model_names.
        """

        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_output = reader.read()
        proc_cpuinfo_output_lines = proc_cpuinfo_output.split("\n")

        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "x86_64" architecture. Physical and logical cores and model name per core information are tracked easily on this platform.
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

        # Get number of physical cores, number_of_cpu_sockets, cpu_model_names for "ARM" architecture. Physical and logical cores and model name per core information are not tracked easily on this platform. Different ARM processors (v6, v7, v8 or models of same ARM vX processors) may have different information in "/proc/cpuinfo" file.
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
        Get current frequency of the selected CPU core.
        """

        cpu_core_current_frequency = "-"

        # "/sys/devices/system/cpu/cpu[NUMBER]/cpufreq" is used instead of "/sys/devices/system/cpu/cpufreq/policy[NUMBER]" because CPU core current frequencies may be same for all cores on RB_Pi devices and "scaling_cur_freq" file may be available for only 0th core of the relevant CPU group (little cores , big cores).
        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cpufreq/scaling_cur_freq") as reader:
                cpu_core_current_frequency = float(reader.read().strip()) / 1000000
        # CPU core current frequency may not be available in "/sys/devices/system/cpu/cpufreq/policy..." folders on virtual machines (x86_64). Get it by reading "/proc/cpuinfo" file.
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
                # try-except is used in order to skip to the next loop without application error if a "FileNotFoundError" error is encountered when process is ended after process list is get.
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


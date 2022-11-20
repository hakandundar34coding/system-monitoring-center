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

        # CPU tab GUI
        self.cpu_tab_gui()

        # "0" value of "initial_already_run" variable means that initial function is not run before or
        # tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    def cpu_tab_gui(self):
        """
        Generate CPU tab GUI.
        """

        # CPU tab grid
        self.cpu_tab_grid = Gtk.Grid()
        self.cpu_tab_grid.set_row_spacing(10)
        self.cpu_tab_grid.set_margin_top(2)
        self.cpu_tab_grid.set_margin_bottom(2)
        self.cpu_tab_grid.set_margin_start(2)
        self.cpu_tab_grid.set_margin_end(2)

        # Bold and 2x label atributes
        self.attribute_list_bold_2x = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold_2x.insert(attribute)
        attribute = Pango.attr_scale_new(2.0)
        self.attribute_list_bold_2x.insert(attribute)

        # Bold label atributes
        self.attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold.insert(attribute)

        # Tab name, device name labels
        self.cpu_gui_label_grid()

        # Drawingarea and related information labels
        self.cpu_gui_da_grid()

        # Performance information labels
        self.cpu_gui_performance_info_grid()

        # Connect signals
        self.cpu_gui_signals()


    def cpu_gui_label_grid(self):
        """
        Generate tab name, device name labels.
        """

        # Tab name label grid
        tab_name_label_grid = Gtk.Grid()
        self.cpu_tab_grid.attach(tab_name_label_grid, 0, 0, 1, 1)

        # Tab name label
        tab_name_label = Gtk.Label()
        tab_name_label.set_halign(Gtk.Align.START)
        tab_name_label.set_margin_end(60)
        tab_name_label.set_attributes(self.attribute_list_bold_2x)
        tab_name_label.set_label(_tr("CPU"))
        tab_name_label_grid.attach(tab_name_label, 0, 0, 1, 2)

        # Device vendor-model label
        self.device_vendor_model_label = Gtk.Label()
        self.device_vendor_model_label.set_halign(Gtk.Align.START)
        self.device_vendor_model_label.set_selectable(True)
        self.device_vendor_model_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.device_vendor_model_label.set_attributes(self.attribute_list_bold)
        self.device_vendor_model_label.set_label("--")
        self.device_vendor_model_label.set_tooltip_text(_tr("Vendor-Model"))
        tab_name_label_grid.attach(self.device_vendor_model_label, 1, 0, 1, 1)

        # Device kernel name label
        self.device_kernel_name_label = Gtk.Label()
        self.device_kernel_name_label.set_halign(Gtk.Align.START)
        self.device_kernel_name_label.set_selectable(True)
        self.device_kernel_name_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.device_kernel_name_label.set_label("--")
        self.device_kernel_name_label.set_tooltip_text(_tr("Device Name In Kernel"))
        tab_name_label_grid.attach(self.device_kernel_name_label, 1, 1, 1, 1)


    def cpu_gui_da_grid(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Drawingarea grid
        da_cpu_usage_grid = Gtk.Grid()
        da_cpu_usage_grid.set_hexpand(True)
        da_cpu_usage_grid.set_vexpand(True)
        self.cpu_tab_grid.attach(da_cpu_usage_grid, 0, 1, 1, 1)

        # Drawingarea upper-left label
        self.da_upper_left_label = Gtk.Label()
        self.da_upper_left_label.set_halign(Gtk.Align.START)
        self.da_upper_left_label.set_label(_tr("CPU Usage (Average)"))
        da_cpu_usage_grid.attach(self.da_upper_left_label, 0, 0, 1, 1)

        # Drawingarea upper-right label
        da_upper_right_label = Gtk.Label()
        da_upper_right_label.set_halign(Gtk.Align.END)
        da_upper_right_label.set_label("100%")
        da_cpu_usage_grid.attach(da_upper_right_label, 1, 0, 1, 1)

        # Drawingarea
        self.da_cpu_usage = Gtk.DrawingArea()
        self.da_cpu_usage.set_hexpand(True)
        self.da_cpu_usage.set_vexpand(True)
        da_cpu_usage_grid.attach(self.da_cpu_usage, 0, 2, 2, 1)

        # Drawingarea lower-right label
        da_lower_right_label = Gtk.Label()
        da_lower_right_label.set_halign(Gtk.Align.END)
        da_lower_right_label.set_label("0")
        da_cpu_usage_grid.attach(da_lower_right_label, 0, 3, 2, 1)


    def cpu_gui_performance_info_grid(self):
        """
        Generate performance information labels.
        """

        # Performance information labels grid
        performance_info_grid = Gtk.Grid()
        performance_info_grid.set_column_homogeneous(True)
        performance_info_grid.set_row_homogeneous(True)
        performance_info_grid.set_column_spacing(12)
        performance_info_grid.set_row_spacing(10)
        self.cpu_tab_grid.attach(performance_info_grid, 0, 2, 1, 1)

        # Performance information labels
        # Add viewports for showing borders around some the performance data and round the corners of the viewports.
        css = b"viewport {border-style: solid; border-radius: 8px 8px 8px 8px; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
        style_provider_viewport = Gtk.CssProvider()
        style_provider_viewport.load_from_data(css)

        # Add separators for showing lines with contrast colors between some the performance data and set color of the separators.
        css = b"separator {background: rgba(50%,50%,50%,0.6);}"
        style_provider_separator = Gtk.CssProvider()
        style_provider_separator.load_from_data(css)

        # Styled information widgets (Average Usage and Frequency)
        # Styled information viewport
        viewport = Gtk.Viewport()
        viewport.get_style_context().add_provider(style_provider_viewport, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        performance_info_grid.attach(viewport, 0, 0, 1, 1)
        # Styled information grid
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(3)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)
        grid.set_margin_start(5)
        grid.set_margin_end(5)
        grid.set_valign(Gtk.Align.CENTER)
        viewport.set_child(grid)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Average Usage"))
        label.set_tooltip_text(_tr("Average CPU usage of all cores"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Frequency"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 1, 0, 1, 1)
        # Styled information separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_halign(Gtk.Align.CENTER)
        separator.set_valign(Gtk.Align.CENTER)
        separator.set_size_request(60, -1)
        separator.get_style_context().add_provider(style_provider_separator, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        grid.attach(separator, 0, 1, 1, 1)
        # Styled information separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_halign(Gtk.Align.CENTER)
        separator.set_valign(Gtk.Align.CENTER)
        separator.set_size_request(60, -1)
        separator.get_style_context().add_provider(style_provider_separator, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        grid.attach(separator, 1, 1, 1, 1)
        # Styled information label (Average Usage)
        self.cpu_average_usage_label = Gtk.Label()
        self.cpu_average_usage_label.set_selectable(True)
        self.cpu_average_usage_label.set_attributes(self.attribute_list_bold)
        self.cpu_average_usage_label.set_label("--")
        self.cpu_average_usage_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.cpu_average_usage_label, 0, 2, 1, 1)
        # Styled information label (Frequency)
        self.cpu_frequency_label = Gtk.Label()
        self.cpu_frequency_label.set_selectable(True)
        self.cpu_frequency_label.set_attributes(self.attribute_list_bold)
        self.cpu_frequency_label.set_label("--")
        self.cpu_frequency_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.cpu_frequency_label, 1, 2, 1, 1)

        # Styled information widgets (Processes-Threads and Up Time)
        # Styled information viewport
        viewport = Gtk.Viewport()
        viewport.get_style_context().add_provider(style_provider_viewport, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        performance_info_grid.attach(viewport, 0, 1, 1, 1)
        # Styled information grid
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(3)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)
        grid.set_margin_start(5)
        grid.set_margin_end(5)
        grid.set_valign(Gtk.Align.CENTER)
        viewport.set_child(grid)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Processes-Threads"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Up Time"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 1, 0, 1, 1)
        # Styled information separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_halign(Gtk.Align.CENTER)
        separator.set_valign(Gtk.Align.CENTER)
        separator.set_size_request(60, -1)
        separator.get_style_context().add_provider(style_provider_separator, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        grid.attach(separator, 0, 1, 1, 1)
        # Styled information separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_halign(Gtk.Align.CENTER)
        separator.set_valign(Gtk.Align.CENTER)
        separator.set_size_request(60, -1)
        separator.get_style_context().add_provider(style_provider_separator, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        grid.attach(separator, 1, 1, 1, 1)
        # Styled information label (Processes-Threads)
        self.cpu_processes_threads_label = Gtk.Label()
        self.cpu_processes_threads_label.set_selectable(True)
        self.cpu_processes_threads_label.set_attributes(self.attribute_list_bold)
        self.cpu_processes_threads_label.set_label("--")
        self.cpu_processes_threads_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.cpu_processes_threads_label, 0, 2, 1, 1)
        # Styled information label (Up Time)
        self.cpu_up_time_label = Gtk.Label()
        self.cpu_up_time_label.set_selectable(True)
        self.cpu_up_time_label.set_attributes(self.attribute_list_bold)
        self.cpu_up_time_label.set_label("--")
        self.cpu_up_time_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.cpu_up_time_label, 1, 2, 1, 1)

        # Right information label grid
        performance_info_right_grid = Gtk.Grid()
        performance_info_right_grid.set_column_homogeneous(True)
        performance_info_right_grid.set_row_homogeneous(True)
        performance_info_right_grid.set_column_spacing(2)
        performance_info_right_grid.set_row_spacing(4)
        performance_info_grid.attach(performance_info_right_grid, 1, 0, 1, 2)

        # Right information labels
        label = Gtk.Label()
        label.set_label(_tr("Min-Max Frequency") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 0, 1, 1)

        # Right information label (Min-Max Frequency)
        self.cpu_min_max_frequency_label = Gtk.Label()
        self.cpu_min_max_frequency_label.set_selectable(True)
        self.cpu_min_max_frequency_label.set_attributes(self.attribute_list_bold)
        self.cpu_min_max_frequency_label.set_label("--")
        self.cpu_min_max_frequency_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cpu_min_max_frequency_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.cpu_min_max_frequency_label, 1, 0, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Cache (L1d-L1i)") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 1, 1, 1)

        # Right information label (Cache (L1d-L1i))
        self.cpu_cache_l1d_l1i_label = Gtk.Label()
        self.cpu_cache_l1d_l1i_label.set_selectable(True)
        self.cpu_cache_l1d_l1i_label.set_attributes(self.attribute_list_bold)
        self.cpu_cache_l1d_l1i_label.set_label("--")
        self.cpu_cache_l1d_l1i_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cpu_cache_l1d_l1i_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.cpu_cache_l1d_l1i_label, 1, 1, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Cache (L2-L3)") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 2, 1, 1)

        # Right information label (Cache (L2-L3))
        self.cpu_cache_l2_l3_label = Gtk.Label()
        self.cpu_cache_l2_l3_label.set_selectable(True)
        self.cpu_cache_l2_l3_label.set_attributes(self.attribute_list_bold)
        self.cpu_cache_l2_l3_label.set_label("--")
        self.cpu_cache_l2_l3_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cpu_cache_l2_l3_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.cpu_cache_l2_l3_label, 1, 2, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("CPU Sockets") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 3, 1, 1)

        # Right information label (CPU Sockets)
        self.cpu_sockets_label = Gtk.Label()
        self.cpu_sockets_label.set_selectable(True)
        self.cpu_sockets_label.set_attributes(self.attribute_list_bold)
        self.cpu_sockets_label.set_label("--")
        self.cpu_sockets_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cpu_sockets_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.cpu_sockets_label, 1, 3, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Cores (Physical-Logical)") + ":")
        label.set_tooltip_text(_tr("Number of online physical and logical CPU cores"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 4, 1, 1)

        # Right information label (Cores (Physical-Logical))
        self.cpu_cores_phy_log_label = Gtk.Label()
        self.cpu_cores_phy_log_label.set_selectable(True)
        self.cpu_cores_phy_log_label.set_attributes(self.attribute_list_bold)
        self.cpu_cores_phy_log_label.set_label("--")
        self.cpu_cores_phy_log_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cpu_cores_phy_log_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.cpu_cores_phy_log_label, 1, 4, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Architecture") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 5, 1, 1)

        # Right information label (Architecture)
        self.cpu_architecture_label = Gtk.Label()
        self.cpu_architecture_label.set_selectable(True)
        self.cpu_architecture_label.set_attributes(self.attribute_list_bold)
        self.cpu_architecture_label.set_label("--")
        self.cpu_architecture_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cpu_architecture_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.cpu_architecture_label, 1, 5, 1, 1)


    def cpu_gui_signals(self):
        """
        Connect GUI signals.
        """

        self.da_cpu_usage.set_draw_func(Performance.performance_line_charts_draw_func, "da_cpu_usage")

        # Drawingarea mouse events
        drawing_area_mouse_event = Gtk.EventControllerMotion()
        drawing_area_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawing_area_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawing_area_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        self.da_cpu_usage.add_controller(drawing_area_mouse_event)


    # ----------------------------------- CPU - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
    def cpu_initial_func(self):

        logical_core_list_system_ordered = Performance.logical_core_list_system_ordered
        selected_cpu_core = Performance.selected_cpu_core
        selected_cpu_core_number_only = selected_cpu_core.split("cpu")[1]


        # Get information.
        cpu_core_min_frequency, cpu_core_max_frequency = self.cpu_core_min_max_frequency_func(selected_cpu_core)
        cpu_core_l1d_cache, cpu_core_l1i_cache, cpu_core_l2_cache, cpu_core_l3_cache = self.cpu_core_l1_l2_l3_cache_func(selected_cpu_core)
        cpu_architecture = self.cpu_architecture_func()


        # Show information on labels.
        show_cpu_usage_per_core = Config.show_cpu_usage_per_core
        if show_cpu_usage_per_core == 0:
            self.da_upper_left_label.set_label(_tr("CPU Usage (Average)"))
        if show_cpu_usage_per_core == 1:
            self.da_upper_left_label.set_label(_tr("CPU Usage (Per Core)"))
        if isinstance(cpu_core_max_frequency, str) is False:
            self.cpu_min_max_frequency_label.set_label(f'{cpu_core_min_frequency:.2f} - {cpu_core_max_frequency:.2f} GHz')
        else:
            self.cpu_min_max_frequency_label.set_label(f'{cpu_core_min_frequency} - {cpu_core_max_frequency}')
        self.cpu_architecture_label.set_label(cpu_architecture)
        self.cpu_cache_l1d_l1i_label.set_label(f'{cpu_core_l1d_cache} - {cpu_core_l1i_cache}')
        self.cpu_cache_l2_l3_label.set_label(f'{cpu_core_l2_cache} - {cpu_core_l3_cache}')

        self.initial_already_run = 1


    # ----------------------------------- CPU - Get CPU Data Function (gets CPU data, shows on the labels on the GUI) -----------------------------------
    def cpu_loop_func(self):

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
        number_of_physical_cores, number_of_cpu_sockets, cpu_model_name = self.cpu_number_of_physical_cores_sockets_cpu_name_func(selected_cpu_core_number, number_of_logical_cores)
        cpu_core_current_frequency = self.cpu_core_current_frequency_func(selected_cpu_core)
        number_of_total_processes, number_of_total_threads = self.cpu_total_processes_threads_func()
        system_up_time = self.cpu_system_up_time_func()


        # Show information on labels.
        self.device_vendor_model_label.set_label(cpu_model_name)
        self.device_kernel_name_label.set_label(selected_cpu_core)
        self.cpu_processes_threads_label.set_label(f'{number_of_total_processes} - {number_of_total_threads}')
        self.cpu_up_time_label.set_label(system_up_time)
        self.cpu_average_usage_label.set_label(f'{cpu_usage_percent_ave[-1]:.{Config.performance_cpu_usage_percent_precision}f} %')
        self.cpu_frequency_label.set_label(f'{cpu_core_current_frequency:.2f} GHz')
        self.cpu_sockets_label.set_label(f'{number_of_cpu_sockets}')
        self.cpu_cores_phy_log_label.set_label(f'{number_of_physical_cores} - {number_of_logical_cores}')


    # ----------------------- Get minimum and maximum frequencies of the selected CPU core -----------------------
    def cpu_core_min_max_frequency_func(self, selected_cpu_core):

        try:
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cpufreq/scaling_max_freq") as reader:
                cpu_core_max_frequency = float(reader.read().strip()) / 1000000
            with open("/sys/devices/system/cpu/" + selected_cpu_core + "/cpufreq/scaling_min_freq") as reader:
                cpu_core_min_frequency = float(reader.read().strip()) / 1000000
        except FileNotFoundError:
            cpu_core_max_frequency = "-"
            cpu_core_min_frequency = "-"

        return cpu_core_min_frequency, cpu_core_max_frequency


    # ----------------------- Get cache memory values of the selected CPU core -----------------------
    def cpu_core_l1_l2_l3_cache_func(self, selected_cpu_core):

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


    # ----------------------- Get CPU architecture -----------------------
    def cpu_architecture_func(self):

        cpu_architecture = platform.processor()
        if cpu_architecture == "":
            cpu_architecture = platform.machine()
            if cpu_architecture == "":
                cpu_architecture = "-"

        return cpu_architecture


    # ----------------------- Get number of physical cores, number_of_cpu_sockets, cpu_model_names -----------------------
    def cpu_number_of_physical_cores_sockets_cpu_name_func(self, selected_cpu_core_number, number_of_logical_cores):

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


    # ----------------------- Get current frequency of the selected CPU core -----------------------
    def cpu_core_current_frequency_func(self, selected_cpu_core):

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


    # ----------------------- Get number_of_total_threads and number_of_total_processes -----------------------
    def cpu_total_processes_threads_func(self):

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


    # ----------------------- Get system up time (sut) -----------------------
    def cpu_system_up_time_func(self):

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


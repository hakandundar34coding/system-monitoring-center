#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, GLib, Pango

import os
import subprocess
from threading import Thread

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from MainWindow import MainWindow


class Gpu:

    def __init__(self):

        # GPU tab GUI
        self.gpu_tab_gui()

        # "0" value of "initial_already_run" variable means that initial function is not run before or
        # tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    def gpu_tab_gui(self):
        """
        Generate GPU tab GUI.
        """

        # GPU tab grid
        self.gpu_tab_grid = Gtk.Grid()
        self.gpu_tab_grid.set_row_spacing(10)
        self.gpu_tab_grid.set_margin_top(2)
        self.gpu_tab_grid.set_margin_bottom(2)
        self.gpu_tab_grid.set_margin_start(2)
        self.gpu_tab_grid.set_margin_end(2)

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
        self.gpu_gui_label_grid()

        # Drawingarea and related information labels
        self.gpu_gui_da_grid()

        # Performance information labels
        self.gpu_gui_performance_info_grid()

        # Connect signals
        self.gpu_gui_signals()


    def gpu_gui_label_grid(self):
        """
        Generate tab name, device name labels.
        """

        # Tab name label grid
        tab_name_label_grid = Gtk.Grid()
        self.gpu_tab_grid.attach(tab_name_label_grid, 0, 0, 1, 1)

        # Tab name label
        tab_name_label = Gtk.Label()
        tab_name_label.set_halign(Gtk.Align.START)
        tab_name_label.set_margin_end(60)
        tab_name_label.set_attributes(self.attribute_list_bold_2x)
        tab_name_label.set_label(_tr("GPU"))
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


    def gpu_gui_da_grid(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Drawingarea grid
        da_gpu_usage_grid = Gtk.Grid()
        da_gpu_usage_grid.set_hexpand(True)
        da_gpu_usage_grid.set_vexpand(True)
        self.gpu_tab_grid.attach(da_gpu_usage_grid, 0, 1, 1, 1)

        # Drawingarea upper-left label
        self.da_upper_left_label = Gtk.Label()
        self.da_upper_left_label.set_halign(Gtk.Align.START)
        self.da_upper_left_label.set_label(_tr("GPU Usage"))
        da_gpu_usage_grid.attach(self.da_upper_left_label, 0, 0, 1, 1)

        # Drawingarea upper-right label
        da_upper_right_label = Gtk.Label()
        da_upper_right_label.set_halign(Gtk.Align.END)
        da_upper_right_label.set_label("100%")
        da_gpu_usage_grid.attach(da_upper_right_label, 1, 0, 1, 1)

        # Drawingarea
        self.da_gpu_usage = Gtk.DrawingArea()
        self.da_gpu_usage.set_hexpand(True)
        self.da_gpu_usage.set_vexpand(True)
        da_gpu_usage_grid.attach(self.da_gpu_usage, 0, 2, 2, 1)

        # Drawingarea lower-right label
        da_lower_right_label = Gtk.Label()
        da_lower_right_label.set_halign(Gtk.Align.END)
        da_lower_right_label.set_label("0")
        da_gpu_usage_grid.attach(da_lower_right_label, 0, 3, 2, 1)


    def gpu_gui_performance_info_grid(self):
        """
        Generate performance information labels.
        """

        # Performance information labels grid
        performance_info_grid = Gtk.Grid()
        performance_info_grid.set_column_homogeneous(True)
        performance_info_grid.set_row_homogeneous(True)
        performance_info_grid.set_column_spacing(12)
        performance_info_grid.set_row_spacing(10)
        self.gpu_tab_grid.attach(performance_info_grid, 0, 2, 1, 1)

        # Performance information labels
        # Add viewports for showing borders around some the performance data and round the corners of the viewports.
        css = b"viewport {border-style: solid; border-radius: 8px 8px 8px 8px; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
        style_provider_viewport = Gtk.CssProvider()
        style_provider_viewport.load_from_data(css)

        # Add separators for showing lines with contrast colors between some the performance data and set color of the separators.
        css = b"separator {background: rgba(50%,50%,50%,0.6);}"
        style_provider_separator = Gtk.CssProvider()
        style_provider_separator.load_from_data(css)

        # Styled information widgets (GPU Usage and Video Memory)
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
        label.set_label(_tr("GPU Usage"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Video Memory"))
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
        # Styled information label (GPU Usage)
        self.gpu_usage_label = Gtk.Label()
        self.gpu_usage_label.set_selectable(True)
        self.gpu_usage_label.set_attributes(self.attribute_list_bold)
        self.gpu_usage_label.set_label("--")
        self.gpu_usage_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.gpu_usage_label, 0, 2, 1, 1)
        # Styled information label (Video Memory)
        self.gpu_video_memory_label = Gtk.Label()
        self.gpu_video_memory_label.set_selectable(True)
        self.gpu_video_memory_label.set_attributes(self.attribute_list_bold)
        self.gpu_video_memory_label.set_label("--")
        self.gpu_video_memory_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.gpu_video_memory_label, 1, 2, 1, 1)

        # Styled information widgets (Frequency and Temperature)
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
        label.set_label(_tr("Frequency"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Temperature"))
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
        # Styled information label (Frequency)
        self.gpu_frequency_label = Gtk.Label()
        self.gpu_frequency_label.set_selectable(True)
        self.gpu_frequency_label.set_attributes(self.attribute_list_bold)
        self.gpu_frequency_label.set_label("--")
        self.gpu_frequency_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.gpu_frequency_label, 0, 2, 1, 1)
        # Styled information label (Temperature)
        self.gpu_temperature_label = Gtk.Label()
        self.gpu_temperature_label.set_selectable(True)
        self.gpu_temperature_label.set_attributes(self.attribute_list_bold)
        self.gpu_temperature_label.set_label("--")
        self.gpu_temperature_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.gpu_temperature_label, 1, 2, 1, 1)

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
        self.gpu_min_max_frequency_label = Gtk.Label()
        self.gpu_min_max_frequency_label.set_selectable(True)
        self.gpu_min_max_frequency_label.set_attributes(self.attribute_list_bold)
        self.gpu_min_max_frequency_label.set_label("--")
        self.gpu_min_max_frequency_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.gpu_min_max_frequency_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.gpu_min_max_frequency_label, 1, 0, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Boot VGA") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 1, 1, 1)

        # Right information label (Boot VGA)
        self.gpu_boot_vga_label = Gtk.Label()
        self.gpu_boot_vga_label.set_selectable(True)
        self.gpu_boot_vga_label.set_attributes(self.attribute_list_bold)
        self.gpu_boot_vga_label.set_label("--")
        self.gpu_boot_vga_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.gpu_boot_vga_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.gpu_boot_vga_label, 1, 1, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Power Usage") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 2, 1, 1)

        # Right information label (Power Usage)
        self.gpu_power_usage_label = Gtk.Label()
        self.gpu_power_usage_label.set_selectable(True)
        self.gpu_power_usage_label.set_attributes(self.attribute_list_bold)
        self.gpu_power_usage_label.set_label("--")
        self.gpu_power_usage_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.gpu_power_usage_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.gpu_power_usage_label, 1, 2, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Driver") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 3, 1, 1)

        # Right information label (Driver)
        self.gpu_driver_label = Gtk.Label()
        self.gpu_driver_label.set_selectable(True)
        self.gpu_driver_label.set_attributes(self.attribute_list_bold)
        self.gpu_driver_label.set_label("--")
        self.gpu_driver_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.gpu_driver_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.gpu_driver_label, 1, 3, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Refresh Rate") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 4, 1, 1)

        # Right information label (Refresh Rate)
        self.gpu_refresh_rate_label = Gtk.Label()
        self.gpu_refresh_rate_label.set_selectable(True)
        self.gpu_refresh_rate_label.set_attributes(self.attribute_list_bold)
        self.gpu_refresh_rate_label.set_label("--")
        self.gpu_refresh_rate_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.gpu_refresh_rate_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.gpu_refresh_rate_label, 1, 4, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Resolution") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 5, 1, 1)

        # Right information label (Resolution)
        self.gpu_resolution_label = Gtk.Label()
        self.gpu_resolution_label.set_selectable(True)
        self.gpu_resolution_label.set_attributes(self.attribute_list_bold)
        self.gpu_resolution_label.set_label("--")
        self.gpu_resolution_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.gpu_resolution_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.gpu_resolution_label, 1, 5, 1, 1)


    def gpu_gui_signals(self):
        """
        Connect GUI signals.
        """

        self.da_gpu_usage.set_draw_func(Performance.performance_line_charts_draw_func, "da_gpu_usage")

        # Drawingarea mouse events
        drawing_area_mouse_event = Gtk.EventControllerMotion()
        drawing_area_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawing_area_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawing_area_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        self.da_gpu_usage.add_controller(drawing_area_mouse_event)


    # ----------------------------------- GPU - Initial Function -----------------------------------
    def gpu_initial_func(self):

        # Define initial values
        self.chart_data_history = Config.chart_data_history
        self.gpu_load_list = [0] * self.chart_data_history
        # Currently highest monitor refresh rate is 360. 365 is used in order to get GPU load for AMD GPUs precisely.
        self.amd_gpu_load_list = [0] * 365


        # Get information.
        self.gpu_get_gpu_list_and_boot_vga_func()
        self.gpu_set_selected_gpu_func()
        if_default_gpu = self.gpu_default_gpu_func()
        gpu_device_model_name = self.gpu_device_model_name_vendor_id_func()
        gpu_driver_name = self.gpu_driver_name_func()


        # Set GPU tab label texts by using information get
        self.device_vendor_model_label.set_text(gpu_device_model_name)
        self.device_kernel_name_label.set_text(f'{self.gpu_list[self.selected_gpu_number]}')
        self.gpu_boot_vga_label.set_text(if_default_gpu)
        self.gpu_driver_label.set_text(gpu_driver_name)

        self.initial_already_run = 1


    # ----------------------------------- GPU - Get GPU Data Function -----------------------------------
    def gpu_loop_func(self):

        # Run "gpu_initial_func" if "initial_already_run variable is "0" which means all settings of the application is reset and initial function has be be run in order to avoid errors. This check is required only for GPU tab (not required for other Performance tab sub-tabs).
        if self.initial_already_run == 0:
            self.gpu_initial_func()

        # Get information.
        current_resolution, current_refresh_rate = self.gpu_resolution_refresh_rate_func()
        gpu_pci_address = self.gpu_pci_address_func()
        gpu_load, gpu_memory, gpu_current_frequency, gpu_min_max_frequency, gpu_temperature, gpu_power = self.gpu_load_memory_frequency_power_func(gpu_pci_address)

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
        # Avoid errors and also run "main_gui_device_selection_list" if this is first loop of the function.
        except AttributeError:
            MainWindow.main_gui_device_selection_list()
        self.gpu_list_prev = gpu_list


        # Set and update GPU tab label texts by using information get
        self.gpu_usage_label.set_text(gpu_load)
        self.gpu_video_memory_label.set_text(gpu_memory)
        self.gpu_frequency_label.set_text(gpu_current_frequency)
        self.gpu_temperature_label.set_text(gpu_temperature)
        self.gpu_min_max_frequency_label.set_text(gpu_min_max_frequency)
        self.gpu_power_usage_label.set_text(gpu_power)
        self.gpu_refresh_rate_label.set_text(current_refresh_rate)
        self.gpu_resolution_label.set_text(f'{current_resolution}')


    # ----------------------- Get GPU list -----------------------
    def gpu_get_gpu_list_and_boot_vga_func(self):

        self.gpu_list = []
        self.gpu_device_path_list = []
        self.gpu_device_sub_path_list = []
        self.default_gpu = ""

        # Get GPU list from "/sys/class/drm/" directory which is used by x86_64 desktop systems.
        if os.path.isdir("/dev/dri/") == True:

            for file in os.listdir("/sys/class/drm/"):
                if "-" not in file and file.split("-")[0].rstrip("0123456789") == "card":
                    self.gpu_list.append(file)
                    self.gpu_device_path_list.append("/sys/class/drm/" + file + "/")
                    self.gpu_device_sub_path_list.append("/device/")

                    # Get if default GPU information.
                    try:
                        with open("/sys/class/drm/" + file + "/device/" + "boot_vga") as reader:
                            if reader.read().strip() == "1":
                                self.default_gpu = file
                    except (FileNotFoundError, NotADirectoryError) as me:
                        pass

        # Try to get GPU list from "/sys/devices/" folder which is used by some ARM systems with NVIDIA GPU.
        for file in os.listdir("/sys/devices/"):

            if file.split(".")[0] == "gpu":
                self.gpu_list.append(file)
                self.gpu_device_path_list.append("/sys/devices/" + file + "/")
                self.gpu_device_sub_path_list.append("/")

                # Get if default GPU information
                try:
                    with open("/sys/devices/" + file + "/" + "boot_vga") as reader:
                        if reader.read().strip() == "1":
                            self.default_gpu = file
                except (FileNotFoundError, NotADirectoryError) as me:
                    pass


    # ----------------------- Get default GPU -----------------------
    def gpu_set_selected_gpu_func(self):

        # "" is predefined gpu name before release of the software. This statement is used in order to avoid error, if no gpu selection is made since first run of the software.
        if Config.selected_gpu == "":
            if self.default_gpu != "":
                set_selected_gpu = self.default_gpu
            if self.default_gpu == "":
                set_selected_gpu = self.gpu_list[0]
        if Config.selected_gpu in self.gpu_list:
            set_selected_gpu = Config.selected_gpu
        else:
            if self.default_gpu != "":
                set_selected_gpu = self.default_gpu
            if self.default_gpu == "":
                set_selected_gpu = self.gpu_list[0]
        self.selected_gpu_number = self.gpu_list.index(set_selected_gpu)


    # ----------------------- Get if default GPU -----------------------
    def gpu_default_gpu_func(self):

        # Set default GPU if there is only 1 GPU on the system and these is not "boot_vga" file (on some systems such as ARM devices) which means default_gpu = "".
        if len(self.gpu_list) == 1:
            if_default_gpu = _tr("Yes")
        else:
            if self.gpu_list[self.selected_gpu_number] == self.default_gpu:
                if_default_gpu = _tr("Yes")
            else:
                if_default_gpu = _tr("No")

        return if_default_gpu


    # ----------------------- Get GPU driver name -----------------------
    def gpu_driver_name_func(self):

        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.gpu_list[selected_gpu_number]
        gpu_device_path = self.gpu_device_path_list[selected_gpu_number]
        gpu_device_sub_path = self.gpu_device_sub_path_list[selected_gpu_number]

        # Read device driver name by reading "uevent" file.
        with open(gpu_device_path + gpu_device_sub_path + "uevent") as reader:
            uevent_output_lines = reader.read().strip().split("\n")

        gpu_driver_name = "-"
        for line in uevent_output_lines:
            if line.startswith("DRIVER="):
                gpu_driver_name = line.split("=")[-1]
                break

        return gpu_driver_name


    # ----------------------- Get GPU device model name and vendor name -----------------------
    def gpu_device_model_name_vendor_id_func(self):

        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.gpu_list[selected_gpu_number]
        gpu_device_path = self.gpu_device_path_list[selected_gpu_number]
        gpu_device_sub_path = self.gpu_device_sub_path_list[selected_gpu_number]

        # Read device vendor and model ids by reading "modalias" file.
        with open(gpu_device_path + gpu_device_sub_path + "modalias") as reader:
            modalias_output = reader.read().strip()

        # Determine device subtype.
        device_subtype, device_alias = modalias_output.split(":", 1)
        device_vendor_name, device_model_name, self.device_vendor_id, device_model_id = Performance.performance_get_device_vendor_model_func(modalias_output)
        if device_vendor_name == "Unknown":
            device_vendor_name = "[" + _tr("Unknown") + "]"
        if device_model_name == "Unknown":
            device_model_name = "[" + _tr("Unknown") + "]"
        gpu_device_model_name = f'{device_vendor_name} - {device_model_name}'

        return gpu_device_model_name


    # ----------------------- Get GPU PCI address which will be used for detecting the selected GPU for processing GPU performance information -----------------------
    def gpu_pci_address_func(self):

        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.gpu_list[selected_gpu_number]
        gpu_device_path = self.gpu_device_path_list[selected_gpu_number]
        gpu_device_sub_path = self.gpu_device_sub_path_list[selected_gpu_number]

        # Read device driver name by reading "uevent" file.
        with open(gpu_device_path + gpu_device_sub_path + "uevent") as reader:
            uevent_output_lines = reader.read().strip().split("\n")

        # ARM GPUs does not have PCI address.
        gpu_pci_address = "-"
        for line in uevent_output_lines:
            if line.startswith("PCI_SLOT_NAME="):
                gpu_pci_address = line.split("=")[-1]
                break

        return gpu_pci_address


    # ----------------------- Get GPU load, memory, frequencies, power -----------------------
    def gpu_load_memory_frequency_power_func(self, gpu_pci_address):

        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.gpu_list[selected_gpu_number]
        gpu_device_path = self.gpu_device_path_list[selected_gpu_number]
        gpu_device_sub_path = self.gpu_device_sub_path_list[selected_gpu_number]

        # Define initial values. These values will be used if they can not be detected.
        gpu_load = "-"
        gpu_memory_used = "-"
        gpu_memory_capacity = "-"
        gpu_temperature = "-"
        gpu_current_frequency = "-"
        gpu_min_frequency = "-"
        gpu_max_frequency = "-"
        gpu_min_max_frequency = "-"
        gpu_power = "-"


        # If selected GPU vendor is Intel.
        if self.device_vendor_id == "v00008086":

            # Get GPU min frequency.
            try:
                with open(gpu_device_path + "gt_min_freq_mhz") as reader:
                    gpu_min_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_min_frequency = "-"

            if gpu_min_frequency != "-":
                gpu_min_frequency = f'{gpu_min_frequency} MHz'

            # Get GPU max frequency.
            try:
                with open(gpu_device_path + "gt_max_freq_mhz") as reader:
                    gpu_max_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_max_frequency = "-"

            if gpu_max_frequency != "-":
                gpu_max_frequency = f'{gpu_max_frequency} MHz'

            # Get GPU current frequency by reading "gt_cur_freq_mhz" file. This file may not be reliable because is contains a constant value on some systems. Actual value can be get by using "intel_gpu_top" tool by using root privileges.
            try:
                with open(gpu_device_path + "gt_cur_freq_mhz") as reader:
                    gpu_current_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_current_frequency = "-"

            if gpu_current_frequency != "-":
                gpu_current_frequency = f'{gpu_current_frequency} MHz'


        # If selected GPU vendor is AMD.
        if self.device_vendor_id in ["v00001022", "v00001002"]:

            # For more information about files under "/sys/class/drm/card[NUMBER]/device/" and their content for AMD GPUs: https://dri.freedesktop.org/docs/drm/gpu/amdgpu.html and https://wiki.archlinux.org/title/AMDGPU.

            # Get GPU current, min, max frequencies (engine frequencies). This file contains all available frequencies of the GPU. There is no separate frequency information in files for video clock frequency for AMD GPUs.
            gpu_frequency_file_output = "-"
            try:
                with open(gpu_device_path + "device/pp_dpm_sclk") as reader:
                    gpu_frequency_file_output = reader.read().strip().split("\n")
            except FileNotFoundError:
                gpu_current_frequency = "-"
                gpu_max_frequency = "-"

            if gpu_frequency_file_output != "-":
                for line in gpu_frequency_file_output:
                    if "*" in line:
                        gpu_current_frequency = line.split(":")[1].rstrip("*").strip()
                        # Add a space character between value and unit. "Mhz" is used in the relevant file instead of "MHz".
                        if "Mhz" in gpu_current_frequency:
                            gpu_current_frequency = gpu_current_frequency.split("Mhz")[0] + " MHz"
                        break
                gpu_min_frequency = gpu_frequency_file_output[0].split(":")[1].strip()
                # Add a space character between value and unit.
                if "Mhz" in gpu_min_frequency:
                    gpu_min_frequency = gpu_min_frequency.split("Mhz")[0] + " MHz"
                gpu_max_frequency = gpu_frequency_file_output[-1].split(":")[1].strip()
                # Add a space character between value and unit.
                if "Mhz" in gpu_max_frequency:
                    gpu_max_frequency = gpu_max_frequency.split("Mhz")[0] + " MHz"

            # Get GPU load average. There is no "%" character in "gpu_busy_percent" file. This file contains GPU load for a very small time.
            try:
                self.gpu_load_amd_func()
                gpu_load = f'{(sum(self.amd_gpu_load_list) / len(self.amd_gpu_load_list)):.0f} %'
            except Exception:
                gpu_load = "-"

            # Get GPU used memory (data in this file is in Bytes). There is also "mem_info_vis_vram_used" file for visible memory (can be shown on the "lspci" command) and "mem_info_gtt_used" file for reserved memory from system memory. gtt+vram=total video memory. Probably "mem_busy_percent" is for memory controller load.
            try:
                with open(gpu_device_path + "device/mem_info_vram_used") as reader:
                    gpu_memory_used = reader.read().strip()
            except FileNotFoundError:
                gpu_memory_used = "-"

            if gpu_memory_used != "-":
                gpu_memory_used = f'{(int(gpu_memory_used) / 1024 / 1024):.0f} MiB'

            # Get GPU memory capacity (data in this file is in Bytes).
            try:
                with open(gpu_device_path + "device/mem_info_vram_total") as reader:
                    gpu_memory_capacity = reader.read().strip()
            except FileNotFoundError:
                gpu_memory_capacity = "-"

            if gpu_memory_capacity != "-":
                gpu_memory_capacity = f'{(int(gpu_memory_capacity) / 1024 / 1024):.0f} MiB'

            # Get GPU temperature.
            try:
                gpu_sensor_list = os.listdir(gpu_device_path + "device/hwmon/")
                for sensor in gpu_sensor_list:
                    if os.path.isfile(gpu_device_path + "device/hwmon/" + sensor + "/temp1_input") == True:
                        with open(gpu_device_path + "device/hwmon/" + sensor + "/temp1_input") as reader:
                            gpu_temperature = reader.read().strip()
                        gpu_temperature = f'{(int(gpu_temperature) / 1000):.0f} °C'
                        break
            except (FileNotFoundError, NotADirectoryError, OSError) as me:
                gpu_temperature = "-"

            # Get GPU power usage.
            try:
                gpu_sensor_list = os.listdir(gpu_device_path + "device/hwmon/")
                for sensor in gpu_sensor_list:
                    if os.path.isfile(gpu_device_path + "device/hwmon/" + sensor + "/power1_input") == True:
                        with open(gpu_device_path + "device/hwmon/" + sensor + "/power1_input") as reader:
                            gpu_power = reader.read().strip()
                        # Value in this file is in microwatts.
                        gpu_power = f'{(int(gpu_power) / 1000000):.2f} W'
                    elif os.path.isfile(gpu_device_path + "device/hwmon/" + sensor + "/power1_average") == True:
                        with open(gpu_device_path + "device/hwmon/" + sensor + "/power1_average") as reader:
                            gpu_power = reader.read().strip()
                        gpu_power = f'{(int(gpu_power) / 1000000):.2f} W'
                    else:
                        gpu_power = "-"
            except (FileNotFoundError, NotADirectoryError, OSError) as me:
                gpu_power = "-"


        # If selected GPU vendor is Broadcom (for RB-Pi ARM devices).
        if self.device_vendor_id in ["Brcm"]:

            # Get GPU memory capacity. This information is get by using "vcgencmd" tool and it is not installed on the systems by default.
            try:
                if Config.environment_type == "flatpak":
                    gpu_memory_capacity = (subprocess.check_output(["flatpak-spawn", "--host", "vcgencmd", "get_mem", "gpu"], shell=False)).decode().strip().split("=")[1]
                else:
                    gpu_memory_capacity = (subprocess.check_output(["vcgencmd", "get_mem", "gpu"], shell=False)).decode().strip().split("=")[1]
            except Exception:
                gpu_memory_capacity = "-"

            # Get GPU current frequency. This information is get by using "vcgencmd" tool and it is not installed on the systems by default.
            try:
                if Config.environment_type == "flatpak":
                    gpu_current_frequency = (subprocess.check_output(["flatpak-spawn", "--host", "vcgencmd", "measure_clock", "core"], shell=False)).decode().strip().split("=")[1]
                else:
                    gpu_current_frequency = (subprocess.check_output(["vcgencmd", "measure_clock", "core"], shell=False)).decode().strip().split("=")[1]
                gpu_current_frequency = f'{float(gpu_current_frequency)/1000000:.0f} MHz'
            except Exception:
                gpu_current_frequency = "-"


        # If selected GPU vendor is NVIDIA and selected GPU is used on a PCI used system.
        if self.device_vendor_id == "v000010DE" and gpu_device_path.startswith("/sys/class/drm/") == True:

            # Try to get GPU usage information in a separate thread in order to prevent this function from blocking the main thread and GUI for a very small time which stops the GUI for a very small time.
            gpu_tool_output = "-"
            Thread(target=self.gpu_load_nvidia_func, daemon=True).start()

            try:
                gpu_tool_output = self.gpu_tool_output
            # Prevent error if thread is not finished before using the output variable "gpu_tool_output".
            except AttributeError:
                pass

            # Get values from command output if there was no error when running the command.
            if gpu_tool_output != "-":

                # Get line number of the selected GPU by using its PCI address.
                for i, line in enumerate(gpu_tool_output):
                    if gpu_pci_address in line or gpu_pci_address.upper() in line:
                        gpu_info_line_no = i
                        break

                gpu_tool_output_for_selected_gpu = gpu_tool_output[gpu_info_line_no].split(",")

                gpu_load = gpu_tool_output_for_selected_gpu[3].strip()
                gpu_memory_capacity = gpu_tool_output_for_selected_gpu[5].strip()
                gpu_memory_used = gpu_tool_output_for_selected_gpu[7].strip()
                gpu_temperature = gpu_tool_output_for_selected_gpu[8].strip()
                gpu_current_frequency = gpu_tool_output_for_selected_gpu[9].strip()
                gpu_max_frequency = gpu_tool_output_for_selected_gpu[10].strip()
                gpu_power = gpu_tool_output_for_selected_gpu[11].strip()

                if gpu_load in ["[Not Supported]", "[N/A]"]:
                    gpu_load = "-"
                if gpu_memory_used in ["[Not Supported]", "[N/A]"]:
                    gpu_memory_used = "-"
                if gpu_memory_capacity in ["[Not Supported]", "[N/A]"]:
                    gpu_memory_capacity = "-"
                if gpu_temperature in ["[Not Supported]", "[N/A]"]:
                    gpu_temperature = "-"
                if gpu_current_frequency in ["[Not Supported]", "[N/A]"]:
                    gpu_current_frequency = "-"
                if gpu_max_frequency in ["[Not Supported]", "[N/A]"]:
                    gpu_max_frequency = "-"
                if gpu_power in ["[Not Supported]", "[N/A]"]:
                    gpu_power = "-"

            try:
                gpu_temperature = float(gpu_temperature)
                gpu_temperature = f'{gpu_temperature:.0f} °C'
            except ValueError:
                pass


        # If selected GPU vendor is NVIDIA and selected GPU is used on an ARM system.
        if self.device_vendor_id in ["v000010DE", "Nvidia"] and gpu_device_path.startswith("/sys/devices/") == True:

            # Get GPU frequency folders list. NVIDIA Tegra GPU files are listed in "/sys/devices/gpu.0/devfreq/57000000.gpu/" folder.
            gpu_frequency_files_list = os.listdir(gpu_device_path + "devfreq/")
            gpu_frequency_folders_list = []
            for file in gpu_frequency_files_list:
                if file.endswith(".gpu") and os.path.isdir(gpu_device_path + "devfreq/" + file) == True:
                    gpu_frequency_folders_list.append(gpu_device_path + "devfreq/" + file + "/")
            gpu_frequency_folder = gpu_frequency_folders_list[0]

            # Get GPU min frequency.
            try:
                with open(gpu_frequency_folder + "min_freq") as reader:
                    gpu_min_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_min_frequency = "-"

            if gpu_min_frequency != "-":
                gpu_min_frequency = f'{(float(gpu_min_frequency) / 1000000):.0f}'

            # Get GPU max frequency.
            try:
                with open(gpu_frequency_folder + "max_freq") as reader:
                    gpu_max_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_max_frequency = "-"

            if gpu_max_frequency != "-":
                gpu_max_frequency = f'{(float(gpu_max_frequency) / 1000000):.0f} MHz'

            # Get GPU current frequency.
            try:
                with open(gpu_frequency_folder + "cur_freq") as reader:
                    gpu_current_frequency = reader.read().strip()
            except FileNotFoundError:
                gpu_current_frequency = "-"

            if gpu_current_frequency != "-":
                gpu_current_frequency = f'{(float(gpu_current_frequency) / 1000000):.0f} MHz'

            # Get GPU load.
            try:
                with open(gpu_device_path + "load") as reader:
                    gpu_load = reader.read().strip()
            except FileNotFoundError:
                gpu_load = "-"

            if gpu_load != "-":
                gpu_load = f'{(float(gpu_load) / 10):.0f} %'


        gpu_memory = f'{gpu_memory_used} / {gpu_memory_capacity}'
        gpu_min_max_frequency = f'{gpu_min_frequency} - {gpu_max_frequency}'

        return gpu_load, gpu_memory, gpu_current_frequency, gpu_min_max_frequency, gpu_temperature, gpu_power


    # ----------------------- Get GPU load average for NVIDIA (PCI) GPUs -----------------------
    def gpu_load_nvidia_func(self):

        # Define command for getting GPU usage information.
        if Config.environment_type == "flatpak":
            gpu_tool_command = ["flatpak-spawn", "--host", "nvidia-smi", "--query-gpu=gpu_name,gpu_bus_id,driver_version,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used,temperature.gpu,clocks.current.graphics,clocks.max.graphics,power.draw", "--format=csv"]
        else:
            gpu_tool_command = ["nvidia-smi", "--query-gpu=gpu_name,gpu_bus_id,driver_version,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used,temperature.gpu,clocks.current.graphics,clocks.max.graphics,power.draw", "--format=csv"]

        # Try to get GPU usage information.
        try:
            self.gpu_tool_output = (subprocess.check_output(gpu_tool_command, shell=False)).decode().strip().split("\n")
        # Prevent errors because nvidia-smi may not be installed on some devices (such as N.Switch with NVIDIA Tegra GPU).
        except FileNotFoundError:
            pass


    # ----------------------- Get GPU load average for AMD GPUs -----------------------
    def gpu_load_amd_func(self, *args):

        selected_gpu_number = self.selected_gpu_number
        selected_gpu = self.gpu_list[selected_gpu_number]
        gpu_device_path = self.gpu_device_path_list[selected_gpu_number]
        gpu_device_sub_path = self.gpu_device_sub_path_list[selected_gpu_number]

        # Destroy GLib source for preventing it repeating the function.
        try:
            self.gpu_glib_source.destroy()
        # "try-except" is used in order to prevent errors if this is first run of the function.
        except AttributeError:
            pass
        self.gpu_glib_source = GLib.timeout_source_new(1000 / 365)

        # Read file to get GPU load information. This information is calculated for a very small time (screen refresh rate or content (game, etc.) refresh rate?) and directly plotting this data gives spikes.
        with open(gpu_device_path + "device/gpu_busy_percent") as reader:
            gpu_load = reader.read().strip()

        # Add GPU load data into a list in order to calculate average of the list.
        self.amd_gpu_load_list.append(float(gpu_load))
        del self.amd_gpu_load_list[0]

        # Prevent running the function again if tab is GPU switched off.
        if Config.current_main_tab != 0 or Config.performance_tab_current_sub_tab != 5:
            return

        self.gpu_glib_source.set_callback(self.gpu_load_amd_func)
        # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
        self.gpu_glib_source.attach(GLib.MainContext.default())


    # ----------------------- Get screen resolution and refresh rate -----------------------
    def gpu_resolution_refresh_rate_func(self):

        resolution_list = []
        refresh_rate_list = []

        try:
            monitor_list = Gdk.Display().get_default().get_monitors()
        except Exception:
            current_resolution = "-"
            current_refresh_rate = "-"
            return current_resolution, current_refresh_rate

        for monitor in monitor_list:
            monitor_rectangle = monitor.get_geometry()
            monitor_width = monitor_rectangle.width
            monitor_height = monitor_rectangle.height
            resolution_list.append(str(monitor_width) + "x" + str(monitor_height))
            # Milli-Hertz is converted to Hertz
            refresh_rate = float(monitor.get_refresh_rate() / 1000)
            refresh_rate_list.append(f'{refresh_rate:.2f} Hz')

        current_resolution = ', '.join(resolution_list)
        current_refresh_rate = ', '.join(refresh_rate_list)

        return current_resolution, current_refresh_rate


Gpu = Gpu()


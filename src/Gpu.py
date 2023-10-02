import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

import os
import subprocess

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

        self.da_gpu_usage_grid()

        self.grid_for_da_gpu_memory_encoder_decoder_load()
        self.da_gpu_memory_grid()
        self.da_gpu_encoder_load_grid()
        self.da_gpu_decoder_load_grid()

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
        self.device_vendor_model_label.set_tooltip_text(_tr("Vendor") + "-" + _tr("Model"))
        grid.attach(self.device_vendor_model_label, 1, 0, 1, 1)

        # Label (device kernel name)
        self.device_kernel_name_label = Common.device_kernel_name_label()
        self.device_kernel_name_label.set_tooltip_text(_tr("Device Name In Kernel"))
        grid.attach(self.device_kernel_name_label, 1, 1, 1, 1)


    def da_gpu_usage_grid(self):
        """
        Generate tab drawingarea (GPU usage) and related information labels.
        """

        # Grid (drawingarea)
        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.tab_grid.attach(grid, 0, 1, 1, 2)

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


    def grid_for_da_gpu_memory_encoder_decoder_load(self):
        """
        Generate tab drawingarea (GPU memory, GPU encoder and decoder loads) and related information labels.
        """

        # Grid (drawingarea)
        self.da_gpu_memory_encoder_decoder_load_grid = Gtk.Grid()
        self.da_gpu_memory_encoder_decoder_load_grid.set_hexpand(True)
        self.da_gpu_memory_encoder_decoder_load_grid.set_vexpand(True)
        self.da_gpu_memory_encoder_decoder_load_grid.set_column_homogeneous(True)
        self.da_gpu_memory_encoder_decoder_load_grid.set_column_spacing(10)
        self.tab_grid.attach(self.da_gpu_memory_encoder_decoder_load_grid, 0, 3, 1, 1)


    def da_gpu_memory_grid(self):
        """
        Generate tab drawingarea (GPU memory) and related information labels.
        """

        # Grid (drawingarea)
        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.da_gpu_memory_encoder_decoder_load_grid.attach(grid, 0, 0, 1, 1)

        # Label (drawingarea upper-left)
        label = Common.da_upper_lower_label(_tr("GPU Memory"), Gtk.Align.START)
        grid.attach(label, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        label = Common.da_upper_lower_label("100%", Gtk.Align.END)
        grid.attach(label, 1, 0, 1, 1)

        # DrawingArea
        self.da_gpu_memory = Common.drawingarea(Performance.performance_line_charts_draw, "da_gpu_memory")
        grid.attach(self.da_gpu_memory, 0, 2, 2, 1)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label("0", Gtk.Align.END)
        grid.attach(label, 0, 3, 2, 1)


    def da_gpu_encoder_load_grid(self):
        """
        Generate tab drawingarea (GPU encoder_load) and related information labels.
        """

        # Grid (drawingarea)
        grid = Gtk.Grid()
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.da_gpu_memory_encoder_decoder_load_grid.attach(grid, 1, 0, 1, 1)

        # Label (drawingarea upper-left)
        self.label_video_encoder_or_encoder_decoder_load = Common.da_upper_lower_label(_tr("Video Encoder"), Gtk.Align.START)
        grid.attach(self.label_video_encoder_or_encoder_decoder_load, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        label = Common.da_upper_lower_label("100%", Gtk.Align.END)
        grid.attach(label, 1, 0, 1, 1)

        # DrawingArea
        self.da_gpu_encoder_load = Common.drawingarea(Performance.performance_line_charts_draw, "da_gpu_encoder_load")
        grid.attach(self.da_gpu_encoder_load, 0, 2, 2, 1)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label("0", Gtk.Align.END)
        grid.attach(label, 0, 3, 2, 1)


    def da_gpu_decoder_load_grid(self):
        """
        Generate tab drawingarea (GPU decoder) and related information labels.
        """

        # Grid (drawingarea)
        self.grid_video_decoder_load = Gtk.Grid()
        self.grid_video_decoder_load.set_hexpand(True)
        self.grid_video_decoder_load.set_vexpand(True)
        self.da_gpu_memory_encoder_decoder_load_grid.attach(self.grid_video_decoder_load, 2, 0, 1, 1)

        # Label (drawingarea upper-left)
        label = Common.da_upper_lower_label(_tr("Video Decoder"), Gtk.Align.START)
        self.grid_video_decoder_load.attach(label, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        label = Common.da_upper_lower_label("100%", Gtk.Align.END)
        self.grid_video_decoder_load.attach(label, 1, 0, 1, 1)

        # DrawingArea
        self.da_gpu_decoder_load = Common.drawingarea(Performance.performance_line_charts_draw, "da_gpu_decoder_load")
        self.grid_video_decoder_load.attach(self.da_gpu_decoder_load, 0, 2, 2, 1)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label("0", Gtk.Align.END)
        self.grid_video_decoder_load.attach(label, 0, 3, 2, 1)


    def information_grid(self):
        """
        Generate performance/information labels.
        """

        # Grid (performance/information labels)
        performance_info_grid = Common.performance_info_grid()
        self.tab_grid.attach(performance_info_grid, 0, 4, 1, 1)

        # Styled information widgets (GPU Usage and Video Memory)
        # ScrolledWindow (GPU Usage and Video Memory)
        scrolledwindow, self.gpu_usage_label, self.video_memory_label = Common.styled_information_scrolledwindow(_tr("GPU Usage"), None, _tr("GPU Memory"), None)
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

        # Label (Memory Frequency)
        label = Common.static_information_label(_tr("Memory Frequency") + ":")
        performance_info_right_grid.attach(label, 0, 1, 1, 1)
        # Label (Memory Frequency)
        self.memory_frequency_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.memory_frequency_label, 1, 1, 1, 1)

        # Label (Power Usage)
        label = Common.static_information_label(_tr("Power Usage") + ":")
        performance_info_right_grid.attach(label, 0, 2, 1, 1)
        # Label (Power Usage)
        self.power_usage_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.power_usage_label, 1, 2, 1, 1)

        # Label (Boot VGA)
        label = Common.static_information_label(_tr("Boot VGA") + ":")
        performance_info_right_grid.attach(label, 0, 3, 1, 1)
        # Label (Boot VGA)
        self.boot_vga_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.boot_vga_label, 1, 3, 1, 1)

        # Label (Driver)
        label = Common.static_information_label(_tr("Driver") + ":")
        performance_info_right_grid.attach(label, 0, 4, 1, 1)
        # Label (Driver)
        self.driver_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.driver_label, 1, 4, 1, 1)

        # Label (Details...)
        label = Common.static_information_label(_tr("Details") + ":")
        performance_info_right_grid.attach(label, 0, 5, 1, 1)
        # Label (Show...)
        self.details_label = Common.clickable_label(_tr("Show..."), self.on_details_label_released)
        performance_info_right_grid.attach(self.details_label, 1, 5, 1, 1)


    def on_details_label_released(self, event, count, x, y):
        """
        Show GPU details window.
        """

        widget = event.get_widget()

        try:
            self.gpu_details_window.present()
        except AttributeError:
            # Avoid generating window multiple times on every button click.
            self.gpu_details_window_gui()
            self.gpu_details_window.present()
        self.gpu_details_info_get()
        self.gpu_details_update()


    def gpu_details_window_gui(self):
        """
        GPU details window GUI.
        """

        # Window
        self.gpu_details_window = Gtk.Window()
        self.gpu_details_window.set_default_size(420, 490)
        self.gpu_details_window.set_title(_tr("GPU"))
        self.gpu_details_window.set_icon_name("system-monitoring-center")
        self.gpu_details_window.set_transient_for(MainWindow.main_window)
        self.gpu_details_window.set_modal(True)
        self.gpu_details_window.set_hide_on_close(True)

        # ScrolledWindow
        scrolledwindow = Common.window_main_scrolledwindow()
        self.gpu_details_window.set_child(scrolledwindow)

        # Viewport
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Main grid
        main_grid = Common.window_main_grid()
        viewport.set_child(main_grid)

        # Information labels
        # Label (Vendor - Model)
        label = Common.static_information_label(_tr("Vendor") + " - " + _tr("Model"))
        main_grid.attach(label, 0, 0, 1, 1)
        # Label (Vendor - Model)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 0, 1, 1)
        # Label (Vendor - Model)
        self.gpu_details_vendor_model_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_vendor_model_label, 2, 0, 1, 1)

        # Label (GPU)
        label = Common.static_information_label(_tr("GPU"))
        main_grid.attach(label, 0, 1, 1, 1)
        # Label (GPU)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 1, 1, 1)
        # Label (GPU)
        self.gpu_details_gpu_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_gpu_label, 2, 1, 1, 1)

        # Label (PCIe Address)
        label = Common.static_information_label(_tr("PCIe Address"))
        main_grid.attach(label, 0, 2, 1, 1)
        # Label (PCIe Address)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 2, 1, 1)
        # Label (PCIe Address)
        self.gpu_details_pcie_address_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_pcie_address_label, 2, 2, 1, 1)

        # Label (GPU Interface)
        label = Common.static_information_label(_tr("GPU Interface"))
        main_grid.attach(label, 0, 3, 1, 1)
        # Label (GPU Interface)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 3, 1, 1)
        # Label (GPU Interface)
        self.gpu_details_gpu_interface_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_gpu_interface_label, 2, 3, 1, 1)

        # Label (Link Speed)
        label = Common.static_information_label(_tr("Link Speed"))
        main_grid.attach(label, 0, 4, 1, 1)
        # Label (Link Speed)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 4, 1, 1)
        # Label (Link Speed)
        self.gpu_details_link_speed_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_link_speed_label, 2, 4, 1, 1)

        # Label (GPU Usage)
        label = Common.static_information_label(_tr("GPU Usage"))
        main_grid.attach(label, 0, 5, 1, 1)
        # Label (GPU Usage)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 5, 1, 1)
        # Label (GPU Usage)
        self.gpu_details_gpu_usage_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_gpu_usage_label, 2, 5, 1, 1)

        # Label (GPU Memory)
        label = Common.static_information_label(_tr("GPU Memory"))
        main_grid.attach(label, 0, 6, 1, 1)
        # Label (GPU Memory)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 6, 1, 1)
        # Label (GPU Memory)
        self.gpu_details_gpu_memory_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_gpu_memory_label, 2, 6, 1, 1)

        # Label (Frequency)
        label = Common.static_information_label(_tr("Frequency"))
        main_grid.attach(label, 0, 7, 1, 1)
        # Label (Frequency)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 7, 1, 1)
        # Label (Frequency)
        self.gpu_details_frequency_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_frequency_label, 2, 7, 1, 1)

        # Label (Min-Max Frequency)
        label = Common.static_information_label(_tr("Min-Max Frequency"))
        main_grid.attach(label, 0, 8, 1, 1)
        # Label (Min-Max Frequency)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 8, 1, 1)
        # Label (Min-Max Frequency)
        self.gpu_details_min_max_frequency_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_min_max_frequency_label, 2, 8, 1, 1)

        # Label (Memory Frequency)
        label = Common.static_information_label(_tr("Memory Frequency"))
        main_grid.attach(label, 0, 9, 1, 1)
        # Label (Memory Frequency)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 9, 1, 1)
        # Label (Memory Frequency)
        self.gpu_details_memory_frequency_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_memory_frequency_label, 2, 9, 1, 1)

        # Label (Temperature)
        label = Common.static_information_label(_tr("Temperature"))
        main_grid.attach(label, 0, 10, 1, 1)
        # Label (Temperature)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 10, 1, 1)
        # Label (Temperature)
        self.gpu_details_temperature_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_temperature_label, 2, 10, 1, 1)

        # Label (Power Usage)
        label = Common.static_information_label(_tr("Power Usage"))
        main_grid.attach(label, 0, 11, 1, 1)
        # Label (Power Usage)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 11, 1, 1)
        # Label (Power Usage)
        self.gpu_details_power_usage_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_power_usage_label, 2, 11, 1, 1)

        # Label (Boot VGA)
        label = Common.static_information_label(_tr("Boot VGA"))
        main_grid.attach(label, 0, 12, 1, 1)
        # Label (Boot VGA)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 12, 1, 1)
        # Label (Boot VGA)
        self.gpu_details_boot_vga_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_boot_vga_label, 2, 12, 1, 1)

        # Label (Driver)
        label = Common.static_information_label(_tr("Driver"))
        main_grid.attach(label, 0, 13, 1, 1)
        # Label (Driver)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 13, 1, 1)
        # Label (Driver)
        self.gpu_details_driver_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_driver_label, 2, 13, 1, 1)

        # Label (Connections)
        label = Common.static_information_label(_tr("Connections"))
        main_grid.attach(label, 0, 14, 1, 1)
        # Label (Connections)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 14, 1, 1)
        # Label (Connections)
        self.gpu_details_gpu_connections_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_gpu_connections_label, 2, 14, 1, 1)

        # Label (Refresh Rate)
        label = Common.static_information_label(_tr("Refresh Rate"))
        main_grid.attach(label, 0, 15, 1, 1)
        # Label (Refresh Rate)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 15, 1, 1)
        # Label (Refresh Rate)
        self.gpu_details_refresh_rate_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_refresh_rate_label, 2, 15, 1, 1)

        # Label (Resolution)
        label = Common.static_information_label(_tr("Resolution"))
        main_grid.attach(label, 0, 16, 1, 1)
        # Label (Resolution)
        label = Common.static_information_label(":")
        main_grid.attach(label, 1, 16, 1, 1)
        # Label (Resolution)
        self.gpu_details_resolution_label = Common.dynamic_information_label()
        main_grid.attach(self.gpu_details_resolution_label, 2, 16, 1, 1)


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

        current_resolution, current_refresh_rate = Libsysmon.get_resolution_refresh_rate()
        gpu_pci_address = Libsysmon.get_gpu_pci_address(selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)
        gpu_current_link_speed = Libsysmon.get_gpu_current_link_speed(gpu_device_path)
        gpu_max_link_speed = Libsysmon.get_gpu_max_link_speed(gpu_device_path)
        gpu_interface = Libsysmon.get_gpu_interface(gpu_device_path)
        gpu_connections = Libsysmon.get_gpu_connections(gpu_device_path, selected_gpu)

        # Set GPU Details window title
        self.gpu_details_window.set_title(_tr("GPU") + ": " + selected_gpu)

        # Set label text by using GPU data
        self.gpu_details_vendor_model_label.set_label(self.gpu_information_share_dict["gpu_device_model_name"])
        self.gpu_details_gpu_label.set_label(selected_gpu)
        self.gpu_details_pcie_address_label.set_label(gpu_pci_address)
        self.gpu_details_gpu_interface_label.set_label(gpu_interface)
        self.gpu_details_link_speed_label.set_label(gpu_current_link_speed + " / " + gpu_max_link_speed)
        self.gpu_details_gpu_usage_label.set_label(self.gpu_information_share_dict2["gpu_load"])
        self.gpu_details_gpu_memory_label.set_label(self.gpu_information_share_dict2["gpu_memory_used"] + " / " + self.gpu_information_share_dict2["gpu_memory_capacity"])
        self.gpu_details_frequency_label.set_label(self.gpu_information_share_dict2["gpu_current_frequency"])
        self.gpu_details_min_max_frequency_label.set_label(self.gpu_information_share_dict2["gpu_min_frequency"] + " - " + self.gpu_information_share_dict2["gpu_max_frequency"])
        self.gpu_details_memory_frequency_label.set_label(self.gpu_information_share_dict2["gpu_memory_current_frequency"] + " / " + self.gpu_information_share_dict2["gpu_memory_max_frequency"])
        self.gpu_details_temperature_label.set_label(self.gpu_information_share_dict2["gpu_temperature"])
        self.gpu_details_power_usage_label.set_label(self.gpu_information_share_dict2["gpu_power_current"] + " / " + self.gpu_information_share_dict2["gpu_power_max"])
        self.gpu_details_boot_vga_label.set_label(self.gpu_information_share_dict["if_default_gpu"])
        self.gpu_details_driver_label.set_label(self.gpu_information_share_dict["gpu_driver_name"])
        self.gpu_details_gpu_connections_label.set_label(gpu_connections)
        self.gpu_details_refresh_rate_label.set_label(current_refresh_rate)
        self.gpu_details_resolution_label.set_label(current_resolution)


    def gpu_details_update(self, *args):
        """
        Update GPU information on the GPU details window.
        """

        if self.gpu_details_window.get_visible() == True:
            # Destroy GLib source for preventing it repeating the function.
            try:
                self.main_glib_source.destroy()
            # Prevent errors if this is first run of the function.
            except AttributeError:
                pass
            self.main_glib_source = GLib.timeout_source_new(Config.update_interval * 1000)
            self.gpu_details_info_get()
            self.main_glib_source.set_callback(self.gpu_details_update)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed.
            # A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        # Define initial values
        self.chart_data_history = Config.chart_data_history
        self.gpu_load_list = [0] * self.chart_data_history
        self.gpu_memory_list = [0] * self.chart_data_history
        self.gpu_encoder_load_list = [0] * self.chart_data_history
        self.gpu_decoder_load_list = [0] * self.chart_data_history

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
        gpu_pci_address = Libsysmon.get_gpu_pci_address(selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)
        gpu_load_memory_frequency_power_dict = Libsysmon.get_gpu_load_memory_frequency_power(gpu_pci_address, device_vendor_id, selected_gpu_number, gpu_list, gpu_device_path_list, gpu_device_sub_path_list)

        gpu_load = gpu_load_memory_frequency_power_dict["gpu_load"]
        gpu_encoder_load = gpu_load_memory_frequency_power_dict["gpu_encoder_load"]
        gpu_decoder_load = gpu_load_memory_frequency_power_dict["gpu_decoder_load"]
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

        gpu_encoder_load = gpu_encoder_load.split()[0]
        if gpu_encoder_load == "-":
            self.gpu_encoder_load_list.append(0)
        else:
            self.gpu_encoder_load_list.append(float(gpu_encoder_load))
            gpu_encoder_load = f'{gpu_encoder_load} %'
        del self.gpu_encoder_load_list[0]

        gpu_decoder_load = gpu_decoder_load.split()[0]
        if gpu_decoder_load == "-":
            self.gpu_decoder_load_list.append(0)
        else:
            self.gpu_decoder_load_list.append(float(gpu_decoder_load))
            gpu_decoder_load = f'{gpu_decoder_load} %'
        del self.gpu_decoder_load_list[0]

        self.da_gpu_usage.queue_draw()
        self.da_gpu_memory.queue_draw()
        self.da_gpu_encoder_load.queue_draw()
        self.da_gpu_decoder_load.queue_draw()

        # Update video encoder and decoder load graphs GUI
        self.update_video_encoder_decoder_load_graph_gui()

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
        self.gpu_usage_label.set_label(gpu_load)
        self.video_memory_label.set_label(f'{gpu_memory_used} / {gpu_memory_capacity}')
        self.frequency_label.set_label(gpu_current_frequency)
        self.temperature_label.set_label(gpu_temperature)
        self.min_max_frequency_label.set_label(f'{gpu_min_frequency} - {gpu_max_frequency}')
        self.power_usage_label.set_label(gpu_power_current + " / " + gpu_power_max)
        self.memory_frequency_label.set_label(f'{gpu_memory_current_frequency} / {gpu_memory_max_frequency}')


    def update_video_encoder_decoder_load_graph_gui(self):
        """
        A single video engine load is get for new AMD GPUs.
        Because AMD GPUs have a single engine (VCN) for video encoding and decoding after 2018.
        In this case, video engine load value is tracked by "gpu_encoder_load" variable.
        "gpu_decoder_load" variable ise set as "-9999". Code using this function may recognize that
        there is a single video engine load value.
        """

        if self.gpu_decoder_load_list[-1] == float(-9999):
            if self.grid_video_decoder_load.get_visible() == True:
                self.grid_video_decoder_load.set_visible(False)
                self.label_video_encoder_or_encoder_decoder_load.set_text(_tr("Video Encoder") + " + " + _tr("Video Decoder"))
        elif self.gpu_decoder_load_list[-1] != float(-9999):
            if self.grid_video_decoder_load.get_visible() == False:
                self.grid_video_decoder_load.set_visible(True)
                self.label_video_encoder_or_encoder_decoder_load.set_text(_tr("Video Encoder"))

Gpu = Gpu()


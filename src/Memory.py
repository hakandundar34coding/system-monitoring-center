#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, GLib, Pango

import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from MainWindow import MainWindow


class Memory:

    def __init__(self):

        # Memory tab GUI
        self.memory_tab_gui()

        # "0" value of "initial_already_run" variable means that initial function is not run before or
        # tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    def memory_tab_gui(self):
        """
        Generate Memory tab GUI.
        """

        # Memory tab grid
        self.memory_tab_grid = Gtk.Grid()
        self.memory_tab_grid.set_row_spacing(10)
        self.memory_tab_grid.set_margin_top(2)
        self.memory_tab_grid.set_margin_bottom(2)
        self.memory_tab_grid.set_margin_start(2)
        self.memory_tab_grid.set_margin_end(2)

        # Bold and 2x label atributes
        self.attribute_list_bold_2x = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold_2x.insert(attribute)
        attribute = Pango.attr_scale_new(2.0)
        self.attribute_list_bold_2x.insert(attribute)

        # Bold and underlined label atributes
        self.attribute_list_bold_underlined = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold_underlined.insert(attribute)
        attribute = Pango.attr_underline_new(Pango.Underline.SINGLE)
        self.attribute_list_bold_underlined.insert(attribute)

        # Bold label atributes
        self.attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold.insert(attribute)

        # Tab name, device name labels
        self.memory_gui_label_grid()

        # Drawingarea and related information labels
        self.memory_gui_da_grid()

        # Performance information labels
        self.memory_gui_performance_info_grid()

        # Connect signals
        self.memory_gui_signals()


    def memory_gui_label_grid(self):
        """
        Generate tab name, device name labels.
        """

        # Tab name label grid
        tab_name_label_grid = Gtk.Grid()
        self.memory_tab_grid.attach(tab_name_label_grid, 0, 0, 1, 1)

        # Tab name label
        tab_name_label = Gtk.Label()
        tab_name_label.set_halign(Gtk.Align.START)
        tab_name_label.set_margin_end(60)
        tab_name_label.set_attributes(self.attribute_list_bold_2x)
        tab_name_label.set_label(_tr("Memory"))
        tab_name_label_grid.attach(tab_name_label, 0, 0, 1, 2)

        # Device vendor-model label
        self.device_vendor_model_label = Gtk.Label()
        self.device_vendor_model_label.set_halign(Gtk.Align.START)
        self.device_vendor_model_label.set_selectable(True)
        self.device_vendor_model_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.device_vendor_model_label.set_attributes(self.attribute_list_bold)
        self.device_vendor_model_label.set_label("--")
        tab_name_label_grid.attach(self.device_vendor_model_label, 1, 0, 1, 1)

        # Device kernel name label
        self.device_kernel_name_label = Gtk.Label()
        self.device_kernel_name_label.set_halign(Gtk.Align.START)
        self.device_kernel_name_label.set_selectable(True)
        self.device_kernel_name_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.device_kernel_name_label.set_label("--")
        tab_name_label_grid.attach(self.device_kernel_name_label, 1, 1, 1, 1)


    def memory_gui_da_grid(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Drawingarea grid
        da_memory_usage_grid = Gtk.Grid()
        da_memory_usage_grid.set_hexpand(True)
        da_memory_usage_grid.set_vexpand(True)
        self.memory_tab_grid.attach(da_memory_usage_grid, 0, 1, 1, 1)

        # Drawingarea upper-left label
        self.da_upper_left_label = Gtk.Label()
        self.da_upper_left_label.set_halign(Gtk.Align.START)
        self.da_upper_left_label.set_label(_tr("RAM Usage"))
        da_memory_usage_grid.attach(self.da_upper_left_label, 0, 0, 1, 1)

        # Drawingarea upper-right label
        da_upper_right_label = Gtk.Label()
        da_upper_right_label.set_halign(Gtk.Align.END)
        da_upper_right_label.set_label("100%")
        da_memory_usage_grid.attach(da_upper_right_label, 1, 0, 1, 1)

        # Drawingarea
        self.da_memory_usage = Gtk.DrawingArea()
        self.da_memory_usage.set_hexpand(True)
        self.da_memory_usage.set_vexpand(True)
        da_memory_usage_grid.attach(self.da_memory_usage, 0, 2, 2, 1)

        # Drawingarea lower-right label
        da_lower_right_label = Gtk.Label()
        da_lower_right_label.set_halign(Gtk.Align.END)
        da_lower_right_label.set_label("0")
        da_memory_usage_grid.attach(da_lower_right_label, 0, 3, 2, 1)


    def memory_gui_performance_info_grid(self):
        """
        Generate performance information labels.
        """

        # Performance information labels grid
        performance_info_grid = Gtk.Grid()
        performance_info_grid.set_column_homogeneous(True)
        performance_info_grid.set_column_spacing(10)
        performance_info_grid.set_row_spacing(6)
        self.memory_tab_grid.attach(performance_info_grid, 0, 2, 1, 1)

        # Performance information labels
        # Add viewports for showing borders around some the performance data and round the corners of the viewports.
        css = b"viewport {border-style: solid; border-radius: 8px 8px 8px 8px; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
        style_provider_viewport = Gtk.CssProvider()
        style_provider_viewport.load_from_data(css)

        # Add separators for showing lines with contrast colors between some the performance data and set color of the separators.
        css = b"separator {background: rgba(50%,50%,50%,0.6);}"
        style_provider_separator = Gtk.CssProvider()
        style_provider_separator.load_from_data(css)

        # Performance information left area title label
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("RAM"))
        label.set_halign(Gtk.Align.START)
        performance_info_grid.attach(label, 0, 0, 1, 1)

        # Styled information widgets (for RAM used and available)
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
        label.set_label(_tr("Used"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Available"))
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
        # Styled information label (for RAM used)
        self.ram_used_label = Gtk.Label()
        self.ram_used_label.set_selectable(True)
        self.ram_used_label.set_attributes(self.attribute_list_bold)
        self.ram_used_label.set_label("--")
        self.ram_used_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.ram_used_label, 0, 2, 1, 1)
        # Styled information label (for RAM available)
        self.ram_available_label = Gtk.Label()
        self.ram_available_label.set_selectable(True)
        self.ram_available_label.set_attributes(self.attribute_list_bold)
        self.ram_available_label.set_label("--")
        self.ram_available_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.ram_available_label, 1, 2, 1, 1)

        # Performance information lower left area grid
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_column_spacing(2)
        grid.set_row_spacing(3)
        performance_info_grid.attach(grid, 0, 2, 1, 1)

        # Performance information lower left area label
        label = Gtk.Label()
        label.set_label(_tr("Capacity"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 0, 1, 1)

        # Performance information lower left area label (for RAM Capacity)
        self.ram_capacity_label = Gtk.Label()
        self.ram_capacity_label.set_selectable(True)
        self.ram_capacity_label.set_attributes(self.attribute_list_bold)
        self.ram_capacity_label.set_label("--")
        self.ram_capacity_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.ram_capacity_label.set_halign(Gtk.Align.START)
        grid.attach(self.ram_capacity_label, 1, 0, 1, 1)

        # Performance information lower left area label
        label = Gtk.Label()
        label.set_label(_tr("Free"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)

        # Performance information lower left area label (for RAM Free)
        self.ram_free_label = Gtk.Label()
        self.ram_free_label.set_selectable(True)
        self.ram_free_label.set_attributes(self.attribute_list_bold)
        self.ram_free_label.set_label("--")
        self.ram_free_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.ram_free_label.set_halign(Gtk.Align.START)
        grid.attach(self.ram_free_label, 1, 1, 1, 1)

        # Performance information lower left area label
        label = Gtk.Label()
        label.set_label(_tr("Hardware"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)

        # Performance information lower left area label (for RAM Hardware)
        self.ram_hardware_label = Gtk.Label()
        self.ram_hardware_label.set_attributes(self.attribute_list_bold_underlined)
        self.ram_hardware_label.set_label(_tr("Show..."))
        self.ram_hardware_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.ram_hardware_label.set_halign(Gtk.Align.START)
        self.cursor_link = Gdk.Cursor.new_from_name("pointer")
        self.ram_hardware_label.set_cursor(self.cursor_link)
        grid.attach(self.ram_hardware_label, 1, 2, 1, 1)

        # Performance information right area title label
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Swap Memory"))
        label.set_halign(Gtk.Align.START)
        performance_info_grid.attach(label, 1, 0, 1, 1)

        # Styled information widgets (for Swap used percent and used)
        # Styled information viewport
        viewport = Gtk.Viewport()
        viewport.get_style_context().add_provider(style_provider_viewport, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        performance_info_grid.attach(viewport, 1, 1, 1, 1)
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
        label.set_label(_tr("Used"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Used"))
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
        # Styled information grid (for Swap used label and drawingarea)
        grid_label_and_da = Gtk.Grid()
        grid_label_and_da.set_column_spacing(5)
        grid.attach(grid_label_and_da, 0, 2, 1, 1)
        # Styled information drawingarea (for Swap used)
        self.da_swap_usage = Gtk.DrawingArea()
        self.da_swap_usage.set_hexpand(True)
        grid_label_and_da.attach(self.da_swap_usage, 0, 0, 1, 1)
        # Styled information label (for Swap used)
        self.swap_used_percent_label = Gtk.Label()
        self.swap_used_percent_label.set_selectable(True)
        self.swap_used_percent_label.set_attributes(self.attribute_list_bold)
        self.swap_used_percent_label.set_label("--")
        self.swap_used_percent_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid_label_and_da.attach(self.swap_used_percent_label, 1, 0, 1, 1)
        # Styled information label (for Swap free)
        self.swap_used_label = Gtk.Label()
        self.swap_used_label.set_selectable(True)
        self.swap_used_label.set_attributes(self.attribute_list_bold)
        self.swap_used_label.set_label("--")
        self.swap_used_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.swap_used_label, 1, 2, 1, 1)

        # Performance information lower right area grid
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_column_spacing(2)
        grid.set_row_spacing(3)
        performance_info_grid.attach(grid, 1, 2, 1, 1)

        # Performance information lower right area label
        label = Gtk.Label()
        label.set_label(_tr("Free"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 0, 1, 1)

        # Performance information lower right area label (for RAM Capacity)
        self.swap_free_label = Gtk.Label()
        self.swap_free_label.set_selectable(True)
        self.swap_free_label.set_attributes(self.attribute_list_bold)
        self.swap_free_label.set_label("--")
        self.swap_free_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.swap_free_label.set_halign(Gtk.Align.START)
        grid.attach(self.swap_free_label, 1, 0, 1, 1)

        # Performance information lower right area label
        label = Gtk.Label()
        label.set_label(_tr("Capacity"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)

        # Performance information lower right area label (for RAM Free)
        self.swap_capacity_label = Gtk.Label()
        self.swap_capacity_label.set_selectable(True)
        self.swap_capacity_label.set_attributes(self.attribute_list_bold)
        self.swap_capacity_label.set_label("--")
        self.swap_capacity_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.swap_capacity_label.set_halign(Gtk.Align.START)
        grid.attach(self.swap_capacity_label, 1, 1, 1, 1)

        # Performance information lower right area label
        label = Gtk.Label()
        label.set_label(_tr("Details"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)

        # Performance information lower right area label (for RAM Hardware)
        self.swap_details_label = Gtk.Label()
        self.swap_details_label.set_attributes(self.attribute_list_bold_underlined)
        self.swap_details_label.set_label(_tr("Show..."))
        self.swap_details_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.swap_details_label.set_halign(Gtk.Align.START)
        self.cursor_link = Gdk.Cursor.new_from_name("pointer")
        self.swap_details_label.set_cursor(self.cursor_link)
        grid.attach(self.swap_details_label, 1, 2, 1, 1)


    def memory_gui_signals(self):
        """
        Connect GUI signals.
        """

        self.da_memory_usage.set_draw_func(Performance.performance_line_charts_draw_func, "da_memory_usage")
        self.da_swap_usage.set_draw_func(Performance.performance_bar_charts_draw, "da_swap_usage")

        # Drawingarea mouse events
        drawing_area_mouse_event = Gtk.EventControllerMotion()
        drawing_area_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawing_area_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawing_area_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        self.da_memory_usage.add_controller(drawing_area_mouse_event)

        # "Show" labels mouse events. Definition of separate events are required for different widgets.
        show_label_mouse_event = Gtk.GestureClick()
        show_label_mouse_event.connect("released", self.on_details_released)
        self.ram_hardware_label.add_controller(show_label_mouse_event)
        show_label_mouse_event = Gtk.GestureClick()
        show_label_mouse_event.connect("released", self.on_details_released)
        self.swap_details_label.add_controller(show_label_mouse_event)


    def on_details_released(self, event, count, x, y):
        """
        Show RAM hardware window or swap details window.
        """

        widget = event.get_widget()

        # Show RAM hardware window
        if widget == self.ram_hardware_label:
            memory_ram_hardware_info = self.memory_ram_hardware_info_get()
            try:
                self.ram_hardware_window.present()
            except AttributeError:
                # Avoid generating window multiple times on every button click.
                self.ram_hardware_window_gui()
                self.ram_hardware_window.present()
            self.ram_hardware_win_label.set_label(memory_ram_hardware_info)

        # Show swap details window
        if widget == self.swap_details_label:
            try:
                self.swap_details_window.present()
            except AttributeError:
                # Avoid generating window multiple times on every button click.
                self.swap_details_window_gui()
                self.swap_details_window.present()
            self.memory_swap_details_info_get()
            self.memory_swap_details_update()


    def ram_hardware_window_gui(self):
        """
        RAM hardware window GUI.
        """

        # Window
        self.ram_hardware_window = Gtk.Window()
        self.ram_hardware_window.set_default_size(400, 480)
        self.ram_hardware_window.set_title(_tr("Physical RAM"))
        self.ram_hardware_window.set_icon_name("system-monitoring-center")
        self.ram_hardware_window.set_transient_for(MainWindow.main_window)
        self.ram_hardware_window.set_modal(True)
        self.ram_hardware_window.set_hide_on_close(True)

        # Add viewports for showing borders around some the performance data.
        css = b"scrolledwindow {border-style: solid; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
        style_provider_scrolledwindow = Gtk.CssProvider()
        style_provider_scrolledwindow.load_from_data(css)

        # ScrolledWindow
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_margin_top(10)
        scrolledwindow.set_margin_bottom(10)
        scrolledwindow.set_margin_start(10)
        scrolledwindow.set_margin_end(10)
        scrolledwindow.get_style_context().add_provider(style_provider_scrolledwindow, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.ram_hardware_window.set_child(scrolledwindow)

        # Viewport
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Main grid
        main_grid = Gtk.Grid.new()
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        viewport.set_child(main_grid)

        # Label
        self.ram_hardware_win_label = Gtk.Label()
        self.ram_hardware_win_label.set_halign(Gtk.Align.START)
        self.ram_hardware_win_label.set_valign(Gtk.Align.START)
        self.ram_hardware_win_label.set_selectable(True)
        self.ram_hardware_win_label.set_label("--")
        main_grid.attach(self.ram_hardware_win_label, 0, 0, 1, 1)


    def memory_ram_hardware_info_get(self):
        """
        Get RAM hardware information by using "dmidecode" command.
        """

        # Initial value of the variable
        memory_ram_hardware_info = ""

        # "sudo" has to be used for using "pkexec" to run "dmidecode" with root privileges.
        command_list = ["pkexec", "sudo", "dmidecode", "-t", "16,17"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        try:
            dmidecode_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()
        except Exception:
            dmidecode_output = "-"
            memory_ram_hardware_info = "-"

        dmidecode_output_lines = dmidecode_output.split("\n")

        # Initial value of "maximum_capacity". This value will be used if value could not be get.
        maximum_capacity = "-"
        number_of_devices = "-"

        # Perform the following operations if "Physical Memory Array" is found in "dmidecode_output" output. This information may not be available on some systems.
        if "Physical Memory Array" in dmidecode_output:
            for line in dmidecode_output_lines:
                line = line.strip()
                if line.startswith("Maximum Capacity:"):
                    maximum_capacity = line.split(":")[1].strip()
                    continue
                if line.startswith("Number Of Devices:"):
                    number_of_devices = line.split(":")[1].strip()
                    continue
        memory_ram_hardware_info = memory_ram_hardware_info + _tr("Maximum Capacity") + " :    " + maximum_capacity
        memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Number Of Devices") + " :    " + number_of_devices + "\n"

        # Perform the following operations if "Memory Device" is found in "dmidecode_output" output. This information may not be available on some systems.
        if "Memory Device" in dmidecode_output:
            data_per_slot = dmidecode_output.split("Memory Device")
            # First element in this list is not information of memory device and it is deleted.
            del data_per_slot[0]
            for data in data_per_slot:
                data_lines = data.split("\n")
                memory_size = "-"
                memory_form_factor = "-"
                memory_locator = "-"
                memory_bank_locator = "-"
                memory_type = "-"
                memory_speed = "-"
                memory_manufacturer = "-"
                for line in data_lines:
                    line = line.strip()
                    if  line.startswith("Size:"):
                        memory_size = line.split(":")[1].strip()
                        continue
                    if line.startswith("Form Factor:"):
                        memory_form_factor = line.split(":")[1].strip()
                        continue
                    if line.startswith("Locator:"):
                        memory_locator = line.split(":")[1].strip()
                        continue
                    if line.startswith("Bank Locator:"):
                        memory_bank_locator = line.split(":")[1].strip()
                        continue
                    if line.startswith("Type:"):
                        memory_type = line.split(":")[1].strip()
                        continue
                    if line.startswith("Speed:"):
                        memory_speed = line.split(":")[1].strip()
                        continue
                    if line.startswith("Manufacturer:"):
                        memory_manufacturer = line.split(":")[1].strip()
                        continue
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Capacity") + " :    " + memory_size
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Type") + " :    " + memory_type
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Speed") + " :    " + memory_speed
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Manufacturer") + " :    " + memory_manufacturer
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Form Factor") + " :    " + memory_form_factor
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Locator") + " :    " + memory_locator
                memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Bank Locator") + " :    " + memory_bank_locator
                memory_ram_hardware_info = memory_ram_hardware_info + "\n"

        # Perform the following operations if "Memory Device" is not found in "dmidecode_output" output. This information may not be available on some systems.
        if "Memory Device" not in dmidecode_output:
            memory_size = "-"
            memory_form_factor = "-"
            memory_locator = "-"
            memory_bank_locator = "-"
            memory_type = "-"
            memory_speed = "-"
            memory_manufacturer = "-"

            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Capacity") + " :    " + memory_size
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Type") + " :    " + memory_type
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Speed") + " :    " + memory_speed
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Manufacturer") + " :    " + memory_manufacturer
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Form Factor") + " :    " + memory_form_factor
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Locator") + " :    " + memory_locator
            memory_ram_hardware_info = memory_ram_hardware_info + "\n" + _tr("Bank Locator") + " :    " + memory_bank_locator

        return memory_ram_hardware_info


    def swap_details_window_gui(self):
        """
        Swap details window GUI.
        """

        # Window
        self.swap_details_window = Gtk.Window()
        self.swap_details_window.set_default_size(320, 280)
        self.swap_details_window.set_title(_tr("Swap Memory"))
        self.swap_details_window.set_icon_name("system-monitoring-center")
        self.swap_details_window.set_transient_for(MainWindow.main_window)
        self.swap_details_window.set_modal(True)
        self.swap_details_window.set_hide_on_close(True)

        # Add viewports for showing borders around some the performance data.
        css = b"scrolledwindow {border-style: solid; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
        style_provider_scrolledwindow = Gtk.CssProvider()
        style_provider_scrolledwindow.load_from_data(css)

        # ScrolledWindow
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        scrolledwindow.set_margin_top(10)
        scrolledwindow.set_margin_bottom(10)
        scrolledwindow.set_margin_start(10)
        scrolledwindow.set_margin_end(10)
        scrolledwindow.get_style_context().add_provider(style_provider_scrolledwindow, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.swap_details_window.set_child(scrolledwindow)

        # Viewport
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Main grid
        main_grid = Gtk.Grid.new()
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        viewport.set_child(main_grid)

        # Label
        self.swap_details_win_label = Gtk.Label()
        self.swap_details_win_label.set_halign(Gtk.Align.START)
        self.swap_details_win_label.set_valign(Gtk.Align.START)
        self.swap_details_win_label.set_selectable(True)
        self.swap_details_win_label.set_label("--")
        main_grid.attach(self.swap_details_win_label, 0, 0, 1, 1)


    def memory_swap_details_info_get(self):
        """
        Get swap memory details information by reading "/proc/swaps" file.
        """

        performance_memory_data_precision = Config.performance_memory_data_precision
        performance_memory_data_unit = Config.performance_memory_data_unit

        # List for language translation
        memory_swap_details_text_list = [_tr("Partition"), _tr("File")]

        # Set initial value of "memory_hardware_information_text".
        memory_swap_details_info = ""

        # Read "/proc/swaps" file for getting swap memory details.
        # Systems may have more than one swap partition/file and this information can be read from this file.
        with open("/proc/swaps") as reader:
            proc_swaps_lines = reader.read().split("\n")

        # Delete header indormation which is get from "/proc/swaps" file.
        del proc_swaps_lines[0]

        for line in proc_swaps_lines:
            if line == "":
                break
            swap_name = "-"
            swap_type = "-"
            swap_size = "-"
            swap_used = "-"
            swap_priority = "-"
            line_split = line.split()
            swap_name = line_split[0].strip()
            swap_type = line_split[1].strip().title()
            # Values in this file are in KiB. They are converted to Bytes.
            swap_size = int(line_split[2].strip()) * 1024
            swap_size = f'{Performance.performance_data_unit_converter_func("data", "none", swap_size, performance_memory_data_unit, performance_memory_data_precision)}'
            swap_used = int(line_split[3].strip()) * 1024
            swap_used = f'{Performance.performance_data_unit_converter_func("data", "none", swap_used, performance_memory_data_unit, performance_memory_data_precision)}'
            swap_priority = line_split[4].strip()
            memory_swap_details_info = memory_swap_details_info + "\n" + _tr("Name") + " :    " + swap_name
            memory_swap_details_info = memory_swap_details_info + "\n" + _tr("Type") + " :    " + _tr(swap_type)
            memory_swap_details_info = memory_swap_details_info + "\n" + _tr("Capacity") + " :    " + swap_size
            memory_swap_details_info = memory_swap_details_info + "\n" + _tr("Used") + " :    " + swap_used
            memory_swap_details_info = memory_swap_details_info + "\n" + _tr("Priority") + " :    " + swap_priority
            memory_swap_details_info = memory_swap_details_info + "\n"
            memory_swap_details_info = memory_swap_details_info + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"

        # In order to remove this string from the last line.
        memory_swap_details_info = memory_swap_details_info.strip("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

        # Remove empty lines.
        memory_swap_details_info = memory_swap_details_info.strip()

        if memory_swap_details_info.strip() == "":
            memory_swap_details_info = "-"

        self.swap_details_win_label.set_label(memory_swap_details_info)


    def memory_swap_details_update(self, *args):
        """
        Update swap memory information on the swap details window.
        """

        if self.swap_details_window.get_visible() == True:
            # Destroy GLib source for preventing it repeating the function.
            try:
                self.main_glib_source.destroy()
            # Prevent errors if this is first run of the function.
            except AttributeError:
                pass
            self.main_glib_source = GLib.timeout_source_new(Config.update_interval * 1000)
            self.memory_swap_details_info_get()
            self.main_glib_source.set_callback(self.memory_swap_details_update)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed.
            # A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


    # ----------------------------------- Memory - Initial Function -----------------------------------
    def memory_initial_func(self):

        performance_memory_data_precision = Config.performance_memory_data_precision
        performance_memory_data_unit = Config.performance_memory_data_unit

        # Get total_physical_ram value (this value is very similar to RAM hardware size which is a bit different than ram_total value)
        # "block_size_bytes" file may not be present on some systems such as ARM CPU used systems. Currently kernel 5.10 does not have this feature but this feature will be included in the newer versions of the kernel.
        try:
            # "memory block size" is read from this file and size of the blocks depend on architecture (For more information see: https://www.kernel.org/doc/html/latest/admin-guide/mm/memory-hotplug.html).
            with open("/sys/devices/system/memory/block_size_bytes") as reader:
                # Value in this file is in hex form and it is converted into integer (byte)
                block_size = int(reader.read().strip(), 16)
        except FileNotFoundError:
            block_size = "-"
        if block_size != "-":
            total_online_memory = 0
            total_offline_memory = 0
            # Number of folders (of which name start with "memory") in this folder is multiplied with the integer value of "block_size_bytes" file content (hex value).
            files_in_sys_devices_system_memory = os.listdir("/sys/devices/system/memory/")
            for file in files_in_sys_devices_system_memory:
                if os.path.isdir("/sys/devices/system/memory/" + file) and file.startswith("memory"):
                    with open("/sys/devices/system/memory/" + file + "/online") as reader:
                        memory_online_offline_value = reader.read().strip()
                    if memory_online_offline_value == "1":
                        total_online_memory = total_online_memory + block_size
                    if memory_online_offline_value == "0":
                        total_offline_memory = total_offline_memory + block_size
            # Summation of total online and offline memories gives RAM hardware size. RAM harware size and total RAM value get from proc file system of by using "free" command are not same thing. Because some of the RAM may be reserved for harware and/or by the OS kernel.
            total_physical_ram = (total_online_memory + total_offline_memory)
        else:
            # Try to get physical RAM for RB Pi devices. This information is get by using "vcgencmd" tool and it is not installed on the systems by default.
            command_list = ["vcgencmd", "get_config", "total_mem"]
            if Config.environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list
            try:
                total_physical_ram = (subprocess.check_output(command_list, shell=False)).decode().strip().split("=")[1]
                # The value get by "vcgencmd get_config total_mem" command is in MiB unit.
                total_physical_ram = float(total_physical_ram)*1024*1024
            except Exception:
                total_physical_ram = "-"


        # Get ram_total and swap_total values
        with open("/proc/meminfo") as reader:
            proc_memory_info_output_lines = reader.read().split("\n")
        for line in proc_memory_info_output_lines:
            # Values in this file are in "KiB" unit. These values are multiplied with 1024 in order to obtain byte (nearly) values.
            if "MemTotal:" in line:
                ram_total = int(line.split()[1]) * 1024


        # Set Memory tab label texts by using information get
        if total_physical_ram != "-":
            self.device_vendor_model_label.set_text(_tr("Physical RAM") + ": " + str(Performance.performance_data_unit_converter_func("data", "none", total_physical_ram, 0, 1)))
        else:
            self.device_vendor_model_label.set_text(_tr("RAM") + " - " + _tr("Capacity") + ": " + str(Performance.performance_data_unit_converter_func("data", "none", ram_total, 0, 1)))

        self.initial_already_run = 1


    # ----------------------------------- Memory - Get Memory Data Function -----------------------------------
    def memory_loop_func(self):

        ram_used = Performance.ram_used
        ram_usage_percent = Performance.ram_usage_percent
        ram_available = Performance.ram_available
        ram_free = Performance.ram_free
        ram_total = Performance.ram_total

        self.swap_usage_percent = Performance.swap_usage_percent
        swap_used = Performance.swap_used
        swap_free = Performance.swap_free
        swap_total = Performance.swap_total

        performance_memory_data_precision = Config.performance_memory_data_precision
        performance_memory_data_unit = Config.performance_memory_data_unit

        self.da_memory_usage.queue_draw()
        self.da_swap_usage.queue_draw()


        # Set and update Memory tab label texts by using information get
        self.device_kernel_name_label.set_text(_tr("Swap Memory") + ": " + str(Performance.performance_data_unit_converter_func("data", "none", swap_total, 0, 1)))
        self.ram_used_label.set_text(f'{Performance.performance_data_unit_converter_func("data", "none", ram_used, performance_memory_data_unit, performance_memory_data_precision)} ({ram_usage_percent[-1]:.0f}%)')
        self.ram_available_label.set_text(Performance.performance_data_unit_converter_func("data", "none", ram_available, performance_memory_data_unit, performance_memory_data_precision))
        self.ram_capacity_label.set_text(Performance.performance_data_unit_converter_func("data", "none", ram_total, performance_memory_data_unit, performance_memory_data_precision))
        self.ram_free_label.set_text(Performance.performance_data_unit_converter_func("data", "none", ram_free, performance_memory_data_unit, performance_memory_data_precision))
        self.swap_used_percent_label.set_text(f'{self.swap_usage_percent[-1]:.0f}%')
        self.swap_used_label.set_text(f'{Performance.performance_data_unit_converter_func("data", "none", swap_used, performance_memory_data_unit, performance_memory_data_precision)}')
        self.swap_free_label.set_text(Performance.performance_data_unit_converter_func("data", "none", swap_free, performance_memory_data_unit, performance_memory_data_precision))
        self.swap_capacity_label.set_text(Performance.performance_data_unit_converter_func("data", "none", swap_total, performance_memory_data_unit, performance_memory_data_precision))


Memory = Memory()


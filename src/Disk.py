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


class Disk:

    def __init__(self):

        # Disk tab GUI
        self.disk_tab_gui()

        # "0" value of "initial_already_run" variable means that initial function is not run before or
        # tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    def disk_tab_gui(self):
        """
        Generate Disk tab GUI.
        """

        # Disk tab grid
        self.disk_tab_grid = Gtk.Grid()
        self.disk_tab_grid.set_row_spacing(10)
        self.disk_tab_grid.set_margin_top(2)
        self.disk_tab_grid.set_margin_bottom(2)
        self.disk_tab_grid.set_margin_start(2)
        self.disk_tab_grid.set_margin_end(2)

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
        self.disk_gui_label_grid()

        # Drawingarea and related information labels
        self.disk_gui_da_grid()

        # Performance information labels
        self.disk_gui_performance_info_grid()

        # Connect signals
        self.disk_gui_signals()


    def disk_gui_label_grid(self):
        """
        Generate tab name, device name labels.
        """

        # Tab name label grid
        tab_name_label_grid = Gtk.Grid()
        self.disk_tab_grid.attach(tab_name_label_grid, 0, 0, 1, 1)

        # Tab name label
        tab_name_label = Gtk.Label()
        tab_name_label.set_halign(Gtk.Align.START)
        tab_name_label.set_margin_end(60)
        tab_name_label.set_attributes(self.attribute_list_bold_2x)
        tab_name_label.set_label(_tr("Disk"))
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


    def disk_gui_da_grid(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Drawingarea grid
        da_disk_speed_grid = Gtk.Grid()
        da_disk_speed_grid.set_hexpand(True)
        da_disk_speed_grid.set_vexpand(True)
        self.disk_tab_grid.attach(da_disk_speed_grid, 0, 1, 1, 1)

        # Drawingarea upper-left label
        da_upper_left_label = Gtk.Label()
        da_upper_left_label.set_halign(Gtk.Align.START)
        da_upper_left_label.set_label(_tr("Read Speed") + " (-) & " + _tr("Write Speed") + " (-  -)")
        da_disk_speed_grid.attach(da_upper_left_label, 0, 0, 1, 1)

        # Drawingarea upper-right label
        self.da_upper_right_label = Gtk.Label()
        self.da_upper_right_label.set_halign(Gtk.Align.END)
        self.da_upper_right_label.set_label("--")
        da_disk_speed_grid.attach(self.da_upper_right_label, 1, 0, 1, 1)

        # Drawingarea
        self.da_disk_speed = Gtk.DrawingArea()
        self.da_disk_speed.set_hexpand(True)
        self.da_disk_speed.set_vexpand(True)
        da_disk_speed_grid.attach(self.da_disk_speed, 0, 2, 2, 1)

        # Drawingarea lower-right label
        da_lower_right_label = Gtk.Label()
        da_lower_right_label.set_halign(Gtk.Align.END)
        da_lower_right_label.set_label("0")
        da_disk_speed_grid.attach(da_lower_right_label, 0, 3, 2, 1)


    def disk_gui_performance_info_grid(self):
        """
        Generate performance information labels.
        """

        # Performance information labels grid
        performance_info_grid = Gtk.Grid()
        performance_info_grid.set_column_homogeneous(True)
        performance_info_grid.set_row_homogeneous(True)
        performance_info_grid.set_column_spacing(12)
        performance_info_grid.set_row_spacing(10)
        self.disk_tab_grid.attach(performance_info_grid, 0, 2, 1, 1)

        # Performance information labels
        # Add viewports for showing borders around some the performance data and round the corners of the viewports.
        css = b"viewport {border-style: solid; border-radius: 8px 8px 8px 8px; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
        style_provider_viewport = Gtk.CssProvider()
        style_provider_viewport.load_from_data(css)

        # Add separators for showing lines with contrast colors between some the performance data and set color of the separators.
        css = b"separator {background: rgba(50%,50%,50%,0.6);}"
        style_provider_separator = Gtk.CssProvider()
        style_provider_separator.load_from_data(css)

        # Styled information widgets (Read Speed and Write Speed)
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
        label.set_label(_tr("Read Speed"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Write Speed"))
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
        self.disk_read_speed_label = Gtk.Label()
        self.disk_read_speed_label.set_selectable(True)
        self.disk_read_speed_label.set_attributes(self.attribute_list_bold)
        self.disk_read_speed_label.set_label("--")
        self.disk_read_speed_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.disk_read_speed_label, 0, 2, 1, 1)
        # Styled information label (Frequency)
        self.disk_write_speed_label = Gtk.Label()
        self.disk_write_speed_label.set_selectable(True)
        self.disk_write_speed_label.set_attributes(self.attribute_list_bold)
        self.disk_write_speed_label.set_label("--")
        self.disk_write_speed_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.disk_write_speed_label, 1, 2, 1, 1)

        # Styled information widgets (Read Data and Write Data)
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
        label.set_label(_tr("Read Data"))
        label.set_tooltip_text(_tr("Measured value since last system start"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Write Data"))
        label.set_tooltip_text(_tr("Measured value since last system start"))
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
        self.disk_read_data_label = Gtk.Label()
        self.disk_read_data_label.set_selectable(True)
        self.disk_read_data_label.set_attributes(self.attribute_list_bold)
        self.disk_read_data_label.set_label("--")
        self.disk_read_data_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.disk_read_data_label, 0, 2, 1, 1)
        # Styled information label (Up Time)
        self.disk_write_data_label = Gtk.Label()
        self.disk_write_data_label.set_selectable(True)
        self.disk_write_data_label.set_attributes(self.attribute_list_bold)
        self.disk_write_data_label.set_label("--")
        self.disk_write_data_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.disk_write_data_label, 1, 2, 1, 1)

        # Right information label grid
        performance_info_right_grid = Gtk.Grid()
        performance_info_right_grid.set_column_homogeneous(True)
        #performance_info_right_grid.set_row_homogeneous(True)
        performance_info_right_grid.set_column_spacing(2)
        performance_info_right_grid.set_row_spacing(4)
        performance_info_grid.attach(performance_info_right_grid, 1, 0, 1, 2)

        # Right information labels
        # Right information label (System Disk)
        label = Gtk.Label()
        label.set_label(_tr("System Disk") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 0, 1, 1)

        # Right information label (System Disk)
        self.disk_system_disk_label = Gtk.Label()
        self.disk_system_disk_label.set_selectable(True)
        self.disk_system_disk_label.set_attributes(self.attribute_list_bold)
        self.disk_system_disk_label.set_label("--")
        self.disk_system_disk_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_system_disk_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.disk_system_disk_label, 1, 0, 1, 1)

        # Right information label (for Disk used percent)
        label = Gtk.Label()
        label.set_label(_tr("Used") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 2, 1, 1)

        # Right information grid (for Disk used percent label and drawingarea)
        grid_label_and_da = Gtk.Grid()
        grid_label_and_da.set_column_spacing(5)
        performance_info_right_grid.attach(grid_label_and_da, 1, 2, 1, 1)

        # Styled information drawingarea (for Disk used percent)
        self.da_disk_usage = Gtk.DrawingArea()
        self.da_disk_usage.set_hexpand(True)
        grid_label_and_da.attach(self.da_disk_usage, 0, 0, 1, 1)

        # Right information label (Used percent)
        self.disk_used_percent_label = Gtk.Label()
        self.disk_used_percent_label.set_selectable(True)
        self.disk_used_percent_label.set_attributes(self.attribute_list_bold)
        self.disk_used_percent_label.set_label("--")
        self.disk_used_percent_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_used_percent_label.set_halign(Gtk.Align.START)
        grid_label_and_da.attach(self.disk_used_percent_label, 1, 0, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Free") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 3, 1, 1)

        # Right information label (Free))
        self.disk_free_label = Gtk.Label()
        self.disk_free_label.set_selectable(True)
        self.disk_free_label.set_attributes(self.attribute_list_bold)
        self.disk_free_label.set_label("--")
        self.disk_free_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_free_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.disk_free_label, 1, 3, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Used") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 4, 1, 1)

        # Right information label (Used)
        self.disk_used_label = Gtk.Label()
        self.disk_used_label.set_selectable(True)
        self.disk_used_label.set_attributes(self.attribute_list_bold)
        self.disk_used_label.set_label("--")
        self.disk_used_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_used_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.disk_used_label, 1, 4, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Capacity") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 5, 1, 1)

        # Right information label (Capacity)
        self.disk_capacity_label = Gtk.Label()
        self.disk_capacity_label.set_selectable(True)
        self.disk_capacity_label.set_attributes(self.attribute_list_bold)
        self.disk_capacity_label.set_label("--")
        self.disk_capacity_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_capacity_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.disk_capacity_label, 1, 5, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Details") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 6, 1, 1)

        # Performance information lower right area label (for disk details)
        self.disk_details_label = Gtk.Label()
        self.disk_details_label.set_attributes(self.attribute_list_bold_underlined)
        self.disk_details_label.set_label(_tr("Show..."))
        self.disk_details_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_label.set_halign(Gtk.Align.START)
        self.cursor_link = Gdk.Cursor.new_from_name("pointer")
        self.disk_details_label.set_cursor(self.cursor_link)
        performance_info_right_grid.attach(self.disk_details_label, 1, 6, 1, 1)


    def disk_gui_signals(self):
        """
        Connect GUI signals.
        """

        self.da_disk_speed.set_draw_func(Performance.performance_line_charts_draw_func, "da_disk_speed_usage")
        self.da_disk_usage.set_draw_func(Performance.performance_bar_charts_draw, "da_disk_usage")

        # Drawingarea mouse events
        drawing_area_mouse_event = Gtk.EventControllerMotion()
        drawing_area_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawing_area_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawing_area_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        self.da_disk_speed.add_controller(drawing_area_mouse_event)

        # "Show" label mouse events
        show_label_mouse_event = Gtk.GestureClick()
        show_label_mouse_event.connect("released", self.on_details_released)
        self.disk_details_label.add_controller(show_label_mouse_event)


    def on_details_released(self, event, count, x, y):
        """
        Show Disk details window.
        """

        widget = event.get_widget()

        try:
            self.disk_details_window.present()
        except AttributeError:
            # Avoid generating window multiple times on every button click.
            self.disk_details_window_gui()
            self.disk_details_window.present()
        self.disk_details_info_get()
        self.disk_details_update()


    def disk_details_window_gui(self):
        """
        Disk details window GUI.
        """

        # Window
        self.disk_details_window = Gtk.Window()
        self.disk_details_window.set_default_size(400, 380)
        self.disk_details_window.set_title(_tr("Disk"))
        self.disk_details_window.set_icon_name("system-monitoring-center")
        self.disk_details_window.set_transient_for(MainWindow.main_window)
        self.disk_details_window.set_modal(True)
        self.disk_details_window.set_hide_on_close(True)

        # Style provider for showing borders of scrolledwindow.
        css = b"scrolledwindow {border-style: solid; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
        style_provider_scrolledwindow = Gtk.CssProvider()
        style_provider_scrolledwindow.load_from_data(css)

        # ScrolledWindow
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_margin_top(10)
        scrolledwindow.set_margin_bottom(10)
        scrolledwindow.set_margin_start(10)
        scrolledwindow.set_margin_end(10)
        scrolledwindow.get_style_context().add_provider(style_provider_scrolledwindow, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.disk_details_window.set_child(scrolledwindow)

        # Viewport
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Main grid
        main_grid = Gtk.Grid.new()
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        main_grid.set_column_spacing(10)
        main_grid.set_row_spacing(5)
        scrolledwindow.set_child(main_grid)

        # Information labels
        # Information label (Disk)
        label = Gtk.Label()
        label.set_label(_tr("Disk"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 0, 1, 1)

        # Information label (Disk)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 0, 1, 1)

        # Information label (Disk)
        self.disk_details_disk_label = Gtk.Label()
        self.disk_details_disk_label.set_selectable(True)
        self.disk_details_disk_label.set_label("--")
        self.disk_details_disk_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_disk_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_disk_label, 2, 0, 1, 1)

        # Information label (Parent Name)
        label = Gtk.Label()
        label.set_label(_tr("Parent Name"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 1, 1, 1)

        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 1, 1, 1)

        # Information label (Parent Name)
        self.disk_details_parent_disk_label = Gtk.Label()
        self.disk_details_parent_disk_label.set_selectable(True)
        self.disk_details_parent_disk_label.set_label("--")
        self.disk_details_parent_disk_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_parent_disk_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_parent_disk_label, 2, 1, 1, 1)

        # Information label (System Disk)
        label = Gtk.Label()
        label.set_label(_tr("System Disk"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 2, 1, 1)

        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 2, 1, 1)

        # Information label (System Disk)
        self.disk_details_system_disk_label = Gtk.Label()
        self.disk_details_system_disk_label.set_selectable(True)
        self.disk_details_system_disk_label.set_label("--")
        self.disk_details_system_disk_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_system_disk_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_system_disk_label, 2, 2, 1, 1)

        # Information label (Type)
        label = Gtk.Label()
        label.set_label(_tr("Type"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 3, 1, 1)

        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 3, 1, 1)

        # Information label (Type)
        self.disk_details_disk_type_label = Gtk.Label()
        self.disk_details_disk_type_label.set_selectable(True)
        self.disk_details_disk_type_label.set_label("--")
        self.disk_details_disk_type_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_disk_type_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_disk_type_label, 2, 3, 1, 1)

        # Information label (File System)
        label = Gtk.Label()
        label.set_label(_tr("File System"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 4, 1, 1)

        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 4, 1, 1)

        # Information label (File System)
        self.disk_details_file_system_label = Gtk.Label()
        self.disk_details_file_system_label.set_selectable(True)
        self.disk_details_file_system_label.set_label("--")
        self.disk_details_file_system_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_file_system_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_file_system_label, 2, 4, 1, 1)

        # Information label (Capacity)
        label = Gtk.Label()
        label.set_label(_tr("Capacity"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 5, 1, 1)

        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 5, 1, 1)

        # Information label (Capacity)
        self.disk_details_capacity_label = Gtk.Label()
        self.disk_details_capacity_label.set_selectable(True)
        self.disk_details_capacity_label.set_label("--")
        self.disk_details_capacity_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_capacity_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_capacity_label, 2, 5, 1, 1)

        # Information label (Capacity (Mass Storage))
        label = Gtk.Label()
        label.set_label(_tr("Capacity") + "\n" + "(" + _tr("Mass Storage") + ")")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 6, 1, 1)

        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 6, 1, 1)

        # Information label (Capacity (Mass Storage))
        self.disk_details_capacity_mass_label = Gtk.Label()
        self.disk_details_capacity_mass_label.set_selectable(True)
        self.disk_details_capacity_mass_label.set_label("--")
        self.disk_details_capacity_mass_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_capacity_mass_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_capacity_mass_label, 2, 6, 1, 1)

        # Information label (Free)
        label = Gtk.Label()
        label.set_label(_tr("Free"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 7, 1, 1)

        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 7, 1, 1)

        # Information label (Free)
        self.disk_details_free_label = Gtk.Label()
        self.disk_details_free_label.set_selectable(True)
        self.disk_details_free_label.set_label("--")
        self.disk_details_free_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_free_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_free_label, 2, 7, 1, 1)

        # Information label (Used)
        label = Gtk.Label()
        label.set_label(_tr("Used"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 8, 1, 1)

        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 8, 1, 1)

        # Information label (Used)
        self.disk_details_used_label = Gtk.Label()
        self.disk_details_used_label.set_selectable(True)
        self.disk_details_used_label.set_label("--")
        self.disk_details_used_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_used_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_used_label, 2, 8, 1, 1)

        # Information label (Vendor-Model)
        label = Gtk.Label()
        label.set_label(_tr("Vendor-Model"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 9, 1, 1)

        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 9, 1, 1)

        # Information label (Vendor-Model)
        self.disk_details_vendor_model_label = Gtk.Label()
        self.disk_details_vendor_model_label.set_selectable(True)
        self.disk_details_vendor_model_label.set_label("--")
        self.disk_details_vendor_model_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_vendor_model_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_vendor_model_label, 2, 9, 1, 1)

        # Information label (Label (File System))
        label = Gtk.Label()
        label.set_label(_tr("Label (File System)"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 10, 1, 1)

        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 10, 1, 1)

        # Information label (Label (File System))
        self.disk_details_label_fs_label = Gtk.Label()
        self.disk_details_label_fs_label.set_selectable(True)
        self.disk_details_label_fs_label.set_label("--")
        self.disk_details_label_fs_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_label_fs_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_label_fs_label, 2, 10, 1, 1)

        # Information label (Mount Point)
        label = Gtk.Label()
        label.set_label(_tr("Mount Point"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 11, 1, 1)

        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 1, 11, 1, 1)

        # Information label (Mount Point)
        self.disk_details_mount_point_label = Gtk.Label()
        self.disk_details_mount_point_label.set_selectable(True)
        self.disk_details_mount_point_label.set_label("--")
        self.disk_details_mount_point_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.disk_details_mount_point_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.disk_details_mount_point_label, 2, 11, 1, 1)


    def disk_details_info_get(self):
        """
        Get disk details information.
        """

        # Get selected disk name and pci.ids file content
        selected_disk = self.selected_disk

        disk_sector_size = Performance.disk_sector_size

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        performance_disk_data_precision = Config.performance_disk_data_precision
        performance_disk_data_unit = Config.performance_disk_data_unit
        disk_list = Performance.disk_list

        # Get information.
        disk_type = Disk.disk_type_func(selected_disk)
        disk_parent_name = Disk.disk_parent_name_func(selected_disk, disk_type, disk_list)
        disk_file_system_information = Disk.disk_file_system_information_func(disk_list)
        disk_file_system, disk_capacity, disk_used, disk_free, disk_usage_percentage, disk_mount_point  = Disk.disk_file_system_capacity_used_free_used_percent_mount_point_func(disk_file_system_information, disk_list, selected_disk)
        if disk_file_system  == "fuseblk":
            disk_file_system = Disk.disk_file_system_fuseblk_func(selected_disk)
        disk_if_system_disk = Disk.disk_if_system_disk_func(selected_disk)
        disk_capacity_mass_storage = Disk.disk_capacity_mass_storage_func(selected_disk, disk_mount_point, disk_sector_size)
        disk_device_model_name = Disk.disk_device_model_name_func(selected_disk, disk_type, disk_parent_name)
        disk_label = Disk.disk_label_func(selected_disk)

        # Set Disk Details window title
        self.disk_details_window.set_title(_tr("Disk") + ": " + selected_disk)

        # Set label text by using storage/disk data
        self.disk_details_disk_label.set_label(selected_disk)
        self.disk_details_parent_disk_label.set_label(disk_parent_name)
        self.disk_details_system_disk_label.set_label(disk_if_system_disk)
        self.disk_details_disk_type_label.set_label(disk_type)
        self.disk_details_file_system_label.set_label(disk_file_system)
        self.disk_details_capacity_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", disk_capacity_mass_storage, performance_disk_data_unit, performance_disk_data_precision)}')
        self.disk_details_capacity_mass_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", disk_capacity, performance_disk_data_unit, performance_disk_data_precision)}')
        self.disk_details_free_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", disk_free, performance_disk_data_unit, performance_disk_data_precision)}')
        self.disk_details_used_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", disk_used, performance_disk_data_unit, performance_disk_data_precision)} - {disk_usage_percentage:.0f}%')
        self.disk_details_vendor_model_label.set_label(disk_device_model_name)
        self.disk_details_label_fs_label.set_label(disk_label)
        self.disk_details_mount_point_label.set_label(disk_mount_point)


    def disk_details_update(self, *args):
        """
        Update swap memory information on the swap details window.
        """

        if self.disk_details_window.get_visible() == True:
            # Destroy GLib source for preventing it repeating the function.
            try:
                self.main_glib_source.destroy()
            # Prevent errors if this is first run of the function.
            except AttributeError:
                pass
            self.main_glib_source = GLib.timeout_source_new(Config.update_interval * 1000)
            self.disk_details_info_get()
            self.main_glib_source.set_callback(self.disk_details_update)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed.
            # A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


    # ----------------------------------- Disk - Initial Function -----------------------------------
    def disk_initial_func(self):

        disk_list = Performance.disk_list
        selected_disk_number = Performance.selected_disk_number
        selected_disk = disk_list[selected_disk_number]
        # Definition to access to this variable from "DiskDetails" module.
        self.selected_disk = selected_disk

        # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
        try:
            check_value = "/sys/class/block/" + selected_disk
        except Exception:
            return

        # Get information.
        disk_type = self.disk_type_func(selected_disk)
        disk_parent_name = self.disk_parent_name_func(selected_disk, disk_type, disk_list)
        disk_device_model_name = self.disk_device_model_name_func(selected_disk, disk_type, disk_parent_name)
        if_system_disk = self.disk_if_system_disk_func(selected_disk)


        # Show information on labels.
        self.device_vendor_model_label.set_text(disk_device_model_name)
        self.device_kernel_name_label.set_text(f'{selected_disk}  ({disk_type})')
        self.disk_system_disk_label.set_text(if_system_disk)

        self.initial_already_run = 1


    # ----------------------------------- Disk - Get Disk Data Function -----------------------------------
    def disk_loop_func(self):

        disk_list = Performance.disk_list
        selected_disk_number = Performance.selected_disk_number
        selected_disk = disk_list[selected_disk_number]
        disk_sector_size = Performance.disk_sector_size

        # Run "disk_initial_func" if selected disk is changed since the last loop.
        try:                                                                                      
            if self.selected_disk_prev != selected_disk:
                self.disk_initial_func()
        # try-except is used in order to avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.selected_disk_prev = selected_disk

        disk_read_speed = Performance.disk_read_speed
        disk_write_speed = Performance.disk_write_speed

        performance_disk_data_precision = Config.performance_disk_data_precision
        performance_disk_data_unit = Config.performance_disk_data_unit
        performance_disk_speed_bit = Config.performance_disk_speed_bit

        self.da_disk_speed.queue_draw()
        self.da_disk_usage.queue_draw()

        # Run "main_gui_device_selection_list" if selected device list is changed since the last loop.
        disk_list_system_ordered = Performance.disk_list_system_ordered
        try:                                                                                      
            if self.disk_list_system_ordered_prev != disk_list_system_ordered:
                MainWindow.main_gui_device_selection_list()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list" if this is first loop of the function.
        except AttributeError:
            pass
        self.disk_list_system_ordered_prev = disk_list_system_ordered

        # Run "main_gui_device_selection_list" if "hide_loop_ramdisk_zram_disks" option is changed since the last loop.
        hide_loop_ramdisk_zram_disks = Config.hide_loop_ramdisk_zram_disks
        try:                                                                                      
            if self.hide_loop_ramdisk_zram_disks_prev != hide_loop_ramdisk_zram_disks:
                MainWindow.main_gui_device_selection_list()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list" if this is first loop of the function.
        except AttributeError:
            pass
        self.hide_loop_ramdisk_zram_disks_prev = hide_loop_ramdisk_zram_disks

        # Update disk usage percentages on disk list between Performance tab sub-tabs.
        self.disk_update_disk_usage_percentages_on_disk_list_func()

        # Check if disk exists in the disk list and if disk directory exists in order to prevent errors when disk is removed suddenly when the same disk is selected on the GUI. This error occurs because foreground thread and background thread are different for performance monitoring. Tracking of disk list changes is performed by background thread and there may be a time difference between these two threads. This situtation may cause errors when viewed list is removed suddenly. There may be a better way for preventing these errors/fixing this problem.
        try:
            if os.path.isdir("/sys/class/block/" + selected_disk) == False:
                return
        except Exception:
            return


        # Get information.
        disk_read_data, disk_write_data = self.disk_read_write_data_func(selected_disk, disk_list)
        disk_file_system_information = self.disk_file_system_information_func(disk_list)
        disk_file_system, disk_capacity, disk_used, disk_free, self.disk_usage_percentage, disk_mount_point  = self.disk_file_system_capacity_used_free_used_percent_mount_point_func(disk_file_system_information, disk_list, selected_disk)


        # Show information on labels.
        self.disk_read_speed_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", performance_disk_speed_bit, disk_read_speed[selected_disk_number][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.disk_write_speed_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", performance_disk_speed_bit, disk_write_speed[selected_disk_number][-1], performance_disk_data_unit, performance_disk_data_precision)}/s')
        self.disk_read_data_label.set_text(Performance.performance_data_unit_converter_func("data", "none", disk_read_data, performance_disk_data_unit, performance_disk_data_precision))
        self.disk_write_data_label.set_text(Performance.performance_data_unit_converter_func("data", "none", disk_write_data, performance_disk_data_unit, performance_disk_data_precision))
        if disk_mount_point != "-":
            self.disk_used_percent_label.set_text(f'{self.disk_usage_percentage:.0f}%')
        if disk_mount_point == "-":
            self.disk_used_percent_label.set_text("-%")
        self.disk_free_label.set_text(Performance.performance_data_unit_converter_func("data", "none", disk_free, performance_disk_data_unit, performance_disk_data_precision))
        self.disk_used_label.set_text(Performance.performance_data_unit_converter_func("data", "none", disk_used, performance_disk_data_unit, performance_disk_data_precision))
        self.disk_capacity_label.set_text(Performance.performance_data_unit_converter_func("data", "none", disk_capacity, performance_disk_data_unit, performance_disk_data_precision))


    # ----------------------- Get disk type (Disk or Partition) -----------------------
    def disk_type_func(self, selected_disk):

        with open("/sys/class/block/" + selected_disk + "/uevent") as reader:
            sys_class_block_disk_uevent_lines = reader.read().split("\n")

        for line in sys_class_block_disk_uevent_lines:
            if "DEVTYPE" in line:
                disk_type = _tr(line.split("=")[1].capitalize())
                break

        return disk_type


    # ----------------------- Get disk parent name -----------------------
    def disk_parent_name_func(self, selected_disk, disk_type, disk_list):

        disk_parent_name = "-"
        if disk_type == _tr("Partition"):
            for check_disk_dir in disk_list:
                if os.path.isdir("/sys/class/block/" + check_disk_dir + "/" + selected_disk) == True:
                    disk_parent_name = check_disk_dir

        return disk_parent_name


    # ----------------------- Get disk vendor and model -----------------------
    def disk_device_model_name_func(self, selected_disk, disk_type, disk_parent_name):

        if disk_type == _tr("Disk"):
            disk_or_parent_disk_name = selected_disk
        if disk_type == _tr("Partition"):
            disk_or_parent_disk_name = disk_parent_name

        # Get disk vendor and model.
        device_vendor_name = "-"
        device_model_name = "-"
        # Try to get device vendor model if this is a NVMe SSD. These disks do not have "modalias" or "model" files under "/sys/class/block/" + selected_disk + "/device" directory.
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/device/modalias") as reader:
                modalias_output = reader.read().strip()
            device_vendor_name, device_model_name, _, _ = Performance.performance_get_device_vendor_model_func(modalias_output)
        except (FileNotFoundError, NotADirectoryError) as me:
            pass
        # Try to get device vendor model if this is a SCSI, IDE or virtio device (on QEMU virtual machines).
        try:
            with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/modalias") as reader:
                modalias_output = reader.read().strip()
            device_vendor_name, device_model_name, _, _ = Performance.performance_get_device_vendor_model_func(modalias_output)
        except (FileNotFoundError, NotADirectoryError) as me:
            pass
        # Try to get device vendor model if this is a SCSI or IDE disk.
        if device_vendor_name == "[scsi_or_ide_disk]":
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/vendor") as reader:
                    device_vendor_name = reader.read().strip()
            except (FileNotFoundError, NotADirectoryError) as me:
                device_vendor_name = "Unknown"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/model") as reader:
                    device_model_name = reader.read().strip()
            except (FileNotFoundError, NotADirectoryError) as me:
                device_model_name = "Unknown"
        if device_vendor_name == "Unknown":
            device_vendor_name = "[" + _tr("Unknown") + "]"
        if device_model_name == "Unknown":
            device_model_name = "[" + _tr("Unknown") + "]"
        disk_device_model_name = f'{device_vendor_name} - {device_model_name}'
        # Get disk vendor and model if disk is loop device or swap disk.
        if selected_disk.startswith("loop"):
            disk_device_model_name = "[Loop Device]"
        if selected_disk.startswith("zram"):
            disk_device_model_name = "[" + _tr("Swap").upper() + "]"
        if selected_disk.startswith("ram"):
            disk_device_model_name = "[Ramdisk]"
        if selected_disk.startswith("dm-"):
            disk_device_model_name = "[Device Mapper]"
        if selected_disk.startswith("mmcblk"):
            # Read database file for MMC disk register values. For more info about CIDs: https://www.kernel.org/doc/Documentation/mmc/mmc-dev-attrs.txt
            with open(os.path.dirname(os.path.realpath(__file__)) + "/../database/sdcard.ids") as reader:
                ids_file_output = reader.read().strip()
            # Get device vendor, model names from device ID file content.
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/manfid") as reader:
                    disk_vendor_manfid = reader.read().strip()
                search_text1 = "MANFID " + disk_vendor_manfid.split("0x", 1)[-1]
                if search_text1 in ids_file_output:
                    disk_vendor = ids_file_output.split(search_text1, 1)[1].split("\n", 1)[0].strip()
                else:
                    disk_vendor = "-"
            except Exception:
                disk_vendor = "-"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/name") as reader:
                    disk_name = reader.read().strip()
                disk_model = disk_name
            except FileNotFoundError:
                disk_model = "-"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/type") as reader:
                    disk_card_type = reader.read().strip()
            except FileNotFoundError:
                disk_card_type = "-"
            try:
                with open("/sys/class/block/" + disk_or_parent_disk_name + "/device/speed_class") as reader:
                    disk_card_speed_class = reader.read().strip()
            except FileNotFoundError:
                disk_card_speed_class = "-"
            disk_device_model_name = f'{disk_vendor} - {disk_model} ({disk_card_type} Card, Class {disk_card_speed_class})'

        return disk_device_model_name


    # ----------------------- Get file system information (file systems, capacities, used, free, used percentages and mount points) of all disks -----------------------
    def disk_file_system_information_func(self, disk_list):

        # Get file system information of the mounted disks by using "df" command.
        command_list = ["df", "--output=source,fstype,size,used,avail,pcent,target"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list

        df_output_lines = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split("\n")

        # Remove command output title line. Only disk information will be left.
        del df_output_lines[0]

        # Get mounted disk list.
        mounted_disk_list = []
        for line in df_output_lines:
            disk_name = line.split()[0]
            mounted_disk_list.append(disk_name.split("/dev/")[-1])

        # Get file system information of the mounted and unmounted disks.
        disk_filesystem_information_list = []
        for disk in disk_list:
            if disk in mounted_disk_list:
                index = mounted_disk_list.index(disk)
                disk_file_system = df_output_lines[index].split()[1]
                disk_capacity = int(df_output_lines[index].split()[2]) * 1024
                disk_used = int(df_output_lines[index].split()[3]) * 1024
                disk_free = int(df_output_lines[index].split()[4]) * 1024
                disk_used_percentage = int(df_output_lines[index].split()[5].strip("%"))
                disk_mount_point = df_output_lines[index].split("% ", 1)[-1]
            else:
                disk_file_system = "[" + _tr("Not mounted") + "]"
                disk_capacity = "[" + _tr("Not mounted") + "]"
                disk_used = "[" + _tr("Not mounted") + "]"
                disk_free = "[" + _tr("Not mounted") + "]"
                disk_used_percentage = 0
                disk_mount_point = "[" + _tr("Not mounted") + "]"
            disk_filesystem_information_list.append([disk, disk_file_system, disk_capacity, disk_used, disk_free, disk_used_percentage, disk_mount_point])

        return disk_filesystem_information_list


    # ----------------------- Get file file systems, capacities, used, free, used percentages and mount points of all disks -----------------------
    def disk_file_system_capacity_used_free_used_percent_mount_point_func(self, disk_filesystem_information_list, disk_list, selected_disk):

        disk_index = disk_list.index(selected_disk)
        disk_file_system = disk_filesystem_information_list[disk_index][1]
        disk_capacity = disk_filesystem_information_list[disk_index][2]
        disk_used = disk_filesystem_information_list[disk_index][3]
        disk_free = disk_filesystem_information_list[disk_index][4]
        disk_usage_percentage = disk_filesystem_information_list[disk_index][5]
        disk_mount_point = disk_filesystem_information_list[disk_index][6]

        return disk_file_system, disk_capacity, disk_used, disk_free, disk_usage_percentage, disk_mount_point


    # ----------------------- Get disk mount point -----------------------
    def disk_mount_point_func(self, selected_disk):

        with open("/proc/mounts") as reader:
            proc_mounts_output = reader.read().strip()
        self.proc_mounts_output_lines = proc_mounts_output.split("\n")

        disk_mount_point = "-"
        disk_mount_point_list_scratch = []
        for line in self.proc_mounts_output_lines:
            line_split = line.split()
            if line_split[0].split("/")[-1] == selected_disk:
                # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                disk_mount_point_list_scratch.append(bytes(line_split[1], "utf-8").decode("unicode_escape"))

        if len(disk_mount_point_list_scratch) == 1:
            disk_mount_point = disk_mount_point_list_scratch[0]

        # System disk is listed twice with different mountpoints on some systems (such as systems use btrfs filsystem or chroot). "/" mountpoint information is used.
        if len(disk_mount_point_list_scratch) > 1 and "/" in disk_mount_point_list_scratch:
            disk_mount_point = "/"

        # System disks on some devices such as ARM devices may not be listed in "/proc/mounts" file.
        if disk_mount_point == "-":
            system_disk = "-"
            with open("/proc/cmdline") as reader:
                proc_cmdline = reader.read()
            if "root=UUID=" in proc_cmdline:
                disk_uuid_partuuid = proc_cmdline.split("root=UUID=", 1)[1].split(" ", 1)[0].strip()
                system_disk = os.path.realpath(f'/dev/disk/by-uuid/{disk_uuid_partuuid}').split("/")[-1].strip()
            if "root=PARTUUID=" in proc_cmdline:
                disk_uuid_partuuid = proc_cmdline.split("root=PARTUUID=", 1)[1].split(" ", 1)[0].strip()
                system_disk = os.path.realpath(f'/dev/disk/by-partuuid/{disk_uuid_partuuid}').split("/")[-1].strip()
            if system_disk != "-" and system_disk == selected_disk:
                if "/dev/root / " in proc_mounts_output:
                    disk_mount_point = "/"

        return disk_mount_point


    # ----------------------- Get disk file system if it is detected as 'fuseblk'. -----------------------
    def disk_file_system_fuseblk_func(self, selected_disk):

        # Try to get actual file system by using "lsblk" tool if file system
        # has been get as "fuseblk" (this happens for USB drives). Because "/proc/mounts"
        # file contains file system information as in user space. To be able to get the
        # actual file system, root access is needed for reading from some files or 
        # "lsblk" tool could be used.
        try:
            disk_for_file_system = "/dev/" + selected_disk
            if Config.environment_type == "flatpak":
                disk_file_system = (subprocess.check_output(["flatpak-spawn", "--host", "lsblk", "-no", "FSTYPE", disk_for_file_system], shell=False)).decode().strip()
            else:
                disk_file_system = (subprocess.check_output(["lsblk", "-no", "FSTYPE", disk_for_file_system], shell=False)).decode().strip()
        except Exception:
            disk_file_system = "fuseblk"

        return disk_file_system


    # ----------------------- Get if system disk -----------------------
    def disk_if_system_disk_func(self, selected_disk):

        if selected_disk in Performance.system_disk_list:
            if_system_disk = _tr("Yes")
        else:
            if_system_disk = _tr("No")

        return if_system_disk


    # ----------------------- Get disk read data and disk write data -----------------------
    def disk_read_write_data_func(self, selected_disk, disk_list):

        disk_read_data = Performance.disk_read_data[disk_list.index(selected_disk)]
        disk_write_data = Performance.disk_write_data[disk_list.index(selected_disk)]

        return disk_read_data, disk_write_data


    # ----------------------- Get disk capacity (mass storage) -----------------------
    def disk_capacity_mass_storage_func(self, selected_disk, disk_mount_point, disk_sector_size):

        with open("/sys/class/block/" + selected_disk + "/size") as reader:
            disk_capacity_mass_storage = int(reader.read()) * disk_sector_size

        return disk_capacity_mass_storage


    # ----------------------- Get disk label -----------------------
    def disk_label_func(self, selected_disk):

        disk_label = "-"
        try:
            disk_label_list = os.listdir("/dev/disk/by-label/")
            for label in disk_label_list:
                if os.path.realpath("/dev/disk/by-label/" + label).split("/")[-1] == selected_disk:
                    # String is decoded in order to convert string with escape characters such as "\\040" if they exist.
                    disk_label = bytes(label, "utf-8").decode("unicode_escape")
        except FileNotFoundError:
            pass

        return disk_label


    # ----------------------- Update disk usage percentages on disk list between Performance tab sub-tabs -----------------------
    def disk_update_disk_usage_percentages_on_disk_list_func(self):

        # Get disk usage percentages.
        device_list = Performance.disk_list_system_ordered
        disk_usage_percentage_list = []
        for device in device_list:
            disk_filesystem_information_list = self.disk_file_system_information_func(device_list)
            _, _, _, _, disk_usage_percentage, disk_mount_point = self.disk_file_system_capacity_used_free_used_percent_mount_point_func(disk_filesystem_information_list, device_list, device)
            # Append percentage number with no fractions in order to avoid updating the list very frequently.
            disk_usage_percentage_list.append(f'{disk_usage_percentage:.0f}')

        # Update disk usage percentages on disk list if disk usage percentages are changed since the last loop.
        try:                                                                                      
            if self.disk_usage_percentage_list_prev != disk_usage_percentage_list:
                MainWindow.main_gui_device_selection_list()
        # try-except is used in order to avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.disk_usage_percentage_list_prev = disk_usage_percentage_list


Disk = Disk()


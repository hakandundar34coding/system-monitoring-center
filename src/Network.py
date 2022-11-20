#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, Pango

import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from MainWindow import MainWindow


class Network:

    def __init__(self):

        # Network tab GUI
        self.network_tab_gui()

        # "0" value of "initial_already_run" variable means that initial function is not run before or
        # tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    def network_tab_gui(self):
        """
        Generate Network tab GUI.
        """

        # Network tab grid
        self.network_tab_grid = Gtk.Grid()
        self.network_tab_grid.set_row_spacing(10)
        self.network_tab_grid.set_margin_top(2)
        self.network_tab_grid.set_margin_bottom(2)
        self.network_tab_grid.set_margin_start(2)
        self.network_tab_grid.set_margin_end(2)

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
        self.network_gui_label_grid()

        # Drawingarea and related information labels
        self.network_gui_da_grid()

        # Performance information labels
        self.network_gui_performance_info_grid()

        # Connect signals
        self.network_gui_signals()


    def network_gui_label_grid(self):
        """
        Generate tab name, device name labels.
        """

        # Tab name label grid
        tab_name_label_grid = Gtk.Grid()
        self.network_tab_grid.attach(tab_name_label_grid, 0, 0, 1, 1)

        # Tab name label
        tab_name_label = Gtk.Label()
        tab_name_label.set_halign(Gtk.Align.START)
        tab_name_label.set_margin_end(60)
        tab_name_label.set_attributes(self.attribute_list_bold_2x)
        tab_name_label.set_label(_tr("Network"))
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


    def network_gui_da_grid(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Drawingarea grid
        da_network_speed_grid = Gtk.Grid()
        da_network_speed_grid.set_hexpand(True)
        da_network_speed_grid.set_vexpand(True)
        self.network_tab_grid.attach(da_network_speed_grid, 0, 1, 1, 1)

        # Drawingarea upper-left label
        da_upper_left_label = Gtk.Label()
        da_upper_left_label.set_halign(Gtk.Align.START)
        da_upper_left_label.set_label(_tr("Read Speed") + " (-) & " + _tr("Write Speed") + " (-  -)")
        da_network_speed_grid.attach(da_upper_left_label, 0, 0, 1, 1)

        # Drawingarea upper-right label
        self.da_upper_right_label = Gtk.Label()
        self.da_upper_right_label.set_halign(Gtk.Align.END)
        self.da_upper_right_label.set_label("--")
        da_network_speed_grid.attach(self.da_upper_right_label, 1, 0, 1, 1)

        # Drawingarea
        self.da_network_speed = Gtk.DrawingArea()
        self.da_network_speed.set_hexpand(True)
        self.da_network_speed.set_vexpand(True)
        da_network_speed_grid.attach(self.da_network_speed, 0, 2, 2, 1)

        # Drawingarea lower-right label
        da_lower_right_label = Gtk.Label()
        da_lower_right_label.set_halign(Gtk.Align.END)
        da_lower_right_label.set_label("0")
        da_network_speed_grid.attach(da_lower_right_label, 0, 3, 2, 1)


    def network_gui_performance_info_grid(self):
        """
        Generate performance information labels.
        """

        # Performance information labels grid
        performance_info_grid = Gtk.Grid()
        performance_info_grid.set_column_homogeneous(True)
        performance_info_grid.set_row_homogeneous(True)
        performance_info_grid.set_column_spacing(12)
        performance_info_grid.set_row_spacing(10)
        self.network_tab_grid.attach(performance_info_grid, 0, 2, 1, 1)

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
        label.set_label(_tr("Download Speed"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Upload Speed"))
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
        # Styled information label (Download Speed)
        self.network_download_speed_label = Gtk.Label()
        self.network_download_speed_label.set_selectable(True)
        self.network_download_speed_label.set_attributes(self.attribute_list_bold)
        self.network_download_speed_label.set_label("--")
        self.network_download_speed_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.network_download_speed_label, 0, 2, 1, 1)
        # Styled information label (Upload Speed)
        self.network_upload_speed_label = Gtk.Label()
        self.network_upload_speed_label.set_selectable(True)
        self.network_upload_speed_label.set_attributes(self.attribute_list_bold)
        self.network_upload_speed_label.set_label("--")
        self.network_upload_speed_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.network_upload_speed_label, 1, 2, 1, 1)

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
        label.set_label(_tr("Download Data"))
        label.set_tooltip_text(_tr("Measured value since last system start"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Styled information label
        label = Gtk.Label()
        label.set_label(_tr("Upload Data"))
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
        # Styled information label (Download Data)
        self.network_download_data_label = Gtk.Label()
        self.network_download_data_label.set_selectable(True)
        self.network_download_data_label.set_attributes(self.attribute_list_bold)
        self.network_download_data_label.set_label("--")
        self.network_download_data_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.network_download_data_label, 0, 2, 1, 1)
        # Styled information label (Upload Data)
        self.network_upload_data_label = Gtk.Label()
        self.network_upload_data_label.set_selectable(True)
        self.network_upload_data_label.set_attributes(self.attribute_list_bold)
        self.network_upload_data_label.set_label("--")
        self.network_upload_data_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.network_upload_data_label, 1, 2, 1, 1)

        # Right information label grid
        performance_info_right_grid = Gtk.Grid()
        performance_info_right_grid.set_column_homogeneous(True)
        performance_info_right_grid.set_row_homogeneous(True)
        performance_info_right_grid.set_column_spacing(2)
        performance_info_right_grid.set_row_spacing(4)
        performance_info_grid.attach(performance_info_right_grid, 1, 0, 1, 2)

        # Right information labels
        # Right information label (Connection Type)
        label = Gtk.Label()
        label.set_label(_tr("Connection Type") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 0, 1, 1)

        # Right information label (Connection Type)
        self.network_connection_type_label = Gtk.Label()
        self.network_connection_type_label.set_selectable(True)
        self.network_connection_type_label.set_attributes(self.attribute_list_bold)
        self.network_connection_type_label.set_label("--")
        self.network_connection_type_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.network_connection_type_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.network_connection_type_label, 1, 0, 1, 1)

        # Right information label (Connected-SSID)
        label = Gtk.Label()
        label.set_label(_tr("Connected-SSID") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 1, 1, 1)

        # Right information label (Connected-SSID)
        self.network_connected_ssid_label = Gtk.Label()
        self.network_connected_ssid_label.set_selectable(True)
        self.network_connected_ssid_label.set_attributes(self.attribute_list_bold)
        self.network_connected_ssid_label.set_label("--")
        self.network_connected_ssid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.network_connected_ssid_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.network_connected_ssid_label, 1, 1, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("Link Quality") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 2, 1, 1)

        # Right information label (Link Quality))
        self.network_link_quality_label = Gtk.Label()
        self.network_link_quality_label.set_selectable(True)
        self.network_link_quality_label.set_attributes(self.attribute_list_bold)
        self.network_link_quality_label.set_label("--")
        self.network_link_quality_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.network_link_quality_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.network_link_quality_label, 1, 2, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("IPv4 Address") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 3, 1, 1)

        # Right information label (IPv4 Address)
        self.network_ipv4_address_label = Gtk.Label()
        self.network_ipv4_address_label.set_selectable(True)
        self.network_ipv4_address_label.set_attributes(self.attribute_list_bold)
        self.network_ipv4_address_label.set_label("--")
        self.network_ipv4_address_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.network_ipv4_address_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.network_ipv4_address_label, 1, 3, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("IPv6 Address") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 4, 1, 1)

        # Right information label (IPv6 Address)
        self.network_ipv6_address_label = Gtk.Label()
        self.network_ipv6_address_label.set_selectable(True)
        self.network_ipv6_address_label.set_attributes(self.attribute_list_bold)
        self.network_ipv6_address_label.set_label("--")
        self.network_ipv6_address_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.network_ipv6_address_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.network_ipv6_address_label, 1, 4, 1, 1)

        label = Gtk.Label()
        label.set_label(_tr("MAC Address") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 5, 1, 1)

        # Right information label (MAC Address)
        self.network_mac_address_label = Gtk.Label()
        self.network_mac_address_label.set_selectable(True)
        self.network_mac_address_label.set_attributes(self.attribute_list_bold)
        self.network_mac_address_label.set_label("--")
        self.network_mac_address_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.network_mac_address_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.network_mac_address_label, 1, 5, 1, 1)


    def network_gui_signals(self):
        """
        Connect GUI signals.
        """

        self.da_network_speed.set_draw_func(Performance.performance_line_charts_draw_func, "da_network_speed")

        # Drawingarea mouse events
        drawing_area_mouse_event = Gtk.EventControllerMotion()
        drawing_area_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawing_area_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawing_area_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        self.da_network_speed.add_controller(drawing_area_mouse_event)


    # ----------------------------------- Network - Initial Function -----------------------------------
    def network_initial_func(self):

        network_card_list = Performance.network_card_list
        selected_network_card_number = Performance.selected_network_card_number
        selected_network_card = network_card_list[selected_network_card_number]


        # Get information.
        network_card_device_model_name = self.network_device_model_name_func(selected_network_card)
        connection_type = self.network_connection_type_func(selected_network_card)
        network_card_mac_address = self.network_card_mac_address_func(selected_network_card)
        network_address_ipv4, network_address_ipv6 = self.network_address_ipv4_ipv6_func(selected_network_card)


        # Set Network tab label texts by using information get
        self.device_vendor_model_label.set_text(network_card_device_model_name)
        self.device_kernel_name_label.set_text(selected_network_card)
        self.network_connection_type_label.set_text(connection_type)
        self.network_ipv4_address_label.set_text(network_address_ipv4)
        self.network_ipv6_address_label.set_text(network_address_ipv6)
        self.network_mac_address_label.set_text(network_card_mac_address)

        self.initial_already_run = 1


    # ----------------------------------- Network - Initial Function -----------------------------------
    def network_loop_func(self):

        network_card_list = Performance.network_card_list
        selected_network_card_number = Performance.selected_network_card_number
        selected_network_card = network_card_list[selected_network_card_number]

        # Run "network_initial_func" if selected network card is changed since the last loop.
        try:
            if self.selected_network_card_prev != selected_network_card:
                self.network_initial_func()
        # Avoid errors if this is first loop of the function.
        except AttributeError:
            pass
        self.selected_network_card_prev = selected_network_card

        network_receive_speed = Performance.network_receive_speed
        network_send_speed = Performance.network_send_speed
        network_receive_bytes = Performance.network_receive_bytes
        network_send_bytes = Performance.network_send_bytes

        performance_network_data_precision = Config.performance_network_data_precision
        performance_network_data_unit = Config.performance_network_data_unit
        performance_network_speed_bit = Config.performance_network_speed_bit

        self.da_network_speed.queue_draw()

        # Run "main_gui_device_selection_list_func" if selected device list is changed since the last loop.
        network_card_list_system_ordered = Performance.network_card_list_system_ordered
        try:                                                                                      
            if self.network_card_list_system_ordered_prev != network_card_list_system_ordered:
                MainWindow.main_gui_device_selection_list_func()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list_func" if this is first loop of the function.
        except AttributeError:
            pass
        self.network_card_list_system_ordered_prev = network_card_list_system_ordered


        # Get information.
        network_card_connected = self.network_card_connected_func(selected_network_card)
        network_ssid = self.network_ssid_func(selected_network_card)
        network_link_quality = self.network_link_quality_func(selected_network_card, network_card_connected)


        # Set and update Network tab label texts by using information get
        self.network_download_speed_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", performance_network_speed_bit, network_receive_speed[selected_network_card_number][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.network_upload_speed_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", performance_network_speed_bit, network_send_speed[selected_network_card_number][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.network_download_data_label.set_text(Performance.performance_data_unit_converter_func("data", "none", network_receive_bytes[selected_network_card_number], performance_network_data_unit, performance_network_data_precision))
        self.network_upload_data_label.set_text(Performance.performance_data_unit_converter_func("data", "none", network_send_bytes[selected_network_card_number], performance_network_data_unit, performance_network_data_precision))
        self.network_connected_ssid_label.set_text(f'{network_card_connected} - {network_ssid}')
        self.network_link_quality_label.set_text(network_link_quality)


    # ----------------------- Get network card vendor and model -----------------------
    def network_device_model_name_func(self, selected_network_card):

        # Get device vendor and model names
        device_vendor_name = "-"
        device_model_name = "-"
        # Get device vendor and model names if it is not a virtual device.
        if os.path.isdir("/sys/devices/virtual/net/" + selected_network_card) == False:
            # Check if there is a "modalias" file. Some network interfaces (such as usb0, usb1, etc.) may not have this file.
            if os.path.isfile("/sys/class/net/" + selected_network_card + "/device/modalias") == True:
                # Read device vendor and model ids by reading "modalias" file.
                with open("/sys/class/net/" + selected_network_card + "/device/modalias") as reader:
                    modalias_output = reader.read().strip()
                device_vendor_name, device_model_name, _, _ = Performance.performance_get_device_vendor_model_func(modalias_output)
                if device_vendor_name == "Unknown":
                    device_vendor_name = "[" + _tr("Unknown") + "]"
                if device_model_name == "Unknown":
                    device_model_name = "[" + _tr("Unknown") + "]"
            network_card_device_model_name = f'{device_vendor_name} - {device_model_name}'
        # Get device vendor and model names if it is a virtual device.
        else:
            # lo (Loopback Device) is a system device and it is not a physical device. It could not be found in "pci.ids" file.
            if selected_network_card == "lo":
                network_card_device_model_name = "Loopback Device"
            else:
                network_card_device_model_name = "[" + _tr("Virtual Network Interface") + "]"

        return network_card_device_model_name


    # ----------------------- Get network card connection type -----------------------
    def network_connection_type_func(self, selected_network_card):

        if selected_network_card.startswith("en"):
            connection_type = _tr("Ethernet")
        elif selected_network_card.startswith("wl"):
            connection_type = _tr("Wi-Fi")
        else:
            connection_type = "-"

        return connection_type


    # ----------------------- Get network card MAC address -----------------------
    def network_card_mac_address_func(self, selected_network_card):

        try:
            with open("/sys/class/net/" + selected_network_card + "/address") as reader:
                network_card_mac_address = reader.read().strip().upper()
        # Some network interfaces (such as some of the virtual network interfaces) may not have a MAC address.
        except FileNotFoundError:
            network_card_mac_address = "-"

        return network_card_mac_address


    # ----------------------- Get network card IPv4 and IPv6 addresses -----------------------
    def network_address_ipv4_ipv6_func(self, selected_network_card):

        try:
            ip_output = (subprocess.check_output(["ip", "a", "show", selected_network_card], shell=False)).decode()
        # "ip" program is in "/sbin/" on some systems (such as Slackware based distributions).
        except FileNotFoundError:
            ip_output = (subprocess.check_output(["/sbin/ip", "a", "show", selected_network_card], shell=False)).decode()
        ip_output_lines = ip_output.strip().split("\n")
        network_address_ipv4 = "-"
        network_address_ipv6 = "-"
        for line in ip_output_lines:
            if "inet " in line:
                network_address_ipv4 = line.split()[1].split("/")[0]
            if "inet6 " in line:
                network_address_ipv6 = line.split()[1].split("/")[0]

        return network_address_ipv4, network_address_ipv6


    # ----------------------- Get network card connected information -----------------------
    def network_card_connected_func(self, selected_network_card):

        with open("/sys/class/net/" + selected_network_card + "/operstate") as reader:
            network_info = reader.read().strip()
        if network_info == "up":
            network_card_connected = _tr("Yes")
        elif network_info == "down":
            network_card_connected = _tr("No")
        elif network_info == "unknown":
            network_card_connected = f'[{_tr("Unknown")}]'
        else:
            network_card_connected = network_info

        return network_card_connected


    # ----------------------- Get network name (SSID) -----------------------
    def network_ssid_func(self, selected_network_card):

        try:                                                                                      
            if Config.environment_type == "flatpak":
                nmcli_output_lines = (subprocess.check_output(["flatpak-spawn", "--host", "nmcli", "-get-values", "DEVICE,CONNECTION", "device", "status"], shell=False)).decode().strip().split("\n")
            else:
                nmcli_output_lines = (subprocess.check_output(["nmcli", "-get-values", "DEVICE,CONNECTION", "device", "status"], shell=False)).decode().strip().split("\n")
        # Avoid errors because Network Manager (which is required for running "nmcli" command) may not be installed on all systems (very rare).
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            network_ssid = f'[{_tr("Unknown")}]'

        # Check if "nmcli_output_lines" value is get.
        if "nmcli_output_lines" in locals():
            for line in nmcli_output_lines:
                line_splitted = line.split(":")
                if selected_network_card == line_splitted[0]:
                    network_ssid = line_splitted[1].strip()
                    break

        # "network_ssid" value is get as "" if selected network card is not connected a Wi-Fi network.
        if network_ssid == "":
            network_ssid = "-"

        return network_ssid


    # ----------------------- Get network signal strength (link value) -----------------------
    def network_link_quality_func(self, selected_network_card, network_card_connected):

        network_link_quality = "-"
        # Translated value have to be used by using gettext constant. Not "Yes".
        if selected_network_card.startswith("wl") == True and network_card_connected == _tr("Yes"):
            with open("/proc/net/wireless") as reader:
                proc_net_wireless_output_lines = reader.read().strip().split("\n")
            for line in proc_net_wireless_output_lines:
                line_splitted = line.split()
                if selected_network_card == line_splitted[0].split(":")[0]:
                    # "split(".")" is used in order to remove "." at the end of the signal value.
                    network_link_quality = line_splitted[2].split(".")[0]
                    if network_link_quality != "-":
                        network_link_quality = f'{network_link_quality} (link)'
                    break

        return network_link_quality


Network = Network()


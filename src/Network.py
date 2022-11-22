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

        # Label (Network)
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        label.set_margin_end(60)
        label.set_attributes(attribute_list_bold_2x)
        label.set_label(_tr("Network"))
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
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        label.set_label(_tr("Read Speed") + " (-) & " + _tr("Write Speed") + " (-  -)")
        grid.attach(label, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        self.da_upper_right_label = Gtk.Label()
        self.da_upper_right_label.set_halign(Gtk.Align.END)
        self.da_upper_right_label.set_label("--")
        grid.attach(self.da_upper_right_label, 1, 0, 1, 1)

        # DrawingArea
        self.da_network_speed = Gtk.DrawingArea()
        self.da_network_speed.set_hexpand(True)
        self.da_network_speed.set_vexpand(True)
        grid.attach(self.da_network_speed, 0, 2, 2, 1)

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

        # Add viewports for showing borders around some the performance data and round the corners of the viewports.
        css = b"viewport {border-style: solid; border-radius: 8px 8px 8px 8px; border-width: 1px 1px 1px 1px; border-color: rgba(50%,50%,50%,0.6);}"
        style_provider_viewport = Gtk.CssProvider()
        style_provider_viewport.load_from_data(css)

        # Add separators for showing lines with contrast colors between some the performance data and set color of the separators.
        css = b"separator {background: rgba(50%,50%,50%,0.6);}"
        style_provider_separator = Gtk.CssProvider()
        style_provider_separator.load_from_data(css)

        # Styled information widgets (Download Speed and Upload Speed)
        # Viewport (Download Speed and Upload Speed)
        viewport = Gtk.Viewport()
        viewport.get_style_context().add_provider(style_provider_viewport, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        performance_info_grid.attach(viewport, 0, 0, 1, 1)
        # Grid (Download Speed and Upload Speed)
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(3)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)
        grid.set_margin_start(5)
        grid.set_margin_end(5)
        grid.set_valign(Gtk.Align.CENTER)
        viewport.set_child(grid)
        # Label (Download Speed)
        label = Gtk.Label()
        label.set_label(_tr("Download Speed"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Label (Upload Speed)
        label = Gtk.Label()
        label.set_label(_tr("Upload Speed"))
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
        # Label (Download Speed)
        self.download_speed_label = Gtk.Label()
        self.download_speed_label.set_selectable(True)
        self.download_speed_label.set_attributes(self.attribute_list_bold)
        self.download_speed_label.set_label("--")
        self.download_speed_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.download_speed_label, 0, 2, 1, 1)
        # Label (Upload Speed)
        self.upload_speed_label = Gtk.Label()
        self.upload_speed_label.set_selectable(True)
        self.upload_speed_label.set_attributes(self.attribute_list_bold)
        self.upload_speed_label.set_label("--")
        self.upload_speed_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.upload_speed_label, 1, 2, 1, 1)

        # Styled information widgets (Download Data and Upload Data)
        # Viewport (Download Data and Upload Data)
        viewport = Gtk.Viewport()
        viewport.get_style_context().add_provider(style_provider_viewport, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        performance_info_grid.attach(viewport, 0, 1, 1, 1)
        # Grid (Download Data and Upload Data)
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_spacing(3)
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)
        grid.set_margin_start(5)
        grid.set_margin_end(5)
        grid.set_valign(Gtk.Align.CENTER)
        viewport.set_child(grid)
        # Label (Download Data)
        label = Gtk.Label()
        label.set_label(_tr("Download Data"))
        label.set_tooltip_text(_tr("Measured value since last system start"))
        label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(label, 0, 0, 1, 1)
        # Label (Upload Data)
        label = Gtk.Label()
        label.set_label(_tr("Upload Data"))
        label.set_tooltip_text(_tr("Measured value since last system start"))
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
        # Label (Download Data)
        self.download_data_label = Gtk.Label()
        self.download_data_label.set_selectable(True)
        self.download_data_label.set_attributes(self.attribute_list_bold)
        self.download_data_label.set_label("--")
        self.download_data_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.download_data_label, 0, 2, 1, 1)
        # Label (Upload Data)
        self.upload_data_label = Gtk.Label()
        self.upload_data_label.set_selectable(True)
        self.upload_data_label.set_attributes(self.attribute_list_bold)
        self.upload_data_label.set_label("--")
        self.upload_data_label.set_ellipsize(Pango.EllipsizeMode.END)
        grid.attach(self.upload_data_label, 1, 2, 1, 1)

        # Grid - Right information labels
        performance_info_right_grid = Gtk.Grid()
        performance_info_right_grid.set_column_homogeneous(True)
        performance_info_right_grid.set_row_homogeneous(True)
        performance_info_right_grid.set_column_spacing(2)
        performance_info_right_grid.set_row_spacing(4)
        performance_info_grid.attach(performance_info_right_grid, 1, 0, 1, 2)

        # Labels - Right information labels
        # Label (Connection Type)
        label = Gtk.Label()
        label.set_label(_tr("Connection Type") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 0, 1, 1)
        # Label (Connection Type)
        self.connection_type_label = Gtk.Label()
        self.connection_type_label.set_selectable(True)
        self.connection_type_label.set_attributes(self.attribute_list_bold)
        self.connection_type_label.set_label("--")
        self.connection_type_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.connection_type_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.connection_type_label, 1, 0, 1, 1)

        # Label (Connected-SSID)
        label = Gtk.Label()
        label.set_label(_tr("Connected-SSID") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 1, 1, 1)
        # Label (Connected-SSID)
        self.connected_ssid_label = Gtk.Label()
        self.connected_ssid_label.set_selectable(True)
        self.connected_ssid_label.set_attributes(self.attribute_list_bold)
        self.connected_ssid_label.set_label("--")
        self.connected_ssid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.connected_ssid_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.connected_ssid_label, 1, 1, 1, 1)

        # Label (Link Quality)
        label = Gtk.Label()
        label.set_label(_tr("Link Quality") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 2, 1, 1)
        # Label (Link Quality)
        self.link_quality_label = Gtk.Label()
        self.link_quality_label.set_selectable(True)
        self.link_quality_label.set_attributes(self.attribute_list_bold)
        self.link_quality_label.set_label("--")
        self.link_quality_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.link_quality_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.link_quality_label, 1, 2, 1, 1)

        # Label (IPv4 Address)
        label = Gtk.Label()
        label.set_label(_tr("IPv4 Address") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 3, 1, 1)
        # Label (IPv4 Address)
        self.ipv4_address_label = Gtk.Label()
        self.ipv4_address_label.set_selectable(True)
        self.ipv4_address_label.set_attributes(self.attribute_list_bold)
        self.ipv4_address_label.set_label("--")
        self.ipv4_address_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.ipv4_address_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.ipv4_address_label, 1, 3, 1, 1)

        # Label (IPv6 Address)
        label = Gtk.Label()
        label.set_label(_tr("IPv6 Address") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 4, 1, 1)
        # Label (IPv6 Address)
        self.ipv6_address_label = Gtk.Label()
        self.ipv6_address_label.set_selectable(True)
        self.ipv6_address_label.set_attributes(self.attribute_list_bold)
        self.ipv6_address_label.set_label("--")
        self.ipv6_address_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.ipv6_address_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.ipv6_address_label, 1, 4, 1, 1)

        # Label (MAC Address)
        label = Gtk.Label()
        label.set_label(_tr("MAC Address") + ":")
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(label, 0, 5, 1, 1)
        # Label (MAC Address)
        self.mac_address_label = Gtk.Label()
        self.mac_address_label.set_selectable(True)
        self.mac_address_label.set_attributes(self.attribute_list_bold)
        self.mac_address_label.set_label("--")
        self.mac_address_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.mac_address_label.set_halign(Gtk.Align.START)
        performance_info_right_grid.attach(self.mac_address_label, 1, 5, 1, 1)


    def connect_signals(self):
        """
        Connect GUI signals.
        """

        self.da_network_speed.set_draw_func(Performance.performance_line_charts_draw_func, "da_network_speed")

        # Drawingarea mouse events
        drawingarea_mouse_event = Gtk.EventControllerMotion()
        drawingarea_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawingarea_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawingarea_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        self.da_network_speed.add_controller(drawingarea_mouse_event)


    def network_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        network_card_list = Performance.network_card_list
        selected_network_card_number = Performance.selected_network_card_number
        selected_network_card = network_card_list[selected_network_card_number]


        # Get information.
        network_card_device_model_name = self.device_model_name_func(selected_network_card)
        connection_type = self.connection_type_func(selected_network_card)
        network_card_mac_address = self.mac_address_func(selected_network_card)
        network_address_ipv4, network_address_ipv6 = self.ipv4_ipv6_address_func(selected_network_card)


        # Set Network tab label texts by using information get
        self.device_vendor_model_label.set_text(network_card_device_model_name)
        self.device_kernel_name_label.set_text(selected_network_card)
        self.connection_type_label.set_text(connection_type)
        self.ipv4_address_label.set_text(network_address_ipv4)
        self.ipv6_address_label.set_text(network_address_ipv6)
        self.mac_address_label.set_text(network_card_mac_address)

        self.initial_already_run = 1


    def network_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

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
        self.download_speed_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", performance_network_speed_bit, network_receive_speed[selected_network_card_number][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.upload_speed_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", performance_network_speed_bit, network_send_speed[selected_network_card_number][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.download_data_label.set_text(Performance.performance_data_unit_converter_func("data", "none", network_receive_bytes[selected_network_card_number], performance_network_data_unit, performance_network_data_precision))
        self.upload_data_label.set_text(Performance.performance_data_unit_converter_func("data", "none", network_send_bytes[selected_network_card_number], performance_network_data_unit, performance_network_data_precision))
        self.connected_ssid_label.set_text(f'{network_card_connected} - {network_ssid}')
        self.link_quality_label.set_text(network_link_quality)


    def device_model_name_func(self, selected_network_card):
        """
        Get network card vendor and model.
        """

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


    def connection_type_func(self, selected_network_card):
        """
        Get connection type on the selected network card.
        """

        if selected_network_card.startswith("en"):
            connection_type = _tr("Ethernet")
        elif selected_network_card.startswith("wl"):
            connection_type = _tr("Wi-Fi")
        else:
            connection_type = "-"

        return connection_type


    def mac_address_func(self, selected_network_card):
        """
        Get network card MAC address.
        """

        try:
            with open("/sys/class/net/" + selected_network_card + "/address") as reader:
                network_card_mac_address = reader.read().strip().upper()
        # Some network interfaces (such as some of the virtual network interfaces) may not have a MAC address.
        except FileNotFoundError:
            network_card_mac_address = "-"

        return network_card_mac_address


    def ipv4_ipv6_address_func(self, selected_network_card):
        """
        Get IPv4 and IPv6 addresses on the selected network card.
        """

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


    def network_card_connected_func(self, selected_network_card):
        """
        Get connected information for the selected network card.
        """

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


    def network_ssid_func(self, selected_network_card):
        """
        Get network name (SSID).
        """

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


    def network_link_quality_func(self, selected_network_card, network_card_connected):
        """
        Get network signal strength (link value).
        """

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


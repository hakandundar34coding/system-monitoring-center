#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os
import subprocess

from locale import gettext as _tr

from Config import Config
from Performance import Performance


# Define class
class Network:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/NetworkTab.ui")

        # Get GUI objects
        self.grid1401 = builder.get_object('grid1401')
        self.drawingarea1401 = builder.get_object('drawingarea1401')
        self.button1401 = builder.get_object('button1401')
        self.label1401 = builder.get_object('label1401')
        self.label1402 = builder.get_object('label1402')
        self.label1403 = builder.get_object('label1403')
        self.label1404 = builder.get_object('label1404')
        self.label1405 = builder.get_object('label1405')
        self.label1406 = builder.get_object('label1406')
        self.label1407 = builder.get_object('label1407')
        self.label1408 = builder.get_object('label1408')
        self.label1409 = builder.get_object('label1409')
        self.label1410 = builder.get_object('label1410')
        self.label1411 = builder.get_object('label1411')
        self.label1412 = builder.get_object('label1412')
        self.label1413 = builder.get_object('label1413')

        # Add viewports for showing borders around some the performance data and round the corners of the viewports.
        css = b"viewport {border-radius: 8px 8px 8px 8px;}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        self.viewport1401 = builder.get_object('viewport1401')
        self.viewport1401.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.viewport1402 = builder.get_object('viewport1402')
        self.viewport1402.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Add separators for showing lines with contrast colors between some the performance data and set color of the separators.
        css = b"separator {background: rgba(50%,50%,50%,0.6);}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        self.separator1401 = builder.get_object('separator1401')
        self.separator1401.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.separator1402 = builder.get_object('separator1402')
        self.separator1402.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.separator1403 = builder.get_object('separator1403')
        self.separator1403.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.separator1404 = builder.get_object('separator1404')
        self.separator1404.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Get chart functions from another module and define as local objects for lower CPU usage.
        self.performance_line_charts_draw_func = Performance.performance_line_charts_draw_func
        self.performance_line_charts_enter_notify_event_func = Performance.performance_line_charts_enter_notify_event_func
        self.performance_line_charts_leave_notify_event_func = Performance.performance_line_charts_leave_notify_event_func
        self.performance_line_charts_motion_notify_event_func = Performance.performance_line_charts_motion_notify_event_func

        # Connect GUI signals
        self.button1401.connect("clicked", self.on_button1401_clicked)
        self.drawingarea1401.connect("draw", self.performance_line_charts_draw_func)
        self.drawingarea1401.connect("enter-notify-event", self.performance_line_charts_enter_notify_event_func)
        self.drawingarea1401.connect("leave-notify-event", self.performance_line_charts_leave_notify_event_func)
        self.drawingarea1401.connect("motion-notify-event", self.performance_line_charts_motion_notify_event_func)

        # Set event masks for drawingarea in order to enable these events.
        self.drawingarea1401.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK | Gdk.EventMask.POINTER_MOTION_MASK)

        # "0" value of "initial_already_run" variable means that initial function is not run before or tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    # ----------------------- "customizations menu" Button -----------------------
    def on_button1401_clicked(self, widget):

        from NetworkMenu import NetworkMenu
        NetworkMenu.popover1401p.set_relative_to(widget)
        NetworkMenu.popover1401p.set_position(1)
        NetworkMenu.popover1401p.popup()


    # ----------------------------------- Network - Initial Function -----------------------------------
    def network_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

        network_card_list = Performance.network_card_list
        selected_network_card_number = Performance.selected_network_card_number
        selected_network_card = network_card_list[selected_network_card_number]


        # Get information.
        network_card_device_model_name = self.network_device_model_name_func(selected_network_card)
        connection_type = self.network_connection_type_func(selected_network_card)
        network_card_mac_address = self.network_card_mac_address_func(selected_network_card)
        network_address_ipv4, network_address_ipv6 = self.network_address_ipv4_ipv6_func(selected_network_card)


        # Set Network tab label texts by using information get
        self.label1401.set_text(network_card_device_model_name)
        self.label1402.set_text(selected_network_card)
        self.label1407.set_text(connection_type)
        self.label1410.set_text(network_address_ipv4)
        self.label1411.set_text(network_address_ipv6)
        self.label1412.set_text(network_card_mac_address)

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

        self.drawingarea1401.queue_draw()

        # Run "main_gui_device_selection_list_func" if selected device list is changed since the last loop.
        network_card_list_system_ordered = Performance.network_card_list_system_ordered
        try:                                                                                      
            if self.network_card_list_system_ordered_prev != network_card_list_system_ordered:
                from MainGUI import MainGUI
                MainGUI.main_gui_device_selection_list_func()
        # try-except is used in order to avoid error and also run "main_gui_device_selection_list_func" if this is first loop of the function.
        except AttributeError:
            pass
        self.network_card_list_system_ordered_prev = network_card_list_system_ordered


        # Get information.
        network_card_connected = self.network_card_connected_func(selected_network_card)
        network_ssid = self.network_ssid_func(selected_network_card)
        network_signal_strength = self.network_signal_strength_func(selected_network_card, network_card_connected)


        # Set and update Network tab label texts by using information get
        self.label1403.set_text(f'{self.performance_data_unit_converter_func("speed", performance_network_speed_bit, network_receive_speed[selected_network_card_number][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.label1404.set_text(f'{self.performance_data_unit_converter_func("speed", performance_network_speed_bit, network_send_speed[selected_network_card_number][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.label1405.set_text(self.performance_data_unit_converter_func("data", "none", network_receive_bytes[selected_network_card_number], performance_network_data_unit, performance_network_data_precision))
        self.label1406.set_text(self.performance_data_unit_converter_func("data", "none", network_send_bytes[selected_network_card_number], performance_network_data_unit, performance_network_data_precision))
        self.label1408.set_text(f'{network_card_connected} - {network_ssid}')
        self.label1409.set_text(network_signal_strength)


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
            nmcli_output_lines = (subprocess.check_output(["nmcli", "-get-values", "DEVICE,CONNECTION", "device", "status"], shell=False)).decode().strip().split("\n")
        # Avoid errors because Network Manager (which is required for running "nmcli" command) may not be installed on all systems (very rare).
        except FileNotFoundError:
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
    def network_signal_strength_func(self, selected_network_card, network_card_connected):

        network_signal_strength = "-"
        # Translated value have to be used by using gettext constant. Not "Yes".
        if selected_network_card.startswith("wl") == True and network_card_connected == _tr("Yes"):
            with open("/proc/net/wireless") as reader:
                proc_net_wireless_output_lines = reader.read().strip().split("\n")
            for line in proc_net_wireless_output_lines:
                line_splitted = line.split()
                if selected_network_card == line_splitted[0].split(":")[0]:
                    # "split(".")" is used in order to remove "." at the end of the signal value.
                    network_signal_strength = line_splitted[2].split(".")[0]
                    if network_signal_strength != "-":
                        network_signal_strength = f'{network_signal_strength} (link)'
                    break

        return network_signal_strength


# Generate object
Network = Network()


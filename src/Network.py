import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import os
import subprocess

from locale import gettext as _tr

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common


class Network:

    def __init__(self):

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_grid = Common.tab_grid()

        self.tab_title_grid()

        self.da_grid()

        self.information_grid()


    def tab_title_grid(self):
        """
        Generate tab name, device name labels.
        """

        # Grid (tab title)
        grid = Gtk.Grid()
        self.tab_grid.attach(grid, 0, 0, 1, 1)

        # Label (Network)
        label = Common.tab_title_label(_tr("Network"))
        grid.attach(label, 0, 0, 1, 2)

        # Label (device vendor-model label)
        self.device_vendor_model_label = Common.device_vendor_model_label()
        self.device_vendor_model_label.set_tooltip_text(_tr("Vendor-Model"))
        grid.attach(self.device_vendor_model_label, 1, 0, 1, 1)

        # Label (device kernel name)
        self.device_kernel_name_label = Common.device_kernel_name_label()
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
        label = Common.da_upper_lower_label(_tr("Download Speed") + " (-) & " + _tr("Upload Speed") + " (-  -)", Gtk.Align.START)
        grid.attach(label, 0, 0, 1, 1)

        # Label (drawingarea upper-right)
        self.da_upper_right_label = Common.da_upper_lower_label("--", Gtk.Align.END)
        grid.attach(self.da_upper_right_label, 1, 0, 1, 1)

        # DrawingArea
        self.da_network_speed = Common.drawingarea(Performance.performance_line_charts_draw, "da_network_speed")
        grid.attach(self.da_network_speed, 0, 2, 2, 1)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label("0", Gtk.Align.END)
        grid.attach(label, 0, 3, 2, 1)


    def information_grid(self):
        """
        Generate performance/information labels.
        """

        # Grid (performance/information labels)
        performance_info_grid = Common.performance_info_grid()
        self.tab_grid.attach(performance_info_grid, 0, 2, 1, 1)

        # Styled information widgets (Download Speed and Upload Speed)
        # ScrolledWindow (Download Speed and Upload Speed)
        scrolledwindow, self.download_speed_label, self.upload_speed_label = Common.styled_information_scrolledwindow(_tr("Download Speed"), None, _tr("Upload Speed"), None)
        performance_info_grid.attach(scrolledwindow, 0, 0, 1, 1)

        # Styled information widgets (Downloaded Data and Uploaded Data)
        # ScrolledWindow (Downloaded Data and Uploaded Data)
        scrolledwindow, self.download_data_label, self.upload_data_label = Common.styled_information_scrolledwindow(_tr("Downloaded Data"), _tr("Measured value since last system start"), _tr("Uploaded Data"), _tr("Measured value since last system start"))
        performance_info_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # Grid - Right information labels
        performance_info_right_grid = Common.performance_info_right_grid()
        performance_info_grid.attach(performance_info_right_grid, 1, 0, 1, 2)

        # Labels - Right information labels
        # Label (Connection Type)
        label = Common.static_information_label(_tr("Connection Type") + ":")
        performance_info_right_grid.attach(label, 0, 0, 1, 1)
        # Label (Connection Type)
        self.connection_type_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.connection_type_label, 1, 0, 1, 1)

        # Label (Connected-SSID)
        label = Common.static_information_label(_tr("Connected-SSID") + ":")
        performance_info_right_grid.attach(label, 0, 1, 1, 1)
        # Label (Connected-SSID)
        self.connected_ssid_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.connected_ssid_label, 1, 1, 1, 1)

        # Label (Link Quality)
        label = Common.static_information_label(_tr("Link Quality") + ":")
        performance_info_right_grid.attach(label, 0, 2, 1, 1)
        # Label (Link Quality)
        self.link_quality_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.link_quality_label, 1, 2, 1, 1)

        # Label (IPv4 Address)
        label = Common.static_information_label(_tr("IPv4 Address") + ":")
        performance_info_right_grid.attach(label, 0, 3, 1, 1)
        # Label (IPv4 Address)
        self.ipv4_address_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.ipv4_address_label, 1, 3, 1, 1)

        # Label (IPv6 Address)
        label = Common.static_information_label(_tr("IPv6 Address") + ":")
        performance_info_right_grid.attach(label, 0, 4, 1, 1)
        # Label (IPv6 Address)
        self.ipv6_address_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.ipv6_address_label, 1, 4, 1, 1)

        # Label (MAC Address)
        label = Common.static_information_label(_tr("MAC Address") + ":")
        performance_info_right_grid.attach(label, 0, 5, 1, 1)
        # Label (MAC Address)
        self.mac_address_label = Common.dynamic_information_label()
        performance_info_right_grid.attach(self.mac_address_label, 1, 5, 1, 1)


    def network_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        network_card_list = Performance.network_card_list
        selected_network_card = Performance.selected_network_card


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
        selected_network_card = Performance.selected_network_card

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

        performance_network_data_precision = Config.performance_network_data_precision
        performance_network_data_unit = Config.performance_network_data_unit
        performance_network_speed_bit = Config.performance_network_speed_bit

        self.da_network_speed.queue_draw()

        # Run "main_gui_device_selection_list" if selected device list is changed since the last loop.
        network_card_list = Performance.network_card_list
        try:                                                                                      
            if self.network_card_list_prev != network_card_list:
                MainWindow.main_gui_device_selection_list()
        # Avoid error if this is first loop of the function.
        except AttributeError:
            pass
        self.network_card_list_prev = list(network_card_list)


        # Get information.
        network_send_bytes, network_receive_bytes = self.network_download_upload_data_func(selected_network_card)
        network_card_connected = self.network_card_connected_func(selected_network_card)
        network_ssid = self.network_ssid_func(selected_network_card)
        network_link_quality = self.network_link_quality_func(selected_network_card, network_card_connected)


        # Set and update Network tab label texts by using information get
        self.download_speed_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", performance_network_speed_bit, network_receive_speed[selected_network_card][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.upload_speed_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", performance_network_speed_bit, network_send_speed[selected_network_card][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.download_data_label.set_text(Performance.performance_data_unit_converter_func("data", "none", network_receive_bytes, performance_network_data_unit, performance_network_data_precision))
        self.upload_data_label.set_text(Performance.performance_data_unit_converter_func("data", "none", network_send_bytes, performance_network_data_unit, performance_network_data_precision))
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
                device_vendor_name, device_model_name, _, _ = Common.device_vendor_model(modalias_output)
                if device_vendor_name == "Unknown":
                    device_vendor_name = "[" + _tr("Unknown") + "]"
                if device_model_name == "Unknown":
                    device_model_name = "[" + _tr("Unknown") + "]"
            network_card_device_model_name = f'{device_vendor_name} - {device_model_name}'
        # Get device vendor and model names if it is a virtual device.
        else:
            # lo (Loopback Device) is a system device and it is not a physical device.
            if selected_network_card == "lo":
                network_card_device_model_name = "[" + "Loopback Device" + "]"
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


    def network_download_upload_data_func(self, selected_network_card):
        """
        Get network card download data and upload data.
        """

        network_io = Performance.network_io()

        network_receive_bytes = network_io[selected_network_card]["download_bytes"]
        network_send_bytes = network_io[selected_network_card]["upload_bytes"]

        return network_send_bytes, network_receive_bytes


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
            network_card_connected = "[" + _tr("Unknown") + "]"
        else:
            network_card_connected = network_info

        return network_card_connected


    def network_ssid_func(self, selected_network_card):
        """
        Get network name (SSID).
        """

        command_list = ["nmcli", "-get-values", "DEVICE,CONNECTION", "device", "status"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        try:
            nmcli_output_lines = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")
        # Avoid errors because Network Manager (required "nmcli" command) may not be installed (very rare).
        except (FileNotFoundError, subprocess.CalledProcessError) as me:
            nmcli_output_lines = "-"
            network_ssid = "[" + _tr("Unknown") + "]"

        # Check if "nmcli_output_lines" value is get.
        if nmcli_output_lines != "-":
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
                    # Remove "." at the end of the signal value.
                    network_link_quality = line_splitted[2].split(".")[0]
                    if network_link_quality != "-":
                        network_link_quality = f'{network_link_quality} (link)'
                    break

        return network_link_quality


Network = Network()


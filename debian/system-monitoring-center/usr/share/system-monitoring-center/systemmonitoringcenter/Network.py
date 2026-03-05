import tkinter as tk
from tkinter import ttk

import os
import subprocess

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class Network:

    def __init__(self):

        self.name = "Network"

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_frame = ttk.Frame(MainWindow.network_tab_main_frame)
        self.tab_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.tab_frame.columnconfigure(0, weight=1)
        self.tab_frame.rowconfigure(1, weight=1)

        self.tab_title_frame()

        self.da_frame()

        self.information_frame()


    def tab_title_frame(self):
        """
        Generate tab name, device name labels.
        """

        # Grid (tab title)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=0, column=0, sticky="new", padx=0, pady=(0, 10))
        """frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)"""

        # Label (Network)
        label = Common.tab_title_label(frame, _tr("Network"))

        # Label (device vendor-model label)
        self.device_vendor_model_label = Common.device_vendor_model_label(frame)
        tooltip = Common.tooltip(self.device_vendor_model_label, _tr("Vendor - Model"))

        # Label (device kernel name)
        self.device_kernel_name_label = Common.device_kernel_name_label(frame)
        tooltip = Common.tooltip(self.device_kernel_name_label, _tr("Device Name In Kernel"))


    def da_frame(self):
        """
        Generate tab drawingarea and related information labels.
        """

        # Frame (drawingarea)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(0, 10))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Label (drawingarea upper-left)
        self.da_upper_left_label = Common.da_upper_lower_label(frame, _tr("Download Speed") + " (-) & " + _tr("Upload Speed") + " (-  -)")
        self.da_upper_left_label.grid(row=0, column=0, sticky="w")

        # Label (drawingarea upper-right)
        self.da_upper_right_label  = Common.da_upper_lower_label(frame, "--")
        self.da_upper_right_label .grid(row=0, column=1, sticky="e")

        # Label (for showing graphics)
        self.da_network_speed = Common.drawingarea(frame, "da_network_speed")
        self.da_network_speed.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label(frame, "0")
        label.grid(row=2, column=1, sticky="e")


    def information_frame(self):
        """
        Generate performance/information labels.
        """

        # Frame (performance/information labels)
        performance_info_grid = ttk.Frame(self.tab_frame)
        performance_info_grid.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        performance_info_grid.columnconfigure((0, 1), weight=1, uniform="equal")
        performance_info_grid.rowconfigure((0, 1), weight=1, uniform="equal")
        #performance_info_grid.rowconfigure(0, weight=1)

        # Styled information widgets (Download Speed and Upload Speed)
        # Frame (Download Speed and Upload Speed)
        _frame, self.download_speed_label, self.upload_speed_label = Common.styled_information_scrolledwindow(performance_info_grid, _tr("Download Speed"), None, _tr("Upload Speed"), None)
        _frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=(0, 5))

        # Styled information widgets (Downloaded Data and Uploaded Data)
        # Frame (Downloaded Data and Uploaded Data)
        _frame, self.download_data_label, self.upload_data_label = Common.styled_information_scrolledwindow(performance_info_grid, _tr("Downloaded Data"), _tr("Measured value since last system start"), _tr("Uploaded Data"), _tr("Measured value since last system start"))
        _frame.grid(row=1, column=0, sticky="nsew", padx=(0, 15), pady=(5, 0))

        # Frame - Right information labels
        performance_info_right_frame = ttk.Frame(performance_info_grid)
        performance_info_right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=0, pady=0)
        performance_info_right_frame.columnconfigure((0, 1), weight=1, uniform="equal")

        # Labels - Right information labels
        # Label (Connection Type)
        label = Common.static_information_label(performance_info_right_frame, _tr("Connection Type") + ":")
        label.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Connection Type)
        self.connection_type_label = Common.dynamic_information_label(performance_info_right_frame)
        self.connection_type_label.grid(row=0, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Connected-SSID)
        label = Common.static_information_label(performance_info_right_frame, _tr("Connected-SSID") + ":")
        label.grid(row=1, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Connected-SSID)
        self.connected_ssid_label = Common.dynamic_information_label(performance_info_right_frame)
        self.connected_ssid_label.grid(row=1, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (Link Quality)
        label = Common.static_information_label(performance_info_right_frame, _tr("Link Quality") + ":")
        label.grid(row=2, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (Link Quality)
        self.link_quality_label = Common.dynamic_information_label(performance_info_right_frame)
        self.link_quality_label.grid(row=2, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (IPv4 Address)
        label = Common.static_information_label(performance_info_right_frame, _tr("IPv4 Address") + ":")
        label.grid(row=3, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (IPv4 Address)
        self.ipv4_address_label = Common.dynamic_information_label(performance_info_right_frame)
        self.ipv4_address_label.grid(row=3, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (IPv6 Address)
        label = Common.static_information_label(performance_info_right_frame, _tr("IPv6 Address") + ":")
        label.grid(row=4, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (IPv6 Address)
        self.ipv6_address_label = Common.dynamic_information_label(performance_info_right_frame)
        self.ipv6_address_label.grid(row=4, column=1, sticky="w", padx=(4, 0), pady=(0, 4))

        # Label (MAC Address)
        label = Common.static_information_label(performance_info_right_frame, _tr("MAC Address") + ":")
        label.grid(row=5, column=0, sticky="w", padx=0, pady=(0, 4))
        # Label (MAC Address)
        self.mac_address_label = Common.dynamic_information_label(performance_info_right_frame)
        self.mac_address_label.grid(row=5, column=1, sticky="w", padx=(4, 0), pady=(0, 4))


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        network_card_list = Performance.network_card_list
        selected_network_card = Performance.selected_network_card


        # Get information.
        network_card_device_model_name = Libsysmon.get_network_card_device_model_name(selected_network_card)
        connection_type = Libsysmon.get_connection_type(selected_network_card)
        network_card_mac_address = Libsysmon.get_mac_address(selected_network_card)
        network_address_ipv4, network_address_ipv6 = Libsysmon.get_ipv4_ipv6_address(selected_network_card)


        # Set Network tab label texts by using information get
        self.device_vendor_model_label.config(text=network_card_device_model_name)
        self.device_kernel_name_label.config(text=selected_network_card)
        self.connection_type_label.config(text=connection_type)
        self.ipv4_address_label.config(text=network_address_ipv4)
        self.ipv6_address_label.config(text=network_address_ipv6)
        self.mac_address_label.config(text=network_card_mac_address)

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        network_card_list = Performance.network_card_list
        selected_network_card = Performance.selected_network_card

        # Run "initial_func" if selected network card is changed since the last loop.
        try:
            if self.selected_network_card_prev != selected_network_card:
                self.initial_func()
        # Avoid errors if this is first loop of the function.
        except AttributeError:
            pass
        self.selected_network_card_prev = selected_network_card

        network_receive_speed = Performance.network_receive_speed
        network_send_speed = Performance.network_send_speed

        performance_network_data_precision = Config.performance_network_data_precision
        performance_network_data_unit = Config.performance_network_data_unit
        performance_network_speed_bit = Config.performance_network_speed_bit

        Performance.performance_line_charts_draw(self.da_network_speed, "da_network_speed")

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
        network_send_bytes, network_receive_bytes = Libsysmon.get_network_download_upload_data(selected_network_card)
        network_card_connected = Libsysmon.get_network_card_connected(selected_network_card)
        network_ssid = Libsysmon.get_network_ssid(selected_network_card)
        network_link_quality = Libsysmon.get_network_link_quality(selected_network_card, network_card_connected)


        # Set and update Network tab label texts by using information get
        self.download_speed_label.config(text=f'{Libsysmon.data_unit_converter("speed", performance_network_speed_bit, network_receive_speed[selected_network_card][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.upload_speed_label.config(text=f'{Libsysmon.data_unit_converter("speed", performance_network_speed_bit, network_send_speed[selected_network_card][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.download_data_label.config(text=Libsysmon.data_unit_converter("data", "none", network_receive_bytes, performance_network_data_unit, performance_network_data_precision))
        self.upload_data_label.config(text=Libsysmon.data_unit_converter("data", "none", network_send_bytes, performance_network_data_unit, performance_network_data_precision))
        self.connected_ssid_label.config(text=f'{network_card_connected} - {network_ssid}')
        self.link_quality_label.config(text=network_link_quality)


Network = Network()


import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


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
        self.device_vendor_model_label.set_label(network_card_device_model_name)
        self.device_kernel_name_label.set_label(selected_network_card)
        self.connection_type_label.set_label(connection_type)
        self.ipv4_address_label.set_label(network_address_ipv4)
        self.ipv6_address_label.set_label(network_address_ipv6)
        self.mac_address_label.set_label(network_card_mac_address)

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
        network_send_bytes, network_receive_bytes = Libsysmon.get_network_download_upload_data(selected_network_card)
        network_card_connected = Libsysmon.get_network_card_connected(selected_network_card)
        network_ssid = Libsysmon.get_network_ssid(selected_network_card)
        network_link_quality = Libsysmon.get_network_link_quality(selected_network_card, network_card_connected)


        # Set and update Network tab label texts by using information get
        self.download_speed_label.set_label(f'{Libsysmon.data_unit_converter("speed", performance_network_speed_bit, network_receive_speed[selected_network_card][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.upload_speed_label.set_label(f'{Libsysmon.data_unit_converter("speed", performance_network_speed_bit, network_send_speed[selected_network_card][-1], performance_network_data_unit, performance_network_data_precision)}/s')
        self.download_data_label.set_label(Libsysmon.data_unit_converter("data", "none", network_receive_bytes, performance_network_data_unit, performance_network_data_precision))
        self.upload_data_label.set_label(Libsysmon.data_unit_converter("data", "none", network_send_bytes, performance_network_data_unit, performance_network_data_precision))
        self.connected_ssid_label.set_label(f'{network_card_connected} - {network_ssid}')
        self.link_quality_label.set_label(network_link_quality)


Network = Network()


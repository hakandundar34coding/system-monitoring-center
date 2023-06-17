import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk

from locale import gettext as _tr

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common


class NetworkMenu:

    def __init__(self):

        self.menu_gui()


    def menu_gui(self):
        """
        Generate menu GUI.
        """

        # Popover
        self.menu_po = Gtk.Popover()

        # Grid (main)
        main_grid = Common.menu_main_grid()
        self.menu_po.set_child(main_grid)

        # Label - menu title (Network)
        label = Common.menu_title_label(_tr("Network"))
        main_grid.attach(label, 0, 0, 2, 1)

        # Label (Graph - Show)
        label = Common.title_label(_tr("Graph - Show"))
        main_grid.attach(label, 0, 1, 2, 1)

        # CheckButton (Download Speed)
        self.download_speed_cb = Common.checkbutton(_tr("Download Speed"), None)
        main_grid.attach(self.download_speed_cb, 0, 2, 1, 1)

        # CheckButton (Upload Speed)
        self.upload_speed_cb = Common.checkbutton(_tr("Upload Speed"), None)
        main_grid.attach(self.upload_speed_cb, 1, 2, 1, 1)

        # CheckButton (Selected Device)
        self.selected_device_cb = Common.checkbutton(_tr("Selected Device"), None)
        main_grid.attach(self.selected_device_cb, 0, 3, 1, 1)

        # CheckButton (All Devices)
        self.all_devices_cb = Common.checkbutton(_tr("All Devices"), self.selected_device_cb)
        main_grid.attach(self.all_devices_cb, 1, 3, 1, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 4, 2, 1)

        # Button (Graph Color)
        self.graph_color_button = Common.graph_color_button()
        main_grid.attach(self.graph_color_button, 0, 5, 2, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 6, 2, 1)

        # Label - title (Precision)
        label = Common.title_label(_tr("Precision"))
        main_grid.attach(label, 0, 7, 2, 1)

        # DropDown - precision (Network)
        item_list = ['0', '0.0', '0.00', '0.000']
        self.network_precision_dd = Common.dropdown_and_model(item_list)
        main_grid.attach(self.network_precision_dd, 0, 8, 2, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 9, 2, 1)

        # Label - title (Data Unit)
        label = Common.title_label(_tr("Data Unit"))
        main_grid.attach(label, 0, 10, 2, 1)

        # Label (Show data as powers of:)
        label = Gtk.Label()
        label.set_label(_tr("Show data as powers of") + ":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 11, 2, 1)

        # CheckButton (1024)
        self.data_power_of_1024_cb = Common.checkbutton("1024", None)
        main_grid.attach(self.data_power_of_1024_cb, 0, 12, 1, 1)

        # CheckButton (1000)
        self.data_power_of_1000_cb = Common.checkbutton("1000", self.data_power_of_1024_cb)
        main_grid.attach(self.data_power_of_1000_cb, 1, 12, 1, 1)

        # CheckButton (Show speed units as multiples of bits)
        self.data_bits_cb = Common.checkbutton(_tr("Show speed units as multiples of bits"), None)
        main_grid.attach(self.data_bits_cb, 0, 13, 2, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 14, 2, 1)

        # Button (Reset)
        self.reset_button = Common.reset_button()
        main_grid.attach(self.reset_button, 0, 18, 2, 1)

        # Connect signals
        self.menu_po.connect("show", self.on_menu_po_show)
        self.reset_button.connect("clicked", self.on_reset_button_clicked)


    def connect_signals(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.download_speed_cb.connect("toggled", self.on_download_speed_cb_toggled)
        self.upload_speed_cb.connect("toggled", self.on_upload_speed_cb_toggled)
        self.selected_device_cb.connect("toggled", self.on_network_menu_device_selection_cb)
        self.all_devices_cb.connect("toggled", self.on_network_menu_device_selection_cb)
        self.data_power_of_1024_cb.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.data_power_of_1000_cb.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.data_bits_cb.connect("toggled", self.on_data_bits_cb_toggled)
        self.network_precision_dd.connect("notify::selected-item", self.on_selected_item_notify)


    def disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.download_speed_cb.disconnect_by_func(self.on_download_speed_cb_toggled)
        self.upload_speed_cb.disconnect_by_func(self.on_upload_speed_cb_toggled)
        self.selected_device_cb.disconnect_by_func(self.on_network_menu_device_selection_cb)
        self.all_devices_cb.disconnect_by_func(self.on_network_menu_device_selection_cb)
        self.data_power_of_1024_cb.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.data_power_of_1000_cb.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.data_bits_cb.disconnect_by_func(self.on_data_bits_cb_toggled)
        self.network_precision_dd.disconnect_by_func(self.on_selected_item_notify)


    def on_menu_po_show(self, widget):
        """
        Run code when menu is shown.
        """

        try:
            self.disconnect_signals()
        except TypeError:
            pass
        self.set_gui()
        self.connect_signals()


    def on_download_speed_cb_toggled(self, widget):
        """
        Show/Hide network read speed line.
        """

        if widget.get_active() == True:
            Config.plot_network_download_speed = 1
        if widget.get_active() == False:
            if self.upload_speed_cb.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_network_download_speed = 0

        Common.save_tab_settings()


    def on_upload_speed_cb_toggled(self, widget):
        """
        Show/Hide network write speed line.
        """

        if widget.get_active() == True:
            Config.plot_network_upload_speed = 1
        if widget.get_active() == False:
            if self.download_speed_cb.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_network_upload_speed = 0

        Common.save_tab_settings()


    def on_network_menu_device_selection_cb(self, widget):
        """
        Set device selection (Selected/All) for showing speed data.
        """

        if widget.get_active() == True:
            if widget == self.selected_device_cb:
                Config.show_network_usage_per_network_card = 0
            if widget == self.all_devices_cb:
                Config.show_network_usage_per_network_card = 1

        Common.save_tab_settings()


    def on_selected_item_notify(self, widget, parameter):
        """
        Change network data/speed precision.
        Notify signal is sent when DropDown widget selection is changed.
        Currently GtkExpression parameter for DropDown can not be used because of PyGObject.
        """

        Config.performance_network_data_precision = widget.get_selected()

        Common.save_tab_settings()


    def on_data_unit_radiobuttons_toggled(self, widget):
        """
        Change data unit powers of (1024 or 1000) selection.
        """

        if self.data_power_of_1024_cb.get_active() == True:
            Config.performance_network_data_unit = 0
        elif self.data_power_of_1000_cb.get_active() == True:
            Config.performance_network_data_unit = 1

        Common.save_tab_settings()


    def on_data_bits_cb_toggled(self, widget):
        """
        Show speed units as multiples of bits/bytes.
        """

        if widget.get_active() == True:
            Config.performance_network_speed_bit = 1
        else:
            Config.performance_network_speed_bit = 0

        Common.save_tab_settings()


    def on_reset_button_clicked(self, widget):
        """
        Reset all tab settings.
        """

        # Load default settings
        Config.config_default_performance_network_func()
        Config.config_save_func()
        Performance.performance_set_selected_network_card_func()

        # Reset device list between Performance tab sub-tabs because selected device is reset.
        MainWindow.main_gui_device_selection_list()

        Common.update_tab_and_menu_gui(self)


    def set_gui(self):
        """
        Set menu GUI items.
        """

        # Set active checkbuttons if network download speed/network upload speed values are "1"
        if Config.plot_network_download_speed == 1:
            self.download_speed_cb.set_active(True)
        if Config.plot_network_download_speed == 0:
            self.download_speed_cb.set_active(False)
        if Config.plot_network_upload_speed == 1:
            self.upload_speed_cb.set_active(True)
        if Config.plot_network_upload_speed == 0:
            self.upload_speed_cb.set_active(False)

        # Select radiobutton appropriate for seleted/all devices chart setting
        if Config.show_network_usage_per_network_card == 0:
            self.selected_device_cb.set_active(True)
        if Config.show_network_usage_per_network_card == 1:
            self.all_devices_cb.set_active(True)

        # Set data unit radiobuttons and checkbuttons.
        if Config.performance_network_data_unit == 0:
            self.data_power_of_1024_cb.set_active(True)
        if Config.performance_network_data_unit == 1:
            self.data_power_of_1000_cb.set_active(True)
        if Config.performance_network_speed_bit == 1:
            self.data_bits_cb.set_active(True)
        if Config.performance_network_speed_bit == 0:
            self.data_bits_cb.set_active(False)

        self.network_precision_dd.set_selected(Config.performance_network_data_precision)

NetworkMenu = NetworkMenu()


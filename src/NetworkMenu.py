#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os

from Config import Config
from Performance import Performance
from Network import Network
from MainGUI import MainGUI


# Define class
class NetworkMenu:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/NetworkMenus.ui")

        # Get GUI objects
        self.popover1401p = builder.get_object('popover1401p')
        self.button1401p = builder.get_object('button1401p')
        self.button1403p = builder.get_object('button1403p')
        self.combobox1401p = builder.get_object('combobox1401p')
        self.checkbutton1401p = builder.get_object('checkbutton1401p')
        self.checkbutton1402p = builder.get_object('checkbutton1402p')
        self.radiobutton1401p = builder.get_object('radiobutton1401p')
        self.radiobutton1402p = builder.get_object('radiobutton1402p')
        self.radiobutton1403p = builder.get_object('radiobutton1403p')
        self.radiobutton1404p = builder.get_object('radiobutton1404p')
        self.checkbutton1404p = builder.get_object('checkbutton1404p')
        self.colorchooserdialog1401 = Gtk.ColorChooserDialog()

        # Connect GUI signals
        self.popover1401p.connect("show", self.on_popover1401p_show)
        self.button1401p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1403p.connect("clicked", self.on_button1403p_clicked)


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def network_tab_customization_popover_connect_signals_func(self):

        self.checkbutton1401p.connect("toggled", self.on_checkbutton1401p_toggled)
        self.checkbutton1402p.connect("toggled", self.on_checkbutton1402p_toggled)
        self.radiobutton1401p.connect("toggled", self.on_radiobutton1401p_toggled)
        self.radiobutton1402p.connect("toggled", self.on_radiobutton1402p_toggled)
        self.radiobutton1403p.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.radiobutton1404p.connect("toggled", self.on_data_unit_radiobuttons_toggled)
        self.checkbutton1404p.connect("toggled", self.on_checkbutton1404p_toggled)
        self.combobox1401p.connect("changed", self.on_combobox1401p_changed)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def network_tab_customization_popover_disconnect_signals_func(self):

        self.checkbutton1401p.disconnect_by_func(self.on_checkbutton1401p_toggled)
        self.checkbutton1402p.disconnect_by_func(self.on_checkbutton1402p_toggled)
        self.radiobutton1401p.disconnect_by_func(self.on_radiobutton1401p_toggled)
        self.radiobutton1402p.disconnect_by_func(self.on_radiobutton1402p_toggled)
        self.radiobutton1403p.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.radiobutton1404p.disconnect_by_func(self.on_data_unit_radiobuttons_toggled)
        self.checkbutton1404p.disconnect_by_func(self.on_checkbutton1404p_toggled)
        self.combobox1401p.disconnect_by_func(self.on_combobox1401p_changed)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover1401p_show(self, widget):

        try:
            self.network_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        self.network_tab_popover_set_gui()
        self.network_tab_customization_popover_connect_signals_func()


    # ----------------------- "network download speed" Checkbutton -----------------------
    def on_checkbutton1401p_toggled(self, widget):

        if widget.get_active() == True:
            Config.plot_network_download_speed = 1
        if widget.get_active() == False:
            if self.checkbutton1402p.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_network_download_speed = 0

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "network upload speed" Checkbutton -----------------------
    def on_checkbutton1402p_toggled(self, widget):

        if widget.get_active() == True:
            Config.plot_network_upload_speed = 1
        if widget.get_active() == False:
            if self.checkbutton1401p.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_network_upload_speed = 0

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "Selected Device" Radiobutton -----------------------
    def on_radiobutton1401p_toggled(self, widget):

        if widget.get_active() == True:
            Config.show_network_usage_per_network_card = 0

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "All Devices" Radiobutton -----------------------
    def on_radiobutton1402p_toggled(self, widget):

        if widget.get_active() == True:
            Config.show_network_usage_per_network_card = 1

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "network data precision" Combobox -----------------------
    def on_combobox1401p_changed(self, widget):

        Config.performance_network_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "Show units as powers of: 1024 or 1000" Radiobuttons -----------------------
    def on_data_unit_radiobuttons_toggled(self, widget):

        if self.radiobutton1403p.get_active() == True:
            Config.performance_network_data_unit = 0
        elif self.radiobutton1404p.get_active() == True:
            Config.performance_network_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "Show speed units as multiples of bits" Checkbutton -----------------------
    def on_checkbutton1404p_toggled(self, widget):

        if widget.get_active() == True:
            Config.performance_network_speed_bit = 1
        else:
            Config.performance_network_speed_bit = 0

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "foreground and background color" Buttons -----------------------
    def on_chart_color_buttons_clicked(self, widget):

        # Get current foreground/background color of the chart and set it as selected color of the dialog when dialog is shown.
        if widget == self.button1401p:
            red, blue, green, alpha = Config.chart_line_color_network_speed_data
        self.colorchooserdialog1401.set_rgba(Gdk.RGBA(red, blue, green, alpha))

        dialog_response = self.colorchooserdialog1401.run()

        if dialog_response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog1401.get_rgba()
            if widget == self.button1401p:
                Config.chart_line_color_network_speed_data = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog1401.hide()

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "Reset All" Button -----------------------
    def on_button1403p_clicked(self, widget):

        # Load default settings
        Config.config_default_performance_network_func()
        Config.config_save_func()
        Performance.performance_set_selected_network_card_func()

        # Reset device list between Performance tab sub-tabs because selected device is reset.
        MainGUI.main_gui_device_selection_list_func()

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        self.network_tab_customization_popover_disconnect_signals_func()
        self.network_tab_popover_set_gui()
        self.network_tab_customization_popover_connect_signals_func()


    # ----------------------- Called for setting menu GUI items -----------------------
    def network_tab_popover_set_gui(self):

        # Set active checkbuttons if network download speed/network upload speed values are "1"
        if Config.plot_network_download_speed == 1:
            self.checkbutton1401p.set_active(True)
        if Config.plot_network_download_speed == 0:
            self.checkbutton1401p.set_active(False)
        if Config.plot_network_upload_speed == 1:
            self.checkbutton1402p.set_active(True)
        if Config.plot_network_upload_speed == 0:
            self.checkbutton1402p.set_active(False)

        # Select radiobutton appropriate for seleted/all devices chart setting
        if Config.show_network_usage_per_network_card == 0:
            self.radiobutton1401p.set_active(True)
        if Config.show_network_usage_per_network_card == 1:
            self.radiobutton1402p.set_active(True)

        # Set data unit radiobuttons and checkbuttons.
        if Config.performance_network_data_unit == 0:
            self.radiobutton1403p.set_active(True)
        if Config.performance_network_data_unit == 1:
            self.radiobutton1404p.set_active(True)
        if Config.performance_network_speed_bit == 1:
            self.checkbutton1404p.set_active(True)
        if Config.performance_network_speed_bit == 0:
            self.checkbutton1404p.set_active(False)

        # Add Network data precision data into combobox
        liststore1401p = Gtk.ListStore()
        liststore1401p.set_column_types([str, int])
        self.combobox1401p.set_model(liststore1401p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1401p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1401p.pack_start(renderer_text, True)
        self.combobox1401p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1401p.append([data[1], data[2]])
        self.combobox1401p.set_active(Config.performance_network_data_precision)


# Generate object
NetworkMenu = NetworkMenu()


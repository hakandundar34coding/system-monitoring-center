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
        self.button1402p = builder.get_object('button1402p')
        self.button1403p = builder.get_object('button1403p')
        self.combobox1401p = builder.get_object('combobox1401p')
        self.combobox1402p = builder.get_object('combobox1402p')
        self.combobox1403p = builder.get_object('combobox1403p')
        self.combobox1404p = builder.get_object('combobox1404p')
        self.combobox1405p = builder.get_object('combobox1405p')
        self.checkbutton1401p = builder.get_object('checkbutton1401p')
        self.checkbutton1402p = builder.get_object('checkbutton1402p')
        self.colorchooserdialog1401 = Gtk.ColorChooserDialog()

        # Connect GUI signals
        self.popover1401p.connect("show", self.on_popover1401p_show)
        self.button1401p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1402p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1403p.connect("clicked", self.on_button1403p_clicked)


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def network_tab_customization_popover_connect_signals_func(self):

        self.checkbutton1401p.connect("toggled", self.on_checkbutton1401p_toggled)
        self.checkbutton1402p.connect("toggled", self.on_checkbutton1402p_toggled)
        self.combobox1401p.connect("changed", self.on_combobox1401p_changed)
        self.combobox1402p.connect("changed", self.on_combobox1402p_changed)
        self.combobox1403p.connect("changed", self.on_combobox1403p_changed)
        self.combobox1404p.connect("changed", self.on_combobox1404p_changed)
        self.combobox1405p.connect("changed", self.on_combobox1405p_changed)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def network_tab_customization_popover_disconnect_signals_func(self):

        self.checkbutton1401p.disconnect_by_func(self.on_checkbutton1401p_toggled)
        self.checkbutton1402p.disconnect_by_func(self.on_checkbutton1402p_toggled)
        self.combobox1401p.disconnect_by_func(self.on_combobox1401p_changed)
        self.combobox1402p.disconnect_by_func(self.on_combobox1402p_changed)
        self.combobox1403p.disconnect_by_func(self.on_combobox1403p_changed)
        self.combobox1404p.disconnect_by_func(self.on_combobox1404p_changed)
        self.combobox1405p.disconnect_by_func(self.on_combobox1405p_changed)


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


    # ----------------------- "foreground and background color" Buttons -----------------------
    def on_chart_color_buttons_clicked(self, widget):

        # Get current foreground/background color of the chart and set it as selected color of the dialog when dialog is shown.
        if widget == self.button1401p:
            red, blue, green, alpha = Config.chart_line_color_network_speed_data
        if widget == self.button1402p:
            red, blue, green, alpha = Config.chart_background_color_all_charts
        self.colorchooserdialog1401.set_rgba(Gdk.RGBA(red, blue, green, alpha))

        dialog_response = self.colorchooserdialog1401.run()

        if dialog_response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog1401.get_rgba()
            if widget == self.button1401p:
                Config.chart_line_color_network_speed_data = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
            if widget == self.button1402p:
                Config.chart_background_color_all_charts = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog1401.hide()

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "network download/upload speed number precision" Combobox -----------------------
    def on_combobox1401p_changed(self, widget):

        Config.performance_network_speed_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "network download/upload data number precision" Combobox -----------------------
    def on_combobox1402p_changed(self, widget):

        Config.performance_network_data_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "network download/upload speed data units" Combobox -----------------------
    def on_combobox1403p_changed(self, widget):

        Config.performance_network_speed_data_unit = Config.data_speed_unit_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "network download/upload data units" Combobox -----------------------
    def on_combobox1404p_changed(self, widget):

        Config.performance_network_data_data_unit = Config.data_unit_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        Config.config_save_func()


    # ----------------------- "Selected Device" Combobox -----------------------
    def on_combobox1405p_changed(self, widget):

        Config.selected_network_card = Performance.network_card_list[widget.get_active()]
        Performance.set_selected_network_card = Config.selected_network_card
        Performance.performance_set_selected_network_card_func()

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

        # Apply changes immediately (without waiting update interval).
        Network.network_initial_func()
        Network.network_loop_func()
        self.network_tab_customization_popover_disconnect_signals_func()
        self.network_tab_popover_set_gui()
        self.network_tab_customization_popover_connect_signals_func()


    # ----------------------- Called for setting menu GUI items -----------------------
    def network_tab_popover_set_gui(self):

        # Set active comboboxes if network download speed/network upload speed values are "1"
        if Config.plot_network_download_speed == 1:
            self.checkbutton1401p.set_active(True)
        if Config.plot_network_download_speed == 0:
            self.checkbutton1401p.set_active(False)
        if Config.plot_network_upload_speed == 1:
            self.checkbutton1402p.set_active(True)
        if Config.plot_network_upload_speed == 0:
            self.checkbutton1402p.set_active(False)

        # Add Network speed data precision data into combobox
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
        self.combobox1401p.set_active(Config.performance_network_speed_data_precision)

        # Add Network data data precision data into combobox
        liststore1402p = Gtk.ListStore()
        liststore1402p.set_column_types([str, int])
        self.combobox1402p.set_model(liststore1402p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1402p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1402p.pack_start(renderer_text, True)
        self.combobox1402p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1402p.append([data[1], data[2]])
        self.combobox1402p.set_active(Config.performance_network_data_data_precision)

        # Add Network speed data unit data into combobox
        liststore1403p = Gtk.ListStore()
        liststore1403p.set_column_types([str, int])
        self.combobox1403p.set_model(liststore1403p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1403p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1403p.pack_start(renderer_text, True)
        self.combobox1403p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_speed_unit_list:
            liststore1403p.append([data[1], data[2]])
        for data_list in Config.data_speed_unit_list:
            if data_list[2] == Config.performance_network_speed_data_unit:      
                self.combobox1403p.set_active(data_list[0])

        # Add Network data data unit data into combobox
        liststore1404p = Gtk.ListStore()
        liststore1404p.set_column_types([str, int])
        self.combobox1404p.set_model(liststore1404p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1404p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1404p.pack_start(renderer_text, True)
        self.combobox1404p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_unit_list:
            liststore1404p.append([data[1], data[2]])
        for data_list in Config.data_unit_list:
            if data_list[2] == Config.performance_network_data_data_unit:      
                self.combobox1404p.set_active(data_list[0])

        # Add Network Card list into combobox
        liststore1405p = Gtk.ListStore()
        liststore1405p.set_column_types([str])
        self.combobox1405p.set_model(liststore1405p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1405p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1405p.pack_start(renderer_text, True)
        self.combobox1405p.add_attribute(renderer_text, "text", 0)
        liststore1405p.clear()
        for network_card in Performance.network_card_list:
            liststore1405p.append([network_card])
        self.combobox1405p.set_active(Performance.selected_network_card_number)


# Generate object
NetworkMenu = NetworkMenu()


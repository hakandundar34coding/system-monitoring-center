#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os

from Config import Config
from Performance import Performance
from Disk import Disk


# Define class
class DiskMenu:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/DiskMenus.ui")

        # Get GUI objects
        self.popover1301p = builder.get_object('popover1301p')
        self.button1301p = builder.get_object('button1301p')
        self.button1302p = builder.get_object('button1302p')
        self.button1303p = builder.get_object('button1303p')
        self.combobox1301p = builder.get_object('combobox1301p')
        self.combobox1302p = builder.get_object('combobox1302p')
        self.combobox1303p = builder.get_object('combobox1303p')
        self.combobox1304p = builder.get_object('combobox1304p')
        self.combobox1305p = builder.get_object('combobox1305p')
        self.checkbutton1301p = builder.get_object('checkbutton1301p')
        self.checkbutton1302p = builder.get_object('checkbutton1302p')
        self.colorchooserdialog1301 = Gtk.ColorChooserDialog()

        # Connect GUI signals
        self.popover1301p.connect("show", self.on_popover1301p_show)
        self.button1301p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1302p.connect("clicked", self.on_chart_color_buttons_clicked)
        self.button1303p.connect("clicked", self.on_button1303p_clicked)


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def disk_tab_customization_popover_connect_signals_func(self):

        self.checkbutton1301p.connect("toggled", self.on_checkbutton1301p_toggled)
        self.checkbutton1302p.connect("toggled", self.on_checkbutton1302p_toggled)
        self.combobox1301p.connect("changed", self.on_combobox1301p_changed)
        self.combobox1302p.connect("changed", self.on_combobox1302p_changed)
        self.combobox1303p.connect("changed", self.on_combobox1303p_changed)
        self.combobox1304p.connect("changed", self.on_combobox1304p_changed)
        self.combobox1305p.connect("changed", self.on_combobox1305p_changed)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def disk_tab_customization_popover_disconnect_signals_func(self):

        self.checkbutton1301p.disconnect_by_func(self.on_checkbutton1301p_toggled)
        self.checkbutton1302p.disconnect_by_func(self.on_checkbutton1302p_toggled)
        self.combobox1301p.disconnect_by_func(self.on_combobox1301p_changed)
        self.combobox1302p.disconnect_by_func(self.on_combobox1302p_changed)
        self.combobox1303p.disconnect_by_func(self.on_combobox1303p_changed)
        self.combobox1304p.disconnect_by_func(self.on_combobox1304p_changed)
        self.combobox1305p.disconnect_by_func(self.on_combobox1305p_changed)


    # ----------------------- Called for running code/functions when menu is shown -----------------------
    def on_popover1301p_show(self, widget):

        try:
            self.disk_tab_customization_popover_disconnect_signals_func()
        except TypeError:
            pass
        self.disk_tab_popover_set_gui()
        self.disk_tab_customization_popover_connect_signals_func()


    # ----------------------- "disk read speed" Checkbutton -----------------------
    def on_checkbutton1301p_toggled(self, widget):

        if widget.get_active() == True:
            Config.plot_disk_read_speed = 1
        if widget.get_active() == False:
            if self.checkbutton1302p.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_disk_read_speed = 0

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "disk write speed" Checkbutton -----------------------
    def on_checkbutton1302p_toggled(self, widget):

        if widget.get_active() == True:
            Config.plot_disk_write_speed = 1
        if widget.get_active() == False:
            if self.checkbutton1301p.get_active() == False:
                widget.set_active(True)
                return
            Config.plot_disk_write_speed = 0

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "foreground and background color" Buttons -----------------------
    def on_chart_color_buttons_clicked(self, widget):

        # Get current foreground/background color of the chart and set it as selected color of the dialog when dialog is shown.
        if widget == self.button1301p:
            red, blue, green, alpha = Config.chart_line_color_disk_speed_usage
        if widget == self.button1302p:
            red, blue, green, alpha = Config.chart_background_color_all_charts
        self.colorchooserdialog1301.set_rgba(Gdk.RGBA(red, blue, green, alpha))

        dialog_response = self.colorchooserdialog1301.run()

        if dialog_response == Gtk.ResponseType.OK:
            selected_color = self.colorchooserdialog1301.get_rgba()
            if widget == self.button1301p:
                Config.chart_line_color_disk_speed_usage = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
            if widget == self.button1302p:
                Config.chart_background_color_all_charts = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        self.colorchooserdialog1301.hide()

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "disk read/write speed number precision" Combobox -----------------------
    def on_combobox1301p_changed(self, widget):

        Config.performance_disk_speed_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "disk read/write data number precision" Combobox -----------------------
    def on_combobox1302p_changed(self, widget):

        Config.performance_disk_usage_data_precision = Config.data_unit_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "disk read/write speed data units" Combobox -----------------------
    def on_combobox1303p_changed(self, widget):

        Config.performance_disk_speed_data_unit = Config.data_speed_unit_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "disk read/write data units" Combobox -----------------------
    def on_combobox1304p_changed(self, widget):

        Config.performance_disk_usage_data_unit = Config.data_unit_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "Selected Device" Combobox -----------------------
    def on_combobox1305p_changed(self, widget):
 
        Config.selected_disk = Performance.disk_list_system_ordered[widget.get_active()]
        Disk.selected_disk_number = Config.selected_disk
        Performance.performance_set_selected_disk_func()

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        Config.config_save_func()


    # ----------------------- "Reset All" Button -----------------------
    def on_button1303p_clicked(self, widget):

        # Load default settings
        Config.config_default_performance_disk_func()
        Config.config_save_func()
        Performance.performance_set_selected_disk_func()

        # Apply changes immediately (without waiting update interval).
        Disk.disk_initial_func()
        Disk.disk_loop_func()
        self.disk_tab_customization_popover_disconnect_signals_func()
        self.disk_tab_popover_set_gui()
        self.disk_tab_customization_popover_connect_signals_func()


    # ----------------------- Called for setting menu GUI items -----------------------
    def disk_tab_popover_set_gui(self):

        # Set active comboboxes if disk read speed/disk write speed values are "1"
        if Config.plot_disk_read_speed == 1:
            self.checkbutton1301p.set_active(True)
        if Config.plot_disk_read_speed == 0:
            self.checkbutton1301p.set_active(False)
        if Config.plot_disk_write_speed == 1:
            self.checkbutton1302p.set_active(True)
        if Config.plot_disk_write_speed == 0:
            self.checkbutton1302p.set_active(False)

        # Add Disk speed data precision data into combobox
        liststore1301p = Gtk.ListStore()
        liststore1301p.set_column_types([str, int])
        self.combobox1301p.set_model(liststore1301p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1301p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1301p.pack_start(renderer_text, True)
        self.combobox1301p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1301p.append([data[1], data[2]])
        self.combobox1301p.set_active(Config.performance_disk_speed_data_precision)

        # Add Disk usage data precision data into combobox
        liststore1302p = Gtk.ListStore()
        liststore1302p.set_column_types([str, int])
        self.combobox1302p.set_model(liststore1302p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1302p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1302p.pack_start(renderer_text, True)
        self.combobox1302p.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            liststore1302p.append([data[1], data[2]])
        self.combobox1302p.set_active(Config.performance_disk_usage_data_precision)

        # Add Disk speed data unit data into combobox
        liststore1303p = Gtk.ListStore()
        liststore1303p.set_column_types([str, int])
        self.combobox1303p.set_model(liststore1303p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1303p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1303p.pack_start(renderer_text, True)
        self.combobox1303p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_speed_unit_list:
            liststore1303p.append([data[1], data[2]])
        for data_list in Config.data_speed_unit_list:
            if data_list[2] == Config.performance_disk_speed_data_unit:      
                self.combobox1303p.set_active(data_list[0])

        # Add Disk usage data unit data into combobox
        liststore1304p = Gtk.ListStore()
        liststore1304p.set_column_types([str, int])
        self.combobox1304p.set_model(liststore1304p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1304p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1304p.pack_start(renderer_text, True)
        self.combobox1304p.add_attribute(renderer_text, "text", 0)
        for data in Config.data_unit_list:
            liststore1304p.append([data[1], data[2]])
        for data_list in Config.data_unit_list:
            if data_list[2] == Config.performance_disk_usage_data_unit:      
                self.combobox1304p.set_active(data_list[0])

        # Add Disk list into combobox
        liststore1305p = Gtk.ListStore()
        liststore1305p.set_column_types([str])
        self.combobox1305p.set_model(liststore1305p)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox1305p.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox1305p.pack_start(renderer_text, True)
        self.combobox1305p.add_attribute(renderer_text, "text", 0)
        liststore1305p.clear()
        for disk in Performance.disk_list_system_ordered:
            liststore1305p.append([disk])
        self.combobox1305p.set_active(Performance.selected_disk_number)


# Generate object
DiskMenu = DiskMenu()


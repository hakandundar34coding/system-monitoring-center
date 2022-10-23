#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib
import os

from locale import gettext as _tr

from Config import Config
from Performance import Performance


# Define class
class PerformanceSummaryHeaderbar:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/PerformanceSummaryHeaderBarGrid.ui")

        # Get GUI objects
        self.grid101 = builder.get_object('grid101')
        self.drawingarea101 = builder.get_object('drawingarea101')
        self.drawingarea102 = builder.get_object('drawingarea102')
        self.label101 = builder.get_object('label101')
        self.label102 = builder.get_object('label102')
        self.label103 = builder.get_object('label103')
        self.label104 = builder.get_object('label104')
        self.label105 = builder.get_object('label105')
        self.label106 = builder.get_object('label106')

        # Get chart functions from another module and define as local objects for lower CPU usage.
        self.performance_bar_charts_draw_func = Performance.performance_bar_charts_draw_func

        # Connect GUI signals
        self.drawingarea101.connect("draw", self.performance_bar_charts_draw_func)
        self.drawingarea102.connect("draw", self.performance_bar_charts_draw_func)

        # Run initial function
        self.performance_summary_headerbar_initial_func()


    # ----------------------------------- Performance Summary Headerbar - Initial Function -----------------------------------
    def performance_summary_headerbar_initial_func(self):

        # Set empty characters at the right side of the labels by using "f'value:<[number of characters]'" in order to prevent movement of the label when data numbers change. Total length of the string is set as [number of characters] characters if actual length is smaller. This code has no effect if length of the string equals to this value or bigger.
        self.label103.set_text(f'{_tr("CPU"):<6}')
        self.label104.set_text(f'{_tr("RAM"):<6}')
        self.label105.set_text(f'{_tr("Disk"):<13}')
        self.label106.set_text(f'{_tr("Network"):<13}')

        # Define tooltip text in order to use multiple translated texts (combine them) to avoid additional texts.
        self.label105.set_tooltip_text(f'{_tr("Read Speed")}+{_tr("Write Speed")}')
        self.label106.set_tooltip_text(f'{_tr("Download Speed")}+{_tr("Upload Speed")}')

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()


    # ----------------------------------- Performance Summary Headerbar - Get Performance Summary Headerbar Data Function -----------------------------------
    def performance_summary_headerbar_loop_func(self):

        # Update performance data on the headerbar
        selected_disk_number = Performance.selected_disk_number
        selected_network_card_number = Performance.selected_network_card_number
        self.drawingarea101.queue_draw()
        self.drawingarea102.queue_draw()
        self.label101.set_text(f'{self.performance_data_unit_converter_func("speed", Config.performance_disk_speed_bit, (Performance.disk_read_speed[selected_disk_number][-1] + Performance.disk_write_speed[selected_disk_number][-1]), Config.performance_disk_data_unit, 1)}/s')
        self.label102.set_text(f'{self.performance_data_unit_converter_func("speed", Config.performance_network_speed_bit, (Performance.network_receive_speed[selected_network_card_number][-1] + Performance.network_send_speed[selected_network_card_number][-1]), Config.performance_network_data_unit, 1)}/s')


# Generate object
PerformanceSummaryHeaderbar = PerformanceSummaryHeaderbar()


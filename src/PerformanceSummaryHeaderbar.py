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

        # Connect GUI signals
        self.drawingarea101.connect("draw", self.on_drawingarea101_draw)
        self.drawingarea102.connect("draw", self.on_drawingarea102_draw)

        # Run initial function
        self.performance_summary_headerbar_initial_func()


    # ----------------------- Called for drawing average CPU usage as bar chart -----------------------
    def on_drawingarea101_draw(self, widget, ctx):

        cpu_usage_percent_ave = Performance.cpu_usage_percent_ave

        chart_line_color = Config.chart_line_color_cpu_percent
        chart_background_color = Config.chart_background_color_all_charts

        chart101_width = Gtk.Widget.get_allocated_width(widget)
        chart101_height = Gtk.Widget.get_allocated_height(widget)

        ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        ctx.rectangle(0, 0, chart101_width, chart101_height)
        ctx.fill()

        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.7 * chart_line_color[3])
        ctx.rectangle(0, 0, chart101_width, chart101_height)
        ctx.stroke()

        ctx.set_line_width(1)
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.5 * chart_line_color[3])
        ctx.rectangle(0, 0, chart101_width*cpu_usage_percent_ave[-1]/100, chart101_height)
        ctx.fill()


    # ----------------------- Called for drawing RAM usage as bar chart -----------------------
    def on_drawingarea102_draw(self, widget, ctx):

        ram_usage_percent = Performance.ram_usage_percent

        chart_line_color = Config.chart_line_color_ram_swap_percent
        chart_background_color = Config.chart_background_color_all_charts

        chart102_width = Gtk.Widget.get_allocated_width(widget)
        chart102_height = Gtk.Widget.get_allocated_height(widget)

        ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        ctx.rectangle(0, 0, chart102_width, chart102_height)
        ctx.fill()

        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.7 * chart_line_color[3])
        ctx.rectangle(0, 0, chart102_width, chart102_height)
        ctx.stroke()

        ctx.set_line_width(1)
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.5 * chart_line_color[3])
        ctx.rectangle(0, 0, chart102_width*ram_usage_percent[-1]/100, chart102_height)
        ctx.fill()


    # ----------------------------------- Performance Summary Headerbar - Initial Function -----------------------------------
    def performance_summary_headerbar_initial_func(self):

        # Set empty characters at the right side of the labels by using "f'value:<[number of characters]'" in order to prevent movement of the label when data numbers change. Total length of the string is set as [number of characters] characters if actual length is smaller. This code has no effect if length of the string equals to this value or bigger.
        self.label103.set_text(f'{_tr("CPU"):<5}')
        self.label104.set_text(f'{_tr("RAM"):<5}')
        self.label105.set_text(f'{_tr("Disk"):<10}')
        self.label106.set_text(f'{_tr("Network"):<10}')

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
        self.label101.set_text(f'{self.performance_data_unit_converter_func((Performance.disk_read_speed[selected_disk_number][-1] + Performance.disk_write_speed[selected_disk_number][-1]), 0, 0)}/s')
        self.label102.set_text(f'{self.performance_data_unit_converter_func((Performance.network_receive_speed[selected_network_card_number][-1] + Performance.network_send_speed[selected_network_card_number][-1]), 0, 0)}/s')


# Generate object
PerformanceSummaryHeaderbar = PerformanceSummaryHeaderbar()


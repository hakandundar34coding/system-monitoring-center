#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
# Imported for using gradient colors
import cairo

from locale import gettext as _tr

from Config import Config
from Performance import Performance


# Define class
class Ram:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/RamTab.ui")

        # Get GUI objects
        self.grid1201 = builder.get_object('grid1201')
        self.drawingarea1201 = builder.get_object('drawingarea1201')
        self.drawingarea1202 = builder.get_object('drawingarea1202')
        self.button1201 = builder.get_object('button1201')
        self.label1201 = builder.get_object('label1201')
        self.label1202 = builder.get_object('label1202')
        self.label1203 = builder.get_object('label1203')
        self.label1204 = builder.get_object('label1204')
        self.label1205 = builder.get_object('label1205')
        self.label1206 = builder.get_object('label1206')
        self.label1207 = builder.get_object('label1207')
        self.label1208 = builder.get_object('label1208')
        self.label1209 = builder.get_object('label1209')
        self.label1210 = builder.get_object('label1210')
        self.eventbox1201 = builder.get_object('eventbox1201')
        self.eventbox1202 = builder.get_object('eventbox1202')

        # Connect GUI signals
        self.button1201.connect("clicked", self.on_button1201_clicked)
        self.drawingarea1201.connect("draw", self.on_drawingarea1201_draw)
        self.drawingarea1202.connect("draw", self.on_drawingarea1202_draw)
        self.eventbox1201.connect("button-press-event", self.on_eventbox1201_button_click_event)
        self.eventbox1202.connect("button-press-event", self.on_eventbox1202_button_click_event)


    # ----------------------- "customizations menu" Button -----------------------
    def on_button1201_clicked(self, widget):

        from RamMenu import RamMenu
        RamMenu.popover1201p.set_relative_to(widget)
        RamMenu.popover1201p.set_position(1)
        RamMenu.popover1201p.popup()


    # ----------------------- Called for opening RAM Hardware Window -----------------------
    def on_eventbox1201_button_click_event(self, widget, event):

        if event.button == 1:
            from RamHardwareInformation import RamHardwareInformation
            # Run function to get RAM hardware information text (polkit dialog will be shown for getting this information).
            RamHardwareInformation.ram_hardware_information_get_func()
            # This statement is used in order to avoid errors if user closes polkit window without entering password.
            if RamHardwareInformation.memory_hardware_information_text != "":
                RamHardwareInformation.window1201w.show()


    # ----------------------- Called for opening RAM Hardware Window -----------------------
    def on_eventbox1202_button_click_event(self, widget, event):

        if event.button == 1:
            from RamSwapDetails import RamSwapDetails
            RamSwapDetails.window1201w2.show()


    # ----------------------- Called for drawing RAM usage as line chart -----------------------
    def on_drawingarea1201_draw(self, widget, ctx):

        # Get values from "Config and Peformance" modules and use this defined values in order to avoid multiple uses of variables from another module since CPU usage is higher for this way.
        chart_data_history = Config.chart_data_history
        chart_x_axis = list(range(0, chart_data_history))

        ram_usage_percent = Performance.ram_usage_percent

        chart_line_color = Config.chart_line_color_ram_swap_percent
        chart_background_color = Config.chart_background_color_all_charts

        # Chart foreground and chart fill below line colors may be set different for charts in different style (line, bar, etc.) and different places (tab pages, headerbar, etc.).
        # Set chart foreground color (chart outer frame and gridline colors) same as "chart_line_color" in multiplication with transparency factor "0.4".
        # Set chart fill below line color same as "chart_line_color" in multiplication with transparency factor "0.15".

        # Get drawingarea width and height. Therefore chart width and height is updated dynamically by using these values when window size is changed by user.
        chart_width = Gtk.Widget.get_allocated_width(widget)
        chart_height = Gtk.Widget.get_allocated_height(widget)

        # Set color for chart background, draw chart background rectangle and fill the inner area.
        # Only one drawing style with multiple properties (color, line width, dash style) can be set at the same time.
        # As a result style should be set, drawing should be done and another style shpuld be set for next drawing.
        ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        ctx.rectangle(0, 0, chart_width, chart_height)
        ctx.fill()

        # Change line width and color for chart gridlines.
        ctx.set_line_width(1)
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.25 * chart_line_color[3])
        # Draw horizontal gridlines (range(3) means 3 gridlines will be drawn)
        for i in range(3):
            ctx.move_to(0, chart_height/4*(i+1))
            ctx.line_to(chart_width, chart_height/4*(i+1))
        # Draw vertical gridlines
        for i in range(4):
            ctx.move_to(chart_width/5*(i+1), 0)
            ctx.line_to(chart_width/5*(i+1), chart_height)
        # "stroke" command draws line (line or closed shapes with empty inner area). "fill" command should be used for filling inner areas.
        ctx.stroke()

        # Draw chart outer rectange.
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
        ctx.rectangle(0, 0, chart_width, chart_height)
        ctx.stroke()

        ctx.move_to(chart_width*chart_x_axis[0]/(chart_data_history-1), chart_height - chart_height*ram_usage_percent[0]/100)
        # Move drawing point (cairo context which is used for drawing on drawable objects) from data point to data point and connect them by a line in order to draw a curve.
        # First, move drawing point to the lower left corner of the chart and draw all data points one by one by going to the right direction.
        # Move drawing point to the next data points and connect them by a line.
        for i in range(len(chart_x_axis) - 1):
            # Distance to move on the horizontal and vertical axes.
            delta_x_chart1201 = (chart_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart_width * chart_x_axis[i]/(chart_data_history-1))
            delta_y_chart1201 = (chart_height*ram_usage_percent[i+1]/100) - (chart_height*ram_usage_percent[i]/100)
            # Move
            ctx.rel_line_to(delta_x_chart1201, -delta_y_chart1201)

        # Move drawing point 10 pixel right in order to go out of the visible drawing area for drawing a closed shape for filling the inner area.
        ctx.rel_line_to(10, 0)
        # Move drawing point "chart_height+10" down in order to stay out of the visible drawing area for drawing a closed shape for filling the inner area.
        ctx.rel_line_to(0, chart_height+10)
        # Move drawing point "chart1101_width+20" pixel left (by using a minus sign) in order to stay out of the visible drawing area for drawing a closed shape for filling the inner area.
        ctx.rel_line_to(-(chart_width+20), 0)
        # Move drawing point "chart_height+10" up in order to stay out of the visible drawing area for drawing a closed shape for filling the inner area.
        ctx.rel_line_to(0, -(chart_height+10))
        # Finally close the curve in order to fill the inner area which will represent a curve with a filled "below" area.
        ctx.close_path()
        # Use "stroke_preserve" in order to use the same area for filling. 
        ctx.stroke_preserve()
        # Change the color for filling operation.
        gradient_pattern = cairo.LinearGradient(0, 0, 0, chart_height)
        gradient_pattern.add_color_stop_rgba(0, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.55 * chart_line_color[3])
        gradient_pattern.add_color_stop_rgba(1, chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.10 * chart_line_color[3])
        ctx.set_source(gradient_pattern)
        # Fill the area
        ctx.fill()


    # ----------------------- Called for drawing Swap usage as bar chart -----------------------
    def on_drawingarea1202_draw(self, widget, ctx):

        try:
            swap_percent_check = self.swap_percent
        # "swap_percent" value is get in this module and drawingarea may try to use this value before relevant function (which provides this value) is finished.
        except AttributeError:
            return

        chart_line_color = Config.chart_line_color_ram_swap_percent
        chart_background_color = Config.chart_background_color_all_charts

        chart1202_width = Gtk.Widget.get_allocated_width(widget)
        chart1202_height = Gtk.Widget.get_allocated_height(widget)

        ctx.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        ctx.rectangle(0, 0, chart1202_width, chart1202_height)
        ctx.fill()

        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.6 * chart_line_color[3])
        ctx.rectangle(0, 0, chart1202_width, chart1202_height)
        ctx.stroke()
        ctx.set_line_width(1)
        ctx.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.3 * chart_line_color[3])
        ctx.rectangle(0, 0, chart1202_width*self.swap_percent/100, chart1202_height)
        ctx.fill()


    # ----------------------------------- RAM - Initial Function -----------------------------------
    def ram_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

        performance_ram_swap_data_precision = Config.performance_ram_swap_data_precision
        performance_ram_swap_data_unit = Config.performance_ram_swap_data_unit

        # Get total_physical_ram value (this value is very similar to RAM hardware size which is a bit different than ram_total value)
        # "block_size_bytes" file may not be present on some systems such as ARM CPU used systems. Currently kernel 5.10 does not have this feature but this feature will be included in the newer versions of the kernel.
        try:
            # "memory block size" is read from this file and size of the blocks depend on architecture (For more information see: https://www.kernel.org/doc/html/latest/admin-guide/mm/memory-hotplug.html).
            with open("/sys/devices/system/memory/block_size_bytes") as reader:
                # Value in this file is in hex form and it is converted into integer (byte)
                block_size = int(reader.read().strip(), 16)
        except FileNotFoundError:
            block_size = "-"
        if block_size != "-":
            total_online_memory = 0
            total_offline_memory = 0
            # Number of folders (of which name start with "memory") in this folder is multiplied with the integer value of "block_size_bytes" file content (hex value).
            files_in_sys_devices_system_memory = os.listdir("/sys/devices/system/memory/")
            for file in files_in_sys_devices_system_memory:
                if os.path.isdir("/sys/devices/system/memory/" + file) and file.startswith("memory"):
                    with open("/sys/devices/system/memory/" + file + "/online") as reader:
                        memory_online_offline_value = reader.read().strip()
                    if memory_online_offline_value == "1":
                        total_online_memory = total_online_memory + block_size
                    if memory_online_offline_value == "0":
                        total_offline_memory = total_offline_memory + block_size
            # Summation of total online and offline memories gives RAM hardware size. RAM harware size and total RAM value get from proc file system of by using "free" command are not same thing. Because some of the RAM may be reserved for harware and/or by the OS kernel.
            total_physical_ram = (total_online_memory + total_offline_memory)
        else:
            total_physical_ram = f'[{_tr("Unknown")}]'

        # Get ram_total and swap_total values
        with open("/proc/meminfo") as reader:
            proc_memory_info_output_lines = reader.read().split("\n")
        for line in proc_memory_info_output_lines:
            # Values in this file are in "KiB" unit. These values are multiplied with 1024 in order to obtain byte (nearly) values.
            if "MemTotal:" in line:
                ram_total = int(line.split()[1]) * 1024
            if "SwapTotal:" in line:
                swap_total = int(line.split()[1]) * 1024


        # Set RAM tab label texts by using information get
        self.label1201.set_text(_tr("Physical RAM") + ": " + str(self.performance_data_unit_converter_func(total_physical_ram, 0, 1)))    # f strings have lower CPU usage than joining method but strings are joinied by by this method because gettext could not be worked with Python f strings.
        self.label1202.set_text(_tr("Swap Memory") + ": " + str(self.performance_data_unit_converter_func(swap_total, 0, 1)))
        self.label1205.set_text(self.performance_data_unit_converter_func(ram_total, performance_ram_swap_data_unit, performance_ram_swap_data_precision))

        self.initial_already_run = 1


    # ----------------------------------- RAM - Get RAM Data Function -----------------------------------
    def ram_loop_func(self):

        ram_used = Performance.ram_used
        ram_usage_percent = Performance.ram_usage_percent
        ram_available = Performance.ram_available
        ram_free = Performance.ram_free

        performance_ram_swap_data_precision = Config.performance_ram_swap_data_precision
        performance_ram_swap_data_unit = Config.performance_ram_swap_data_unit

        self.drawingarea1201.queue_draw()
        self.drawingarea1202.queue_draw()

        # Get RAM usage values
        # Read total swap area and free swap area from /proc/meminfo file
        with open("/proc/meminfo") as reader:
            memory_info = reader.read().split("\n")
        for line in memory_info:
            if line.startswith("SwapTotal:"):
                swap_total = int(line.split()[1]) * 1024
            if line.startswith("SwapFree:"):
                swap_free = int(line.split()[1]) * 1024
        # Calculate values if swap memory exists.
        if swap_free != 0:
            swap_used = swap_total - swap_free
            self.swap_percent = swap_used / swap_total * 100
        # Set values as "0" if swap memory does not exist.
        if swap_free == 0:
            swap_used = 0
            self.swap_percent = 0


        # Set and update RAM tab label texts by using information get
        self.label1203.set_text(f'{self.performance_data_unit_converter_func(ram_used, performance_ram_swap_data_unit, performance_ram_swap_data_precision)} ({ram_usage_percent[-1]:.0f}%)')
        self.label1204.set_text(self.performance_data_unit_converter_func(ram_available, performance_ram_swap_data_unit, performance_ram_swap_data_precision))
        self.label1206.set_text(self.performance_data_unit_converter_func(ram_free, performance_ram_swap_data_unit, performance_ram_swap_data_precision))
        self.label1207.set_text(f'{self.swap_percent:.0f}%')
        self.label1208.set_text(f'{self.performance_data_unit_converter_func(swap_used, performance_ram_swap_data_unit, performance_ram_swap_data_precision)}')
        self.label1209.set_text(self.performance_data_unit_converter_func(swap_free, performance_ram_swap_data_unit, performance_ram_swap_data_precision))
        self.label1210.set_text(self.performance_data_unit_converter_func((swap_total), performance_ram_swap_data_unit, performance_ram_swap_data_precision))


# Generate object
Ram = Ram()


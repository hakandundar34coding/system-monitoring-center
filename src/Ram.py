#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os

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

        # Get chart functions from another module and define as local objects for lower CPU usage.
        self.performance_line_charts_draw_func = Performance.performance_line_charts_draw_func
        self.performance_line_charts_enter_notify_event_func = Performance.performance_line_charts_enter_notify_event_func
        self.performance_line_charts_leave_notify_event_func = Performance.performance_line_charts_leave_notify_event_func
        self.performance_line_charts_motion_notify_event_func = Performance.performance_line_charts_motion_notify_event_func
        self.performance_bar_charts_draw_func = Performance.performance_bar_charts_draw_func

        # Connect GUI signals
        self.button1201.connect("clicked", self.on_button1201_clicked)
        self.drawingarea1201.connect("draw", self.performance_line_charts_draw_func)
        self.drawingarea1201.connect("enter-notify-event", self.performance_line_charts_enter_notify_event_func)
        self.drawingarea1201.connect("leave-notify-event", self.performance_line_charts_leave_notify_event_func)
        self.drawingarea1201.connect("motion-notify-event", self.performance_line_charts_motion_notify_event_func)
        self.drawingarea1202.connect("draw", self.performance_bar_charts_draw_func)
        self.eventbox1201.connect("button-press-event", self.on_eventbox1201_button_click_event)
        self.eventbox1202.connect("button-press-event", self.on_eventbox1202_button_click_event)

        # Set event masks for drawingarea in order to enable these events.
        self.drawingarea1201.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK | Gdk.EventMask.POINTER_MOTION_MASK)


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
        if total_physical_ram != f'[{_tr("Unknown")}]':
            self.label1201.set_text(_tr("Physical RAM") + ": " + str(self.performance_data_unit_converter_func(total_physical_ram, 0, 1)))    # f strings have lower CPU usage than joining method but strings are joinied by by this method because gettext could not be worked with Python f strings.
        else:
             self.label1201.set_text(_tr("RAM") + " - " + _tr("Capacity") + ": " + self.performance_data_unit_converter_func(ram_total, performance_ram_swap_data_unit, performance_ram_swap_data_precision))
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


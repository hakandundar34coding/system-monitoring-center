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
class MemorySwapDetails:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MemorySwapDetailsWindow.ui")

        # Get GUI objects
        self.window1201w2 = builder.get_object('window1201w2')
        self.label1201w2 = builder.get_object('label1201w2')

        # Connect GUI signals
        self.window1201w2.connect("delete-event", self.on_window1201w2_delete_event)
        self.window1201w2.connect("show", self.on_window1201w2_show)


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window1201w2_delete_event(self, widget, event):

        widget.hide()
        return True


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window1201w2_show(self, widget):

        # Reset label text when window is shown.
        self.label1201w2.set_text("-")

        # Get and show swap memory information.
        self.memory_swap_details_run_func()


    # ----------------------------------- Memory - Swap Details Loop Function -----------------------------------
    def memory_swap_details_loop_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

        performance_memory_data_precision = Config.performance_memory_data_precision
        performance_memory_data_unit = Config.performance_memory_data_unit

        # This list is defined in order to make some command output strings to be translated into other languages.
        memory_swap_details_text_list = [_tr("Partition"), _tr("File")]

        # Set initial value of "memory_hardware_information_text". Hardware information will be appended to this string.
        swap_details_text = ""

        # Read "/proc/swaps" file for getting swap memory details. Systems may has more than one swap partition/file and this information can be read from this file.
        with open("/proc/swaps") as reader:
            proc_swaps_lines = reader.read().split("\n")

        # Delete header indormation which is get from "/proc/swaps" file.
        del proc_swaps_lines[0]

        for line in proc_swaps_lines:
            if line == "":
                break
            swap_name = "-"
            swap_type = "-"
            swap_size = "-"
            swap_used = "-"
            swap_priority = "-"
            line_split = line.split()
            swap_name = line_split[0].strip()
            swap_type = line_split[1].strip().title()
            # Values in this file are in KiB. They are converted to Bytes.
            swap_size = int(line_split[2].strip()) * 1024
            swap_size = f'{self.performance_data_unit_converter_func("data", "none", swap_size, performance_memory_data_unit, performance_memory_data_precision)}'
            swap_used = int(line_split[3].strip()) * 1024
            swap_used = f'{self.performance_data_unit_converter_func("data", "none", swap_used, performance_memory_data_unit, performance_memory_data_precision)}'
            swap_priority = line_split[4].strip()
            swap_details_text = swap_details_text + "\n" + _tr("Name") + " :    " + swap_name
            swap_details_text = swap_details_text + "\n" + _tr("Type") + " :    " + _tr(swap_type)
            swap_details_text = swap_details_text + "\n" + _tr("Capacity") + " :    " + swap_size
            swap_details_text = swap_details_text + "\n" + _tr("Used") + " :    " + swap_used
            swap_details_text = swap_details_text + "\n" + _tr("Priority") + " :    " + swap_priority
            swap_details_text = swap_details_text + "\n"
            swap_details_text = swap_details_text + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"

        # In order to remove this string from the last line.
        swap_details_text = swap_details_text.strip("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")

        # Delete empty lines at the beginning and end of the string.
        swap_details_text = swap_details_text.strip()

        if swap_details_text.strip() == "":
            swap_details_text = "-"

        self.label1201w2.set_text(swap_details_text)


    # ----------------------------------- Memory - Swap Details - Run Function -----------------------------------
    def memory_swap_details_run_func(self):

        if self.window1201w2.get_visible() == True:
            GLib.idle_add(self.memory_swap_details_loop_func)
            GLib.timeout_add(Config.update_interval * 1000, self.memory_swap_details_run_func)


# Generate object
MemorySwapDetails = MemorySwapDetails()


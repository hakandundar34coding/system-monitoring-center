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
class FloatingSummary:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/FloatingSummaryWindow.ui")

        # Get GUI objects
        self.window3001 = builder.get_object('window3001')
        self.grid3001 = builder.get_object('grid3001')
        self.label3001 = builder.get_object('label3001')
        self.label3002 = builder.get_object('label3002')
        self.label3003 = builder.get_object('label3003')
        self.label3004 = builder.get_object('label3004')
        self.label3005 = builder.get_object('label3005')
        self.label3006 = builder.get_object('label3006')
        self.label3007 = builder.get_object('label3007')
        self.label3008 = builder.get_object('label3008')

        # Connect GUI signals
        self.window3001.connect("button-press-event", self.on_window3001_button_press_event)

        # Prevent window to be resized, hide it on the taskbar, hide its window title/border and keep it on top of all windows.
        self.window3001.set_resizable(False)
        self.window3001.set_skip_taskbar_hint(True)
        self.window3001.set_decorated(False)
        self.window3001.set_keep_above(True)

        # Floating Summary window is closed when main window is closed (when application is run as running a desktop application). But it is not closed when main window is closed if application is run from an IDE for debugging/developing purposes.

        # Run initial function
        self.floating_summary_initial_func()


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window3001_show(self, widget):

        # Run loop function to show data immediately without waiting the update interval in the main window module.
        self.floating_summary_loop_func()


    # ----------------------- Called for clicking and dragging the window -----------------------
    def on_window3001_button_press_event(self, widget, event):

        if event.button == 1:
            widget.begin_move_drag(event.button, event.x_root, event.y_root, event.time)


    # ----------------------------------- FloatingSummary - Initial Function -----------------------------------
    def floating_summary_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()


    # ----------------------------------- FloatingSummary - Loop Function -----------------------------------
    def floating_summary_loop_func(self):

        # Set transperancy of the window.
        self.window3001.set_opacity(Config.floating_summary_window_transparency)

        floating_summary_data_shown_prev = []
        floating_summary_data_shown = Config.floating_summary_data_shown
        # Remove all labels and add preferred ones if user makes changes on visible performance data (labels).
        if floating_summary_data_shown != floating_summary_data_shown_prev:
            # 9 is large enough to remove all labels on the grid.
            for i in reversed(range(9)):
                try:
                    label_to_remove = self.grid3001.get_child_at(0, i)
                    self.grid3001.remove(label_to_remove)
                except Exception:
                    pass

            grid_row_count = 0
            # Attach label for average CPU usage percent data
            if 0 in floating_summary_data_shown:
                grid_row_count = 0
                self.grid3001.attach(self.label3001, 0, grid_row_count, 1, 1)
            # Attach label for RAM usage percent data
            if 1 in floating_summary_data_shown:
                grid_row_count = grid_row_count + 1
                self.grid3001.attach(self.label3002, 0, grid_row_count, 1, 1)
            # Attach label for disk read+write speed data
            if 2 in floating_summary_data_shown:
                grid_row_count = grid_row_count + 1
                self.grid3001.attach(self.label3003, 0, grid_row_count, 1, 1)
            # Attach label for disk read speed data
            if 3 in floating_summary_data_shown:
                grid_row_count = grid_row_count + 1
                self.grid3001.attach(self.label3004, 0, grid_row_count, 1, 1)
            # Attach label for disk write speed data
            if 4 in floating_summary_data_shown:
                grid_row_count = grid_row_count + 1
                self.grid3001.attach(self.label3005, 0, grid_row_count, 1, 1)
            # Attach label for network download+upload speed data
            if 5 in floating_summary_data_shown:
                grid_row_count = grid_row_count + 1
                self.grid3001.attach(self.label3006, 0, grid_row_count, 1, 1)
            # Attach label for network download speed data
            if 6 in floating_summary_data_shown:
                grid_row_count = grid_row_count + 1
                self.grid3001.attach(self.label3007, 0, grid_row_count, 1, 1)
            # Attach label for network upload speed data
            if 7 in floating_summary_data_shown:
                grid_row_count = grid_row_count + 1
                self.grid3001.attach(self.label3008, 0, grid_row_count, 1, 1)

        # list1 = list(list2) have to be used for proper working of the code because using this equation without "list()" makes a connection between these lists instead of copying one list with a different variable name.
        floating_summary_data_shown_prev = list(floating_summary_data_shown)

        # Set label texts for showing peformance data
        if 0 in floating_summary_data_shown:
            self.label3001.set_text(_tr("CPU") + ": " + f'{Performance.cpu_usage_percent_ave[-1]:.0f} %')
        if 1 in floating_summary_data_shown:
            self.label3002.set_text(_tr("RAM") + ": " + f'{Performance.ram_usage_percent[-1]:.0f} %')
        if 2 in floating_summary_data_shown:
            self.label3003.set_text(_tr("Disk R+W") + ": " + f'{self.performance_data_unit_converter_func((Performance.disk_read_speed[Performance.selected_disk_number][-1] + Performance.disk_write_speed[Performance.selected_disk_number][-1]), 0, 2)}/s')
        if 3 in floating_summary_data_shown:
            self.label3004.set_text(_tr("Disk R") + ": " + f'{self.performance_data_unit_converter_func(Performance.disk_read_speed[Performance.selected_disk_number][-1], 0, 2)}/s')
        if 4 in floating_summary_data_shown:
            self.label3005.set_text(_tr("Disk W") + ": " + f'{self.performance_data_unit_converter_func(Performance.disk_write_speed[Performance.selected_disk_number][-1], 0, 2)}/s')
        if 5 in floating_summary_data_shown:
            self.label3006.set_text(_tr("Network D+U") + ": " + f'{self.performance_data_unit_converter_func((Performance.network_receive_speed[Performance.selected_network_card_number][-1] + Performance.network_send_speed[Performance.selected_network_card_number][-1]), 0, 2)}/s')
        if 6 in floating_summary_data_shown:
            self.label3007.set_text(_tr("Network D") + ": " + f'{self.performance_data_unit_converter_func(Performance.network_receive_speed[Performance.selected_network_card_number][-1], 0, 2)}/s')
        if 7 in floating_summary_data_shown:
            self.label3008.set_text(_tr("Network U") + ": " + f'{self.performance_data_unit_converter_func(Performance.network_send_speed[Performance.selected_network_card_number][-1], 0, 2)}/s')


# Generate object
FloatingSummary = FloatingSummary()


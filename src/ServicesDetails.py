#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib
import os
import subprocess
import time
from datetime import datetime

from locale import gettext as _tr

from Config import Config
import Services
from Performance import Performance


# Define class
class ServicesDetails:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder6101w = Gtk.Builder()
        builder6101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ServicesDetailsWindow.ui")

        # Get GUI objects
        self.window6101w = builder6101w.get_object('window6101w')
        self.notebook6101w = builder6101w.get_object('notebook6101w')
        # Service Details window "General" tab GUI objects
        self.label6101w = builder6101w.get_object('label6101w')
        self.label6102w = builder6101w.get_object('label6102w')
        self.label6103w = builder6101w.get_object('label6103w')
        self.label6104w = builder6101w.get_object('label6104w')
        self.label6105w = builder6101w.get_object('label6105w')
        self.label6106w = builder6101w.get_object('label6106w')
        self.label6107w = builder6101w.get_object('label6107w')
        self.label6108w = builder6101w.get_object('label6108w')
        self.label6109w = builder6101w.get_object('label6109w')
        self.label6110w = builder6101w.get_object('label6110w')
        self.label6114w = builder6101w.get_object('label6114w')
        self.label6115w = builder6101w.get_object('label6115w')
        self.label6117w = builder6101w.get_object('label6117w')
        self.label6118w = builder6101w.get_object('label6118w')
        # Service Details window "Dependencies" tab GUI objects
        self.label6119w = builder6101w.get_object('label6119w')
        self.label6120w = builder6101w.get_object('label6120w')
        self.label6121w = builder6101w.get_object('label6121w')
        self.label6122w = builder6101w.get_object('label6122w')

        # Connect GUI signals
        self.window6101w.connect("delete-event", self.on_window6101w_delete_event)
        self.window6101w.connect("show", self.on_window6101w_show)


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window6101w_delete_event(self, widget, event):

        self.update_window_value = 0
        self.window6101w.hide()
        return True


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window6101w_show(self, widget):

        try:
            # Delete "update_interval" variable in order to let the code to run initial function. Otherwise, data from previous service (if it was viewed) will be used.
            del self.update_interval
        except AttributeError:
            pass

        # This value is checked for repeating the function for getting the service data.
        self.update_window_value = 1

        # Call this function in order to reset Services Details window GUI.
        self.services_details_gui_reset_function()
        self.services_details_run_func()


    # ----------------------- Called for resetting window GUI -----------------------
    def services_details_gui_reset_function(self):

        # Switch to fist page (Summary tab) of the notebook.
        self.notebook6101w.set_current_page(0)

        self.label6101w.set_text("--")
        self.label6102w.set_text("--")
        self.label6103w.set_text("--")
        self.label6104w.set_text("--")
        self.label6105w.set_text("--")
        self.label6106w.set_text("--")
        self.label6107w.set_text("--")
        self.label6108w.set_text("--")
        self.label6109w.set_text("--")
        self.label6110w.set_text("--")
        self.label6114w.set_text("--")
        self.label6115w.set_text("--")
        self.label6117w.set_text("--")
        self.label6118w.set_text("--")
        self.label6119w.set_text("--")
        self.label6120w.set_text("--")
        self.label6121w.set_text("--")
        self.label6122w.set_text("--")


    # ----------------------------------- Services - Services Details Function (the code of this module in order to avoid running them during module import and defines "Services" tab GUI objects and functions/signals) -----------------------------------
    def services_details_initial_func(self):

        # Define data unit conversion function objects in for lower CPU usage.
        self.performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        self.performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        self.performance_define_data_unit_converter_variables_func()

        # Get right clicked service name.
        self.selected_service_name = Services.selected_service_name

        # Get system boot time (will be used for appending to process start times to get process start times as date time.)
        with open("/proc/stat") as reader:
            stat_lines = reader.read().split("\n")
        for line in stat_lines:
            if "btime " in line:
                self.system_boot_time = int(line.split()[1].strip())

        # These lists are defined in order to make these texts translatable to other languages. String names are capitalized here as they are capitalized in the code by using ".capitalize()" in order to use translated strings.
        service_state_list = [_tr("Enabled"), _tr("Disabled"), _tr("Masked"), _tr("Unmasked"), _tr("Static"), _tr("Generated"), _tr("Enabled-runtime"), _tr("Indirect"), _tr("Active"), _tr("Inactive"), _tr("Loaded"), _tr("Dead"), _tr("Exited"), _tr("Running")]
        services_other_text_list = [_tr("Yes"), _tr("No")]


    # ----------------------------------- Services - Services Details Foreground Function -----------------------------------
    def services_details_loop_func(self):

        services_memory_data_precision = Config.services_memory_data_precision
        services_memory_data_unit = Config.services_memory_data_unit

        # Get all information of the service.
        systemctl_show_lines = (subprocess.check_output(["systemctl", "show", self.selected_service_name], shell=False)).decode().strip().split("\n")

        # Initial value of the variables. These values will be used if they could not be detected.
        selected_service_type = "-"
        selected_service_main_pid = "-"
        selected_service_exec_main_start_times_stamp_monotonic = "-"
        selected_service_exec_main_exit_times_stamp_monotonic ="-"
        selected_service_memory_current = "-"
        selected_service_requires = "-"
        selected_service_conflicts = "-"
        selected_service_after = "-"
        selected_service_before = "-"
        selected_service_triggered_by = "-"
        selected_service_documentation = "-"
        selected_service_description = "-"
        selected_service_active_state = "-"
        selected_service_load_state = "-"
        selected_service_sub_state = "-"
        selected_service_fragment_path = "-"
        selected_service_unit_file_state = "-"
        selected_service_unit_file_preset = "-"

        for line in systemctl_show_lines:
            if "Type=" in line:
                selected_service_type = _tr(line.split("=")[1].capitalize())
                # Skip to next loop if searched line ("Type=") is found in order to avoid redundant line search.
                continue
            if "MainPID=" in line:
                selected_service_main_pid = line.split("=")[1]
                continue
            if "ExecMainStartTimestampMonotonic=" in line:
                line_split = line.split("=")[1]
                if line_split != "0":
                    # Time is read from the service file (in microseconds), divided by 1000000 in order to obtain time in seconds and appended to system boot time for getting service start time. Because time data is get as "elapsed time after system boot" from the file.
                    selected_service_exec_main_start_times_stamp_monotonic = int(line.split("=")[1])/1000000 + self.system_boot_time
                    selected_service_exec_main_start_times_stamp_monotonic = datetime.fromtimestamp(selected_service_exec_main_start_times_stamp_monotonic).strftime("%d.%m.%Y %H:%M:%S")
                if line_split == "0":
                    selected_service_exec_main_start_times_stamp_monotonic = "-"
                continue
            if "ExecMainExitTimestampMonotonic=" in line:
                line_split = line.split("=")[1]
                if line_split != "0":
                    # Time is read from the service file (in microseconds), divided by 1000000 in order to obtain time in seconds and appended to system boot time for getting service start time. Because time data is get as "elapsed time after system boot" from the file.
                    selected_service_exec_main_exit_times_stamp_monotonic = int(line.split("=")[1])/1000000 + self.system_boot_time
                    selected_service_exec_main_exit_times_stamp_monotonic = datetime.fromtimestamp(selected_service_exec_main_exit_times_stamp_monotonic).strftime("%d.%m.%Y %H:%M:%S")
                if line_split == "0":
                    selected_service_exec_main_exit_times_stamp_monotonic = "-"
                continue
            if "MemoryCurrent=" in line:
                selected_service_memory_current = line.split("=")[1]
                if selected_service_memory_current == "-" or selected_service_memory_current == "[not set]":
                    selected_service_memory_current = "-"
                else:
                    try:
                        selected_service_memory_current = f'{self.performance_data_unit_converter_func("data", "none", int(selected_service_memory_current), services_memory_data_unit, services_memory_data_precision)}'
                    except Exception:
                        selected_service_memory_current = "-"
                continue
            if "Requires=" in line:
                selected_service_requires = sorted(line.split("=")[1].split())
                continue
            if "Conflicts=" in line:
                selected_service_conflicts = sorted(line.split("=")[1].split())
                continue
            if "After=" in line:
                selected_service_after = sorted(line.split("=")[1].split())
                continue
            if "Before=" in line:
                selected_service_before = sorted(line.split("=")[1].split())
                continue
            if "TriggeredBy=" in line:
                selected_service_triggered_by = line.split("=")[1]
                continue
            if "Documentation=" in line:
                selected_service_documentation = line.split("=")[1].split()
                # Convert string into multi-line string if there are more than one documentation information.
                selected_service_documentation_scratch = []
                for documentation in selected_service_documentation:
                    selected_service_documentation_scratch.append(documentation.strip('"'))
                selected_service_documentation = selected_service_documentation_scratch
                continue
            if "Description=" in line:
                selected_service_description = line.split("=")[1]
                continue
            if "ActiveState=" in line:
                selected_service_active_state = _tr(line.split("=")[1].capitalize())
                continue
            if "LoadState=" in line:
                selected_service_load_state = _tr(line.split("=")[1].capitalize())
                continue
            if "SubState=" in line:
                selected_service_sub_state = _tr(line.split("=")[1].capitalize())
                continue
            if "FragmentPath=" in line:
                selected_service_fragment_path = line.split("=")[1]
                continue
            if "UnitFileState=" in line:
                selected_service_unit_file_state = _tr(line.split("=")[1].capitalize())
                continue
            if "UnitFilePreset=" in line:
                selected_service_unit_file_preset = _tr(line.split("=")[1].capitalize())
                continue


        # Set label text by using service data
        self.label6101w.set_text(self.selected_service_name)
        self.label6102w.set_text(selected_service_description)
        self.label6103w.set_text(f'{selected_service_unit_file_state} - {selected_service_unit_file_preset}')
        self.label6104w.set_text(selected_service_load_state)
        self.label6105w.set_text(selected_service_active_state)
        self.label6106w.set_text(selected_service_sub_state)
        self.label6107w.set_text(selected_service_fragment_path)
        self.label6108w.set_text(',\n'.join(selected_service_documentation))
        self.label6109w.set_text(selected_service_triggered_by)
        self.label6110w.set_text(selected_service_main_pid)
        self.label6114w.set_text(selected_service_exec_main_start_times_stamp_monotonic)
        self.label6115w.set_text(selected_service_exec_main_exit_times_stamp_monotonic)
        self.label6117w.set_text(selected_service_type)
        self.label6118w.set_text(selected_service_memory_current)
        self.label6119w.set_text(',\n'.join(selected_service_requires))
        self.label6120w.set_text(',\n'.join(selected_service_conflicts))
        self.label6121w.set_text(',\n'.join(selected_service_after))
        self.label6122w.set_text(',\n'.join(selected_service_before))


    # ----------------------------------- Services Details - Run Function -----------------------------------
    # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to change the update interval and run the loop again without waiting ending the previous update interval.
    def services_details_run_func(self, *args):

        if hasattr(ServicesDetails, "update_interval") == False:
            GLib.idle_add(self.services_details_initial_func)

        # Destroy GLib source for preventing it repeating the function.
        try:
            self.main_glib_source.destroy()
        # "try-except" is used in order to prevent errors if this is first run of the function.
        except AttributeError:
            pass
        self.update_interval = Config.update_interval
        self.main_glib_source = GLib.timeout_source_new(self.update_interval * 1000)

        if self.update_window_value == 1:
            GLib.idle_add(self.services_details_loop_func)
            self.main_glib_source.set_callback(self.services_details_run_func)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


# Generate object
ServicesDetails = ServicesDetails()


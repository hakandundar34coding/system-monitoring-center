import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

import os
import time
import subprocess
from datetime import datetime

from locale import gettext as _tr

from Config import Config
from Services import Services
from Performance import Performance
from MainWindow import MainWindow
import Common


class ServicesDetails:

    def __init__(self):

        self.window_gui()


    def window_gui(self):
        """
        Generate window GUI.
        """

        # Window
        self.service_details_window = Gtk.Window()
        self.service_details_window.set_default_size(500, 435)
        self.service_details_window.set_title(_tr("Service Details"))
        self.service_details_window.set_icon_name("system-monitoring-center")
        self.service_details_window.set_transient_for(MainWindow.main_window)
        self.service_details_window.set_modal(True)
        self.service_details_window.set_hide_on_close(True)

        # Grid
        self.main_grid = Gtk.Grid()
        self.service_details_window.set_child(self.main_grid)

        # Notebook
        notebook = Gtk.Notebook()
        notebook.set_margin_top(10)
        notebook.set_margin_bottom(10)
        notebook.set_margin_start(10)
        notebook.set_margin_end(10)
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)
        self.main_grid.attach(notebook, 0, 0, 1, 1)

        # Tab pages and ScrolledWindow
        # "Summary" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("Summary"))
        self.scrolledwindow_summary_tab = Gtk.ScrolledWindow()
        notebook.append_page(self.scrolledwindow_summary_tab, tab_title_label)
        # "Dependencies" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("Dependencies"))
        self.scrolledwindow_dependencies_tab = Gtk.ScrolledWindow()
        notebook.append_page(self.scrolledwindow_dependencies_tab, tab_title_label)

        self.summary_tab_gui()
        self.dependencies_tab_gui()

        self.gui_signals()


    def summary_tab_gui(self):
        """
        Generate "Summary" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_summary_tab.set_child(viewport)

        # Grid
        grid = Common.window_main_grid()
        viewport.set_child(grid)

        # Label (Name)
        label = Common.static_information_label(_tr("Name"))
        grid.attach(label, 0, 0, 1, 1)
        # Label (Name)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 0, 1, 1)
        # Label (Name)
        self.name_label = Common.dynamic_information_label()
        grid.attach(self.name_label, 2, 0, 1, 1)

        # Label (Description)
        label = Common.static_information_label(_tr("Description"))
        grid.attach(label, 0, 1, 1, 1)
        # Label (Description)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 1, 1, 1)
        # Label (Description)
        self.description_label = Common.dynamic_information_label()
        grid.attach(self.description_label, 2, 1, 1, 1)

        # Label (Unit File State - Preset)
        label = Common.static_information_label(_tr("Unit File State - Preset"))
        grid.attach(label, 0, 2, 1, 1)
        # Label (Unit File State - Preset)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 2, 1, 1)
        # Label (Unit File State - Preset)
        self.unit_file_state_label = Common.dynamic_information_label()
        grid.attach(self.unit_file_state_label, 2, 2, 1, 1)

        # Label (Load State)
        label = Common.static_information_label(_tr("Load State"))
        grid.attach(label, 0, 3, 1, 1)
        # Label (Load State)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 3, 1, 1)
        # Label (Load State)
        self.load_state_label = Common.dynamic_information_label()
        grid.attach(self.load_state_label, 2, 3, 1, 1)

        # Label (Active State)
        label = Common.static_information_label(_tr("Active State"))
        grid.attach(label, 0, 4, 1, 1)
        # Label (Active State)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 4, 1, 1)
        # Label (Active State)
        self.active_state_label = Common.dynamic_information_label()
        grid.attach(self.active_state_label, 2, 4, 1, 1)

        # Label (Sub-State)
        label = Common.static_information_label(_tr("Sub-State"))
        grid.attach(label, 0, 5, 1, 1)
        # Label (Sub-State)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 5, 1, 1)
        # Label (Sub-State)
        self.sub_state_label = Common.dynamic_information_label()
        grid.attach(self.sub_state_label, 2, 5, 1, 1)

        # Label (Path)
        label = Common.static_information_label(_tr("Path"))
        grid.attach(label, 0, 6, 1, 1)
        # Label (Path)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 6, 1, 1)
        # Label (Path)
        self.path_label = Common.dynamic_information_label()
        grid.attach(self.path_label, 2, 6, 1, 1)

        # Label (Documentation)
        label = Common.static_information_label(_tr("Documentation"))
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 7, 1, 1)
        # Label (Documentation)
        label = Common.static_information_label(":")
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 7, 1, 1)
        # Label (Documentation)
        self.documentation_label = Common.dynamic_information_label()
        grid.attach(self.documentation_label, 2, 7, 1, 1)

        # Label (Triggered By)
        label = Common.static_information_label(_tr("Triggered By"))
        grid.attach(label, 0, 8, 1, 1)
        # Label (Triggered By)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 8, 1, 1)
        # Label (Triggered By)
        self.triggered_by_label = Common.dynamic_information_label()
        grid.attach(self.triggered_by_label, 2, 8, 1, 1)

        # Label (Main PID)
        label = Common.static_information_label(_tr("Main PID"))
        grid.attach(label, 0, 9, 1, 1)
        # Label (Main PID)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 9, 1, 1)
        # Label (Main PID)
        self.main_pid_label = Common.dynamic_information_label()
        grid.attach(self.main_pid_label, 2, 9, 1, 1)

        # Label (Main Process Start Time)
        label = Common.static_information_label(_tr("Main Process Start Time"))
        grid.attach(label, 0, 10, 1, 1)
        # Label (Main Process Start Time)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 10, 1, 1)
        # Label (Main Process Start Time)
        self.main_process_start_time_label = Common.dynamic_information_label()
        grid.attach(self.main_process_start_time_label, 2, 10, 1, 1)

        # Label (Main Process End Time)
        label = Common.static_information_label(_tr("Main Process End Time"))
        grid.attach(label, 0, 11, 1, 1)
        # Label (Main Process End Time)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 11, 1, 1)
        # Label (Main Process End Time)
        self.main_process_end_time_label = Common.dynamic_information_label()
        grid.attach(self.main_process_end_time_label, 2, 11, 1, 1)

        # Label (Type)
        label = Common.static_information_label(_tr("Type"))
        grid.attach(label, 0, 12, 1, 1)
        # Label (Type)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 12, 1, 1)
        # Label (Type)
        self.type_label = Common.dynamic_information_label()
        grid.attach(self.type_label, 2, 12, 1, 1)

        # Label (Memory (RSS))
        label = Common.static_information_label(_tr("Memory (RSS)"))
        grid.attach(label, 0, 13, 1, 1)
        # Label (Memory (RSS))
        label = Common.static_information_label(":")
        grid.attach(label, 1, 13, 1, 1)
        # Label (Memory (RSS))
        self.memory_rss_label = Common.dynamic_information_label()
        grid.attach(self.memory_rss_label, 2, 13, 1, 1)


    def dependencies_tab_gui(self):
        """
        Generate "Dependencies" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_dependencies_tab.set_child(viewport)

        # Grid
        grid = Common.window_main_grid()
        viewport.set_child(grid)

        # Label (Requires)
        label = Common.static_information_label(_tr("Requires"))
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 0, 1, 1)
        # Label (Requires)
        label = Common.static_information_label(":")
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 0, 1, 1)
        # Label (Requires)
        self.requires_label = Common.dynamic_information_label()
        grid.attach(self.requires_label, 2, 0, 1, 1)

        # Label (Conflicts)
        label = Common.static_information_label(_tr("Conflicts"))
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)
        # Label (Conflicts)
        label = Common.static_information_label(":")
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 1, 1, 1)
        # Label (Conflicts)
        self.conflicts_label = Common.dynamic_information_label()
        grid.attach(self.conflicts_label, 2, 1, 1, 1)

        # Label (After)
        label = Common.static_information_label(_tr("After"))
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)
        # Label (After)
        label = Common.static_information_label(":")
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 2, 1, 1)
        # Label (After)
        self.after_label = Common.dynamic_information_label()
        grid.attach(self.after_label, 2, 2, 1, 1)

        # Label (Before)
        label = Common.static_information_label(_tr("Before"))
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)
        # Label (Before)
        label = Common.static_information_label(":")
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 3, 1, 1)
        # Label (Before)
        self.before_label = Common.dynamic_information_label()
        grid.attach(self.before_label, 2, 3, 1, 1)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # Window signals
        self.service_details_window.connect("close-request", self.on_service_details_window_delete_event)
        self.service_details_window.connect("show", self.on_service_details_window_show)


    def on_service_details_window_delete_event(self, widget):
        """
        Called when window is closed.
        """

        self.update_window_value = 0
        self.service_details_window.hide()
        return True


    def on_service_details_window_show(self, widget):
        """
        Run code after window is shown.
        """

        try:
            # Delete "update_interval" variable in order to let the code to run initial function.
            # Otherwise, data from previous service (if it was viewed) will be used.
            del self.update_interval
        except AttributeError:
            pass

        # This value is checked for repeating the function for getting the service data.
        self.update_window_value = 1

        self.services_details_run_func()


    def services_details_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

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


    def services_details_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        services_memory_data_precision = Config.services_memory_data_precision
        services_memory_data_unit = Config.services_memory_data_unit

        selected_service_name = Services.selected_service_name

        # Get all information of the service.
        command_list = ["systemctl", "show", selected_service_name]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        systemctl_show_lines = (subprocess.check_output(command_list, shell=False)).decode().strip().split("\n")

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
                        selected_service_memory_current = f'{Performance.performance_data_unit_converter_func("data", "none", int(selected_service_memory_current), services_memory_data_unit, services_memory_data_precision)}'
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
        self.name_label.set_label(self.selected_service_name)
        self.description_label.set_label(selected_service_description)
        self.unit_file_state_label.set_label(f'{selected_service_unit_file_state} - {selected_service_unit_file_preset}')
        self.load_state_label.set_label(selected_service_load_state)
        self.active_state_label.set_label(selected_service_active_state)
        self.sub_state_label.set_label(selected_service_sub_state)
        self.path_label.set_label(selected_service_fragment_path)
        self.documentation_label.set_label(',\n'.join(selected_service_documentation))
        self.triggered_by_label.set_label(selected_service_triggered_by)
        self.main_pid_label.set_label(selected_service_main_pid)
        self.main_process_start_time_label.set_label(selected_service_exec_main_start_times_stamp_monotonic)
        self.main_process_end_time_label.set_label(selected_service_exec_main_exit_times_stamp_monotonic)
        self.type_label.set_label(selected_service_type)
        self.memory_rss_label.set_label(selected_service_memory_current)
        self.requires_label.set_label(',\n'.join(selected_service_requires))
        self.conflicts_label.set_label(',\n'.join(selected_service_conflicts))
        self.after_label.set_label(',\n'.join(selected_service_after))
        self.before_label.set_label(',\n'.join(selected_service_before))


    def services_details_run_func(self, *args):
        """
        Run initial and loop functions of service details window.
        "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()".
        "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to change the update interval and
        run the loop again without waiting ending the previous update interval.
        """

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


ServicesDetails = ServicesDetails()


import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

import os
import time
import subprocess
from datetime import datetime

from .Config import Config
from .Services import Services
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


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
        self.notebook = Gtk.Notebook()
        self.notebook.set_margin_top(10)
        self.notebook.set_margin_bottom(10)
        self.notebook.set_margin_start(10)
        self.notebook.set_margin_end(10)
        self.notebook.set_hexpand(True)
        self.notebook.set_vexpand(True)
        self.main_grid.attach(self.notebook, 0, 0, 1, 1)

        # Tab pages and ScrolledWindow
        # "Summary" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("Summary"))
        self.scrolledwindow_summary_tab = Gtk.ScrolledWindow()
        self.notebook.append_page(self.scrolledwindow_summary_tab, tab_title_label)
        # "Dependencies" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("Dependencies"))
        self.scrolledwindow_dependencies_tab = Gtk.ScrolledWindow()
        self.notebook.append_page(self.scrolledwindow_dependencies_tab, tab_title_label)

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
        label = Common.static_information_label(_tr("Unit File State") + " - " + _tr("Preset"))
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
        self.service_details_window.connect("close-request", self.on_service_details_window_close_request_event)
        self.service_details_window.connect("show", self.on_service_details_window_show)


    def on_service_details_window_close_request_event(self, widget):
        """
        Called when window is closed.
        """

        self.update_window_value = 0
        self.service_details_window.set_visible(False)


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

        # Select first tab of the notebook when the window is hidden and shown again.
        self.notebook.set_current_page(0)
        self.services_details_run_func()


    def services_details_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        # Get right clicked service name.
        self.selected_service_name = Services.selected_service_name

        # Get system boot time (will be used for appending to process start times to get process start times as date time.)
        self.system_boot_time = Libsysmon.get_system_boot_time()


    def services_details_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        services_memory_data_precision = Config.services_memory_data_precision
        services_memory_data_unit = Config.services_memory_data_unit

        selected_service_name = Services.selected_service_name

        service_detailed_info_dict = Libsysmon.get_service_detailed_information(selected_service_name)

        # Set label text by using service data
        self.name_label.set_label(self.selected_service_name)
        self.description_label.set_label(service_detailed_info_dict["description"])
        self.unit_file_state_label.set_label(service_detailed_info_dict["unit_file_state"] + " - " + service_detailed_info_dict["unit_file_preset"])
        self.load_state_label.set_label(service_detailed_info_dict["load_state"])
        self.active_state_label.set_label(service_detailed_info_dict["active_state"])
        self.sub_state_label.set_label(service_detailed_info_dict["sub_state"])
        self.path_label.set_label(service_detailed_info_dict["fragment_path"])
        self.documentation_label.set_label(',\n'.join(service_detailed_info_dict["documentation"]))
        self.triggered_by_label.set_label(service_detailed_info_dict["triggered_by"])
        self.main_pid_label.set_label(service_detailed_info_dict["main_pid"])
        self.main_process_start_time_label.set_label(service_detailed_info_dict["exec_main_start_times_stamp_monotonic"])
        self.main_process_end_time_label.set_label(service_detailed_info_dict["exec_main_exit_times_stamp_monotonic"])
        self.type_label.set_label(service_detailed_info_dict["service_type"])
        if service_detailed_info_dict["memory_current"] != -1:
            memory_current = f'{Libsysmon.data_unit_converter("data", "none", service_detailed_info_dict["memory_current"], services_memory_data_unit, services_memory_data_precision)}'
        else:
            memory_current = "-"
        self.memory_rss_label.set_label(memory_current)
        self.requires_label.set_label(',\n'.join(service_detailed_info_dict["requires"]))
        self.conflicts_label.set_label(',\n'.join(service_detailed_info_dict["conflicts"]))
        self.after_label.set_label(',\n'.join(service_detailed_info_dict["after"]))
        self.before_label.set_label(',\n'.join(service_detailed_info_dict["before"]))


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


import tkinter as tk
from tkinter import ttk

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

        #self.window_gui()
        pass


    def window_gui(self):
        """
        Generate window GUI.
        """

        # Window (Service Details)
        self.service_details_window, frame = Common.window(MainWindow.main_window, _tr("Service Details"))

        # Notebook
        notebook = ttk.Notebook(frame)
        notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Summary Tab
        self.frame_summary_tab = tk.Frame(notebook)
        notebook.add(self.frame_summary_tab, text=_tr("Summary"))
        #self.frame_summary_tab.grid_configure(ipadx=10, ipady=10)

        # Dependencies Tab
        self.frame_dependencies_tab = tk.Frame(notebook)
        notebook.add(self.frame_dependencies_tab, text=_tr("Dependencies"))

        self.summary_tab_gui()
        self.dependencies_tab_gui()

        self.gui_signals()


    def summary_tab_gui(self):
        """
        Generate "Summary" tab GUI objects.
        """

        # Label (Name)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Name"))
        label.grid(row=0, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Name)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=0, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Name)
        self.name_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.name_label.grid(row=0, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Description)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Description"))
        label.grid(row=1, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Description)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=1, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Description)
        self.description_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.description_label.grid(row=1, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Unit File State - Preset)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Unit File State") + " - " + _tr("Preset"))
        label.grid(row=2, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Unit File State - Preset)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=2, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Unit File State - Preset)
        self.unit_file_state_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.unit_file_state_label.grid(row=2, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Load State)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Load State"))
        label.grid(row=3, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Load State)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=3, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Load State)
        self.load_state_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.load_state_label.grid(row=3, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Active State)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Active State"))
        label.grid(row=4, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Active State)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=4, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Active State)
        self.active_state_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.active_state_label.grid(row=4, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Sub-State)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Sub-State"))
        label.grid(row=5, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Sub-State)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=5, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Sub-State)
        self.sub_state_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.sub_state_label.grid(row=5, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Path)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Path"))
        label.grid(row=6, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Path)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=6, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Path)
        self.path_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.path_label.grid(row=6, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Documentation)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Documentation"))
        label.grid(row=7, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Documentation)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=7, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Documentation)
        self.documentation_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.documentation_label.grid(row=7, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Triggered By)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Triggered By"))
        label.grid(row=8, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Triggered By)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=8, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Triggered By)
        self.triggered_by_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.triggered_by_label.grid(row=8, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Main PID)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Main PID"))
        label.grid(row=9, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Main PID)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=9, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Main PID)
        self.main_pid_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.main_pid_label.grid(row=9, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Main Process Start Time)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Main Process Start Time"))
        label.grid(row=10, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Main Process Start Time)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=10, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Main Process Start Time)
        self.main_process_start_time_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.main_process_start_time_label.grid(row=10, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Main Process End Time)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Main Process End Time"))
        label.grid(row=11, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Main Process End Time)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=11, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Main Process End Time)
        self.main_process_end_time_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.main_process_end_time_label.grid(row=11, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Type)
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Type"))
        label.grid(row=12, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Type)
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=12, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Type)
        self.type_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.type_label.grid(row=12, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Memory (RSS))
        label = Common.static_information_label(self.frame_summary_tab, text=_tr("Memory (RSS)"))
        label.grid(row=13, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Memory (RSS))
        label = Common.static_information_label(self.frame_summary_tab, text=":")
        label.grid(row=13, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Memory (RSS))
        self.memory_rss_label = Common.dynamic_information_label(self.frame_summary_tab)
        self.memory_rss_label.grid(row=13, column=2, sticky="nsew", padx=0, pady=4)


    def dependencies_tab_gui(self):
        """
        Generate "Dependencies" tab GUI objects.
        """

        # Label (Requires)
        label = Common.static_information_label(self.frame_dependencies_tab, text=_tr("Requires"))
        label.grid(row=0, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Requires)
        label = Common.static_information_label(self.frame_dependencies_tab, text=":")
        label.grid(row=0, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Requires)
        self.requires_label = Common.dynamic_information_label(self.frame_dependencies_tab)
        self.requires_label.grid(row=0, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Conflicts)
        label = Common.static_information_label(self.frame_dependencies_tab, text=_tr("Conflicts"))
        label.grid(row=1, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Conflicts)
        label = Common.static_information_label(self.frame_dependencies_tab, text=":")
        label.grid(row=1, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Conflicts)
        self.conflicts_label = Common.dynamic_information_label(self.frame_dependencies_tab)
        self.conflicts_label.grid(row=1, column=2, sticky="nsew", padx=0, pady=4)

        # Label (After)
        label = Common.static_information_label(self.frame_dependencies_tab, text=_tr("After"))
        label.grid(row=2, column=0, sticky="nsew", padx=0, pady=4)
        # Label (After)
        label = Common.static_information_label(self.frame_dependencies_tab, text=":")
        label.grid(row=2, column=1, sticky="nsew", padx=5, pady=4)
        # Label (After)
        self.after_label = Common.dynamic_information_label(self.frame_dependencies_tab)
        self.after_label.grid(row=2, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Before)
        label = Common.static_information_label(self.frame_dependencies_tab, text=_tr("Before"))
        label.grid(row=3, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Before)
        label = Common.static_information_label(self.frame_dependencies_tab, text=":")
        label.grid(row=3, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Before)
        self.before_label = Common.dynamic_information_label(self.frame_dependencies_tab)
        self.before_label.grid(row=3, column=2, sticky="nsew", padx=0, pady=4)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        self.service_details_window.after(1, self.on_details_window_show)


    def on_details_window_show(self):
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
        #self.notebook.set_current_page(0)
        self.details_run_func()


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.update_interval = Config.update_interval

        # Get system boot time (will be used for appending to process start times to get process start times as date time.)
        self.system_boot_time = Libsysmon.get_system_boot_time()


    def details_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        services_memory_data_precision = Config.services_memory_data_precision
        services_memory_data_unit = Config.services_memory_data_unit

        selected_service_name = Services.selected_row_name

        service_detailed_info_dict = Libsysmon.get_service_detailed_information(selected_service_name)

        # Set label text by using service data
        self.name_label.config(text=selected_service_name)
        self.description_label.config(text=service_detailed_info_dict["description"])
        self.unit_file_state_label.config(text=service_detailed_info_dict["unit_file_state"] + " - " + service_detailed_info_dict["unit_file_preset"])
        self.load_state_label.config(text=service_detailed_info_dict["load_state"])
        self.active_state_label.config(text=service_detailed_info_dict["active_state"])
        self.sub_state_label.config(text=service_detailed_info_dict["sub_state"])
        self.path_label.config(text=service_detailed_info_dict["fragment_path"])
        self.documentation_label.config(text=',\n'.join(service_detailed_info_dict["documentation"]))
        self.triggered_by_label.config(text=service_detailed_info_dict["triggered_by"])
        self.main_pid_label.config(text=service_detailed_info_dict["main_pid"])
        self.main_process_start_time_label.config(text=service_detailed_info_dict["exec_main_start_times_stamp_monotonic"])
        self.main_process_end_time_label.config(text=service_detailed_info_dict["exec_main_exit_times_stamp_monotonic"])
        self.type_label.config(text=service_detailed_info_dict["service_type"])
        if service_detailed_info_dict["memory_current"] != -1:
            memory_current = f'{Libsysmon.data_unit_converter("data", "none", service_detailed_info_dict["memory_current"], services_memory_data_unit, services_memory_data_precision)}'
        else:
            memory_current = "-"
        self.memory_rss_label.config(text=memory_current)
        self.requires_label.config(text=',\n'.join(service_detailed_info_dict["requires"]))
        self.conflicts_label.config(text=',\n'.join(service_detailed_info_dict["conflicts"]))
        self.after_label.config(text=',\n'.join(service_detailed_info_dict["after"]))
        self.before_label.config(text=',\n'.join(service_detailed_info_dict["before"]))


    def details_run_func(self):
        """
        Run initial and loop functions of service details window.
        """

        if hasattr(ServicesDetails, "update_interval") == False:
            self.initial_func()

        self.details_loop_func()

        self.service_details_window.after(int(Config.update_interval*1000), self.details_run_func)


ServicesDetails = ServicesDetails()


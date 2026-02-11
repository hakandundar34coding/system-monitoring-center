import tkinter as tk
from tkinter import ttk

import os
import time
import subprocess
from datetime import datetime

from .Config import Config
from .Processes import Processes
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class ProcessesDetails:

    def __init__(self, selected_process_pid):

        self.window_gui()

        self.initial_already_run = 0

        # Get selected_process_pid for using it for the current process object instance.
        self.selected_process_pid = selected_process_pid


    def window_gui(self):
        """
        Generate window GUI.
        """

        # Window (Process Details)
        self.process_details_window, self.frame = Common.window(MainWindow.main_window, _tr("Process Details"))
        # Restore default grab setting in order to remove blocking main window (Processes tab).
        self.process_details_window.grab_release()

        # Notebook
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_notebook_tab_changed)

        # Summary Tab
        self.frame_summary_tab = tk.Frame(self.notebook)
        self.notebook.add(self.frame_summary_tab, text=_tr("Summary"))

        # CPU Tab
        self.frame_cpu_tab = tk.Frame(self.notebook)
        self.notebook.add(self.frame_cpu_tab, text=_tr("CPU"))

        # Memory Tab
        self.frame_memory_tab = tk.Frame(self.notebook)
        self.notebook.add(self.frame_memory_tab, text=_tr("Memory"))

        # Disk Tab
        self.frame_disk_tab = tk.Frame(self.notebook)
        self.notebook.add(self.frame_disk_tab, text=_tr("Disk"))

        # File Tab
        self.frame_files_tab = tk.Frame(self.notebook)
        self.notebook.add(self.frame_files_tab, text=_tr("File"))

        self.summary_tab_gui()
        self.cpu_tab_gui()
        self.memory_tab_gui()
        self.disk_tab_gui()
        self.file_tab_gui()

        self.gui_signals()


    def summary_tab_gui(self):
        """
        Generate "Summary" tab GUI objects.
        """

        self.frame_summary_tab.columnconfigure(0, weight=1)
        #self.frame_summary_tab.rowconfigure(0, weight=1)

        frame = tk.Frame(self.frame_summary_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        frame.columnconfigure(2, weight=1)
        frame.rowconfigure(0, weight=1)

        # Label (Name)
        label = Common.static_information_label(frame, text=_tr("Name"))
        label.grid(row=0, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Name)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=0, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Name)
        self.name_label = Common.dynamic_information_label_wrap(frame)
        self.name_label.grid(row=0, column=2, sticky="nsew", padx=0, pady=4)

        # Label (PID)
        label = Common.static_information_label(frame, text=_tr("PID"))
        label.grid(row=1, column=0, sticky="nsew", padx=0, pady=4)
        # Label (PID)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=1, column=1, sticky="nsew", padx=5, pady=4)
        # Label (PID)
        self.pid_label = Common.dynamic_information_label_wrap(frame)
        self.pid_label.grid(row=1, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Status)
        label = Common.static_information_label(frame, text=_tr("Status"))
        label.grid(row=2, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Status)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=2, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Status)
        self.status_label = Common.dynamic_information_label_wrap(frame)
        self.status_label.grid(row=2, column=2, sticky="nsew", padx=0, pady=4)

        # Label (User)
        label = Common.static_information_label(frame, text=_tr("User"))
        label.grid(row=3, column=0, sticky="nsew", padx=0, pady=4)
        # Label (User)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=3, column=1, sticky="nsew", padx=5, pady=4)
        # Label (User)
        self.user_label = Common.dynamic_information_label_wrap(frame)
        self.user_label.grid(row=3, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Priority)
        label = Common.static_information_label(frame, text=_tr("Priority"))
        label.grid(row=4, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Priority)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=4, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Priority)
        self.priority_label = Common.dynamic_information_label_wrap(frame)
        self.priority_label.grid(row=4, column=2, sticky="nsew", padx=0, pady=4)

        # Label (CPU)
        label = Common.static_information_label(frame, text=_tr("CPU"))
        label.grid(row=5, column=0, sticky="nsew", padx=0, pady=4)
        # Label (CPU)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=5, column=1, sticky="nsew", padx=5, pady=4)
        # Label (CPU)
        self.cpu_label = Common.dynamic_information_label_wrap(frame)
        self.cpu_label.grid(row=5, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Memory (RSS))
        label = Common.static_information_label(frame, text=_tr("Memory (RSS)"))
        label.grid(row=6, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Memory (RSS))
        label = Common.static_information_label(frame, text=":")
        label.grid(row=6, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Memory (RSS))
        self.memory_rss_label = Common.dynamic_information_label_wrap(frame)
        self.memory_rss_label.grid(row=6, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Read Speed)
        label = Common.static_information_label(frame, text=_tr("Read Speed"))
        label.grid(row=7, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Read Speed)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=7, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Read Speed)
        self.read_speed_label = Common.dynamic_information_label_wrap(frame)
        self.read_speed_label.grid(row=7, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Write Speed)
        label = Common.static_information_label(frame, text=_tr("Write Speed"))
        label.grid(row=8, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Write Speed)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=8, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Write Speed)
        self.write_speed_label = Common.dynamic_information_label_wrap(frame)
        self.write_speed_label.grid(row=8, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Start Time)
        label = Common.static_information_label(frame, text=_tr("Start Time"))
        label.grid(row=9, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Start Time)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=9, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Start Time)
        self.start_time_label = Common.dynamic_information_label_wrap(frame)
        self.start_time_label.grid(row=9, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Path)
        label = Common.static_information_label(frame, text=_tr("Path"))
        label.grid(row=10, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Path)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=10, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Path)
        self.path_label = Common.dynamic_information_label_wrap(frame)
        self.path_label.grid(row=10, column=2, sticky="nsew", padx=0, pady=4)

        # Label (PPID)
        label = Common.static_information_label(frame, text=_tr("PPID"))
        label.grid(row=11, column=0, sticky="nsew", padx=0, pady=4)
        # Label (PPID)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=11, column=1, sticky="nsew", padx=5, pady=4)
        # Label (PPID)
        self.ppid_label = Common.dynamic_information_label_wrap(frame)
        self.ppid_label.grid(row=11, column=2, sticky="nsew", padx=0, pady=4)

        # Label (UID)
        label = Common.static_information_label(frame, text=_tr("UID"))
        label.grid(row=12, column=0, sticky="nsew", padx=0, pady=4)
        # Label (UID)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=12, column=1, sticky="nsew", padx=5, pady=4)
        # Label (UID)
        self.uid_label = Common.dynamic_information_label_wrap(frame)
        self.uid_label.grid(row=12, column=2, sticky="nsew", padx=0, pady=4)

        # Label (GID)
        label = Common.static_information_label(frame, text=_tr("GID"))
        label.grid(row=13, column=0, sticky="nsew", padx=0, pady=4)
        # Label (GID)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=13, column=1, sticky="nsew", padx=5, pady=4)
        # Label (GID)
        self.gid_label = Common.dynamic_information_label_wrap(frame)
        self.gid_label.grid(row=13, column=2, sticky="nsew", padx=0, pady=4)


    def cpu_tab_gui(self):
        """
        Generate "CPU" tab GUI objects.
        """

        self.frame_cpu_tab.columnconfigure(0, weight=1)
        self.frame_cpu_tab.rowconfigure(0, weight=1)

        frame = tk.Frame(self.frame_cpu_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        frame.columnconfigure(2, weight=1)
        frame.rowconfigure(0, weight=1)

        # Frame (drawingarea)
        drawingarea_grid = ttk.Frame(frame)
        drawingarea_grid.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=0, pady=(0, 10))
        drawingarea_grid.columnconfigure(0, weight=1)
        drawingarea_grid.rowconfigure(1, weight=1)

        # Label (drawingarea upper-left)
        self.da_upper_left_label = Common.da_upper_lower_label(drawingarea_grid, _tr("CPU Usage (Average)"))
        self.da_upper_left_label.grid(row=0, column=0, sticky="w")

        # Label (drawingarea upper-right)
        self.drawingarea_cpu_limit_label = Common.da_upper_lower_label(drawingarea_grid, "100%")
        self.drawingarea_cpu_limit_label.grid(row=0, column=1, sticky="e")

        # Label (for showing graphics)
        self.processes_details_da_cpu_usage = Common.drawingarea(drawingarea_grid, "processes_details_da_cpu_usage")
        self.processes_details_da_cpu_usage.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label(drawingarea_grid, "0")
        label.grid(row=2, column=1, sticky="e")

        # Label (CPU)
        label = Common.static_information_label(frame, text=_tr("CPU"))
        label.grid(row=1, column=0, sticky="nsew", padx=0, pady=4)
        # Label (CPU)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=1, column=1, sticky="nsew", padx=5, pady=4)
        # Label (CPU)
        self.cpu_label2 = Common.dynamic_information_label_wrap(frame)
        self.cpu_label2.grid(row=1, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Threads)
        label = Common.static_information_label(frame, text=_tr("Threads"))
        label.grid(row=2, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Threads)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=2, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Threads)
        self.threads_label = Common.dynamic_information_label_wrap(frame)
        self.threads_label.grid(row=2, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Threads (TID))
        label = Common.static_information_label(frame, text=_tr("Threads (TID)"))
        label.grid(row=3, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Threads (TID))
        label = Common.static_information_label(frame, text=":")
        label.grid(row=3, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Threads (TID))
        self.tid_label = Common.dynamic_information_label_wrap(frame)
        self.tid_label.grid(row=3, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Used CPU Core(s))
        label = Common.static_information_label(frame, text=_tr("Used CPU Core(s)"))
        label.grid(row=4, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Used CPU Core(s))
        label = Common.static_information_label(frame, text=":")
        label.grid(row=4, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Used CPU Core(s))
        self.used_cpu_cores_label = Common.dynamic_information_label_wrap(frame)
        self.used_cpu_cores_label.grid(row=4, column=2, sticky="nsew", padx=0, pady=4)

        # Label (CPU Times)
        label = Common.static_information_label(frame, text=_tr("CPU Times"))
        label.grid(row=5, column=0, sticky="nsew", padx=0, pady=4)
        # Label (CPU Times)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=5, column=1, sticky="nsew", padx=5, pady=4)
        # Label (CPU Times)
        self.cpu_times_label = Common.dynamic_information_label_wrap(frame)
        self.cpu_times_label.grid(row=5, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Context Switches)
        label = Common.static_information_label(frame, text=_tr("Context Switches"))
        label.grid(row=6, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Context Switches)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=6, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Context Switches)
        self.context_switches_label = Common.dynamic_information_label_wrap(frame)
        self.context_switches_label.grid(row=6, column=2, sticky="nsew", padx=0, pady=4)

        # Label (CPU Affinity)
        label = Common.static_information_label(frame, text=_tr("CPU Affinity"))
        label.grid(row=7, column=0, sticky="nsew", padx=0, pady=4)
        # Label (CPU Affinity)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=7, column=1, sticky="nsew", padx=5, pady=4)
        # Label (CPU Affinity)
        self.cpu_affinity_label = Common.dynamic_information_label_wrap(frame)
        self.cpu_affinity_label.grid(row=7, column=2, sticky="nsew", padx=0, pady=4)


    def memory_tab_gui(self):
        """
        Generate "Memory" tab GUI objects.
        """

        self.frame_memory_tab.columnconfigure(0, weight=1)
        self.frame_memory_tab.rowconfigure(0, weight=1)

        frame = tk.Frame(self.frame_memory_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        frame.columnconfigure(2, weight=1)
        frame.rowconfigure(0, weight=1)

        # Frame (drawingarea)
        drawingarea_grid = ttk.Frame(frame)
        drawingarea_grid.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=0, pady=(0, 10))
        drawingarea_grid.columnconfigure(0, weight=1)
        drawingarea_grid.rowconfigure(1, weight=1)

        # Label (drawingarea upper-left)
        self.da_upper_left_label = Common.da_upper_lower_label(drawingarea_grid, _tr("RAM Usage"))
        self.da_upper_left_label.grid(row=0, column=0, sticky="w")

        # Label (drawingarea upper-right)
        self.drawingarea_memory_limit_label = Common.da_upper_lower_label(drawingarea_grid, "100%")
        self.drawingarea_memory_limit_label.grid(row=0, column=1, sticky="e")

        # Label (for showing graphics)
        self.processes_details_da_memory_usage = Common.drawingarea(drawingarea_grid, "processes_details_da_memory_usage")
        self.processes_details_da_memory_usage.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label(drawingarea_grid, "0")
        label.grid(row=2, column=1, sticky="e")

        # Label (Memory)
        label = Common.static_information_label(frame, text=_tr("Memory"))
        label.grid(row=1, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Memory)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=1, column=1, sticky="nsew", padx=5, pady=4)
        # Label (CMemory)
        self.memory_label = Common.dynamic_information_label_wrap(frame)
        self.memory_label.grid(row=1, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Memory (RSS))
        label = Common.static_information_label(frame, text=_tr("Memory (RSS)"))
        label.grid(row=2, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Memory (RSS))
        label = Common.static_information_label(frame, text=":")
        label.grid(row=2, column=1, sticky="nsew", padx=5, pady=4)
        # Label (CMemory (RSS))
        self.memory_rss_label2 = Common.dynamic_information_label_wrap(frame)
        self.memory_rss_label2.grid(row=2, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Memory (VMS))
        label = Common.static_information_label(frame, text=_tr("Memory (VMS)"))
        label.grid(row=3, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Memory (VMS))
        label = Common.static_information_label(frame, text=":")
        label.grid(row=3, column=1, sticky="nsew", padx=5, pady=4)
        # Label (CMemory (VMS))
        self.memory_vms_label = Common.dynamic_information_label_wrap(frame)
        self.memory_vms_label.grid(row=3, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Memory (Shared))
        label = Common.static_information_label(frame, text=_tr("Memory (Shared)"))
        label.grid(row=4, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Memory (Shared))
        label = Common.static_information_label(frame, text=":")
        label.grid(row=4, column=1, sticky="nsew", padx=5, pady=4)
        # Label (CMemory (Shared)PU)
        self.memory_shared_label = Common.dynamic_information_label_wrap(frame)
        self.memory_shared_label.grid(row=4, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Memory (USS))
        label = Common.static_information_label(frame, text=_tr("Memory (USS)"))
        label.grid(row=5, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Memory (USS))
        label = Common.static_information_label(frame, text=":")
        label.grid(row=5, column=1, sticky="nsew", padx=5, pady=4)
        # Label (CMemory (USS))
        self.memory_uss_label = Common.dynamic_information_label_wrap(frame)
        self.memory_uss_label.grid(row=5, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Swap Memory)
        label = Common.static_information_label(frame, text=_tr("Swap Memory"))
        label.grid(row=6, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Swap Memory)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=6, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Swap Memory)
        self.swap_memory_label = Common.dynamic_information_label_wrap(frame)
        self.swap_memory_label.grid(row=6, column=2, sticky="nsew", padx=0, pady=4)


    def disk_tab_gui(self):
        """
        Generate "Disk" tab GUI objects.
        """

        self.frame_disk_tab.columnconfigure(0, weight=1)
        self.frame_disk_tab.rowconfigure(0, weight=1)

        frame = tk.Frame(self.frame_disk_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        frame.columnconfigure(2, weight=1)
        frame.rowconfigure(0, weight=1)

        # Frame (drawingarea)
        drawingarea_grid = ttk.Frame(frame)
        drawingarea_grid.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=0, pady=(0, 10))
        drawingarea_grid.columnconfigure(0, weight=1)
        drawingarea_grid.rowconfigure(1, weight=1)

        # Label (drawingarea upper-left)
        self.da_upper_left_label = Common.da_upper_lower_label(drawingarea_grid, _tr("Read Speed") + " (-) & " + _tr("Write Speed") + " (-  -)")
        self.da_upper_left_label.grid(row=0, column=0, sticky="w")

        # Label (drawingarea upper-right)
        self.drawingarea_disk_limit_label = Common.da_upper_lower_label(drawingarea_grid, "--")
        self.drawingarea_disk_limit_label.grid(row=0, column=1, sticky="e")

        # Label (for showing graphics)
        self.processes_details_da_disk_speed = Common.drawingarea(drawingarea_grid, "processes_details_da_disk_speed")
        self.processes_details_da_disk_speed.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

        # Label (drawingarea lower-right)
        label = Common.da_upper_lower_label(drawingarea_grid, "0")
        label.grid(row=2, column=1, sticky="e")

        # Label (Read Speed)
        label = Common.static_information_label(frame, text=_tr("Read Speed"))
        label.grid(row=1, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Read Speed)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=1, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Read Speed)
        self.read_speed_label2 = Common.dynamic_information_label_wrap(frame)
        self.read_speed_label2.grid(row=1, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Write Speed)
        label = Common.static_information_label(frame, text=_tr("Write Speed"))
        label.grid(row=2, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Write Speed)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=2, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Write Speed)
        self.write_speed_label2 = Common.dynamic_information_label_wrap(frame)
        self.write_speed_label2.grid(row=2, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Read Data)
        label = Common.static_information_label(frame, text=_tr("Read Data"))
        label.grid(row=3, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Read Data)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=3, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Read Data)
        self.read_data_label = Common.dynamic_information_label_wrap(frame)
        self.read_data_label.grid(row=3, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Written Data)
        label = Common.static_information_label(frame, text=_tr("Written Data"))
        label.grid(row=4, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Written Data)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=4, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Written Data)
        self.written_data_label = Common.dynamic_information_label_wrap(frame)
        self.written_data_label.grid(row=4, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Read Count)
        label = Common.static_information_label(frame, text=_tr("Read Count"))
        label.grid(row=5, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Read Count)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=5, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Read Count)
        self.read_count_label = Common.dynamic_information_label_wrap(frame)
        self.read_count_label.grid(row=5, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Write Count)
        label = Common.static_information_label(frame, text=_tr("Write Count"))
        label.grid(row=6, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Write Count)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=6, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Write Count)
        self.write_count_label = Common.dynamic_information_label_wrap(frame)
        self.write_count_label.grid(row=6, column=2, sticky="nsew", padx=0, pady=4)


    def file_tab_gui(self):
        """
        Generate "File" tab GUI objects.
        """

        self.frame_files_tab.columnconfigure(0, weight=1)
        #self.frame_files_tab.rowconfigure(0, weight=1)

        frame = tk.Frame(self.frame_files_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        frame.columnconfigure(2, weight=1)
        frame.rowconfigure(0, weight=1)

        # Label (Path)
        label = Common.static_information_label(frame, text=_tr("Path"))
        label.grid(row=0, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Path)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=0, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Path)
        self.path_label2 = Common.dynamic_information_label_wrap(frame)
        self.path_label2.grid(row=0, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Current Working Directory)
        label = Common.static_information_label(frame, text=_tr("Current Working Directory"))
        label.grid(row=1, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Current Working Directory)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=1, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Current Working Directory)
        self.cwd_label = Common.dynamic_information_label_wrap(frame)
        self.cwd_label.grid(row=1, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Command Line)
        label = Common.static_information_label(frame, text=_tr("Command Line"))
        label.grid(row=2, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Command Line)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=2, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Command Line)
        self.commandline_label = Common.dynamic_information_label_wrap(frame)
        self.commandline_label.grid(row=2, column=2, sticky="nsew", padx=0, pady=4)

        # Label (Opened Files)
        label = Common.static_information_label(frame, text=_tr("Opened Files"))
        label.grid(row=3, column=0, sticky="nsew", padx=0, pady=4)
        # Label (Opened Files)
        label = Common.static_information_label(frame, text=":")
        label.grid(row=3, column=1, sticky="nsew", padx=5, pady=4)
        # Label (Opened Files)
        self.opened_files_label = Common.dynamic_information_label_wrap(frame)
        self.opened_files_label.grid(row=3, column=2, sticky="nsew", padx=0, pady=4)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # Window signals
        self.process_details_window.after(1, self.on_details_window_show)
        self.process_details_window.protocol('WM_DELETE_WINDOW', self.on_details_window_close_request)


    def on_notebook_tab_changed(self, event):
        """
        In order to prevent empty graphs, run loop function when tab selection changed.
        """

        self.process_details_run_func()


    def on_details_window_close_request(self):
        """
        Called when window is closed.
        """

        self.process_details_window.after_cancel(self.loop_id)
        self.process_details_window.destroy()
        self = None


    def on_details_window_show(self):
        """
        Run code after window is shown.
        """

        try:
            # Delete "update_interval" variable in order to let the code to run initial function.
            # Otherwise, data from previous process (if it was viewed) will be used.
            del self.update_interval
        except AttributeError:
            pass

        # Delete first row of the grid and widget in it if it is a label.
        # This widget can be a label if a process is ended when its window is opened.
        # An information label is added into the first row of the grid in this situation
        # and it stays here if a window of another process is opened.
        """widget_in_first_row = self.main_grid.get_child_at(0, 0)
        widget_name_in_first_row = widget_in_first_row.get_name()
        if widget_name_in_first_row == "GtkLabel":
            self.main_grid.remove_row(0)
            widget_in_first_row.destroy()"""

        # This value is checked for repeating the function for getting the process data.
        self.update_window_value = 1

        self.process_details_run_func()


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        chart_data_history = Config.chart_data_history

        self.process_cpu_usage_list = [0] * chart_data_history
        self.process_ram_usage_list = [0] * chart_data_history
        self.process_disk_read_speed_list = [0] * chart_data_history
        self.process_disk_write_speed_list = [0] * chart_data_history

        self.system_boot_time = Libsysmon.get_system_boot_time()

        pid_list_prev = []
        self.piter_dict = {}
        self.selected_data_rows_prev = {}
        self.rows_additional_data_dict_prev = {}
        self.rows_data_dict_prev = {}
        self.row_id_list_prev = []

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        # Run initial function of the module if this is the first loop of the module.
        if self.initial_already_run == 0:
            self.initial_func()

        processes_cpu_precision = Config.processes_cpu_precision
        processes_memory_data_precision = Config.processes_memory_data_precision
        processes_memory_data_unit = Config.processes_memory_data_unit
        processes_disk_data_precision = Config.processes_disk_data_precision
        processes_disk_data_unit = Config.processes_disk_data_unit
        processes_disk_speed_bit = Config.processes_disk_speed_bit

        # Get "selected_process_pid"
        selected_process_pid = self.selected_process_pid

        # Get information
        self.username_uid_dict = Libsysmon.get_username_uid_dict()

        processes_cpu_divide_by_core = Config.processes_cpu_divide_by_core
        process_list = [selected_process_pid]
        processes_of_user = "all"
        hide_kernel_threads = 0
        if processes_cpu_divide_by_core == 1:
            cpu_usage_divide_by_cores = "yes"
        elif processes_cpu_divide_by_core == 0:
            cpu_usage_divide_by_cores = "no"
        detail_level = "high"
        rows_data_dict, self.rows_additional_data_dict = Libsysmon.get_processes_information(process_list, processes_of_user, hide_kernel_threads, cpu_usage_divide_by_cores, detail_level, self.rows_data_dict_prev, self.rows_additional_data_dict_prev, self.system_boot_time, self.username_uid_dict)
        self.row_id_list = list(rows_data_dict.keys())
        #self.row_id_list = [str(x) for x in self.row_id_list]
        pid_list = self.rows_additional_data_dict["pid_list"]
        ppid_list = self.rows_additional_data_dict["ppid_list"]
        username_list = self.rows_additional_data_dict["username_list"]
        cmdline_list = self.rows_additional_data_dict["cmdline_list"]

        try:
            row_data_dict = rows_data_dict[selected_process_pid]
        except KeyError:
            self.update_window_value = 0
            self.process_details_process_end_label_func()
            return

        process_name = row_data_dict["name"]
        cpu_usage = row_data_dict["cpu_usage"]
        memory_rss = row_data_dict["memory_rss"]
        disk_read_speed = row_data_dict["read_speed"]
        disk_write_speed = row_data_dict["write_speed"]
        read_data = row_data_dict["read_data"]
        written_data = row_data_dict["written_data"]
        memory_uss = row_data_dict["memory_uss"]
        memory_swap = row_data_dict["memory_swap"]

        fd_ls_output, task_ls_output = Libsysmon.get_fd_task_ls_output(selected_process_pid)
        if task_ls_output == "-":
            self.update_window_value = 0
            self.process_details_process_end_label_func()
            return

        selected_process_threads = Libsysmon.get_process_tids(task_ls_output)
        selected_process_exe, selected_process_cwd, selected_process_open_files = Libsysmon.get_process_exe_cwd_open_files(selected_process_pid, fd_ls_output)

        self.rows_data_dict_prev = dict(rows_data_dict)
        self.row_id_list_prev = self.row_id_list
        self.rows_additional_data_dict_prev = dict(self.rows_additional_data_dict)

        # Stop running functions in order to prevent errors.
        try:
            if self.update_window_value == 0:
                return
        except AttributeError:
            pass

        # Set window title
        self.process_details_window.title(_tr("Process Details") + ": " + process_name + " - (" + _tr("PID") + ": " + str(selected_process_pid) + ")")

        # Update data lists for graphs.
        self.process_cpu_usage_list.append(cpu_usage)
        del self.process_cpu_usage_list[0]
        self.process_ram_usage_list.append(memory_rss)
        del self.process_ram_usage_list[0]
        self.process_disk_read_speed_list.append(disk_read_speed)
        del self.process_disk_read_speed_list[0]
        self.process_disk_write_speed_list.append(disk_write_speed)
        del self.process_disk_write_speed_list[0]

        # Update graphs.
        Performance.performance_line_charts_draw(self.processes_details_da_cpu_usage, "processes_details_da_cpu_usage")
        Performance.performance_line_charts_draw(self.processes_details_da_memory_usage, "processes_details_da_memory_usage")
        Performance.performance_line_charts_draw(self.processes_details_da_disk_speed, "processes_details_da_disk_speed")

        # Show information on labels (Summary tab).
        self.name_label.config(text=process_name)
        self.pid_label.config(text=f'{selected_process_pid}')
        self.status_label.config(text=_tr(row_data_dict["status"]))
        self.user_label.config(text=row_data_dict["username"])
        self.priority_label.config(text=f'{row_data_dict["nice"]}')
        self.cpu_label.config(text=f'{cpu_usage:.{processes_cpu_precision}f} %')
        self.memory_rss_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", memory_rss, processes_memory_data_unit, processes_memory_data_precision)}')
        if read_data != "-":
            self.read_speed_label.config(text=f'{Libsysmon.data_unit_converter("speed", processes_disk_speed_bit, disk_read_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
        if read_data == "-":
            self.read_speed_label.config(text="-")
        if written_data != "-":
            self.write_speed_label.config(text=f'{Libsysmon.data_unit_converter("speed", processes_disk_speed_bit, disk_write_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
        if written_data == "-":
            self.write_speed_label.set_label("-")
        self.start_time_label.config(text=datetime.fromtimestamp(row_data_dict["start_time"]).strftime("%d.%m.%Y %H:%M:%S"))
        self.path_label.config(text=selected_process_exe)
        self.ppid_label.config(text=f'{row_data_dict["ppid"]}')
        self.uid_label.config(text=f'Real: {row_data_dict["uid_real"]}, Effective: {row_data_dict["uid_effective"]}, Saved: {row_data_dict["uid_saved"]}')
        self.gid_label.config(text=f'Real: {row_data_dict["gid_real"]}, Effective: {row_data_dict["gid_effective"]}, Saved: {row_data_dict["gid_saved"]}')

        # Show information on labels (CPU tab).
        self.cpu_label2.config(text=f'{cpu_usage:.{processes_cpu_precision}f} %')
        self.threads_label.config(text=f'{row_data_dict["number_of_threads"]}')
        self.tid_label.config(text=', '.join(selected_process_threads))
        self.used_cpu_cores_label.config(text=f'{row_data_dict["cpu_numbers"]}')
        self.cpu_times_label.config(text=f'User: {row_data_dict["cpu_time_user"]}, System: {row_data_dict["cpu_time_kernel"]}, Children User: {row_data_dict["cpu_time_children_user"]}, Children System: {row_data_dict["cpu_time_children_kernel"]}, IO Wait: {row_data_dict["cpu_time_io_wait"]}')
        self.context_switches_label.config(text=f'Voluntary: {row_data_dict["ctx_switches_voluntary"]}, Involuntary: {row_data_dict["ctx_switches_nonvoluntary"]}')
        self.cpu_affinity_label.config(text=row_data_dict["cpu_affinity"])

        # Show information on labels (Memory tab).
        self.memory_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", row_data_dict["memory"], processes_memory_data_unit, processes_memory_data_precision)}')
        self.memory_rss_label2.config(text=f'{Libsysmon.data_unit_converter("data", "none", memory_rss, processes_memory_data_unit, processes_memory_data_precision)}')
        self.memory_vms_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", row_data_dict["memory_vms"], processes_memory_data_unit, processes_memory_data_precision)}')
        self.memory_shared_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", row_data_dict["memory_shared"], processes_memory_data_unit, processes_memory_data_precision)}')
        if memory_uss != "-" and memory_swap != "-":
            self.memory_uss_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", memory_uss, processes_memory_data_unit, processes_memory_data_precision)}')
            self.swap_memory_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", memory_swap, processes_memory_data_unit, processes_memory_data_precision)}')
        if memory_uss == "-" and memory_swap == "-":
            self.memory_uss_label.config(text=memory_uss)
            self.swap_memory_label.config(text=memory_swap)

        # Show information on labels (Disk tab).
        if read_data != "-" and written_data != "-":
            self.read_speed_label2.config(text=f'{Libsysmon.data_unit_converter("speed", processes_disk_speed_bit, disk_read_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
            self.write_speed_label2.config(text=f'{Libsysmon.data_unit_converter("speed", processes_disk_speed_bit, disk_write_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
            self.read_data_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", read_data, processes_disk_data_unit, processes_disk_data_precision)}')
            self.written_data_label.config(text=f'{Libsysmon.data_unit_converter("data", "none", written_data, processes_disk_data_unit, processes_disk_data_precision)}')
            self.read_count_label.config(text=f'{row_data_dict["read_count"]}')
            self.write_count_label.config(text=f'{row_data_dict["write_count"]}')
        if read_data == "-" and written_data == "-":
            self.read_speed_label2.config(text="-")
            self.write_speed_label2.config(text="-")
            self.read_data_label.config(text="-")
            self.written_data_label.config(text="-")
            self.read_count_label.config(text="-")
            self.write_count_label.config(text="-")

        # Show information on labels (Path tab).
        self.path_label2.config(text=selected_process_exe)
        self.cwd_label.config(text=selected_process_cwd)
        self.commandline_label.config(text=row_data_dict["command_line"])
        if selected_process_open_files != "-":
            self.opened_files_label.config(text=',\n'.join(selected_process_open_files))
        if selected_process_open_files == "-":
            self.opened_files_label.config(text="-")


    def process_details_run_func(self):
        """
        Run initial and loop functions of process details window.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        try:
            self.process_details_window.after_cancel(self.loop_id)
        except AttributeError:
            pass

        self.loop_func()

        self.loop_id = self.process_details_window.after(int(Config.update_interval*1000), self.process_details_run_func)


    def process_details_process_end_label_func(self):
        """
        Show information label below window titlebar if the process is ended.
        """

        # Label
        label_process_end_warning = tk.Label(self.frame, text=_tr("This process is not running anymore."), bg="red", wraplength=400, justify="center")
        label_process_end_warning.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.notebook.grid(row=1)


    def process_details_show_process_details():
        """
        Generate object for every process because more than one process window can be opened on Processes tab.
        """

        # Determine max. number of Process Details windows.
        if Libsysmon.get_environment_type() == "flatpak":
            max_number_of_windows = 3
        else:
            max_number_of_windows = 8

        for selected_process_pid in Processes.selected_process_pid_list:
            # Prevent opening more than 8 (3 for Flatpak environment) windows in order to avoid very high CPU usage.
            if len(processes_details_object_list) == max_number_of_windows:
                break
            try:
                processes_details_object_list.append(ProcessesDetails(selected_process_pid))
            # Prevent errors if Enter key is pressed without selecting a process.
            except AttributeError:
                return
            #processes_details_object_list[-1].process_details_window.set_visible(True)

processes_details_object_list = []


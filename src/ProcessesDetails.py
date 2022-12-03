#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, GLib, Pango

import os
import time
import subprocess
from datetime import datetime

from locale import gettext as _tr

from Config import Config
from Processes import Processes
from Performance import Performance
from MainWindow import MainWindow
import Common


class ProcessesDetails:

    def __init__(self, selected_process_pid):

        self.window_gui()

        # Get selected_process_pid for using it for the current process object instance.
        self.selected_process_pid = selected_process_pid


    def window_gui(self):
        """
        Generate window GUI.
        """

        # Window
        self.process_details_window = Gtk.Window()
        self.process_details_window.set_default_size(500, 470)
        self.process_details_window.set_title(_tr("Process Details"))
        self.process_details_window.set_icon_name("system-monitoring-center")
        self.process_details_window.set_transient_for(MainWindow.main_window)
        #self.process_details_window.set_modal(True)
        #self.process_details_window.set_hide_on_close(True)

        # Grid
        self.main_grid = Gtk.Grid()
        self.process_details_window.set_child(self.main_grid)

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
        # "CPU" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("CPU"))
        self.scrolledwindow_cpu_tab = Gtk.ScrolledWindow()
        notebook.append_page(self.scrolledwindow_cpu_tab, tab_title_label)
        # "Memory" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("Memory"))
        self.scrolledwindow_memory_tab = Gtk.ScrolledWindow()
        notebook.append_page(self.scrolledwindow_memory_tab, tab_title_label)
        # "Disk" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("Disk"))
        self.scrolledwindow_disk_tab = Gtk.ScrolledWindow()
        notebook.append_page(self.scrolledwindow_disk_tab, tab_title_label)
        # "File" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("File"))
        self.scrolledwindow_file_tab = Gtk.ScrolledWindow()
        notebook.append_page(self.scrolledwindow_file_tab, tab_title_label)

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

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_summary_tab.set_child(viewport)

        # Grid
        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)
        viewport.set_child(grid)

        # Label (Name)
        label = Gtk.Label()
        label.set_label(_tr("Name"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 0, 1, 1)
        # Label (Name)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 0, 1, 1)
        # Label (Name)
        self.name_label = Gtk.Label()
        self.name_label.set_selectable(True)
        self.name_label.set_label("--")
        self.name_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.name_label.set_halign(Gtk.Align.START)
        grid.attach(self.name_label, 2, 0, 1, 1)

        # Label (PID)
        label = Gtk.Label()
        label.set_label(_tr("PID"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)
        # Label (PID)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 1, 1, 1)
        # Label (PID)
        self.pid_label = Gtk.Label()
        self.pid_label.set_selectable(True)
        self.pid_label.set_label("--")
        self.pid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.pid_label.set_halign(Gtk.Align.START)
        grid.attach(self.pid_label, 2, 1, 1, 1)

        # Label (Status)
        label = Gtk.Label()
        label.set_label(_tr("Status"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)
        # Label (Status)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 2, 1, 1)
        # Label (Status)
        self.status_label = Gtk.Label()
        self.status_label.set_selectable(True)
        self.status_label.set_label("--")
        self.status_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.status_label.set_halign(Gtk.Align.START)
        grid.attach(self.status_label, 2, 2, 1, 1)

        # Label (User)
        label = Gtk.Label()
        label.set_label(_tr("User"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)
        # Label (User)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 3, 1, 1)
        # Label (User)
        self.user_label = Gtk.Label()
        self.user_label.set_selectable(True)
        self.user_label.set_label("--")
        self.user_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.user_label.set_halign(Gtk.Align.START)
        grid.attach(self.user_label, 2, 3, 1, 1)

        # Label (Priority)
        label = Gtk.Label()
        label.set_label(_tr("Priority"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 4, 1, 1)
        # Label (Priority)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 4, 1, 1)
        # Label (Priority)
        self.priority_label = Gtk.Label()
        self.priority_label.set_selectable(True)
        self.priority_label.set_label("--")
        self.priority_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.priority_label.set_halign(Gtk.Align.START)
        grid.attach(self.priority_label, 2, 4, 1, 1)

        # Label (CPU)
        label = Gtk.Label()
        label.set_label(_tr("CPU"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 5, 1, 1)
        # Label (CPU)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 5, 1, 1)
        # Label (CPU)
        self.cpu_label = Gtk.Label()
        self.cpu_label.set_selectable(True)
        self.cpu_label.set_label("--")
        self.cpu_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cpu_label.set_halign(Gtk.Align.START)
        grid.attach(self.cpu_label, 2, 5, 1, 1)

        # Label (Memory (RSS))
        label = Gtk.Label()
        label.set_label(_tr("Memory (RSS)"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 6, 1, 1)
        # Label (Memory (RSS))
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 6, 1, 1)
        # Label (Memory (RSS))
        self.memory_rss_label = Gtk.Label()
        self.memory_rss_label.set_selectable(True)
        self.memory_rss_label.set_label("--")
        self.memory_rss_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.memory_rss_label.set_halign(Gtk.Align.START)
        grid.attach(self.memory_rss_label, 2, 6, 1, 1)

        # Label (Read Speed)
        label = Gtk.Label()
        label.set_label(_tr("Read Speed"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 7, 1, 1)
        # Label (Read Speed)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 7, 1, 1)
        # Label (Read Speed)
        self.read_speed_label = Gtk.Label()
        self.read_speed_label.set_selectable(True)
        self.read_speed_label.set_label("--")
        self.read_speed_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.read_speed_label.set_halign(Gtk.Align.START)
        grid.attach(self.read_speed_label, 2, 7, 1, 1)

        # Label (Write Speed)
        label = Gtk.Label()
        label.set_label(_tr("Write Speed"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 8, 1, 1)
        # Label (Write Speed)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 8, 1, 1)
        # Label (Write Speed)
        self.write_speed_label = Gtk.Label()
        self.write_speed_label.set_selectable(True)
        self.write_speed_label.set_label("--")
        self.write_speed_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.write_speed_label.set_halign(Gtk.Align.START)
        grid.attach(self.write_speed_label, 2, 8, 1, 1)

        # Label (Start Time)
        label = Gtk.Label()
        label.set_label(_tr("Start Time"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 9, 1, 1)
        # Label (Start Time)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 9, 1, 1)
        # Label (Start Time)
        self.start_time_label = Gtk.Label()
        self.start_time_label.set_selectable(True)
        self.start_time_label.set_label("--")
        self.start_time_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.start_time_label.set_halign(Gtk.Align.START)
        grid.attach(self.start_time_label, 2, 9, 1, 1)

        # Label (Path)
        label = Gtk.Label()
        label.set_label(_tr("Path"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 10, 1, 1)
        # Label (Path)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 10, 1, 1)
        # Label (Path)
        self.path_label = Gtk.Label()
        self.path_label.set_selectable(True)
        self.path_label.set_label("--")
        self.path_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.path_label.set_halign(Gtk.Align.START)
        grid.attach(self.path_label, 2, 10, 1, 1)

        # Label (PPID)
        label = Gtk.Label()
        label.set_label(_tr("PPID"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 11, 1, 1)
        # Label (PPID)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 11, 1, 1)
        # Label (PPID)
        self.ppid_label = Gtk.Label()
        self.ppid_label.set_selectable(True)
        self.ppid_label.set_label("--")
        self.ppid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.ppid_label.set_halign(Gtk.Align.START)
        grid.attach(self.ppid_label, 2, 11, 1, 1)

        # Label (UID)
        label = Gtk.Label()
        label.set_label(_tr("UID"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 12, 1, 1)
        # Label (UID)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 12, 1, 1)
        # Label (UID)
        self.uid_label = Gtk.Label()
        self.uid_label.set_selectable(True)
        self.uid_label.set_label("--")
        self.uid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.uid_label.set_halign(Gtk.Align.START)
        grid.attach(self.uid_label, 2, 12, 1, 1)

        # Label (GID)
        label = Gtk.Label()
        label.set_label(_tr("GID"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 13, 1, 1)
        # Label (GID)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 13, 1, 1)
        # Label (GID)
        self.gid_label = Gtk.Label()
        self.gid_label.set_selectable(True)
        self.gid_label.set_label("--")
        self.gid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.gid_label.set_halign(Gtk.Align.START)
        grid.attach(self.gid_label, 2, 13, 1, 1)


    def cpu_tab_gui(self):
        """
        Generate "CPU" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_cpu_tab.set_child(viewport)

        # Grid
        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)
        viewport.set_child(grid)

        # Grid (Drawingarea and related widgets)
        drawingarea_grid = Gtk.Grid()
        drawingarea_grid.set_hexpand(True)
        grid.attach(drawingarea_grid, 0, 0, 3, 1)

        # Label (CPU Usage (Average))
        label = Gtk.Label()
        label.set_label(_tr("CPU Usage (Average)"))
        label.set_halign(Gtk.Align.START)
        drawingarea_grid.attach(label, 0, 0, 1, 1)

        # Label (graphic limit)
        self.drawingarea_cpu_limit_label = Gtk.Label()
        self.drawingarea_cpu_limit_label.set_halign(Gtk.Align.END)
        self.drawingarea_cpu_limit_label.set_label("100%")
        drawingarea_grid.attach(self.drawingarea_cpu_limit_label, 1, 0, 1, 1)

        # DrawingArea
        self.processes_details_da_cpu_usage = Gtk.DrawingArea()
        self.processes_details_da_cpu_usage.set_hexpand(True)
        #self.processes_details_da_cpu_usage.set_vexpand(True)
        self.processes_details_da_cpu_usage.set_size_request(-1, 160)
        drawingarea_grid.attach(self.processes_details_da_cpu_usage, 0, 1, 2, 1)

        # Label (0)
        label = Gtk.Label()
        label.set_label("0")
        label.set_halign(Gtk.Align.END)
        drawingarea_grid.attach(label, 0, 2, 2, 1)

        # Label (CPU)
        label = Gtk.Label()
        label.set_label(_tr("CPU"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)
        # Label (CPU)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 1, 1, 1)
        # Label (CPU)
        self.cpu_label2 = Gtk.Label()
        self.cpu_label2.set_selectable(True)
        self.cpu_label2.set_label("--")
        self.cpu_label2.set_ellipsize(Pango.EllipsizeMode.END)
        self.cpu_label2.set_halign(Gtk.Align.START)
        grid.attach(self.cpu_label2, 2, 1, 1, 1)

        # Label (Threads)
        label = Gtk.Label()
        label.set_label(_tr("Threads"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)
        # Label (Threads)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 2, 1, 1)
        # Label (Threads)
        self.threads_label = Gtk.Label()
        self.threads_label.set_selectable(True)
        self.threads_label.set_label("--")
        self.threads_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.threads_label.set_halign(Gtk.Align.START)
        grid.attach(self.threads_label, 2, 2, 1, 1)

        # Label (Threads (TID))
        label = Gtk.Label()
        label.set_label(_tr("Threads (TID)"))
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)
        # Label (Threads (TID))
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 3, 1, 1)
        # Label (Threads (TID))
        self.tid_label = Gtk.Label()
        self.tid_label.set_selectable(True)
        self.tid_label.set_label("--")
        self.tid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.tid_label.set_halign(Gtk.Align.START)
        grid.attach(self.tid_label, 2, 3, 1, 1)

        # Label (Used CPU Core(s))
        label = Gtk.Label()
        label.set_label(_tr("Used CPU Core(s)"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 4, 1, 1)
        # Label (Used CPU Core(s))
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 4, 1, 1)
        # Label (Used CPU Core(s))
        self.used_cpu_cores_label = Gtk.Label()
        self.used_cpu_cores_label.set_selectable(True)
        self.used_cpu_cores_label.set_label("--")
        self.used_cpu_cores_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.used_cpu_cores_label.set_halign(Gtk.Align.START)
        grid.attach(self.used_cpu_cores_label, 2, 4, 1, 1)

        # Label (CPU Times)
        label = Gtk.Label()
        label.set_label(_tr("CPU Times"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 5, 1, 1)
        # Label (CPU Times)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 5, 1, 1)
        # Label (CPU Times)
        self.cpu_times_label = Gtk.Label()
        self.cpu_times_label.set_selectable(True)
        self.cpu_times_label.set_label("--")
        self.cpu_times_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cpu_times_label.set_halign(Gtk.Align.START)
        grid.attach(self.cpu_times_label, 2, 5, 1, 1)

        # Label (Context Switches)
        label = Gtk.Label()
        label.set_label(_tr("Context Switches"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 6, 1, 1)
        # Label (Context Switches)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 6, 1, 1)
        # Label (Context Switches)
        self.context_switches_label = Gtk.Label()
        self.context_switches_label.set_selectable(True)
        self.context_switches_label.set_label("--")
        self.context_switches_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.context_switches_label.set_halign(Gtk.Align.START)
        grid.attach(self.context_switches_label, 2, 6, 1, 1)


    def memory_tab_gui(self):
        """
        Generate "Memory" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_memory_tab.set_child(viewport)

        # Grid
        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)
        viewport.set_child(grid)

        # Grid (Drawingarea and related widgets)
        drawingarea_grid = Gtk.Grid()
        drawingarea_grid.set_hexpand(True)
        grid.attach(drawingarea_grid, 0, 0, 3, 1)

        # Label (Memory (RSS))
        label = Gtk.Label()
        label.set_label(_tr("Memory (RSS)"))
        label.set_halign(Gtk.Align.START)
        drawingarea_grid.attach(label, 0, 0, 1, 1)

        # Label (graphic limit)
        self.drawingarea_memory_limit_label = Gtk.Label()
        self.drawingarea_memory_limit_label.set_halign(Gtk.Align.END)
        self.drawingarea_memory_limit_label.set_label("100%")
        drawingarea_grid.attach(self.drawingarea_memory_limit_label, 1, 0, 1, 1)

        # DrawingArea
        self.processes_details_da_memory_usage = Gtk.DrawingArea()
        self.processes_details_da_memory_usage.set_hexpand(True)
        #self.processes_details_da_memory_usage.set_vexpand(True)
        self.processes_details_da_memory_usage.set_size_request(-1, 160)
        drawingarea_grid.attach(self.processes_details_da_memory_usage, 0, 1, 2, 1)

        # Label (0)
        label = Gtk.Label()
        label.set_label("0")
        label.set_halign(Gtk.Align.END)
        drawingarea_grid.attach(label, 0, 2, 2, 1)

        # Label (Memory (RSS))
        label = Gtk.Label()
        label.set_label(_tr("Memory (RSS)"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)
        # Label (Memory (RSS))
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 1, 1, 1)
        # Label (Memory (RSS))
        self.memory_rss_label2 = Gtk.Label()
        self.memory_rss_label2.set_selectable(True)
        self.memory_rss_label2.set_label("--")
        self.memory_rss_label2.set_ellipsize(Pango.EllipsizeMode.END)
        self.memory_rss_label2.set_halign(Gtk.Align.START)
        grid.attach(self.memory_rss_label2, 2, 1, 1, 1)

        # Label (Memory (VMS))
        label = Gtk.Label()
        label.set_label(_tr("Memory (VMS)"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)
        # Label (Memory (VMS))
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 2, 1, 1)
        # Label (Memory (VMS))
        self.memory_vms_label = Gtk.Label()
        self.memory_vms_label.set_selectable(True)
        self.memory_vms_label.set_label("--")
        self.memory_vms_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.memory_vms_label.set_halign(Gtk.Align.START)
        grid.attach(self.memory_vms_label, 2, 2, 1, 1)

        # Label (Memory (Shared))
        label = Gtk.Label()
        label.set_label(_tr("Memory (Shared)"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)
        # Label (Memory (Shared))
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 3, 1, 1)
        # Label (Memory (Shared))
        self.memory_shared_label = Gtk.Label()
        self.memory_shared_label.set_selectable(True)
        self.memory_shared_label.set_label("--")
        self.memory_shared_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.memory_shared_label.set_halign(Gtk.Align.START)
        grid.attach(self.memory_shared_label, 2, 3, 1, 1)

        # Label (Memory (USS))
        label = Gtk.Label()
        label.set_label(_tr("Memory (USS)"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 4, 1, 1)
        # Label (Memory (USS))
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 4, 1, 1)
        # Label (Memory (USS))
        self.memory_uss_label = Gtk.Label()
        self.memory_uss_label.set_selectable(True)
        self.memory_uss_label.set_label("--")
        self.memory_uss_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.memory_uss_label.set_halign(Gtk.Align.START)
        grid.attach(self.memory_uss_label, 2, 4, 1, 1)

        # Label (Swap Memory)
        label = Gtk.Label()
        label.set_label(_tr("Swap Memory"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 5, 1, 1)
        # Label (Swap Memory)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 5, 1, 1)
        # Label (Swap Memory)
        self.swap_memory_label = Gtk.Label()
        self.swap_memory_label.set_selectable(True)
        self.swap_memory_label.set_label("--")
        self.swap_memory_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.swap_memory_label.set_halign(Gtk.Align.START)
        grid.attach(self.swap_memory_label, 2, 5, 1, 1)


    def disk_tab_gui(self):
        """
        Generate "Disk" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_disk_tab.set_child(viewport)

        # Grid
        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)
        viewport.set_child(grid)

        # Grid (Drawingarea and related widgets)
        drawingarea_grid = Gtk.Grid()
        drawingarea_grid.set_hexpand(True)
        grid.attach(drawingarea_grid, 0, 0, 3, 1)

        # Label (Read Speed (-) & Write Speed (--))
        label = Gtk.Label()
        label.set_label(_tr("Read Speed") + " (-) & " + _tr("Write Speed") + " (-  -)")
        label.set_halign(Gtk.Align.START)
        drawingarea_grid.attach(label, 0, 0, 1, 1)

        # Label (graphic limit)
        self.drawingarea_disk_limit_label = Gtk.Label()
        self.drawingarea_disk_limit_label.set_halign(Gtk.Align.END)
        self.drawingarea_disk_limit_label.set_label("--")
        drawingarea_grid.attach(self.drawingarea_disk_limit_label, 1, 0, 1, 1)

        # DrawingArea
        self.processes_details_da_disk_speed = Gtk.DrawingArea()
        self.processes_details_da_disk_speed.set_hexpand(True)
        #self.processes_details_da_disk_speed.set_vexpand(True)
        self.processes_details_da_disk_speed.set_size_request(-1, 160)
        drawingarea_grid.attach(self.processes_details_da_disk_speed, 0, 1, 2, 1)

        # Label (0)
        label = Gtk.Label()
        label.set_label("0")
        label.set_halign(Gtk.Align.END)
        drawingarea_grid.attach(label, 0, 2, 2, 1)

        # Label (Read Speed)
        label = Gtk.Label()
        label.set_label(_tr("Read Speed"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)
        # Label (Read Speed)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 1, 1, 1)
        # Label (Read Speed)
        self.read_speed_label2 = Gtk.Label()
        self.read_speed_label2.set_selectable(True)
        self.read_speed_label2.set_label("--")
        self.read_speed_label2.set_ellipsize(Pango.EllipsizeMode.END)
        self.read_speed_label2.set_halign(Gtk.Align.START)
        grid.attach(self.read_speed_label2, 2, 1, 1, 1)

        # Label (Write Speed)
        label = Gtk.Label()
        label.set_label(_tr("Write Speed"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)
        # Label (Write Speed)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 2, 1, 1)
        # Label (Write Speed)
        self.write_speed_label2 = Gtk.Label()
        self.write_speed_label2.set_selectable(True)
        self.write_speed_label2.set_label("--")
        self.write_speed_label2.set_ellipsize(Pango.EllipsizeMode.END)
        self.write_speed_label2.set_halign(Gtk.Align.START)
        grid.attach(self.write_speed_label2, 2, 2, 1, 1)

        # Label (Read Data)
        label = Gtk.Label()
        label.set_label(_tr("Read Data"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)
        # Label (Read Data)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 3, 1, 1)
        # Label (Read Data)
        self.read_data_label = Gtk.Label()
        self.read_data_label.set_selectable(True)
        self.read_data_label.set_label("--")
        self.read_data_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.read_data_label.set_halign(Gtk.Align.START)
        grid.attach(self.read_data_label, 2, 3, 1, 1)

        # Label (Written Data)
        label = Gtk.Label()
        label.set_label(_tr("Written Data"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 4, 1, 1)
        # Label (Written Data)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 4, 1, 1)
        # Label (Written Data)
        self.write_data_label = Gtk.Label()
        self.write_data_label.set_selectable(True)
        self.write_data_label.set_label("--")
        self.write_data_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.write_data_label.set_halign(Gtk.Align.START)
        grid.attach(self.write_data_label, 2, 4, 1, 1)

        # Label (Read Count)
        label = Gtk.Label()
        label.set_label(_tr("Read Count"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 5, 1, 1)
        # Label (Read Count)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 5, 1, 1)
        # Label (Read Count)
        self.read_count_label = Gtk.Label()
        self.read_count_label.set_selectable(True)
        self.read_count_label.set_label("--")
        self.read_count_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.read_count_label.set_halign(Gtk.Align.START)
        grid.attach(self.read_count_label, 2, 5, 1, 1)

        # Label (Write Count)
        label = Gtk.Label()
        label.set_label(_tr("Write Count"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 6, 1, 1)
        # Label (Write Count)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 6, 1, 1)
        # Label (Write Count)
        self.write_count_label = Gtk.Label()
        self.write_count_label.set_selectable(True)
        self.write_count_label.set_label("--")
        self.write_count_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.write_count_label.set_halign(Gtk.Align.START)
        grid.attach(self.write_count_label, 2, 6, 1, 1)


    def file_tab_gui(self):
        """
        Generate "File" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_file_tab.set_child(viewport)

        # Grid
        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)
        viewport.set_child(grid)

        # Label (Path)
        label = Gtk.Label()
        label.set_label(_tr("Path"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 0, 1, 1)
        # Label (Path)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 0, 1, 1)
        # Label (Path)
        self.path_label2 = Gtk.Label()
        self.path_label2.set_selectable(True)
        self.path_label2.set_label("--")
        self.path_label2.set_ellipsize(Pango.EllipsizeMode.END)
        self.path_label2.set_halign(Gtk.Align.START)
        grid.attach(self.path_label2, 2, 0, 1, 1)

        # Label (Current Working Directory)
        label = Gtk.Label()
        label.set_label(_tr("Current Working Directory"))
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 1, 1, 1)
        # Label (Current Working Directory)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 1, 1, 1, 1)
        # Label (Current Working Directory)
        self.cwd_label = Gtk.Label()
        self.cwd_label.set_selectable(True)
        self.cwd_label.set_label("--")
        self.cwd_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cwd_label.set_halign(Gtk.Align.START)
        grid.attach(self.cwd_label, 2, 1, 1, 1)

        # Label (Command Line)
        label = Gtk.Label()
        label.set_label(_tr("Command Line"))
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)
        # Label (Command Line)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 2, 1, 1)
        # Label (Command Line)
        self.commandline_label = Gtk.Label()
        self.commandline_label.set_selectable(True)
        self.commandline_label.set_label("--")
        self.commandline_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.commandline_label.set_halign(Gtk.Align.START)
        grid.attach(self.commandline_label, 2, 2, 1, 1)

        # Label (Opened Files)
        label = Gtk.Label()
        label.set_label(_tr("Opened Files"))
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)
        # Label (Opened Files)
        label = Gtk.Label()
        label.set_label(":")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 3, 1, 1)
        # Label (Opened Files)
        self.opened_files_label = Gtk.Label()
        self.opened_files_label.set_selectable(True)
        self.opened_files_label.set_label("--")
        self.opened_files_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.opened_files_label.set_halign(Gtk.Align.START)
        grid.attach(self.opened_files_label, 2, 3, 1, 1)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        self.processes_details_da_cpu_usage.set_draw_func(Performance.performance_line_charts_draw_func, "processes_details_da_cpu_usage")
        self.processes_details_da_memory_usage.set_draw_func(Performance.performance_line_charts_draw_func, "processes_details_da_memory_usage")
        self.processes_details_da_disk_speed.set_draw_func(Performance.performance_line_charts_draw_func, "processes_details_da_disk_speed")

        # Drawingarea mouse events (CPU usage drawingarea)
        drawingarea_mouse_event = Gtk.EventControllerMotion()
        drawingarea_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawingarea_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawingarea_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        self.processes_details_da_cpu_usage.add_controller(drawingarea_mouse_event)

        # Drawingarea mouse events (Memory usage drawingarea)
        drawingarea_mouse_event = Gtk.EventControllerMotion()
        drawingarea_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawingarea_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawingarea_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        self.processes_details_da_memory_usage.add_controller(drawingarea_mouse_event)

        # Drawingarea mouse events (Disk speed drawingarea)
        drawingarea_mouse_event = Gtk.EventControllerMotion()
        drawingarea_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawingarea_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawingarea_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        self.processes_details_da_disk_speed.add_controller(drawingarea_mouse_event)

        # Window signals
        self.process_details_window.connect("close-request", self.on_process_details_window_delete_event)
        self.process_details_window.connect("show", self.on_process_details_window_show)


    def on_process_details_window_delete_event(self, widget):
        """
        Called when window close button (X) is clicked.
        """

        self.update_window_value = 0
        self.process_details_window.hide()
        # Remove the current process object instance from the list if the window is closed.
        processes_details_object_list.remove(self)
        # Delete the current process object instance if the window is closed.
        del self
        return True


    def on_process_details_window_show(self, widget):
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
        widget_in_first_row = self.main_grid.get_child_at(0, 0)
        widget_name_in_first_row = widget_in_first_row.get_name()
        if widget_name_in_first_row == "GtkLabel":
            self.main_grid.remove_row(0)
            widget_in_first_row.destroy()

        # This value is checked for repeating the function for getting the process data.
        self.update_window_value = 1

        self.process_details_run_func()


    def process_details_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.process_status_list = Processes.process_status_list
        self.global_process_cpu_times_prev = []
        self.disk_read_write_data_prev = []

        chart_data_history = Config.chart_data_history

        self.process_cpu_usage_list = [0] * chart_data_history
        self.process_ram_usage_list = [0] * chart_data_history
        self.process_disk_read_speed_list = [0] * chart_data_history
        self.process_disk_write_speed_list = [0] * chart_data_history

        # Get system boot time.
        with open("/proc/stat") as reader:
            stat_lines = reader.read().split("\n")
        for line in stat_lines:
            if "btime " in line:
                self.system_boot_time = int(line.split()[1].strip())

        self.number_of_clock_ticks = Processes.number_of_clock_ticks


    def process_details_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        processes_cpu_precision = Config.processes_cpu_precision
        processes_memory_data_precision = Config.processes_memory_data_precision
        processes_memory_data_unit = Config.processes_memory_data_unit
        processes_disk_data_precision = Config.processes_disk_data_precision
        processes_disk_data_unit = Config.processes_disk_data_unit
        processes_disk_speed_bit = Config.processes_disk_speed_bit

        # Get "selected_process_pid".
        selected_process_pid = self.selected_process_pid

        # Get information.
        usernames_username_list, usernames_uid_list = self.processes_details_usernames_uids_func()
        stat_output, status_output, statm_output, io_output, smaps_output, cmdline_output = self.processes_details_stat_status_statm_io_smaps_cmdline_outputs_func(selected_process_pid)
        if stat_output == "-" or status_output == "-" or statm_output == "-":
            self.update_window_value = 0
            self.process_details_process_end_label_func()
            return
        global_cpu_time_all = self.process_details_global_cpu_time_func()
        stat_output_split = stat_output.split()
        status_output_split = status_output.split("\n")
        io_output_lines = io_output.split("\n")
        fd_ls_output, task_ls_output = self.processes_details_fd_task_ls_output_func(selected_process_pid)
        if task_ls_output == "-":
            self.update_window_value = 0
            self.process_details_process_end_label_func()
            return
        selected_process_name = self.process_name_func(selected_process_pid, stat_output, cmdline_output)
        selected_process_username = self.process_user_name_func(selected_process_pid, status_output_split, usernames_username_list, usernames_uid_list)
        selected_process_status = self.process_status_func(stat_output_split)
        selected_process_nice = self.process_nice_func(stat_output_split)
        selected_process_cpu_percent = self.process_cpu_usage_func(stat_output_split, global_cpu_time_all)
        selected_process_memory_rss = self.process_memory_rss_func(stat_output_split)
        selected_process_read_bytes, selected_process_write_bytes = self.process_disk_read_write_data_func(io_output_lines)
        selected_process_read_speed, selected_process_write_speed = self.process_disk_read_write_speed_func(selected_process_read_bytes, selected_process_write_bytes)
        selected_process_start_time = self.process_start_time_func(stat_output_split)
        selected_process_ppid = self.process_ppid_func(stat_output_split)
        selected_process_uid_real, selected_process_uid_effective, selected_process_uid_saved = self.process_real_effective_saved_uids_func(status_output_split)
        selected_process_gid_real, selected_process_gid_effective, selected_process_gid_saved = self.process_real_effective_saved_gids_func(status_output_split)
        selected_process_num_threads = self.process_number_of_threads_func(stat_output_split)
        selected_process_threads = self.process_tids_func(task_ls_output)
        selected_process_cpu_num = self.process_cpu_number_func(stat_output_split)
        selected_process_cpu_times_user, selected_process_cpu_times_kernel, selected_process_cpu_times_children_user, selected_process_cpu_times_children_kernel, selected_process_cpu_times_io_wait = self.process_cpu_times_func(stat_output_split)
        selected_process_num_ctx_switches_voluntary, selected_process_num_ctx_switches_nonvoluntary = self.process_context_switches_func(status_output_split)
        selected_process_memory_vms = self.process_memory_vms_func(stat_output_split)
        selected_process_memory_shared = self.process_memory_shared_func(statm_output)
        selected_process_memory_uss, selected_process_memory_swap = self.process_memory_uss_and_swap_func(smaps_output)
        selected_process_read_count, selected_process_write_count = self.process_read_write_counts_func(io_output_lines)
        selected_process_cmdline = self.process_cmdline_func(cmdline_output)
        selected_process_exe, selected_process_cwd, selected_process_open_files = self.process_exe_cwd_open_files_func(selected_process_pid, fd_ls_output)

        # Stop running functions in order to prevent errors.
        if self.update_window_value == 0:
            return

        # Set window title
        self.process_details_window.set_title(_tr("Process Details") + ": " + selected_process_name + " - (" + _tr("PID") + ": " + selected_process_pid + ")")

        # Update data lists for graphs.
        self.process_cpu_usage_list.append(selected_process_cpu_percent)
        del self.process_cpu_usage_list[0]
        self.process_ram_usage_list.append(selected_process_memory_rss)
        del self.process_ram_usage_list[0]
        self.process_disk_read_speed_list.append(selected_process_read_speed)
        del self.process_disk_read_speed_list[0]
        self.process_disk_write_speed_list.append(selected_process_write_speed)
        del self.process_disk_write_speed_list[0]

        # Update graphs.
        self.processes_details_da_cpu_usage.queue_draw()
        self.processes_details_da_memory_usage.queue_draw()
        self.processes_details_da_disk_speed.queue_draw()

        # Show information on labels (Summary tab).
        self.name_label.set_label(selected_process_name)
        self.pid_label.set_label(f'{selected_process_pid}')
        self.status_label.set_label(selected_process_status)
        self.user_label.set_label(selected_process_username)
        self.priority_label.set_label(f'{selected_process_nice}')
        self.cpu_label.set_label(f'{selected_process_cpu_percent:.{processes_cpu_precision}f} %')
        self.memory_rss_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", selected_process_memory_rss, processes_memory_data_unit, processes_memory_data_precision)}')
        if selected_process_read_bytes != "-":
            self.read_speed_label.set_label(f'{Performance.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_read_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
        if selected_process_read_bytes == "-":
            self.read_speed_label.set_label("-")
        if selected_process_write_bytes != "-":
            self.write_speed_label.set_label(f'{Performance.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_write_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
        if selected_process_write_bytes == "-":
            self.write_speed_label.set_label("-")
        self.start_time_label.set_label(datetime.fromtimestamp(selected_process_start_time).strftime("%d.%m.%Y %H:%M:%S"))
        self.path_label.set_label(selected_process_exe)
        self.ppid_label.set_label(f'{selected_process_ppid}')
        self.uid_label.set_label(f'Real: {selected_process_uid_real}, Effective: {selected_process_uid_effective}, Saved: {selected_process_uid_saved}')
        self.gid_label.set_label(f'Real: {selected_process_gid_real}, Effective: {selected_process_gid_effective}, Saved: {selected_process_gid_saved}')

        # Show information on labels (CPU tab).
        self.cpu_label2.set_label(f'{selected_process_cpu_percent:.{processes_cpu_precision}f} %')
        self.threads_label.set_label(f'{selected_process_num_threads}')
        self.tid_label.set_label(',\n'.join(selected_process_threads))
        self.used_cpu_cores_label.set_label(f'{selected_process_cpu_num}')
        self.cpu_times_label.set_label(f'User: {selected_process_cpu_times_user}, System: {selected_process_cpu_times_kernel}, Children User: {selected_process_cpu_times_children_user}, Children System: {selected_process_cpu_times_children_kernel}, IO Wait: {selected_process_cpu_times_io_wait}')
        self.context_switches_label.set_label(f'Voluntary: {selected_process_num_ctx_switches_voluntary}, Involuntary: {selected_process_num_ctx_switches_nonvoluntary}')

        # Show information on labels (Memory tab).
        self.memory_rss_label2.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", selected_process_memory_rss, processes_memory_data_unit, processes_memory_data_precision)}')
        self.memory_vms_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", selected_process_memory_vms, processes_memory_data_unit, processes_memory_data_precision)}')
        self.memory_shared_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", selected_process_memory_shared, processes_memory_data_unit, processes_memory_data_precision)}')
        if selected_process_memory_uss != "-" and selected_process_memory_swap != "-":
            self.memory_uss_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", selected_process_memory_uss, processes_memory_data_unit, processes_memory_data_precision)}')
            self.swap_memory_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", selected_process_memory_swap, processes_memory_data_unit, processes_memory_data_precision)}')
        if selected_process_memory_uss == "-" and selected_process_memory_swap == "-":
            self.memory_uss_label.set_label(selected_process_memory_uss)
            self.swap_memory_label.set_label(selected_process_memory_swap)

        # Show information on labels (Disk tab).
        if selected_process_read_bytes != "-" and selected_process_write_bytes != "-":
            self.read_speed_label2.set_label(f'{Performance.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_read_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
            self.write_speed_label2.set_label(f'{Performance.performance_data_unit_converter_func("speed", processes_disk_speed_bit, selected_process_write_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
            self.read_data_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", selected_process_read_bytes, processes_disk_data_unit, processes_disk_data_precision)}')
            self.write_data_label.set_label(f'{Performance.performance_data_unit_converter_func("data", "none", selected_process_write_bytes, processes_disk_data_unit, processes_disk_data_precision)}')
            self.read_count_label.set_label(f'{selected_process_read_count}')
            self.write_count_label.set_label(f'{selected_process_write_count}')
        if selected_process_read_bytes == "-" and selected_process_write_bytes == "-":
            self.read_speed_label2.set_label("-")
            self.write_speed_label2.set_label("-")
            self.read_data_label.set_label("-")
            self.write_data_label.set_label("-")
            self.read_count_label.set_label("-")
            self.write_count_label.set_label("-")

        # Show information on labels (Path tab).
        self.path_label2.set_label(selected_process_exe)
        self.cwd_label.set_label(selected_process_cwd)
        self.commandline_label.set_label(' '.join(selected_process_cmdline))
        if selected_process_open_files != "-":
            self.opened_files_label.set_label(',\n'.join(selected_process_open_files))
        if selected_process_open_files == "-":
            self.opened_files_label.set_label("-")


    def process_details_run_func(self, *args):
        """
        Run initial and loop functions of process details window.
        "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()".
        "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to change the update interval and
        run the loop again without waiting ending the previous update interval.
        """

        if hasattr(self, "update_interval") == False:
            GLib.idle_add(self.process_details_initial_func)

        # Destroy GLib source for preventing it repeating the function.
        try:
            self.main_glib_source.destroy()
        # "try-except" is used in order to prevent errors if this is first run of the function.
        except AttributeError:
            pass
        self.update_interval = Config.update_interval
        self.main_glib_source = GLib.timeout_source_new(self.update_interval * 1000)

        if self.update_window_value == 1:
            GLib.idle_add(self.process_details_loop_func)
            self.main_glib_source.set_callback(self.process_details_run_func)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


    def process_details_process_end_label_func(self):
        """
        Show information label below window titlebar if the process is ended.
        """

        # Prevent adding more than one label (if there is already a label).
        widget_in_first_row = self.main_grid.get_child_at(0, 0)
        widget_name_in_first_row = widget_in_first_row.get_name()
        if widget_name_in_first_row == "GtkLabel":
            return

        # Generate a new label for the information. This label does not exist in the ".ui" UI file.
        label_process_end_warning = Gtk.Label(label=_tr("This process is not running anymore."))
        css = b"label {background: rgba(100%,0%,0%,1.0);}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        label_process_end_warning.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.main_grid.insert_row(0)
        # Attach the label to the grid at (0, 0) position.
        self.main_grid.attach(label_process_end_warning, 0, 0, 1, 1)
        label_process_end_warning.set_visible(True)


    def processes_details_usernames_uids_func(self):
        """
        Get usernames and UIDs.
        """

        usernames_username_list = []
        usernames_uid_list = []
        with open("/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")
        for line in etc_passwd_lines:
            line_splitted = line.split(":")
            usernames_username_list.append(line_splitted[0])
            usernames_uid_list.append(line_splitted[2])

        return usernames_username_list, usernames_uid_list


    def processes_details_stat_status_statm_io_smaps_cmdline_outputs_func(self, selected_process_pid):
        """
        Get stat, status, statm, io, smaps, cmdline file outputs.
        """

        # Generate command for getting file outputs.
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host", "cat"]
        else:
            command_list = ["cat"]
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/stat")
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/status")
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/statm")
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/io")
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/smaps")
        command_list.append("/proc/version")
        command_list.append("/proc/" + selected_process_pid + "/cmdline")

        cat_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()

        # Get split text by using the first line. This text will be used for splitting
        # the outputs of different procfs files. Because output of some files may be ""
        # and they are not shown in the output of command if multiple files are used as arguments.
        cat_output_lines = cat_output.split("\n")
        split_text = cat_output_lines[0].strip()
        cat_output_split = cat_output.split(split_text)
        del cat_output_split[0]
        # Get output of procfs files.
        stat_output = cat_output_split[0].strip()
        status_output = cat_output_split[1].strip()
        statm_output = cat_output_split[2].strip()
        io_output = cat_output_split[3].strip()
        smaps_output = cat_output_split[4].strip()
        cmdline_output = cat_output_split[5].strip().replace("\x00", " ")                     # "\x00" characters in "cmdline" file are replaced with " ".

        if stat_output == "":
            stat_output = "-"
        if status_output == "":
            status_output = "-"
        if statm_output == "":
            statm_output = "-"
        if io_output == "":
            io_output = "-"
        if smaps_output == "":
            smaps_output = "-"
        if cmdline_output == "":
            cmdline_output = "-"

        return stat_output, status_output, statm_output, io_output, smaps_output, cmdline_output


    def processes_details_fd_task_ls_output_func(self, selected_process_pid):
        """
        Get fd and stat folder list outputs.
        """

        # Generate command for getting file outputs.
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host", "ls"]
        else:
            command_list = ["ls"]
        command_list.append("/proc/" + selected_process_pid + "/fd/")
        command_list.append("/proc/" + selected_process_pid + "/task/")

        ls_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()

        # Get output of procfs folders.
        if "/fd/" in ls_output and "/task/" in ls_output:
            fd_ls_output, task_ls_output = ls_output.split("\n\n")
        elif "/fd/" in ls_output and "/task/" not in ls_output:
            fd_ls_output = ls_output
            task_ls_output = "-"
        elif "/fd/" not in ls_output and "/task/" in ls_output:
            fd_ls_output = "-"
            task_ls_output = ls_output
        else:
            fd_ls_output = "-"
            task_ls_output = "-"

        return fd_ls_output, task_ls_output


    def process_details_global_cpu_time_func(self):
        """
        Get global CPU time.
        """

        # global_cpu_time_all value is get just after "/proc/[PID]/stat file is
        # read in order to measure global an process specific CPU times at the
        # same time (nearly) for ensuring accurate process CPU usage percent.
        global_cpu_time_all = time.time() * self.number_of_clock_ticks

        return global_cpu_time_all


    def process_name_func(self, selected_process_pid, stat_output, cmdline_output):
        """
        Get process name.
        """

        first_parentheses = stat_output.find("(")                                             # Process name is in parantheses and name may include whitespaces (may also include additinl parantheses). First parantheses "(" index is get by using "find()".
        second_parentheses = stat_output.rfind(")")                                           # Last parantheses ")" index is get by using "find()".
        process_name_from_stat = stat_output[first_parentheses+1:second_parentheses]          # Process name is get from string by using the indexes get previously.
        selected_process_name = process_name_from_stat

        if len(selected_process_name) == 15:                                                  # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name.
            selected_process_name = cmdline_output.split("/")[-1].split(" ")[0]
            if selected_process_name.startswith(process_name_from_stat) == False:
                selected_process_name = cmdline_output.split(" ")[0].split("/")[-1]
                if selected_process_name.startswith(process_name_from_stat) == False:
                    selected_process_name = process_name_from_stat

        return selected_process_name


    def process_user_name_func(self, selected_process_pid, status_output_split, usernames_username_list, usernames_uid_list):
        """
        Get process user name.
        """

        for line in status_output_split:
            if "Uid:\t" in line:
                # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
                real_user_id = line.split(":")[1].split()[0].strip()
                try:
                    selected_process_username = usernames_username_list[usernames_uid_list.index(real_user_id)]
                except ValueError:
                    selected_process_username = real_user_id

        return selected_process_username


    def process_status_func(self, stat_output_split):
        """
        Get process status.
        """

        selected_process_status = self.process_status_list[stat_output_split[-50]]

        return selected_process_status


    def process_nice_func(self, stat_output_split):
        """
        Get process nice.
        """

        selected_process_nice = int(stat_output_split[-34])

        return selected_process_nice


    def process_cpu_usage_func(self, stat_output_split, global_cpu_time_all):
        """
        Get process CPU usage.
        """

        # Get process cpu time in user mode (utime + stime)
        process_cpu_time = int(stat_output_split[-39]) + int(stat_output_split[-38])
        global_process_cpu_times = [global_cpu_time_all, process_cpu_time]
        try:
            global_cpu_time_all_prev, process_cpu_time_prev = self.global_process_cpu_times_prev
        # It gives various errors (ValueError, IndexError, UnboundLocalError) if a new process is started, a new column is shown on the treeview, etc because previous CPU time values are not present in these situations. Following CPU time values are used in these situations.
        except (ValueError, IndexError, UnboundLocalError) as me:
            process_cpu_time_prev = process_cpu_time                                      # There is no "process_cpu_time_prev" value and get it from "process_cpu_time" if this is first loop of the process.
            global_cpu_time_all_prev = global_process_cpu_times[0] - 1                    # Subtract "1" CPU time (a negligible value) if this is first loop of the process.
        process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
        global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
        selected_process_cpu_percent = process_cpu_time_difference / global_cpu_time_difference * 100 / Common.number_of_logical_cores()
        self.global_process_cpu_times_prev = global_process_cpu_times

        return selected_process_cpu_percent


    def process_memory_rss_func(self, stat_output_split):
        """
        Get process memory (RSS).
        """

        # Get process RSS (resident set size) memory pages and multiply with memory_page_size in order to convert the value into bytes.
        selected_process_memory_rss = int(stat_output_split[-29]) * Processes.memory_page_size

        return selected_process_memory_rss


    def process_disk_read_write_data_func(self, io_output_lines):
        """
        Get process disk read data, disk write data.
        """

        if io_output_lines != ["-"]:
            selected_process_read_bytes = int(io_output_lines[4].split(":")[1])
            selected_process_write_bytes = int(io_output_lines[5].split(":")[1])
        else:
            selected_process_read_bytes = 0
            selected_process_write_bytes = 0

        return selected_process_read_bytes, selected_process_write_bytes


    def process_disk_read_write_speed_func(self, selected_process_read_bytes, selected_process_write_bytes):
        """
        Get process disk read speed, disk write speed.
        """

        # Get disk read speed.
        disk_read_write_data = [selected_process_read_bytes, selected_process_write_bytes]
        if self.disk_read_write_data_prev == []:
            # Make process_read_bytes_prev equal to process_read_bytes for giving "0" disk read speed value if this is first loop of the process.
            selected_process_read_bytes_prev = selected_process_read_bytes
        else:
            selected_process_read_bytes_prev = self.disk_read_write_data_prev[0]
        selected_process_read_speed = (selected_process_read_bytes - int(selected_process_read_bytes_prev)) / self.update_interval

        # Get disk write speed.
        if self.disk_read_write_data_prev == []:
            # Make process_write_bytes_prev equal to process_write_bytes for giving "0" disk write speed value if this is first loop of the process.
            selected_process_write_bytes_prev = selected_process_write_bytes
        else:
            selected_process_write_bytes_prev = self.disk_read_write_data_prev[1]
        selected_process_write_speed = (selected_process_write_bytes - int(selected_process_write_bytes_prev)) / self.update_interval

        self.disk_read_write_data_prev = disk_read_write_data

        return selected_process_read_speed, selected_process_write_speed


    def process_start_time_func(self, stat_output_split):
        """
        Get process start time.
        """

        # Elapsed time between system boot and process start time (measured in clock ticks and need to be divided by sysconf(_SC_CLK_TCK) for converting into wall clock time)
        selected_process_start_time_raw = int(stat_output_split[-31])
        selected_process_start_time = (selected_process_start_time_raw / self.number_of_clock_ticks) + self.system_boot_time

        return selected_process_start_time


    def process_ppid_func(self, stat_output_split):
        """
        Get process PPID.
        """

        selected_process_ppid = int(stat_output_split[-49])

        return selected_process_ppid


    def process_real_effective_saved_uids_func(self, status_output_split):
        """
        Get process real, effective and saved UIDs.
        """

        for line in status_output_split:
            if "Uid:\t" in line:
                line_split = line.split(":")[1].split()
                # There are 4 values in the Uid line (real, effective, user, filesystem UIDs)
                selected_process_uid_real = line_split[0].strip()
                selected_process_uid_effective = line_split[1].strip()
                selected_process_uid_saved = line_split[2].strip()

        return selected_process_uid_real, selected_process_uid_effective, selected_process_uid_saved


    def process_real_effective_saved_gids_func(self, status_output_split):
        """
        Get process real, effective and saved GIDs.
        """

        for line in status_output_split:
            if "Gid:\t" in line:
                line_split = line.split(":")[1].split()
                # There are 4 values in the Gid line (real, effective, user, filesystem GIDs)
                selected_process_gid_real = line_split[0].strip()
                selected_process_gid_effective = line_split[1].strip()
                selected_process_gid_saved = line_split[2].strip()

        return selected_process_gid_real, selected_process_gid_effective, selected_process_gid_saved


    def process_number_of_threads_func(self, stat_output_split):
        """
        Get number of threads of the process.
        """

        selected_process_num_threads = stat_output_split[-33]

        return selected_process_num_threads


    def process_tids_func(self, task_ls_output):
        """
        Get threads (TIDs) of the process.
        """

        task_ls_output_lines = task_ls_output.split("\n")
        selected_process_threads = [filename for filename in task_ls_output_lines if filename.isdigit()]
        selected_process_threads = sorted(selected_process_threads, key=int)

        return selected_process_threads


    def process_cpu_number_func(self, stat_output_split):
        """
        Get the last CPU core number which process executed on.
        """

        selected_process_cpu_num = stat_output_split[-14]

        return selected_process_cpu_num


    def process_cpu_times_func(self, stat_output_split):
        """
        Get CPU times of the process.
        """

        selected_process_cpu_times_user = stat_output_split[-39]
        selected_process_cpu_times_kernel = stat_output_split[-38]
        selected_process_cpu_times_children_user = stat_output_split[-37]
        selected_process_cpu_times_children_kernel = stat_output_split[-36]
        selected_process_cpu_times_io_wait = stat_output_split[-11]

        return selected_process_cpu_times_user, selected_process_cpu_times_kernel, selected_process_cpu_times_children_user, selected_process_cpu_times_children_kernel, selected_process_cpu_times_io_wait


    def process_context_switches_func(self, status_output_split):
        """
        Get process context switches.
        """

        for line in status_output_split:
            if line.startswith("voluntary_ctxt_switches:"):
                selected_process_num_ctx_switches_voluntary = line.split(":")[1].strip()
            if line.startswith("nonvoluntary_ctxt_switches:"):
                selected_process_num_ctx_switches_nonvoluntary = line.split(":")[1].strip()

        return selected_process_num_ctx_switches_voluntary, selected_process_num_ctx_switches_nonvoluntary


    def process_memory_vms_func(self, stat_output_split):
        """
        Get process memory (VMS).
        """

        selected_process_memory_vms = int(stat_output_split[-30])

        return selected_process_memory_vms


    def process_memory_shared_func(self, statm_output):
        """
        Get process memory (Shared).
        """

        selected_process_memory_shared = int(statm_output.split()[2]) * Processes.memory_page_size

        return selected_process_memory_shared


    def process_memory_uss_and_swap_func(self, smaps_output):
        """
        Get process memory (USS - Unique Set Size) and swap memory.
        """

        smaps_output_lines = smaps_output.split("\n")

        private_clean = 0
        private_dirty = 0
        memory_swap = 0
        for line in smaps_output_lines:
            if "Private_Clean:" in line:
                private_clean = private_clean + int(line.split(":")[1].split()[0].strip())
            if "Private_Dirty:" in line:
                private_dirty = private_dirty + int(line.split(":")[1].split()[0].strip())
            if line.startswith("Swap:"):
                memory_swap = memory_swap + int(line.split(":")[1].split()[0].strip())
        # Kilobytes value converted into bytes value (there is a negligible deviation in bytes unit)
        selected_process_memory_uss = (private_clean + private_dirty) * 1024
        selected_process_memory_swap = memory_swap * 1024

        return selected_process_memory_uss, selected_process_memory_swap


    def process_read_write_counts_func(self, io_output_lines):
        """
        Get process read count, write count.
        """

        if io_output_lines != ["-"]:
            selected_process_read_count = int(io_output_lines[2].split(":")[1])
            selected_process_write_count = int(io_output_lines[3].split(":")[1])
        # Root access is needed for reading "/proc/[PID]/io" file else it gives error.
        else:
            selected_process_read_count = 0
            selected_process_write_count = 0

        return selected_process_read_count, selected_process_write_count


    def process_cmdline_func(self, cmdline_output):
        """
        Get process cmdline.
        """

        selected_process_cmdline = cmdline_output.split(" ")

        if selected_process_cmdline == [""]:
            selected_process_cmdline = "-"

        return selected_process_cmdline


    def process_exe_cwd_open_files_func(self, selected_process_pid, fd_ls_output):
        """
        Get process cwd and open files.
        """

        command_list = ["readlink"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list

        # "/proc/self" folder will be used for splitting the "readlink" command output.
        command_list.append("/proc/self")

        # Get process exe path.
        selected_process_exe_path = "/proc/" + selected_process_pid + "/exe"
        command_list.append(selected_process_exe_path)

        # Append command for splitting command output.
        command_list.append("/proc/self")

        # Get process cwd path.
        selected_process_cwd_path = "/proc/" + selected_process_pid + "/cwd"
        command_list.append(selected_process_cwd_path)

        # Append command for splitting command output.
        command_list.append("/proc/self")

        # Get process fd path list.
        fd_ls_output_lines = fd_ls_output.split("\n")
        selected_process_fds = [filename for filename in fd_ls_output_lines if filename.isdigit()]
        selected_process_fds = sorted(selected_process_fds, key=int)

        selected_process_fd_paths = []
        for fd in selected_process_fds:
            selected_process_fd_paths.append("/proc/" + selected_process_pid + "/fd/" + fd)

        if selected_process_fd_paths == []:
            selected_process_fd_paths = "-"

        # Append command list for process open files.
        if selected_process_fd_paths != "-":
            for path in selected_process_fd_paths:
                command_list.append(path)

        # Get "readlink" command output.
        readlink_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE)).stdout.decode().strip()
        readlink_output_lines = readlink_output.split("\n")

        # Split the "readlink" command output.
        split_text = readlink_output_lines[0].strip()
        readlink_output_split = readlink_output.split(split_text)
        del readlink_output_split[0]

        # Get process exe.
        selected_process_exe = readlink_output_split[0].strip()
        if selected_process_exe == "":
            selected_process_exe = "-"

        # Get process cwd.
        selected_process_cwd = readlink_output_split[1].strip()
        if selected_process_cwd == "":
            selected_process_cwd = "-"

        # Get process open files list.
        selected_process_open_files = []
        readlink_output_split = readlink_output_split[2].strip().split("\n")
        for file in readlink_output_split:
            file_strip = file.strip()
            # Prevent adding lines which are not files.
            if file_strip.count("/") > 1:
                selected_process_open_files.append(file_strip)

        if selected_process_open_files == []:
            selected_process_open_files = "-"

        return selected_process_exe, selected_process_cwd, selected_process_open_files


processes_details_object_list = []
def process_details_show_process_details():
    """
    Generate object for every process because more than one process window can be opened on Processes tab.
    """

    # Prevent opening more than 8 windows in order to avoid very high CPU usage.
    # This limit is 3 for Flatpak environment. Because CPU usage is higher in this environment.
    if Config.environment_type == "flatpak":
        max_number_of_windows = 3
    else:
        max_number_of_windows = 8

    if len(processes_details_object_list) == max_number_of_windows:
        return

    processes_details_object_list.append(ProcessesDetails(Processes.selected_process_pid))
    processes_details_object_list[-1].process_details_window.show()


import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

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

        # Get selected_process_pid for using it for the current process object instance.
        self.selected_process_pid = selected_process_pid


    def window_gui(self):
        """
        Generate window GUI.
        """

        # Window
        self.process_details_window = Gtk.Window()
        self.process_details_window.set_default_size(500, 485)
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

        # Label (PID)
        label = Common.static_information_label(_tr("PID"))
        grid.attach(label, 0, 1, 1, 1)
        # Label (PID)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 1, 1, 1)
        # Label (PID)
        self.pid_label = Common.dynamic_information_label()
        grid.attach(self.pid_label, 2, 1, 1, 1)

        # Label (Status)
        label = Common.static_information_label(_tr("Status"))
        grid.attach(label, 0, 2, 1, 1)
        # Label (Status)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 2, 1, 1)
        # Label (Status)
        self.status_label = Common.dynamic_information_label()
        grid.attach(self.status_label, 2, 2, 1, 1)

        # Label (User)
        label = Common.static_information_label(_tr("User"))
        grid.attach(label, 0, 3, 1, 1)
        # Label (User)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 3, 1, 1)
        # Label (User)
        self.user_label = Common.dynamic_information_label()
        grid.attach(self.user_label, 2, 3, 1, 1)

        # Label (Priority)
        label = Common.static_information_label(_tr("Priority"))
        grid.attach(label, 0, 4, 1, 1)
        # Label (Priority)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 4, 1, 1)
        # Label (Priority)
        self.priority_label = Common.dynamic_information_label()
        grid.attach(self.priority_label, 2, 4, 1, 1)

        # Label (CPU)
        label = Common.static_information_label(_tr("CPU"))
        grid.attach(label, 0, 5, 1, 1)
        # Label (CPU)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 5, 1, 1)
        # Label (CPU)
        self.cpu_label = Common.dynamic_information_label()
        grid.attach(self.cpu_label, 2, 5, 1, 1)

        # Label (Memory (RSS))
        label = Common.static_information_label(_tr("Memory (RSS)"))
        grid.attach(label, 0, 6, 1, 1)
        # Label (Memory (RSS))
        label = Common.static_information_label(":")
        grid.attach(label, 1, 6, 1, 1)
        # Label (Memory (RSS))
        self.memory_rss_label = Common.dynamic_information_label()
        grid.attach(self.memory_rss_label, 2, 6, 1, 1)

        # Label (Read Speed)
        label = Common.static_information_label(_tr("Read Speed"))
        grid.attach(label, 0, 7, 1, 1)
        # Label (Read Speed)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 7, 1, 1)
        # Label (Read Speed)
        self.read_speed_label = Common.dynamic_information_label()
        grid.attach(self.read_speed_label, 2, 7, 1, 1)

        # Label (Write Speed)
        label = Common.static_information_label(_tr("Write Speed"))
        grid.attach(label, 0, 8, 1, 1)
        # Label (Write Speed)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 8, 1, 1)
        # Label (Write Speed)
        self.write_speed_label = Common.dynamic_information_label()
        grid.attach(self.write_speed_label, 2, 8, 1, 1)

        # Label (Start Time)
        label = Common.static_information_label(_tr("Start Time"))
        grid.attach(label, 0, 9, 1, 1)
        # Label (Start Time)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 9, 1, 1)
        # Label (Start Time)
        self.start_time_label = Common.dynamic_information_label()
        grid.attach(self.start_time_label, 2, 9, 1, 1)

        # Label (Path)
        label = Common.static_information_label(_tr("Path"))
        grid.attach(label, 0, 10, 1, 1)
        # Label (Path)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 10, 1, 1)
        # Label (Path)
        self.path_label = Common.dynamic_information_label()
        grid.attach(self.path_label, 2, 10, 1, 1)

        # Label (PPID)
        label = Common.static_information_label(_tr("PPID"))
        grid.attach(label, 0, 11, 1, 1)
        # Label (PPID)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 11, 1, 1)
        # Label (PPID)
        self.ppid_label = Common.dynamic_information_label()
        grid.attach(self.ppid_label, 2, 11, 1, 1)

        # Label (UID)
        label = Common.static_information_label(_tr("UID"))
        grid.attach(label, 0, 12, 1, 1)
        # Label (UID)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 12, 1, 1)
        # Label (UID)
        self.uid_label = Common.dynamic_information_label()
        grid.attach(self.uid_label, 2, 12, 1, 1)

        # Label (GID)
        label = Common.static_information_label(_tr("GID"))
        grid.attach(label, 0, 13, 1, 1)
        # Label (GID)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 13, 1, 1)
        # Label (GID)
        self.gid_label = Common.dynamic_information_label()
        grid.attach(self.gid_label, 2, 13, 1, 1)


    def cpu_tab_gui(self):
        """
        Generate "CPU" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_cpu_tab.set_child(viewport)

        # Grid
        grid = Common.window_main_grid()
        viewport.set_child(grid)

        # Grid (Drawingarea and related widgets)
        drawingarea_grid = Gtk.Grid()
        drawingarea_grid.set_hexpand(True)
        grid.attach(drawingarea_grid, 0, 0, 3, 1)

        # Label (CPU Usage (Average))
        label = Common.da_upper_lower_label(_tr("CPU Usage (Average)"), Gtk.Align.START)
        drawingarea_grid.attach(label, 0, 0, 1, 1)

        # Label (graphic limit)
        self.drawingarea_cpu_limit_label = Common.da_upper_lower_label("100%", Gtk.Align.END)
        drawingarea_grid.attach(self.drawingarea_cpu_limit_label, 1, 0, 1, 1)

        # DrawingArea
        self.processes_details_da_cpu_usage = Common.drawingarea(Performance.performance_line_charts_draw, "processes_details_da_cpu_usage")
        self.processes_details_da_cpu_usage.set_vexpand(False)
        self.processes_details_da_cpu_usage.set_size_request(-1, 160)
        drawingarea_grid.attach(self.processes_details_da_cpu_usage, 0, 1, 2, 1)

        # Label (0)
        label = Common.da_upper_lower_label("0", Gtk.Align.END)
        drawingarea_grid.attach(label, 0, 2, 2, 1)

        # Label (CPU)
        label = Common.static_information_label(_tr("CPU"))
        grid.attach(label, 0, 1, 1, 1)
        # Label (CPU)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 1, 1, 1)
        # Label (CPU)
        self.cpu_label2 = Common.dynamic_information_label()
        grid.attach(self.cpu_label2, 2, 1, 1, 1)

        # Label (Threads)
        label = Common.static_information_label(_tr("Threads"))
        grid.attach(label, 0, 2, 1, 1)
        # Label (Threads)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 2, 1, 1)
        # Label (Threads)
        self.threads_label = Common.dynamic_information_label()
        grid.attach(self.threads_label, 2, 2, 1, 1)

        # Label (Threads (TID))
        label = Common.static_information_label(_tr("Threads (TID)"))
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)
        # Label (Threads (TID))
        label = Common.static_information_label(":")
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 3, 1, 1)
        # Label (Threads (TID))
        self.tid_label = Common.dynamic_information_label()
        grid.attach(self.tid_label, 2, 3, 1, 1)

        # Label (Used CPU Core(s))
        label = Common.static_information_label(_tr("Used CPU Core(s)"))
        grid.attach(label, 0, 4, 1, 1)
        # Label (Used CPU Core(s))
        label = Common.static_information_label(":")
        grid.attach(label, 1, 4, 1, 1)
        # Label (Used CPU Core(s))
        self.used_cpu_cores_label = Common.dynamic_information_label()
        grid.attach(self.used_cpu_cores_label, 2, 4, 1, 1)

        # Label (CPU Times)
        label = Common.static_information_label(_tr("CPU Times"))
        grid.attach(label, 0, 5, 1, 1)
        # Label (CPU Times)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 5, 1, 1)
        # Label (CPU Times)
        self.cpu_times_label = Common.dynamic_information_label()
        grid.attach(self.cpu_times_label, 2, 5, 1, 1)

        # Label (Context Switches)
        label = Common.static_information_label(_tr("Context Switches"))
        grid.attach(label, 0, 6, 1, 1)
        # Label (Context Switches)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 6, 1, 1)
        # Label (Context Switches)
        self.context_switches_label = Common.dynamic_information_label()
        grid.attach(self.context_switches_label, 2, 6, 1, 1)

        # Label (CPU Affinity)
        label = Common.static_information_label(_tr("CPU Affinity"))
        grid.attach(label, 0, 7, 1, 1)
        # Label (CPU Affinity)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 7, 1, 1)
        # Label (CPU Affinity)
        self.cpu_affinity_label = Common.dynamic_information_label()
        grid.attach(self.cpu_affinity_label, 2, 7, 1, 1)


    def memory_tab_gui(self):
        """
        Generate "Memory" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_memory_tab.set_child(viewport)

        # Grid
        grid = Common.window_main_grid()
        viewport.set_child(grid)

        # Grid (Drawingarea and related widgets)
        drawingarea_grid = Gtk.Grid()
        drawingarea_grid.set_hexpand(True)
        grid.attach(drawingarea_grid, 0, 0, 3, 1)

        # Label (Memory (RSS))
        label = Common.da_upper_lower_label(_tr("Memory (RSS)"), Gtk.Align.START)
        drawingarea_grid.attach(label, 0, 0, 1, 1)

        # Label (graphic limit)
        self.drawingarea_memory_limit_label = Common.da_upper_lower_label("--", Gtk.Align.END)
        drawingarea_grid.attach(self.drawingarea_memory_limit_label, 1, 0, 1, 1)

        # DrawingArea
        self.processes_details_da_memory_usage = Common.drawingarea(Performance.performance_line_charts_draw, "processes_details_da_memory_usage")
        self.processes_details_da_memory_usage.set_vexpand(False)
        self.processes_details_da_memory_usage.set_size_request(-1, 160)
        drawingarea_grid.attach(self.processes_details_da_memory_usage, 0, 1, 2, 1)

        # Label (0)
        label = Common.da_upper_lower_label("0", Gtk.Align.END)
        drawingarea_grid.attach(label, 0, 2, 2, 1)

        # Label (Memory)
        label = Common.static_information_label(_tr("Memory"))
        grid.attach(label, 0, 1, 1, 1)
        # Label (Memory)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 1, 1, 1)
        # Label (Memory)
        self.memory_label = Common.dynamic_information_label()
        grid.attach(self.memory_label, 2, 1, 1, 1)

        # Label (Memory (RSS))
        label = Common.static_information_label(_tr("Memory (RSS)"))
        grid.attach(label, 0, 2, 1, 1)
        # Label (Memory (RSS))
        label = Common.static_information_label(":")
        grid.attach(label, 1, 2, 1, 1)
        # Label (Memory (RSS))
        self.memory_rss_label2 = Common.dynamic_information_label()
        grid.attach(self.memory_rss_label2, 2, 2, 1, 1)

        # Label (Memory (VMS))
        label = Common.static_information_label(_tr("Memory (VMS)"))
        grid.attach(label, 0, 3, 1, 1)
        # Label (Memory (VMS))
        label = Common.static_information_label(":")
        grid.attach(label, 1, 3, 1, 1)
        # Label (Memory (VMS))
        self.memory_vms_label = Common.dynamic_information_label()
        grid.attach(self.memory_vms_label, 2, 3, 1, 1)

        # Label (Memory (Shared))
        label = Common.static_information_label(_tr("Memory (Shared)"))
        grid.attach(label, 0, 4, 1, 1)
        # Label (Memory (Shared))
        label = Common.static_information_label(":")
        grid.attach(label, 1, 4, 1, 1)
        # Label (Memory (Shared))
        self.memory_shared_label = Common.dynamic_information_label()
        grid.attach(self.memory_shared_label, 2, 4, 1, 1)

        # Label (Memory (USS))
        label = Common.static_information_label(_tr("Memory (USS)"))
        grid.attach(label, 0, 5, 1, 1)
        # Label (Memory (USS))
        label = Common.static_information_label(":")
        grid.attach(label, 1, 5, 1, 1)
        # Label (Memory (USS))
        self.memory_uss_label = Common.dynamic_information_label()
        grid.attach(self.memory_uss_label, 2, 5, 1, 1)

        # Label (Swap Memory)
        label = Common.static_information_label(_tr("Swap Memory"))
        grid.attach(label, 0, 6, 1, 1)
        # Label (Swap Memory)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 6, 1, 1)
        # Label (Swap Memory)
        self.swap_memory_label = Common.dynamic_information_label()
        grid.attach(self.swap_memory_label, 2, 6, 1, 1)


    def disk_tab_gui(self):
        """
        Generate "Disk" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_disk_tab.set_child(viewport)

        # Grid
        grid = Common.window_main_grid()
        viewport.set_child(grid)

        # Grid (Drawingarea and related widgets)
        drawingarea_grid = Gtk.Grid()
        drawingarea_grid.set_hexpand(True)
        grid.attach(drawingarea_grid, 0, 0, 3, 1)

        # Label (Read Speed (-) & Write Speed (--))
        label = Common.da_upper_lower_label(_tr("Read Speed") + " (-) & " + _tr("Write Speed") + " (-  -)", Gtk.Align.START)
        drawingarea_grid.attach(label, 0, 0, 1, 1)

        # Label (graphic limit)
        self.drawingarea_disk_limit_label = Common.da_upper_lower_label("--", Gtk.Align.END)
        drawingarea_grid.attach(self.drawingarea_disk_limit_label, 1, 0, 1, 1)

        # DrawingArea
        self.processes_details_da_disk_speed = Common.drawingarea(Performance.performance_line_charts_draw, "processes_details_da_disk_speed")
        self.processes_details_da_disk_speed.set_vexpand(False)
        self.processes_details_da_disk_speed.set_size_request(-1, 160)
        drawingarea_grid.attach(self.processes_details_da_disk_speed, 0, 1, 2, 1)

        # Label (0)
        label = Common.da_upper_lower_label("0", Gtk.Align.END)
        drawingarea_grid.attach(label, 0, 2, 2, 1)

        # Label (Read Speed)
        label = Common.static_information_label(_tr("Read Speed"))
        grid.attach(label, 0, 1, 1, 1)
        # Label (Read Speed)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 1, 1, 1)
        # Label (Read Speed)
        self.read_speed_label2 = Common.dynamic_information_label()
        grid.attach(self.read_speed_label2, 2, 1, 1, 1)

        # Label (Write Speed)
        label = Common.static_information_label(_tr("Write Speed"))
        grid.attach(label, 0, 2, 1, 1)
        # Label (Write Speed)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 2, 1, 1)
        # Label (Write Speed)
        self.write_speed_label2 = Common.dynamic_information_label()
        grid.attach(self.write_speed_label2, 2, 2, 1, 1)

        # Label (Read Data)
        label = Common.static_information_label(_tr("Read Data"))
        grid.attach(label, 0, 3, 1, 1)
        # Label (Read Data)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 3, 1, 1)
        # Label (Read Data)
        self.read_data_label = Common.dynamic_information_label()
        grid.attach(self.read_data_label, 2, 3, 1, 1)

        # Label (Written Data)
        label = Common.static_information_label(_tr("Written Data"))
        grid.attach(label, 0, 4, 1, 1)
        # Label (Written Data)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 4, 1, 1)
        # Label (Written Data)
        self.write_data_label = Common.dynamic_information_label()
        grid.attach(self.write_data_label, 2, 4, 1, 1)

        # Label (Read Count)
        label = Common.static_information_label(_tr("Read Count"))
        grid.attach(label, 0, 5, 1, 1)
        # Label (Read Count)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 5, 1, 1)
        # Label (Read Count)
        self.read_count_label = Common.dynamic_information_label()
        grid.attach(self.read_count_label, 2, 5, 1, 1)

        # Label (Write Count)
        label = Common.static_information_label(_tr("Write Count"))
        grid.attach(label, 0, 6, 1, 1)
        # Label (Write Count)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 6, 1, 1)
        # Label (Write Count)
        self.write_count_label = Common.dynamic_information_label()
        grid.attach(self.write_count_label, 2, 6, 1, 1)


    def file_tab_gui(self):
        """
        Generate "File" tab GUI objects.
        """

        # Viewport
        viewport = Gtk.Viewport()
        self.scrolledwindow_file_tab.set_child(viewport)

        # Grid
        grid = Common.window_main_grid()
        viewport.set_child(grid)

        # Label (Path)
        label = Common.static_information_label(_tr("Path"))
        grid.attach(label, 0, 0, 1, 1)
        # Label (Path)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 0, 1, 1)
        # Label (Path)
        self.path_label2 = Common.dynamic_information_label()
        grid.attach(self.path_label2, 2, 0, 1, 1)

        # Label (Current Working Directory)
        label = Common.static_information_label(_tr("Current Working Directory"))
        grid.attach(label, 0, 1, 1, 1)
        # Label (Current Working Directory)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 1, 1, 1)
        # Label (Current Working Directory)
        self.cwd_label = Common.dynamic_information_label()
        grid.attach(self.cwd_label, 2, 1, 1, 1)

        # Label (Command Line)
        label = Common.static_information_label(_tr("Command Line"))
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 2, 1, 1)
        # Label (Command Line)
        label = Common.static_information_label(":")
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 2, 1, 1)
        # Label (Command Line)
        self.commandline_label = Common.dynamic_information_label()
        grid.attach(self.commandline_label, 2, 2, 1, 1)

        # Label (Opened Files)
        label = Common.static_information_label(_tr("Opened Files"))
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, 3, 1, 1)
        # Label (Opened Files)
        label = Common.static_information_label(":")
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 1, 3, 1, 1)
        # Label (Opened Files)
        self.opened_files_label = Common.dynamic_information_label()
        grid.attach(self.opened_files_label, 2, 3, 1, 1)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # Window signals
        self.process_details_window.connect("close-request", self.on_process_details_window_close_request_event)
        self.process_details_window.connect("show", self.on_process_details_window_show)


    def on_process_details_window_close_request_event(self, widget):
        """
        Called when window is closed.
        """

        self.update_window_value = 0
        self.process_details_window.set_visible(False)
        # Remove the current process object instance from the list if the window is closed.
        processes_details_object_list.remove(self)
        # Delete the current process object instance after the window is closed.
        del self


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

        chart_data_history = Config.chart_data_history

        self.process_cpu_usage_list = [0] * chart_data_history
        self.process_ram_usage_list = [0] * chart_data_history
        self.process_disk_read_speed_list = [0] * chart_data_history
        self.process_disk_write_speed_list = [0] * chart_data_history

        # Get system boot time
        self.system_boot_time = Libsysmon.get_system_boot_time()

        self.processes_data_dict_prev = {}


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

        # Get "selected_process_pid"
        selected_process_pid = self.selected_process_pid

        # Get information
        self.username_uid_dict = Libsysmon.get_username_uid_dict()
        processes_data_dict = self.get_process_detailed_information(selected_process_pid)
        try:
            process_data_dict = processes_data_dict[selected_process_pid]
        except KeyError:
            self.update_window_value = 0
            self.process_details_process_end_label_func()
            return

        process_name = process_data_dict["name"]
        cpu_usage = process_data_dict["cpu_usage"]
        memory_rss = process_data_dict["memory_rss"]
        disk_read_speed = process_data_dict["read_speed"]
        disk_write_speed = process_data_dict["write_speed"]
        read_data = process_data_dict["read_data"]
        written_data = process_data_dict["written_data"]
        memory_uss = process_data_dict["memory_uss"]
        memory_swap = process_data_dict["memory_swap"]

        fd_ls_output, task_ls_output = Libsysmon.get_fd_task_ls_output(selected_process_pid)
        if task_ls_output == "-":
            self.update_window_value = 0
            self.process_details_process_end_label_func()
            return

        selected_process_threads = Libsysmon.get_process_tids(task_ls_output)
        selected_process_exe, selected_process_cwd, selected_process_open_files = Libsysmon.get_process_exe_cwd_open_files(selected_process_pid, fd_ls_output)

        # Stop running functions in order to prevent errors.
        if self.update_window_value == 0:
            return

        # Set window title
        self.process_details_window.set_title(_tr("Process Details") + ": " + process_name + " - (" + _tr("PID") + ": " + str(selected_process_pid) + ")")

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
        self.processes_details_da_cpu_usage.queue_draw()
        self.processes_details_da_memory_usage.queue_draw()
        self.processes_details_da_disk_speed.queue_draw()

        # Show information on labels (Summary tab).
        self.name_label.set_label(process_name)
        self.pid_label.set_label(f'{selected_process_pid}')
        self.status_label.set_label(_tr(process_data_dict["status"]))
        self.user_label.set_label(process_data_dict["username"])
        self.priority_label.set_label(f'{process_data_dict["nice"]}')
        self.cpu_label.set_label(f'{cpu_usage:.{processes_cpu_precision}f} %')
        self.memory_rss_label.set_label(f'{Libsysmon.data_unit_converter("data", "none", memory_rss, processes_memory_data_unit, processes_memory_data_precision)}')
        if read_data != "-":
            self.read_speed_label.set_label(f'{Libsysmon.data_unit_converter("speed", processes_disk_speed_bit, disk_read_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
        if read_data == "-":
            self.read_speed_label.set_label("-")
        if written_data != "-":
            self.write_speed_label.set_label(f'{Libsysmon.data_unit_converter("speed", processes_disk_speed_bit, disk_write_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
        if written_data == "-":
            self.write_speed_label.set_label("-")
        self.start_time_label.set_label(datetime.fromtimestamp(process_data_dict["start_time"]).strftime("%d.%m.%Y %H:%M:%S"))
        self.path_label.set_label(selected_process_exe)
        self.ppid_label.set_label(f'{process_data_dict["ppid"]}')
        self.uid_label.set_label(f'Real: {process_data_dict["uid_real"]}, Effective: {process_data_dict["uid_effective"]}, Saved: {process_data_dict["uid_saved"]}')
        self.gid_label.set_label(f'Real: {process_data_dict["gid_real"]}, Effective: {process_data_dict["gid_effective"]}, Saved: {process_data_dict["gid_saved"]}')

        # Show information on labels (CPU tab).
        self.cpu_label2.set_label(f'{cpu_usage:.{processes_cpu_precision}f} %')
        self.threads_label.set_label(f'{process_data_dict["number_of_threads"]}')
        self.tid_label.set_label(',\n'.join(selected_process_threads))
        self.used_cpu_cores_label.set_label(f'{process_data_dict["cpu_numbers"]}')
        self.cpu_times_label.set_label(f'User: {process_data_dict["cpu_time_user"]}, System: {process_data_dict["cpu_time_kernel"]}, Children User: {process_data_dict["cpu_time_children_user"]}, Children System: {process_data_dict["cpu_time_children_kernel"]}, IO Wait: {process_data_dict["cpu_time_io_wait"]}')
        self.context_switches_label.set_label(f'Voluntary: {process_data_dict["ctx_switches_voluntary"]}, Involuntary: {process_data_dict["ctx_switches_nonvoluntary"]}')
        self.cpu_affinity_label.set_label(process_data_dict["cpu_affinity"])

        # Show information on labels (Memory tab).
        self.memory_label.set_label(f'{Libsysmon.data_unit_converter("data", "none", process_data_dict["memory"], processes_memory_data_unit, processes_memory_data_precision)}')
        self.memory_rss_label2.set_label(f'{Libsysmon.data_unit_converter("data", "none", memory_rss, processes_memory_data_unit, processes_memory_data_precision)}')
        self.memory_vms_label.set_label(f'{Libsysmon.data_unit_converter("data", "none", process_data_dict["memory_vms"], processes_memory_data_unit, processes_memory_data_precision)}')
        self.memory_shared_label.set_label(f'{Libsysmon.data_unit_converter("data", "none", process_data_dict["memory_shared"], processes_memory_data_unit, processes_memory_data_precision)}')
        if memory_uss != "-" and memory_swap != "-":
            self.memory_uss_label.set_label(f'{Libsysmon.data_unit_converter("data", "none", memory_uss, processes_memory_data_unit, processes_memory_data_precision)}')
            self.swap_memory_label.set_label(f'{Libsysmon.data_unit_converter("data", "none", memory_swap, processes_memory_data_unit, processes_memory_data_precision)}')
        if memory_uss == "-" and memory_swap == "-":
            self.memory_uss_label.set_label(memory_uss)
            self.swap_memory_label.set_label(memory_swap)

        # Show information on labels (Disk tab).
        if read_data != "-" and written_data != "-":
            self.read_speed_label2.set_label(f'{Libsysmon.data_unit_converter("speed", processes_disk_speed_bit, disk_read_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
            self.write_speed_label2.set_label(f'{Libsysmon.data_unit_converter("speed", processes_disk_speed_bit, disk_write_speed, processes_disk_data_unit, processes_disk_data_precision)}/s')
            self.read_data_label.set_label(f'{Libsysmon.data_unit_converter("data", "none", read_data, processes_disk_data_unit, processes_disk_data_precision)}')
            self.write_data_label.set_label(f'{Libsysmon.data_unit_converter("data", "none", written_data, processes_disk_data_unit, processes_disk_data_precision)}')
            self.read_count_label.set_label(f'{process_data_dict["read_count"]}')
            self.write_count_label.set_label(f'{process_data_dict["write_count"]}')
        if read_data == "-" and written_data == "-":
            self.read_speed_label2.set_label("-")
            self.write_speed_label2.set_label("-")
            self.read_data_label.set_label("-")
            self.write_data_label.set_label("-")
            self.read_count_label.set_label("-")
            self.write_count_label.set_label("-")

        # Show information on labels (Path tab).
        self.path_label2.set_label(selected_process_exe)
        self.cwd_label.set_label(selected_process_cwd)
        self.commandline_label.set_label(process_data_dict["command_line"])
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
        style_provider = Gtk.CssProvider()
        try:
            css = b"label {background: rgba(100%,0%,0%,1.0);}"
            style_provider.load_from_data(css)
        except Exception:
            css = "label {background: rgba(100%,0%,0%,1.0);}"
            style_provider.load_from_data(css, len(css))
        label_process_end_warning.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.main_grid.insert_row(0)
        # Attach the label to the grid at (0, 0) position.
        self.main_grid.attach(label_process_end_warning, 0, 0, 1, 1)
        label_process_end_warning.set_visible(True)


    def get_process_detailed_information(self, selected_process_pid):
        """
        Get process detailed information.
        """

        processes_cpu_divide_by_core = Config.processes_cpu_divide_by_core
        process_list = [selected_process_pid]
        processes_of_user = "all"
        hide_kernel_threads = 0
        if processes_cpu_divide_by_core == 1:
            cpu_usage_divide_by_cores = "yes"
        elif processes_cpu_divide_by_core == 0:
            cpu_usage_divide_by_cores = "no"
        detail_level = "high"
        processes_data_dict = Libsysmon.get_processes_information(process_list, processes_of_user, hide_kernel_threads, cpu_usage_divide_by_cores, detail_level, self.processes_data_dict_prev, self.system_boot_time, self.username_uid_dict)
        self.processes_data_dict_prev = dict(processes_data_dict)

        return processes_data_dict


processes_details_object_list = []
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
        processes_details_object_list[-1].process_details_window.set_visible(True)


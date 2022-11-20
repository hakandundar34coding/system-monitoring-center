#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Pango

from locale import gettext as _tr

from Config import Config
from Processes import Processes
from MainWindow import MainWindow


class ProcessesMenu:

    def __init__(self):

        # Menu GUI
        self.menu_gui()


    def menu_gui(self):
        """
        Generate menu GUI.
        """

        # Popover
        self.processes_menu_po = Gtk.Popover()

        # Main grid
        main_grid = Gtk.Grid()
        main_grid.set_row_spacing(5)
        main_grid.set_margin_top(5)
        main_grid.set_margin_bottom(5)
        main_grid.set_margin_start(5)
        main_grid.set_margin_end(5)
        self.processes_menu_po.set_child(main_grid)

        # Bold label atributes
        self.attribute_list_bold = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold.insert(attribute)

        # Label - Menu title
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Processes"))
        label.set_halign(Gtk.Align.CENTER)
        label.set_margin_bottom(10)
        main_grid.attach(label, 0, 0, 1, 1)

        # Notebook
        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)
        main_grid.attach(notebook, 0, 1, 1, 1)

        # Tab pages and ScrolledWindow
        # "View" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("View"))
        self.grid_view_tab = Gtk.Grid()
        self.grid_view_tab.set_margin_top(15)
        self.grid_view_tab.set_margin_bottom(5)
        self.grid_view_tab.set_margin_start(5)
        self.grid_view_tab.set_margin_end(5)
        self.grid_view_tab.set_row_spacing(5)
        notebook.append_page(self.grid_view_tab, tab_title_label)
        # "Add/Remove Columns" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("Add/Remove Columns"))
        self.grid_add_remove_columns_tab = Gtk.Grid()
        self.grid_add_remove_columns_tab.set_margin_top(15)
        self.grid_add_remove_columns_tab.set_margin_bottom(5)
        self.grid_add_remove_columns_tab.set_margin_start(5)
        self.grid_add_remove_columns_tab.set_margin_end(5)
        self.grid_add_remove_columns_tab.set_row_spacing(5)
        notebook.append_page(self.grid_add_remove_columns_tab, tab_title_label)
        # "Numbers" tab
        tab_title_label = Gtk.Label()
        tab_title_label.set_label(_tr("Numbers"))
        self.grid_numbers_tab = Gtk.Grid()
        self.grid_numbers_tab.set_margin_top(15)
        self.grid_numbers_tab.set_margin_bottom(5)
        self.grid_numbers_tab.set_margin_start(5)
        self.grid_numbers_tab.set_margin_end(5)
        self.grid_numbers_tab.set_row_spacing(5)
        notebook.append_page(self.grid_numbers_tab, tab_title_label)

        # Button (Reset)
        self.reset_button = Gtk.Button()
        self.reset_button.set_label(_tr("Reset"))
        self.reset_button.set_halign(Gtk.Align.CENTER)
        main_grid.attach(self.reset_button, 0, 2, 1, 1)

        # "View" tab GUI
        self.view_tab_gui()
        # "Add/Remove Columns" tab GUI
        self.add_remove_columns_tab_gui()
        # "Numbers" tab GUI
        self.numbers_tab_gui()

        # GUI signals
        self.gui_signals()


    def view_tab_gui(self):
        """
        Generate "View" tab GUI objects.
        """

        # Grid
        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)
        self.grid_view_tab.attach(grid, 0, 0, 1, 1)

        # Label - Tab title
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("View"))
        label.set_halign(Gtk.Align.START)
        label.set_margin_bottom(10)
        grid.attach(label, 0, 0, 1, 1)

        # Checkbutton (Show processes of all users)
        self.show_processes_of_all_users_cb = Gtk.CheckButton()
        self.show_processes_of_all_users_cb.set_label(_tr("Show processes of all users"))
        self.show_processes_of_all_users_cb.set_halign(Gtk.Align.START)
        grid.attach(self.show_processes_of_all_users_cb, 0, 1, 1, 1)

        # Checkbutton (Show processes as tree)
        self.show_processes_as_tree_cb = Gtk.CheckButton()
        self.show_processes_as_tree_cb.set_label(_tr("Show processes as tree"))
        self.show_processes_as_tree_cb.set_halign(Gtk.Align.START)
        grid.attach(self.show_processes_as_tree_cb, 0, 2, 1, 1)

        # Checkbutton (Show tree lines)
        self.show_tree_lines_cb = Gtk.CheckButton()
        self.show_tree_lines_cb.set_label(_tr("Show tree lines"))
        self.show_tree_lines_cb.set_halign(Gtk.Align.START)
        self.show_tree_lines_cb.set_margin_start(20)
        grid.attach(self.show_tree_lines_cb, 0, 3, 1, 1)

        # Grid (Expand/Collapse all buttons)
        grid_buttons = Gtk.Grid()
        grid_buttons.set_margin_start(20)
        grid_buttons.add_css_class("linked")
        grid.attach(grid_buttons, 0, 4, 1, 1)

        # Button (Expand all)
        self.expand_all_button = Gtk.Button()
        self.expand_all_button.set_label("Expand all")
        grid_buttons.attach(self.expand_all_button, 0, 1, 1, 1)

        # Button (Collapse all)
        self.collapse_all_button = Gtk.Button()
        self.collapse_all_button.set_label("Collapse all")
        grid_buttons.attach(self.collapse_all_button, 1, 1, 1, 1)


    def add_remove_columns_tab_gui(self):
        """
        Generate "Add/Remove Columns" tab GUI objects.
        """

        # Grid
        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)
        self.grid_add_remove_columns_tab.attach(grid, 0, 0, 1, 1)

        # Label - Tab title
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Add/Remove Columns"))
        label.set_halign(Gtk.Align.START)
        label.set_margin_bottom(10)
        grid.attach(label, 0, 0, 2, 1)

        # Checkbutton (Name)
        self.name_cb = Gtk.CheckButton()
        self.name_cb.set_label(_tr("Name"))
        self.name_cb.set_active(True)
        self.name_cb.set_sensitive(False)
        self.name_cb.set_halign(Gtk.Align.START)
        grid.attach(self.name_cb, 0, 1, 1, 1)

        # Checkbutton (PID)
        self.pid_cb = Gtk.CheckButton()
        self.pid_cb.set_label(_tr("PID"))
        self.pid_cb.set_halign(Gtk.Align.START)
        grid.attach(self.pid_cb, 0, 2, 1, 1)

        # Checkbutton (User)
        self.user_cb = Gtk.CheckButton()
        self.user_cb.set_label(_tr("User"))
        self.user_cb.set_halign(Gtk.Align.START)
        grid.attach(self.user_cb, 0, 3, 1, 1)

        # Checkbutton (Status)
        self.status_cb = Gtk.CheckButton()
        self.status_cb.set_label(_tr("Status"))
        self.status_cb.set_halign(Gtk.Align.START)
        grid.attach(self.status_cb, 0, 4, 1, 1)

        # Checkbutton (CPU)
        self.cpu_cb = Gtk.CheckButton()
        self.cpu_cb.set_label(_tr("CPU"))
        self.cpu_cb.set_halign(Gtk.Align.START)
        grid.attach(self.cpu_cb, 0, 5, 1, 1)

        # Checkbutton (Memory (RSS))
        self.memory_rss_cb = Gtk.CheckButton()
        self.memory_rss_cb.set_label(_tr("Memory (RSS)"))
        self.memory_rss_cb.set_halign(Gtk.Align.START)
        grid.attach(self.memory_rss_cb, 0, 6, 1, 1)

        # Checkbutton (Memory (VMS))
        self.memory_vms_cb = Gtk.CheckButton()
        self.memory_vms_cb.set_label(_tr("Memory (VMS)"))
        self.memory_vms_cb.set_halign(Gtk.Align.START)
        grid.attach(self.memory_vms_cb, 0, 7, 1, 1)

        # Checkbutton (Memory (Shared))
        self.memory_shared_cb = Gtk.CheckButton()
        self.memory_shared_cb.set_label(_tr("Memory (Shared)"))
        self.memory_shared_cb.set_halign(Gtk.Align.START)
        grid.attach(self.memory_shared_cb, 0, 8, 1, 1)

        # Checkbutton (Read Data)
        self.read_data_cb = Gtk.CheckButton()
        self.read_data_cb.set_label(_tr("Read Data"))
        self.read_data_cb.set_halign(Gtk.Align.START)
        grid.attach(self.read_data_cb, 0, 9, 1, 1)

        # Checkbutton (Write Data)
        self.write_data_cb = Gtk.CheckButton()
        self.write_data_cb.set_label(_tr("Write Data"))
        self.write_data_cb.set_halign(Gtk.Align.START)
        grid.attach(self.write_data_cb, 0, 10, 1, 1)

        # Checkbutton (Read Speed)
        self.read_speed_cb = Gtk.CheckButton()
        self.read_speed_cb.set_label(_tr("Read Speed"))
        self.read_speed_cb.set_halign(Gtk.Align.START)
        grid.attach(self.read_speed_cb, 1, 1, 1, 1)

        # Checkbutton (Write Speed)
        self.write_speed_cb = Gtk.CheckButton()
        self.write_speed_cb.set_label(_tr("Write Speed"))
        self.write_speed_cb.set_halign(Gtk.Align.START)
        grid.attach(self.write_speed_cb, 1, 2, 1, 1)

        # Checkbutton (Priority)
        self.priority_cb = Gtk.CheckButton()
        self.priority_cb.set_label(_tr("Priority"))
        self.priority_cb.set_halign(Gtk.Align.START)
        grid.attach(self.priority_cb, 1, 3, 1, 1)

        # Checkbutton (Threads)
        self.threads_cb = Gtk.CheckButton()
        self.threads_cb.set_label(_tr("Threads"))
        self.threads_cb.set_halign(Gtk.Align.START)
        grid.attach(self.threads_cb, 1, 4, 1, 1)

        # Checkbutton (PPID)
        self.ppid_cb = Gtk.CheckButton()
        self.ppid_cb.set_label(_tr("PPID"))
        self.ppid_cb.set_halign(Gtk.Align.START)
        grid.attach(self.ppid_cb, 1, 5, 1, 1)

        # Checkbutton (UID)
        self.uid_cb = Gtk.CheckButton()
        self.uid_cb.set_label(_tr("UID"))
        self.uid_cb.set_halign(Gtk.Align.START)
        grid.attach(self.uid_cb, 1, 6, 1, 1)

        # Checkbutton (GID)
        self.gid_cb = Gtk.CheckButton()
        self.gid_cb.set_label(_tr("GID"))
        self.gid_cb.set_halign(Gtk.Align.START)
        grid.attach(self.gid_cb, 1, 7, 1, 1)

        # Checkbutton (Path)
        self.path_cb = Gtk.CheckButton()
        self.path_cb.set_label(_tr("Path"))
        self.path_cb.set_halign(Gtk.Align.START)
        grid.attach(self.path_cb, 1, 8, 1, 1)

        # Checkbutton (Command Line)
        self.commandline_cb = Gtk.CheckButton()
        self.commandline_cb.set_label(_tr("Command Line"))
        self.commandline_cb.set_halign(Gtk.Align.START)
        grid.attach(self.commandline_cb, 1, 9, 1, 1)


    def numbers_tab_gui(self):
        """
        Generate "Numbers" tab GUI objects.
        """

        # Grid
        grid = Gtk.Grid()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(10)
        grid.set_row_spacing(5)
        self.grid_numbers_tab.attach(grid, 0, 0, 1, 1)

        # Grid (Precision)
        precision_grid = Gtk.Grid()
        precision_grid.set_column_spacing(5)
        precision_grid.set_row_spacing(5)
        precision_grid.set_column_homogeneous(True)
        grid.attach(precision_grid, 0, 0, 2, 1)

        # Label - Title (Precision)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Precision"))
        label.set_halign(Gtk.Align.START)
        label.set_margin_bottom(10)
        precision_grid.attach(label, 0, 0, 3, 1)

        # Label "CPU"
        label = Gtk.Label()
        label.set_label(_tr("CPU"))
        label.set_halign(Gtk.Align.START)
        precision_grid.attach(label, 0, 1, 1, 1)

        # ComboBox (Precision - CPU)
        self.precision_cpu_cmb = Gtk.ComboBox()
        precision_grid.attach(self.precision_cpu_cmb, 0, 2, 1, 1)

        # Label "Memory"
        label = Gtk.Label()
        label.set_label(_tr("Memory"))
        label.set_halign(Gtk.Align.START)
        precision_grid.attach(label, 1, 1, 1, 1)

        # ComboBox (Precision - Memory)
        self.precision_memory_cmb = Gtk.ComboBox()
        precision_grid.attach(self.precision_memory_cmb, 1, 2, 1, 1)

        # Label "Disk"
        label = Gtk.Label()
        label.set_label(_tr("Disk"))
        label.set_halign(Gtk.Align.START)
        precision_grid.attach(label, 2, 1, 1, 1)

        # ComboBox (Precision - Disk)
        self.precision_disk_cmb = Gtk.ComboBox()
        precision_grid.attach(self.precision_disk_cmb, 2, 2, 1, 1)

        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        grid.attach(separator, 0, 3, 2, 1)

        # Label - Title (Data Unit)
        label = Gtk.Label()
        label.set_attributes(self.attribute_list_bold)
        label.set_label(_tr("Data Unit"))
        label.set_halign(Gtk.Align.START)
        label.set_margin_bottom(10)
        grid.attach(label, 0, 4, 2, 1)

        # Label "Memory"
        label = Gtk.Label()
        label.set_label(_tr("Memory"))
        label.set_halign(Gtk.Align.CENTER)
        grid.attach(label, 0, 5, 2, 1)

        # Label - Memory "Show data as powers of:"
        label = Gtk.Label()
        label.set_label(_tr("Show data as powers of") + ":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 6, 2, 1)

        # Checkbutton - Memory (1024)
        self.memory_data_power_of_1024_cb = Gtk.CheckButton()
        self.memory_data_power_of_1024_cb.set_group(None)
        self.memory_data_power_of_1024_cb.set_label("1024")
        self.memory_data_power_of_1024_cb.set_halign(Gtk.Align.START)
        grid.attach(self.memory_data_power_of_1024_cb, 0, 7, 1, 1)

        # Checkbutton - Memory (1000)
        self.memory_data_power_of_1000_cb = Gtk.CheckButton()
        self.memory_data_power_of_1000_cb.set_group(self.memory_data_power_of_1024_cb)
        self.memory_data_power_of_1000_cb.set_label("1000")
        self.memory_data_power_of_1000_cb.set_halign(Gtk.Align.START)
        grid.attach(self.memory_data_power_of_1000_cb, 1, 7, 1, 1)

        # Label "Disk"
        label = Gtk.Label()
        label.set_label(_tr("Disk"))
        label.set_halign(Gtk.Align.CENTER)
        grid.attach(label, 0, 8, 2, 1)

        # Label - Disk "Show data as powers of:"
        label = Gtk.Label()
        label.set_label(_tr("Show data as powers of") + ":")
        label.set_halign(Gtk.Align.START)
        grid.attach(label, 0, 9, 2, 1)

        # Checkbutton - Disk (1024)
        self.disk_data_power_of_1024_cb = Gtk.CheckButton()
        self.disk_data_power_of_1024_cb.set_group(None)
        self.disk_data_power_of_1024_cb.set_label("1024")
        self.disk_data_power_of_1024_cb.set_halign(Gtk.Align.START)
        grid.attach(self.disk_data_power_of_1024_cb, 0, 10, 1, 1)

        # Checkbutton - Disk (1000)
        self.disk_data_power_of_1000_cb = Gtk.CheckButton()
        self.disk_data_power_of_1000_cb.set_group(self.disk_data_power_of_1024_cb)
        self.disk_data_power_of_1000_cb.set_label("1000")
        self.disk_data_power_of_1000_cb.set_halign(Gtk.Align.START)
        grid.attach(self.disk_data_power_of_1000_cb, 1, 10, 1, 1)

        # Checkbutton "Show speed units as multiples of bits"
        self.show_speed_units_bytes_cb = Gtk.CheckButton()
        self.show_speed_units_bytes_cb.set_group(None)
        self.show_speed_units_bytes_cb.set_label(_tr("Show speed units as multiples of bits"))
        self.show_speed_units_bytes_cb.set_halign(Gtk.Align.START)
        grid.attach(self.show_speed_units_bytes_cb, 0, 11, 2, 1)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        self.processes_menu_po.connect("show", self.on_processes_menu_po_show)
        self.reset_button.connect("clicked", self.on_reset_button_clicked)
        self.expand_all_button.connect("clicked", self.on_expand_collapse_buttons_clicked)
        self.collapse_all_button.connect("clicked", self.on_expand_collapse_buttons_clicked)


    def gui_connect_signals_func(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.show_processes_of_all_users_cb.connect("toggled", self.on_show_processes_of_all_users_cb_toggled)
        self.show_processes_as_tree_cb.connect("toggled", self.on_show_processes_as_tree_cb_toggled)
        self.show_tree_lines_cb.connect("toggled", self.on_show_tree_lines_cb_toggled)

        self.name_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.pid_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.user_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.status_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.cpu_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.memory_rss_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.memory_vms_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.memory_shared_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.read_data_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.write_data_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.read_speed_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.write_speed_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.priority_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.threads_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.ppid_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.gid_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.uid_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.path_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.commandline_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)

        self.precision_cpu_cmb.connect("changed", self.on_precision_cpu_cmb_changed)
        self.precision_memory_cmb.connect("changed", self.on_precision_memory_cmb_changed)
        self.precision_disk_cmb.connect("changed", self.on_precision_disk_cmb_changed)
        self.memory_data_power_of_1024_cb.connect("toggled", self.on_memory_data_unit_radiobuttons_toggled)
        self.memory_data_power_of_1000_cb.connect("toggled", self.on_memory_data_unit_radiobuttons_toggled)
        self.disk_data_power_of_1024_cb.connect("toggled", self.on_disk_data_unit_radiobuttons_toggled)
        self.disk_data_power_of_1000_cb.connect("toggled", self.on_disk_data_unit_radiobuttons_toggled)
        self.show_speed_units_bytes_cb.connect("toggled", self.on_show_speed_units_bytes_cb_toggled)


    def gui_disconnect_signals_func(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.show_processes_of_all_users_cb.disconnect_by_func(self.on_show_processes_of_all_users_cb_toggled)
        self.show_processes_as_tree_cb.disconnect_by_func(self.on_show_processes_as_tree_cb_toggled)
        self.show_tree_lines_cb.disconnect_by_func(self.on_show_tree_lines_cb_toggled)

        self.name_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.pid_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.user_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.status_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.cpu_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.memory_rss_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.memory_vms_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.memory_shared_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.read_data_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.write_data_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.read_speed_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.write_speed_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.priority_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.threads_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.ppid_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.uid_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.gid_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.path_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.commandline_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)

        self.precision_cpu_cmb.disconnect_by_func(self.on_precision_cpu_cmb_changed)
        self.precision_memory_cmb.disconnect_by_func(self.on_precision_memory_cmb_changed)
        self.precision_disk_cmb.disconnect_by_func(self.on_precision_disk_cmb_changed)
        self.memory_data_power_of_1024_cb.disconnect_by_func(self.on_memory_data_unit_radiobuttons_toggled)
        self.memory_data_power_of_1000_cb.disconnect_by_func(self.on_memory_data_unit_radiobuttons_toggled)
        self.disk_data_power_of_1024_cb.disconnect_by_func(self.on_disk_data_unit_radiobuttons_toggled)
        self.disk_data_power_of_1000_cb.disconnect_by_func(self.on_disk_data_unit_radiobuttons_toggled)
        self.show_speed_units_bytes_cb.disconnect_by_func(self.on_show_speed_units_bytes_cb_toggled)


    def on_processes_menu_po_show(self, widget):
        """
        Run code when customizations menu popover is shown.
        """
 
        try:
            self.gui_disconnect_signals_func()
        except TypeError:
            pass
        self.set_gui()
        self.gui_connect_signals_func()


    def on_expand_collapse_buttons_clicked(self, widget):
        """
        Expand/Collapse treeview rows.
        """

        if widget == self.expand_all_button:
            Processes.treeview.expand_all()

        if widget == self.collapse_all_button:
            Processes.treeview.collapse_all()


    def on_reset_button_clicked(self, widget):
        """
        Reset customizations.
        """

        # Load default settings
        Config.config_default_processes_func()
        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        self.gui_disconnect_signals_func()
        self.set_gui()
        self.gui_connect_signals_func()


    def on_show_processes_of_all_users_cb_toggled(self, widget):
        """
        Show processes of all users or current user.
        """

        if widget.get_active() == True:
            Config.show_processes_of_all_users = 1
        if widget.get_active() == False:
            Config.show_processes_of_all_users = 0

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    def on_show_processes_as_tree_cb_toggled(self, widget):
        """
        Show processes as tree or list.
        """

        if widget.get_active() == True:
            Config.show_processes_as_tree = 1
            self.show_tree_lines_cb.set_sensitive(True)
            self.expand_all_button.set_sensitive(True)
            self.collapse_all_button.set_sensitive(True)
        if widget.get_active() == False:
            Config.show_processes_as_tree = 0
            self.show_tree_lines_cb.set_sensitive(False)
            self.expand_all_button.set_sensitive(False)
            self.collapse_all_button.set_sensitive(False)

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    def on_show_tree_lines_cb_toggled(self, widget):
        """
        Show/Hide treeview tree lines.
        """

        if widget.get_active() == True:
            Config.show_tree_lines = 1
        if widget.get_active() == False:
            Config.show_tree_lines = 0

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    def on_add_remove_checkbuttons_toggled(self, widget):
        """
        Run a function for adding/removing columns to treeview.
        """

        self.processes_add_remove_columns_function()


    def on_precision_cpu_cmb_changed(self, widget):
        """
        Set CPU usage precision.
        """

        Config.processes_cpu_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    def on_precision_memory_cmb_changed(self, widget):
        """
        Set memory usage precision.
        """

        Config.processes_memory_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    def on_precision_disk_cmb_changed(self, widget):
        """
        Set disk speed precision.
        """

        Config.processes_disk_data_precision = Config.number_precision_list[widget.get_active()][2]

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    def on_memory_data_unit_radiobuttons_toggled(self, widget):
        """
        Change data unit powers of (1024 or 1000) selection for memory information.
        """

        if self.memory_data_power_of_1024_cb.get_active() == True:
            Config.processes_memory_data_unit = 0
        elif self.memory_data_power_of_1000_cb.get_active() == True:
            Config.processes_memory_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    def on_disk_data_unit_radiobuttons_toggled(self, widget):
        """
        Change data unit powers of (1024 or 1000) selection for disk information.
        """

        if self.disk_data_power_of_1024_cb.get_active() == True:
            Config.processes_disk_data_unit = 0
        elif self.disk_data_power_of_1000_cb.get_active() == True:
            Config.processes_disk_data_unit = 1

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    def on_show_speed_units_bytes_cb_toggled(self, widget):
        """
        Show speed units as multiples of bits/bytes.
        """

        if widget.get_active() == True:
            Config.processes_disk_speed_bit = 1
        else:
            Config.processes_disk_speed_bit = 0

        # Apply changes immediately (without waiting update interval).
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


    def set_gui(self):
        """
        Set GUI items.
        """

        # Set GUI objects on View tab
        if Config.show_processes_of_all_users == 1:
            self.show_processes_of_all_users_cb.set_active(True)
        if Config.show_processes_of_all_users == 0:
            self.show_processes_of_all_users_cb.set_active(False)
        if Config.show_processes_as_tree == 1:
            self.show_processes_as_tree_cb.set_active(True)
            self.show_tree_lines_cb.set_sensitive(True)
            self.expand_all_button.set_sensitive(True)
            self.collapse_all_button.set_sensitive(True)
        if Config.show_processes_as_tree == 0:
            self.show_processes_as_tree_cb.set_active(False)
            self.show_tree_lines_cb.set_sensitive(False)
            self.expand_all_button.set_sensitive(False)
            self.collapse_all_button.set_sensitive(False)
        if Config.show_tree_lines == 1:
            self.show_tree_lines_cb.set_active(True)
        if Config.show_tree_lines == 0:
            self.show_tree_lines_cb.set_active(False)

        # Set GUI objects on Add/Remove Column tab
        if 0 in Config.processes_treeview_columns_shown:
            self.name_cb.set_active(True)
        else:
            self.name_cb.set_active(False)
        if 1 in Config.processes_treeview_columns_shown:
            self.pid_cb.set_active(True)
        else:
            self.pid_cb.set_active(False)
        if 2 in Config.processes_treeview_columns_shown:
            self.user_cb.set_active(True)
        else:
            self.user_cb.set_active(False)
        if 3 in Config.processes_treeview_columns_shown:
            self.status_cb.set_active(True)
        else:
            self.status_cb.set_active(False)
        if 4 in Config.processes_treeview_columns_shown:
            self.cpu_cb.set_active(True)
        else:
            self.cpu_cb.set_active(False)
        if 5 in Config.processes_treeview_columns_shown:
            self.memory_rss_cb.set_active(True)
        else:
            self.memory_rss_cb.set_active(False)
        if 6 in Config.processes_treeview_columns_shown:
            self.memory_vms_cb.set_active(True)
        else:
            self.memory_vms_cb.set_active(False)
        if 7 in Config.processes_treeview_columns_shown:
            self.memory_shared_cb.set_active(True)
        else:
            self.memory_shared_cb.set_active(False)
        if 8 in Config.processes_treeview_columns_shown:
            self.read_data_cb.set_active(True)
        else:
            self.read_data_cb.set_active(False)
        if 9 in Config.processes_treeview_columns_shown:
            self.write_data_cb.set_active(True)
        else:
            self.write_data_cb.set_active(False)
        if 10 in Config.processes_treeview_columns_shown:
            self.read_speed_cb.set_active(True)
        else:
            self.read_speed_cb.set_active(False)
        if 11 in Config.processes_treeview_columns_shown:
            self.write_speed_cb.set_active(True)
        else:
            self.write_speed_cb.set_active(False)
        if 12 in Config.processes_treeview_columns_shown:
            self.priority_cb.set_active(True)
        else:
            self.priority_cb.set_active(False)
        if 13 in Config.processes_treeview_columns_shown:
            self.threads_cb.set_active(True)
        else:
            self.threads_cb.set_active(False)
        if 14 in Config.processes_treeview_columns_shown:
            self.ppid_cb.set_active(True)
        else:
            self.ppid_cb.set_active(False)
        if 15 in Config.processes_treeview_columns_shown:
            self.uid_cb.set_active(True)
        else:
            self.uid_cb.set_active(False)
        if 16 in Config.processes_treeview_columns_shown:
            self.gid_cb.set_active(True)
        else:
            self.gid_cb.set_active(False)
        if 17 in Config.processes_treeview_columns_shown:
            self.path_cb.set_active(True)
        else:
            self.path_cb.set_active(False)
        if 18 in Config.processes_treeview_columns_shown:
            self.commandline_cb.set_active(True)
        else:
            self.commandline_cb.set_active(False)

        # Set GUI objects on Numbers tab 
        # Set data unit checkboxes.
        if Config.processes_memory_data_unit == 0:
            self.memory_data_power_of_1024_cb.set_active(True)
        if Config.processes_memory_data_unit == 1:
            self.memory_data_power_of_1000_cb.set_active(True)
        if Config.processes_disk_data_unit == 0:
            self.disk_data_power_of_1024_cb.set_active(True)
        if Config.processes_disk_data_unit == 1:
            self.disk_data_power_of_1000_cb.set_active(True)
        if Config.processes_disk_speed_bit == 1:
            self.show_speed_units_bytes_cb.set_active(True)
        if Config.processes_disk_speed_bit == 0:
            self.show_speed_units_bytes_cb.set_active(False)

        # Add CPU usage precision data into combobox
        precision_cpu_ls = Gtk.ListStore()
        precision_cpu_ls.set_column_types([str, int])
        self.precision_cpu_cmb.set_model(precision_cpu_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.precision_cpu_cmb.clear()
        renderer_text = Gtk.CellRendererText()
        self.precision_cpu_cmb.pack_start(renderer_text, True)
        self.precision_cpu_cmb.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            precision_cpu_ls.append([data[1], data[2]])
        self.precision_cpu_cmb.set_active(Config.processes_cpu_precision)

        # Add Memory data precision data into combobox
        precision_memory_ls = Gtk.ListStore()
        precision_memory_ls.set_column_types([str, int])
        self.precision_memory_cmb.set_model(precision_memory_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.precision_memory_cmb.clear()
        renderer_text = Gtk.CellRendererText()
        self.precision_memory_cmb.pack_start(renderer_text, True)
        self.precision_memory_cmb.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            precision_memory_ls.append([data[1], data[2]])
        self.precision_memory_cmb.set_active(Config.processes_memory_data_precision)

        # Add Disk data precision data into combobox
        precision_disk_ls = Gtk.ListStore()
        precision_disk_ls.set_column_types([str, int])
        self.precision_disk_cmb.set_model(precision_disk_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.precision_disk_cmb.clear()
        renderer_text = Gtk.CellRendererText()
        self.precision_disk_cmb.pack_start(renderer_text, True)
        self.precision_disk_cmb.add_attribute(renderer_text, "text", 0)
        for data in Config.number_precision_list:
            precision_disk_ls.append([data[1], data[2]])
        self.precision_disk_cmb.set_active(Config.processes_disk_data_precision)


    def processes_add_remove_columns_function(self):
        """
        Add/Remove columns to treeview.
        """

        Config.processes_treeview_columns_shown = []

        if self.name_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(0)
        if self.pid_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(1)
        if self.user_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(2)
        if self.status_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(3)
        if self.cpu_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(4)
        if self.memory_rss_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(5)
        if self.memory_vms_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(6)
        if self.memory_shared_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(7)
        if self.read_data_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(8)
        if self.write_data_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(9)
        if self.read_speed_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(10)
        if self.write_speed_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(11)
        if self.priority_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(12)
        if self.threads_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(13)
        if self.ppid_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(14)
        if self.uid_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(15)
        if self.gid_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(16)
        if self.path_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(17)
        if self.commandline_cb.get_active() == True:
            Config.processes_treeview_columns_shown.append(18)

        # Apply changes immediately (without waiting update interval).
        Processes.treeview_column_order_width_row_sorting()
        Processes.processes_initial_func()
        Processes.processes_loop_func()
        Config.config_save_func()


ProcessesMenu = ProcessesMenu()


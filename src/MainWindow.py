#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('Gio', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, GLib, Gio, Pango

import os
import locale

from locale import gettext as _tr

from Config import Config
from Performance import Performance


class MainWindow():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """
        Run initial functions and generate main window.
        """

        # Light/Dark theme
        self.light_dark_theme()

        # Configurations for language translation support
        self.language_translation_support()

        # Detect environment type (Flatpak or native)
        self.environment_type_detection()

        # Generate main window GUI
        self.main_window_gui()

        # Show root privileges warning
        self.root_privileges_warning()

        # Hide "Services" tab if systemd is not used on the system.
        self.hide_services_tab()

        # Run "Performance" module in order to provide performance data
        # to Performance tab and performance summary on the headerbar.
        Performance.performance_background_initial_func()

        # Define these settings in order to avoid error on the first call 
        # of "main_gui_tab_loop" function. This value is used in order to detect
        # the current tab without checking GUI obejects for lower CPU usage.
        # This value is not saved into settings file.
        Config.current_main_tab = -1
        Config.performance_tab_current_sub_tab = -1

        # Switch to default tab
        self.switch_to_default_tab()

        # Connect GUI signals after switching to default tab.
        self.connect_signals()


    def main_window_gui(self):
        """
        Generate main window GUI.
        """

        # Application window
        self.main_window = Gtk.ApplicationWindow()
        self.main_window.set_default_size(670, 570)
        self.main_window.set_title(_tr("System Monitoring Center"))
        self.main_window.set_icon_name("system-monitoring-center")

        # Resize/set state (full screen or not) of the main window if "remember window size" option is enabled.
        remember_window_size = Config.remember_window_size
        if remember_window_size[0] == 1:
            if remember_window_size[1] == 1:
                self.main_window.maximize()
            else:
                self.main_window.set_default_size(remember_window_size[2], remember_window_size[3])

        # HeaderBar (Main window)
        self.window_headerbar = Gtk.HeaderBar()
        self.window_headerbar.set_title_widget(None)
        self.main_window.set_titlebar(self.window_headerbar)

        # Main Grid
        self.main_grid = Gtk.Grid.new()
        self.main_grid.set_column_spacing(0)
        self.main_grid.set_row_spacing(4)
        self.main_grid.set_margin_top(5)
        self.main_grid.set_margin_bottom(5)
        self.main_grid.set_margin_start(5)
        self.main_grid.set_margin_end(5)
        self.main_window.set_child(self.main_grid)

        # Main menu
        self.main_menu_gui()

        # MenuButton (Main menu)
        self.main_menu_menubutton = Gtk.MenuButton()
        self.main_menu_menubutton.set_icon_name("open-menu-symbolic")
        self.main_menu_menubutton.set_has_frame(False)
        self.main_menu_menubutton.set_popover(self.main_menu_po_menu)
        self.main_menu_menubutton.set_direction(Gtk.ArrowType.DOWN)
        self.window_headerbar.pack_end(self.main_menu_menubutton)

        # MenuButton (Tab menus)
        self.tab_menu_menubutton = Gtk.MenuButton()
        self.tab_menu_menubutton.set_icon_name("document-properties-symbolic")
        self.tab_menu_menubutton.set_tooltip_text(_tr("Customization menu for the current tab"))
        self.tab_menu_menubutton.set_has_frame(False)
        self.tab_menu_menubutton.set_create_popup_func(self.tab_menu_popup_func)
        self.tab_menu_menubutton.set_direction(Gtk.ArrowType.DOWN)
        self.window_headerbar.pack_end(self.tab_menu_menubutton)

        # Performance summary on the window headerbar
        self.performance_summary_headerbar_gui()

        # Main tab (Performance, Processes, etc.) GUI
        self.main_tabs()

        # Performance tab sub-tab (Summary, CPU, etc.) GUI
        self.performance_tab_sub_tabs()


    def performance_summary_headerbar_gui(self):
        """
        Generate and configure performance summary GUI objects on the window headerbar.
        """

        # Main Grid
        self.performance_summary_hb_grid = Gtk.Grid.new()
        self.performance_summary_hb_grid.set_column_spacing(5)
        self.performance_summary_hb_grid.set_row_spacing(3)
        self.performance_summary_hb_grid.set_margin_start(6)
        self.performance_summary_hb_grid.set_valign(Gtk.Align.CENTER)
        self.window_headerbar.pack_start(self.performance_summary_hb_grid)

        # Bold and 2x label atributes
        attribute_list_small_size = Pango.AttrList()
        attribute = Pango.attr_size_new(10000)
        attribute_list_small_size.insert(attribute)

        # Label (CPU)
        label = Gtk.Label()
        label.set_attributes(attribute_list_small_size)
        label.set_halign(Gtk.Align.START)
        label.set_label(_tr("CPU") + ":")
        self.performance_summary_hb_grid.attach(label, 0, 0, 1, 1)

        # Label (RAM)
        label = Gtk.Label()
        label.set_attributes(attribute_list_small_size)
        label.set_halign(Gtk.Align.START)
        label.set_label(_tr("RAM") + ":")
        self.performance_summary_hb_grid.attach(label, 0, 1, 1, 1)

        # Label (Disk)
        label = Gtk.Label()
        label.set_attributes(attribute_list_small_size)
        label.set_halign(Gtk.Align.START)
        label.set_margin_start(10)
        label.set_label(_tr("Disk") + ":")
        label.set_tooltip_text(f'{_tr("Read Speed")} + {_tr("Write Speed")}')
        self.performance_summary_hb_grid.attach(label, 2, 0, 1, 1)

        # Label (Network)
        label = Gtk.Label()
        label.set_attributes(attribute_list_small_size)
        label.set_halign(Gtk.Align.START)
        label.set_margin_start(10)
        label.set_label(_tr("Network") + ":")
        label.set_tooltip_text(f'{_tr("Download Speed")} + {_tr("Upload Speed")}')
        self.performance_summary_hb_grid.attach(label, 2, 1, 1, 1)

        # DrawingArea (CPU)
        self.ps_hb_cpu_da = Gtk.DrawingArea()
        self.ps_hb_cpu_da.set_size_request(32, 10)
        self.ps_hb_cpu_da.set_halign(Gtk.Align.START)
        self.performance_summary_hb_grid.attach(self.ps_hb_cpu_da, 1, 0, 1, 1)

        # DrawingArea (RAM)
        self.ps_hb_ram_da = Gtk.DrawingArea()
        self.ps_hb_ram_da.set_size_request(32, 10)
        self.ps_hb_ram_da.set_halign(Gtk.Align.START)
        self.performance_summary_hb_grid.attach(self.ps_hb_ram_da, 1, 1, 1, 1)

        # Label (disk speed)
        self.ps_hb_disk_label = Gtk.Label()
        self.ps_hb_disk_label.set_attributes(attribute_list_small_size)
        self.ps_hb_disk_label.set_halign(Gtk.Align.START)
        self.ps_hb_disk_label.set_label("--")
        self.performance_summary_hb_grid.attach(self.ps_hb_disk_label, 3, 0, 1, 1)

        # Label (network speed)
        self.ps_hb_network_label = Gtk.Label()
        self.ps_hb_network_label.set_attributes(attribute_list_small_size)
        self.ps_hb_network_label.set_halign(Gtk.Align.START)
        self.ps_hb_network_label.set_label("--")
        self.performance_summary_hb_grid.attach(self.ps_hb_network_label, 3, 1, 1, 1)

        # Remove performance summary from the window headerbar
        if Config.performance_summary_on_the_headerbar == 0:
            self.window_headerbar.remove(self.performance_summary_hb_grid)


    def main_tabs(self):
        """
        Generate main tab (Performance, Processes, etc.) GUI objects.
        """

        # Grid (main tab togglebutton)
        main_tab_tb_grid = Gtk.Grid.new()
        main_tab_tb_grid.set_column_homogeneous(True)
        main_tab_tb_grid.set_halign(Gtk.Align.CENTER)
        main_tab_tb_grid.add_css_class("linked")
        main_tab_tb_grid.set_size_request(660, -1)  
        self.main_grid.attach(main_tab_tb_grid, 0, 0, 1, 1)

        # ToggleButton (Performance tab)
        self.performance_tb = Gtk.ToggleButton()
        self.performance_tb.set_group(None)
        main_tab_tb_grid.attach(self.performance_tb, 0, 0, 1, 1)
        # Grid (Performance tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_row_homogeneous(True)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        self.performance_tb.set_child(grid)
        # Image (Performance tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-performance-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (Performance tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("Performance"))
        grid.attach(label, 0, 1, 1, 1)

        # ToggleButton (Processes tab)
        self.processes_tb = Gtk.ToggleButton()
        self.processes_tb.set_group(self.performance_tb)
        main_tab_tb_grid.attach(self.processes_tb, 1, 0, 1, 1)
        # Grid (Processes tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_row_homogeneous(True)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        self.processes_tb.set_child(grid)
        # Image (Processes tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-process-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (Processes tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("Processes"))
        grid.attach(label, 0, 1, 1, 1)

        # ToggleButton (Users tab)
        self.users_tb = Gtk.ToggleButton()
        self.users_tb.set_group(self.performance_tb)
        main_tab_tb_grid.attach(self.users_tb, 2, 0, 1, 1)
        # Grid (Users tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_row_homogeneous(True)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        self.users_tb.set_child(grid)
        # Image (Users tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-user-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (Users tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("Users"))
        grid.attach(label, 0, 1, 1, 1)

        # ToggleButton (Services tab)
        self.services_tb = Gtk.ToggleButton()
        self.services_tb.set_group(self.performance_tb)
        main_tab_tb_grid.attach(self.services_tb, 3, 0, 1, 1)
        # Grid (Services tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_row_homogeneous(True)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        self.services_tb.set_child(grid)
        # Image (Services tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-services-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (Services tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("Services"))
        grid.attach(label, 0, 1, 1, 1)

        # ToggleButton (System tab)
        self.system_tb = Gtk.ToggleButton()
        self.system_tb.set_group(self.performance_tb)
        main_tab_tb_grid.attach(self.system_tb, 4, 0, 1, 1)
        # Grid (System tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_row_homogeneous(True)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        self.system_tb.set_child(grid)
        # Image (System tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-system-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (System tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("System"))
        grid.attach(label, 0, 1, 1, 1)

        # Separator between main tab togglebuttons and main tabs
        separator = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
        separator.set_size_request(-1, -1)  
        self.main_grid.attach(separator, 0, 1, 1, 1)

        # Stack (main tab)
        self.main_tab_stack = Gtk.Stack.new()
        self.main_tab_stack.set_hexpand(True)
        self.main_tab_stack.set_vexpand(True)
        self.main_tab_stack.set_hhomogeneous(True)
        self.main_tab_stack.set_vhomogeneous(True)
        self.main_tab_stack.set_transition_type(Gtk.StackTransitionType.NONE)
        self.main_grid.attach(self.main_tab_stack, 0, 2, 1, 1)

        # Main Grid (Performance tab)
        self.performance_tab_main_grid = Gtk.Grid.new()
        self.performance_tab_main_grid.set_column_spacing(2)
        self.main_tab_stack.add_child(self.performance_tab_main_grid)

        # Main Grid (Processes tab)
        self.processes_tab_main_grid = Gtk.Grid.new()
        self.main_tab_stack.add_child(self.processes_tab_main_grid)

        # Main Grid (Users tab)
        self.users_tab_main_grid = Gtk.Grid.new()
        self.main_tab_stack.add_child(self.users_tab_main_grid)

        # Main Grid (Services tab)
        self.services_tab_main_grid = Gtk.Grid.new()
        self.main_tab_stack.add_child(self.services_tab_main_grid)

        # Main Grid (system tab)
        self.system_tab_main_grid = Gtk.Grid.new()
        self.main_tab_stack.add_child(self.system_tab_main_grid)


    def performance_tab_sub_tabs(self):
        """
        Generate Performance tab sub-tab (Summary, CPU, etc.) GUI.
        """

        # Main Grid (Performance tab sub-tab togglebuttons)
        self.sub_tab_tb_grid = Gtk.Grid.new()
        self.sub_tab_tb_grid.set_orientation(Gtk.Orientation.VERTICAL)
        self.sub_tab_tb_grid.add_css_class("linked")
        self.sub_tab_tb_grid.set_valign(Gtk.Align.START)
        self.sub_tab_tb_grid.set_margin_top(35)
        self.performance_tab_main_grid.attach(self.sub_tab_tb_grid, 0, 0, 1, 1)

        # ToggleButton (Summary tab)
        self.summary_tb = Gtk.ToggleButton()
        self.summary_tb.set_group(None)
        self.sub_tab_tb_grid.attach(self.summary_tb, 0, 0, 1, 1)
        # Grid (Summary tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_column_spacing(3)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_margin_top(2)
        grid.set_margin_bottom(2)
        self.summary_tb.set_child(grid)
        # Image (Summary tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-performance-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (Summary tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("Summary"))
        grid.attach(label, 1, 0, 1, 1)

        # ToggleButton (CPU tab)
        self.cpu_tb = Gtk.ToggleButton()
        self.cpu_tb.set_group(self.summary_tb)
        self.sub_tab_tb_grid.attach(self.cpu_tb, 0, 2, 1, 1)
        # Grid (CPU tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_column_spacing(3)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_margin_top(2)
        grid.set_margin_bottom(2)
        self.cpu_tb.set_child(grid)
        # Image (CPU tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-cpu-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (CPU tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("CPU"))
        grid.attach(label, 1, 0, 1, 1)

        # ToggleButton (Memory tab)
        self.memory_tb = Gtk.ToggleButton()
        self.memory_tb.set_group(self.summary_tb)
        self.sub_tab_tb_grid.attach(self.memory_tb, 0, 4, 1, 1)
        # Grid (Memory tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_column_spacing(3)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_margin_top(2)
        grid.set_margin_bottom(2)
        self.memory_tb.set_child(grid)
        # Image (Memory tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-ram-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (Memory tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("Memory"))
        grid.attach(label, 1, 0, 1, 1)

        # ToggleButton (Disk tab)
        self.disk_tb = Gtk.ToggleButton()
        self.disk_tb.set_group(self.summary_tb)
        self.sub_tab_tb_grid.attach(self.disk_tb, 0, 6, 1, 1)
        # Grid (Disk tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_column_spacing(3)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_margin_top(2)
        grid.set_margin_bottom(2)
        self.disk_tb.set_child(grid)
        # Image (Disk tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-disk-hdd-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (Disk tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("Disk"))
        grid.attach(label, 1, 0, 1, 1)

        # ToggleButton (Network tab)
        self.network_tb = Gtk.ToggleButton()
        self.network_tb.set_group(self.summary_tb)
        self.sub_tab_tb_grid.attach(self.network_tb, 0, 8, 1, 1)
        # Grid (Network tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_column_spacing(3)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_margin_top(2)
        grid.set_margin_bottom(2)
        self.network_tb.set_child(grid)
        # Image (Network tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-network-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (Network tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("Network"))
        grid.attach(label, 1, 0, 1, 1)

        # ToggleButton (GPU tab)
        self.gpu_tb = Gtk.ToggleButton()
        self.gpu_tb.set_group(self.summary_tb)
        self.sub_tab_tb_grid.attach(self.gpu_tb, 0, 10, 1, 1)
        # Grid (GPU tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_column_spacing(3)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_margin_top(2)
        grid.set_margin_bottom(2)
        self.gpu_tb.set_child(grid)
        # Image (GPU tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-graphics-card-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (GPU tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("GPU"))
        grid.attach(label, 1, 0, 1, 1)

        # ToggleButton (Sensors tab)
        self.sensors_tb = Gtk.ToggleButton()
        self.sensors_tb.set_group(self.summary_tb)
        self.sub_tab_tb_grid.attach(self.sensors_tb, 0, 12, 1, 1)
        # Grid (Sensors tab togglebutton)
        grid = Gtk.Grid.new()
        grid.set_column_spacing(3)
        grid.set_valign(Gtk.Align.CENTER)
        grid.set_margin_top(2)
        grid.set_margin_bottom(2)
        self.sensors_tb.set_child(grid)
        # Image (Sensors tab togglebutton)
        image = Gtk.Image()
        image.set_from_icon_name("system-monitoring-center-temperature-symbolic")
        image.set_pixel_size(24)
        grid.attach(image, 0, 0, 1, 1)
        # Label (Sensors tab togglebutton)
        label = Gtk.Label()
        label.set_label(_tr("Sensors"))
        grid.attach(label, 1, 0, 1, 1)

        # Separator between Performance tab sub-tab togglebuttons and sub-tabs
        separator = Gtk.Separator.new(Gtk.Orientation.VERTICAL)
        separator.set_size_request(-1, 446)  
        self.performance_tab_main_grid.attach(separator, 1, 0, 1, 1)

        # Stack (Performance tab sub-tabs)
        self.sub_tab_stack = Gtk.Stack.new()
        self.sub_tab_stack.set_hexpand(True)
        self.sub_tab_stack.set_vexpand(True)
        self.sub_tab_stack.set_hhomogeneous(True)
        self.sub_tab_stack.set_vhomogeneous(True)
        self.sub_tab_stack.set_transition_type(Gtk.StackTransitionType.NONE)
        self.performance_tab_main_grid.attach(self.sub_tab_stack, 2, 0, 1, 1)

        # Main Grid (Summary tab)
        self.summary_tab_main_grid = Gtk.Grid.new()
        self.sub_tab_stack.add_child(self.summary_tab_main_grid)

        # Main Grid (CPU tab)
        self.cpu_tab_main_grid = Gtk.Grid.new()
        self.sub_tab_stack.add_child(self.cpu_tab_main_grid)

        # Main Grid (Memory tab)
        self.memory_tab_main_grid = Gtk.Grid.new()
        self.sub_tab_stack.add_child(self.memory_tab_main_grid)

        # Main Grid (Disk tab)
        self.disk_tab_main_grid = Gtk.Grid.new()
        self.sub_tab_stack.add_child(self.disk_tab_main_grid)

        # Main Grid (Network tab)
        self.network_tab_main_grid = Gtk.Grid.new()
        self.sub_tab_stack.add_child(self.network_tab_main_grid)

        # Main Grid (GPU tab)
        self.gpu_tab_main_grid = Gtk.Grid.new()
        self.sub_tab_stack.add_child(self.gpu_tab_main_grid)

        # Main Grid (Sensors tab)
        self.sensors_tab_main_grid = Gtk.Grid.new()
        self.sub_tab_stack.add_child(self.sensors_tab_main_grid)


    def connect_signals(self):
        """
        Connect GUI signals.
        """

        # Main window signals
        self.main_window.connect("close-request", self.on_main_window_close_request)
        self.main_window.connect("show", self.on_main_window_show)

        # Main tab togglebutton signals
        self.performance_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)
        self.processes_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)
        self.users_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)
        self.services_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)
        self.system_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)

        # Performance tab sub-tabs togglebutton signals
        self.summary_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)
        self.cpu_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)
        self.memory_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)
        self.disk_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)
        self.network_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)
        self.gpu_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)
        self.sensors_tb.connect("toggled", self.on_main_gui_togglebuttons_toggled)

        # Performance summary drawingarea (on the window headerbar) functions
        self.ps_hb_cpu_da.set_draw_func(Performance.performance_bar_charts_draw, "ps_hb_cpu_da")
        self.ps_hb_ram_da.set_draw_func(Performance.performance_bar_charts_draw, "ps_hb_ram_da")


    def on_main_window_close_request(self, widget):
        """
        Called when window close button (X) is clicked.
        """

        # Get and save window state (if full screen or not), window size (width, height)
        if Config.remember_window_size[0] == 1:
            main_window_state = widget.is_maximized()
            if main_window_state == True:
                main_window_state = 1
            if main_window_state == False:
                main_window_state = 0
            main_window_width = widget.get_width()
            main_window_height = widget.get_height()
            remember_window_size_value = Config.remember_window_size[0]
            Config.remember_window_size = [remember_window_size_value, main_window_state, main_window_width, main_window_height]
            Config.config_save_func()

        # Close the application
        self.main_window.get_application().quit()


    def on_main_window_show(self, widget):
        """
        Called when window is shown.
        """

        # Start the main loop function
        self.main_gui_tab_loop()

        # Run main tab function (It is also called when main tab togglebuttons are toggled).
        self.main_gui_tab_switch()

        # Check for updates (Python package only)
        self.check_for_updates()


    def main_menu_gui(self):
        """
        Generate main menu GUI.
        """

        # Menu actions
        # "General Settings" action
        action = Gio.SimpleAction.new("settings", None)
        action.connect("activate", self.on_main_menu_settings_button_clicked)
        self.main_window.add_action(action)
        # "About" action
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_main_menu_about_button_clicked)
        self.main_window.add_action(action)

        # Menu model
        main_menu_model = Gio.Menu.new()
        main_menu_model.append(_tr("General Settings"), "win.settings")
        main_menu_model.append(_tr("About"), "win.about")

        # Popover menu
        self.main_menu_po_menu = Gtk.PopoverMenu()
        self.main_menu_po_menu.set_menu_model(main_menu_model)


    def on_main_menu_settings_button_clicked(self, action, parameter):
        """
        Generate and show settings window.
        """

        from SettingsWindow import SettingsWindow
        SettingsWindow.settings_window.present()


    def on_main_menu_about_button_clicked(self, action, parameter):
        """
        Generate and show about dialog.
        """

        try:
            self.about_dialog.present()
        except AttributeError:
            # Avoid generating menu multiple times on every main menu button click.
            self.about_dialog_gui()
            self.about_dialog.present()


    def about_dialog_gui(self):
        """
        Generate about dialog.
        """

        # Get software version
        with open(os.path.dirname(os.path.abspath(__file__)) + "/__version__") as reader:
            software_version = reader.read().strip()

        # Define translators list
        translators_list = [
                            "panmourovaty (čeština)",
                            "Baumfinder (Deutsch)",
                            "MasterKia (فارسی)",
                            "Kálmán Szalai (Magyar)",
                            "ski007, K0RR, sdorpl (polski)",
                            "Bruno do Nascimento (português do Brasil)",
                            "Ricardo Simões (português europeu)",
                            "akorny (Русский)",
                            "Hakan Dündar (Türkçe)",
                            "ruojiner, Luo ( 汉语)"
                           ]
        translators_list = '\n'.join(translators_list)

        # AboutDialog
        self.about_dialog = Gtk.AboutDialog()
        self.about_dialog.set_modal(self.main_window)
        self.about_dialog.set_transient_for(self.main_window)
        self.about_dialog.set_program_name(_tr("System Monitoring Center"))
        self.about_dialog.set_logo_icon_name("system-monitoring-center")
        self.about_dialog.set_comments(_tr("Multi-featured system monitor."))
        self.about_dialog.set_authors(["Hakan Dündar"])
        self.about_dialog.set_version(software_version)
        self.about_dialog.set_copyright("© 2022 Hakan Dündar")
        self.about_dialog.set_website("https://github.com/hakandundar34coding/system-monitoring-center")
        self.about_dialog.set_license_type(Gtk.License.GPL_3_0)
        self.about_dialog.set_translator_credits(translators_list)
        # Hide the window/dialog when it is closed. Otherwise, it is deleted.
        # But opening window/dialog multiple times without deleting it consumes more memory each time.
        self.about_dialog.set_hide_on_close(True)


    def tab_menu_popup_func(self, val=None):
        """
        Set menu popup function by checking the current main tab and the sub-tab.
        Relevant menu is attached to the tab menu menubutton by checking tabs.
        """

        if Config.current_main_tab == 0:

            if Config.performance_tab_current_sub_tab == 0:
                self.tab_menu_menubutton.set_popover(None)

            elif Config.performance_tab_current_sub_tab == 1:
                from CpuMenu import CpuMenu
                self.tab_menu_menubutton.set_popover(CpuMenu.cpu_menu_po)

            elif Config.performance_tab_current_sub_tab == 2:
                from MemoryMenu import MemoryMenu
                self.tab_menu_menubutton.set_popover(MemoryMenu.memory_menu_po)

            elif Config.performance_tab_current_sub_tab == 3:
                from DiskMenu import DiskMenu
                self.tab_menu_menubutton.set_popover(DiskMenu.disk_menu_po)

            elif Config.performance_tab_current_sub_tab == 4:
                from NetworkMenu import NetworkMenu
                self.tab_menu_menubutton.set_popover(NetworkMenu.network_menu_po)

            elif Config.performance_tab_current_sub_tab == 5:
                from GpuMenu import GpuMenu
                self.tab_menu_menubutton.set_popover(GpuMenu.gpu_menu_po)

            elif Config.performance_tab_current_sub_tab == 6:
                self.tab_menu_menubutton.set_popover(None)

        elif Config.current_main_tab == 1:
            from ProcessesMenu import ProcessesMenu
            self.tab_menu_menubutton.set_popover(ProcessesMenu.processes_menu_po)

        elif Config.current_main_tab == 2:
            from UsersMenu import UsersMenu
            self.tab_menu_menubutton.set_popover(UsersMenu.users_menu_po)

        elif Config.current_main_tab == 3:
            from ServicesMenu import ServicesMenu
            self.tab_menu_menubutton.set_popover(ServicesMenu.services_menu_po)

        elif Config.current_main_tab == 4:
             self.tab_menu_menubutton.set_popover(None)


    def light_dark_theme(self):
        """
        Set light/dark theme for GUI.
        """

        if Config.light_dark_theme == "system":
            pass

        elif Config.light_dark_theme == "light":
            Gtk.Settings.get_default().props.gtk_application_prefer_dark_theme = False

        elif Config.light_dark_theme == "dark":
            Gtk.Settings.get_default().props.gtk_application_prefer_dark_theme = True


    def language_translation_support(self):
        """
        Configurations for language translation support.
        """

        locale.bindtextdomain("system-monitoring-center", os.path.dirname(os.path.realpath(__file__)) + "/../locale")
        locale.textdomain("system-monitoring-center")

        if Config.language == "system":
            application_language = os.environ.get("LANG")
        else:
            application_language = Config.language

        try:
            locale.setlocale(locale.LC_ALL, application_language)
        # Prevent errors if there are problems with language installations on the system.
        except Exception:
            pass


    def environment_type_detection(self):
        """
        Detect environment type (Flatpak, Python package or native).
        This information will be used for accessing host OS commands if the application is
        # run in Flatpak environment or for showing new version information, etc. if the application
        # is a Python package.
        """

        current_dir = os.path.dirname(os.path.realpath(__file__))
        current_user_homedir = os.environ.get('HOME')
        application_flatpak_id = os.getenv('FLATPAK_ID')

        if application_flatpak_id != None:
            environment_type = "flatpak"

        elif current_dir.startswith("/usr/local/lib/python") == True or current_dir.startswith(current_user_homedir + "/.local/lib/python") == True:
            environment_type = "python_package"

        else:
            environment_type = "native"

        Config.environment_type = environment_type


    def on_main_gui_togglebuttons_toggled(self, widget):
        """
        Called by tab togglebuttons. Prevents repetitive calls when togglebuttons are toggled.
        Runs tab functions (Performance, Processes, CPU, Memory, etc.) when their togglebutton is toggled).
        """

        if widget.get_active() == True:
            self.main_gui_tab_switch()


    def main_gui_tab_switch(self):
        """
        Runs tab functions (Performance, Processes, CPU, Memory, etc.) when their togglebuttons is toggled).
        """

        # Switch to "Performance" tab
        if self.performance_tb.get_active() == True:
            self.main_tab_stack.set_visible_child(self.performance_tab_main_grid)
            if Config.remember_last_opened_tabs_on_application_start == 1:
                # No need to save Config values after this value is defined.Because save operation
                # is performed for Performance tab sub-tabs (CPU, Memory, Disk, Network, GPU, Sensors tabs).
                Config.default_main_tab = 0
            Config.current_main_tab = 0

            # Switch to "Summary" tab
            if self.summary_tb.get_active() == True:
                self.sub_tab_stack.set_visible_child(self.summary_tab_main_grid)
                if Config.remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 0
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 0
                # Attach the grid to the grid (on the Main Window) at (0, 0) position if not attached.
                if self.summary_tab_main_grid.get_child_at(0,0) == None:
                    global Summary
                    from Summary import Summary
                    self.summary_tab_main_grid.attach(Summary.tab_grid, 0, 0, 1, 1)
                # Run initial function of the module if this is the first loop of the module.
                if Summary.initial_already_run == 0:
                    GLib.idle_add(Summary.summary_initial_func)
                # Run loop Summary loop function in order to get data without waiting update interval.
                GLib.idle_add(Summary.summary_loop_func)
                # Show device selection list on a listbox between radiobuttons of Performance tab sub-tabs.
                self.main_gui_device_selection_list()
                self.tab_menu_menubutton.set_sensitive(False)
                return

            # Switch to "CPU" tab
            if self.cpu_tb.get_active() == True:
                self.sub_tab_stack.set_visible_child(self.cpu_tab_main_grid)
                if Config.remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 1
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 1
                if self.cpu_tab_main_grid.get_child_at(0,0) == None:
                    global Cpu
                    from Cpu import Cpu
                    self.cpu_tab_main_grid.attach(Cpu.tab_grid, 0, 0, 1, 1)
                if Cpu.initial_already_run == 0:
                    GLib.idle_add(Cpu.cpu_initial_func)
                GLib.idle_add(Cpu.cpu_loop_func)
                self.main_gui_device_selection_list()
                self.tab_menu_menubutton.set_sensitive(True)
                return

            # Switch to "Memory" tab
            elif self.memory_tb.get_active() == True:
                self.sub_tab_stack.set_visible_child(self.memory_tab_main_grid)
                if Config.remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 2
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 2
                if self.memory_tab_main_grid.get_child_at(0,0) == None:
                    global Memory
                    from Memory import Memory
                    self.memory_tab_main_grid.attach(Memory.tab_grid, 0, 0, 1, 1)
                if Memory.initial_already_run == 0:
                    GLib.idle_add(Memory.memory_initial_func)
                GLib.idle_add(Memory.memory_loop_func)
                self.main_gui_device_selection_list()
                self.tab_menu_menubutton.set_sensitive(True)
                return

            # Switch to "Disk" tab
            elif self.disk_tb.get_active() == True:
                self.sub_tab_stack.set_visible_child(self.disk_tab_main_grid)
                if Config.remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 3
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 3
                if self.disk_tab_main_grid.get_child_at(0,0) == None:
                    global Disk
                    from Disk import Disk
                    self.disk_tab_main_grid.attach(Disk.tab_grid, 0, 0, 1, 1)
                if Disk.initial_already_run == 0:
                    GLib.idle_add(Disk.disk_initial_func)
                GLib.idle_add(Disk.disk_loop_func)
                self.main_gui_device_selection_list()
                self.tab_menu_menubutton.set_sensitive(True)
                return

            # Switch to "Network" tab
            elif self.network_tb.get_active() == True:
                self.sub_tab_stack.set_visible_child(self.network_tab_main_grid)
                if Config.remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 4
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 4
                if self.network_tab_main_grid.get_child_at(0,0) == None:
                    global Network
                    from Network import Network
                    self.network_tab_main_grid.attach(Network.tab_grid, 0, 0, 1, 1)
                if Network.initial_already_run == 0:
                    GLib.idle_add(Network.network_initial_func)
                GLib.idle_add(Network.network_loop_func)
                self.main_gui_device_selection_list()
                self.tab_menu_menubutton.set_sensitive(True)
                return

            # Switch to "GPU" tab
            elif self.gpu_tb.get_active() == True:
                self.sub_tab_stack.set_visible_child(self.gpu_tab_main_grid)
                if Config.remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 5
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 5
                if self.gpu_tab_main_grid.get_child_at(0,0) == None:
                    global Gpu
                    from Gpu import Gpu
                    self.gpu_tab_main_grid.attach(Gpu.tab_grid, 0, 0, 1, 1)
                if Gpu.initial_already_run == 0:
                    GLib.idle_add(Gpu.gpu_initial_func)
                GLib.idle_add(Gpu.gpu_loop_func)
                try:
                    self.main_gui_device_selection_list()
                except AttributeError:
                    pass
                self.tab_menu_menubutton.set_sensitive(True)
                return

            # Switch to "Sensors" tab
            elif self.sensors_tb.get_active() == True:
                self.sub_tab_stack.set_visible_child(self.sensors_tab_main_grid)
                if Config.remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 6
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 6
                if 'Sensors' not in globals():
                    global Sensors
                    import Sensors
                    Sensors.sensors_import_func()
                    Sensors.sensors_gui_func()
                    self.sensors_tab_main_grid.attach(Sensors.sensors_tab_grid, 0, 0, 1, 1)
                if Sensors.initial_already_run == 0:
                    Sensors.sensors_initial_func()
                Sensors.sensors_loop_func()
                self.main_gui_device_selection_list()
                self.tab_menu_menubutton.set_sensitive(False)
                return

        # Switch to "Processes" tab
        elif self.processes_tb.get_active() == True:
            self.main_tab_stack.set_visible_child(self.processes_tab_main_grid)
            if Config.remember_last_opened_tabs_on_application_start == 1:
                Config.default_main_tab = 1
                Config.config_save_func()
            Config.current_main_tab = 1
            if self.processes_tab_main_grid.get_child_at(0,0) == None:
                global Processes
                from Processes import Processes
                self.processes_tab_main_grid.attach(Processes.processes_tab_grid, 0, 0, 1, 1)
            if Processes.initial_already_run == 0:
                GLib.idle_add(Processes.processes_initial_func)
            GLib.idle_add(Processes.processes_loop_func)
            self.tab_menu_menubutton.set_sensitive(True)
            return

        # Switch to "Users" tab
        elif self.users_tb.get_active() == True:
            self.main_tab_stack.set_visible_child(self.users_tab_main_grid)
            if Config.remember_last_opened_tabs_on_application_start == 1:
                Config.default_main_tab = 2
                Config.config_save_func()
            Config.current_main_tab = 2
            if self.users_tab_main_grid.get_child_at(0,0) == None:
                global Users
                from Users import Users
                self.users_tab_main_grid.attach(Users.users_tab_grid, 0, 0, 1, 1)
            if Users.initial_already_run == 0:
                GLib.idle_add(Users.users_initial_func)
            GLib.idle_add(Users.users_loop_func)
            self.tab_menu_menubutton.set_sensitive(True)
            return

        # Switch to "Services" tab
        elif self.services_tb.get_active() == True:
            self.main_tab_stack.set_visible_child(self.services_tab_main_grid)
            if Config.remember_last_opened_tabs_on_application_start == 1:
                Config.default_main_tab = 3
                Config.config_save_func()
            Config.current_main_tab = 3
            if self.services_tab_main_grid.get_child_at(0,0) == None:
                global Services
                from Services import Services
                self.services_tab_main_grid.attach(Services.services_tab_grid, 0, 0, 1, 1)
            if Services.initial_already_run == 0:
                GLib.idle_add(Services.services_initial_func)
            GLib.idle_add(Services.services_loop_func)
            self.tab_menu_menubutton.set_sensitive(True)
            return

        # Switch to "System" tab
        elif self.system_tb.get_active() == True:
            self.main_tab_stack.set_visible_child(self.system_tab_main_grid)
            if Config.remember_last_opened_tabs_on_application_start == 1:
                Config.default_main_tab = 4
                Config.config_save_func()
            Config.current_main_tab = 4
            if self.system_tab_main_grid.get_child_at(0,0) == None:
                global System
                from System import System
                self.system_tab_main_grid.attach(System.tab_grid, 0, 0, 1, 1)
            if System.initial_already_run == 0:
                GLib.idle_add(System.system_initial_func)
            self.tab_menu_menubutton.set_sensitive(False)
            return


    def main_gui_device_selection_list(self):
        """
        Add device list into the listbox between the Performance tab sub-tab radiobuttons (CPU, Memory, etc.).
        """

        # Delete previous scrolledwindow and widgets in it in order to add a new one again.
        # Otherwise, removing all of the listbox rows requires removing them one by one.
        try:
            self.sub_tab_tb_grid.remove(self.device_list_sw)
            # It has to be deleted after removal in order to prevent Gtk warnings when new one is added.
            del self.device_list_sw
        # Prevent error if this is the first tab switch and there is no scrolledwindow.
        except AttributeError:
            pass

        # Define variables for to be used for adding devices to list.
        # Check if Summary tab is selected.
        if Config.performance_tab_current_sub_tab == 0:
            device_list = [_tr("Summary")]
            selected_device_number = 0
            listbox_row_number = 1
            tooltip_text = ""

        # Check if CPU tab is selected.
        elif Config.performance_tab_current_sub_tab == 1:
            device_list = Performance.logical_core_list_system_ordered
            selected_device_number = Performance.selected_cpu_core_number
            listbox_row_number = 3
            tooltip_text = _tr("CPU core selection affects only frequency and cache memory information.")

        # Check if Memory tab is selected.
        elif Config.performance_tab_current_sub_tab == 2:
            device_list = [_tr("RAM") + "-" + _tr("Swap Memory")]
            selected_device_number = 0
            listbox_row_number = 5
            tooltip_text = ""

        # Check if Disk tab is selected.
        elif Config.performance_tab_current_sub_tab == 3:
            device_list_full = Performance.disk_list_system_ordered
            device_list = []
            for device in device_list_full:
                # Do not add the device into the listbox and skip to the next loop if
                # "hide_loop_ramdisk_zram_disks" option is enabled and device is a loop, ramdisk or zram device.
                if Config.hide_loop_ramdisk_zram_disks == 1:
                    if device.startswith("loop") == True or device.startswith("ram") == True or device.startswith("zram") == True:
                        continue
                device_list.append(device)
            # "selected_device_number" for Disk tab is get in a different way.
            # Because device list may be changed if "hide_loop_ramdisk_zram_disks" option is enabled.
            selected_device_number = device_list.index(Performance.disk_list_system_ordered[Performance.selected_disk_number])
            listbox_row_number = 7
            tooltip_text = ""

        # Check if Network tab is selected.
        elif Config.performance_tab_current_sub_tab == 4:
            device_list = Performance.network_card_list
            selected_device_number = Performance.selected_network_card_number
            listbox_row_number = 9
            tooltip_text = ""

        # Check if GPU tab is selected.
        elif Config.performance_tab_current_sub_tab == 5:
            device_list = Gpu.gpu_list
            selected_device_number = Gpu.selected_gpu_number
            listbox_row_number = 11
            tooltip_text = ""

        # Check if Sensors tab is selected.
        elif Config.performance_tab_current_sub_tab == 6:
            return

        # Generate new widgets.
        self.device_list_sw = Gtk.ScrolledWindow()
        viewport = Gtk.Viewport()
        listbox = Gtk.ListBox()

        # Set properties of the scrolledwindow.
        self.device_list_sw.set_size_request(-1, 130)
        self.device_list_sw.set_margin_start(8)
        self.device_list_sw.set_tooltip_text(tooltip_text)

        # Run function when a listbox row is clicked.
        def on_row_activated(widget, row):

            # Get selected device name.
            selected_device = device_list[row.get_index()]

            # Check if Summary tab is selected.
            if Config.performance_tab_current_sub_tab == 0:
                pass

            # Check if CPU tab is selected.
            elif Config.performance_tab_current_sub_tab == 1:
                # Set selected device.
                Config.selected_cpu_core = selected_device
                Performance.performance_set_selected_cpu_core_func()

                # Apply changes immediately (without waiting update interval).
                Cpu.cpu_initial_func()
                Cpu.cpu_loop_func()
                Config.config_save_func()

            # Check if Memory tab is selected.
            elif Config.performance_tab_current_sub_tab == 2:
                pass

            # Check if Disk tab is selected.
            elif Config.performance_tab_current_sub_tab == 3:
                Config.selected_disk = selected_device
                Performance.performance_set_selected_disk_func()

                # Apply changes immediately (without waiting update interval).
                Disk.disk_initial_func()
                Disk.disk_loop_func()
                Config.config_save_func()

            # Check if Network tab is selected.
            elif Config.performance_tab_current_sub_tab == 4:
                Config.selected_network_card = selected_device
                Performance.performance_set_selected_network_card_func()

                # Apply changes immediately (without waiting update interval).
                Network.network_initial_func()
                Network.network_loop_func()
                Config.config_save_func()

            # Check if GPU tab is selected.
            elif Config.performance_tab_current_sub_tab == 5:
                Config.selected_gpu = selected_device
                Gpu.gpu_get_gpu_list_and_boot_vga_func()

                # Apply changes immediately (without waiting update interval).
                Gpu.gpu_initial_func()
                Gpu.gpu_loop_func()
                Config.config_save_func()

            # Check if Sensors tab is selected.
            elif Config.performance_tab_current_sub_tab == 6:
                pass

        # Add devices to listbox.
        for device in device_list:
            row = Gtk.ListBoxRow()
            grid = Gtk.Grid()
            label = Gtk.Label()
            label.set_label(device)
            grid.attach(label, 0, 0, 1, 1)
            # Also add disk usage percentage label next to device name if this is Disk tab.
            if Config.performance_tab_current_sub_tab == 3:
                disk_filesystem_information_list = Disk.disk_file_system_information_func(device_list)
                _, _, _, _, disk_usage_percentage, disk_mount_point = Disk.disk_file_system_capacity_used_free_used_percent_mount_point_func(disk_filesystem_information_list, device_list, device)
                label = Gtk.Label()
                label.set_sensitive(False)
                if disk_mount_point == "[" + _tr("Not mounted") + "]":
                    label.set_label(f'  (-%)')
                else:
                    label.set_label(f'  ({disk_usage_percentage:.0f}%)')
                grid.attach(label, 1, 0, 1, 1)
            row.set_child(grid)
            listbox.append(row)

        # Connect signal for the listbox.
        listbox.connect("row-activated", on_row_activated)

        # Add widgets into the grid in main GUI module.
        viewport.set_child(listbox)
        self.device_list_sw.set_child(viewport)
        self.sub_tab_tb_grid.attach(self.device_list_sw, 0, listbox_row_number, 1, 1)

        try:
            listbox.select_row(listbox.get_row_at_index(selected_device_number))
        # Prevent error if a disk is hidden by changing the relevant option while it was selected.
        # There is no need to update the list from this function because it will be set as hidden in the list
        # by another function (in Disk module) immediately.
        except IndexError:
            pass


    def hide_services_tab(self):
        """
        Hide Services tab if systemd is not used on the system.
        """

        try:
            # Access host OS commands if the application is run in Flatpak environment.
            if Config.environment_type == "flatpak":
                import subprocess
                process_name = (subprocess.check_output(["flatpak-spawn", "--host", "cat", "/proc/1/comm"], shell=False)).decode().strip()
            else:
                with open("/proc/1/comm") as reader:
                    process_name = reader.read().strip()
            if process_name != "systemd":
                self.services_tb.set_visible(False)
        except Exception:
            pass


    def root_privileges_warning(self):
        """
        Show information for warning the user if the application has been run with root privileges (if UID=0).
        Information is shown below the application window headerbar.
        """

        if os.geteuid() == 0:

            # Define label style
            css = b"label {background: rgba(100%,0%,0%,1.0);}"
            style_provider = Gtk.CssProvider()
            style_provider.load_from_data(css)

            # Generate a new label for the information and attach it to the grid at (0, 0) position.
            label_root_warning = Gtk.Label(label=_tr("Warning! The application has been run with root privileges, you may harm your system."))
            label_root_warning.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            self.main_grid.insert_row(0)
            # Attach the label to the grid at (0, 0) position.
            self.main_grid.attach(label_root_warning, 0, 0, 1, 1)
            label_root_warning.set_visible(True)


    def check_for_updates(self):
        """
        Check if there is a newer version of the software if relevant setting is enabled and
        the application is a Python package (directory is in "/usr/local/lib/..." or in "/home/[user_name]/.local/lib/...".
        New version can not be checked if the application is run with root privileges.
        Because "pip" does not run "index" command in this situation.
        """

        if Config.environment_type!= "python_package":
            return

        if Config.check_for_updates_automatically == 1:

            # Get current directory (which code of this application is in) and current user home directory (symlinks will be generated in).
            current_dir = os.path.dirname(os.path.realpath(__file__))
            current_user_homedir = os.environ.get('HOME')

            # Run the function in a separate thread in order to avoid blocking the GUI because "pip ..." command runs about 1 seconds.
            from threading import Thread
            Thread(target=self.update_check_func, daemon=True).start()


    def update_check_func(self):
        """
        Check if there is a newer version of the application on PyPI.
        """

        import time, subprocess

        # Wait 5 seconds before running the command in order to avoid high CPU usage at the beginning of the measurement.
        time.sleep(5)

        # Get installed and latest versions of the application.
        command_list = ["pip", "index", "versions", "system-monitoring-center"]
        try:
            pip_index_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split("\n")
        except Exception:
            return

        # Get installed and latest versions of the application by processing the command output.
        current_version = "-"
        last_version = "-"
        for line in pip_index_output:
            if "INSTALLED" in line:
                current_version = line.split("INSTALLED:")[1].strip()
            if "LATEST" in line:
                last_version = line.split("LATEST:")[1].strip()

        # Show an information label with a green background below the window headerbar if there is a newer version on PyPI.
        if current_version != last_version:
            # Show the notification information on the label by using "GLib.idle_add" in order to avoid
            # problems (bugs, data corruption, etc.) because of threading.
            GLib.idle_add(self.update_check_gui_notification)


    def update_check_gui_notification(self):
        """
        Show a notification label below the window titlebar if there is a newer version of the application on PyPI.
        """

        # Define label style
        css = b"label {background: rgba(24%,70%,45%,1.0);}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        # Generate a new label for the information and attach it to the grid at (0, 0) position.
        label_new_version_information = Gtk.Label(label=_tr("There is a newer version on PyPI."))
        label_new_version_information.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.main_grid.insert_row(0)
        self.main_grid.attach(label_new_version_information, 0, 0, 1, 1)
        label_new_version_information.set_visible(True)


    def main_gui_application_system_integration_func(self):
        """
        Copy files for GUI icons and application shortcut (.desktop file) in user folders if they are not copied before.
        These files are required if the application is installed as a Python package. Because these files are not copied
        # in system image folders in this situation. These images will not be recolorable if they are not in system or
        # user image folders. This function is stopped if environment type is Flatpak.
        """

        if Config.environment_type == "flatpak":
            return

        # Called for removing files.
        def remove_file(file):
            try:
                os.remove(file)
            except Exception:
                pass

        # Called for generating folders.
        def generate_folder(folder):
            try:
                os.makedirs(folder)
            except Exception:
                pass

        # Called for copying files.
        def copy_file(source, target):
            try:
                shutil.copy2(source, target)
            except Exception:
                pass

        # Get current directory (which code of this application is in) and current user home directory (files will be copied in).
        current_dir = os.path.dirname(os.path.realpath(__file__))
        current_user_homedir = os.environ.get('HOME')

        # Define folder list in the home directory for copying files.
        home_dir_folder_list = [current_user_homedir + "/.local/share/applications/",
                                current_user_homedir + "/.local/share/icons/hicolor/scalable/actions/",
                                current_user_homedir + "/.local/share/icons/hicolor/scalable/apps/"]

        # Generate folders to copy files in them if they are not generated before.
        for folder in home_dir_folder_list:
            if os.path.isdir(folder) == False:
                generate_folder(folder)

        # Get icon file paths in the home directory.
        icon_list_actions = [current_user_homedir + "/.local/share/icons/hicolor/scalable/actions/" + file for file in os.listdir(current_user_homedir + "/.local/share/icons/hicolor/scalable/actions/") if file.startswith("system-monitoring-center-")]
        icon_list_apps = [current_user_homedir + "/.local/share/icons/hicolor/scalable/apps/" + file for file in os.listdir(current_user_homedir + "/.local/share/icons/hicolor/scalable/apps/") if file.startswith("system-monitoring-center.svg")]
        icon_list_home = sorted(icon_list_actions + icon_list_apps)

        # Get icon file paths in the installation directory. These files are copied under this statement in order to avoid copying them if this is a system package which copies GUI images into "/usr/share/icons/..." folder during installation.
        try:
            icon_list_actions = [current_dir + "/../icons/hicolor/scalable/actions/" + file for file in os.listdir(current_dir + "/../icons/hicolor/scalable/actions/") if file.startswith("system-monitoring-center-")]
            icon_list_apps = [current_dir + "/../icons/hicolor/scalable/apps/" + file for file in os.listdir(current_dir + "/../icons/hicolor/scalable/apps/") if file.startswith("system-monitoring-center.svg")]
            icon_list_current = sorted(icon_list_actions + icon_list_apps)

            # Copy .desktop file if it is not copied before.
            if os.path.isfile(current_user_homedir + "/.local/share/applications/io.github.hakandundar34coding.system-monitoring-center.desktop") == False:
                # Try to remove if there is a broken symlink of the file (symlink was generated in previous versions of the application).
                remove_file(current_user_homedir + "/.local/share/applications/io.github.hakandundar34coding.system-monitoring-center.desktop")
                # Import module for copying files
                import shutil
                copy_file(current_dir + "/../integration/io.github.hakandundar34coding.system-monitoring-center.desktop", current_user_homedir + "/.local/share/applications/")
        except Exception:
            icon_list_current = []

        # Check if number of icon files are different. Remove the files in the home directory and copy the files in the installation directory if they are different.
        if len(icon_list_home) != len(icon_list_current):

            # Import module for copying files
            import shutil

            for file in icon_list_home:
                remove_file(file)

            for file in icon_list_current:
                copy_file(file, current_user_homedir + "/.local/share/icons/hicolor/scalable/" + file.split("/")[-2] + "/")


    def switch_to_default_tab(self):
        """
        Switches to default main tab and sub-tab on initial run.
        This function have to be run before "main_gui_tab_loop" function.
        """

        if Config.default_main_tab == 0:
             self.performance_tb.set_active(True)
        elif Config.default_main_tab == 1:
             self.processes_tb.set_active(True)
        elif Config.default_main_tab == 2:
             self.users_tb.set_active(True)
        elif Config.default_main_tab == 3:
             self.services_tb.set_active(True)
        elif Config.default_main_tab == 4:
             self.system_tb.set_active(True)

        if Config.performance_tab_default_sub_tab == 0:
             self.summary_tb.set_active(True)
        elif Config.performance_tab_default_sub_tab == 1:
             self.cpu_tb.set_active(True)
        elif Config.performance_tab_default_sub_tab == 2:
             self.memory_tb.set_active(True)
        elif Config.performance_tab_default_sub_tab == 3:
             self.disk_tb.set_active(True)
        elif Config.performance_tab_default_sub_tab == 4:
             self.network_tb.set_active(True)
        elif Config.performance_tab_default_sub_tab == 5:
             self.gpu_tb.set_active(True)
        elif Config.performance_tab_default_sub_tab == 6:
             self.sensors_tb.set_active(True)


    def main_gui_tab_loop(self, *args):
        """
        Called for running loop functions of opened tabs to get performance/usage data.
        "*args" is used in order to prevent warning and obtain a repeated function by using "GLib.timeout_source_new()".
        "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to change the update interval
        and run the loop again without waiting ending the previous update interval.
        """

        # Destroy GLib source for preventing it repeating the function.
        try:
            self.main_glib_source.destroy()
        # Prevent errors if this is first run of the function.
        except AttributeError:
            pass
        self.main_glib_source = GLib.timeout_source_new(Config.update_interval * 1000)

        Performance.performance_background_loop_func()

        if Config.performance_summary_on_the_headerbar == 1:
            GLib.idle_add(self.performance_summary_headerbar_loop)

        if Config.current_main_tab == 0:
            if Config.performance_tab_current_sub_tab == 0:
                GLib.idle_add(Summary.summary_loop_func)
            elif Config.performance_tab_current_sub_tab == 1:
                GLib.idle_add(Cpu.cpu_loop_func)
            elif Config.performance_tab_current_sub_tab == 2:
                GLib.idle_add(Memory.memory_loop_func)
            elif Config.performance_tab_current_sub_tab == 3:
                GLib.idle_add(Disk.disk_loop_func)
            elif Config.performance_tab_current_sub_tab == 4:
                GLib.idle_add(Network.network_loop_func)
            elif Config.performance_tab_current_sub_tab == 5:
                GLib.idle_add(Gpu.gpu_loop_func)
            elif Config.performance_tab_current_sub_tab == 6:
                GLib.idle_add(Sensors.sensors_loop_func)
        elif Config.current_main_tab == 1:
            GLib.idle_add(Processes.processes_loop_func)
        elif Config.current_main_tab == 2:
            GLib.idle_add(Users.users_loop_func)

        self.main_glib_source.set_callback(self.main_gui_tab_loop)
        # Attach GLib.Source to MainContext.
        # Therefore it will be part of the main loop until it is destroyed.
        # A function may be attached to the MainContext multiple times.
        self.main_glib_source.attach(GLib.MainContext.default())


    def performance_summary_headerbar_loop(self):
        """
        Loop function of performance summary on window headerbar.
        Update performance data on the headerbar.
        """

        selected_disk_number = Performance.selected_disk_number
        selected_network_card_number = Performance.selected_network_card_number
        self.ps_hb_cpu_da.queue_draw()
        self.ps_hb_ram_da.queue_draw()
        self.ps_hb_disk_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", Config.performance_disk_speed_bit, (Performance.disk_read_speed[selected_disk_number][-1] + Performance.disk_write_speed[selected_disk_number][-1]), Config.performance_disk_data_unit, 1)}/s')
        self.ps_hb_network_label.set_text(f'{Performance.performance_data_unit_converter_func("speed", Config.performance_network_speed_bit, (Performance.network_receive_speed[selected_network_card_number][-1] + Performance.network_send_speed[selected_network_card_number][-1]), Config.performance_network_data_unit, 1)}/s')


MainWindow = MainWindow()


import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('Gio', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, GLib, Gio, GObject, Pango

import os
import time
import subprocess
from datetime import datetime

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class Processes:

    def __init__(self):

        self.name = "Processes"

        self.tab_gui()

        # "0" value of "initial_already_run" variable means that initial function is not run before or
        # tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_grid = Common.tab_grid()

        self.tab_title_grid()

        self.tab_info_grid()

        self.gui_signals()

        self.right_click_menu()

        # Set initial value for process searching.
        self.process_search_type = "all"

        # Add PID column (1) to shown columns in order to prevent errors during process search if PID column is hidden in
        # previous versions (<=v2.10.0) of the application.
        treeview_columns_shown = Config.processes_treeview_columns_shown
        if 1 not in treeview_columns_shown:
            treeview_columns_shown.append(1)
        Config.processes_treeview_columns_shown = sorted(treeview_columns_shown)


        data_column_order = Config.processes_data_column_order
        if len(data_column_order) < 20:
            data_column_widths = Config.processes_data_column_widths
            Config.processes_data_column_order = data_column_order + [-1]
            Config.processes_data_column_widths = data_column_widths + [-1]


    def tab_title_grid(self):
        """
        Generate tab name label, searchentry.
        """

        # Grid (tab title)
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.tab_grid.attach(grid, 0, 0, 1, 1)

        # Label (Processes)
        label = Common.tab_title_label(_tr("Processes"))
        grid.attach(label, 0, 0, 1, 1)

        # Grid (search widgets)
        search_grid = Gtk.Grid()
        search_grid.set_column_spacing(3)
        search_grid.add_css_class("linked")
        search_grid.set_halign(Gtk.Align.CENTER)
        grid.attach(search_grid, 1, 0, 1, 1)

        # SearchEntry
        self.searchentry = Common.searchentry(self.on_searchentry_changed)
        search_grid.attach(self.searchentry, 0, 0, 1, 1)

        # MenuButton (search customization)
        self.search_customization_menubutton = Gtk.MenuButton()
        self.search_customization_menubutton.set_icon_name("edit-find-symbolic")
        self.search_customization_menubutton.set_halign(Gtk.Align.START)
        self.search_customization_menubutton.set_valign(Gtk.Align.CENTER)
        self.search_customization_menubutton.set_create_popup_func(self.search_customization_menu_gui)
        self.search_customization_menubutton.set_direction(Gtk.ArrowType.DOWN)
        search_grid.attach(self.search_customization_menubutton, 1, 0, 1, 1)


    def tab_info_grid(self):
        """
        Generate information GUI objects.
        """

        # ScrolledWindow
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.tab_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # TreeView
        self.treeview = Gtk.TreeView()
        self.treeview.set_activate_on_single_click(True)
        self.treeview.set_fixed_height_mode(True)
        self.treeview.set_headers_clickable(True)
        self.treeview.set_enable_search(True)
        self.treeview.set_search_column(2)
        self.treeview.set_tooltip_column(3)                                                       # "3" is used for process command line
        scrolledwindow.set_child(self.treeview)

        # TreeSelection
        self.selection = self.treeview.get_selection()
        self.selection.set_mode(Gtk.SelectionMode.MULTIPLE)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # Treeview signals
        self.treeview.connect("columns-changed", Common.on_columns_changed, self)

        # Treeview mouse events
        treeview_mouse_event = Gtk.GestureClick()
        treeview_mouse_event.connect("pressed", self.on_treeview_pressed)
        self.treeview.add_controller(treeview_mouse_event)

        treeview_mouse_event_right_click = Gtk.GestureClick()
        treeview_mouse_event_right_click.set_button(3)
        treeview_mouse_event_right_click.connect("released", self.on_treeview_released)
        self.treeview.add_controller(treeview_mouse_event_right_click)

        treeview_mouse_event_left_click = Gtk.GestureClick()
        treeview_mouse_event_left_click.set_button(1)
        treeview_mouse_event_left_click.connect("released", self.on_treeview_released_button1)
        self.treeview.add_controller(treeview_mouse_event_left_click)

        # TreeSelection events
        self.selection_changed_signal_handler = self.selection.connect("changed", self.treeview_selection_changed)

        # SeachEntry focus action and accelerator
        Common.searchentry_focus_action_and_accelerator(MainWindow)

        # Right click menu actions
        # "Pause Process" action
        action = Gio.SimpleAction.new("processes_pause_process", None)
        action.connect("activate", self.on_process_manage_items_clicked)
        MainWindow.main_window.add_action(action)

        # "Continue Process" action
        action = Gio.SimpleAction.new("processes_continue_process", None)
        action.connect("activate", self.on_process_manage_items_clicked)
        MainWindow.main_window.add_action(action)

        # "End Process" action
        action = Gio.SimpleAction.new("processes_end_process", None)
        action.connect("activate", self.on_process_manage_items_clicked)
        MainWindow.main_window.add_action(action)

        # "End Process Immediately" action
        action = Gio.SimpleAction.new("processes_end_process_immediately", None)
        action.connect("activate", self.on_process_manage_items_clicked)
        MainWindow.main_window.add_action(action)

        # Priority actions. One option have to be chosen for radiobuttons. It is chosen by using "GLib.Variant("s", "[action_name]")".
        self.priority_action = Gio.SimpleAction.new_stateful("processes_priority_group", GLib.VariantType.new("s"), GLib.Variant("s", "processes_priority_normal"))
        self.priority_action.connect("activate", self.on_change_priority_item_clicked)
        MainWindow.main_window.add_action(self.priority_action)

        # "Priority - Custom Value" action
        action = Gio.SimpleAction.new("processes_priority_custom_value", None)
        action.connect("activate", self.on_change_priority_item_clicked)
        MainWindow.main_window.add_action(action)

        # "Set CPU Affinity" action
        action = Gio.SimpleAction.new("processes_set_cpu_affinity", None)
        action.connect("activate", self.on_process_cpu_affinity_item_clicked)
        MainWindow.main_window.add_action(action)

        # "Details" action
        action = Gio.SimpleAction.new("processes_details", None)
        action.connect("activate", self.on_details_item_clicked)
        MainWindow.main_window.add_action(action)

        # Accelerators for right click menu actions
        application = MainWindow.main_window.get_application()
        application.set_accels_for_action("win.processes_pause_process", ["<Control>S"])
        application.set_accels_for_action("win.processes_continue_process", ["<Control>C"])
        application.set_accels_for_action("win.processes_end_process", ["<Control>E"])
        application.set_accels_for_action("win.processes_end_process_immediately", ["<Control>K"])
        application.set_accels_for_action("win.processes_set_cpu_affinity", ["<Control>R"])
        application.set_accels_for_action("win.processes_details", ["Return", "KP_Enter"])


    def right_click_menu(self):
        """
        Generate right click menu GUI.
        """

        # Menu models
        process_management_menu_section = Gio.Menu.new()
        process_management_menu_section.append(_tr("Pause Process"), "win.processes_pause_process")
        process_management_menu_section.append(_tr("Continue Process"), "win.processes_continue_process")
        process_management_menu_section.append(_tr("End Process"), "win.processes_end_process")
        process_management_menu_section.append(_tr("End Process Immediately"), "win.processes_end_process_immediately")
        process_management_menu_section_item = Gio.MenuItem.new()
        process_management_menu_section_item.set_section(process_management_menu_section)

        priority_options_submenu_section = Gio.Menu.new()
        priority_very_high_menu_item = Gio.MenuItem()
        priority_very_high_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_LABEL, GLib.Variant("s", _tr("Very High")))
        priority_very_high_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_ACTION, GLib.Variant("s", "win.processes_priority_group"))
        priority_very_high_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_TARGET, GLib.Variant("s", "processes_priority_very_high"))
        priority_options_submenu_section.append_item(priority_very_high_menu_item)
        priority_high_menu_item = Gio.MenuItem()
        priority_high_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_LABEL, GLib.Variant("s", _tr("High")))
        priority_high_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_ACTION, GLib.Variant("s", "win.processes_priority_group"))
        priority_high_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_TARGET, GLib.Variant("s", "processes_priority_high"))
        priority_options_submenu_section.append_item(priority_high_menu_item)
        priority_normal_menu_item = Gio.MenuItem()
        priority_normal_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_LABEL, GLib.Variant("s", _tr("Normal")))
        priority_normal_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_ACTION, GLib.Variant("s", "win.processes_priority_group"))
        priority_normal_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_TARGET, GLib.Variant("s", "processes_priority_normal"))
        priority_options_submenu_section.append_item(priority_normal_menu_item)
        priority_low_menu_item = Gio.MenuItem()
        priority_low_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_LABEL, GLib.Variant("s", _tr("Low")))
        priority_low_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_ACTION, GLib.Variant("s", "win.processes_priority_group"))
        priority_low_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_TARGET, GLib.Variant("s", "processes_priority_low"))
        priority_options_submenu_section.append_item(priority_low_menu_item)
        priority_very_low_menu_item = Gio.MenuItem()
        priority_very_low_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_LABEL, GLib.Variant("s", _tr("Very Low")))
        priority_very_low_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_ACTION, GLib.Variant("s", "win.processes_priority_group"))
        priority_very_low_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_TARGET, GLib.Variant("s", "processes_priority_very_low"))
        priority_options_submenu_section.append_item(priority_very_low_menu_item)
        priority_options_submenu_section_item = Gio.MenuItem.new()
        priority_options_submenu_section_item.set_section(priority_options_submenu_section)

        priority_custom_value_submenu_section = Gio.Menu.new()
        priority_custom_value_submenu_section.append(_tr("Custom Value..."), "win.processes_priority_custom_value")
        priority_custom_value_submenu_section_item = Gio.MenuItem.new()
        priority_custom_value_submenu_section_item.set_section(priority_custom_value_submenu_section)

        priority_submenu = Gio.Menu.new()
        priority_submenu.append_item(priority_options_submenu_section_item)
        priority_submenu.append_item(priority_custom_value_submenu_section_item)

        priority_menu_section = Gio.Menu.new()
        priority_menu_section.append_submenu(_tr("Change Priority"), priority_submenu)
        priority_menu_section_item = Gio.MenuItem.new()
        priority_menu_section_item.set_section(priority_menu_section)

        cpu_affinity_menu_section = Gio.Menu.new()
        cpu_affinity_menu_section.append(_tr("Set CPU Affinity"), "win.processes_set_cpu_affinity")
        cpu_affinity_menu_section_item = Gio.MenuItem.new()
        cpu_affinity_menu_section_item.set_section(cpu_affinity_menu_section)

        details_menu_section = Gio.Menu.new()
        details_menu_section.append(_tr("Details"), "win.processes_details")
        details_menu_section_item = Gio.MenuItem.new()
        details_menu_section_item.set_section(details_menu_section)

        right_click_menu_model = Gio.Menu.new()
        right_click_menu_model.append_item(process_management_menu_section_item)
        right_click_menu_model.append_item(priority_menu_section_item)
        right_click_menu_model.append_item(cpu_affinity_menu_section_item)
        right_click_menu_model.append_item(details_menu_section_item)

        # Popover menu
        self.right_click_menu_po = Gtk.PopoverMenu()
        self.right_click_menu_po.set_menu_model(right_click_menu_model)
        #self.right_click_menu_po.set_parent(self.treeview)
        self.right_click_menu_po.set_parent(MainWindow.main_window)
        self.right_click_menu_po.set_position(Gtk.PositionType.BOTTOM)
        self.right_click_menu_po.set_has_arrow(False)


    def search_customization_menu_gui(self, val=None):
        """
        Generate search customizations popover menu GUI.
        """

        # Prevent generating menu on every MenuButton click
        if hasattr(self, "search_menu_po") == True:
            return

        # Popover
        self.search_menu_po = Gtk.Popover()

        # Grid (main)
        main_grid = Common.menu_main_grid()
        self.search_menu_po.set_child(main_grid)

        # Label (Search:)
        label = Common.title_label(_tr("Search...").strip("...") + ":")
        main_grid.attach(label, 0, 0, 1, 1)

        # CheckButton (All)
        self.search_process_all_cb = Common.checkbutton(_tr("All"), None)
        main_grid.attach(self.search_process_all_cb, 0, 1, 1, 1)

        # CheckButton (Name)
        self.search_process_name_cb = Common.checkbutton(_tr("Name"), self.search_process_all_cb)
        main_grid.attach(self.search_process_name_cb, 0, 2, 1, 1)

        # CheckButton (Command Line)
        self.search_process_command_line_cb = Common.checkbutton(_tr("Command Line"), self.search_process_all_cb)
        main_grid.attach(self.search_process_command_line_cb, 0, 3, 1, 1)

        # CheckButton (PID)
        self.search_process_pid_cb = Common.checkbutton(_tr("PID"), self.search_process_all_cb)
        main_grid.attach(self.search_process_pid_cb, 0, 4, 1, 1)

        # Set Popover of MenuButton
        self.search_customization_menubutton.set_popover(self.search_menu_po)

        # Set GUI once.
        self.search_popover_set_gui()

        # Connect signals
        self.search_process_all_cb.connect("toggled", self.on_search_menu_cb_toggled)
        self.search_process_name_cb.connect("toggled", self.on_search_menu_cb_toggled)
        self.search_process_command_line_cb.connect("toggled", self.on_search_menu_cb_toggled)
        self.search_process_pid_cb.connect("toggled", self.on_search_menu_cb_toggled)


    def search_popover_set_gui(self):
        """
        Select the default search option checkbutton.
        """

        self.search_process_all_cb.set_active(True)


    def on_search_menu_cb_toggled(self, widget):
        """
        Search again if process search type (process name or command line) is changed.
        """

        if widget == self.search_process_all_cb:
            self.process_search_type = "all"
        elif widget == self.search_process_name_cb:
            self.process_search_type = "name"
        elif widget == self.search_process_command_line_cb:
            self.process_search_type = "command_line"
        elif widget == self.search_process_pid_cb:
            self.process_search_type = "pid"

        self.on_searchentry_changed(self.searchentry)


    def priority_custom_value_gui(self):
        """
        Generate process priority (nice) custom value window GUI.
        """

        # Window
        self.priority_custom_value_window = Gtk.Window()
        self.priority_custom_value_window.set_default_size(400, -1)
        self.priority_custom_value_window.set_title(_tr("Change Priority"))
        self.priority_custom_value_window.set_icon_name("system-monitoring-center")
        self.priority_custom_value_window.set_transient_for(MainWindow.main_window)
        self.priority_custom_value_window.set_resizable(False)
        self.priority_custom_value_window.set_modal(True)
        self.priority_custom_value_window.set_hide_on_close(True)

        # Main grid
        main_grid = Gtk.Grid.new()
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        main_grid.set_row_spacing(10)
        self.priority_custom_value_window.set_child(main_grid)

        # Label
        label = Gtk.Label()
        label.set_label(_tr("Change priority of these processes") + ":\n(" + _tr("Smaller value means higher process priority") + ")")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 0, 1, 1)

        # ScrolledWindow (for process name and PID Label)
        scrolledwindow = Common.window_main_scrolledwindow()
        scrolledwindow.set_size_request(-1, 150)
        main_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # Viewport (for process name and PID Label)
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Grid (for process name and PID Label)
        grid = Gtk.Grid.new()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        viewport.set_child(grid)

        # Label (process name and PID)
        self.priority_process_name_and_pid_label = Gtk.Label()
        self.priority_process_name_and_pid_label.set_selectable(True)
        self.priority_process_name_and_pid_label.set_label("--")
        self.priority_process_name_and_pid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.priority_process_name_and_pid_label.set_halign(Gtk.Align.START)
        grid.attach(self.priority_process_name_and_pid_label, 0, 0, 1, 1)

        # Adjustment (for scale)
        self.adjustment = Gtk.Adjustment()
        self.adjustment.set_step_increment(1.0)

        # Scale
        self.scale = Gtk.Scale(adjustment=self.adjustment)
        self.scale.set_draw_value(True)
        self.scale.set_digits(0)
        main_grid.attach(self.scale, 0, 2, 1, 1)

        # Show min and max values of the Scale
        self.scale.add_mark(-20, Gtk.PositionType.BOTTOM, "-20")
        self.scale.add_mark(19, Gtk.PositionType.BOTTOM, "19")

        # Grid (buttons)
        grid = Gtk.Grid.new()
        grid.set_column_homogeneous(True)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(50)
        main_grid.attach(grid, 0, 3, 1, 1)

        # Button (Cancel)
        self.priority_custom_value_cancel_button = Gtk.Button()
        self.priority_custom_value_cancel_button.set_label(_tr("Cancel"))
        grid.attach(self.priority_custom_value_cancel_button, 0, 0, 1, 1)

        # Button (Change Priority)
        self.priority_custom_value_change_priority_button = Gtk.Button()
        self.priority_custom_value_change_priority_button.set_label(_tr("Change Priority"))
        grid.attach(self.priority_custom_value_change_priority_button, 1, 0, 1, 1)

        # Signals (buttons)
        self.priority_custom_value_cancel_button.connect("clicked", self.on_priority_custom_value_window_buttons_clicked)
        self.priority_custom_value_change_priority_button.connect("clicked", self.on_priority_custom_value_window_buttons_clicked)


    def on_priority_custom_value_window_buttons_clicked(self, widget):
        """
        Close the process custom priority window or change process priority.
        """

        if widget == self.priority_custom_value_cancel_button:
            self.priority_custom_value_window.set_visible(False)

        if widget == self.priority_custom_value_change_priority_button:
            # Get new priority (nice value) of the process
            selected_process_nice = str(int(self.adjustment.get_value()))
            Libsysmon.change_process_priority(self.selected_process_pid_list, selected_process_nice)
            self.priority_custom_value_window.set_visible(False)


    def set_cpu_affinity_window_gui(self):
        """
        Generate process CPU affinity window GUI.
        """

        # Window
        self.cpu_affinity_window = Gtk.Window()
        self.cpu_affinity_window.set_default_size(400, -1)
        self.cpu_affinity_window.set_title(_tr("Set CPU Affinity"))
        self.cpu_affinity_window.set_icon_name("system-monitoring-center")
        self.cpu_affinity_window.set_transient_for(MainWindow.main_window)
        self.cpu_affinity_window.set_resizable(False)
        self.cpu_affinity_window.set_modal(True)
        self.cpu_affinity_window.set_hide_on_close(True)

        # Main grid
        main_grid = Gtk.Grid.new()
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        main_grid.set_row_spacing(10)
        self.cpu_affinity_window.set_child(main_grid)

        # Label
        label = Gtk.Label()
        label.set_label(_tr("Processes") + ":")
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 0, 1, 1)

        # ScrolledWindow (for process name and PID Label)
        scrolledwindow = Common.window_main_scrolledwindow()
        scrolledwindow.set_size_request(-1, 150)
        main_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # Viewport (for process name and PID Label)
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Grid (for process name and PID Label)
        grid = Gtk.Grid.new()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        viewport.set_child(grid)

        # Label (process name and PID)
        self.cpu_affinity_process_name_and_pid_label = Gtk.Label()
        self.cpu_affinity_process_name_and_pid_label.set_selectable(True)
        self.cpu_affinity_process_name_and_pid_label.set_label("--")
        self.cpu_affinity_process_name_and_pid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.cpu_affinity_process_name_and_pid_label.set_halign(Gtk.Align.START)
        grid.attach(self.cpu_affinity_process_name_and_pid_label, 0, 0, 1, 1)

        # ScrolledWindow (for CPU core CheckButtons)
        scrolledwindow = Common.window_main_scrolledwindow()
        scrolledwindow.set_size_request(-1, 150)
        main_grid.attach(scrolledwindow, 0, 2, 1, 1)

        # Viewport (for CPU core CheckButtons)
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Grid (for CPU core CheckButtons)
        grid = Gtk.Grid.new()
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        viewport.set_child(grid)

        self.cpu_affinity_select_all_button = Gtk.Button()
        self.cpu_affinity_select_all_button.set_label(_tr("Select All"))
        self.cpu_affinity_select_all_button.set_halign(Gtk.Align.CENTER)
        grid.attach(self.cpu_affinity_select_all_button, 0, 0, 1, 1)

        self.cpu_affinity_select_none_button = Gtk.Button()
        self.cpu_affinity_select_none_button.set_label(_tr("Select None"))
        self.cpu_affinity_select_none_button.set_halign(Gtk.Align.CENTER)
        grid.attach(self.cpu_affinity_select_none_button, 1, 0, 1, 1)

        number_of_all_logical_cores = Libsysmon.get_number_of_all_logical_cores()
        for i in range(number_of_all_logical_cores):
            checkbutton = Common.checkbutton("cpu" + str(i), None)
            grid.attach(checkbutton, 0, i+1, 1, 1)
            checkbutton.connect("toggled", self.on_cpu_affinity_cores_checkbutton_clicked)

        # Grid (buttons)
        grid = Gtk.Grid.new()
        grid.set_column_homogeneous(True)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_column_spacing(50)
        main_grid.attach(grid, 0, 3, 1, 1)

        # Button (Cancel)
        self.cpu_affinity_cancel_button = Gtk.Button()
        self.cpu_affinity_cancel_button.set_label(_tr("Cancel"))
        grid.attach(self.cpu_affinity_cancel_button, 0, 0, 1, 1)

        # Button (Change Priority)
        self.cpu_affinity_set_cpu_affinity_button = Gtk.Button()
        self.cpu_affinity_set_cpu_affinity_button.set_label(_tr("Set CPU Affinity"))
        grid.attach(self.cpu_affinity_set_cpu_affinity_button, 1, 0, 1, 1)

        # Signals (buttons)
        self.cpu_affinity_select_all_button.connect("clicked", self.on_cpu_affinity_select_all_none_buttons_clicked)
        self.cpu_affinity_select_none_button.connect("clicked", self.on_cpu_affinity_select_all_none_buttons_clicked)
        self.cpu_affinity_cancel_button.connect("clicked", self.on_cpu_affinity_window_buttons_clicked)
        self.cpu_affinity_set_cpu_affinity_button.connect("clicked", self.on_cpu_affinity_window_buttons_clicked)


    def on_cpu_affinity_select_all_none_buttons_clicked(self, widget):
        """
        Select all/none of the CPU cores for CPU affinity.
        """

        number_of_all_logical_cores = Libsysmon.get_number_of_all_logical_cores()
        parent_grid = self.cpu_affinity_select_all_button.get_parent()

        if widget == self.cpu_affinity_select_all_button:
            for i in range(number_of_all_logical_cores):
                checkbutton = parent_grid.get_child_at(0, i+1)
                checkbutton.set_active(True)
            self.cpu_affinity_set_cpu_affinity_button.set_sensitive(True)

        elif widget == self.cpu_affinity_select_none_button:
            for i in range(number_of_all_logical_cores):
                checkbutton = parent_grid.get_child_at(0, i+1)
                checkbutton.set_active(False)
            self.cpu_affinity_set_cpu_affinity_button.set_sensitive(False)


    def on_cpu_affinity_cores_checkbutton_clicked(self, widget):
        """
        Set sensitive/insensitive "Set CPU Affinity" button if any/none CPU cores are selected.
        """

        number_of_all_logical_cores = Libsysmon.get_number_of_all_logical_cores()
        parent_grid = self.cpu_affinity_select_all_button.get_parent()

        checkbutton_active_list = []
        for i in range(number_of_all_logical_cores):
            checkbutton = parent_grid.get_child_at(0, i+1)
            checkbutton_active_list.append(checkbutton.get_active())

        if list(set(checkbutton_active_list)) == [False]:
            self.cpu_affinity_set_cpu_affinity_button.set_sensitive(False)
        else:
            self.cpu_affinity_set_cpu_affinity_button.set_sensitive(True)


    def on_cpu_affinity_window_buttons_clicked(self, widget):
        """
        Close the process CPU affinity window or change CPU affinity.
        """

        if widget == self.cpu_affinity_cancel_button:
            self.cpu_affinity_window.set_visible(False)

        if widget == self.cpu_affinity_set_cpu_affinity_button:
            number_of_all_logical_cores = Libsysmon.get_number_of_all_logical_cores()
            parent_grid = self.cpu_affinity_select_all_button.get_parent()

            cpu_affinity_core_list = []
            for i in range(number_of_all_logical_cores):
                checkbutton = parent_grid.get_child_at(0, i+1)
                if checkbutton.get_active() == True:
                    cpu_affinity_core_list.append(i)

            Libsysmon.set_process_cpu_affinity(self.selected_process_pid_list, cpu_affinity_core_list)
            self.cpu_affinity_window.set_visible(False)


    def on_process_manage_items_clicked(self, action, parameter):
        """
        Pause, continue, end, end immediately processes.
        """

        # Stop running the function if process managing keyboard shortcuts are pressed or
        # right clicked on column titles without selecting a process.
        if len(self.selected_process_pid_list) == 0:
            return

        # Stop running the function if the action is called by using keyboard shortcuts when another tab is opened.
        # Because keyboard shortcuts are defined for window instead of treeview for a simpler code.
        if Config.current_main_tab != 1:
            return

        # Get right clicked process names.
        selected_process_name_list = []
        for selected_process_pid in self.selected_process_pid_list:
            selected_process_name = self.tab_data_rows[self.pid_list.index(selected_process_pid)][2]
            selected_process_name_list.append(selected_process_name)

        if action.get_name() == "processes_pause_process":
            manage_option = "pause_process"
            process_dialog_message = _tr("Do you want to pause these processes?")
        elif action.get_name() == "processes_continue_process":
            manage_option = "continue_process"
        elif action.get_name() == "processes_end_process":
            manage_option = "end_process"
            process_dialog_message = _tr("Do you want to end these processes?")
        elif action.get_name() == "processes_end_process_immediately":
            manage_option = "end_process_immediately"
            process_dialog_message = _tr("Do you want to end these processes immediately?")

        if action.get_name() in ["processes_continue_process"]:
            Libsysmon.manage_process(self.selected_process_pid_list, manage_option)

        if action.get_name() in ["processes_pause_process", "processes_end_process", "processes_end_process_immediately"]:
            # Show warning dialog if process is tried to be ended.
            if Config.warn_before_stopping_processes == 1:
                selected_process_pid_name_text = ""
                for i, selected_process_pid in enumerate(self.selected_process_pid_list):
                    if selected_process_pid_name_text != "":
                        selected_process_pid_name_text = selected_process_pid_name_text + "\n"
                    selected_process_pid_name_text = selected_process_pid_name_text + f'{selected_process_name_list[i]} - (PID: {selected_process_pid})'
                messagedialog = Gtk.MessageDialog(transient_for=MainWindow.main_window,
                                                  modal=True,
                                                  title="",
                                                  message_type=Gtk.MessageType.WARNING,
                                                  buttons=Gtk.ButtonsType.YES_NO,
                                                  text=process_dialog_message,
                                                  secondary_text="")

                # Get Box widget of the MessageDialog for appending custom content (ScrolledWindow, etc.).
                message_area = messagedialog.get_message_area()

                # ScrolledWindow (for process name and PID Label)
                scrolledwindow = Common.window_main_scrolledwindow()
                scrolledwindow.set_size_request(-1, 150)
                message_area.append(scrolledwindow)

                # Viewport (for process name and PID Label)
                viewport = Gtk.Viewport()
                scrolledwindow.set_child(viewport)

                # Grid (for process name and PID Label)
                grid = Gtk.Grid.new()
                grid.set_margin_top(10)
                grid.set_margin_bottom(10)
                grid.set_margin_start(10)
                grid.set_margin_end(10)
                viewport.set_child(grid)

                # Label (process name and PID)
                process_manage_process_name_and_pid_label = Gtk.Label()
                process_manage_process_name_and_pid_label.set_selectable(True)
                process_manage_process_name_and_pid_label.set_label("--")
                process_manage_process_name_and_pid_label.set_ellipsize(Pango.EllipsizeMode.END)
                process_manage_process_name_and_pid_label.set_halign(Gtk.Align.START)
                grid.attach(process_manage_process_name_and_pid_label, 0, 0, 1, 1)

                process_manage_process_name_and_pid_label.set_label(selected_process_pid_name_text)

                messagedialog.connect("response", self.on_messagedialog_response, self.selected_process_pid_list, manage_option)
                messagedialog.present()


    def on_messagedialog_response(self, widget, response, process_pid_list, manage_option):
        """
        End process if "YES" button on the dialog is clicked.
        """

        if response == Gtk.ResponseType.YES:
            Libsysmon.manage_process(process_pid_list, manage_option)

        messagedialog = widget
        messagedialog.set_visible(False)


    def set_priority_menu_option(self):
        """
        Set process priority (nice) option on the right click menu.
        """

        # Unselect all priority option RadioButtons if multiple processes are selected.
        if len(self.selected_process_pid_list) > 1:
            self.priority_action.set_state(GLib.Variant("s", ""))
            return

        # Get process current priority value if one process is selected.
        if len(self.selected_process_pid_list) == 1:
            selected_process_nice = Libsysmon.get_process_priority(str(self.selected_process_pid_list[0]))
            if selected_process_nice == "-":
                return
        else:
            selected_process_nice = 0

        # Set menu GUI
        if selected_process_nice <= -11 and selected_process_nice >= -20:
            self.priority_action.set_state(GLib.Variant("s", "processes_priority_very_high"))
        if selected_process_nice < 0 and selected_process_nice > -11:
            self.priority_action.set_state(GLib.Variant("s", "processes_priority_high"))
        if selected_process_nice == 0:
            self.priority_action.set_state(GLib.Variant("s", "processes_priority_normal"))
        if selected_process_nice < 11 and selected_process_nice > 0:
            self.priority_action.set_state(GLib.Variant("s", "processes_priority_low"))
        if selected_process_nice <= 19 and selected_process_nice >= 11:
            self.priority_action.set_state(GLib.Variant("s", "processes_priority_very_low"))


    def on_change_priority_item_clicked(self, action, parameter):
        """
        Change process priority (nice).
        """

        # Stop running the function if the action is called by using keyboard shortcuts when another tab is opened.
        # Because keyboard shortcuts are defined for window instead of treeview for a simpler code.
        if Config.current_main_tab != 1:
            return

        if action.get_name() == "processes_priority_group":

            if parameter == GLib.Variant("s", "processes_priority_very_high"):
                action.set_state(GLib.Variant("s", "processes_priority_very_high"))
                priority_option = "priority_very_high"
            elif parameter == GLib.Variant("s", "processes_priority_high"):
                action.set_state(GLib.Variant("s", "processes_priority_high"))
                priority_option = "priority_high"
            elif parameter == GLib.Variant("s", "processes_priority_normal"):
                action.set_state(GLib.Variant("s", "processes_priority_normal"))
                priority_option = "priority_normal"
            elif parameter == GLib.Variant("s", "processes_priority_low"):
                action.set_state(GLib.Variant("s", "processes_priority_low"))
                priority_option = "priority_low"
            elif parameter == GLib.Variant("s", "processes_priority_very_low"):
                action.set_state(GLib.Variant("s", "processes_priority_very_low"))
                priority_option = "priority_very_low"

            Libsysmon.change_process_priority(self.selected_process_pid_list, priority_option)

        if action.get_name() == "processes_priority_custom_value":

            selected_process_name_list = Common.get_selected_process_names(self)

            # Get process current priority value if one process is selected.
            if len(self.selected_process_pid_list) == 1:
                selected_process_nice = Libsysmon.get_process_priority(str(self.selected_process_pid_list[0]))
                if selected_process_nice == "-":
                    return
            else:
                selected_process_nice = 0

            # Show process custom priority window.
            try:
                self.priority_custom_value_window.present()
            except AttributeError:
                # Avoid generating menu multiple times on every click.
                self.priority_custom_value_gui()
                self.priority_custom_value_window.present()

            # Set adjustment widget by using process priority (nice value).
            self.adjustment.configure(selected_process_nice, -20, 19, 1, 0, 0)

            # Show process name and PID on a label.
            selected_process_name_pid_text = Common.get_process_name_pid_list_text(self, selected_process_name_list)
            self.priority_process_name_and_pid_label.set_label(selected_process_name_pid_text)


    def on_process_cpu_affinity_item_clicked(self, action, parameter):
        """
        Show process CPU affinity window.
        """

        if Config.current_main_tab != 1:
            return

        selected_process_name_list = Common.get_selected_process_names(self)

        # Get process current CPU affinity value if one process is selected.
        if len(self.selected_process_pid_list) == 1:
            selected_process_cpu_affinity = Libsysmon.get_process_cpu_affinity(str(self.selected_process_pid_list[0]))
            if selected_process_cpu_affinity == "-":
                return
        else:
            selected_process_cpu_affinity = "-"

        # Show process CPU affinity window.
        try:
            self.cpu_affinity_window.present()
        except AttributeError:
            # Avoid generating menu multiple times on every click.
            self.set_cpu_affinity_window_gui()
            self.cpu_affinity_window.present()

        # Set CPU core CheckButtons
        number_of_all_logical_cores = Libsysmon.get_number_of_all_logical_cores()
        parent_grid = self.cpu_affinity_select_all_button.get_parent()
        if selected_process_cpu_affinity == "-":
            for i in range(number_of_all_logical_cores):
                checkbutton = parent_grid.get_child_at(0, i+1)
                #checkbutton.set_inconsistent(True)
                checkbutton.set_active(False)
                self.cpu_affinity_set_cpu_affinity_button.set_sensitive(False)
        else:
            for i in range(number_of_all_logical_cores):
                checkbutton = parent_grid.get_child_at(0, i+1)
                if i in selected_process_cpu_affinity:
                    checkbutton.set_active(True)
                else:
                    checkbutton.set_active(False)
            self.cpu_affinity_set_cpu_affinity_button.set_sensitive(True)

        # Show process name and PID on a label.
        selected_process_name_pid_text = Common.get_process_name_pid_list_text(self, selected_process_name_list)
        self.cpu_affinity_process_name_and_pid_label.set_label(selected_process_name_pid_text)


    def on_details_item_clicked(self, action, parameter):
        """
        Show process details window.
        """

        # Stop running the function if the action is called by using keyboard shortcuts when another tab is opened.
        # Because keyboard shortcuts are defined for window instead of treeview for a simpler code.
        if Config.current_main_tab != 1:
            return

        from . import ProcessesDetails
        ProcessesDetails.process_details_show_process_details()


    def on_searchentry_changed(self, widget):
        """
        Called by searchentry when text is changed.
        """

        process_search_text = self.searchentry.get_text().lower()

        treeview = self.treeview
        sort_model = treeview.get_model()
        filter_model = sort_model.get_model()
        treestore = filter_model.get_model()

        pid_list = self.pid_list

        global cmdline_list

        # Get PID, iter, shown, expanded information from sort model before changing search text.
        pid_piter_sort_model_before_dict = self.get_sort_model_piter_information(treeview, sort_model)

        # Show/hide iters (rows) by using search text.
        for piter in self.piter_list:
            if piter == None:
                continue
            if self.process_search_type == "all":
                process_name_in_model = treestore.get_value(piter, self.filter_column)
                process_pid_in_model = treestore.get_value(piter, 4)
                process_command_line_in_model = cmdline_list[pid_list.index(process_pid_in_model)]
                process_data_text_in_model = f'{process_name_in_model}{process_pid_in_model}{process_command_line_in_model}'
            elif self.process_search_type == "name":
                process_data_text_in_model = treestore.get_value(piter, self.filter_column)
            elif self.process_search_type == "command_line":
                process_pid_in_model = treestore.get_value(piter, 4)
                process_data_text_in_model = cmdline_list[pid_list.index(process_pid_in_model)]
            elif self.process_search_type == "pid":
                process_data_text_in_model = f'{treestore.get_value(piter, 4)}'

            if process_search_text in process_data_text_in_model.lower():
                pid = treestore.get_value(piter, 4)
                treestore.set_value(piter, 0, True)
                piter = treestore.iter_parent(piter)
            else:
                treestore.set_value(piter, 0, False)

        # Get PID, iter, shown, expanded information from sort model after changing search text.
        pid_piter_sort_model_after_dict = self.get_sort_model_piter_information(treeview, sort_model)

        # Expand rows after search text change if if is expanded before or it is made shown again.
        for pid in pid_piter_sort_model_after_dict:
            piter = pid_piter_sort_model_after_dict[pid]["piter"]
            if pid not in pid_piter_sort_model_before_dict:
                treeview.expand_row(sort_model.get_path(piter), False)
                continue
            if pid_piter_sort_model_before_dict[pid]["expanded"] == True:
                treeview.expand_row(sort_model.get_path(piter), False)


    def get_sort_model_piter_information(self, treeview, sort_model):
        """
        Get PID, iter, shown, expanded information from treeview sort model.
        """

        pid_piter_sort_model_dict = {}
        # Get PID, iter, shown, expanded information for for root rows.
        list_current = []
        for i, row in enumerate(sort_model):
            piter = sort_model.get_iter(i)
            pid = sort_model.get_value(piter, 4)
            sub_dict = {}
            sub_dict["piter"] = piter
            sub_dict["shown"] = sort_model.get_value(piter, 0)
            sub_dict["expanded"] = treeview.row_expanded(sort_model.get_path(piter))
            pid_piter_sort_model_dict[pid] = sub_dict
            list_current.append(piter)
        list_current = list(list_current)
        list_next = []
        # Get PID, iter, shown, expanded information for for children rows.
        while list_current != []:
            for piter in list_current:
                children_count = sort_model.iter_n_children(piter)
                for i in range(children_count):
                    piter_child = sort_model.iter_nth_child(piter, i)
                    if piter_child == None:
                        continue
                    pid = sort_model.get_value(piter_child, 4)
                    sub_dict = {}
                    sub_dict["piter"] = piter_child
                    sub_dict["shown"] = sort_model.get_value(piter_child, 0)
                    sub_dict["expanded"] = treeview.row_expanded(sort_model.get_path(piter_child))
                    pid_piter_sort_model_dict[pid] = sub_dict
                    list_next.append(piter_child)
            list_current = list(list_next)
            list_next = []

        return pid_piter_sort_model_dict


    def treeview_selection_changed(self, widget):
        """
        Get selected rows.
        """

        try:
            self.path_list_prev = list(self.path_list)
        except AttributeError:
            pass

        model, self.path_list = self.selection.get_selected_rows()
        self.get_pids_from_paths()

        self.multiple_process_information_summation_gui()


    def multiple_process_information_summation_gui(self):
        """
        Add/Remove Grid and labels for showing process information (CPU, memory, disk read speed, etc.)
        if multiple processes are selected.
        """

        # Remove Grid and labels if selection is changed.
        try:
            if self.selected_process_pid_list != self.selected_process_pid_list_prev:
                if self.tab_grid.get_child_at(0, 2) != None:
                    self.tab_grid.remove(self.multiple_process_information_grid)
                self.dynamic_information_column_label_dict = {}
        except AttributeError:
            self.dynamic_information_column_label_dict = {}

        # Remove Grid and labels if selection is not changed by user but signal is called for Selection.
        # For example, a search may be performed.
        if self.tab_grid.get_child_at(0, 2) != None:
            self.tab_grid.remove(self.multiple_process_information_grid)

        self.selected_process_pid_list_prev = self.selected_process_pid_list

        if Config.show_multiple_processes_summation != 1:
            return

        # Prevent adding widgets if multiple processes are not selected.
        selected_process_count = len(self.selected_process_pid_list)
        if selected_process_count < 2:
            return

        # Grid
        self.multiple_process_information_grid = Gtk.Grid()
        self.multiple_process_information_grid.set_row_homogeneous(True)
        self.multiple_process_information_grid.set_column_spacing(20)
        self.tab_grid.attach(self.multiple_process_information_grid, 0, 2, 1, 1)

        summable_column_number = 0

        # Label (Processes ([COUNT]))
        static_information_label = Gtk.Label()
        self.multiple_process_information_grid.attach(static_information_label, summable_column_number, 0, 1, 1)
        static_information_label.set_margin_end(20)
        static_information_label.set_text(_tr("Processes") + ": " + str(selected_process_count))

        # Label (Total:)
        dynamic_information_label = Gtk.Label()
        self.multiple_process_information_grid.attach(dynamic_information_label, summable_column_number, 1, 1, 1)
        dynamic_information_label.set_halign(Gtk.Align.END)
        dynamic_information_label.set_margin_end(20)
        dynamic_information_label.set_text(_tr("Total") + ":")

        # Labels (Column titles and column value summations)
        for column_shown in self.treeview_columns_shown:
            column_title = self.row_data_list[column_shown][1]
            if column_title not in self.summable_column_dict:
                continue

            summable_column_number = summable_column_number + 1

            # Label ([COLUMN TITLE])
            static_information_label = Common.static_information_label(column_title)
            self.multiple_process_information_grid.attach(static_information_label, summable_column_number, 0, 1, 1)

            # Label ([COLUMN VALUE SUMMATION])
            dynamic_information_label = Common.static_information_label("--")
            self.multiple_process_information_grid.attach(dynamic_information_label, summable_column_number, 1, 1, 1)
            self.dynamic_information_column_label_sub_dict = {"column_title": column_title, "label": dynamic_information_label}
            self.dynamic_information_column_label_dict[column_shown] = self.dynamic_information_column_label_sub_dict

        self.multiple_process_information_summation_set_values()


    def multiple_process_information_summation_set_values(self):
        """
        Update labels for showing process information (CPU, memory, disk read speed, etc.)
        if multiple processes are selected.
        """

        global processes_cpu_precision, processes_cpu_divide_by_core
        global processes_memory_data_precision, processes_memory_data_unit
        global processes_disk_data_precision, processes_disk_data_unit, processes_disk_speed_bit

        for column_shown in sorted(list(self.dynamic_information_column_label_dict.keys())):
            column_title = self.dynamic_information_column_label_dict[column_shown]["column_title"]
            data_name = self.summable_column_dict[column_title]
            label =  self.dynamic_information_column_label_dict[column_shown]["label"]

            # Get process information summation
            process_data_summation = 0
            for pid in self.selected_process_pid_list:
                row_data_dict = self.rows_data_dict[pid]
                process_data = row_data_dict[data_name]
                process_data_summation = process_data_summation + process_data

            # Set label values
            if data_name in ["cpu_usage"]:
                label.set_text(f'{process_data_summation:.{processes_cpu_precision}f} %')
            elif data_name in ["memory_rss", "memory_vms", "memory_shared", "read_data", "written_data", "memory"]:
                label.set_text(f'{Libsysmon.data_unit_converter("data", "none", process_data_summation, processes_memory_data_unit, processes_memory_data_precision)}')
            elif data_name in ["read_speed", "write_speed"]:
                label.set_text(f'{Libsysmon.data_unit_converter("speed", processes_disk_speed_bit, process_data_summation, processes_disk_data_unit, processes_disk_data_precision)}/s')


    def on_treeview_pressed(self, event, count, x, y):
        """
        Mouse single right click and double left click events (button press).
        Details window is shown when double clicked.
        """

        # Show details window if double clicked on a row
        if int(event.get_button()) == 1 and int(count) == 2:
            from . import ProcessesDetails
            ProcessesDetails.process_details_show_process_details()


    def get_pids_from_paths(self):
        """
        Get process PIDs from selected treeview paths.
        """

        model = self.treeview.get_model()

        treeiter_list = []
        for path in self.path_list:
            treeiter = model.get_iter(path)
            treeiter_list.append(treeiter)

        self.selected_process_pid_list = []
        for treeiter in treeiter_list:
            if treeiter == None:
                continue
            try:
                selected_process_pid = model[treeiter][:][4]
            # It gives error such as "ValueError: [True, 'system-monitoring-center-process-symbolic', 'python3', 2411, 'user', 'Running', 1.6633495783351964, 98824192, 548507648, 45764608, 0, 16384, 0, 5461, 0, 4, 1727, 1000, 1000, '/usr/bin/python3.9'] is not in list" rarely.
            # It is handled in this situation.
            except ValueError:
                continue
            self.selected_process_pid_list.append(selected_process_pid)


    def on_treeview_released(self, event, count, x, y):
        """
        Mouse single right click event (button release).
        Right click menu is opened.
        """

        # Remember and reselect previous row selection if right clicked on selection of multiple rows.
        # Otherwise, TreeSelection selects only right clicked row.
        # Also block "changed" signal of TreeSelection for preventing calling selection functions multiple times.
        with self.selection.handler_block(self.selection_changed_signal_handler):
            if hasattr(Processes, "path_list_prev") and \
                self.path_list != self.path_list_prev and \
                len(self.path_list_prev) > 1 and \
                len(self.path_list) == 1 and \
                self.path_list[0] in self.path_list_prev:
                    for path in self.path_list_prev:
                        self.selection.select_path(path)
                    self.path_list = list(self.path_list_prev)
                    self.get_pids_from_paths()

        # Show multiple process summmation GUI again after reselecting (remembering) of multiple processes.
        self.multiple_process_information_summation_gui()

        # Show right click menu if right clicked on a row
        if int(event.get_button()) == 3:

            # Stop running the function if process managing keyboard shortcuts are pressed or
            # right clicked on column titles without selecting a process.
            if len(self.selected_process_pid_list) == 0:
                return

            rectangle = Gdk.Rectangle()
            rectangle.x = int(x)
            rectangle.y = int(y)
            rectangle.width = 1
            rectangle.height = 1
            # Convert teeview coordinates to window coordinates. Because popovermenu is set for window instead of treeview.
            treeview_x_coord, treeview_y_coord = self.treeview.translate_coordinates(MainWindow.main_window,0,0)
            rectangle.x = rectangle.x + treeview_x_coord
            rectangle.y = rectangle.y + treeview_y_coord

            # New coordinates have to be set for popovermenu on every popup.
            self.right_click_menu_po.set_pointing_to(rectangle)
            self.right_click_menu_po.popup()
            self.set_priority_menu_option()


    def on_treeview_released_button1(self, event, count, x, y):
        """
        Mouse single left click event (button release).
        """
        pass


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        # data list explanation:
        # row_data_list = [
        #                 [treeview column number, treeview column title, internal column count, cell renderer count, treeview column sort column id, [data type 1, data type 2, ...], [cell renderer type 1, cell renderer type 2, ...], [cell attribute 1, cell attribute 2, ...], [cell renderer data 1, cell renderer data 2, ...], [cell left/right alignment 1, cell left/right alignment 2, ...], [set expand 1 {if cell will allocate unused space} cell expand 2, ...], [cell function 1, cell function 2, ...]]
        #                 .
        #                 .
        #                 ]
        self.row_data_list = [
                             [0, _tr('Name'), 3, 2, 3, [bool, str, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'icon_name', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
                             [1, _tr('PID'), 2, 1, 2, [str, int], ['internal_column', 'CellRendererText'], ['no_cell_attribute', 'text'], [0, 1], ['no_cell_alignment', 1.0], [False, False], ['no_cell_function', 'no_cell_function']],
                             [2, _tr('User'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                             [3, _tr('Status'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                             [4, _tr('CPU'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_cpu_usage_percent]],
                             [5, _tr('Memory (RSS)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_memory_rss]],
                             [6, _tr('Memory (VMS)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_memory_vms]],
                             [7, _tr('Memory (Shared)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_memory_shared]],
                             [8, _tr('Read Data'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_read_data]],
                             [9, _tr('Written Data'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_write_data]],
                             [10, _tr('Read Speed'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_read_speed]],
                             [11, _tr('Write Speed'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_disk_write_speed]],
                             [12, _tr('Priority'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                             [13, _tr('Threads'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                             [14, _tr('PPID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                             [15, _tr('UID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                             [16, _tr('GID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                             [17, _tr('Start Time'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [0.0], [False], [cell_data_function_start_time]],
                             [18, _tr('Command Line'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                             [19, _tr('CPU Time'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_cpu_time]],
                             [20, _tr('Memory'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_memory]],
                             [21, _tr('CPU') + " - " + _tr('Recursive'), 1, 1, 1, [float], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_cpu_usage_percent_recursive]],
                             [22, _tr('Memory (RSS)') + " - " + _tr('Recursive'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_memory_rss_recursive]],
                             [23, _tr('Memory') + " - " + _tr('Recursive'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_memory_recursive]]
                             ]

        self.summable_column_dict = {_tr('CPU'): "cpu_usage", _tr('Memory (RSS)'): "memory_rss", _tr('Memory (VMS)'): "memory_vms",
                                     _tr('Memory (Shared)'): "memory_shared", _tr('Read Data'): "read_data",
                                     _tr('Written Data'): "written_data", _tr('Read Speed'): "read_speed",
                                     _tr('Write Speed'): "write_speed", _tr('Memory'): "memory"}

        # Define data unit conversion function objects in for lower CPU usage.
        global data_unit_converter
        data_unit_converter = Libsysmon.data_unit_converter

        self.tab_data_rows_prev = []
        self.pid_list_prev = []
        self.piter_list = []
        self.show_processes_as_tree_prev = Config.show_processes_as_tree
        self.treeview_columns_shown_prev = []
        self.data_row_sorting_column_prev = ""
        self.data_row_sorting_order_prev = ""
        self.data_column_order_prev = []
        self.data_column_widths_prev = []
        self.rows_data_dict_prev = {}

        global number_of_clock_ticks, application_image_dict
        number_of_clock_ticks = Libsysmon.number_of_clock_ticks
        self.system_boot_time = Libsysmon.get_system_boot_time()
        self.username_uid_dict = Libsysmon.get_username_uid_dict()
        application_image_dict = Libsysmon.get_application_name_image_dict()

        # Define process status text list for translation
        process_status_list = [_tr("Running"), _tr("Sleeping"), _tr("Waiting"), _tr("Idle"), _tr("Zombie"), _tr("Stopped")]

        # Search filter is "Process Name". "-1" is used because "row_data_list" has internal column count and
        # it has to be converted to Python index. For example, if there are 3 internal columns but index is 2 for the last
        # internal column number for the relevant treeview column.
        self.filter_column = self.row_data_list[0][2] - 1

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        # Run initial function of the module if this is the first loop of the module.
        if self.initial_already_run == 0:
            self.initial_func()

        update_interval = Config.update_interval

        # Get configrations one time per floop instead of getting them multiple times (hundreds of times for many of them) in every loop which causes high CPU usage.
        global processes_cpu_precision, processes_cpu_divide_by_core
        global processes_memory_data_precision, processes_memory_data_unit
        global processes_disk_data_precision, processes_disk_data_unit, processes_disk_speed_bit
        processes_cpu_precision = Config.processes_cpu_precision
        processes_cpu_divide_by_core = Config.processes_cpu_divide_by_core
        processes_memory_data_precision = Config.processes_memory_data_precision
        processes_memory_data_unit = Config.processes_memory_data_unit
        processes_disk_data_precision = Config.processes_disk_data_precision
        processes_disk_data_unit = Config.processes_disk_data_unit
        processes_disk_speed_bit = Config.processes_disk_speed_bit

        # Define global variables and get treeview columns, sort column/order, column widths, etc.
        self.treeview_columns_shown = Config.processes_treeview_columns_shown
        self.data_row_sorting_column = Config.processes_data_row_sorting_column
        self.data_row_sorting_order = Config.processes_data_row_sorting_order
        self.data_column_order = Config.processes_data_column_order
        self.data_column_widths = Config.processes_data_column_widths
        self.show_processes_of_all_users = Config.show_processes_of_all_users
        self.show_processes_as_tree = Config.show_processes_as_tree
        # For obtaining lower CPU usage
        treeview_columns_shown = self.treeview_columns_shown
        treeview_columns_shown = set(treeview_columns_shown)

        # Define lists for appending some performance data for calculating max values to determine cell background color.
        # "0" values are added for preventing errors if the lists are empty.
        cpu_usage_list = [0]
        memory_rss_list = [0]
        memory_vms_list = [0]
        memory_shared_list = [0]
        memory_list = [0]
        disk_read_data_list = [0]
        disk_write_data_list = [0]
        disk_read_speed_list = [0]
        disk_write_speed_list = [0]
        cpu_usage_recursive_list = [0]
        memory_rss_recursive_list = [0]
        memory_recursive_list = [0]

        # Get process information
        global cmdline_list, application_image_dict
        process_list = []
        if self.show_processes_of_all_users == 1:
            processes_of_user = "all"
        else:
            processes_of_user = "current"
        if processes_cpu_divide_by_core == 1:
            cpu_usage_divide_by_cores = "yes"
        else:
            cpu_usage_divide_by_cores = "no"
        detail_level = "medium"
        self.rows_data_dict = Libsysmon.get_processes_information(process_list, processes_of_user, cpu_usage_divide_by_cores, detail_level, self.rows_data_dict_prev, self.system_boot_time, self.username_uid_dict)
        self.rows_data_dict_prev = dict(self.rows_data_dict)
        pid_list = self.rows_data_dict["pid_list"]
        ppid_list = self.rows_data_dict["ppid_list"]
        username_list = self.rows_data_dict["username_list"]
        cmdline_list = self.rows_data_dict["cmdline_list"]

        # Get and append process data
        tab_data_rows = []
        for pid in pid_list:
            row_data_dict = self.rows_data_dict[pid]
            process_name = row_data_dict["name"]
            ppid = row_data_dict["ppid"]
            # Get process image
            if ppid == 2 or pid == 2:
                process_image = "system-monitoring-center-process-symbolic"
            else:
                process_image = "application-x-executable"
                if process_name in application_image_dict:
                    process_image = application_image_dict[process_name]
            process_commandline = row_data_dict["command_line"]
            tab_data_row = [True, process_image, process_name, process_commandline]
            if 1 in treeview_columns_shown:
                tab_data_row.append(pid)
            if 2 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["username"])
            if 3 in treeview_columns_shown:
                tab_data_row.append(_tr(row_data_dict["status"]))
            if 4 in treeview_columns_shown or 21 in treeview_columns_shown:
                cpu_usage = row_data_dict["cpu_usage"]
                cpu_usage_list.append(cpu_usage)
                if 4 in treeview_columns_shown:
                    tab_data_row.append(cpu_usage)
            if 5 in treeview_columns_shown or 20 in treeview_columns_shown or 22 in treeview_columns_shown or 23 in treeview_columns_shown:
                memory_rss = row_data_dict["memory_rss"]
                memory_rss_list.append(memory_rss)
                if 5 in treeview_columns_shown:
                    tab_data_row.append(memory_rss)
            if 6 in treeview_columns_shown:
                memory_vms = row_data_dict["memory_vms"]
                tab_data_row.append(memory_vms)
                memory_vms_list.append(memory_vms)
            if 7 in treeview_columns_shown or 20 in treeview_columns_shown or 23 in treeview_columns_shown:
                memory_shared = row_data_dict["memory_shared"]
                memory_shared_list.append(memory_shared)
                if 7 in treeview_columns_shown:
                    tab_data_row.append(memory_shared)
            if 8 in treeview_columns_shown:
                process_read_bytes = row_data_dict["read_data"]
                tab_data_row.append(process_read_bytes)
                disk_read_data_list.append(process_read_bytes)
            if 9 in treeview_columns_shown:
                process_write_bytes = row_data_dict["written_data"]
                tab_data_row.append(process_write_bytes)
                disk_write_data_list.append(process_write_bytes)
            if 10 in treeview_columns_shown:
                disk_read_speed = row_data_dict["read_speed"]
                tab_data_row.append(disk_read_speed)
                disk_read_speed_list.append(disk_read_speed)
            if 11 in treeview_columns_shown:
                disk_write_speed = row_data_dict["write_speed"]
                tab_data_row.append(disk_write_speed)
                disk_write_speed_list.append(disk_write_speed)
            if 12 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["nice"])
            if 13 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["number_of_threads"])
            if 14 in treeview_columns_shown:
                tab_data_row.append(ppid)
            if 15 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["uid"])
            if 16 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["gid"])
            if 17 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["start_time"])
            if 18 in treeview_columns_shown:
                tab_data_row.append(process_commandline)
            if 19 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["cpu_time"])
            if 20 in treeview_columns_shown or 23 in treeview_columns_shown:
                memory = row_data_dict["memory"]
                memory_list.append(memory)
                if 20 in treeview_columns_shown:
                    tab_data_row.append(memory)

            # Append process data into a list
            tab_data_rows.append(tab_data_row)

        # Remove first element (0) from "list_of_cell_coloring_data_lists" if data is appended to them.
        list_of_cell_coloring_data_lists = [
                                            cpu_usage_list,
                                            memory_rss_list,
                                            memory_vms_list,
                                            memory_shared_list,
                                            memory_list,
                                            disk_read_data_list,
                                            disk_write_data_list,
                                            disk_read_speed_list,
                                            disk_write_speed_list,
                                            cpu_usage_recursive_list,
                                            memory_rss_recursive_list,
                                            memory_recursive_list
                                            ]

        for cell_coloring_data_list in list_of_cell_coloring_data_lists:
            if cell_coloring_data_list != [0]:
                del cell_coloring_data_list[0]

        tab_data_rows, cpu_usage_recursive_list, memory_rss_recursive_list, memory_recursive_list = self.recursive_cpu_memory_usage(tab_data_rows, treeview_columns_shown, pid_list, ppid_list, cpu_usage_list, memory_rss_list, memory_list)

        self.tab_data_rows = tab_data_rows
        self.pid_list = pid_list

        # Convert set to list (it was set before getting process information)
        treeview_columns_shown = sorted(list(treeview_columns_shown))

        reset_row_unique_data_list_prev = Common.treeview_add_remove_columns(self)
        if reset_row_unique_data_list_prev == "yes":
            self.pid_list_prev = []
        Common.treeview_reorder_columns_sort_rows_set_column_widths(self)

        # Append treestore items (rows) as tree or list structure depending on user preferences.
        if self.show_processes_as_tree != self.show_processes_as_tree_prev:                       # Check if "show_processes_as_tree" setting has been changed since last loop and redefine "piter_list" in order to prevent resetting it in every loop which will cause high CPU consumption because piter_list and treestore content would have been appended/builded from zero.
            self.pid_list_prev = []                                                               # Redefine (clear) "pid_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
            self.treestore.clear()                                                                # Clear treestore because items will be appended from zero (in tree or list structure).
            self.piter_list = []

        # Prevent errors if no rows are found.
        if len(tab_data_rows[0]) == 0:
            return

        deleted_rows, new_rows, updated_existing_row_index = Common.get_new_deleted_updated_rows(pid_list, self.pid_list_prev)
        Common.update_treestore_rows(self, self.rows_data_dict, deleted_rows, new_rows, updated_existing_row_index, pid_list, self.pid_list_prev, self.show_processes_as_tree, self.show_processes_of_all_users)
        Common.searchentry_update_placeholder_text(self, _tr("Processes"))

        # Expand all treeview rows (if treeview items are in tree structured, not list) if this is the first loop
        # of the Processes tab. It expands treeview rows (and children) in all loops if this control is not made.
        # "First loop" control is made by checking if pid_list_prev is empty.
        if self.pid_list_prev == []:
            self.treeview.expand_all()

        self.pid_list_prev = self.pid_list
        self.tab_data_rows_prev = self.tab_data_rows
        self.show_processes_as_tree_prev = self.show_processes_as_tree
        self.treeview_columns_shown_prev = self.treeview_columns_shown
        self.data_row_sorting_column_prev = self.data_row_sorting_column
        self.data_row_sorting_order_prev = self.data_row_sorting_order
        self.data_column_order_prev = self.data_column_order
        self.data_column_widths_prev = self.data_column_widths

        # Get max values of some performance data for setting cell background colors depending on relative performance data.
        global max_value_cpu_usage_list, max_value_memory_rss_list, max_value_memory_vms_list, max_value_memory_shared_list, max_value_memory_list
        global max_value_disk_read_data_list, max_value_disk_write_data_list, max_value_disk_read_speed_list, max_value_disk_write_speed_list
        global max_value_cpu_usage_recursive_list, max_value_memory_rss_recursive_list, max_value_memory_recursive_list
        max_value_cpu_usage_list = max(cpu_usage_list)
        max_value_memory_rss_list = max(memory_rss_list)
        max_value_memory_vms_list = max(memory_vms_list)
        max_value_memory_shared_list = max(memory_shared_list)
        max_value_memory_list = max(memory_list)
        max_value_disk_read_data_list = max(disk_read_data_list)
        max_value_disk_write_data_list = max(disk_write_data_list)
        max_value_disk_read_speed_list = max(disk_read_speed_list)
        max_value_disk_write_speed_list = max(disk_write_speed_list)
        max_value_cpu_usage_recursive_list = max(cpu_usage_recursive_list)
        max_value_memory_rss_recursive_list = max(memory_rss_recursive_list)
        max_value_memory_recursive_list = max(memory_recursive_list)

        # Show/Hide treeview expander arrows. If "child rows" are not used and there is no need for these expanders (they would be shown as empty spaces in this situation).
        if self.show_processes_as_tree == 1:
            self.treeview.set_show_expanders(True)
        else:
            self.treeview.set_show_expanders(False)

        # Show/Hide treeview tree lines
        if Config.show_tree_lines == 1:
            self.treeview.set_enable_tree_lines(True)
        else:
            self.treeview.set_enable_tree_lines(False)

        # Update multiple process information summation labels
        self.multiple_process_information_summation_set_values()


    def recursive_cpu_memory_usage(self, tab_data_rows, treeview_columns_shown, pid_list, ppid_list, cpu_usage_list, memory_rss_list, memory_list):
        """
        Get recursive CPU usage percentage, recursive memory (RSS) and recursive memory information of processes.
        """

        # Define lists before rest of the function for avoiding errors.
        cpu_usage_recursive_list = [0]
        memory_rss_recursive_list = [0]
        memory_recursive_list = [0]

        # Do not run rest of the function for avoiding high CPU usage because of getting PID-child PID dictionary.
        if 21 not in treeview_columns_shown and \
           22 not in treeview_columns_shown and \
           23 not in treeview_columns_shown:
            return tab_data_rows, cpu_usage_recursive_list, memory_rss_recursive_list, memory_recursive_list

        # Get PID-child PID dictionary
        pid_child_pid_dict = {}
        for i, ppid in enumerate(ppid_list):
            pid = pid_list[i]
            if ppid not in pid_child_pid_dict:
                pid_child_pid_dict[ppid] = [pid]
            else:
                pid_child_pid_dict[ppid].append(pid)
        # Append PIDs of sub-branches to PIDs of parent branches in order to
        # generate branches from their roots to end of their all sub-branches.
        pid_child_pid_dict_prev = {}
        while pid_child_pid_dict != pid_child_pid_dict_prev:
            pid_child_pid_dict_prev = dict(pid_child_pid_dict)
            for ppid in pid_child_pid_dict:
                for pid in pid_child_pid_dict[ppid][:]:
                    if pid in pid_child_pid_dict:
                        pid_child_pid_dict[ppid] = list(pid_child_pid_dict[ppid]) + list(pid_child_pid_dict[pid])
                # Remove duplicated PIDs and information for 0th PID in the dictionary
                pid_child_pid_dict_scratch = dict(pid_child_pid_dict)
                pid_child_pid_dict = {}
                for pid in pid_child_pid_dict_scratch:
                    if pid == "0":
                        continue
                    pid_child_pid_dict[pid] = sorted(list(set(pid_child_pid_dict_scratch[pid])), key=int)

        treeview_columns_shown = sorted(list(treeview_columns_shown))

        # Get recursive CPU usage percentage of processes
        if 21 in treeview_columns_shown:
            cpu_total_data_column_index = treeview_columns_shown.index(21) + 3
            for i, pid in enumerate(pid_list):
                process_cpu_usage_total = cpu_usage_list[i]
                if pid in pid_child_pid_dict:
                    child_pid_list = pid_child_pid_dict[pid]
                    for child_pid in child_pid_list:
                        child_pid_index = pid_list.index(child_pid)
                        cpu_usage = cpu_usage_list[child_pid_index]
                        process_cpu_usage_total = process_cpu_usage_total + cpu_usage
                cpu_usage_recursive_list.append(process_cpu_usage_total)
                tab_data_rows[i].insert(cpu_total_data_column_index, process_cpu_usage_total)

        # Get recursive memory (RSS) usage of processes
        if 22 in treeview_columns_shown:
            memory_rss_total_data_column_index = treeview_columns_shown.index(22) + 3
            for i, pid in enumerate(pid_list):
                process_memory_rss_total = memory_rss_list[i]
                if pid in pid_child_pid_dict:
                    child_pid_list = pid_child_pid_dict[pid]
                    for child_pid in child_pid_list:
                        child_pid_index = pid_list.index(child_pid)
                        memory_rss = memory_rss_list[child_pid_index]
                        process_memory_rss_total = process_memory_rss_total + memory_rss
                memory_rss_recursive_list.append(process_memory_rss_total)
                tab_data_rows[i].insert(memory_rss_total_data_column_index, process_memory_rss_total)

        # Get recursive memory usage of processes
        if 23 in treeview_columns_shown:
            memory_total_data_column_index = treeview_columns_shown.index(23) + 3
            for i, pid in enumerate(pid_list):
                process_memory_total = memory_list[i]
                if pid in pid_child_pid_dict:
                    child_pid_list = pid_child_pid_dict[pid]
                    for child_pid in child_pid_list:
                        child_pid_index = pid_list.index(child_pid)
                        memory = memory_list[child_pid_index]
                        process_memory_total = process_memory_total + memory
                memory_recursive_list.append(process_memory_total)
                tab_data_rows[i].insert(memory_total_data_column_index, process_memory_total)

        return tab_data_rows, cpu_usage_recursive_list, memory_rss_recursive_list, memory_recursive_list


# ----------------------------------- Processes - Treeview Cell Functions (defines functions for treeview cell for setting data precisions and/or data units) -----------------------------------
def cell_data_function_cpu_usage_percent(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', f'{value:.{processes_cpu_precision}f} %')
    cell_backround_color(cell, value, max_value_cpu_usage_list)

def cell_data_function_memory_rss(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', data_unit_converter("data", "none", value, processes_memory_data_unit, processes_memory_data_precision))
    cell_backround_color(cell, value, max_value_memory_rss_list)

def cell_data_function_memory_vms(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', data_unit_converter("data", "none", value, processes_memory_data_unit, processes_memory_data_precision))
    cell_backround_color(cell, value, max_value_memory_vms_list)

def cell_data_function_memory_shared(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', data_unit_converter("data", "none", value, processes_memory_data_unit, processes_memory_data_precision))
    cell_backround_color(cell, value, max_value_memory_shared_list)

def cell_data_function_memory(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', data_unit_converter("data", "none", value, processes_memory_data_unit, processes_memory_data_precision))
    cell_backround_color(cell, value, max_value_memory_list)

def cell_data_function_disk_read_data(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', data_unit_converter("data", "none", value, processes_disk_data_unit, processes_disk_data_precision))
    cell_backround_color(cell, value, max_value_disk_read_data_list)

def cell_data_function_disk_write_data(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', data_unit_converter("data", "none", value, processes_disk_data_unit, processes_disk_data_precision))
    cell_backround_color(cell, value, max_value_disk_write_data_list)

def cell_data_function_disk_read_speed(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', f'{data_unit_converter("speed", processes_disk_speed_bit, value, processes_disk_data_unit, processes_disk_data_precision)}/s')
    cell_backround_color(cell, value, max_value_disk_read_speed_list)

def cell_data_function_disk_write_speed(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', f'{data_unit_converter("speed", processes_disk_speed_bit, value, processes_disk_data_unit, processes_disk_data_precision)}/s')
    cell_backround_color(cell, value, max_value_disk_write_speed_list)

def cell_data_function_cpu_time(tree_column, cell, tree_model, iter, data):
    global number_of_clock_ticks
    time_days = tree_model.get(iter, data)[0]/number_of_clock_ticks/60/60/24
    time_days_int = int(time_days)
    time_hours = (time_days -time_days_int) * 24
    time_hours_int = int(time_hours)
    time_minutes = (time_hours - time_hours_int) * 60
    time_minutes_int = int(time_minutes)
    time_seconds = (time_minutes - time_minutes_int) * 60
    if time_days_int == 0 and time_hours_int == 0:
        cpu_time = f'{time_minutes_int:02}:{time_seconds:05.2f}'
    elif time_days_int == 0:
        cpu_time = f'{time_hours_int:02}:{time_minutes_int:02}:{time_seconds:05.2f}'
    else:
        cpu_time = f'{time_days_int:02}:{time_hours_int:02}:{time_minutes_int:02}:{time_seconds:05.2f}'
    cell.set_property('text', cpu_time)

def cell_data_function_start_time(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', datetime.fromtimestamp(tree_model.get(iter, data)[0]).strftime("%d.%m.%Y %H:%M:%S"))

def cell_data_function_cpu_usage_percent_recursive(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', f'{value:.{processes_cpu_precision}f} %')
    cell_backround_color(cell, value, max_value_cpu_usage_recursive_list)

def cell_data_function_memory_rss_recursive(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', data_unit_converter("data", "none", value, processes_memory_data_unit, processes_memory_data_precision))
    cell_backround_color(cell, value, max_value_memory_rss_recursive_list)

def cell_data_function_memory_recursive(tree_column, cell, tree_model, iter, data):
    value = tree_model.get(iter, data)[0]
    cell.set_property('text', data_unit_converter("data", "none", value, processes_memory_data_unit, processes_memory_data_precision))
    cell_backround_color(cell, value, max_value_memory_recursive_list)

def cell_backround_color(cell, value, max_value):
    color = Gdk.RGBA()
    color.red = 0.7
    color.green = 0.35
    color.blue = 0.05
    if value > 0.7 * max_value:
        color.alpha = 0.45
    elif value <= 0.7 * max_value and value > 0.4 * max_value:
        color.alpha = 0.35
    elif value <= 0.4 * max_value and value > 0.2 * max_value:
        color.alpha = 0.25
    elif value <= 0.2 * max_value and value > 0.1 * max_value:
        color.alpha = 0.15
    elif value <= 0.1 * max_value:
        color.alpha = 0.0
    cell.set_property('background-rgba', color)


Processes = Processes()


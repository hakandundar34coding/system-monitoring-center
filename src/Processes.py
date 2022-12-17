#!/usr/bin/env python3

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

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from MainWindow import MainWindow
import Common


class Processes:

    def __init__(self):

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

        # SearchEntry
        self.searchentry = Common.scrolledwindow_searchentry()
        grid.attach(self.searchentry, 1, 0, 1, 1)


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
        self.treeview.set_tooltip_column(2)
        scrolledwindow.set_child(self.treeview)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        self.searchentry.connect("changed", self.on_searchentry_changed)

        # Treeview mouse events.
        treeview_mouse_event = Gtk.GestureClick()
        treeview_mouse_event.connect("pressed", self.on_treeview_pressed)
        treeview_mouse_event.connect("released", self.on_treeview_released)
        self.treeview.add_controller(treeview_mouse_event)

        treeview_mouse_event_right_click = Gtk.GestureClick()
        treeview_mouse_event_right_click.set_button(3)
        treeview_mouse_event_right_click.connect("pressed", self.on_treeview_pressed)
        self.treeview.add_controller(treeview_mouse_event_right_click)

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

        # "Details" action
        action = Gio.SimpleAction.new("processes_details", None)
        action.connect("activate", self.on_details_item_clicked)
        MainWindow.main_window.add_action(action)

        # Accelerators for right click menu actions
        application = MainWindow.main_window.get_application()
        application.set_accels_for_action("win.processes_pause_process", ["<Control>S"])
        application.set_accels_for_action("win.processes_continue_process", ["<Control>C"])
        application.set_accels_for_action("win.processes_end_process", ["<Control>T"])
        application.set_accels_for_action("win.processes_end_process_immediately", ["<Control>K"])
        application.set_accels_for_action("win.processes_details", ["Return"])


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

        details_menu_section = Gio.Menu.new()
        details_menu_section.append(_tr("Details"), "win.processes_details")
        details_menu_section_item = Gio.MenuItem.new()
        details_menu_section_item.set_section(details_menu_section)

        right_click_menu_model = Gio.Menu.new()
        right_click_menu_model.append_item(process_management_menu_section_item)
        right_click_menu_model.append_item(priority_menu_section_item)
        right_click_menu_model.append_item(details_menu_section_item)

        # Popover menu
        self.right_click_menu_po = Gtk.PopoverMenu()
        self.right_click_menu_po.set_menu_model(right_click_menu_model)
        #self.right_click_menu_po.set_parent(self.treeview)
        self.right_click_menu_po.set_parent(MainWindow.main_window)
        self.right_click_menu_po.set_position(Gtk.PositionType.BOTTOM)
        self.right_click_menu_po.set_has_arrow(False)


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
        label.set_label(_tr("Change priority of this process:\n(Smaller value means higher process priority)"))
        label.set_halign(Gtk.Align.START)
        main_grid.attach(label, 0, 0, 1, 1)

        # Label (process name and PID)
        self.priority_process_name_and_pid_label = Gtk.Label()
        self.priority_process_name_and_pid_label.set_selectable(True)
        self.priority_process_name_and_pid_label.set_label("--")
        self.priority_process_name_and_pid_label.set_ellipsize(Pango.EllipsizeMode.END)
        self.priority_process_name_and_pid_label.set_halign(Gtk.Align.START)
        main_grid.attach(self.priority_process_name_and_pid_label, 0, 1, 1, 1)

        # Adjustment (for scale)
        self.adjustment = Gtk.Adjustment()
        self.adjustment.set_step_increment(1.0)

        # Scale
        self.scale = Gtk.Scale(adjustment=self.adjustment)
        self.scale.set_draw_value(True)
        self.scale.set_digits(0)
        main_grid.attach(self.scale, 0, 2, 1, 1)

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
            self.priority_custom_value_window.hide()

        if widget == self.priority_custom_value_change_priority_button:
            # Get right clicked process pid and name.
            selected_process_pid = self.selected_process_pid

            # Get new priority (nice value) of the process.
            selected_process_nice = str(int(self.adjustment.get_value()))

            # Define commands for the process.
            priority_command = ["renice", "-n", selected_process_nice, "-p", selected_process_pid]
            priority_command_pkexec = ["pkexec", "renice", "-n", selected_process_nice, "-p", selected_process_pid]

            if Config.environment_type == "flatpak":
                priority_command = ["flatpak-spawn", "--host"] + priority_command
                priority_command_pkexec = ["flatpak-spawn", "--host"] + priority_command_pkexec

            # Try to change priority (nice value) of the process.
            try:
                (subprocess.check_output(priority_command, stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:
                # Try to change priority (nice value) of the process if root privileges are required.
                try:
                    (subprocess.check_output(priority_command_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
                # Prevent errors if wrong password is used or polkit dialog is closed by user.
                except subprocess.CalledProcessError:
                    return

            self.priority_custom_value_window.hide()


    def on_process_manage_items_clicked(self, action, parameter):
        """
        Pause, continue, end, end immediately processes.
        """

        # Stop running the function if the action is called by using keyboard shortcuts when another tab is opened.
        # Because keyboard shortcuts are defined for window instead of treeview for a simpler code.
        if Config.current_main_tab != 1:
            return

        # Get right clicked process pid and name.
        selected_process_pid = self.selected_process_pid
        selected_process_name = self.processes_data_rows[self.pid_list.index(selected_process_pid)][2]

        # Pause Process
        if action.get_name() == "processes_pause_process":
            process_command = ["kill", "-19", selected_process_pid]
            process_command_pkexec = ["pkexec", "kill", "-19", selected_process_pid]

        # Continue Process
        if action.get_name() == "processes_continue_process":
            process_command = ["kill", "-18", selected_process_pid]
            process_command_pkexec = ["pkexec", "kill", "-18", selected_process_pid]

        # End Process
        if action.get_name() == "processes_end_process":
            process_command = ["kill", "-15", selected_process_pid]
            process_command_pkexec = ["pkexec", "kill", "-15", selected_process_pid]
            process_dialog_message = _tr("Do you want to end this process?")

        # End Process Immediately
        if action.get_name() == "processes_end_process_immediately":
            process_command = ["kill", "-9", selected_process_pid]
            process_command_pkexec = ["pkexec", "kill", "-9", selected_process_pid]
            process_dialog_message = _tr("Do you want to end this process immediately?")

        if Config.environment_type == "flatpak":
            process_command = ["flatpak-spawn", "--host"] + process_command
            process_command_pkexec = ["flatpak-spawn", "--host"] + process_command_pkexec


        if action.get_name() == "processes_pause_process" or action.get_name() == "processes_continue_process":

            # Try to end the process without using root privileges.
            try:
                (subprocess.check_output(process_command, stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:
                # End the process if root privileges are given.
                try:
                    (subprocess.check_output(process_command_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
                # Prevent errors if wrong password is used or polkit dialog is closed by user.
                except subprocess.CalledProcessError:
                    pass

        # Show warning dialog if process is tried to be ended.
        if Config.warn_before_stopping_processes == 1 and (action.get_name() == "processes_end_process" or action.get_name() == "processes_end_process_immediately"):
            messagedialog = Gtk.MessageDialog(transient_for=MainWindow.main_window,
                                              modal=True,
                                              title="",
                                              message_type=Gtk.MessageType.WARNING,
                                              buttons=Gtk.ButtonsType.YES_NO,
                                              text=process_dialog_message,
                                              secondary_text=selected_process_name + " (" + "PID" + ": " + str(selected_process_pid) + ")")

            messagedialog.connect("response", self.on_messagedialog_response, process_command, process_command_pkexec)
            messagedialog.present()


    def on_messagedialog_response(self, widget, response, process_command, process_command_pkexec):
        """
        End process if "YES" button on the dialog is clicked.
        """

        if response == Gtk.ResponseType.YES:
            # Try to end the process without using root privileges.
            try:
                (subprocess.check_output(process_command, stderr=subprocess.STDOUT, shell=False)).decode()
            except subprocess.CalledProcessError:
                # End the process if root privileges are given.
                try:
                    (subprocess.check_output(process_command_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
                # Prevent errors if wrong password is used or polkit dialog is closed by user.
                except subprocess.CalledProcessError:
                    pass

        messagedialog = widget
        messagedialog.hide()


    def set_priority_menu_option(self):
        """
        Set process priority (nice) option on the right click menu.
        """

        # Get right clicked process pid and name.
        selected_process_pid = self.selected_process_pid

        # Get process stat file path.
        selected_process_stat_file = "/proc/" + selected_process_pid + "/stat"

        # Get priority (nice value) of the process.
        command_list = ["cat", selected_process_stat_file]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list

        cat_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE)).stdout.decode().strip()

        # Process may be ended just after pid_list is generated. "cat" command output is get as "" in this situation.
        if cat_output != "":
            selected_process_nice = int(cat_output.split()[-34])
        else:
            return

        # Set menu GUI.
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

        # Get right clicked process pid.
        selected_process_pid = self.selected_process_pid

        if action.get_name() == "processes_priority_group":

            # Set priority (Very High)
            if parameter == GLib.Variant("s", "processes_priority_very_high"):
                action.set_state(GLib.Variant("s", "processes_priority_very_high"))
                priority_command = ["renice", "-n", "-20", "-p", selected_process_pid]
                priority_command_pkexec = ["pkexec", "renice", "-n", "-20", "-p", selected_process_pid]

            # Set priority (High)
            elif parameter == GLib.Variant("s", "processes_priority_high"):
                action.set_state(GLib.Variant("s", "processes_priority_high"))
                priority_command = ["renice", "-n", "-10", "-p", selected_process_pid]
                priority_command_pkexec = ["pkexec", "renice", "-n", "-10", "-p", selected_process_pid]

            # Set priority (Normal)
            elif parameter == GLib.Variant("s", "processes_priority_normal"):
                action.set_state(GLib.Variant("s", "processes_priority_normal"))
                priority_command = ["renice", "-n", "-0", "-p", selected_process_pid]
                priority_command_pkexec = ["pkexec", "renice", "-n", "0", "-p", selected_process_pid]

            # Set priority (Low)
            elif parameter == GLib.Variant("s", "processes_priority_low"):
                action.set_state(GLib.Variant("s", "processes_priority_low"))
                priority_command = ["renice", "-n", "10", "-p", selected_process_pid]
                priority_command_pkexec = ["pkexec", "renice", "-n", "10", "-p", selected_process_pid]

            # Set priority (Very Low)
            elif parameter == GLib.Variant("s", "processes_priority_very_low"):
                action.set_state(GLib.Variant("s", "processes_priority_very_low"))
                priority_command = ["renice", "-n", "19", "-p", selected_process_pid]
                priority_command_pkexec = ["pkexec", "renice", "-n", "19", "-p", selected_process_pid]

            if Config.environment_type == "flatpak":
                priority_command = ["flatpak-spawn", "--host"] + priority_command
                priority_command_pkexec = ["flatpak-spawn", "--host"] + priority_command_pkexec

            # Try to change priority of the process.
            try:
                (subprocess.check_output(priority_command, stderr=subprocess.STDOUT, shell=False)).decode()
                # Stop running the function if process priority is changed without root privileges.
                return
            except subprocess.CalledProcessError:
                # Try to change priority of the process if root privileges are required.
                try:
                    (subprocess.check_output(priority_command_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
                except subprocess.CalledProcessError:
                    return

        if action.get_name() == "processes_priority_custom_value":

            # Get right clicked process name.
            selected_process_name = self.processes_data_rows[Processes.pid_list.index(selected_process_pid)][2]

            # Get process stat file path.
            selected_process_stat_file = "/proc/" + selected_process_pid + "/stat"

            # Get priority (nice value) of the process.
            command_list = ["cat", selected_process_stat_file]
            if Config.environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list

            cat_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE)).stdout.decode().strip()

            # Process may be ended just after pid_list is generated. "cat" command output is get as "" in this situation.
            if cat_output != "":
                selected_process_nice = int(cat_output.split()[-34])
            else:
                return

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
            self.priority_process_name_and_pid_label.set_label(f'{selected_process_name} - (PID: {selected_process_pid})')


    def on_details_item_clicked(self, action, parameter):
        """
        Show process details window.
        """

        # Stop running the function if the action is called by using keyboard shortcuts when another tab is opened.
        # Because keyboard shortcuts are defined for window instead of treeview for a simpler code.
        if Config.current_main_tab != 1:
            return

        import ProcessesDetails
        ProcessesDetails.process_details_show_process_details()


    def on_searchentry_changed(self, widget):
        """
        Called by searchentry when text is changed.
        """

        process_search_text = self.searchentry.get_text().lower()

        # Set visible/hidden processes
        for piter in self.piter_list:
            self.treestore.set_value(piter, 0, False)
            process_data_text_in_model = self.treestore.get_value(piter, self.filter_column)
            if process_search_text in str(process_data_text_in_model).lower():
                self.treestore.set_value(piter, 0, True)
                # Make parent processes visible if one of its children is visible.
                piter_parent = self.treestore.iter_parent(piter)
                while piter_parent != None:
                    self.treestore.set_value(piter_parent, 0, True)
                    piter_parent = self.treestore.iter_parent(piter_parent)
        # Expand all treeview rows (if tree view is preferred) after filtering is applied (after any text is typed into search entry).
        self.treeview.expand_all()


    def on_treeview_pressed(self, event, count, x, y):
        """
        Mouse single right click and double left click events (button press).
        Right click menu is opened when right clicked. Details window is shown when double clicked.
        """

        # Convert coordinates for getting path.
        x_bin, y_bin = self.treeview.convert_widget_to_bin_window_coords(x,y)

        # Get right/double clicked row data
        try:
            path, _, _, _ = self.treeview.get_path_at_pos(int(x_bin), int(y_bin))
        # Prevent errors when right clicked on an empty area on the treeview.
        except TypeError:
            return
        model = self.treeview.get_model()
        treeiter = model.get_iter(path)
        self.aaa=model
        # Get right/double clicked process PID
        if treeiter == None:
            return
        try:
            self.selected_process_pid = self.pid_list[self.processes_data_rows.index(model[treeiter][:])]
        # It gives error such as "ValueError: [True, 'system-monitoring-center-process-symbolic', 'python3', 2411, 'user', 'Running', 1.6633495783351964, 98824192, 548507648, 45764608, 0, 16384, 0, 5461, 0, 4, 1727, 1000, 1000, '/usr/bin/python3.9'] is not in list" rarely.
        # It is handled in this situation.
        except ValueError:
            return

        # Show right click menu if right clicked on a row
        if int(event.get_button()) == 3:

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

        # Show details window if double clicked on a row
        if int(event.get_button()) == 1 and int(count) == 2:
            import ProcessesDetails
            ProcessesDetails.process_details_show_process_details()


    def on_treeview_released(self, event, count, x, y):
        """
        Mouse single left click event (button release).
        Update teeview column/row width/sorting/order.
        """

        # Check if left mouse button is used
        if int(event.get_button()) == 1:
            self.treeview_column_order_width_row_sorting()


    def processes_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        # data list explanation:
        # processes_data_list = [
        #                       [treeview column number, treeview column title, internal column count, cell renderer count, treeview column sort column id, [data type 1, data type 2, ...], [cell renderer type 1, cell renderer type 2, ...], [cell attribute 1, cell attribute 2, ...], [cell renderer data 1, cell renderer data 2, ...], [cell left/right alignment 1, cell left/right alignment 2, ...], [set expand 1 {if cell will allocate unused space} cell expand 2, ...], [cell function 1, cell function 2, ...]]
        #                       .
        #                       .
        #                       ]
        global processes_data_list
        processes_data_list = [
                              [0, _tr('Name'), 3, 2, 3, [bool, str, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'icon_name', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
                              [1, _tr('PID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
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
                              [17, _tr('Path'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                              [18, _tr('Command Line'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']]
                              ]

        # Define data unit conversion function objects in for lower CPU usage.
        global performance_define_data_unit_converter_variables_func, performance_define_data_unit_converter_variables_func, performance_data_unit_converter_func
        performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
        performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        # Define data unit conversion variables before they are used.
        performance_define_data_unit_converter_variables_func()


        global processes_data_rows_prev, pid_list_prev, global_process_cpu_times_prev, disk_read_write_data_prev, show_processes_as_tree_prev, processes_treeview_columns_shown_prev, processes_data_row_sorting_column_prev, processes_data_row_sorting_order_prev, processes_data_column_order_prev, processes_data_column_widths_prev
        processes_data_rows_prev = []
        pid_list_prev = []
        self.piter_list = []
        global_process_cpu_times_prev = []
        disk_read_write_data_prev = []
        show_processes_as_tree_prev = Config.show_processes_as_tree
        processes_treeview_columns_shown_prev = []
        processes_data_row_sorting_column_prev = ""
        processes_data_row_sorting_order_prev = ""
        processes_data_column_order_prev = []
        processes_data_column_widths_prev = []

        global process_status_list, number_of_clock_ticks, memory_page_size, application_exec_list, application_icon_list
        process_status_list = {"R": _tr("Running"), "S": _tr("Sleeping"), "D": _tr("Waiting"), "I": _tr("Idle"), "Z": _tr("Zombie"), "T": _tr("Stopped"), "t": "Tracing Stop", "X": "Dead"}    # This list is used in order to show full status of the process. For more information, see: "https://man7.org/linux/man-pages/man5/proc.5.html".
        number_of_clock_ticks = os.sysconf("SC_CLK_TCK")                                          # For many systems CPU ticks 100 times in a second. Wall clock time could be get if CPU times are multiplied with this value or vice versa.
        memory_page_size = os.sysconf("SC_PAGE_SIZE")                                             # This value is used for converting memory page values into byte values. This value depends on architecture (also sometimes depends on machine model). Default value is 4096 Bytes (4 KiB) for most processors.

        # Get application names, images and types.
        global application_exec_list, application_icon_list, application_type_list
        application_exec_list, application_icon_list, application_type_list = self.application_exec_icon_type_list()

        self.filter_column = processes_data_list[0][2] - 1                                        # Search filter is "Process Name". "-1" is used because "processes_data_list" has internal column count and it has to be converted to Python index. For example, if there are 3 internal columns but index is 2 for the last internal column number for the relevant treeview column.

        self.process_status_list = process_status_list
        self.number_of_clock_ticks = number_of_clock_ticks
        self.memory_page_size = memory_page_size
        self.application_exec_list = application_exec_list
        self.application_icon_list = application_icon_list

        self.initial_already_run = 1


    def processes_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        update_interval = Config.update_interval

        # Get GUI obejcts one time per floop instead of getting them multiple times

        # Get configrations one time per floop instead of getting them multiple times (hundreds of times for many of them) in every loop which causes high CPU usage.
        global processes_cpu_precision
        global processes_memory_data_precision, processes_memory_data_unit
        global processes_disk_data_precision, processes_disk_data_unit, processes_disk_speed_bit
        processes_cpu_precision = Config.processes_cpu_precision
        processes_memory_data_precision = Config.processes_memory_data_precision
        processes_memory_data_unit = Config.processes_memory_data_unit
        processes_disk_data_precision = Config.processes_disk_data_precision
        processes_disk_data_unit = Config.processes_disk_data_unit
        processes_disk_speed_bit = Config.processes_disk_speed_bit

        # Define global variables and get treeview columns, sort column/order, column widths, etc.
        global processes_treeview_columns_shown, show_processes_of_all_users
        global processes_treeview_columns_shown_prev, processes_data_row_sorting_column_prev, processes_data_row_sorting_order_prev, processes_data_column_order_prev, processes_data_column_widths_prev
        processes_treeview_columns_shown = Config.processes_treeview_columns_shown
        processes_data_row_sorting_column = Config.processes_data_row_sorting_column
        processes_data_row_sorting_order = Config.processes_data_row_sorting_order
        processes_data_column_order = Config.processes_data_column_order
        processes_data_column_widths = Config.processes_data_column_widths
        show_processes_of_all_users = Config.show_processes_of_all_users

        # Define lists for appending some performance data for calculating max values to determine cell background color.
        cpu_usage_list = []
        memory_rss_list = []
        memory_vms_list = []
        memory_shared_list = []
        disk_read_data_list = []
        disk_write_data_list = []
        disk_read_speed_list = []
        disk_write_speed_list = []

        # Get number of online logical CPU cores (this operation is repeated in every loop because number of online CPU cores may be changed by user and this may cause wrong calculation of CPU usage percent data of the processes even if this is a very rare situation.)
        number_of_logical_cores = Common.number_of_logical_cores()

        # Get current username which will be used for determining processes from only this user or other users.
        current_user_name = os.environ.get('USER')

        # Get process PIDs and define global variables and empty lists for the current loop
        global processes_data_rows_prev, global_process_cpu_times_prev, disk_read_write_data_prev, pid_list_prev
        processes_data_rows = []
        ppid_list = []
        username_list = []
        global_process_cpu_times = []
        disk_read_write_data = []
        pid_list = []

        processes_treeview_columns_shown = set(processes_treeview_columns_shown)                  # For obtaining lower CPU usage (because "if [number] in processes_treeview_columns_shown:" check is repeated thousand of times).


        command_list = ["env", "LANG=C", "ps", "-eo", "comm:96,pid,user:80,s,rss,vsz,sz,nice,thcount,ppid,uid,gid,exe:800,command=CMDLINE"]
        # "exe" parameter is not recognized by "ps" command in "coreutils" package if version
        # is lower than 8.32. "group" parameter is used instead of "exe as a placeholder.
        command_list2 = ["env", "LANG=C", "ps", "-eo", "comm:96,pid,user:80,s,rss,vsz,sz,nice,thcount,ppid,uid,gid,group:800,command=CMDLINE"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
            command_list2 = ["flatpak-spawn", "--host"] + command_list2
        # Get process information by using "ps" command. "env" and "LANG=C" parameters are used in order to get column headers in English.
        exe_column_get = 1
        try:
            # "stderr=subprocess.STDOUT" is used for not printing errors.
            ps_output = (subprocess.check_output(command_list, stderr=subprocess.STDOUT, shell=False)).decode().strip()
        except subprocess.CalledProcessError:
            ps_output = (subprocess.check_output(command_list2, stderr=subprocess.STDOUT, shell=False)).decode().strip()
            exe_column_get = 0

        ps_output_lines = ps_output.split("\n")
        # Get first line (command output headers) for using it to determine column data locations. Because some columns (such as cmdline) may contain spaces.
        ps_output_headers = ps_output_lines[0]
        # Get column locations. "16" is subtracted because some column names may start after a few character on the right side. There is no need to use subtraction for "EXE" column because previous column "GID" is an integer data which is aligned to right.
        pid_column_index = ps_output_headers.index("PID") - 16
        if exe_column_get == 1:
            exe_column_index = ps_output_headers.index("EXE")
        else:
            exe_column_index = ps_output_headers.index("GROUP")
        cmdline_column_index = ps_output_headers.index("CMDLINE") - 16

        # Deleted first line (command output headers).
        del ps_output_lines[0]
        # Get PIDs and user names of the processes from the current user (show processes only from this user)
        # if it is preferred by user. PID values are appended as string values because they are used as string
        # values in various places in the code and this ensures lower CPU usage by avoiding hundreds/thousands
        # of times integer to string conversion. Commandlines will be used for determining full names of the
        # processes if their names are longer than 15 characters.
        cmdline_list = []
        for line in ps_output_lines:
            line_split = line[pid_column_index:].split()
            username = line_split[1]
            if show_processes_of_all_users == 0 and username != current_user_name:
                continue
            else:
                pid_list.append(line_split[0])
                username_list.append(username)
                ppid_list.append(line_split[8])
                cmdline_list.append(line[cmdline_column_index:].strip())

        # Get process data.
        # Get process names, images and CPU times for calculating usage information.
        global previous_line_process
        previous_line_process = 0
        # Read "" and "" files by using "cat" command for calculating process CPU usages and read/write speeds.
        command_list = ["cat"]
        if Config.environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        for pid in pid_list:
            command_list.append(f'/proc/{pid}/stat')
            command_list.append(f'/proc/{pid}/io')
        cat_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()
        global_cpu_time_all = time.time() * number_of_clock_ticks                                 # global_cpu_time_all value is get just after "/proc/[PID]/stat file is get in order to measure global an process specific CPU times at the same time (nearly) for ensuring accurate process CPU usage percent.
        cat_output_lines = cat_output.split("\n")
        process_cpu_time_list = []
        pid_list_from_stat = []
        for line in cat_output_lines:
            line_split = line.split()
            if line_split[0].isdigit():
                process_pid = line_split[0]
                if process_pid not in pid_list:
                    continue
                if previous_line_process == 1:                                                    # Add "disk_read_write" data of the previous process if it has no readable "/proc/[PID]/io" file.
                    disk_read_write_data.append([0, 0])
                pid_list_from_stat.append(process_pid)                                            # This information will be used for removing "cat" command output data of stopped processes.
                process_cpu_time_list.append(int(line_split[-38]) + int(line_split[-39]))         # Get process cpu time in user mode (utime + stime)
                previous_line_process = 1
            else:
                if line_split[0] == "read_bytes:":
                    disk_read_write_data.append([int(line_split[1])])
                if line_split[0] == "write_bytes:":
                    disk_read_write_data[-1].append(int(line_split[1]))
                    previous_line_process = 0
        if len(disk_read_write_data) < len(pid_list_from_stat):                                   # Append disk read/write data of the last process if it the line starts with digit number. This is skipped in the loop.
            disk_read_write_data.append([0, 0])

        # Get process shared memory data for all processes. This information is not provided
        # by "ps" command. "ps" command output is processes line-by-line and next line is
        # detected as process statm file if current line contains string value in the second element.
        if 7 in processes_treeview_columns_shown:
            command_list = ["cat"]
            if Config.environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list
            for pid in pid_list:
                command_list.append("/proc/" + pid + "/stat")
                command_list.append("/proc/" + pid + "/statm")
            cat_output_lines = (subprocess.run(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)).stdout.decode().strip().split("\n")
            process_memory_shared_list = []
            pid_list_from_stat_statm = []
            for i, line in enumerate(cat_output_lines):
                line_split = line.split()
                if line_split[1].isdigit() == False:
                    process_pid = line_split[0]
                    if process_pid not in pid_list:
                        continue
                    next_line = cat_output_lines[i+1]
                    next_line_split = next_line.split()
                    if next_line_split[1].isdigit() == True:
                        process_memory_shared_list.append(int(next_line_split[2]) * memory_page_size)
                    else:
                        process_memory_shared_list.append(0)
                    pid_list_from_stat_statm.append(process_pid)
            if len(process_memory_shared_list) < len(pid_list_from_stat_statm):
                process_memory_shared_list.append(0)

        # Get and append process data.
        for pid in pid_list[:]:                                                                   # "[:]" is used for iterating over copy of the list because elements are removed during iteration. Otherwise incorrect operations (incorrect element removals) are performed on the list.
            index = pid_list.index(pid)
            if pid not in pid_list_from_stat:
                del pid_list[index]
                del username_list[index]
                del ppid_list[index]
                del cmdline_list[index]
                del ps_output_lines[index]
                continue
            index_from_stat = pid_list_from_stat.index(pid)
            ps_output_line = ps_output_lines[index]
            ps_output_line_split = ps_output_line[pid_column_index:].split()
            # Get process full name.
            process_name_from_stat = ps_output_line[:pid_column_index].strip()
            process_name = process_name_from_stat
            if len(process_name) == 15:                                                           # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character (not all process cmdlines have this) in order to obtain full process name.
                process_cmdline = cmdline_list[index]
                process_name = process_cmdline.split("/")[-1].split(" ")[0]
                if process_name.startswith(process_name_from_stat) == False:
                    process_name = process_cmdline.split(" ")[0].split("/")[-1]
                    if process_name.startswith(process_name_from_stat) == False:
                        process_name = process_name_from_stat
            # Get process image.
            if ppid_list[index] == "2" or pid == "2":
                process_icon = "system-monitoring-center-process-symbolic"
            else:
                process_icon = "application-x-executable"                            # Initial value of "process_icon". This icon will be shown for processes of which icon could not be found in default icon theme.
                if process_name in application_exec_list:                                             # Use process icon name from application file if process name is found in application exec list.
                    process_icon = application_icon_list[application_exec_list.index(process_name)]
            processes_data_row = [True, process_icon, process_name]                               # Process row visibility data (True/False) which is used for showing/hiding process when processes of specific user is preferred to be shown or process search feature is used from the GUI.
            # Get process PID. Value is appended as integer for ensuring correct "PID" column sorting such as 1,2,10,101... Otherwise it would sort such as 1,10,101,2...
            if 1 in processes_treeview_columns_shown:
                processes_data_row.append(int(pid))
            # Get process username.
            if 2 in processes_treeview_columns_shown:
                processes_data_row.append(username_list[index])
            # Get process status.
            if 3 in processes_treeview_columns_shown:
                processes_data_row.append(process_status_list[ps_output_line_split[2]])
            # Get process CPU usage.
            if 4 in processes_treeview_columns_shown:
                process_cpu_time = process_cpu_time_list[index_from_stat]
                global_process_cpu_times.append((global_cpu_time_all, process_cpu_time))
                try:
                    global_cpu_time_all_prev, process_cpu_time_prev = global_process_cpu_times_prev[pid_list_prev.index(pid)]
                except (ValueError, IndexError, UnboundLocalError) as e:
                    process_cpu_time_prev = process_cpu_time                                      # There is no "process_cpu_time_prev" value and get it from "process_cpu_time" if this is first loop of the process.
                    global_cpu_time_all_prev = global_process_cpu_times[-1][0] - 1                # Subtract "1" CPU time (a negligible value) if this is first loop of the process.
                process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
                global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
                cpu_usage = process_cpu_time_difference / global_cpu_time_difference * 100 / number_of_logical_cores
                processes_data_row.append(cpu_usage)
                cpu_usage_list.append(cpu_usage)
            # Get process RSS (resident set size) memory pages and multiply with 1024 in order to convert the value into bytes.
            if 5 in processes_treeview_columns_shown:
                memory_rss = int(ps_output_line_split[3]) * 1024
                processes_data_row.append(memory_rss)
                memory_rss_list.append(memory_rss)
            # Get process VMS (virtual memory size) memory and multiply with 1024 in order to convert the value into bytes.
            if 6 in processes_treeview_columns_shown:
                memory_vms = int(ps_output_line_split[4]) * 1024
                processes_data_row.append(memory_vms)
                memory_vms_list.append(memory_vms)
            # Get process shared memory size and multiply with 1024 in order to convert the value into bytes.
            if 7 in processes_treeview_columns_shown:
                if pid in pid_list_from_stat_statm:
                    index_from_stat_statm = pid_list_from_stat_statm.index(pid)
                    process_memory_shared = process_memory_shared_list[index_from_stat_statm]
                else:
                    process_memory_shared = 0
                processes_data_row.append(process_memory_shared)
                memory_shared_list.append(process_memory_shared)
            # Get process read data, write data, read speed, write speed.
            if 8 in processes_treeview_columns_shown or 9 in processes_treeview_columns_shown or 10 in processes_treeview_columns_shown or 11 in processes_treeview_columns_shown:
                process_read_bytes = disk_read_write_data[index_from_stat][0]
                process_write_bytes = disk_read_write_data[index_from_stat][1]
                try:
                    process_read_bytes_prev, process_write_bytes_prev = disk_read_write_data_prev[pid_list_prev.index(pid)]
                except (ValueError, IndexError, UnboundLocalError) as e:
                    process_read_bytes_prev = process_read_bytes                                  # Make process_read_bytes_prev equal to process_read_bytes for giving "0" disk read speed value if this is first loop of the process
                    process_write_bytes_prev = process_write_bytes                                # Make process_write_bytes_prev equal to process_write_bytes for giving "0" disk write speed value if this is first loop of the process
                if pid not in pid_list_prev and disk_read_write_data_prev != []:
                    disk_read_write_data_prev.append((process_read_bytes, process_write_bytes))
                # Get process read data.
                if 8 in processes_treeview_columns_shown:
                    processes_data_row.append(process_read_bytes)
                    disk_read_data_list.append(process_read_bytes)
                # Get process write data.
                if 9 in processes_treeview_columns_shown:
                    processes_data_row.append(process_write_bytes)
                    disk_write_data_list.append(process_write_bytes)
                # Get process read speed.
                if 10 in processes_treeview_columns_shown:
                    disk_read_speed = (process_read_bytes - process_read_bytes_prev) / update_interval
                    processes_data_row.append(disk_read_speed)    # Append process_read_bytes which will be used as "process_read_bytes_prev" value in the next loop and also append disk read speed. 
                    disk_read_speed_list.append(disk_read_speed)
                # Get process write speed.
                if 11 in processes_treeview_columns_shown:
                    disk_write_speed = (process_write_bytes - process_write_bytes_prev) / update_interval
                    processes_data_row.append(disk_write_speed)    # Append process_write_bytes which will be used as "process_write_bytes_prev" value in the next loop and also append disk write speed. 
                    disk_write_speed_list.append(disk_write_speed)
            # Get process nice value.
            if 12 in processes_treeview_columns_shown:
                process_nice = ps_output_line_split[6]
                if process_nice == "-":
                    process_nice = "0"
                processes_data_row.append(int(process_nice))
            # Get process number of threads value.
            if 13 in processes_treeview_columns_shown:
                processes_data_row.append(int(ps_output_line_split[7]))
            # Get process PPID.
            if 14 in processes_treeview_columns_shown:
                processes_data_row.append(int(ps_output_line_split[8]))
            # Append process UID value.
            if 15 in processes_treeview_columns_shown:
                processes_data_row.append(int(ps_output_line_split[9]))
            # Append process GID value.
            if 16 in processes_treeview_columns_shown:
                processes_data_row.append(int(ps_output_line_split[10]))
            # Get process executable path.
            if 17 in processes_treeview_columns_shown:
                if exe_column_get == 1:
                    process_exe = ps_output_line[exe_column_index:cmdline_column_index].strip()
                else:
                    process_exe = "[Not Supported]"
                processes_data_row.append(process_exe)
            # Get process commandline.
            if 18 in processes_treeview_columns_shown:
                processes_data_row.append(ps_output_line[cmdline_column_index:].strip())

            # Append process data into a list (processes_data_rows)
            processes_data_rows.append(processes_data_row)
        global_process_cpu_times_prev = global_process_cpu_times                                  # For using values in the next loop
        disk_read_write_data_prev = disk_read_write_data

        processes_treeview_columns_shown = sorted(list(processes_treeview_columns_shown))         # Convert set to list (it was set before getting process information)

        # Add/Remove treeview columns appropriate for user preferences
        if processes_treeview_columns_shown != processes_treeview_columns_shown_prev:             # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
            cumulative_sort_column_id = -1
            cumulative_internal_data_id = -1
            for column in self.treeview.get_columns():                                             # Remove all columns in the treeview.
                self.treeview.remove_column(column)
            for i, column in enumerate(processes_treeview_columns_shown):
                if processes_data_list[column][0] in processes_treeview_columns_shown:
                    cumulative_sort_column_id = cumulative_sort_column_id + processes_data_list[column][2]
                processes_treeview_column = Gtk.TreeViewColumn(processes_data_list[column][1])    # Define column (also column title is defined)
                for i, cell_renderer_type in enumerate(processes_data_list[column][6]):
                    cumulative_internal_data_id = cumulative_internal_data_id + 1
                    if cell_renderer_type == "internal_column":                                   # Continue to next loop to avoid generating a cell renderer for internal column (internal columns are not shon on the treeview and they do not have cell renderers).
                        continue
                    if cell_renderer_type == "CellRendererPixbuf":                                # Define cell renderer
                        cell_renderer = Gtk.CellRendererPixbuf()
                    if cell_renderer_type == "CellRendererText":
                        cell_renderer = Gtk.CellRendererText()
                    cell_renderer.set_alignment(processes_data_list[column][9][i], 0.5)           # Vertical alignment is set 0.5 in order to leave it as unchanged.
                    processes_treeview_column.pack_start(cell_renderer, processes_data_list[column][10][i])    # Set if column will allocate unused space
                    processes_treeview_column.add_attribute(cell_renderer, processes_data_list[column][7][i], cumulative_internal_data_id)
                    if processes_data_list[column][11][i] != "no_cell_function":
                        processes_treeview_column.set_cell_data_func(cell_renderer, processes_data_list[column][11][i], func_data=cumulative_internal_data_id)    # Define cell function which sets cell data precision and/or data unit
                processes_treeview_column.set_sizing(2)                                           # Set column sizing (2 = auto sizing which is required for "self.treeview.set_fixed_height_mode(True)" command that is used for lower treeview CPU consumption because row heights are not calculated for every row).
                processes_treeview_column.set_sort_column_id(cumulative_sort_column_id)           # Be careful with lists contain same element more than one.
                processes_treeview_column.set_resizable(True)                                     # Set columns resizable by the user when column title button edge handles are dragged.
                processes_treeview_column.set_reorderable(True)                                   # Set columns reorderable by the user when column title buttons are dragged.
                processes_treeview_column.set_min_width(50)                                       # Set minimum column widths as "50 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
                processes_treeview_column.connect("clicked", self.on_column_title_clicked)        # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
                self.treeview.append_column(processes_treeview_column)                            # Append column into treeview

            # Get column data types for appending processes data into treestore
            processes_data_column_types = []
            for column in sorted(processes_treeview_columns_shown):
                internal_column_count = len(processes_data_list[column][5])
                for internal_column_number in range(internal_column_count):
                    processes_data_column_types.append(processes_data_list[column][5][internal_column_number])    # Get column types (int, bool, float, str, etc.)

            # Define a treestore (for storing treeview data in it), a treemodelfilter (for search filtering), treemodelsort (for row sorting when column title buttons are clicked)
            self.treestore = Gtk.TreeStore()
            self.treestore.set_column_types(processes_data_column_types)                           # Set column types of the columns which will be appended into treestore
            treemodelfilter2101 = self.treestore.filter_new()
            treemodelfilter2101.set_visible_column(0)                                             # Column "0" of the treestore will be used for column visibility information (True or False)
            treemodelsort2101 = Gtk.TreeModelSort().new_with_model(treemodelfilter2101)
            self.treeview.set_model(treemodelsort2101)
            pid_list_prev = []                                                                    # Redefine (clear) "pid_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
            self.piter_list = []

        # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
        if processes_treeview_columns_shown_prev != processes_treeview_columns_shown or processes_data_column_order_prev != processes_data_column_order:
            processes_treeview_columns = self.treeview.get_columns()                               # Get shown columns on the treeview in order to use this data for reordering the columns.
            treeview_column_titles = []
            for column in processes_treeview_columns:
                treeview_column_titles.append(column.get_title())
            processes_data_column_order_scratch = []
            for column_order in processes_data_column_order:
                if column_order != -1:
                    processes_data_column_order_scratch.append(column_order)
            for order in reversed(sorted(processes_data_column_order_scratch)):                   # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
                if processes_data_column_order.index(order) in processes_treeview_columns_shown:
                    column_number_to_move = processes_data_column_order.index(order)
                    column_title_to_move = processes_data_list[column_number_to_move][1]
                    column_to_move = processes_treeview_columns[treeview_column_titles.index(column_title_to_move)]
                    self.treeview.move_column_after(column_to_move, None)                          # Column is moved at the beginning of the treeview if "None" is used.

        # Sort process rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
        if processes_treeview_columns_shown_prev != processes_treeview_columns_shown or processes_data_row_sorting_column_prev != processes_data_row_sorting_column or processes_data_row_sorting_order != processes_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
            processes_treeview_columns = self.treeview.get_columns()                               # Get shown columns on the treeview in order to use this data for reordering the columns.
            treeview_column_titles = []
            for column in processes_treeview_columns:
                treeview_column_titles.append(column.get_title())
            for i in range(10):
                if processes_data_row_sorting_column in processes_treeview_columns_shown:
                    for data in processes_data_list:
                        if data[0] == processes_data_row_sorting_column:
                            column_title_for_sorting = data[1]
                if processes_data_row_sorting_column not in processes_treeview_columns_shown:
                    column_title_for_sorting = processes_data_list[0][1]
                column_for_sorting = processes_treeview_columns[treeview_column_titles.index(column_title_for_sorting)]
                column_for_sorting.clicked()                                                      # For row sorting.
                if processes_data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                    break

        # Set column widths if there are changes since last loop.
        if processes_treeview_columns_shown_prev != processes_treeview_columns_shown or processes_data_column_widths_prev != processes_data_column_widths:
            processes_treeview_columns = self.treeview.get_columns()
            treeview_column_titles = []
            for column in processes_treeview_columns:
                treeview_column_titles.append(column.get_title())
            for i, processes_data in enumerate(processes_data_list):
                for j, column_title in enumerate(treeview_column_titles):
                    if column_title == processes_data[1]:
                       column_width = processes_data_column_widths[i]
                       processes_treeview_columns[j].set_fixed_width(column_width)                # Set column width in pixels. Fixed width is unset if value is "-1".

        # Append treestore items (rows) as tree or list structure depending on user preferences.
        global show_processes_as_tree_prev
        show_processes_as_tree = Config.show_processes_as_tree
        if show_processes_as_tree != show_processes_as_tree_prev:                                 # Check if "show_processes_as_tree" setting has been changed since last loop and redefine "piter_list" in order to prevent resetting it in every loop which will cause high CPU consumption because piter_list and treestore content would have been appended/builded from zero.
            pid_list_prev = []                                                                    # Redefine (clear) "pid_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
            self.treestore.clear()                                                                 # Clear treestore because items will be appended from zero (in tree or list structure).
            self.piter_list = []

        # Get new/deleted(ended) processes for updating treestore/treeview
        pid_list_prev_set = set(pid_list_prev)
        pid_list_set = set(pid_list)
        deleted_processes = sorted(list(pid_list_prev_set - pid_list_set), key=int)               # "sorted(list, key=int)" is used for sorting string list (like "'1', '2', '10', '100'") as integer list without converting the list into integer list. Otherwise it is sorted like "'1', '10', '100', '2'".
        new_processes = sorted(list(pid_list_set - pid_list_prev_set), key=int)
        existing_processes = sorted(list(pid_list_set.intersection(pid_list_prev)), key=int)
        updated_existing_proc_index = [[pid_list.index(i), pid_list_prev.index(i)] for i in existing_processes]    # "c = set(a).intersection(b)" is about 19% faster than "c = set(a).intersection(set(b))"
        processes_data_rows_row_length = len(processes_data_rows[0])
        # Append/Remove/Update processes data into treestore
        global process_search_text
        if len(self.piter_list) > 0:
            for i, j in updated_existing_proc_index:
                if processes_data_rows[i] != processes_data_rows_prev[j]:
                    for k in range(1, processes_data_rows_row_length):                            # Start from "1" in order to set first element (treeview row visibility data) as "True" in every loop.
                        if processes_data_rows_prev[j][k] != processes_data_rows[i][k]:
                            self.treestore.set_value(self.piter_list[j], k, processes_data_rows[i][k])
        if len(deleted_processes) > 0:
            for process in reversed(sorted(list(deleted_processes), key=int)):
                self.treestore.remove(self.piter_list[pid_list_prev.index(process)])
                self.piter_list.remove(self.piter_list[pid_list_prev.index(process)])
            self.on_searchentry_changed(self.searchentry)                                           # Update search results.
        if len(new_processes) > 0:
            for process in new_processes:
                if show_processes_as_tree == 1:
                    if ppid_list[pid_list.index(process)] == "0":                                 # Process ppid was set as "0" if it has no parent process. Process is set as tree root (this root has no relationship between root user) process if it has no ppid (parent process). Treeview tree indentation is first level for the tree root proceess.
                        self.piter_list.append(self.treestore.append(None, processes_data_rows[pid_list.index(process)]))
                    if ppid_list[pid_list.index(process)] != "0":
                        if show_processes_of_all_users == 1:                                      # Process appended under tree root process or another process if "Show processes as tree" option is preferred.
                            self.piter_list.append(self.treestore.append(self.piter_list[pid_list.index(ppid_list[pid_list.index(process)])], processes_data_rows[pid_list.index(process)]))
                        parent_process = ppid_list[pid_list.index(process)]                       # Define parent process of the process in order to avoid calculating it multiple times for faster processing.
                        if show_processes_of_all_users == 0 and parent_process not in pid_list:   # Process is appended into treeview as tree root process if "Show processes of all users" is not preferred and process ppid not in pid_list.
                            self.piter_list.append(self.treestore.append(None, processes_data_rows[pid_list.index(process)]))
                        if show_processes_of_all_users == 0 and parent_process in pid_list:       # Process is appended into treeview under tree root process or another process if "Show processes of all users" is preferred and process ppid is in pid_list.
                            self.piter_list.append(self.treestore.append(self.piter_list[pid_list.index(ppid_list[pid_list.index(process)])], processes_data_rows[pid_list.index(process)]))
                if show_processes_as_tree == 0:                                                   # All processes are appended into treeview as tree root process if "Show processes as tree" is not preferred. Thus processes are listed as list structure instead of tree structure.
                    self.piter_list.insert(pid_list.index(process), self.treestore.insert(None, pid_list.index(process), processes_data_rows[pid_list.index(process)]))
            self.on_searchentry_changed(self.searchentry)                                           # Update search results.

        if pid_list_prev == []:                                                                   # Expand all treeview rows (if treeview items are in tree structured, not list) if this is the first loop of the Processes tab. It expands treeview rows (and children) in all loops if this control is not made. "First loop" control is made by checking if pid_list_prev is empty.
            self.treeview.expand_all()

        pid_list_prev = pid_list
        processes_data_rows_prev = processes_data_rows
        show_processes_as_tree_prev = show_processes_as_tree
        processes_treeview_columns_shown_prev = processes_treeview_columns_shown
        processes_data_row_sorting_column_prev = processes_data_row_sorting_column
        processes_data_row_sorting_order_prev = processes_data_row_sorting_order
        processes_data_column_order_prev = processes_data_column_order
        processes_data_column_widths_prev = processes_data_column_widths

        self.processes_data_rows = processes_data_rows
        self.pid_list = pid_list
        self.number_of_logical_cores = number_of_logical_cores

        # Get max values of some performance data for setting cell background colors depending on relative performance data.
        global max_value_cpu_usage_list, max_value_memory_rss_list, max_value_memory_vms_list, max_value_memory_shared_list
        global max_value_disk_read_data_list, max_value_disk_write_data_list, max_value_disk_read_speed_list, max_value_disk_write_speed_list
        try:
            max_value_cpu_usage_list = max(cpu_usage_list)
        except ValueError:
            max_value_cpu_usage_list = 0
        try:
            max_value_memory_rss_list = max(memory_rss_list)
        except ValueError:
            max_value_memory_rss_list = 0
        try:
            max_value_memory_vms_list = max(memory_vms_list)
        except ValueError:
            max_value_memory_vms_list = 0
        try:
            max_value_memory_shared_list = max(memory_shared_list)
        except ValueError:
            max_value_memory_shared_list = 0
        try:
            max_value_disk_read_data_list = max(disk_read_data_list)
        except ValueError:
            max_value_disk_read_data_list = 0
        try:
            max_value_disk_write_data_list = max(disk_write_data_list)
        except ValueError:
            max_value_disk_write_data_list = 0
        try:
            max_value_disk_read_speed_list = max(disk_read_speed_list)
        except ValueError:
            max_value_disk_read_speed_list = 0
        try:
            max_value_disk_write_speed_list = max(disk_write_speed_list)
        except ValueError:
            max_value_disk_write_speed_list = 0

        # Show number of processes on the searchentry as placeholder text
        self.searchentry.props.placeholder_text = _tr("Search...") + "                    " + "(" + _tr("Processes") + ": " + str(len(username_list)) + ")"

        # Show/Hide treeview expander arrows. If "child rows" are not used and there is no need for these expanders (they would be shown as empty spaces in this situation).
        if show_processes_as_tree == 1:
            self.treeview.set_show_expanders(True)
        if show_processes_as_tree == 0:
            self.treeview.set_show_expanders(False)

        # Show/Hide treeview tree lines
        if Config.show_tree_lines == 1:
            self.treeview.set_enable_tree_lines(True)
        if Config.show_tree_lines == 0:
            self.treeview.set_enable_tree_lines(False)


    def on_column_title_clicked(self, widget):
        """
        Get and save column sorting order.
        """

        processes_data_row_sorting_column_title = widget.get_title()                              # Get column title which will be used for getting column number
        for data in processes_data_list:
            if data[1] == processes_data_row_sorting_column_title:
                Config.processes_data_row_sorting_column = data[0]                                # Get column number
        Config.processes_data_row_sorting_order = int(widget.get_sort_order())                    # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
        Config.config_save_func()


    def treeview_column_order_width_row_sorting(self):
        """
        Get and save column order/width, row sorting.
        """

        # Columns in the treeview are get one by one and appended into "processes_data_column_order". "processes_data_column_widths" list elements are modified for widths of every columns in the treeview. Length of these list are always same even if columns are removed, appended and column widths are changed. Only values of the elements (element indexes are always same with "processes_data") are changed if column order/widths are changed.
        processes_treeview_columns = self.treeview.get_columns()
        treeview_column_titles = []
        for column in processes_treeview_columns:
            treeview_column_titles.append(column.get_title())

        processes_data_column_order = [-1] * len(processes_data_list)
        processes_data_column_widths = [-1] * len(processes_data_list)

        processes_treeview_columns_last_index = len(processes_treeview_columns)-1

        for i, processes_data in enumerate(processes_data_list):
            for j, column_title in enumerate(treeview_column_titles):
                if column_title == processes_data[1]:
                    column_index = treeview_column_titles.index(processes_data[1])
                    processes_data_column_order[i] = column_index
                    if j != processes_treeview_columns_last_index:
                        processes_data_column_widths[i] = processes_treeview_columns[column_index].get_width()

        Config.processes_data_column_order = list(processes_data_column_order)
        Config.processes_data_column_widths = list(processes_data_column_widths)
        Config.config_save_func()


    def application_exec_icon_type_list(self):
        """
        Get application names, images and types (desktop_application or application).
        Process name will be searched in "application_exec_list" list and image/application type will be get.
        """

        application_exec_list = []
        application_icon_list = []
        application_type_list = []

        # Get  ".desktop" file names
        application_file_list = [file for file in os.listdir("/usr/share/applications/") if file.endswith(".desktop")]

        for application in application_file_list:

            # "encoding="utf-8"" is used for preventing "UnicodeDecodeError" errors during reading the file content if "C" locale is used.
            with open("/usr/share/applications/" + application, encoding="utf-8") as reader:
                application_file_content = reader.read()

            # Do not include application name or icon name if any of them is not found in the .desktop file.
            if "Exec=" not in application_file_content or "Icon=" not in application_file_content:
                continue

            # Get application exec data
            application_exec = application_file_content.split("Exec=", 1)[1].split("\n", 1)[0].split("/")[-1].split(" ")[0]
            # Splitting operation above may give "sh" as application name and this may cause confusion between "sh" process
            # and splitted application exec (for example: sh -c "gdebi-gtk %f"sh -c "gdebi-gtk %f").
            # This statement is used to avoid from this confusion.
            if application_exec == "sh":
                application_exec = application_file_content.split("Exec=", 1)[1].split("\n", 1)[0]

            # Get application icon name data
            application_icon = application_file_content.split("Icon=", 1)[1].split("\n", 1)[0]

            # Get "desktop_application/application" information
            if "NoDisplay=" in application_file_content:
                desktop_application_value = application_file_content.split("NoDisplay=", 1)[1].split("\n", 1)[0]
                if desktop_application_value == "true":
                    application_type = "application"
                if desktop_application_value == "false":
                    application_type = "desktop_application"
            else:
                application_type = "desktop_application"

            application_exec_list.append(application_exec)
            application_icon_list.append(application_icon)
            application_type_list.append(application_type)

        return application_exec_list, application_icon_list, application_type_list


# ----------------------------------- Processes - Treeview Cell Functions (defines functions for treeview cell for setting data precisions and/or data units) -----------------------------------
def cell_data_function_cpu_usage_percent(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{tree_model.get(iter, data)[0]:.{processes_cpu_precision}f} %')
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_cpu_usage_list)

def cell_data_function_memory_rss(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_memory_data_unit, processes_memory_data_precision))
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_memory_rss_list)

def cell_data_function_memory_vms(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_memory_data_unit, processes_memory_data_precision))
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_memory_vms_list)

def cell_data_function_memory_shared(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_memory_data_unit, processes_memory_data_precision))
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_memory_shared_list)

def cell_data_function_disk_read_data(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_disk_data_unit, processes_disk_data_precision))
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_disk_read_data_list)

def cell_data_function_disk_write_data(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', performance_data_unit_converter_func("data", "none", tree_model.get(iter, data)[0], processes_disk_data_unit, processes_disk_data_precision))
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_disk_write_data_list)

def cell_data_function_disk_read_speed(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{performance_data_unit_converter_func("speed", processes_disk_speed_bit, tree_model.get(iter, data)[0], processes_disk_data_unit, processes_disk_data_precision)}/s')
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_disk_read_speed_list)

def cell_data_function_disk_write_speed(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', f'{performance_data_unit_converter_func("speed", processes_disk_speed_bit, tree_model.get(iter, data)[0], processes_disk_data_unit, processes_disk_data_precision)}/s')
    value = tree_model.get(iter, data)[0]
    cell_backround_color(cell, value, max_value_disk_write_speed_list)

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


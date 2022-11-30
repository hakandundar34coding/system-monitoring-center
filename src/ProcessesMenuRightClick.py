#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
import os
import signal
import subprocess

from locale import gettext as _tr

from Config import Config
import Processes


class ProcessesMenuRightClick:

    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesMenuRightClick.ui")

        # Get GUI objects
        self.menu2101m = builder.get_object('menu2101m')
        self.menuitem2101m = builder.get_object('menuitem2101m')
        self.menuitem2102m = builder.get_object('menuitem2102m')
        self.menuitem2103m = builder.get_object('menuitem2103m')
        self.menuitem2104m = builder.get_object('menuitem2104m')
        self.menuitem2106m = builder.get_object('menuitem2106m')
        self.menuitem2107m = builder.get_object('menuitem2107m')
        self.menuitem2108m = builder.get_object('menuitem2108m')
        self.menuitem2109m = builder.get_object('menuitem2109m')
        self.radiomenuitem2101m = builder.get_object('radiomenuitem2101m')
        self.radiomenuitem2102m = builder.get_object('radiomenuitem2102m')
        self.radiomenuitem2103m = builder.get_object('radiomenuitem2103m')
        self.radiomenuitem2104m = builder.get_object('radiomenuitem2104m')
        self.radiomenuitem2105m = builder.get_object('radiomenuitem2105m')
        self.normalmenuitem2101m = builder.get_object('normalmenuitem2101m')

        # Connect GUI signals
        self.menuitem2101m.connect("activate", self.on_process_manage_menuitems_activate)
        self.menuitem2102m.connect("activate", self.on_process_manage_menuitems_activate)
        self.menuitem2103m.connect("activate", self.on_process_manage_menuitems_activate)
        self.menuitem2104m.connect("activate", self.on_process_manage_menuitems_activate)
        self.menuitem2106m.connect("activate", self.on_menuitem2106m_activate)
        self.menuitem2107m.connect("activate", self.on_expand_collapse_menuitems_activate)
        self.menuitem2108m.connect("activate", self.on_expand_collapse_menuitems_activate)
        self.normalmenuitem2101m.connect("activate", self.on_normalmenuitem2101m_activate)
        # Connect some of the GUI signals by defining signal handler IDs for them to be able to block them during setting radiomenuitems.
        self.radiomenuitem2101m_handler_id = self.radiomenuitem2101m.connect("activate", self.on_process_priority_radioitems_activate)
        self.radiomenuitem2102m_handler_id = self.radiomenuitem2102m.connect("activate", self.on_process_priority_radioitems_activate)
        self.radiomenuitem2103m_handler_id = self.radiomenuitem2103m.connect("activate", self.on_process_priority_radioitems_activate)
        self.radiomenuitem2104m_handler_id = self.radiomenuitem2104m.connect("activate", self.on_process_priority_radioitems_activate)
        self.radiomenuitem2105m_handler_id = self.radiomenuitem2105m.connect("activate", self.on_process_priority_radioitems_activate)


    # ----------------------- Called for stopping, continuing, ending process -----------------------
    def on_process_manage_menuitems_activate(self, widget):

        # Get right clicked process pid and name.
        selected_process_pid = Processes.selected_process_pid
        selected_process_name = Processes.processes_data_rows[Processes.pid_list.index(selected_process_pid)][2]

        # Define signal and command for the process by checking the clicked menu item (Stop Process).
        if widget == self.menuitem2101m:
            process_command = ["kill", "-19", selected_process_pid]
            process_command_pkexec = ["pkexec", "kill", "-19", selected_process_pid]

        # Define signal and command for the process by checking the clicked menu item (Continue Process).
        if widget == self.menuitem2102m:
            process_command = ["kill", "-18", selected_process_pid]
            process_command_pkexec = ["pkexec", "kill", "-18", selected_process_pid]

        # Define signal, command and dialog message text for the process by checking the clicked menu item (Terminate Process).
        if widget == self.menuitem2103m:
            process_command = ["kill", "-15", selected_process_pid]
            process_command_pkexec = ["pkexec", "kill", "-15", selected_process_pid]
            process_dialog_message = _tr("Do you want to end this process?")

        # Define signal, command and dialog message text for the process by checking the clicked menu item (Kill Process).
        if widget == self.menuitem2104m:
            process_command = ["kill", "-9", selected_process_pid]
            process_command_pkexec = ["pkexec", "kill", "-9", selected_process_pid]
            process_dialog_message = _tr("Do you want to end this process immediately?")

        # Show warning dialog if process is tried to be ended.
        if Config.warn_before_stopping_processes == 1 and (widget == self.menuitem2103m or widget == self.menuitem2104m):
            self.processes_end_process_warning_dialog(process_dialog_message, selected_process_name, selected_process_pid)
            if self.dialog2101_response != Gtk.ResponseType.YES:
                return

        if Config.environment_type == "flatpak":
            process_command = ["flatpak-spawn", "--host"] + process_command
            process_command_pkexec = ["flatpak-spawn", "--host"] + process_command_pkexec

        # Try to end the process without using root privileges.
        try:
            (subprocess.check_output(process_command, stderr=subprocess.STDOUT, shell=False)).decode()
        except subprocess.CalledProcessError:
            # End the process if root privileges are given.
            try:
                # Command output is not printed by using "stderr=subprocess.STDOUT".
                (subprocess.check_output(process_command_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
            # This "try-catch" is used in order to prevent errors if wrong password is used or polkit dialog is closed by user.
            except subprocess.CalledProcessError:
                pass


    # ----------------------- Called for changing priority (nice value) of process -----------------------
    def on_process_priority_radioitems_activate(self, widget):

        # Stop running the function if caller widget is not active in order to avoid calling this function twice on every priority change by using radiomenubuttons. Because activated and deactivated widgets call this function.
        if widget.get_active() != True:
            return

        # Get right clicked process pid and name.
        selected_process_pid = Processes.selected_process_pid

        # Define commands for the process by checking the clicked menu item (Very High).
        if self.radiomenuitem2101m.get_active() == True:
            priority_command = ["renice", "-n", "-20", "-p", selected_process_pid]
            priority_command_pkexec = ["pkexec", "renice", "-n", "-20", "-p", selected_process_pid]

        # Define commands for the process by checking the clicked menu item (High).
        if self.radiomenuitem2102m.get_active() == True:
            priority_command = ["renice", "-n", "-10", "-p", selected_process_pid]
            priority_command_pkexec = ["pkexec", "renice", "-n", "-10", "-p", selected_process_pid]

        # Define commands for the process by checking the clicked menu item (Normal).
        if self.radiomenuitem2103m.get_active() == True:
            priority_command = ["renice", "-n", "-0", "-p", selected_process_pid]
            priority_command_pkexec = ["pkexec", "renice", "-n", "0", "-p", selected_process_pid]

        # Define commands for the process by checking the clicked menu item (Low).
        if self.radiomenuitem2104m.get_active() == True:
            priority_command = ["renice", "-n", "10", "-p", selected_process_pid]
            priority_command_pkexec = ["pkexec", "renice", "-n", "10", "-p", selected_process_pid]

        # Define commands for the process by checking the clicked menu item (Very Low).
        if self.radiomenuitem2105m.get_active() == True:
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


    # ----------------------- Called for showing Custom Priority Window -----------------------
    def on_normalmenuitem2101m_activate(self, widget):

        from ProcessesCustomPriorityGUI import ProcessesCustomPriorityGUI
        ProcessesCustomPriorityGUI.window2101w2.show()


    # ----------------------- Called for showing Process Details Window -----------------------
    def on_menuitem2106m_activate(self, widget):

        """from ProcessesDetails import ProcessesDetails
        ProcessesDetails.window2101w.show()"""

        import ProcessesDetails
        ProcessesDetails.processes_details_show_process_details()


    # ----------------------- Called for expanding/collapsing items when "Expand All/Collapse All" menuitems are clicked -----------------------
    def on_expand_collapse_menuitems_activate(self, widget):

        if widget == self.menuitem2107m:
            Processes.treeview2101.expand_all()

        if widget == self.menuitem2108m:
            Processes.treeview2101.collapse_all()


    # ----------------------- Called for setting priority of the process on the right click menu -----------------------
    def processes_add_remove_expand_collapse_menuitems_func(self):

        if Config.show_processes_as_tree == 1:
            self.menuitem2107m.show()
            self.menuitem2108m.show()
            self.menuitem2109m.show()

        if Config.show_processes_as_tree == 0:
            self.menuitem2107m.hide()
            self.menuitem2108m.hide()
            self.menuitem2109m.hide()


    # ----------------------- Called for setting priority of the process on the right click menu -----------------------
    def processes_select_process_nice_option_func(self):

        # Get right clicked process pid and name.
        selected_process_pid = Processes.selected_process_pid

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

        # Pause event signals and make changes on radiobutton selections by using the process priority.
        with self.radiomenuitem2101m.handler_block(self.radiomenuitem2101m_handler_id) as p1, self.radiomenuitem2102m.handler_block(self.radiomenuitem2102m_handler_id) as p2, self.radiomenuitem2103m.handler_block(self.radiomenuitem2103m_handler_id) as p3, self.radiomenuitem2104m.handler_block(self.radiomenuitem2104m_handler_id) as p4, self.radiomenuitem2105m.handler_block(self.radiomenuitem2105m_handler_id) as p5:
            if selected_process_nice <= -11 and selected_process_nice >= -20:
                self.radiomenuitem2101m.set_active(True)
            if selected_process_nice < 0 and selected_process_nice > -11:
                self.radiomenuitem2102m.set_active(True)
            if selected_process_nice == 0:
                self.radiomenuitem2103m.set_active(True)
            if selected_process_nice < 11 and selected_process_nice > 0:
                self.radiomenuitem2104m.set_active(True)
            if selected_process_nice <= 19 and selected_process_nice >= 11:
                self.radiomenuitem2105m.set_active(True)


    # ----------------------------------- Processes - Processes Terminate Process Warning Dialog Function -----------------------------------
    def processes_end_process_warning_dialog(self, process_dialog_message, process_name, process_pid):

        dialog2101 = Gtk.MessageDialog(transient_for=Processes.grid2101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.YES_NO, text=process_dialog_message)
        dialog2101.format_secondary_text(process_name + " (" + "PID" + ": " + str(process_pid) + ")")
        self.dialog2101_response = dialog2101.run()
        dialog2101.destroy()


ProcessesMenuRightClick = ProcessesMenuRightClick()


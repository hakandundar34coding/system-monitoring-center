#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import subprocess

from Config import Config
import Processes
from ProcessesMenuRightClick import ProcessesMenuRightClick


class ProcessesCustomPriorityGUI:

    def __init__(self):

        # Get GUI objects from file
        builder2101w2 = Gtk.Builder()
        builder2101w2.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesCustomPriorityWindow.ui")

        # Get GUI objects
        self.window2101w2 = builder2101w2.get_object('window2101w2')
        self.scale2101w2 = builder2101w2.get_object('scale2101w2')
        self.adjustment2101w2 = builder2101w2.get_object('adjustment2101w2')
        self.label2101w2 = builder2101w2.get_object('label2101w2')
        self.button2101w2 = builder2101w2.get_object('button2101w2')
        self.button2102w2 = builder2101w2.get_object('button2102w2')

        # Connect GUI signals
        self.window2101w2.connect("delete-event", self.on_window2101w2_delete_event)
        self.window2101w2.connect("show", self.on_window2101w2_show)
        self.button2101w2.connect("clicked", self.on_button2101w2_clicked)
        self.button2102w2.connect("clicked", self.on_button2102w2_clicked)


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window2101w2_delete_event(self, widget, event):

        self.window2101w2.hide()
        return True


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window2101w2_show(self, widget):

        # Get right clicked process pid and name.
        selected_process_pid = Processes.selected_process_pid
        selected_process_name = Processes.processes_data_rows[Processes.pid_list.index(selected_process_pid)][2]

        # Get process stat file path.
        selected_process_stat_file = "/proc/" + selected_process_pid + "/stat"

        # Get priority (nice value) of the process.
        if Config.environment_type == "flatpak":
            cat_output = (subprocess.run(["flatpak-spawn", "--host", "cat", selected_process_stat_file], shell=False, stdout=subprocess.PIPE)).stdout.decode().strip()
        else:
            cat_output = (subprocess.run(["cat", selected_process_stat_file], shell=False, stdout=subprocess.PIPE)).stdout.decode().strip()
        # Process may be ended just after pid_list is generated. "cat" command output is get as "" in this situation.
        if cat_output != "":
            selected_process_nice = int(cat_output.split()[-34])
        else:
            return

        # Set adjustment widget by using process priority (nice value).
        self.adjustment2101w2.configure(selected_process_nice, -20, 19, 1, 0, 0)

        # Show process name and PID on a label.
        self.label2101w2.set_text(f'{selected_process_name} - (PID: {selected_process_pid})')


    # ----------------------- "Cancel" Button -----------------------
    def on_button2101w2_clicked(self, widget):

        self.window2101w2.hide()


    # ----------------------- "Apply" Button -----------------------
    def on_button2102w2_clicked(self, widget):

        # Get right clicked process pid and name.
        selected_process_pid = Processes.selected_process_pid

        # Get new priority (nice value) of the process.
        selected_process_nice = str(int(self.adjustment2101w2.get_value()))

        # Define commands for the process.
        priority_command = ["renice", "-n", selected_process_nice, "-p", selected_process_pid]
        priority_command_pkexec = ["pkexec", "renice", "-n", selected_process_nice, "-p", selected_process_pid]

        if Config.environment_type == "flatpak":
            priority_command = ["flatpak-spawn", "--host"] + priority_command
            priority_command_pkexec = ["flatpak-spawn", "--host"] + priority_command_pkexec

        # Try to change priority (nice value) of the process.
        try:
            # Command output is not printed by using "stderr=subprocess.STDOUT".
            (subprocess.check_output(priority_command, stderr=subprocess.STDOUT, shell=False)).decode()
        except subprocess.CalledProcessError:
            # Try to change priority (nice value) of the process if root privileges are required.
            try:
                (subprocess.check_output(priority_command_pkexec, stderr=subprocess.STDOUT, shell=False)).decode()
            # This "try-catch" is used in order to prevent errors if wrong password is used or polkit dialog is closed by user.
            except subprocess.CalledProcessError:
                return

        self.window2101w2.hide()


ProcessesCustomPriorityGUI = ProcessesCustomPriorityGUI()


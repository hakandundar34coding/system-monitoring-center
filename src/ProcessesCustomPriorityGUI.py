#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import subprocess

import Processes
from ProcessesMenuRightClick import ProcessesMenuRightClick


# Define class
class ProcessesCustomPriorityGUI:

    # ----------------------- Always called when object is generated -----------------------
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

        # Get priority (nice value) of the process.
        try:
            with open("/proc/" + selected_process_pid + "/stat") as reader:
                selected_process_nice = int(reader.read().split()[-34])
        # Process may be ended just after pid_list is generated. "try-catch" is used for avoiding errors in this situation.
        except FileNotFoundError:
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

        # Try to change priority (nice value) of the process.
        try:
            # Command output is not printed by using "stderr=subprocess.STDOUT".
            (subprocess.check_output(["renice", "-n", selected_process_nice, "-p", selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
        except subprocess.CalledProcessError:
            # Try to change priority (nice value) of the process if root privileges are required.
            try:
                (subprocess.check_output(["pkexec", "renice", "-n", selected_process_nice, "-p", selected_process_pid], stderr=subprocess.STDOUT, shell=False)).decode()
            # This "try-catch" is used in order to prevent errors if wrong password is used or polkit dialog is closed by user.
            except subprocess.CalledProcessError:
                return

        self.window2101w2.hide()


# Generate object
ProcessesCustomPriorityGUI = ProcessesCustomPriorityGUI()


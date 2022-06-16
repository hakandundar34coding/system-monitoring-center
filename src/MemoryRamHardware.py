#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import subprocess

from locale import gettext as _tr


# Define class
class MemoryRamHardware:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MemoryRamHardwareWindow.ui")

        # Get GUI objects
        self.window1201w = builder.get_object('window1201w')
        self.label1201w = builder.get_object('label1201w')

        # Connect GUI signals
        self.window1201w.connect("delete-event", self.on_window1201w_delete_event)
        self.window1201w.connect("show", self.on_window1201w_show)


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window1201w_delete_event(self, widget, event):

        widget.hide()
        return True


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window1201w_show(self, widget):

        # Reset label text when window is shown.
        self.label1201w.set_text("-")
        # Set label text for showing RAM hardware information.
        try:
            self.label1201w.set_text(self.memory_ram_hardware_information_text)
        # "try-except" is used in order to avoid errors if user closed polkit dialog without entering password.
        except AttributeError:
            pass


    # ----------------------- Called for getting RAM hardware information -----------------------
    def memory_ram_hardware_information_get_func(self):

        # Set initial value of "memory_ram_hardware_information_text". Hardware information will be appended to this string.
        # This value will also be used for preventing showing RAM hardware Information window if user closes polkit window without entering password.
        self.memory_ram_hardware_information_text = ""

        # "sudo" has to be used for using "pkexec" to run "dmidecode" with root privileges.
        try:
            dmidecode_output = (subprocess.check_output(["pkexec", "sudo", "dmidecode", "-t", "16,17"], stderr=subprocess.STDOUT, shell=False)).decode().strip()
        except Exception:
            self.window1201w.hide()
            return

        dmidecode_output_lines = dmidecode_output.split("\n")

        # Initial value of "maximum_capacity". This value will be used if value could not be get.
        maximum_capacity = "-"
        number_of_devices = "-"

        # Perform the following operations if "Physical Memory Array" is found in "dmidecode_output" output. This information may not be available on some systems.
        if "Physical Memory Array" in dmidecode_output:
            for line in dmidecode_output_lines:
                line = line.strip()
                if line.startswith("Maximum Capacity:"):
                    maximum_capacity = line.split(":")[1].strip()
                    continue
                if line.startswith("Number Of Devices:"):
                    number_of_devices = line.split(":")[1].strip()
                    continue
        self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + _tr("Maximum Capacity") + " :    " + maximum_capacity
        self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Number Of Devices") + " :    " + number_of_devices + "\n"

        # Perform the following operations if "Memory Device" is found in "dmidecode_output" output. This information may not be available on some systems.
        if "Memory Device" in dmidecode_output:
            data_per_slot = dmidecode_output.split("Memory Device")
            # First element in this list is not information of memory device and it is deleted.
            del data_per_slot[0]
            for data in data_per_slot:
                data_lines = data.split("\n")
                memory_size = "-"
                memory_form_factor = "-"
                memory_locator = "-"
                memory_bank_locator = "-"
                memory_type = "-"
                memory_speed = "-"
                memory_manufacturer = "-"
                for line in data_lines:
                    line = line.strip()
                    if  line.startswith("Size:"):
                        memory_size = line.split(":")[1].strip()
                        continue
                    if line.startswith("Form Factor:"):
                        memory_form_factor = line.split(":")[1].strip()
                        continue
                    if line.startswith("Locator:"):
                        memory_locator = line.split(":")[1].strip()
                        continue
                    if line.startswith("Bank Locator:"):
                        memory_bank_locator = line.split(":")[1].strip()
                        continue
                    if line.startswith("Type:"):
                        memory_type = line.split(":")[1].strip()
                        continue
                    if line.startswith("Speed:"):
                        memory_speed = line.split(":")[1].strip()
                        continue
                    if line.startswith("Manufacturer:"):
                        memory_manufacturer = line.split(":")[1].strip()
                        continue
                self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"
                self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Capacity") + " :    " + memory_size
                self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Type") + " :    " + memory_type
                self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Speed/Frequency") + " :    " + memory_speed
                self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Manufacturer") + " :    " + memory_manufacturer
                self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Form Factor") + " :    " + memory_form_factor
                self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Locator") + " :    " + memory_locator
                self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Bank Locator") + " :    " + memory_bank_locator
                self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n"

        # Perform the following operations if "Memory Device" is not found in "dmidecode_output" output. This information may not be available on some systems.
        if "Memory Device" not in dmidecode_output:
            memory_size = "-"
            memory_form_factor = "-"
            memory_locator = "-"
            memory_bank_locator = "-"
            memory_type = "-"
            memory_speed = "-"
            memory_manufacturer = "-"

            self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"
            self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Capacity") + " :    " + memory_size
            self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Type") + " :    " + memory_type
            self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Speed/Frequency") + " :    " + memory_speed
            self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Manufacturer") + " :    " + memory_manufacturer
            self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Form Factor") + " :    " + memory_form_factor
            self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Locator") + " :    " + memory_locator
            self.memory_ram_hardware_information_text = self.memory_ram_hardware_information_text + "\n" + _tr("Bank Locator") + " :    " + memory_bank_locator


# Generate object
MemoryRamHardware = MemoryRamHardware()


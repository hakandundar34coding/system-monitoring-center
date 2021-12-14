#!/usr/bin/env python3

# ----------------------------------- RAM - RAM Hardware Information Window GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def ram_hardware_information_import_func():

    global Gtk, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os
    import subprocess


    global MainGUI
    from . import MainGUI


    # Import locale and gettext modules for defining translation texts which will be recognized by gettext application (will be run by programmer externally) and exported into a ".pot" file. 
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    import locale
    from locale import gettext as _tr

    # Define contstants for language translation support
    global application_name
    application_name = "system-monitoring-center"
    translation_files_path = "/usr/share/locale"
    system_current_language = os.environ.get("LANG")

    # Define functions for language translation support
    locale.bindtextdomain(application_name, translation_files_path)
    locale.textdomain(application_name)
    locale.setlocale(locale.LC_ALL, system_current_language)


# ----------------------------------- RAM - RAM Hardware Information Window GUI Function (the code of this module in order to avoid running them during module import and defines GUI objects and functions/signals) -----------------------------------
def ram_hardware_information_gui_func():

    global builder, window1201w
    global label1201w, button1201w


    # RAM Hardware Information window GUI objects - get
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/ui/RamHardwareWindow.ui")

    window1201w = builder.get_object('window1201w')
    label1201w = builder.get_object('label1201w')
    button1201w = builder.get_object('button1201w')


    # RAM Hardware Information window GUI functions
    def on_window1201w_delete_event(widget, event):
        window1201w.hide()
        return True

    def on_window1201w_show(widget):
        label1201w.set_text("-")                                                              # Reset label text when window is shown.
        global memory_hardware_information_text
        try:                                                                                  # "try-except" is used in order to avoid errors if user closed polkit dialog without entering password. Because "memory_hardware_information_text" string will not be defined and will not be get in this situation.
            label1201w.set_text(memory_hardware_information_text)                             # Set label text for showing RAM hardware information.
        except NameError:
            pass

    def on_button1201w_clicked(widget):                                                       # "Close" button
        window1201w.hide()


    # RAM Hardware Information window GUI functions - connect
    window1201w.connect("delete-event", on_window1201w_delete_event)
    window1201w.connect("show", on_window1201w_show)
    button1201w.connect("clicked", on_button1201w_clicked)


# ----------------------------------- RAM - RAM Hardware Information Get Function (gets RAM hardware information) -----------------------------------
def ram_hardware_information_get_func():

    ram_hardware_information_text_list = [_tr("Unknown"), _tr("None")]                        # This list is defined in order to make some command output strings to be translated into other languages.

    global memory_hardware_information_text                                                   # This value will also be used for preventing showing RAM hardware Information window if user closes polkit window without entering password.
    memory_hardware_information_text = ""                                                     # Set initial value of "memory_hardware_information_text". Hardware information will be appended to this string.

    try:
        dmidecode_output = (subprocess.check_output(["pkexec", "sudo", "dmidecode", "-t", "16,17"], stderr=subprocess.STDOUT, shell=False)).decode().strip()    # "sudo" has to be used for using "pkexec" to run "dmidecode" with root privileges.
    except:
        window1201w.hide()
        ram_hardware_information_root_privileges_warning_dialog()
        return

    dmidecode_output_lines = dmidecode_output.split("\n")

    maximum_capacity = "-"                                                                    # Initial value of "maximum_capacity". This value will be used if value could not be get.
    number_of_devices = "-"

    if "Physical Memory Array" in dmidecode_output:                                           # Perform the following operations if "Physical Memory Array" is found in "dmidecode_output" output. This information may not be available on some systems.
        for line in dmidecode_output_lines:
            line = line.strip()
            if line.startswith("Maximum Capacity:"):
                maximum_capacity = line.split(":")[1].strip()
                continue
            if line.startswith("Number Of Devices:"):
                number_of_devices = line.split(":")[1].strip()
                continue
    memory_hardware_information_text = memory_hardware_information_text + _tr("Maximum Capacity") + " :    " + maximum_capacity
    memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Number Of Devices") + " :    " + number_of_devices + "\n"

    if "Memory Device" in dmidecode_output:                                                   # Perform the following operations if "Memory Device" is found in "dmidecode_output" output. This information may not be available on some systems.
        data_per_slot = dmidecode_output.split("Memory Device")
        del data_per_slot[0]                                                                  # First element in this list is not information of memory device and it is deleted.
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
            memory_hardware_information_text = memory_hardware_information_text + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"
            memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Capacity") + " :    " + memory_size
            memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Type") + " :    " + memory_type
            memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Speed/Frequency") + " :    " + memory_speed
            memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Manufacturer") + " :    " + memory_manufacturer
            memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Form Factor") + " :    " + memory_form_factor
            memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Locator") + " :    " + memory_locator
            memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Bank Locator") + " :    " + memory_bank_locator
            memory_hardware_information_text = memory_hardware_information_text + "\n"

    if "Memory Device" not in dmidecode_output:                                               # Perform the following operations if "Memory Device" is not found in "dmidecode_output" output. This information may not be available on some systems.
        memory_size = "-"
        memory_form_factor = "-"
        memory_locator = "-"
        memory_bank_locator = "-"
        memory_type = "-"
        memory_speed = "-"
        memory_manufacturer = "-"

        memory_hardware_information_text = memory_hardware_information_text + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"
        memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Capacity") + " :    " + memory_size
        memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Type") + " :    " + memory_type
        memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Speed") + " :    " + memory_speed
        memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Manufacturer") + " :    " + memory_manufacturer
        memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Form Factor") + " :    " + memory_form_factor
        memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Locator") + " :    " + memory_locator
        memory_hardware_information_text = memory_hardware_information_text + "\n" + _tr("Bank Locator") + " :    " + memory_bank_locator


# ----------------------------------- RAM - RAM Hardware Information Root Privileges Warning Dialog Function (shows a warning dialog when an output text is obtained during disk renaming actions) -----------------------------------
def ram_hardware_information_root_privileges_warning_dialog():

    warning_dialog1201w = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Access Denied"), )
    warning_dialog1201w.format_secondary_text(_tr("Root privileges are needed for viewing RAM hardware information."))
    global warning_dialog1201w_response
    warning_dialog1201w_response = warning_dialog1201w.run()
    warning_dialog1201w.destroy()


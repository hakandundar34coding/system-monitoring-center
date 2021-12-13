#!/usr/bin/env python3

# ----------------------------------- Services - Services Details Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def services_details_import_func():

    global Gtk, GLib, os, Thread, subprocess, time, datetime

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    import os
    from threading import Thread
    import subprocess
    import time
    from datetime import datetime


    global Config, Services, MainGUI
    from . import Config, Services, MainGUI


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


# ----------------------------------- Services - Services Details Window GUI Function (the code of this module in order to avoid running them during module import and defines "Services Details" window GUI objects and functions/signals) -----------------------------------
def services_details_gui_function():

    # Services Details window GUI objects
    global builder6101w, window6101w, notebook6101w
    global label6101w, label6102w, label6103w, label6104w, label6105w, label6106w, label6107w, label6108w, label6109w, label6110w
    global label6111w, label6112w, label6113w, label6114w, label6115w, label6116w, label6117w, label6118w, label6119w, label6120w
    global label6121w, label6122w


    # Services Details window GUI objects - get
    builder6101w = Gtk.Builder()
    builder6101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ServicesDetailsWindow.ui")

    window6101w = builder6101w.get_object('window6101w')

    notebook6101w = builder6101w.get_object('notebook6101w')

    # Service Details window "General" tab GUI objects
    label6101w = builder6101w.get_object('label6101w')
    label6102w = builder6101w.get_object('label6102w')
    label6103w = builder6101w.get_object('label6103w')
    label6104w = builder6101w.get_object('label6104w')
    label6105w = builder6101w.get_object('label6105w')
    label6106w = builder6101w.get_object('label6106w')
    label6107w = builder6101w.get_object('label6107w')
    label6108w = builder6101w.get_object('label6108w')
    label6109w = builder6101w.get_object('label6109w')
    label6110w = builder6101w.get_object('label6110w')
    label6111w = builder6101w.get_object('label6111w')
    label6112w = builder6101w.get_object('label6112w')
    label6113w = builder6101w.get_object('label6113w')
    label6114w = builder6101w.get_object('label6114w')
    label6115w = builder6101w.get_object('label6115w')
    label6116w = builder6101w.get_object('label6116w')
    label6117w = builder6101w.get_object('label6117w')
    label6118w = builder6101w.get_object('label6118w')

    # Service Details window "Dependencies" tab GUI objects
    label6119w = builder6101w.get_object('label6119w')
    label6120w = builder6101w.get_object('label6120w')
    label6121w = builder6101w.get_object('label6121w')
    label6122w = builder6101w.get_object('label6122w')


    # Services Details window GUI functions
    def on_window6101w_delete_event(widget, event):
        window6101w.hide()
        return True

    def on_window6101w_show(widget):
        services_details_gui_reset_function()                                                 # Call this function in order to reset Services Details window. Data from previous service remains visible (for a short time) until getting and showing new service data if window is closed and opened for an another service. Also last selected tab remains same because window is made hidden when close button is clicked.


    # Services Details window GUI functions - connect
    window6101w.connect("delete-event", on_window6101w_delete_event)
    window6101w.connect("show", on_window6101w_show)


# ----------------------------------- Services - Services Details Window GUI Reset Function (resets Services Details window) -----------------------------------
def services_details_gui_reset_function():

    notebook6101w.set_current_page(0)                                                          # Set fist page (Summary tab) of the notebook
    label6101w.set_text("--")
    label6102w.set_text("--")
    label6103w.set_text("--")
    label6104w.set_text("--")
    label6105w.set_text("--")
    label6106w.set_text("--")
    label6107w.set_text("--")
    label6108w.set_text("--")
    label6109w.set_text("--")
    label6110w.set_text("--")
    label6111w.set_text("--")
    label6112w.set_text("--")
    label6113w.set_text("--")
    label6114w.set_text("--")
    label6115w.set_text("--")
    label6116w.set_text("--")
    label6117w.set_text("--")
    label6118w.set_text("--")
    label6119w.set_text("--")
    label6120w.set_text("--")
    label6121w.set_text("--")
    label6122w.set_text("--")


# # ----------------------------------- Services - Services Details Tab Switch Control Function (controls if tab is switched and updates data on the last opened tab immediately without waiting end of the update interval. Signals of notebook for tab switching is not useful because it performs the action and after that it switches the tab. Data updating function does not recognizes tab switch due to this reason.) -----------------------------------
# def services_details_tab_switch_control_func():
# 
#     global previous_page
#     if 'previous_page' not in globals():                                                      # For avoiding errors in the first loop of the control
#         previous_page = None
#         current_page = None
#     current_page = notebook6101w.get_current_page()
#     if current_page != previous_page and previous_page != None:                               # Check if tab is switched
#         ServicesDetails.service_details_foreground_func()                                     # Update the data on the tab
#     previous_page = current_page
#     if window6101w.get_visible() == True:
#         GLib.timeout_add(200, services_details_tab_switch_control_func)                       # Check is performed in every 200 ms which is small enough for immediate update and not very frequent for avoiding high CPU usages.


# ----------------------------------- Services - Services Details Function (the code of this module in order to avoid running them during module import and defines "Services" tab GUI objects and functions/signals) -----------------------------------
def services_details_initial_func():

    global selected_service_name
    selected_service_name = Services.selected_service_name
    services_define_data_unit_converter_variables_func()                                      # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    # Get system boot time (will be used for appending to process start times to get process start times as date time.)
    global system_boot_time
    with open("/proc/stat") as reader:
        stat_lines = reader.read().split("\n")
    for line in stat_lines:
        if "btime " in line:
            system_boot_time = int(line.split()[1].strip())

    service_state_list = [_tr("Enabled"), _tr("Disabled"), _tr("Masked"), _tr("Unmasked"), _tr("Static"), _tr("Generated"), _tr("Enabled-runtime"), _tr("Indirect"), _tr("Active"), _tr("Inactive"), _tr("Loaded"), _tr("Dead"), _tr("Exited"), _tr("Running")]    # This list is defined in order to make English service state names to be translated into other languages. String names are capitalized here as they are capitalized in the code by using ".capitalize()" in order to use translated strings.
    services_other_text_list = [_tr("Yes"), _tr("No")]                                        # This list is defined in order to make English service information to be translated into other languages.


# ----------------------------------- Services - Services Details Foreground Function (updates the service data on the "Services Details" window) -----------------------------------
def services_details_foreground_func():

    services_ram_swap_data_precision = Config.services_ram_swap_data_precision
    services_ram_swap_data_unit = Config.services_ram_swap_data_unit

    systemctl_show_lines = (subprocess.check_output(["systemctl", "show", selected_service_name], shell=False)).decode().strip().split("\n")

    selected_service_type = "-"                                                               # Initial value of "selected_service_type" variable. This value will be used if "selected_service_type" could not be detected.
    selected_service_main_pid = "-"
    selected_service_control_pid = "-"
    selected_service_exec_main_start_times_stamp_monotonic = "-"
    selected_service_exec_main_exit_times_stamp_monotonic ="-"
    selected_service_exec_main_pid = "-"
    selected_service_memory_current = "-"
    selected_service_requires = "-"
    selected_service_conflicts = "-"
    selected_service_after = "-"
    selected_service_before = "-"
    selected_service_triggered_by = "-"
    selected_service_documentation = "-"
    selected_service_description = "-"
    selected_service_active_state = "-"
    selected_service_load_state = "-"
    selected_service_sub_state = "-"
    selected_service_fragment_path = "-"
    selected_service_unit_file_state = "-"
    selected_service_unit_file_preset = "-"
    selected_service_can_start = "-"
    selected_service_can_stop = "-"
    selected_service_can_reload = "-"

    for line in systemctl_show_lines:
        if "Type=" in line:
            selected_service_type = _tr(line.split("=")[1].capitalize())
            continue                                                                          # Skip to next loop if searched line ("Type=") is found in order to avoid redundant line search.
        if "MainPID=" in line:
            selected_service_main_pid = line.split("=")[1]
            continue
        if "ControlPID=" in line:
            selected_service_control_pid = line.split("=")[1]
            continue
        if "ExecMainStartTimestampMonotonic=" in line:
            line_split = line.split("=")[1]
            if line_split != "0":
                selected_service_exec_main_start_times_stamp_monotonic = int(line.split("=")[1])/1000000 + system_boot_time    # Time is read from the service file (in microseconds), divided by 1000000 in order to obtain time in seconds and appended to system boot time for getting service start time. Because time data is get as "elapsed time after system boot" from the file.
                selected_service_exec_main_start_times_stamp_monotonic = datetime.fromtimestamp(selected_service_exec_main_start_times_stamp_monotonic).strftime("%d.%m.%Y %H:%M:%S")
            if line_split == "0":
                selected_service_exec_main_start_times_stamp_monotonic = "-"
            continue
        if "ExecMainExitTimestampMonotonic=" in line:
            line_split = line.split("=")[1]
            if line_split != "0":
                selected_service_exec_main_exit_times_stamp_monotonic = int(line.split("=")[1])/1000000 + system_boot_time    # Time is read from the service file (in microseconds), divided by 1000000 in order to obtain time in seconds and appended to system boot time for getting service start time. Because time data is get as "elapsed time after system boot" from the file.
                selected_service_exec_main_exit_times_stamp_monotonic = datetime.fromtimestamp(selected_service_exec_main_exit_times_stamp_monotonic).strftime("%d.%m.%Y %H:%M:%S")
            if line_split == "0":
                selected_service_exec_main_exit_times_stamp_monotonic = "-"
            continue
        if "ExecMainPID=" in line:
            selected_service_exec_main_pid = line.split("=")[1]
            continue
        if "MemoryCurrent=" in line:
            selected_service_memory_current = line.split("=")[1]
            if selected_service_memory_current == "-" or selected_service_memory_current == "[not set]":
                selected_service_memory_current = "-"
            else:
                try:
                    selected_service_memory_current = f'{services_details_data_unit_converter_func(int(selected_service_memory_current), services_ram_swap_data_unit, services_ram_swap_data_precision)}'
                except:
                    selected_service_memory_current = "-"
            continue
        if "Requires=" in line:
            selected_service_requires = line.split("=")[1].split()
            continue
        if "Conflicts=" in line:
            selected_service_conflicts = line.split("=")[1].split()
            continue
        if "After=" in line:
            selected_service_after = line.split("=")[1].split()
            continue
        if "Before=" in line:
            selected_service_before = line.split("=")[1].split()
            continue
        if "TriggeredBy=" in line:
            selected_service_triggered_by = line.split("=")[1]
            continue
        if "Documentation=" in line:
            selected_service_documentation = line.split("=")[1].split()
            # Convert string into multi-line string if there are more than one documentation information.
            selected_service_documentation_scratch = []
            for documentation in selected_service_documentation:
                selected_service_documentation_scratch.append(documentation.strip('"'))
            selected_service_documentation = selected_service_documentation_scratch
            continue
        if "Description=" in line:
            selected_service_description = line.split("=")[1]
            continue
        if "ActiveState=" in line:
            selected_service_active_state = _tr(line.split("=")[1].capitalize())              # "_tr([value])" is used for using translated string.
            continue
        if "LoadState=" in line:
            selected_service_load_state = _tr(line.split("=")[1].capitalize())                # "_tr([value])" is used for using translated string.
            continue
        if "SubState=" in line:
            selected_service_sub_state = _tr(line.split("=")[1].capitalize())                 # "_tr([value])" is used for using translated string.
            continue
        if "FragmentPath=" in line:
            selected_service_fragment_path = line.split("=")[1]
            continue
        if "UnitFileState=" in line:
            selected_service_unit_file_state = _tr(line.split("=")[1])                        # "_tr([value])" is used for using translated string.
            continue
        if "UnitFilePreset=" in line:
            selected_service_unit_file_preset = _tr(line.split("=")[1])                       # "_tr([value])" is used for using translated string.
            continue
        if "CanStart=" in line:
            selected_service_can_start = _tr(line.split("=")[1].capitalize())                 # "_tr([value])" is used for using translated string.
            continue
        if "CanStop=" in line:
            selected_service_can_stop = _tr(line.split("=")[1].capitalize())                  # "_tr([value])" is used for using translated string.
            continue
        if "CanReload=" in line:
            selected_service_can_reload = _tr(line.split("=")[1].capitalize())                # "_tr([value])" is used for using translated string.
            continue


    # Set label text by using service data
    label6101w.set_text(selected_service_name)
    label6102w.set_text(selected_service_description)
    label6103w.set_text(f'{selected_service_unit_file_state} - {selected_service_unit_file_preset}')
    label6104w.set_text(selected_service_load_state)
    label6105w.set_text(selected_service_active_state)
    label6106w.set_text(selected_service_sub_state)
    label6107w.set_text(selected_service_fragment_path)
    label6108w.set_text(',\n'.join(selected_service_documentation))
    label6109w.set_text(selected_service_triggered_by)
    label6110w.set_text(selected_service_main_pid)
    label6111w.set_text(f'{selected_service_can_start} - {selected_service_can_stop}')
    label6112w.set_text(selected_service_can_reload)
    label6113w.set_text(selected_service_exec_main_pid)
    label6114w.set_text(selected_service_exec_main_start_times_stamp_monotonic)
    label6115w.set_text(selected_service_exec_main_exit_times_stamp_monotonic)
    label6116w.set_text(selected_service_control_pid)
    label6117w.set_text(selected_service_type)
    label6118w.set_text(selected_service_memory_current)
    label6119w.set_text(',\n'.join(selected_service_requires))
    label6120w.set_text(',\n'.join(selected_service_conflicts))
    label6121w.set_text(',\n'.join(selected_service_after))
    label6122w.set_text(',\n'.join(selected_service_before))


# ----------------------------------- Services - Services Details Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def services_details_loop_func():

    if window6101w.get_visible() is True:
        GLib.idle_add(services_details_foreground_func)
        global update_interval
        update_interval = Config.update_interval
        GLib.timeout_add(update_interval * 1000, services_details_loop_func)


# ----------------------------------- Services Details Foreground Thread Run Function (starts execution of the threads) -----------------------------------
def services_details_foreground_thread_run_func():

    services_details_initial_thread = Thread(target=services_details_initial_func, daemon=True)
    services_details_initial_thread.start()
    services_details_initial_thread.join()
    services_details_loop_thread = Thread(target=services_details_loop_func, daemon=True)
    services_details_loop_thread.start()


# ----------------------------------- Services - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def services_define_data_unit_converter_variables_func():

    global data_unit_list

    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently.

    # Unit Name    Abbreviation    bytes   
    # byte         B               1
    # kilobyte     KB              1024
    # megabyte     MB              1.04858E+06
    # gigabyte     GB              1.07374E+09
    # terabyte     TB              1.09951E+12
    # petabyte     PB              1.12590E+15
    # exabyte      EB              1.15292E+18

    # Unit Name    Abbreviation    bytes    
    # bit          b               8
    # kilobit      Kb              8192
    # megabit      Mb              8,38861E+06
    # gigabit      Gb              8,58993E+09
    # terabit      Tb              8,79609E+12
    # petabit      Pb              9,00720E+15
    # exabit       Eb              9,22337E+18

    data_unit_list = [[0, 0, _tr("Auto-Byte")], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, _tr("Auto-bit")], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Services - Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def services_details_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if unit >= 8:
        data = data * 8                                                                       # Source data is byte and a convertion is made by multiplicating with 8 if preferenced unit is bit.
    if unit in [0, 8]:                                                                        # "if unit in [0, 8]:" is about %25 faster than "if unit == 0 or unit == 8:".
        unit_counter = unit + 1
        while data > 1024:
            unit_counter = unit_counter + 1
            data = data/1024
        unit = data_unit_list[unit_counter][2]
        if data == 0:
            precision = 0
        return f'{data:.{precision}f} {unit}'

    data = data / data_unit_list[unit][1]
    unit = data_unit_list[unit][2]
    if data == 0:
        precision = 0
    return f'{data:.{precision}f} {unit}'


# ----------------------------------- Services - Services No Such Process Error Dialog Function (shows an error dialog and stops updating the "Process Details window" when the service is not alive anymore) -----------------------------------
def services_no_such_service_error_dialog():

    error_dialog6101w = Gtk.MessageDialog(transient_for=MainGUI.window1, title="Error", flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text="Service File Does Not Exist Anymore", )
    error_dialog6101w.format_secondary_text(f'Following service file does not exist anymore \nand service details window is closed automatically:\n  {selected_service_name} (PID: {selected_service_pid})')
    error_dialog6101w.run()
    error_dialog6101w.destroy()

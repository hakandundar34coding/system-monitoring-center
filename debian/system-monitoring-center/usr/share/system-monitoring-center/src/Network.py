#!/usr/bin/env python3

# ----------------------------------- Network - Network Tab GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def network_import_func():

    global Gtk, GLib, Thread, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import os
    import subprocess


    global Config, MainGUI, Performance, NetworkGUI
    import Config, MainGUI, Performance, NetworkGUI


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


# ----------------------------------- Network - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
def network_initial_func():

    network_define_data_unit_converter_variables_func()                                       # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    global network_card_list, selected_network_card_number                                    # These variables are defined as global variables because they will be used in "network_loop_func" function.
    network_card_list = Performance.network_card_list
    selected_network_card_number = Performance.selected_network_card_number

    # Get network_card_device_name
    network_card_vendor_name = "-"
    network_card_device_name = "-"
    if network_card_list[selected_network_card_number] != "lo":
        with open("/sys/class/net/" + network_card_list[selected_network_card_number] + "/device/vendor") as reader:   # Get network card vendor id
            network_card_vendor_id = "\n" + reader.read().split("x")[1].strip() + "  "
        with open("/sys/class/net/" + network_card_list[selected_network_card_number] + "/device/device") as reader:   # Get network card device id
            network_card_device_id = "\n\t" + reader.read().split("x")[1].strip() + "  "
        if os.path.isfile("/usr/share/misc/pci.ids") == True:                                 # Check if "pci.ids" file is located in "/usr/share/misc/pci.ids" in order to use it as directory. This directory is used in Debian-like systems.
            pci_ids_file_directory = "/usr/share/misc/pci.ids"
        if os.path.isfile("/usr/share/hwdata/pci.ids") == True:                               # Check if "pci.ids" file is located in "/usr/share/hwdata/pci.ids" in order to use it as directory. This directory is used in systems other than Debian-like systems.
            pci_ids_file_directory = "/usr/share/hwdata/pci.ids"
        with open(pci_ids_file_directory) as reader:                                          # Find network card device model from "pci.ids" file by using vendor id and device id.
            pci_ids_output = reader.read()
            if network_card_vendor_id in pci_ids_output:
                rest_of_the_pci_ids_output = pci_ids_output.split(network_card_vendor_id)[1]
                network_card_vendor_name = rest_of_the_pci_ids_output.split("\n")[0].strip()
            if network_card_device_id in rest_of_the_pci_ids_output:
                rest_of_the_rest_of_the_pci_ids_output = rest_of_the_pci_ids_output.split(network_card_device_id)[1]
                network_card_device_name = rest_of_the_rest_of_the_pci_ids_output.split("\n")[0].strip()
    network_card_device_model_name = f'{network_card_vendor_name} {network_card_device_name}'
    if network_card_list[selected_network_card_number] == "lo":                               # lo (Loopback Device) is a system device and it is not a physical device. Therefore it could not be found in "pci.ids" file.
        network_card_device_model_name = "Loopback Device"
    # Get connection_type
    if "en" in network_card_list[selected_network_card_number]:
        connection_type = _tr("Ethernet")
    elif "wl" in network_card_list[selected_network_card_number]:
        connection_type = _tr("Wi-Fi")
    else:
        connection_type = "-"
    # Get network_card_mac_address
    with open("/sys/class/net/" + network_card_list[selected_network_card_number] + "/address") as reader:
        network_card_mac_address = reader.read().strip().upper()
    # Get network_address_ipv4, network_address_ipv6
    ip_output_lines = (subprocess.check_output("ip a show " + network_card_list[selected_network_card_number], shell=True).strip()).decode().split("\n")
    for line in ip_output_lines:
        if "inet " in line:
            network_address_ipv4 = line.split()[1].split("/")[0]
        if "inet6 " in line:
            network_address_ipv6 = line.split()[1].split("/")[0]
    if "network_address_ipv4" not in locals():
        network_address_ipv4 = "-"
    if "network_address_ipv6" not in locals():
        network_address_ipv6 = "-"

    # Set Network tab label texts by using information get
    NetworkGUI.label1401.set_text(network_card_device_model_name)
    NetworkGUI.label1402.set_text(network_card_list[selected_network_card_number])
    NetworkGUI.label1407.set_text(connection_type)
    NetworkGUI.label1410.set_text(network_address_ipv4)
    NetworkGUI.label1411.set_text(network_address_ipv6)
    NetworkGUI.label1412.set_text(network_card_mac_address)


# ----------------------------------- Network - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
def network_loop_func():

    network_receive_speed = Performance.network_receive_speed
    network_send_speed = Performance.network_send_speed
    network_receive_bytes = Performance.network_receive_bytes
    network_send_bytes = Performance.network_send_bytes

    performance_network_speed_data_precision = Config.performance_network_speed_data_precision
    performance_network_data_data_precision = Config.performance_network_data_data_precision
    performance_network_speed_data_unit = Config.performance_network_speed_data_unit
    performance_network_data_data_unit = Config.performance_network_data_data_unit

    NetworkGUI.drawingarea1401.queue_draw()

    # Get network_card_connected
    with open("/sys/class/net/" + network_card_list[selected_network_card_number] + "/operstate") as reader:   # Get the information of if network card is connected by usng "/sys/class/net/" file.
        network_info = reader.read().strip()
        if network_info == "up":
            network_card_connected = _tr("Yes")
        elif network_info == "down":
            network_card_connected = _tr("No")
        elif network_info == "unknown":
            network_card_connected = _tr("Unknown")
        else:
            network_card_connected = network_info
    # Get network_ssid
    nmcli_output_lines = (subprocess.check_output("nmcli -get-values DEVICE,CONNECTION device status", shell=True).strip()).decode().split("\n")
    for line in nmcli_output_lines:
        line_splitted = line.split(":")
        if network_card_list[selected_network_card_number] == line_splitted[0]:
            network_ssid = line_splitted[1].strip()
            break
    if network_ssid == "":
        network_ssid = "-"
    # Get network_signal_strength
    network_signal_strength = "-"                                                             # Initial value of the "network_signal_strength". This value will be used if value could not be get.
    if "wl" in network_card_list[selected_network_card_number] and network_card_connected == _tr("Yes"):    # Translated value have to be used by using gettext constant. Not "Yes".
        with open("/proc/net/wireless") as reader:
            proc_net_wireless_output_lines = reader.read().strip().split("\n")
        for line in proc_net_wireless_output_lines:
            line_splitted = line.split()
            if network_card_list[selected_network_card_number] == line_splitted[0].split(":")[0]:
                network_signal_strength = line_splitted[2].split(".")[0]                      # "split(".")" is used in order to remove "." at the end of the signal value.
                break

    # Set and update Network tab label texts by using information get
    NetworkGUI.label1403.set_text(f'{network_data_unit_converter_func(network_receive_speed[selected_network_card_number][-1], performance_network_speed_data_unit, performance_network_speed_data_precision)}/s')
    NetworkGUI.label1404.set_text(f'{network_data_unit_converter_func(network_send_speed[selected_network_card_number][-1], performance_network_speed_data_unit, performance_network_speed_data_precision)}/s')
    NetworkGUI.label1405.set_text(network_data_unit_converter_func(network_receive_bytes[selected_network_card_number], performance_network_data_data_unit, performance_network_data_data_precision))
    NetworkGUI.label1406.set_text(network_data_unit_converter_func(network_send_bytes[selected_network_card_number], performance_network_data_data_unit, performance_network_data_data_precision))
    NetworkGUI.label1408.set_text(f'{network_card_connected} - {network_ssid}')
    NetworkGUI.label1409.set_text(network_signal_strength)


# ----------------------------------- Network Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def network_initial_thread_func():

    GLib.idle_add(network_initial_func)


# ----------------------------------- Network Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def network_loop_thread_func(dummy_variable):                                                 # "dummy_variable" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when a tab is switched off and on again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

#     GLib.idle_add(network_loop_func)
#     if MainGUI.radiobutton1004.get_active() == True:
#         global update_interval
#         update_interval = Config.update_interval
#         GLib.timeout_add(update_interval * 1000, network_loop_thread_func)

    if MainGUI.radiobutton1.get_active() == True and MainGUI.radiobutton1004.get_active() == True:
        global network_glib_source, update_interval                                           # GLib source variable name is defined as global to be able to destroy it if tab is switched back in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            network_glib_source.destroy()                                                     # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        network_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(network_loop_func)
        network_glib_source.set_callback(network_loop_thread_func)
        network_glib_source.attach(GLib.MainContext.default())                                # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
        


# ----------------------------------- Network Thread Run Function (starts execution of the threads) -----------------------------------
def network_thread_run_func():

    if "update_interval" not in globals():                                                    # To be able to run initial thread for only one time
        network_initial_thread = Thread(target=network_initial_thread_func, daemon=True)
        network_initial_thread.start()
        network_initial_thread.join()
    network_loop_thread = Thread(target=network_loop_thread_func(None), daemon=True)          # "None" is an arbitrary value which is required for using "GLib.timeout_source_new()".
    network_loop_thread.start()


# ----------------------------------- Network - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def network_define_data_unit_converter_variables_func():

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


# ----------------------------------- Network - Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def network_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if isinstance(data, str) is True:
        return data
    if unit >= 8:
        data = data * 8                                                                       # Source data is byte and a convertion is made by multiplicating with 8 if preferenced unit is bit.
    if unit == 0 or unit == 8:
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

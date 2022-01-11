#!/usr/bin/env python3

# ----------------------------------- Network - Network Tab Import Function -----------------------------------
def network_import_func():

    global Gtk, GLib, os, subprocess

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    import os
    import subprocess


    global Config, MainGUI, Performance
    import Config, MainGUI, Performance


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Network - Network GUI Function -----------------------------------
def network_gui_func():

    # Network tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/NetworkTab.ui")

    # Network tab GUI objects
    global grid1401, drawingarea1401, button1401, label1401, label1402
    global label1403, label1404, label1405, label1406, label1407, label1408, label1409, label1410, label1411, label1412, label1413

    # Network tab GUI objects - get
    grid1401 = builder.get_object('grid1401')
    drawingarea1401 = builder.get_object('drawingarea1401')
    button1401 = builder.get_object('button1401')
    label1401 = builder.get_object('label1401')
    label1402 = builder.get_object('label1402')
    label1403 = builder.get_object('label1403')
    label1404 = builder.get_object('label1404')
    label1405 = builder.get_object('label1405')
    label1406 = builder.get_object('label1406')
    label1407 = builder.get_object('label1407')
    label1408 = builder.get_object('label1408')
    label1409 = builder.get_object('label1409')
    label1410 = builder.get_object('label1410')
    label1411 = builder.get_object('label1411')
    label1412 = builder.get_object('label1412')
    label1413 = builder.get_object('label1413')


    # Network tab GUI functions
    def on_button1401_clicked(widget):
        if 'NetworkMenu' not in globals():
            global NetworkMenu
            import NetworkMenu
            NetworkMenu.network_menus_import_func()
            NetworkMenu.network_menus_gui_func()
            NetworkMenu.popover1401p.set_relative_to(button1401)                              # Set widget that popover menu will display at the edge of.
            NetworkMenu.popover1401p.set_position(1)                                          # Show popover menu at the right edge of the caller button.
        NetworkMenu.popover1401p.popup()                                                      # Show Network tab popover GUI

    # ----------------------------------- Network - Plot Network download/upload speed data as a Line Chart ----------------------------------- 
    def on_drawingarea1401_draw(drawingarea1401, chart1401):

        chart_data_history = Config.chart_data_history
        chart_x_axis = list(range(0, chart_data_history))

        network_receive_speed = Performance.network_receive_speed[Performance.selected_network_card_number]
        network_send_speed = Performance.network_send_speed[Performance.selected_network_card_number]

        chart_line_color = Config.chart_line_color_network_speed_data
        chart_background_color = Config.chart_background_color_all_charts

        chart_foreground_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.4 * chart_line_color[3]]
        chart_fill_below_line_color = [chart_line_color[0], chart_line_color[1], chart_line_color[2], 0.15 * chart_line_color[3]]

        chart1401_width = Gtk.Widget.get_allocated_width(drawingarea1401)
        chart1401_height = Gtk.Widget.get_allocated_height(drawingarea1401)

        chart1401.set_source_rgba(chart_background_color[0], chart_background_color[1], chart_background_color[2], chart_background_color[3])
        chart1401.rectangle(0, 0, chart1401_width, chart1401_height)
        chart1401.fill()

        chart1401.set_line_width(1)
        chart1401.set_dash([4, 3])
        chart1401.set_source_rgba(chart_foreground_color[0], chart_foreground_color[1], chart_foreground_color[2], chart_foreground_color[3])
        for i in range(3):
            chart1401.move_to(0, chart1401_height/4*(i+1))
            chart1401.line_to(chart1401_width, chart1401_height/4*(i+1))
        for i in range(4):
            chart1401.move_to(chart1401_width/5*(i+1), 0)
            chart1401.line_to(chart1401_width/5*(i+1), chart1401_height)
        chart1401.stroke()

        chart1401_y_limit = 1.1 * ((max(max(network_receive_speed), max(network_send_speed))) + 0.0000001)
        if Config.plot_network_download_speed == 1 and Config.plot_network_upload_speed == 0:
            chart1401_y_limit = 1.1 * (max(network_receive_speed) + 0.0000001)
        if Config.plot_network_download_speed == 0 and Config.plot_network_upload_speed == 1:
            chart1401_y_limit = 1.1 * (max(network_send_speed) + 0.0000001)

        # ---------- Start - This block of code is used in order to show maximum value of the chart as multiples of 1, 10, 100. ----------
        data_unit_for_chart_y_limit = 0
        if Config.performance_network_speed_data_unit >= 8:
            data_unit_for_chart_y_limit = 8
        try:
            chart1401_y_limit_str = f'{network_data_unit_converter_func(chart1401_y_limit, data_unit_for_chart_y_limit, 0)}/s'
        except NameError:
            return
        chart1401_y_limit_split = chart1401_y_limit_str.split(" ")
        chart1401_y_limit_float = float(chart1401_y_limit_split[0])
        number_of_digits = len(str(int(chart1401_y_limit_split[0])))
        multiple = 10 ** (number_of_digits - 1)
        number_to_get_next_multiple = chart1401_y_limit_float + (multiple - 0.0001)
        next_multiple = int(number_to_get_next_multiple - (number_to_get_next_multiple % multiple))
        label1413.set_text(f'{next_multiple} {chart1401_y_limit_split[1]}')
        chart1401_y_limit = (chart1401_y_limit * next_multiple / (chart1401_y_limit_float + 0.0000001) + 0.0000001)
        # ---------- End - This block of code is used in order to show maximum value of the chart as multiples of 1, 10, 100. ----------

        chart1401.set_dash([], 0)
        chart1401.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
        chart1401.rectangle(0, 0, chart1401_width, chart1401_height)
        chart1401.stroke()

        if Config.plot_network_download_speed == 1:
            chart1401.set_source_rgba(chart_line_color[0], chart_line_color[1], chart_line_color[2], chart_line_color[3])
            chart1401.move_to(chart1401_width*chart_x_axis[0]/(chart_data_history-1), chart1401_height - chart1401_height*network_receive_speed[0]/chart1401_y_limit)
            for i in range(len(chart_x_axis) - 1):
                delta_x_chart1401a = (chart1401_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1401_width * chart_x_axis[i]/(chart_data_history-1))
                delta_y_chart1401a = (chart1401_height*network_receive_speed[i+1]/chart1401_y_limit) - (chart1401_height*network_receive_speed[i]/chart1401_y_limit)
                chart1401.rel_line_to(delta_x_chart1401a, -delta_y_chart1401a)

            chart1401.rel_line_to(10, 0)
            chart1401.rel_line_to(0, chart1401_height+10)
            chart1401.rel_line_to(-(chart1401_width+20), 0)
            chart1401.rel_line_to(0, -(chart1401_height+10))
            chart1401.close_path()
            chart1401.stroke()

        if Config.plot_network_upload_speed == 1:
            chart1401.set_dash([3, 3])
            chart1401.move_to(chart1401_width*chart_x_axis[0]/(chart_data_history-1), chart1401_height - chart1401_height*network_send_speed[0]/chart1401_y_limit)
            for i in range(len(chart_x_axis) - 1):
                delta_x_chart1401b = (chart1401_width * chart_x_axis[i+1]/(chart_data_history-1)) - (chart1401_width * chart_x_axis[i]/(chart_data_history-1))
                delta_y_chart1401b = (chart1401_height*network_send_speed[i+1]/chart1401_y_limit) - (chart1401_height*network_send_speed[i]/chart1401_y_limit)
                chart1401.rel_line_to(delta_x_chart1401b, -delta_y_chart1401b)

            chart1401.rel_line_to(10, 0)
            chart1401.rel_line_to(0, chart1401_height+10)
            chart1401.rel_line_to(-(chart1401_width+20), 0)
            chart1401.rel_line_to(0, -(chart1401_height+10))
            chart1401.close_path()
            chart1401.stroke()


    # Network tab GUI functions - connect
    button1401.connect("clicked", on_button1401_clicked)
    drawingarea1401.connect("draw", on_drawingarea1401_draw)


# ----------------------------------- Network - Initial Function -----------------------------------
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
        try:                                                                                  # Find network card device model from "pci.ids" file by using vendor id and device id.
            with open("/usr/share/misc/pci.ids") as reader:                                   # Read "pci.ids" file if it is located in "/usr/share/misc/pci.ids" in order to use it as directory. This directory is used in Debian-like systems.
                pci_ids_output = reader.read()
        except FileNotFoundError:
            with open("/usr/share/hwdata/pci.ids") as reader:                                 # Read "pci.ids" file if it is located in "/usr/share/hwdata/pci.ids" in order to use it as directory. This directory is used in systems other than Debian-like systems.
                pci_ids_output = reader.read()
        if network_card_vendor_id in pci_ids_output:                                          # "vendor" information may not be present in the pci.ids file.
            rest_of_the_pci_ids_output = pci_ids_output.split(network_card_vendor_id, 1)[1]    # "1" in the ".split("[string", 1)" is used in order to split only the first instance in the whole text for faster split operation.
            network_card_vendor_name = rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
        else:
            network_card_vendor_name = f'[{_tr("Unknown")}]'
        if network_card_vendor_name != f'[{_tr("Unknown")}]':
            if network_card_device_id in rest_of_the_pci_ids_output:                          # "device name" information may not be present in the pci.ids file.
                rest_of_the_rest_of_the_pci_ids_output = rest_of_the_pci_ids_output.split(network_card_device_id, 1)[1]
                network_card_device_name = rest_of_the_rest_of_the_pci_ids_output.split("\n", 1)[0].strip()
            else:
                network_card_device_name = f'[{_tr("Unknown")}]'
        else:
            network_card_device_name = f'[{_tr("Unknown")}]'
    network_card_device_model_name = f'{network_card_vendor_name} - {network_card_device_name}'
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
    ip_output_lines = (subprocess.check_output(["ip", "a", "show", network_card_list[selected_network_card_number]], shell=False)).decode().strip().split("\n")
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
    label1401.set_text(network_card_device_model_name)
    label1402.set_text(network_card_list[selected_network_card_number])
    label1407.set_text(connection_type)
    label1410.set_text(network_address_ipv4)
    label1411.set_text(network_address_ipv6)
    label1412.set_text(network_card_mac_address)


# ----------------------------------- Network - Initial Function -----------------------------------
def network_loop_func():

    network_receive_speed = Performance.network_receive_speed
    network_send_speed = Performance.network_send_speed
    network_receive_bytes = Performance.network_receive_bytes
    network_send_bytes = Performance.network_send_bytes

    performance_network_speed_data_precision = Config.performance_network_speed_data_precision
    performance_network_data_data_precision = Config.performance_network_data_data_precision
    performance_network_speed_data_unit = Config.performance_network_speed_data_unit
    performance_network_data_data_unit = Config.performance_network_data_data_unit

    drawingarea1401.queue_draw()

    # Get network_card_connected
    with open("/sys/class/net/" + network_card_list[selected_network_card_number] + "/operstate") as reader:   # Get the information of if network card is connected by usng "/sys/class/net/" file.
        network_info = reader.read().strip()
        if network_info == "up":
            network_card_connected = _tr("Yes")
        elif network_info == "down":
            network_card_connected = _tr("No")
        elif network_info == "unknown":
            network_card_connected = f'[{_tr("Unknown")}]'
        else:
            network_card_connected = network_info
    # Get network_ssid
    try:                                                                                      # "try-catch" is used in order to avoid errors because Network Manager (which is required for running "nmcli" command) may not be installed on all systems. This is a very rare sitution.
        nmcli_output_lines = (subprocess.check_output(["nmcli", "-get-values", "DEVICE,CONNECTION", "device", "status"], shell=False)).decode().strip().split("\n")
    except FileNotFoundError:
        network_ssid = f'[{_tr("Unknown")}]'
    if "nmcli_output_lines" in locals():                                                      # Check if "nmcli_output_lines" value is get.
        for line in nmcli_output_lines:
            line_splitted = line.split(":")
            if network_card_list[selected_network_card_number] == line_splitted[0]:
                network_ssid = line_splitted[1].strip()
                break
    if network_ssid == "":                                                                    # "network_ssid" value is get as "" if selected network card is not connected a Wi-Fi network.
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
    label1403.set_text(f'{network_data_unit_converter_func(network_receive_speed[selected_network_card_number][-1], performance_network_speed_data_unit, performance_network_speed_data_precision)}/s')
    label1404.set_text(f'{network_data_unit_converter_func(network_send_speed[selected_network_card_number][-1], performance_network_speed_data_unit, performance_network_speed_data_precision)}/s')
    label1405.set_text(network_data_unit_converter_func(network_receive_bytes[selected_network_card_number], performance_network_data_data_unit, performance_network_data_data_precision))
    label1406.set_text(network_data_unit_converter_func(network_send_bytes[selected_network_card_number], performance_network_data_data_unit, performance_network_data_data_precision))
    label1408.set_text(f'{network_card_connected} - {network_ssid}')
    label1409.set_text(network_signal_strength)


# ----------------------------------- Network Run Function -----------------------------------
def network_run_func(*args):

    if "update_interval" not in globals():
        GLib.idle_add(network_initial_func)
    if MainGUI.radiobutton1.get_active() == True and MainGUI.radiobutton1004.get_active() == True:
        global network_glib_source, update_interval
        try:
            network_glib_source.destroy()
        except NameError:
            pass
        update_interval = Config.update_interval
        network_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(network_loop_func)
        network_glib_source.set_callback(network_run_func)
        network_glib_source.attach(GLib.MainContext.default())


# ----------------------------------- Network - Define Data Unit Converter Variables Function -----------------------------------
def network_define_data_unit_converter_variables_func():

    global data_unit_list
    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently. [[index, calculated byte value, unit abbreviation], ...]
    data_unit_list = [[0, 0, "Auto-Byte"], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, "Auto-bit"], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Network - Data Unit Converter Function -----------------------------------
def network_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if isinstance(data, str) is True:
        return data
    if unit >= 8:
        data = data * 8
    if unit in [0, 8]:
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

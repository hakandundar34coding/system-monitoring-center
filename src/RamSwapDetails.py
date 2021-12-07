#!/usr/bin/env python3

# ----------------------------------- RAM - Swap Details Window GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def ram_swap_details_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global MainGUI, Config
    import MainGUI, Config


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


# ----------------------------------- RAM - Swap Details Window GUI Function (the code of this module in order to avoid running them during module import and defines GUI objects and functions/signals) -----------------------------------
def ram_swap_details_gui_func():

    global builder, window1201w2
    global label1201w2, button1201w2


    # Swap Details window GUI objects - get
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/RamSwapDetailsWindow.ui")

    window1201w2 = builder.get_object('window1201w2')
    label1201w2 = builder.get_object('label1201w2')
    button1201w2 = builder.get_object('button1201w2')


    # Swap Details window GUI functions
    def on_window1201w2_delete_event(widget, event):
        window1201w2.hide()
        return True

    def on_window1201w2_show(widget):
        label1201w2.set_text("-")                                                             # Reset label text when window is shown.
        global swap_details_text
        try:                                                                                  # "try-except" is used in order to avoid errors if user closed polkit dialog without entering password. Because "memory_hardware_information_text" string will not be defined and will not be get in this situation.
            label1201w2.set_text(swap_details_text)                                           # Set label text for showing RAM hardware information.
        except NameError:
            pass

    def on_button1201w2_clicked(widget):                                                      # "Close" button
        window1201w2.hide()


    # Swap Details window GUI functions - connect
    window1201w2.connect("delete-event", on_window1201w2_delete_event)
    window1201w2.connect("show", on_window1201w2_show)
    button1201w2.connect("clicked", on_button1201w2_clicked)


# ----------------------------------- RAM - Swap Details Get Function (gets Swap details information) -----------------------------------
def ram_swap_details_get_func():

    ram_define_data_unit_converter_variables_func()                                       # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.
    performance_ram_swap_data_precision = Config.performance_ram_swap_data_precision
    performance_ram_swap_data_unit = Config.performance_ram_swap_data_unit

    ram_hardware_information_text_list = [_tr("Partition"), _tr("File")]                      # This list is defined in order to make some command output strings to be translated into other languages.

    global swap_details_text                                                                  # This value will also be used for preventing showing RAM hardware Information window if user closes polkit window without entering password.
    swap_details_text = ""                                                                    # Set initial value of "memory_hardware_information_text". Hardware information will be appended to this string.

    with open("/proc/swaps") as reader:                                                       # Read "/proc/swaps" file for getting swap memory details. Systems may has more than one swap partition/file and this information can be read from this file.
        proc_swaps_lines = reader.read().split("\n")

    del proc_swaps_lines[0]                                                                   # Delete header indormation which is get from "/proc/swaps" file.

    for line in proc_swaps_lines:
        if line == "":
            break
        swap_name = "-"
        swap_type = "-"
        swap_size = "-"
        swap_used = "-"
        swap_priority = "-"
        line_split = line.split()
        swap_name = line_split[0].strip()
        swap_type = line_split[1].strip().title()
        swap_size = int(line_split[2].strip()) * 1024                                         # Values in this file are in KiB. They are converted to Bytes.
        swap_size = f'{ram_data_unit_converter_func(swap_size, performance_ram_swap_data_unit, performance_ram_swap_data_precision)}'
        swap_used = int(line_split[3].strip()) * 1024                                         # Values in this file are in KiB. They are converted to Bytes.
        swap_used = f'{ram_data_unit_converter_func(swap_used, performance_ram_swap_data_unit, performance_ram_swap_data_precision)}'
        swap_priority = line_split[4].strip()
        swap_details_text = swap_details_text + "\n" + _tr("Partition/File Name") + " :    " + swap_name
        swap_details_text = swap_details_text + "\n" + _tr("Type") + " :    " + swap_type
        swap_details_text = swap_details_text + "\n" + _tr("Size") + " :    " + swap_size
        swap_details_text = swap_details_text + "\n" + _tr("Used") + " :    " + swap_used
        swap_details_text = swap_details_text + "\n" + _tr("Priority") + " :    " + swap_priority
        swap_details_text += "\n"
        swap_details_text = swap_details_text + "\n" + "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -" + "\n"
        swap_details_text = swap_details_text.strip("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n")    # In order to remove this string from the last line.

    swap_details_text = swap_details_text.strip()                                             # Delete empty lines at the beginning and end of the string.

    if swap_details_text.strip() == "":
        swap_details_text = _tr("This system has no swap memory.")


# ----------------------------------- RAM - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def ram_define_data_unit_converter_variables_func():

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


# ----------------------------------- RAM - Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def ram_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if isinstance(data, str) is True:
        return data
    if unit >= 8:
        data = data * 8                                                                       # Source data is byte and a convertion is made by multiplicating with 8 if preferenced unit is bit.
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

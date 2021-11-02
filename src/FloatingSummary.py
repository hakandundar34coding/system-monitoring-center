#!/usr/bin/env python3

# ----------------------------------- FloatingSummary - FloatingSummary Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def floating_summary_import_func():

    global Gtk, GLib, Thread, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread
    import os

    global Config, Performance, MainGUI
    import Config, Performance, MainGUI


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


# ----------------------------------- FloatingSummary - FloatingSummary Window GUI Function (the code of this module in order to avoid running them during module import and defines GUI objects and functions/signals) -----------------------------------
def floating_summary_gui_func():

    # FloatingSummary Window GUI objects - get from file
    builder = Gtk.Builder()
    builder.set_translation_domain(application_name)                                          # For showing translated texts onthe Glade generated GTK GUI
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/FloatingSummaryWindow.ui")

    # FloatingSummary Window GUI objects
    global window3001, grid3001
    global label3001, label3002, label3003, label3004, label3005, label3006, label3007, label3008

    # FloatingSummary Window GUI objects - get
    window3001 = builder.get_object('window3001')
    grid3001 = builder.get_object('grid3001')
    label3001 = builder.get_object('label3001')
    label3002 = builder.get_object('label3002')
    label3003 = builder.get_object('label3003')
    label3004 = builder.get_object('label3004')
    label3005 = builder.get_object('label3005')
    label3006 = builder.get_object('label3006')
    label3007 = builder.get_object('label3007')
    label3008 = builder.get_object('label3008')


    # FloatingSummary Window GUI functions
    def on_window3001_button_press_event(widget, event):                                      # Define a function for clicking and dragging the window.
        if event.button == 1:
            window3001.begin_move_drag(event.button, event.x_root, event.y_root, event.time)


    # FloatingSummary Window GUI functions - connect
    window3001.connect("button-press-event", on_window3001_button_press_event)


    # Set floating summary window properties
    window3001.set_resizable(False)                                                           # For preventing window to be resized.
    window3001.set_skip_taskbar_hint(True)                                                    # For hiding window on the taskbar.
    window3001.set_decorated(False)                                                           # For hiding window title, buttons on the title and window border.
    window3001.set_keep_above(True)                                                           # For keeping the window on top of all windows.
    window3001.set_opacity(Config.floating_summary_window_transparency)                       # Set transperancy of the window.

    # Floating Summary window is closed when main window is closed (when application is run as running a desktop application). But it is not closed when main window is closed if application is run from an IDE for debugging/developing purposes.


# ----------------------------------- FloatingSummary - Initial Function (defines and sets floating summary GUI objects which are not updated on every loop) -----------------------------------
def floating_summary_initial_func():

    global floating_summary_data_shown_prev
    floating_summary_data_shown_prev = []

    floating_summary_define_data_unit_converter_variables_func()                              # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.


# ----------------------------------- FloatingSummary - Loop Function (updates performance data on the floating summary window) -----------------------------------
def floating_summary_loop_func():

    window3001.set_opacity(Config.floating_summary_window_transparency)

    global floating_summary_data_shown_prev
    floating_summary_data_shown = Config.floating_summary_data_shown
    if floating_summary_data_shown != floating_summary_data_shown_prev:                       # Remove all labels and add preferred ones if user makes changes on visible performance data (labels).
        for i in reversed(range(9)):                                                          # 9 is large enough to remove all labels on the grid.
            try:
                label_to_remove = grid3001.get_child_at(0, i)
                grid3001.remove(label_to_remove)
            except:
                pass

        grid_row_count = 0
        if 0 in floating_summary_data_shown:
            grid_row_count = 0
            grid3001.attach(label3001, 0, grid_row_count, 1, 1)                               # Attach label for average CPU usage percent data
        if 1 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            grid3001.attach(label3002, 0, grid_row_count, 1, 1)                               # Attach label for RAM usage percent data
        if 2 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            grid3001.attach(label3003, 0, grid_row_count, 1, 1)                               # Attach label for disk read+write speed data
        if 3 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            grid3001.attach(label3004, 0, grid_row_count, 1, 1)                               # Attach label for disk read speed data
        if 4 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            grid3001.attach(label3005, 0, grid_row_count, 1, 1)                               # Attach label for disk write speed data
        if 5 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            grid3001.attach(label3006, 0, grid_row_count, 1, 1)                               # Attach label for network download+upload speed data
        if 6 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            grid3001.attach(label3007, 0, grid_row_count, 1, 1)                               # Attach label for network download speed data
        if 7 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            grid3001.attach(label3008, 0, grid_row_count, 1, 1)                               # Attach label for network upload speed data

    floating_summary_data_shown_prev = list(floating_summary_data_shown)                      # list1 = list(list2) have to be used for proper working of the code because using this equation without "list()" makes a connection between these lists instead of copying one list with a different variable name.

    # Set label text for showing peformance data
    if 0 in floating_summary_data_shown:
        label3001.set_text(_tr("CPU: ") + f'{Performance.cpu_usage_percent_ave[-1]:.0f} %')
    if 1 in floating_summary_data_shown:
        label3002.set_text(_tr("RAM: ") + f'{Performance.ram_usage_percent[-1]:.0f} %')
    if 2 in floating_summary_data_shown:
        label3003.set_text(_tr("Disk R+W: ") + f'{floating_summary_data_unit_converter_func((Performance.disk_read_speed[Performance.selected_disk_number][-1] + Performance.disk_write_speed[Performance.selected_disk_number][-1]), 0, 2)}/s')
    if 3 in floating_summary_data_shown:
        label3004.set_text(_tr("Disk R: ") + f'{floating_summary_data_unit_converter_func(Performance.disk_read_speed[Performance.selected_disk_number][-1], 0, 2)}/s')
    if 4 in floating_summary_data_shown:
        label3005.set_text(_tr("Disk W: ") + f'{floating_summary_data_unit_converter_func(Performance.disk_write_speed[Performance.selected_disk_number][-1], 0, 2)}/s')
    if 5 in floating_summary_data_shown:
        label3006.set_text(_tr("Network D+U: ") + f'{floating_summary_data_unit_converter_func((Performance.network_receive_speed[Performance.selected_network_card_number][-1] + Performance.network_send_speed[Performance.selected_network_card_number][-1]), 0, 2)}/s')
    if 6 in floating_summary_data_shown:
        label3007.set_text(_tr("Network R: ") + f'{floating_summary_data_unit_converter_func(Performance.network_receive_speed[Performance.selected_network_card_number][-1], 0, 2)}/s')
    if 7 in floating_summary_data_shown:
        label3008.set_text(_tr("Network W: ") + f'{floating_summary_data_unit_converter_func(Performance.network_send_speed[Performance.selected_network_card_number][-1], 0, 2)}/s')


# ----------------------------------- FloatingSummary Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def floating_summary_initial_thread_func():

    GLib.idle_add(floating_summary_initial_func)


# ----------------------------------- FloatingSummary Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def floating_summary_loop_thread_func(*args):                                                 # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when Floating Summary window is set as hidden and shown again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

    if window3001.get_visible() == True:
        global floating_summary_glib_source, update_interval                                  # GLib source variable name is defined as global to be able to destroy it if Floating Summary window is shown again in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            floating_summary_glib_source.destroy()                                            # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        floating_summary_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(floating_summary_loop_func)
        floating_summary_glib_source.set_callback(floating_summary_loop_thread_func)
        floating_summary_glib_source.attach(GLib.MainContext.default())                       # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.


# ----------------------------------- FloatingSummary Thread Run Function (starts execution of the threads) -----------------------------------
def floating_summary_thread_run_func():

    floating_summary_initial_thread = Thread(target=floating_summary_initial_thread_func, daemon=True)
    floating_summary_initial_thread.start()
    floating_summary_initial_thread.join()
    floating_summary_loop_thread = Thread(target=floating_summary_loop_thread_func, daemon=True)
    floating_summary_loop_thread.start()


# ----------------------------------- FloatingSummary - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def floating_summary_define_data_unit_converter_variables_func():

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


# ----------------------------------- FloatingSummary - Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def floating_summary_data_unit_converter_func(data, unit, precision):

    global data_unit_list
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

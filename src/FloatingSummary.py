#!/usr/bin/env python3

# ----------------------------------- FloatingSummary - FloatingSummary Import Function -----------------------------------
def floating_summary_import_func():

    global Gtk, GLib, os

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GLib', '2.0')
    from gi.repository import Gtk, GLib
    import os


    global Config, Performance
    import Config, Performance


    global _tr
    from locale import gettext as _tr


# ----------------------------------- FloatingSummary - FloatingSummary Window GUI Function -----------------------------------
def floating_summary_gui_func():

    # FloatingSummary Window GUI objects - get from file
    builder = Gtk.Builder()
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
    window3001.set_resizable(False)                                                           # Prevent window to be resized.
    window3001.set_skip_taskbar_hint(True)                                                    # Hide window on the taskbar.
    window3001.set_decorated(False)                                                           # Hide window title, buttons on the title and window border.
    window3001.set_keep_above(True)                                                           # Keep the window on top of all windows.

    # Floating Summary window is closed when main window is closed (when application is run as running a desktop application). But it is not closed when main window is closed if application is run from an IDE for debugging/developing purposes.


# ----------------------------------- FloatingSummary - Initial Function -----------------------------------
def floating_summary_initial_func():

    floating_summary_define_data_unit_converter_variables_func()                              # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.


# ----------------------------------- FloatingSummary - Loop Function -----------------------------------
def floating_summary_loop_func():

    window3001.set_opacity(Config.floating_summary_window_transparency)                       # Set transperancy of the window.

    floating_summary_data_shown_prev = []
    floating_summary_data_shown = Config.floating_summary_data_shown
    if floating_summary_data_shown != floating_summary_data_shown_prev:                       # Remove all labels and add preferred ones if user makes changes on visible performance data (labels).
        for i in reversed(range(9)):                                                          # 9 is large enough to remove all labels on the grid.
            try:
                label_to_remove = grid3001.get_child_at(0, i)
                grid3001.remove(label_to_remove)
            except Exception:
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
        label3001.set_text(_tr("CPU") + ": " + f'{Performance.cpu_usage_percent_ave[-1]:.0f} %')
    if 1 in floating_summary_data_shown:
        label3002.set_text(_tr("RAM") + ": " + f'{Performance.ram_usage_percent[-1]:.0f} %')
    if 2 in floating_summary_data_shown:
        label3003.set_text(_tr("Disk R+W") + ": " + f'{floating_summary_data_unit_converter_func((Performance.disk_read_speed[Performance.selected_disk_number][-1] + Performance.disk_write_speed[Performance.selected_disk_number][-1]), 0, 2)}/s')
    if 3 in floating_summary_data_shown:
        label3004.set_text(_tr("Disk R") + ": " + f'{floating_summary_data_unit_converter_func(Performance.disk_read_speed[Performance.selected_disk_number][-1], 0, 2)}/s')
    if 4 in floating_summary_data_shown:
        label3005.set_text(_tr("Disk W") + ": " + f'{floating_summary_data_unit_converter_func(Performance.disk_write_speed[Performance.selected_disk_number][-1], 0, 2)}/s')
    if 5 in floating_summary_data_shown:
        label3006.set_text(_tr("Network D+U") + ": " + f'{floating_summary_data_unit_converter_func((Performance.network_receive_speed[Performance.selected_network_card_number][-1] + Performance.network_send_speed[Performance.selected_network_card_number][-1]), 0, 2)}/s')
    if 6 in floating_summary_data_shown:
        label3007.set_text(_tr("Network D") + ": " + f'{floating_summary_data_unit_converter_func(Performance.network_receive_speed[Performance.selected_network_card_number][-1], 0, 2)}/s')
    if 7 in floating_summary_data_shown:
        label3008.set_text(_tr("Network U") + ": " + f'{floating_summary_data_unit_converter_func(Performance.network_send_speed[Performance.selected_network_card_number][-1], 0, 2)}/s')


# ----------------------------------- FloatingSummary - Run Function -----------------------------------
def floating_summary_run_func(*args):

    if "floating_summary_glib_source" not in globals():
        GLib.idle_add(floating_summary_initial_func)
    if window3001.get_visible() == True:
        global floating_summary_glib_source, update_interval
        try:
            floating_summary_glib_source.destroy()
        except NameError:
            pass
        update_interval = Config.update_interval
        floating_summary_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(floating_summary_loop_func)
        floating_summary_glib_source.set_callback(floating_summary_run_func)
        floating_summary_glib_source.attach(GLib.MainContext.default())


# ----------------------------------- FloatingSummary - Define Data Unit Converter Variables Function -----------------------------------
def floating_summary_define_data_unit_converter_variables_func():

    global data_unit_list
    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently. [[index, calculated byte value, unit abbreviation], ...]
    data_unit_list = [[0, 0, "Auto-Byte"], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09951E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, "Auto-bit"], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- FloatingSummary - Data Unit Converter Function -----------------------------------
def floating_summary_data_unit_converter_func(data, unit, precision):

    global data_unit_list
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

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


# ----------------------------------- FloatingSummary - Initial Function (defines and sets floating summary GUI objects which are not updated on every loop) -----------------------------------
def floating_summary_initial_func():
    # Floating Summary window is closed when main window is closed (when application is run as running a desktop application). But it is not closed when main window is closed if application is run from an IDE for debugging/develoing purposes.

    global floating_summary_window, floating_summary_grid, floating_summary_data_shown_prev
    floating_summary_data_shown_prev = []

    floating_summary_window = Gtk.Window()
    floating_summary_grid = Gtk.Grid()
    floating_summary_window.add(floating_summary_grid)
    floating_summary_grid.set_size_request(-1, -1)

    # Append labels to grid for showing performance data
    grid_row_count = 0
    global floating_summary_cpu_label
    floating_summary_cpu_label = Gtk.Label()
    floating_summary_grid.attach(floating_summary_cpu_label, 0, grid_row_count, 1, 1)
    floating_summary_cpu_label.set_halign(Gtk.Align.START)
    floating_summary_cpu_label.set_valign(Gtk.Align.START)
    grid_row_count = grid_row_count + 1
    global floating_summary_ram_label
    floating_summary_ram_label = Gtk.Label()
    floating_summary_grid.attach(floating_summary_ram_label, 0, grid_row_count, 1, 1)
    floating_summary_ram_label.set_halign(Gtk.Align.START)
    floating_summary_ram_label.set_valign(Gtk.Align.START)
    grid_row_count = grid_row_count + 1
    global floating_summary_disk_read_write_speed_label
    floating_summary_disk_read_write_speed_label = Gtk.Label()
    floating_summary_grid.attach(floating_summary_disk_read_write_speed_label, 0, grid_row_count, 1, 1)
    floating_summary_disk_read_write_speed_label.set_halign(Gtk.Align.START)
    floating_summary_disk_read_write_speed_label.set_valign(Gtk.Align.START)
    grid_row_count = grid_row_count + 1
    global floating_summary_disk_read_speed_label
    floating_summary_disk_read_speed_label = Gtk.Label()
    floating_summary_grid.attach(floating_summary_disk_read_speed_label, 0, grid_row_count, 1, 1)
    floating_summary_disk_read_speed_label.set_halign(Gtk.Align.START)
    floating_summary_disk_read_speed_label.set_valign(Gtk.Align.START)
    grid_row_count = grid_row_count + 1
    global floating_summary_disk_write_speed_label
    floating_summary_disk_write_speed_label = Gtk.Label()
    floating_summary_grid.attach(floating_summary_disk_write_speed_label, 0, grid_row_count, 1, 1)
    floating_summary_disk_write_speed_label.set_halign(Gtk.Align.START)
    floating_summary_disk_write_speed_label.set_valign(Gtk.Align.START)
    grid_row_count = grid_row_count + 1
    global floating_summary_network_receive_send_speed_label
    floating_summary_network_receive_send_speed_label = Gtk.Label()
    floating_summary_grid.attach(floating_summary_network_receive_send_speed_label, 0, grid_row_count, 1, 1)
    floating_summary_network_receive_send_speed_label.set_halign(Gtk.Align.START)
    floating_summary_network_receive_send_speed_label.set_valign(Gtk.Align.START)
    grid_row_count = grid_row_count + 1
    global floating_summary_network_receive_speed_label
    floating_summary_network_receive_speed_label = Gtk.Label()
    floating_summary_grid.attach(floating_summary_network_receive_speed_label, 0, grid_row_count, 1, 1)
    floating_summary_network_receive_speed_label.set_halign(Gtk.Align.START)
    floating_summary_network_receive_speed_label.set_valign(Gtk.Align.START)
    grid_row_count = grid_row_count + 1
    global floating_summary_network_send_speed_label
    floating_summary_network_send_speed_label = Gtk.Label()
    floating_summary_grid.attach(floating_summary_network_send_speed_label, 0, grid_row_count, 1, 1)
    floating_summary_network_send_speed_label.set_halign(Gtk.Align.START)
    floating_summary_network_send_speed_label.set_valign(Gtk.Align.START)
    grid_row_count = grid_row_count + 1

    # Set floating summary window properties
    floating_summary_window.set_resizable(False)                                              # For preventing window to be resized.
    floating_summary_window.set_skip_taskbar_hint(True)                                       # For hiding window on the taskbar.
    floating_summary_window.set_decorated(False)                                              # For hiding window title, buttons on the title and window border.
    floating_summary_window.set_keep_above(True)                                              # For keeping the window on top of all windows.

    # Define a function for clicking and dragging the window.
    def on_floating_summary_window_button_press_event(widget, event):
        if event.button == 1:
            floating_summary_window.begin_move_drag(event.button, event.x_root, event.y_root, event.time)

    floating_summary_window.connect("button-press-event", on_floating_summary_window_button_press_event)

    floating_summary_window.show_all()
    floating_summary_window.set_opacity(Config.floating_summary_window_transparency)          # Set transperancy of the window.

    floating_summary_define_data_unit_converter_variables_func()                              # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.


# ----------------------------------- FloatingSummary - Loop Function (updates performance data on the floating summary window) -----------------------------------
def floating_summary_loop_func():

    if floating_summary_window.get_visible() == False:
        return

    floating_summary_window.set_opacity(Config.floating_summary_window_transparency)

    global floating_summary_data_shown_prev
    floating_summary_data_shown = Config.floating_summary_data_shown
    if floating_summary_data_shown != floating_summary_data_shown_prev:
        for i in reversed(range(9)):
            try:
                label_to_remove = floating_summary_grid.get_child_at(0, i)
                floating_summary_grid.remove(label_to_remove)
            except:
                pass

        grid_row_count = 0
        if 0 in floating_summary_data_shown:
            grid_row_count = 0
            floating_summary_grid.attach(floating_summary_cpu_label, 0, grid_row_count, 1, 1)
        if 1 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            floating_summary_grid.attach(floating_summary_ram_label, 0, grid_row_count, 1, 1)
        if 2 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            floating_summary_grid.attach(floating_summary_disk_read_write_speed_label, 0, grid_row_count, 1, 1)
        if 3 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            floating_summary_grid.attach(floating_summary_disk_read_speed_label, 0, grid_row_count, 1, 1)
        if 4 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            floating_summary_grid.attach(floating_summary_disk_write_speed_label, 0, grid_row_count, 1, 1)
        if 5 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            floating_summary_grid.attach(floating_summary_network_receive_send_speed_label, 0, grid_row_count, 1, 1)
        if 6 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            floating_summary_grid.attach(floating_summary_network_receive_speed_label, 0, grid_row_count, 1, 1)
        if 7 in floating_summary_data_shown:
            grid_row_count = grid_row_count + 1
            floating_summary_grid.attach(floating_summary_network_send_speed_label, 0, grid_row_count, 1, 1)


    floating_summary_data_shown_prev = list(floating_summary_data_shown)                      # list1 = list(list2) have to be used for proper working of the code because using this equation without "list()" makes a connection between these lists instead of copying one list with a different variable name.

    # Set label text for showing peformance data
    if 0 in floating_summary_data_shown:
        floating_summary_cpu_label.set_text(_tr("CPU: ") + f'{Performance.cpu_usage_percent_ave[-1]:.0f} %')
    if 1 in floating_summary_data_shown:
        floating_summary_ram_label.set_text(_tr("RAM: ") + f'{Performance.ram_usage_percent[-1]:.0f} %')
    if 2 in floating_summary_data_shown:
        floating_summary_disk_read_write_speed_label.set_text(_tr("Disk R+W: ") + f'{floating_summary_data_unit_converter_func((Performance.disk_read_speed[Performance.selected_disk_number][-1] + Performance.disk_write_speed[Performance.selected_disk_number][-1]), 0, 2)}/s')
    if 3 in floating_summary_data_shown:
        floating_summary_disk_read_speed_label.set_text(_tr("Disk R: ") + f'{floating_summary_data_unit_converter_func(Performance.disk_read_speed[Performance.selected_disk_number][-1], 0, 2)}/s')
    if 4 in floating_summary_data_shown:
        floating_summary_disk_write_speed_label.set_text(_tr("Disk W: ") + f'{floating_summary_data_unit_converter_func(Performance.disk_write_speed[Performance.selected_disk_number][-1], 0, 2)}/s')
    if 5 in floating_summary_data_shown:
        floating_summary_network_receive_send_speed_label.set_text(_tr("Network D+U: ") + f'{floating_summary_data_unit_converter_func((Performance.network_receive_speed[Performance.selected_network_card_number][-1] + Performance.network_send_speed[Performance.selected_network_card_number][-1]), 0, 2)}/s')
    if 6 in floating_summary_data_shown:
        floating_summary_network_receive_speed_label.set_text(_tr("Network R: ") + f'{floating_summary_data_unit_converter_func(Performance.network_receive_speed[Performance.selected_network_card_number][-1], 0, 2)}/s')
    if 7 in floating_summary_data_shown:
        floating_summary_network_send_speed_label.set_text(_tr("Network W: ") + f'{floating_summary_data_unit_converter_func(Performance.network_send_speed[Performance.selected_network_card_number][-1], 0, 2)}/s')


# ----------------------------------- FloatingSummary Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def floating_summary_initial_thread_func():

    GLib.idle_add(floating_summary_initial_func)


# ----------------------------------- FloatingSummary Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def floating_summary_loop_thread_func():

    GLib.idle_add(floating_summary_loop_func)
    if floating_summary_window.get_visible() == True:
        GLib.timeout_add(Config.update_interval * 1000, floating_summary_loop_thread_func)


# ----------------------------------- FloatingSummary Thread Run Function (starts execution of the threads) -----------------------------------
def floating_summary_thread_run_func():

#     floating_summary_initial_thread = Thread(target=floating_summary_initial_thread_func, daemon=True)
#     floating_summary_initial_thread.start()
#     floating_summary_initial_thread.join()
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

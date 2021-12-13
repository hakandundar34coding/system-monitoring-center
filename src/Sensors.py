#!/usr/bin/env python3

# ----------------------------------- Sensors - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def sensors_import_func():

    global Gtk, Gdk, GLib, Thread, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib
    from threading import Thread
    import os


    global Config, MainGUI
    from . import Config, MainGUI


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


# ----------------------------------- Sensors - Sensors GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab GUI objects and functions/signals) -----------------------------------
def sensors_gui_func():

    # Sensors tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/SensorsTab.ui")

    # Sensors tab GUI objects
    global grid1601, treeview1601, searchentry1601
    global radiobutton1601, radiobutton1602, radiobutton1603, radiobutton1604
    global label1601

    # Sensors tab GUI objects - get
    grid1601 = builder.get_object('grid1601')
    treeview1601 = builder.get_object('treeview1601')
    searchentry1601 = builder.get_object('searchentry1601')
    radiobutton1601 = builder.get_object('radiobutton1601')
    radiobutton1602 = builder.get_object('radiobutton1602')
    radiobutton1603 = builder.get_object('radiobutton1603')
    radiobutton1604 = builder.get_object('radiobutton1604')
    label1601 = builder.get_object('label1601')


    # Sensors tab GUI functions
    def on_treeview1601_button_release_event(widget, event):
        if event.button == 1:                                                                 # Run the following function if mouse is left clicked on the treeview and the mouse button is released.
            sensors_treeview_column_order_width_row_sorting_func()

    def on_searchentry1601_changed(widget):
        radiobutton1601.set_active(True)
        sensors_treeview_filter_search_func()

    def on_radiobutton1601_toggled(widget):                                                   # "Show all sensors" radiobutton
        if radiobutton1601.get_active() == True:
            searchentry1601.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            sensors_treeview_filter_show_all_func()

    def on_radiobutton1602_toggled(widget):                                                   # "Show all temperature sensors" radiobutton
        if radiobutton1602.get_active() == True:
            searchentry1601.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            sensors_treeview_filter_show_all_func()
            sensors_treeview_filter_only_temperature_sensors_func()

    def on_radiobutton1603_toggled(widget):                                                   # "Show all fan sensors" radiobutton
        if radiobutton1603.get_active() == True:
            searchentry1601.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            sensors_treeview_filter_show_all_func()
            sensors_treeview_filter_only_fan_sensors_func()

    def on_radiobutton1604_toggled(widget):                                                   # "Show all voltage and current sensors" radiobutton
        if radiobutton1604.get_active() == True:
            searchentry1601.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            sensors_treeview_filter_show_all_func()
            sensors_treeview_filter_only_voltage_current_sensors_func()


    # Sensors tab GUI functions - connect
    searchentry1601.connect("changed", on_searchentry1601_changed)
    radiobutton1601.connect("toggled", on_radiobutton1601_toggled)
    radiobutton1602.connect("toggled", on_radiobutton1602_toggled)
    radiobutton1603.connect("toggled", on_radiobutton1603_toggled)
    radiobutton1604.connect("toggled", on_radiobutton1604_toggled)


    # Sensors Tab on Sensors Tab - Treeview Properties
    treeview1601.set_activate_on_single_click(True)
    treeview1601.set_show_expanders(False)                                                    # This command is used for hiding expanders (arrows) at the beginning of the rows. For "Sensors" tab, "child rows" are not used and there is no need for these expanders (they are shown as empty spaces in this situation).
    treeview1601.set_fixed_height_mode(True)                                                  # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview1601.set_headers_clickable(True)
    treeview1601.set_enable_search(True)                                                      # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview1601.set_search_column(2)                                                         # This command used for searching by using entry.
    treeview1601.set_tooltip_column(2)


# ----------------------------------- Sensors - Initial Function (contains initial code which defines some variables and gets data which is not wanted to be run in every loop) -----------------------------------
def sensors_initial_func():

    # data list explanation:
    # sensors_data_list = [
    #                     [treeview column number, treeview column title, internal column count, cell renderer count, treeview column sort column id, [data type 1, data type 2, ...], [cell renderer type 1, cell renderer type 2, ...], [cell attribute 1, cell attribute 2, ...], [cell renderer data 1, cell renderer data 2, ...], [cell left/right alignment 1, cell left/right alignment 2, ...], [set expand 1 {if cell will allocate unused space} cell expand 2, ...], [cell function 1, cell function 2, ...]]
    #                     .
    #                     .
    #                     ]
    global sensors_data_list
    sensors_data_list = [
                        [0, _tr('Sensor Group'), 3, 2, 3, [bool, str, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'icon_name', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
                        [1, _tr('Sensor Name'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [2, _tr('Current Vale'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                        [3, _tr('Critical Value'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                        [4, _tr('Max Value'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']]
                        ]

    global sensors_data_rows_prev, sensors_treeview_columns_shown_prev, sensors_data_row_sorting_column_prev, sensors_data_row_sorting_order_prev, sensors_data_column_order_prev, sensors_data_column_widths_prev
    sensors_data_rows_prev = []
    sensors_treeview_columns_shown_prev = []
    sensors_data_row_sorting_column_prev = ""
    sensors_data_row_sorting_order_prev = ""
    sensors_data_column_order_prev = []
    sensors_data_column_widths_prev = []

    global temperature_sensor_icon_name, fan_sensor_icon_name, voltage_current_sensor_icon_name
    temperature_sensor_icon_name = "system-monitoring-center-temperature-symbolic"
    fan_sensor_icon_name = "system-monitoring-center-fan-symbolic"
    voltage_current_sensor_icon_name = "system-monitoring-center-voltage-symbolic"

    global filter_column
    filter_column = sensors_data_list[0][2] - 1                                               # Search filter is "Sensor Group". "-1" is used because "processes_data_list" has internal column count and it has to be converted to Python index. For example, if there are 3 internal columns but index is 2 for the last internal column number for the relevant treeview column.


# ----------------------------------- Sensors - Get Sensor Data Function (gets sensors data, adds into treeview and updates it) -----------------------------------
def sensors_loop_func():

    # Get GUI obejcts one time per floop instead of getting them multiple times
    global treeview1601

    # Define global variables and get treeview columns, sort column/order, column widths, etc.
    global sensors_treeview_columns_shown
    global sensors_treeview_columns_shown_prev, sensors_data_row_sorting_column_prev, sensors_data_row_sorting_order_prev, sensors_data_column_order_prev, sensors_data_column_widths_prev
    sensors_treeview_columns_shown = Config.sensors_treeview_columns_shown
    sensors_data_row_sorting_column = Config.sensors_data_row_sorting_column
    sensors_data_row_sorting_order = Config.sensors_data_row_sorting_order
    sensors_data_column_order = Config.sensors_data_column_order
    sensors_data_column_widths = Config.sensors_data_column_widths

    # Define global variables and empty lists for the current loop
    global sensors_data_rows, sensor_type_list
    sensors_data_rows = []
    sensor_type_list = []
    supported_sensor_attributes = ["temp", "fan", "in", "curr"]

    # Get sensor data
    sensor_groups = sorted(os.listdir("/sys/class/hwmon/"))                                   # Get sensor group names. In some sensor directories there are a name file and multiple label files. For example, name: "coretemp", label: "Core 0", "Core 1", ... For easier grouping and understanding name is used as "Sensor Group" name and labels are used as "Sensor" names.
    sensor_group_names = []
    for sensor_group in sensor_groups:
        files_in_sensor_group = os.listdir("/sys/class/hwmon/" + sensor_group)
        for attribute in supported_sensor_attributes:
            sensor_number = 0
            while True:                                                                       # Continue loop until code breaks it when next sensor data is not available in the folder.
                string_sensor_number = str(sensor_number)                                     # Convert integer value to string value in order to reduce CPU usage. Because this value is used multiple times.
                if (attribute + string_sensor_number + "_label" not in files_in_sensor_group) and (attribute + string_sensor_number + "_input" not in files_in_sensor_group):    # Some sensor groups have both label and input files. Some sensor groups have only label or only input files. Some sensor groups do not have label or input files, but they have name files. Data of sensor groups with only name files are not get because they do not have sensor values.
                    if sensor_number == 0:                                                    # Number in sensor names may start from 0 or 1. Skipped to next loop if number is 0.
                        sensor_number = sensor_number + 1
                        continue
                    if sensor_number > 0:                                                     # Number in sensor names may start from 0 or 1. Loop is broken if number is bigger than 1.
                        break
                # Get sensor group name
                with open("/sys/class/hwmon/" + sensor_group + "/name") as reader:
                    sensor_group_name = reader.read().strip()
                if attribute == "temp":
                    sensor_type = temperature_sensor_icon_name
                if attribute == "fan":
                    sensor_type = fan_sensor_icon_name
                if attribute == "in" or attribute == "curr":
                    sensor_type = voltage_current_sensor_icon_name
                # Get sensor name
                try:
                    with open("/sys/class/hwmon/" + sensor_group + "/" + attribute + string_sensor_number + "_label") as reader:
                        sensor_name = reader.read().strip()
                except OSError:
                    sensor_name = "-"
                # Get sensor current value
                try:
                    with open("/sys/class/hwmon/" + sensor_group + "/" + attribute + string_sensor_number + "_input") as reader:
                        current_value = int(reader.read().strip())                            # Units of data in this file are millidegree Celcius for temperature sensors, RM for fan sensors, millivolt for voltage sensors and milliamper for current sensors.
                        if attribute == "temp":
                            current_value = f'{(current_value / 1000):.0f} °C'                # Convert millidegree Celcius to degree Celcius and show not numbers after ".".
                        if attribute == "fan":
                            current_value = f'{current_value} RPM'
                        if attribute == "in":
                            current_value = f'{(current_value / 1000):.3f} V'                 # Convert millivolt to Volt and show 3 numbers after ".".
                        if attribute == "curr":
                            current_value = f'{(current_value / 1000):.3f} A'                 # Convert milliamper to Amper and show 3 numbers after ".".
                except OSError:
                    current_value = "-"
                # Get sensor critical value
                try:
                    with open("/sys/class/hwmon/" + sensor_group + "/" + attribute + string_sensor_number + "_crit") as reader:
                        critical_value = int(reader.read().strip())                           # Units of data in this file are millidegree Celcius for temperature sensors, RM for fan sensors, millivolt for voltage sensors and milliamper for current sensors.
                        if attribute == "temp":
                            critical_value = f'{(critical_value / 1000):.0f} °C'              # Convert millidegree Celcius to degree Celcius and show not numbers after ".".
                        if attribute == "fan":
                            critical_value = f'{critical_value} RPM'
                        if attribute == "in":
                            critical_value = f'{(critical_value / 1000):.3f} V'               # Convert millivolt to Volt and show 3 numbers after ".".
                        if attribute == "curr":
                            critical_value = f'{(critical_value / 1000):.3f} A'               # Convert milliamper to Amper and show 3 numbers after ".".
                except OSError:
                    critical_value = "-"
                # Get sensor maximum value
                try:
                    with open("/sys/class/hwmon/" + sensor_group + "/" + attribute + string_sensor_number + "_max") as reader:
                        max_value = int(reader.read().strip())                                # Units of data in this file are millidegree Celcius for temperature sensors, RM for fan sensors, millivolt for voltage sensors and milliamper for current sensors.
                        if attribute == "temp":
                            max_value = f'{(max_value / 1000):.0f} °C'                        # Convert millidegree Celcius to degree Celcius and show not numbers after ".".
                        if attribute == "fan":
                            max_value = f'{max_value} RPM'
                        if attribute == "in":
                            max_value = f'{(max_value / 1000):.3f} V'                         # Convert millivolt to Volt and show 3 numbers after ".".
                        if attribute == "curr":
                            max_value = f'{(max_value / 1000):.3f} A'                         # Convert milliamper to Amper and show 3 numbers after ".".
                except OSError:
                    max_value = "-"


                sensor_type_list.append(sensor_type)                                          # Append sensor type. This information will be used for filtering sensors by type when "Show all temperature/fan/voltage and current sensors" radiobuttons are clicked.
                sensors_data_row = [True, sensor_type, sensor_group_name, sensor_name, current_value, critical_value, max_value]    # Append sensor visibility data (on treeview) which is used for showing/hiding sensor when sensor data of specific sensor type (temperature or fan sensor) is preferred to be shown or sensor search feature is used from the GUI.

                # Append sensor data list into main list
                sensors_data_rows.append(sensors_data_row)

                sensor_number = sensor_number + 1                                             # Increase sensor number by "1" in order to use this value for getting next file names of the sensor.

    # Add/Remove treeview columns appropriate for user preferences
    treeview1601.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    if sensors_treeview_columns_shown != sensors_treeview_columns_shown_prev:                 # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        for column in treeview1601.get_columns():                                             # Remove all columns in the treeview.
            treeview1601.remove_column(column)
        for i, column in enumerate(sensors_treeview_columns_shown):
            if sensors_data_list[column][0] in sensors_treeview_columns_shown:
                cumulative_sort_column_id = cumulative_sort_column_id + sensors_data_list[column][2]
            sensors_treeview_column = Gtk.TreeViewColumn(sensors_data_list[column][1])        # Define column (also column title is defined)
            for i, cell_renderer_type in enumerate(sensors_data_list[column][6]):
                cumulative_internal_data_id = cumulative_internal_data_id + 1
                if cell_renderer_type == "internal_column":                                   # Continue to next loop to avoid generating a cell renderer for internal column (internal columns are not shon on the treeview and they do not have cell renderers).
                    continue
                if cell_renderer_type == "CellRendererPixbuf":                                # Define cell renderer
                    cell_renderer = Gtk.CellRendererPixbuf()
                if cell_renderer_type == "CellRendererText":                                  # Define cell renderer
                    cell_renderer = Gtk.CellRendererText()
                cell_renderer.set_alignment(sensors_data_list[column][9][i], 0.5)             # Vertical alignment is set 0.5 in order to leave it as unchanged.
                sensors_treeview_column.pack_start(cell_renderer, sensors_data_list[column][10][i])    # Set if column will allocate unused space
                sensors_treeview_column.add_attribute(cell_renderer, sensors_data_list[column][7][i], cumulative_internal_data_id)
                if sensors_data_list[column][11][i] != "no_cell_function":
                    sensors_treeview_column.set_cell_data_func(cell_renderer, sensors_data_list[column][11][i], func_data=cumulative_internal_data_id)    # Define cell function which sets cell data precision and/or data unit
            sensors_treeview_column.set_sizing(2)                                             # Set column sizing (2 = auto sizing which is required for "treeview1601.set_fixed_height_mode(True)" command that is used for lower treeview CPU consumption because row heights are not calculated for every row).
            sensors_treeview_column.set_sort_column_id(cumulative_sort_column_id)             # Be careful with lists contain same element more than one.
            sensors_treeview_column.set_resizable(True)                                       # Set columns resizable by the user when column title button edge handles are dragged.
            sensors_treeview_column.set_reorderable(True)                                     # Set columns reorderable by the user when column title buttons are dragged.
            sensors_treeview_column.set_min_width(40)                                         # Set minimum column widths as "40 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            sensors_treeview_column.connect("clicked", on_column_title_clicked)               # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
            treeview1601.append_column(sensors_treeview_column)                               # Append column into treeview

        # Get column data types for appending sensors data into treestore
        sensors_data_column_types = []
        for column in sorted(sensors_treeview_columns_shown):
            internal_column_count = len(sensors_data_list[column][5])
            for internal_column_number in range(internal_column_count):
                sensors_data_column_types.append(sensors_data_list[column][5][internal_column_number])    # Get column types (int, bool, float, str, etc.)

        # Define a treestore (for storing treeview data in it), a treemodelfilter (for search filtering), treemodelsort (for row sorting when column title buttons are clicked)
        global treestore1601                                                                  # Define as global variable because treestore is generated in statement and will not be defined in every loop and it will be used outside the statement.
        treestore1601 = Gtk.TreeStore()
        treestore1601.set_column_types(sensors_data_column_types)                             # Set column types of the columns which will be appended into treestore
        treemodelfilter1601 = treestore1601.filter_new()
        treemodelfilter1601.set_visible_column(0)                                             # Column "0" of the treestore will be used for column visibility information (True or False)
        treemodelsort1601 = Gtk.TreeModelSort(treemodelfilter1601)
        treeview1601.set_model(treemodelsort1601)
        global piter_list
        piter_list = []
    treeview1601.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
    if sensors_treeview_columns_shown_prev != sensors_treeview_columns_shown or sensors_data_column_order_prev != sensors_data_column_order:
        sensors_treeview_columns = treeview1601.get_columns()                                 # Get shown columns on the treeview in order to use this data for reordering the columns.
        sensors_treeview_columns_modified = treeview1601.get_columns()
        treeview_column_titles = []
        for column in sensors_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for order in reversed(sorted(sensors_data_column_order)):                             # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
            if sensors_data_column_order.index(order) <= len(sensors_treeview_columns) - 1 and sensors_data_column_order.index(order) in sensors_treeview_columns_shown:
                column_number_to_move = sensors_data_column_order.index(order)
                column_title_to_move = sensors_data_list[column_number_to_move][1]
                column_to_move = sensors_treeview_columns[treeview_column_titles.index(column_title_to_move)]
                column_title_to_move = column_to_move.get_title()
                for data in sensors_data_list:
                    if data[1] == column_title_to_move:
                        treeview1601.move_column_after(column_to_move, None)                  # Column is moved at the beginning of the treeview if "None" is used.

    # Sort sensor rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
    if sensors_treeview_columns_shown_prev != sensors_treeview_columns_shown or sensors_data_row_sorting_column_prev != sensors_data_row_sorting_column or sensors_data_row_sorting_order != sensors_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
        sensors_treeview_columns = treeview1601.get_columns()                                 # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_column_titles = []
        for column in sensors_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i in range(10):
            if sensors_data_row_sorting_column in sensors_treeview_columns_shown:
                for data in sensors_data_list:
                    if data[0] == sensors_data_row_sorting_column:
                        column_title_for_sorting = data[1]
            if sensors_data_row_sorting_column not in sensors_treeview_columns_shown:
                column_title_for_sorting = sensors_data_list[0][1]
            column_for_sorting = sensors_treeview_columns[treeview_column_titles.index(column_title_for_sorting)]
            column_for_sorting.clicked()                                                      # For row sorting.
            if sensors_data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                break

    # Set column widths if there are changes since last loop.
    if sensors_treeview_columns_shown_prev != sensors_treeview_columns_shown or sensors_data_column_widths_prev != sensors_data_column_widths:
        sensors_treeview_columns = treeview1601.get_columns()
        treeview_column_titles = []
        for column in sensors_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i, sensors_data in enumerate(sensors_data_list):
            for j, column_title in enumerate(treeview_column_titles):
                if column_title == sensors_data[1]:
                   column_width = sensors_data_column_widths[i]
                   sensors_treeview_columns[j].set_fixed_width(column_width)                  # Set column width in pixels. Fixed width is unset if value is "-1".

    # Clear piter_list and treestore because sensor data (new/removed) tracking is not performed. Because there may be same named sensors and tracking may not be successful while sensors have no unique identity (more computer examples are needed for understanding if sensors have unique information). PCI tree path could be get from sensor files but this may not be worth because code will be more complex and it may not be an exact solution for all sensors. Also CPU usage is very low (about 0.67-0.84%, tested on Core i7-2630QM 4-core notebook) even treestore is cleared and sensor data is appended from zero.
    treeview1601.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    piter_list = []
    treestore1601.clear()
    # Append sensor data into treeview
    for sensors_data_row in sensors_data_rows:
        # /// Start /// This block of code is used for determining if the newly added sensor will be shown on the treeview (sensor search actions and/or search customizations and/or "Show only temperature/fan sensors" preference affect sensor visibility).
        if radiobutton1602.get_active() == True and sensor_type_list[sensors_data_rows.index(sensors_data_row)] != temperature_sensor_icon_name:    # Hide sensor (set the visibility value as "False") if "Show all temperature sensors" option is selected on the GUI and sensor type is not temperature.
            sensors_data_row[0] = False
        if radiobutton1603.get_active() == True and sensor_type_list[sensors_data_rows.index(sensors_data_row)] != fan_sensor_icon_name:    # Hide sensor (set the visibility value as "False") if "Show all fan sensors" option is selected on the GUI and sensor type is not fan.
            sensors_data_row[0] = False
        if radiobutton1604.get_active() == True and sensor_type_list[sensors_data_rows.index(sensors_data_row)] != voltage_current_sensor_icon_name:    # Hide sensor (set the visibility value as "False") if "Show all voltage and current sensors" option is selected on the GUI and sensor type is not voltage or current.
            sensors_data_row[0] = False
        if searchentry1601.get_text() != "":
            sensor_search_text = searchentry1601.get_text()
            sensor_data_text_in_model = sensors_data_row[filter_column]
            if sensor_search_text not in str(sensor_data_text_in_model).lower():              # Hide sensor (set the visibility value as "False") if search text (typed into the search entry) is not in the appropriate column of the sensor.
                sensors_data_row[0] = False
        # \\\ End \\\ This block of code is used for determining if the newly added sensor will be shown on the treeview (user search actions and/or search customizations and/or "Show onlt temperature/fan sensors" preference affect sensor visibility).
        piter_list.append(treestore1601.append(None, sensors_data_row))                       # All sensors are appended into treeview as tree root for listing sensor data as list (there is no tree view option for sensors tab).
    treeview1601.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    sensors_treeview_columns_shown_prev = sensors_treeview_columns_shown
    sensors_data_row_sorting_column_prev = sensors_data_row_sorting_column
    sensors_data_row_sorting_order_prev = sensors_data_row_sorting_order
    sensors_data_column_order_prev = sensors_data_column_order
    sensors_data_column_widths_prev = sensors_data_column_widths

    # Get number of all/temperature/fan sensors and show these information on the GUI label
    temperature_sensors_count = sensor_type_list.count(temperature_sensor_icon_name)
    fan_sensors_count = sensor_type_list.count(fan_sensor_icon_name)
    voltage_and_current_sensors_count = sensor_type_list.count(voltage_current_sensor_icon_name)
    number_of_all_sensors = len(sensor_type_list)
    label1601.set_text(_tr("Total: ") + str(number_of_all_sensors) + _tr(" sensors (") + str(temperature_sensors_count) + _tr(" temperature, ") + str(fan_sensors_count) + _tr(" fan, ") + str(voltage_and_current_sensors_count) + _tr(" voltage/current sensors)"))    # f strings have lower CPU usage than joining method but strings are joinied by by this method because gettext could not be worked with Python f strings.


# ----------------------------------- Sensors Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def sensors_initial_thread_func():

    GLib.idle_add(sensors_initial_func)


# ----------------------------------- Sensors Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def sensors_loop_thread_func(*args):                                                          # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when a tab is switched off and on again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

    if MainGUI.radiobutton1.get_active() == True and MainGUI.radiobutton1006.get_active() == True:
        global sensors_glib_source, update_interval                                           # GLib source variable name is defined as global to be able to destroy it if tab is switched back in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            sensors_glib_source.destroy()                                                     # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        sensors_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(sensors_loop_func)
        sensors_glib_source.set_callback(sensors_loop_thread_func)
        sensors_glib_source.attach(GLib.MainContext.default())                                # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.


# ----------------------------------- Sensors Thread Run Function (starts execution of the threads) -----------------------------------
def sensors_thread_run_func():

    if "sensors_data_rows" not in globals():                                                  # To be able to run initial thread for only one time
        sensors_initial_thread = Thread(target=sensors_initial_thread_func, daemon=True)
        sensors_initial_thread.start()
        sensors_initial_thread.join()
    sensors_loop_thread = Thread(target=sensors_loop_thread_func, daemon=True)
    sensors_loop_thread.start()


# ----------------------------------- Sensors - Treeview Filter Show All Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def sensors_treeview_filter_show_all_func():

    for piter in piter_list:
        treestore1601.set_value(piter, 0, True)
    treeview1601.expand_all()


# ----------------------------------- Sensors - Treeview Filter Only Temperature Sensors Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def sensors_treeview_filter_only_temperature_sensors_func():

    for piter in piter_list:
        if sensor_type_list[piter_list.index(piter)] != temperature_sensor_icon_name:
            treestore1601.set_value(piter, 0, False)
    treeview1601.expand_all()


# ----------------------------------- Sensors - Treeview Filter Only Fan Sensors Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def sensors_treeview_filter_only_fan_sensors_func():

    for piter in piter_list:
        if sensor_type_list[piter_list.index(piter)] != fan_sensor_icon_name:
            treestore1601.set_value(piter, 0, False)
    treeview1601.expand_all()


# ----------------------------------- Sensors - Treeview Filter Only Voltage and Current Sensors Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def sensors_treeview_filter_only_voltage_current_sensors_func():

    for piter in piter_list:
        if sensor_type_list[piter_list.index(piter)] != voltage_current_sensor_icon_name:
            treestore1601.set_value(piter, 0, False)
    treeview1601.expand_all()


# ----------------------------------- Sensors - Treeview Filter Search Function (updates treeview shown rows when text typed into entry) -----------------------------------
def sensors_treeview_filter_search_func():

    global filter_column
    sensor_search_text = searchentry1601.get_text().lower()
    # Set visible/hidden sensor data
    for piter in piter_list:
        treestore1601.set_value(piter, 0, False)
        sensor_data_text_in_model = treestore1601.get_value(piter, filter_column)
        if sensor_search_text in str(sensor_data_text_in_model).lower():
            treestore1601.set_value(piter, 0, True)

    treeview1601.expand_all()                                                                 # Expand all treeview rows (if tree view is preferred) after filtering is applied (after any text is typed into search entry).


# ----------------------------------- Sensors - Column Title Clicked Function (gets treeview column number (id) and row sorting order by being triggered by Gtk signals) -----------------------------------
def on_column_title_clicked(widget):

    sensors_data_row_sorting_column_title = widget.get_title()                                # Get column title which will be used for getting column number
    for data in sensors_data_list:
        if data[1] == sensors_data_row_sorting_column_title:
            Config.sensors_data_row_sorting_column = data[0]                                  # Get column number
    Config.sensors_data_row_sorting_order = int(widget.get_sort_order())                      # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    Config.config_save_func()


# ----------------------------------- Sensors - Treeview Column Order-Width Row Sorting Function (gets treeview column order/widths and row sorting) -----------------------------------
def sensors_treeview_column_order_width_row_sorting_func():
    # Columns in the treeview are get one by one and appended into "sensors_data_column_order". "sensors_data_column_widths" list elements are modified for widths of every columns in the treeview. Length of these list are always same even if columns are removed, appended and column widths are changed. Only values of the elements (element indexes are always same with "sensors_data") are changed if column order/widths are changed.
    sensors_treeview_columns = treeview1601.get_columns()
    treeview_column_titles = []
    for column in sensors_treeview_columns:
        treeview_column_titles.append(column.get_title())
    for i, sensors_data in enumerate(sensors_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == sensors_data[1]:
                Config.sensors_data_column_order[i] = j
                Config.sensors_data_column_widths[i] = sensors_treeview_columns[j].get_width()
                break
    Config.config_save_func()

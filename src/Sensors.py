#!/usr/bin/env python3

# ----------------------------------- Sensors - Import Function -----------------------------------
def sensors_import_func():

    global Gtk, GLib, os

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GLib', '2.0')
    from gi.repository import Gtk, GLib
    import os


    global Config
    from Config import Config


    global _tr
    from locale import gettext as _tr


# ----------------------------------- Sensors - Sensors GUI Function -----------------------------------
def sensors_gui_func():

    # Sensors tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/SensorsTab.ui")

    # Sensors tab GUI objects
    global grid1601, treeview1601, searchentry1601

    # Sensors tab GUI objects - get
    grid1601 = builder.get_object('grid1601')
    treeview1601 = builder.get_object('treeview1601')
    searchentry1601 = builder.get_object('searchentry1601')

    # Sensors tab GUI functions - connect
    searchentry1601.connect("changed", on_searchentry1601_changed)

    # Sensors Tab on Sensors Tab - Treeview Properties
    treeview1601.set_activate_on_single_click(True)
    treeview1601.set_show_expanders(False)
    treeview1601.set_fixed_height_mode(True)
    treeview1601.set_headers_clickable(True)
    treeview1601.set_enable_search(True)
    treeview1601.set_search_column(2)
    treeview1601.set_tooltip_column(2)

    global initial_already_run
    initial_already_run = 0


# --------------------------------- Called for running code/functions when button is released on the treeview ---------------------------------
def on_treeview1601_button_release_event(widget, event):

    # Check if left mouse button is used
    if event.button == 1:
        sensors_treeview_column_order_width_row_sorting_func()


# --------------------------------- Called for searching items when searchentry text is changed ---------------------------------
def on_searchentry1601_changed(widget):

    # Get search text
    sensor_search_text = searchentry1601.get_text().lower()
    # Set visible/hidden sensor data
    for piter in piter_list:
        treestore1601.set_value(piter, 0, False)
        sensor_data_text_in_model = treestore1601.get_value(piter, filter_column)
        if sensor_search_text in str(sensor_data_text_in_model).lower():
            treestore1601.set_value(piter, 0, True)


# ----------------------------------- Sensors - Initial Function -----------------------------------
def sensors_initial_func():

    global sensors_data_list
    sensors_data_list = [
                        [0, _tr('Sensor Group'), 3, 2, 3, [bool, str, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'icon_name', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
                        [1, _tr('Name'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                        [2, _tr('Current Value'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                        [3, _tr('High'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                        [4, _tr('Critical'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']]
                        ]

    global sensors_data_rows_prev, sensors_treeview_columns_shown_prev, sensors_data_row_sorting_column_prev, sensors_data_row_sorting_order_prev, sensors_data_column_order_prev, sensors_data_column_widths_prev
    sensors_data_rows_prev = []
    sensors_treeview_columns_shown_prev = []
    sensors_data_row_sorting_column_prev = ""
    sensors_data_row_sorting_order_prev = ""
    sensors_data_column_order_prev = []
    sensors_data_column_widths_prev = []

    global temperature_sensor_icon_name, fan_sensor_icon_name, voltage_current_power_sensor_icon_name
    temperature_sensor_icon_name = "system-monitoring-center-temperature-symbolic"
    fan_sensor_icon_name = "system-monitoring-center-fan-symbolic"
    voltage_current_power_sensor_icon_name = "system-monitoring-center-voltage-symbolic"

    global filter_column
    filter_column = sensors_data_list[0][2] - 1                                               # Search filter is "Sensor Group". "-1" is used because "sensors_data_list" has internal column count and it has to be converted to Python index. For example, if there are 3 internal columns but index is 2 for the last internal column number for the relevant treeview column.

    global initial_already_run
    initial_already_run = 1


# ----------------------------------- Sensors - Get Sensor Data Function -----------------------------------
def sensors_loop_func():

    update_interval = Config.update_interval

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
    supported_sensor_attributes = ["temp", "fan", "in", "curr", "power"]

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
                if attribute in ["in", "curr", "power"]:
                    sensor_type = voltage_current_power_sensor_icon_name
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
                        current_value = f'{(current_value / 1000):.0f} °C'                    # Convert millidegree Celcius to degree Celcius and show not numbers after ".".
                    if attribute == "fan":
                        current_value = f'{current_value} RPM'
                    if attribute == "in":
                        current_value = f'{(current_value / 1000):.3f} V'                     # Convert millivolt to Volt and show 3 numbers after ".".
                    if attribute == "curr":
                        current_value = f'{(current_value / 1000):.3f} A'                     # Convert milliamper to Amper and show 3 numbers after ".".
                    if attribute == "power":
                        current_value = f'{(current_value / 1000000):.3f} W'                  # Convert microwatt to Watt and show 3 numbers after ".".
                except OSError:
                    current_value = "-"
                # Get sensor high value
                try:
                    with open("/sys/class/hwmon/" + sensor_group + "/" + attribute + string_sensor_number + "_max") as reader:
                        max_value = int(reader.read().strip())
                    if attribute == "temp":
                        max_value = f'{(max_value / 1000):.0f} °C'
                    if attribute == "fan":
                        max_value = f'{max_value} RPM'
                    if attribute == "in":
                        max_value = f'{(max_value / 1000):.3f} V'
                    if attribute == "curr":
                        max_value = f'{(max_value / 1000):.3f} A'
                    if attribute == "power":
                        max_value = f'{(max_value / 1000000):.3f} W'
                except OSError:
                    max_value = "-"
                # Get sensor critical value
                try:
                    with open("/sys/class/hwmon/" + sensor_group + "/" + attribute + string_sensor_number + "_crit") as reader:
                        critical_value = int(reader.read().strip())
                    if attribute == "temp":
                        critical_value = f'{(critical_value / 1000):.0f} °C'
                    if attribute == "fan":
                        critical_value = f'{critical_value} RPM'
                    if attribute == "in":
                        critical_value = f'{(critical_value / 1000):.3f} V'
                    if attribute == "curr":
                        critical_value = f'{(critical_value / 1000):.3f} A'
                    if attribute == "power":
                        critical_value = f'{(critical_value / 1000000):.3f} W'
                except OSError:
                    critical_value = "-"


                sensor_type_list.append(sensor_type)                                          # Append sensor type. This information will be used for filtering sensors by type when "Show all temperature/fan/voltage and current sensors" radiobuttons are clicked.
                sensors_data_row = [True, sensor_type, sensor_group_name, sensor_name, current_value, max_value, critical_value]    # Append sensor visibility data (on treeview) which is used for showing/hiding sensor when sensor data of specific sensor type (temperature or fan sensor) is preferred to be shown or sensor search feature is used from the GUI.

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
            sensors_treeview_column.set_min_width(50)                                         # Set minimum column widths as "50 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
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
        treeview_column_titles = []
        for column in sensors_treeview_columns:
            treeview_column_titles.append(column.get_title())
        sensors_data_column_order_scratch = []
        for column_order in sensors_data_column_order:
            if column_order != -1:
                sensors_data_column_order_scratch.append(column_order)
        for order in reversed(sorted(sensors_data_column_order_scratch)):                     # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
            if sensors_data_column_order.index(order) in sensors_treeview_columns_shown:
                column_number_to_move = sensors_data_column_order.index(order)
                column_title_to_move = sensors_data_list[column_number_to_move][1]
                column_to_move = sensors_treeview_columns[treeview_column_titles.index(column_title_to_move)]
                treeview1601.move_column_after(column_to_move, None)                          # Column is moved at the beginning of the treeview if "None" is used.

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
        piter_list.append(treestore1601.append(None, sensors_data_row))                       # All sensors are appended into treeview as tree root for listing sensor data as list (there is no tree view option for sensors tab).
    on_searchentry1601_changed(searchentry1601)                                           # Update search results.
    treeview1601.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    sensors_treeview_columns_shown_prev = sensors_treeview_columns_shown
    sensors_data_row_sorting_column_prev = sensors_data_row_sorting_column
    sensors_data_row_sorting_order_prev = sensors_data_row_sorting_order
    sensors_data_column_order_prev = sensors_data_column_order
    sensors_data_column_widths_prev = sensors_data_column_widths

    # Show number of sensors on the searchentry as placeholder text
    searchentry1601.set_placeholder_text(_tr("Search...") + "                    " + "(" + _tr("Sensors") + ": " + str(len(sensor_type_list)) + ")")


# ----------------------------------- Sensors - Column Title Clicked Function -----------------------------------
def on_column_title_clicked(widget):

    sensors_data_row_sorting_column_title = widget.get_title()                                # Get column title which will be used for getting column number
    for data in sensors_data_list:
        if data[1] == sensors_data_row_sorting_column_title:
            Config.sensors_data_row_sorting_column = data[0]                                  # Get column number
    Config.sensors_data_row_sorting_order = int(widget.get_sort_order())                      # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    Config.config_save_func()


# ----------------------------------- Sensors - Treeview Column Order-Width Row Sorting Function -----------------------------------
def sensors_treeview_column_order_width_row_sorting_func():

    sensors_treeview_columns = treeview1601.get_columns()
    treeview_column_titles = []
    for column in sensors_treeview_columns:
        treeview_column_titles.append(column.get_title())

    sensors_data_column_order = [-1] * len(sensors_data_list)
    sensors_data_column_widths = [-1] * len(sensors_data_list)

    sensors_treeview_columns_last_index = len(sensors_treeview_columns)-1

    for i, sensors_data in enumerate(sensors_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == sensors_data[1]:
                column_index = treeview_column_titles.index(sensors_data[1])
                sensors_data_column_order[i] = column_index
                if j != sensors_treeview_columns_last_index:
                    sensors_data_column_widths[i] = sensors_treeview_columns[column_index].get_width()

    Config.sensors_data_column_order = list(sensors_data_column_order)
    Config.sensors_data_column_widths = list(sensors_data_column_widths)
    Config.config_save_func()


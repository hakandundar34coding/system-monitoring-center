import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import os

from .Config import Config
from .MainWindow import MainWindow
from . import Common

_tr = Config._tr


class Sensors:

    def __init__(self):

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_grid = Common.tab_grid()

        self.tab_title_grid()

        self.tab_info_grid()

        self.gui_signals()


    def tab_title_grid(self):
        """
        Generate tab name label and searchentry.
        """

        # Grid (tab title)
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.tab_grid.attach(grid, 0, 0, 1, 1)

        # Label (Sensors)
        label = Common.tab_title_label(_tr("Sensors"))
        grid.attach(label, 0, 0, 1, 1)

        # SearchEntry
        self.searchentry = Common.searchentry(self.on_searchentry_changed)
        grid.attach(self.searchentry, 1, 0, 1, 1)


    def tab_info_grid(self):
        """
        Generate information GUI objects.
        """

        # ScrolledWindow
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.tab_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # TreeView
        self.treeview = Gtk.TreeView()
        self.treeview.set_activate_on_single_click(True)
        self.treeview.set_show_expanders(False)
        self.treeview.set_fixed_height_mode(True)
        self.treeview.set_headers_clickable(True)
        self.treeview.set_enable_search(True)
        self.treeview.set_search_column(2)
        self.treeview.set_tooltip_column(2)
        scrolledwindow.set_child(self.treeview)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # SeachEntry focus action and accelerator
        Common.searchentry_focus_action_and_accelerator(MainWindow)


    def on_searchentry_changed(self, widget):
        """
        Called by searchentry when text is changed.
        """

        sensor_search_text = self.searchentry.get_text().lower()

        # Set visible/hidden sensor data
        for piter in self.piter_list:
            self.treestore.set_value(piter, 0, False)
            sensor_data_text_in_model = self.treestore.get_value(piter, self.filter_column)
            if sensor_search_text in str(sensor_data_text_in_model).lower():
                self.treestore.set_value(piter, 0, True)


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.row_data_list = [
                             [0, _tr('Device'), 3, 2, 3, [bool, str, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'icon_name', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
                             [1, _tr('Name'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                             [2, _tr('Current Value'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                             [3, _tr('High'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                             [4, _tr('Critical'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']]
                             ]

        self.tab_data_rows_prev = []
        self.treeview_columns_shown_prev = []
        self.data_row_sorting_column_prev = ""
        self.data_row_sorting_order_prev = ""
        self.data_column_order_prev = []
        self.data_column_widths_prev = []

        self.supported_sensor_attributes = ["temp", "fan", "in", "curr", "power"]

        global temperature_sensor_icon_name, fan_sensor_icon_name, voltage_current_power_sensor_icon_name
        temperature_sensor_icon_name = "system-monitoring-center-temperature-symbolic"
        fan_sensor_icon_name = "system-monitoring-center-fan-symbolic"
        voltage_current_power_sensor_icon_name = "system-monitoring-center-voltage-symbolic"

        self.filter_column = self.row_data_list[0][2] - 1

        self.initial_already_run = 1


    def loop_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        update_interval = Config.update_interval

        # Define global variables and get treeview columns, sort column/order, column widths, etc.
        self.treeview_columns_shown = Config.sensors_treeview_columns_shown
        self.data_row_sorting_column = Config.sensors_data_row_sorting_column
        self.data_row_sorting_order = Config.sensors_data_row_sorting_order
        self.data_column_order = Config.sensors_data_column_order
        self.data_column_widths = Config.sensors_data_column_widths
        # For obtaining lower CPU usage
        treeview_columns_shown = self.treeview_columns_shown
        treeview_columns_shown = set(treeview_columns_shown)

        # Get sensor data
        tab_data_rows = []
        sensor_groups = sorted(os.listdir("/sys/class/hwmon/"))                                   # Get sensor group names. In some sensor directories there are a name file and multiple label files. For example, name: "coretemp", label: "Core 0", "Core 1", ... For easier grouping and understanding name is used as "Sensor Group" name and labels are used as "Sensor" names.
        sensor_group_names = []
        for sensor_group in sensor_groups:
            files_in_sensor_group = os.listdir("/sys/class/hwmon/" + sensor_group)
            for attribute in self.supported_sensor_attributes:
                sensor_number = 0
                while True:                                                                       # Continue loop until code breaks it when next sensor data is not available in the folder.
                    string_sensor_number = str(sensor_number)                                     # Convert integer value to string value in order to reduce CPU usage. Because this value is used multiple times.
                    if (attribute + string_sensor_number + "_label" not in files_in_sensor_group) and (attribute + string_sensor_number + "_input" not in files_in_sensor_group):    # Some sensor groups have both label and input files. Some sensor groups have only label or only input files. Some sensor groups do not have label or input files, but they have name files. Data of sensor groups with only name files are not get because they do not have sensor values.
                        if sensor_number == 0:                                                    # Number in sensor names may start from 0 or 1. Skipped to next loop if number is 0.
                            sensor_number = sensor_number + 1
                            continue
                        if sensor_number > 0:                                                     # Number in sensor names may start from 0 or 1. Loop is broken if number is bigger than 1.
                            break
                    # Get device name
                    with open("/sys/class/hwmon/" + sensor_group + "/name") as reader:
                        sensor_group_name = reader.read().strip()
                    if attribute == "temp":
                        sensor_type = temperature_sensor_icon_name
                    if attribute == "fan":
                        sensor_type = fan_sensor_icon_name
                    if attribute in ["in", "curr", "power"]:
                        sensor_type = voltage_current_power_sensor_icon_name
                    # Get device detailed name
                    device_path = os.readlink("/sys/class/hwmon/" + sensor_group)
                    device_detailed_name = device_path.split("/")[-2]
                    if device_detailed_name.startswith("hwmon") == True:
                        device_detailed_name = device_path.split("/")[-3]
                        if device_detailed_name.startswith("hwmon") == True:
                            device_detailed_name = "-"
                    if device_detailed_name != "-" and device_detailed_name.startswith("0000:") == False:
                        sensor_group_name = device_detailed_name + " ( " + sensor_group_name + " )"
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


                    tab_data_row = [True, sensor_type, sensor_group_name, sensor_name, current_value, max_value, critical_value]    # Append sensor visibility data (on treeview) which is used for showing/hiding sensor when sensor data of specific sensor type (temperature or fan sensor) is preferred to be shown or sensor search feature is used from the GUI.

                    # Append sensor data list into main list
                    tab_data_rows.append(tab_data_row)

                    sensor_number = sensor_number + 1                                             # Increase sensor number by "1" in order to use this value for getting next file names of the sensor.

        self.tab_data_rows = tab_data_rows

        # Convert set to list (it was set before getting process information)
        treeview_columns_shown = sorted(list(treeview_columns_shown))

        reset_row_unique_data_list_prev = Common.treeview_add_remove_columns(self)
        Common.treeview_reorder_columns_sort_rows_set_column_widths(self)

        # Clear piter_list and treestore because sensor data (new/removed) tracking is not performed. Because there may be same named sensors and tracking may not be successful while sensors have no unique identity (more computer examples are needed for understanding if sensors have unique information). PCI tree path could be get from sensor files but this may not be worth because code will be more complex and it may not be an exact solution for all sensors. Also CPU usage is very low (about 0.67-0.84%, tested on Core i7-2630QM 4-core notebook) even treestore is cleared and sensor data is appended from zero.
        self.piter_list = []
        self.treestore.clear()

        # Append sensor data into treeview
        for tab_data_row in tab_data_rows:
            self.piter_list.append(self.treestore.append(None, tab_data_row))
        # Update search results.
        self.on_searchentry_changed(self.searchentry)

        Common.searchentry_update_placeholder_text(self)

        self.treeview_columns_shown_prev = treeview_columns_shown
        self.data_row_sorting_column_prev = self.data_row_sorting_column
        self.data_row_sorting_order_prev = self.data_row_sorting_order
        self.data_column_order_prev = self.data_column_order
        self.data_column_widths_prev = self.data_column_widths


Sensors = Sensors()


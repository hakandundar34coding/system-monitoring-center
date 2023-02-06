import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gio', '2.0')
gi.require_version('GObject', '2.0')
from gi.repository import Gtk, Gio, GObject

import os
import locale

from locale import gettext as _tr

from Config import Config
import Common


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
        self.searchentry = Common.scrolledwindow_searchentry(self.on_searchentry_changed)
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

        # ColumnView
        self.columnview = Gtk.ColumnView()
        self.columnview.add_css_class("data-table")
        scrolledwindow.set_child(self.columnview)


    def on_searchentry_changed(self, widget):
        """
        Called by searchentry when text is changed.
        """

        self.search_text = self.searchentry.get_text().lower()


    def factory_string(self, cell_data):
        """
        Generate and connect column signals.
        """

        factory_string = Gtk.SignalListItemFactory()
        factory_string.connect("setup", self.on_factory_string_setup)
        factory_string.connect("bind", self.on_factory_string_bind, cell_data)
        factory_string.connect("unbind", self.on_factory_string_unbind, cell_data)
        factory_string.connect("teardown", self.on_factory_string_teardown)

        return factory_string


    def on_factory_string_setup(self, factory, list_item):
        """
        Generate child widget of the list item.
        """

        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        label._binding = None
        list_item.set_child(label)


    def on_factory_string_bind(self, factory, list_item, cell_data):
        """
        Bind the list item to the row widget.
        """

        label = list_item.get_child()
        # Second "get_item()" is used because "TreeListRowSorter" is used.
        list_data = list_item.get_item().get_item()
        #label.set_label(f'{list_data.device_name}')
        label._binding = list_data.bind_property(cell_data, label, "label", GObject.BindingFlags.SYNC_CREATE)


    def on_factory_string_unbind(self, factory, list_item, cell_data):
        """
        Unbind the the row widget.
        """

        label = list_item.get_child()
        if label._binding:
            label._binding.unbind()
            label._binding = None


    def on_factory_string_teardown(self, factory, list_item):
        """
        Teardown child widget of the list item.
        """
        return
        label = list_item.get_child()
        label._binding = None


    def factory_image_string(self, cell_data):
        """
        Generate and connect column signals.
        """

        factory_image_string = Gtk.SignalListItemFactory()
        factory_image_string.connect("setup", self.on_factory_image_string_setup)
        factory_image_string.connect("bind", self.on_factory_image_string_bind, cell_data)
        factory_image_string.connect("unbind", self.on_factory_image_string_unbind, cell_data)
        factory_image_string.connect("teardown", self.on_factory_image_string_teardown)

        return factory_image_string


    def on_factory_image_string_setup(self, factory, list_item):
        """
        Generate child widget of the list item.
        """

        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        image = Gtk.Image()
        image.set_halign(Gtk.Align.START)
        grid = Gtk.Grid(column_spacing=2)
        grid.attach(image, 0, 0, 1, 1)
        grid.attach(label, 1, 0, 1, 1)
        list_item.set_child(grid)


    def on_factory_image_string_bind(self, factory, list_item, cell_data):
        """
        Bind the list item to the row widget.
        """

        grid = list_item.get_child()
        image = grid.get_child_at(0, 0)
        label = grid.get_child_at(1, 0)
        # Second "get_item()" is used because "TreeListRowSorter" is used.
        list_data = list_item.get_item().get_item()
        #image.set_from_icon_name(list_data.sensor_image)
        #label.set_label(list_data.sensor_name)
        list_data.bind_property(cell_data[0], image, "icon-name", GObject.BindingFlags.SYNC_CREATE)
        list_data.bind_property(cell_data[1], label, "label", GObject.BindingFlags.SYNC_CREATE)


    def on_factory_image_string_unbind(self, factory, list_item, cell_data):
        """
        Unbind the the row widget.
        """
        return
        label = list_item.get_child()
        if label._binding:
            label._binding.unbind()
            label._binding = None


    def on_factory_image_string_teardown(self, factory, list_item):
        """
        Teardown child widget of the list item.
        """
        return
        label = list_item.get_child()
        label._binding = None


    def model_func(self, item):

        pass


    def sort_func(self, a, b, cell_data):
        """
        Sort values (integer, float, string, etc.).
        "locale.strxfrm" function is used for locale-aware sorting.
        """

        first = a.get_property(cell_data)
        second = b.get_property(cell_data)

        if isinstance(first, str) == True:
            first = locale.strxfrm(first.lower())
            second = locale.strxfrm(second.lower())

        if first > second:
            return Gtk.Ordering.LARGER
        elif first < second:
            return Gtk.Ordering.SMALLER
        else:
            return Gtk.Ordering.EQUAL


    def filter_func(self, item, cell_data):
        """
        Show/Hide rows by checking search text.
        """

        item = item.get_item()
        cell_value = item.get_property(cell_data)

        return self.search_text in cell_value


    def sensors_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        global sensors_data_list
        sensors_data_list = [
                            [0, _tr('Device'), self.factory_image_string, ["sensor_image", "device_name"]],
                            [1, _tr('Name'), self.factory_string, "sensor_name"],
                            [2, _tr('Current Value'), self.factory_string, "sensor_current_value"],
                            [3, _tr('High'), self.factory_string, "sensor_high"],
                            [4, _tr('Critical'), self.factory_string, "sensor_critical"]
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

        # ListStore and TreeListModel (for tree structure)
        self.liststore = Gio.ListStore(item_type=Sensor)
        treelistmodel = Gtk.TreeListModel.new(self.liststore, False, True, self.model_func)

        # FilterListModel
        self.filterlistmodel = Gtk.FilterListModel()
        self.filterlistmodel.set_model(treelistmodel)

        # TreeListRowSorter
        columnview_sorter = self.columnview.get_sorter()
        treelistrowsorter = Gtk.TreeListRowSorter.new(columnview_sorter)

        # SortListModel
        sorter_model = Gtk.SortListModel(model=treelistmodel, sorter=treelistrowsorter)
        sorter_model.set_model(self.filterlistmodel)

        # Selection
        self.selection = Gtk.NoSelection.new(model=sorter_model)
        self.columnview.set_model(self.selection)

        # CustomSorter and CustomFilter
        #self.sorter = Gtk.CustomSorter.new(self.sort_func, None)
        self.row_filter = Gtk.CustomFilter.new(self.filter_func, sensors_data_list[0][3][1])
        self.filterlistmodel.set_filter(self.row_filter)

        self.search_text = ""

        self.initial_already_run = 1


    def sensors_loop_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        update_interval = Config.update_interval

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


                    sensor_type_list.append(sensor_type)                                          # Append sensor type. This information will be used for filtering sensors by type when "Show all temperature/fan/voltage and current sensors" radiobuttons are clicked.
                    sensors_data_row = [sensor_type, sensor_group_name, sensor_name, current_value, max_value, critical_value]    # Append sensor visibility data (on treeview) which is used for showing/hiding sensor when sensor data of specific sensor type (temperature or fan sensor) is preferred to be shown or sensor search feature is used from the GUI.

                    # Append sensor data list into main list
                    sensors_data_rows.append(sensors_data_row)

                    sensor_number = sensor_number + 1                                             # Increase sensor number by "1" in order to use this value for getting next file names of the sensor.

        # Add/Remove ColumnView columns
        if sensors_treeview_columns_shown != sensors_treeview_columns_shown_prev:
            # Remove all columns
            for column in self.columnview.get_columns():
                self.columnview.remove_column(column)
            # Add columns
            for i, column_data in enumerate(sensors_treeview_columns_shown):
                if sensors_data_list[column_data][0] in sensors_treeview_columns_shown:
                    factory = sensors_data_list[column_data][2](sensors_data_list[column_data][3])
                    if isinstance(sensors_data_list[column_data][3], list) == True:
                        sorter = Gtk.CustomSorter.new(self.sort_func, sensors_data_list[column_data][3][1])
                    else:
                        sorter = Gtk.CustomSorter.new(self.sort_func, sensors_data_list[column_data][3])
                    column = Gtk.ColumnViewColumn(title=sensors_data_list[column_data][1], factory=factory, sorter=sorter)
                    column.set_resizable(True)
                    #column.set_expand(True)
                    self.columnview.append_column(column)

        # Set column widths
        if sensors_treeview_columns_shown_prev != sensors_treeview_columns_shown or \
            sensors_data_column_widths_prev != sensors_data_column_widths:
            # Get columns and column titles
            sensors_treeview_columns = self.columnview.get_columns()
            treeview_column_titles = []
            for column in sensors_treeview_columns:
                treeview_column_titles.append(column.get_title())
            # Set column width in pixels. Fixed-width is unset if value is "-1".
            for i, sensors_data in enumerate(sensors_data_list):
                for j, column_title in enumerate(treeview_column_titles):
                    if column_title == sensors_data[1]:
                       column_width = sensors_data_column_widths[i]
                       sensors_treeview_columns[j].set_fixed_width(column_width)

        # Set row sorting
        if sensors_treeview_columns_shown_prev != sensors_treeview_columns_shown or \
           sensors_data_row_sorting_column_prev != sensors_data_row_sorting_column or \
           sensors_data_row_sorting_order != sensors_data_row_sorting_order_prev:
            # Get columns and column titles
            sensors_treeview_columns = self.columnview.get_columns()
            treeview_column_titles = []
            for column in sensors_treeview_columns:
                treeview_column_titles.append(column.get_title())
            # Get column title which will be used for sorting rows (if sort column is in the columns shown list)
            if sensors_data_row_sorting_column in sensors_treeview_columns_shown:
                for data in sensors_data_list:
                    if data[0] == sensors_data_row_sorting_column:
                        column_title_for_sorting = data[1]
            # Get column title which will be used for sorting rows (if column is not in the columns shown list)
            if sensors_data_row_sorting_column not in sensors_treeview_columns_shown:
                column_title_for_sorting = sensors_data_list[0][1]
            column_for_sorting = sensors_treeview_columns[treeview_column_titles.index(column_title_for_sorting)]
            # Get row sort order
            if sensors_data_row_sorting_order == 0:
                sort_direction = Gtk.SortType.ASCENDING
            if sensors_data_row_sorting_order == 1:
                sort_direction = Gtk.SortType.DESCENDING
            # Sort rows
            self.columnview.sort_by_column(column_for_sorting, sort_direction)

        # Get new sensors for updating treestore
        new_sensors = sensors_data_rows

        # Clear liststore because sensor data (new/removed) tracking is not performed.
        # Because there may be same named sensors and tracking may not be successful while
        # sensors have no unique identity.
        self.liststore.remove_all()
        # Append sensors
        if len(new_sensors) > 0:
            for sensor in new_sensors:
                row = sensor
                self.liststore.append(Sensor(row[0], row[1], row[2], row[3], row[4], row[5]))
        # Update search results
        self.on_searchentry_changed(self.searchentry)

        sensors_treeview_columns_shown_prev = sensors_treeview_columns_shown
        sensors_data_row_sorting_column_prev = sensors_data_row_sorting_column
        sensors_data_row_sorting_order_prev = sensors_data_row_sorting_order
        sensors_data_column_order_prev = sensors_data_column_order
        sensors_data_column_widths_prev = sensors_data_column_widths

        # Show number of sensors on the searchentry as placeholder text
        self.searchentry.props.placeholder_text = _tr("Search...") + "                    " + "(" + _tr("Sensors") + ": " + str(len(sensor_type_list)) + ")"


class Sensor(GObject.Object):
    __gtype_name__ = "Sensor"

    def __init__(self, sensor_image, device_name, sensor_name, sensor_current_value, sensor_high, sensor_critical):
        super().__init__()

        self._sensor_image = sensor_image
        self._device_name = device_name
        self._sensor_name = sensor_name
        self._sensor_current_value = sensor_current_value
        self._sensor_high = sensor_high
        self._sensor_critical = sensor_critical

    @GObject.Property(type=str)
    def sensor_image(self):
        return self._sensor_image

    @GObject.Property(type=str)
    def device_name(self):
        return self._device_name

    @GObject.Property(type=str)
    def sensor_name(self):
        return self._sensor_name

    @GObject.Property(type=str)
    def sensor_current_value(self):
        return self._sensor_current_value

    @GObject.Property(type=str)
    def sensor_high(self):
        return self._sensor_high

    @GObject.Property(type=str)
    def sensor_critical(self):
        return self._sensor_critical


Sensors = Sensors()


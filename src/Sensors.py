import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import os

from .Config import Config
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class Sensors:

    def __init__(self):

        self.name = "Sensors"

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

        Common.reset_tab_settings(self)

        rows_data_dict = Libsysmon.get_sensors_information()
        self.rows_data_dict_prev = dict(rows_data_dict)
        sensor_unique_id_list = rows_data_dict["sensor_unique_id_list"]

        # Get and append sensor data
        tab_data_rows = []
        for sensor_unique_id in sensor_unique_id_list:
            row_data_dict = rows_data_dict[sensor_unique_id]
            sensor_type = row_data_dict["sensor_type"]
            sensor_group_name = row_data_dict["sensor_group_name"]
            sensor_name = row_data_dict["sensor_name"]
            current_value = row_data_dict["current_value"]
            max_value = row_data_dict["max_value"]
            critical_value = row_data_dict["critical_value"]

            if sensor_type == "temperature":
                sensor_image = "system-monitoring-center-temperature-symbolic"
            elif sensor_type == "fan":
                sensor_image = "system-monitoring-center-fan-symbolic"
            elif sensor_type == "voltage_current_power":
                sensor_image = "system-monitoring-center-voltage-symbolic"

            tab_data_row = [True, sensor_image, sensor_group_name, sensor_name, current_value, max_value, critical_value]

            # Append sensor data list into main list
            tab_data_rows.append(tab_data_row)

        self.tab_data_rows = tab_data_rows

        # Convert set to list (it was set before getting process information)
        treeview_columns_shown = sorted(list(treeview_columns_shown))

        reset_row_unique_data_list_prev = Common.treeview_add_remove_columns(self)
        Common.treeview_reorder_columns_sort_rows_set_column_widths(self)

        # Clear piter_list and treestore because sensor data (new/removed) tracking is not performed.
        # Because there may be same named sensors and tracking may not be successful while sensors have no unique
        # identity (more computer examples are needed for understanding if sensors have unique information).
        # PCI tree path could be get from sensor files but this may not be worth because code will be more complex and
        # it may not be an exact solution for all sensors. Also CPU usage is very low 
        # (about 0.67-0.84%, tested on Core i7-2630QM 4-core notebook) even treestore is cleared and sensor data is appended from zero.
        self.piter_list = []
        self.treestore.clear()

        # Append sensor data into treeview
        for tab_data_row in tab_data_rows:
            self.piter_list.append(self.treestore.append(None, tab_data_row))
        # Update search results.
        self.on_searchentry_changed(self.searchentry)

        Common.searchentry_update_placeholder_text(self, _tr("Sensors"))

        self.treeview_columns_shown_prev = self.treeview_columns_shown
        self.data_row_sorting_column_prev = self.data_row_sorting_column
        self.data_row_sorting_order_prev = self.data_row_sorting_order
        self.data_column_order_prev = self.data_column_order
        self.data_column_widths_prev = self.data_column_widths


Sensors = Sensors()


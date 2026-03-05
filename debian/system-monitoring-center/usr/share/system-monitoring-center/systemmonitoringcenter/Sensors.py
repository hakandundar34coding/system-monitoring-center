import tkinter as tk
from tkinter import ttk

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

        self.tab_frame = ttk.Frame(MainWindow.sensors_tab_main_frame)
        self.tab_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.tab_frame.columnconfigure(0, weight=1)
        self.tab_frame.rowconfigure(1, weight=1)

        self.tab_title_frame()

        self.information_frame()


    def tab_title_frame(self):
        """
        Generate tab name label, refresh button, searchentry.
        """

        # Grid (tab title)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=0, column=0, sticky="new", padx=0, pady=(0, 10))
        frame.columnconfigure(1, weight=1)

        # Label (Sensors)
        label = Common.tab_title_label(frame, _tr("Sensors"))

        # Grid (search widgets)
        search_frame = ttk.Frame(frame)
        search_frame.columnconfigure(0, weight=1)
        search_frame.grid(row=0, column=1, sticky="ew", padx=0, pady=0)

        # SearchEntry
        self.searchentry, self.searchentry_text_var = Common.searchentry(search_frame, self)
        self.searchentry.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)


    def information_frame(self):
        """
        Generate information GUI objects.
        """

        # TreeView
        self.treeview, frame = Common.treeview(self.tab_frame, self)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # SeachEntry focus action and accelerator
        Common.searchentry_focus_action_and_accelerator(MainWindow)


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.column_dict = {"device_name": {"column_title": _tr("Device"), "column_type": str, "converted_data": "no"},
                            "sensor_name": {"column_title": _tr("Sensor Name"), "column_type": str, "converted_data": "no"},
                            "current_value": {"column_title": _tr("Current Value"), "column_type": int, "converted_data": "no"},
                            "max_value": {"column_title": _tr("High"), "column_type": int, "converted_data": "no"},
                            "critical_value": {"column_title": _tr("Critical"), "column_type": int, "converted_data": "no"}
                            }

        self.piter_dict = {}
        self.selected_data_rows_prev = {}
        self.rows_data_dict_prev = {}
        self.row_id_list_prev = []
        self.image_dict = {}
        self.treeview_columns_shown_prev = []

        self.initial_already_run = 1


    def loop_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        # Define global variables and get columnview columns, sort column/order, column widths, etc.
        self.temperature_unit = Config.temperature_unit

        try:
            self.treeview_columns_shown_prev = list(self.treeview_columns_shown)
            self.row_sorting_column_prev = self.row_sorting_column
            self.row_sorting_order_prev = self.row_sorting_order
        except AttributeError:
            self.treeview_columns_shown_prev = []
            self.row_sorting_column_prev = 0
            self.row_sorting_order_prev = 0

        self.treeview_columns_shown = Config.sensors_columns_shown
        self.row_sorting_column = Config.sensors_row_sorting_column
        self.row_sorting_order = Config.sensors_row_sorting_order

        rows_data_dict = Libsysmon.get_sensors_information(self.temperature_unit)
        self.row_id_list = list(rows_data_dict.keys())

        Common.add_columns_and_reset_rows_and_columns(self)

        selected_data_rows_raw = {}
        selected_data_rows = {}
        for sensor_name in self.row_id_list:
            row_data_dict = rows_data_dict[sensor_name]
            if sensor_name not in self.image_dict:
                sensor_type = row_data_dict["sensor_type"]
                if sensor_type == "temperature":
                    icon_name = "smc-temperature"
                elif sensor_type == "fan":
                    icon_name = "smc-fan"
                elif sensor_type == "voltage_current_power":
                    icon_name = "smc-voltage"
                sensor_image = tk.PhotoImage(file=MainWindow.image_path + "" + icon_name + ".png").subsample(3, 3)
                self.image_dict[sensor_name] = sensor_image
            selected_data_row_raw = []
            selected_data_row = []
            for column_shown in self.treeview_columns_shown:
                if column_shown == "device_name":
                    selected_data_row.append(row_data_dict["device_name"])
                    selected_data_row_raw.append(row_data_dict["device_name"])
                if column_shown == "sensor_name":
                    selected_data_row.append(row_data_dict["sensor_name"])
                    selected_data_row_raw.append(row_data_dict["sensor_name"])
                if column_shown == "current_value":
                    selected_data_row.append(row_data_dict["current_value"])
                    selected_data_row_raw.append(row_data_dict["current_value"])
                if column_shown == "max_value":
                    selected_data_row.append(row_data_dict["max_value"])
                    selected_data_row_raw.append(row_data_dict["max_value"])
                if column_shown == "critical_value":
                    selected_data_row.append(row_data_dict["critical_value"])
                    selected_data_row_raw.append(row_data_dict["critical_value"])

            selected_data_rows[sensor_name] = selected_data_row
            selected_data_rows_raw[sensor_name] = selected_data_row_raw

        new_rows, deleted_rows, existing_rows = Common.get_new_removed_updated_rows(self.row_id_list, self.row_id_list_prev)

        self.piter_dict = Common.add_remove_update_treeview_rows(self.treeview, self.piter_dict, self.selected_data_rows_prev, self.image_dict, selected_data_rows, selected_data_rows_raw, new_rows, deleted_rows, existing_rows)

        self.row_count = len(self.row_id_list)
        self.row_information = _tr("Sensors")
        self.selected_data_rows = selected_data_rows
        Common.searchentry_placeholder_text(self)

        self.rows_data_dict_prev = dict(rows_data_dict)
        self.row_id_list_prev = self.row_id_list
        self.selected_data_rows_prev = self.selected_data_rows

        Common.sort_columns_on_every_loop(self)


Sensors = Sensors()


import tkinter as tk
from tkinter import ttk

import os
import subprocess

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class Services:

    def __init__(self):

        self.name = "Services"

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_frame = ttk.Frame(MainWindow.services_tab_main_frame)
        self.tab_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.tab_frame.columnconfigure(0, weight=1)
        self.tab_frame.rowconfigure(1, weight=1)

        self.tab_title_frame()

        self.information_frame()

        self.gui_signals()

        self.right_click_menu_gui()

        # Label (Note: This tab is not reloaded automatically. Manually reload for changes.)
        label = Common.static_information_label(self.tab_frame, _tr("Note: This tab is not reloaded automatically. Manually reload for changes."))
        label.grid(row=2, column=0, sticky="w", padx=0, pady=1)


    def tab_title_frame(self):
        """
        Generate tab name label, refresh button, searchentry.
        """

        # Grid (tab title)
        frame = ttk.Frame(self.tab_frame)
        frame.grid(row=0, column=0, sticky="new", padx=0, pady=(0, 10))
        frame.columnconfigure(1, weight=1)

        # Label (Services)
        label = Common.tab_title_label(frame, _tr("Services"))

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
        return


    def right_click_menu_gui(self):
        """
        Generate right click menu GUI.
        """

        self.right_click_menu = tk.Menu(self.treeview, tearoff=False, bd=3, activebackground="gray")
        self.right_click_menu.add_command(label=_tr("Start"), command=lambda: self.on_service_manage_items_activate("start"))
        self.right_click_menu.add_command(label=_tr("Stop"), command=lambda: self.on_service_manage_items_activate("stop"))
        self.right_click_menu.add_command(label=_tr("Restart"), command=lambda: self.on_service_manage_items_activate("restart"))
        self.right_click_menu.add_command(label=_tr("Reload"), command=lambda: self.on_service_manage_items_activate("reload"))
        self.right_click_menu.add_command(label=_tr("Enable"), command=lambda: self.on_service_manage_items_activate("enable"))
        self.right_click_menu.add_command(label=_tr("Disable"), command=lambda: self.on_service_manage_items_activate("disable"))
        self.right_click_menu.add_command(label=_tr("Mask"), command=lambda: self.on_service_manage_items_activate("mask"))
        self.right_click_menu.add_command(label=_tr("Unmask"), command=lambda: self.on_service_manage_items_activate("unmask"))
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label=_tr("Help"), command=self.on_service_help_item_activate)
        self.right_click_menu.add_separator()
        self.right_click_menu.add_command(label=_tr("Details"), accelerator="(Enter)", command=self.on_details_item_activate)

        self.right_click_menu.bind("<FocusOut>", self.right_click_menu_close)

        self.treeview.bind("<Button-3>", self.on_right_click)
        self.treeview.bind("<Double-1>", self.treeview_double_click_event)
        # Treeview "FocusOut" signal may not close right click menu if certain areas of the GUI is clicked. The following signal is used for fixing this issue.
        self.treeview.winfo_toplevel().bind("<Button-1>", self.right_click_menu_close)

        return self.right_click_menu


    def get_selection(self, event):

        self.selected_row_id = self.treeview.identify_row(event.y)
        # Get right clicked row id.
        if self.selected_row_id:
            # Select the row visually if right clicked on a row.
            self.treeview.selection_set(self.selected_row_id)
            # Get data of the selected row.
            self.selected_row_name = self.treeview.item(self.selected_row_id, "text")

        return self.selected_row_name


    def on_right_click(self, event):

        self.get_selection(event)
        # Show menu on mouse coordinates
        self.right_click_menu.post(event.x_root, event.y_root)
        self.right_click_menu.focus_set()


    def right_click_menu_close(self, event):
        """
        Close right click menu if clicked another part of the GUI.
        """

        self.right_click_menu.unpost()


    def on_service_manage_items_activate(self, action_name):
        """
        Start, stop, restart, enable, disable, mask (hide), unmask services.
        """
        
        self.selected_row_name = self.get_selection(event)
        # Manage the selected service and get errors.
        systemctl_error = Libsysmon.manage_service(self.selected_row_name, action_name)

        # Show information dialog if there are errors in the command output.
        if systemctl_error != "-":
            message_text = systemctl_error
            if message_text != "":
                self.service_dialog_label.config(text=message_text)


    def service_information_gui(self):
        """
        Generate information window for service action outputs.
        """

        # Window (Information)
        self.service_dialog, frame = Common.window(MainWindow.main_window, _tr("Information"))
        self.service_dialog.minsize(750, 100)
        self.service_dialog.maxsize(1100, 150)

        # Label ()
        self.service_dialog_label = Common.bold_label(frame, text="")
        self.service_dialog_label.grid(row=0, column=0, sticky="ns", padx=20, pady=20)


    def on_service_help_item_activate(self):
        """
        Show services help window.
        """

        self.services_help_window_gui()


    def services_help_window_gui(self):
        """
        Services tab help window GUI.
        """

        # Window (Service Help)
        self.services_help_window, frame = Common.window(MainWindow.main_window, _tr("Help"))
        self.services_help_window.minsize(1000, 300)
        self.services_help_window.maxsize(1300, 1000)

        # Frame (main)
        main_frame = ttk.Frame(self.services_help_window, style="Card.TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Label (Start)
        start_label = Common.bold_label(main_frame, text=_tr("Start") + ":")
        start_label.grid(row=0, column=0, sticky="nsew", padx=0, pady=4)

        # Label (Start - Help)
        start_help_label = Common.static_information_label(main_frame, text=_tr("Starts a service.") + " " + _tr("This action does not affect a service after system reboot."))
        start_help_label.grid(row=1, column=0, sticky="nsew", padx=0, pady=4)

        # Separator
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.grid(row=2, column=0, sticky="nsew", padx=0, pady=5)

        # Label (Stop)
        stop_label = Common.bold_label(main_frame, text=_tr("Stop") + ":")
        stop_label.grid(row=3, column=0, sticky="nsew", padx=0, pady=4)

        # Label (Stop - Help)
        stop_help_label = Common.static_information_label(main_frame, text=_tr("Stops a service.") + " " + _tr("This action does not affect a service after system reboot."))
        stop_help_label.grid(row=4, column=0, sticky="nsew", padx=0, pady=4)

        # Separator
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.grid(row=5, column=0, sticky="nsew", padx=0, pady=5)

        # Label (Restart)
        restart_label = Common.bold_label(main_frame, text=_tr("Restart") + ":")
        restart_label.grid(row=6, column=0, sticky="nsew", padx=0, pady=4)

        # Label (Restart - Help)
        restart_help_label = Common.static_information_label(main_frame, text=_tr("Restarts a service."))
        restart_help_label.grid(row=7, column=0, sticky="nsew", padx=0, pady=4)

        # Separator
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.grid(row=8, column=0, sticky="nsew", padx=0, pady=5)

        # Label (Reload)
        reload_label = Common.bold_label(main_frame, text=_tr("Reload") + ":")
        reload_label.grid(row=9, column=0, sticky="nsew", padx=0, pady=4)

        # Label (Reload - Help)
        reload_help_label = Common.static_information_label(main_frame, text=_tr("Reloads a service.") + " " + _tr("This action is not available for all services.") + " " + _tr("This action does not affect running process of a service."))
        reload_help_label.grid(row=10, column=0, sticky="nsew", padx=0, pady=4)

        # Separator
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.grid(row=11, column=0, sticky="nsew", padx=0, pady=5)

        # Label (Enable)
        enable_label = Common.bold_label(main_frame, text=_tr("Enable") + ":")
        enable_label.grid(row=12, column=0, sticky="nsew", padx=0, pady=4)

        # Label (Enable - Help)
        enable_help_label = Common.static_information_label(main_frame, text=_tr("Enables a service.") + " " + _tr("This action affects a service after system reboot."))
        enable_help_label.grid(row=13, column=0, sticky="nsew", padx=0, pady=4)

        # Separator
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.grid(row=14, column=0, sticky="nsew", padx=0, pady=5)

        # Label (Disable)
        disable_label = Common.bold_label(main_frame, text=_tr("Disable") + ":")
        disable_label.grid(row=15, column=0, sticky="nsew", padx=0, pady=4)

        # Label (Disable - Help)
        disable_help_label = Common.static_information_label(main_frame, text=_tr("Disables a service.") + " " + _tr("This action affects a service after system reboot.") + " " + _tr("This action does not affect running process of a service."))
        disable_help_label.grid(row=16, column=0, sticky="nsew", padx=0, pady=4)

        # Separator
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.grid(row=17, column=0, sticky="nsew", padx=0, pady=5)

        # Label (Mask)
        mask_label = Common.bold_label(main_frame, text=_tr("Mask") + ":")
        mask_label.grid(row=18, column=0, sticky="nsew", padx=0, pady=4)

        # Label (Mask - Help)
        mask_help_label = Common.static_information_label(main_frame, text=_tr("Disables a service completely.") + " " + _tr("A masked service can not be started, restarted, reloaded or enabled."))
        mask_help_label.grid(row=19, column=0, sticky="nsew", padx=0, pady=4)

        # Separator
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.grid(row=20, column=0, sticky="nsew", padx=0, pady=5)

        # Label (Unmask)
        unmask_label = Common.bold_label(main_frame, text=_tr("Unmask") + ":")
        unmask_label.grid(row=21, column=0, sticky="nsew", padx=0, pady=4)

        # Label (Unmask - Help)
        unmask_help_label = Common.static_information_label(main_frame, text=_tr("Unmasks a service.") + " " + _tr("A service can be started, restarted, reloaded (if it is available) or enabled after unmasking."))
        unmask_help_label.grid(row=22, column=0, sticky="nsew", padx=0, pady=4)


    def on_details_item_activate(self):
        """
        Show service details window.
        """

        from .ServicesDetails import ServicesDetails
        ServicesDetails.window_gui()


    def treeview_double_click_event(self, event):

        region = self.treeview.identify_region(event.x, event.y)
        # Prevent running code if rows are not clicked.
        if region in ["cell", "tree"]:
            self.selected_row_name = self.get_selection(event)
            from .ServicesDetails import ServicesDetails
            ServicesDetails.window_gui()


    def initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.column_dict = {"service_name": {"column_title": _tr("Name"), "column_type": str, "converted_data": "no"},
                            "unit_file_state": {"column_title": _tr("State"), "column_type": str, "converted_data": "no"},
                            "main_pid": {"column_title": _tr("Main PID"), "column_type": int, "converted_data": "no"},
                            "active_state": {"column_title": _tr("Active State"), "column_type": str, "converted_data": "no"},
                            "load_state": {"column_title": _tr("Load State"), "column_type": str, "converted_data": "no"},
                            "sub_state": {"column_title": _tr("Sub-State"), "column_type": str, "converted_data": "no"},
                            "memory_current": {"column_title": _tr("Memory (RSS)"), "column_type": int, "converted_data": "yes"},
                            "description": {"column_title": _tr("Description"), "column_type": str, "converted_data": "no"}
                            }

        # Define data unit conversion function objects in for lower CPU usage.
        global data_unit_converter
        data_unit_converter = Libsysmon.data_unit_converter

        self.piter_dict = {}
        self.selected_data_rows_prev = {}
        self.rows_data_dict_prev = {}
        self.row_id_list_prev = []
        self.image_dict = {}
        self.treeview_columns_shown_prev = []

        service_state_translation_list = [_tr("Enabled"), _tr("Disabled"), _tr("Masked"), _tr("Unmasked"), _tr("Static"), _tr("Generated"), _tr("Enabled-runtime"), _tr("Indirect"), _tr("Active"), _tr("Inactive"), _tr("Loaded"), _tr("Dead"), _tr("Exited"), _tr("Running")]
        services_other_text_translation_list = [_tr("Yes"), _tr("No")]

        self.initial_already_run = 1


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        if self.initial_already_run == 0:
            self.initial_func()

        # Switch to System tab and prevent errors if systemd is not used on the system.
        if Config.init_system != "systemd":
            MainWindow.performance_tab_main_frame.tkraise()
            return

        # Prevent running rest of the code if Services tab is opened again.
        # Because running this function requires more than a few seconds on some systems.
        try:
            if self.loop_already_run == 1:
                return
        except AttributeError:
            pass
        self.loop_already_run = 1

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        global services_memory_data_precision, services_memory_data_unit
        services_memory_data_precision = Config.services_memory_data_precision
        services_memory_data_unit = Config.services_memory_data_unit

        try:
            self.treeview_columns_shown_prev = list(self.treeview_columns_shown)
            self.row_sorting_column_prev = self.row_sorting_column
            self.row_sorting_order_prev = self.row_sorting_order
        except AttributeError:
            self.treeview_columns_shown_prev = []
            self.row_sorting_column_prev = 0
            self.row_sorting_order_prev = 0

        # Define global variables and get treeview columns, sort column/order, column widths, etc.
        self.treeview_columns_shown = Config.services_columns_shown
        self.row_sorting_column = Config.services_row_sorting_column
        self.row_sorting_order = Config.services_row_sorting_order

        rows_data_dict = Libsysmon.get_services_information()
        self.row_id_list = list(rows_data_dict.keys())

        Common.add_columns_and_reset_rows_and_columns(self)

        service_image = tk.PhotoImage(file=MainWindow.image_path + "smc-service-row.png").subsample(3, 3)

        selected_data_rows_raw = {}
        selected_data_rows = {}
        for service_name in self.row_id_list:
            row_data_dict = rows_data_dict[service_name]
            if service_name not in self.image_dict:
                self.image_dict[service_name] = service_image
            selected_data_row_raw = []
            selected_data_row = []
            for column_shown in self.treeview_columns_shown:
                if column_shown == "service_name":
                    selected_data_row.append(row_data_dict["service_name"])
                    selected_data_row_raw.append(row_data_dict["service_name"])
                if column_shown == "unit_file_state":
                    selected_data_row.append(row_data_dict["unit_file_state"])
                    selected_data_row_raw.append(row_data_dict["unit_file_state"])
                if column_shown == "main_pid":
                    selected_data_row.append(row_data_dict["main_pid"])
                    selected_data_row_raw.append(row_data_dict["main_pid"])
                if column_shown == "active_state":
                    selected_data_row.append(row_data_dict["active_state"])
                    selected_data_row_raw.append(row_data_dict["active_state"])
                if column_shown == "load_state":
                    selected_data_row.append(row_data_dict["load_state"])
                    selected_data_row_raw.append(row_data_dict["load_state"])
                if column_shown == "sub_state":
                    selected_data_row.append(row_data_dict["sub_state"])
                    selected_data_row_raw.append(row_data_dict["sub_state"])
                if column_shown == "memory_current":
                    if row_data_dict["memory_current"] == -1:
                        converted_data = "-"
                    else:
                        converted_data = f'{data_unit_converter("data", "none", row_data_dict["memory_current"], services_memory_data_unit, services_memory_data_precision)}'
                    selected_data_row.append(converted_data)
                    selected_data_row_raw.append(row_data_dict["memory_current"])
                if column_shown == "description":
                    selected_data_row.append(row_data_dict["description"])
                    selected_data_row_raw.append(row_data_dict["description"])

            selected_data_rows[service_name] = selected_data_row
            selected_data_rows_raw[service_name] = selected_data_row_raw

        new_rows, deleted_rows, existing_rows = Common.get_new_removed_updated_rows(self.row_id_list, self.row_id_list_prev)

        self.piter_dict = Common.add_remove_update_treeview_rows(self.treeview, self.piter_dict, self.selected_data_rows_prev, self.image_dict, selected_data_rows, selected_data_rows_raw, new_rows, deleted_rows, existing_rows)

        self.row_count = len(self.row_id_list)
        self.row_information = _tr("Services")
        self.selected_data_rows = selected_data_rows
        Common.searchentry_placeholder_text(self)

        self.rows_data_dict_prev = dict(rows_data_dict)
        self.row_id_list_prev = self.row_id_list
        self.selected_data_rows_prev = self.selected_data_rows

        Common.sort_columns_on_every_loop(self)


Services = Services()


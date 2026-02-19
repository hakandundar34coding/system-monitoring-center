import tkinter as tk
from tkinter import ttk, messagebox

import os

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


class SettingsWindow:

    def __init__(self):

        # Define data lists in order to add them into comboboxes.
        self.language_dict = {"system":_tr("System"), "cs.UTF-8":"Čeština", "de.UTF-8":"Deutsch",
                              "en_US.UTF-8":"English (US)", "es":"Español", "fa.UTF-8":"فارسی",
                              "fr.UTF-8":"Français", "hu.UTF-8":"Magyar", "pl.UTF-8":"Polski",
                              "pt_BR.UTF-8":"Português do Brasil", "pt_PT.UTF-8":"Português europeu",
                              "ru_RU.UTF-8":"Русский", "tr.UTF-8":"Türkçe", "zh_CN":"简体中文",
                              "zh_TW":"繁體中文"}

        self.gui_theme_dict = {_tr("System"):"system", _tr("Light"):"light", _tr("Dark"):"dark"}
        self.update_interval_list = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 5.0]
        self.chart_data_history_list = [30, 60, 90, 120, 150, 180, 300, 600, 1200]

        # For translating the text that is used in ".desktop" file.
        _text = [_tr("System Monitor"), _tr("Task Manager")]


    def window_gui(self):
        """
        Generate window GUI.
        """

        # Window (Settings)
        self.settings_window, frame = Common.window(MainWindow.main_window, _tr("Settings"))
        self.settings_window.resizable(False, False)

        # Notebook
        style = ttk.Style()
        style.configure("TNotebook", tabposition="wn")

        notebook = ttk.Notebook(frame)
        notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        notebook.bind("<<NotebookTabChanged>>", self.on_notebook_tab_change)

        # General Settings Tab
        self.frame_general_settings_tab = tk.Frame(notebook)
        notebook.add(self.frame_general_settings_tab, text=_tr("General Settings"))

        # Summary Tab
        self.frame_summary_tab = tk.Frame(notebook)
        notebook.add(self.frame_summary_tab, text=_tr("Summary"))

        # CPU Tab
        self.frame_cpu_tab = tk.Frame(notebook)
        notebook.add(self.frame_cpu_tab, text=_tr("CPU"))

        # Memory Tab
        self.frame_memory_tab = tk.Frame(notebook)
        notebook.add(self.frame_memory_tab, text=_tr("Memory"))

        # Disk Tab
        self.frame_disk_tab = tk.Frame(notebook)
        notebook.add(self.frame_disk_tab, text=_tr("Disk"))

        # Network Tab
        self.frame_network_tab = tk.Frame(notebook)
        notebook.add(self.frame_network_tab, text=_tr("Network"))

        # Sensors Tab
        self.frame_sensors_tab = tk.Frame(notebook)
        notebook.add(self.frame_sensors_tab, text=_tr("Sensors"))

        # Processes Tab
        self.frame_processes_tab = tk.Frame(notebook)
        notebook.add(self.frame_processes_tab, text=_tr("Processes"))

        # Users Tab
        self.frame_users_tab = tk.Frame(notebook)
        notebook.add(self.frame_users_tab, text=_tr("Users"))

        # Services Tab
        self.frame_services_tab = tk.Frame(notebook)
        notebook.add(self.frame_services_tab, text=_tr("Services"))


    def on_notebook_tab_change(self, event):
        """
        Switch to selected Notebook tab if it is not opened before.
        """

        tab_id = event.widget.index("current")
        if tab_id == 0:
            if self.frame_general_settings_tab.winfo_children() == []:
                self.general_settings_tab_gui()
        if tab_id == 1:
            if self.frame_summary_tab.winfo_children() == []:
                self.summary_settings_tab_gui()
        if tab_id == 2:
            if self.frame_cpu_tab.winfo_children() == []:
                self.cpu_settings_tab_gui()
        if tab_id == 3:
            if self.frame_memory_tab.winfo_children() == []:
                self.memory_settings_tab_gui()
        if tab_id == 4:
            if self.frame_disk_tab.winfo_children() == []:
                self.disk_settings_tab_gui()
        if tab_id == 5:
            if self.frame_network_tab.winfo_children() == []:
                self.network_settings_tab_gui()
        if tab_id == 6:
            if self.frame_sensors_tab.winfo_children() == []:
                self.sensors_settings_tab_gui()
        if tab_id == 7:
            if self.frame_processes_tab.winfo_children() == []:
                self.processes_settings_tab_gui()
        if tab_id == 8: 
            if self.frame_users_tab.winfo_children() == []:
                self.users_settings_tab_gui()
        if tab_id == 9:
            if self.frame_services_tab.winfo_children() == []:
                self.services_settings_tab_gui()


    # ***********************************************************************************************
    #                                           General Settings
    # ***********************************************************************************************

    def general_settings_tab_gui(self):

        # Frame
        frame = ttk.Frame(self.frame_general_settings_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        # Label (Language)
        label = ttk.Label(frame, text=_tr("Language (Requires restart)") + ":")
        label.grid(row=0, column=0, sticky="w", padx=0, pady=5)
        # ComboBox (Language)
        self.language_cb = ttk.Combobox(frame, stat="readonly")
        self.language_cb.grid(row=0, column=1, sticky="ew", padx=0, pady=5)
        self.language_cb['values'] = list(self.language_dict.values())
        self.language_cb.bind("<<ComboboxSelected>>", self.on_language_cb_selected)

        # Label (Light/Dark theme)
        label = ttk.Label(frame, text=_tr("Light/Dark theme") + ":")
        label.grid(row=1, column=0, sticky="w", padx=0, pady=5)
        # ComboBox (Light/Dark theme)
        self.dark_light_theme_cb = ttk.Combobox(frame, stat="readonly")
        self.dark_light_theme_cb.grid(row=1, column=1, sticky="ew", padx=0, pady=5)
        self.dark_light_theme_cb['values'] = list(self.gui_theme_dict.keys())
        self.dark_light_theme_cb.bind("<<ComboboxSelected>>", self.on_dark_light_theme_cb_selected)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=2, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Label (Update interval (seconds))
        label = ttk.Label(frame, text=_tr("Update interval (seconds)") + ":")
        label.grid(row=3, column=0, sticky="w", padx=0, pady=5)
        # ComboBox (Update interval (seconds))
        self.update_interval_cb = ttk.Combobox(frame, stat="readonly")
        self.update_interval_cb.grid(row=3, column=1, sticky="ew", padx=0, pady=5)
        self.update_interval_cb['values'] = self.update_interval_list
        self.update_interval_cb.bind("<<ComboboxSelected>>", self.on_update_interval_cb_selected)

        # Label (Graph data history)
        label = ttk.Label(frame, text=_tr("Graph data history") + ":")
        label.grid(row=4, column=0, sticky="w", padx=0, pady=5)
        # ComboBox (Graph data history)
        self.chart_data_history_cb = ttk.Combobox(frame, stat="readonly")
        self.chart_data_history_cb.grid(row=4, column=1, sticky="ew", padx=0, pady=5)
        self.chart_data_history_cb['values'] = self.chart_data_history_list
        self.chart_data_history_cb.bind("<<ComboboxSelected>>", self.on_chart_data_history_cb_selected)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=5, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # CheckButton (Remember last opened tabs)
        self.remember_last_opened_tabs_var = tk.IntVar()
        self.remember_last_opened_tabs_cb = Common.checkbutton(frame, _tr("Remember last opened tabs"), self.remember_last_opened_tabs_var, self.on_remember_last_opened_tabs_cb_toggled)
        self.remember_last_opened_tabs_cb.grid(row=6, column=0, columnspan=2, sticky="w", padx=0, pady=5)

        # CheckButton (Remember last selected devices)
        self.remember_last_selected_devices_var = tk.IntVar()
        self.remember_last_selected_devices_cb = Common.checkbutton(frame, _tr("Remember last selected devices"), self.remember_last_selected_devices_var, self.on_remember_last_selected_devices_cb_toggled)
        self.remember_last_selected_devices_cb.grid(row=7, column=0, columnspan=2, sticky="w", padx=0, pady=5)

        # CheckButton (Remember window size)
        self.remember_window_size_var = tk.IntVar()
        self.remember_window_size_cb = Common.checkbutton(frame, _tr("Remember window size"), self.remember_window_size_var, self.on_remember_window_size_cb_toggled)
        self.remember_window_size_cb.grid(row=8, column=0, columnspan=2, sticky="w", padx=0, pady=5)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=9, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Button (Reset)
        self.reset_general_settings_button = Common.reset_button(frame)
        self.reset_general_settings_button.grid(row=10, column=0, columnspan=2, padx=0, pady=5)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=11, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Button (Reset all settings of the application)
        self.reset_all_settings_button = tk.Button(frame, text=_tr("Reset all settings of the application"), bg="darkred", activebackground="#C20000")
        self.reset_all_settings_button.grid(row=12, column=0, columnspan=2, sticky="ew", padx=0, pady=5)

        # Connect signals
        self.settings_window.after(1, self.general_settings_set_gui)
        self.reset_general_settings_button.config(command=self.on_reset_general_settings_button_clicked)
        self.reset_all_settings_button.config(command=self.on_reset_all_settings_button_clicked)


    def on_language_cb_selected(self, event):
        for i in self.language_dict:
            if self.language_dict[i] == self.language_cb.get():
                Config.language = i
        Config.config_save_func()

    def on_dark_light_theme_cb_selected(self, event):
        Config.light_dark_theme = self.gui_theme_dict[self.dark_light_theme_cb.get()]
        Config.config_save_func()

    def on_update_interval_cb_selected(self, event):
        Config.update_interval = float(self.update_interval_cb.get())
        Config.config_save_func()
        self.settings_gui_apply_settings_immediately_func()

    def on_chart_data_history_cb_selected(self, event):
        Config.chart_data_history = int(self.chart_data_history_cb.get())
        Config.config_save_func()
        self.settings_gui_set_chart_data_history_func()
        self.settings_gui_apply_settings_immediately_func()

    def on_remember_last_opened_tabs_cb_toggled(self):
        Config.remember_last_opened_tabs = self.remember_last_opened_tabs_var.get()

        if self.remember_last_opened_tabs_var.get() == 1:
            Config.default_main_tab = MainWindow.main_tab_var.get()
            Config.performance_tab_default_sub_tab = MainWindow.sub_tab_var.get()
        if self.remember_last_opened_tabs_var.get() == 0:
            Config.default_main_tab = 0
            Config.performance_tab_default_sub_tab = 0

        Config.config_save_func()

    def on_remember_last_selected_devices_cb_toggled(self):
        Config.remember_last_selected_hardware = self.remember_last_selected_devices_var.get()
        Config.config_save_func()
        
    def on_remember_window_size_cb_toggled(self):
        if self.remember_window_size_var.get() == 1:
            main_window_width = MainWindow.main_window.winfo_width()
            main_window_height = MainWindow.main_window.winfo_height()
            Config.remember_window_size = str(main_window_width) + "x" + str(main_window_height)
        if self.remember_window_size_var.get() == 0:
            Config.remember_window_size = "0x0"

        Config.config_save_func()


    def on_reset_general_settings_button_clicked(self):
        """
        Reset settings on the "Settings" window.
        """

        Config.config_default_general_func()
        Config.config_save_func()
        # Set GUI objects of the Settings window without disconnecting signals
        # of the widgets in order to use these signals to reset the settings.
        self.general_settings_set_gui()

        # Length of performance data lists (cpu_usage_percent_ave, ram_usage_percent_ave, ...)
        # have to be set after "chart_data_history" setting is reset in order to avoid errors.
        self.settings_gui_set_chart_data_history_func()

        # Apply selected CPU core, disk, network card changes
        Performance.performance_set_selected_cpu_core_func()
        Performance.performance_set_selected_disk_func()
        Performance.performance_set_selected_network_card_func()
        # Apply selected GPU changes
        try:
            from .MainWindow import Gpu
            Libsysmon.gpu_set_selected_gpu(Gpu.selected_gpu, Gpu.default_gpu, Gpu.gpu_list)
        # Prevent errors because "gpu_get_gpu_list_and_set_selected_gpu_func" module requires
        # some modules in the Gpu module. They are imported if Gpu tab is switched on.
        except ImportError:
            pass

        # Apply changes immediately (without waiting update interval).
        self.settings_gui_apply_settings_immediately_func()


    def general_settings_set_gui(self):
        self.language_cb.current(list(self.language_dict.keys()).index(Config.language))
        self.dark_light_theme_cb.current(list(self.gui_theme_dict.values()).index(Config.light_dark_theme))
        self.update_interval_cb.current(self.update_interval_list.index(Config.update_interval))
        self.chart_data_history_cb.current(self.chart_data_history_list.index(Config.chart_data_history))
        self.remember_last_opened_tabs_var.set(Config.remember_last_opened_tabs)
        self.remember_last_selected_devices_var.set(Config.remember_last_selected_hardware)
        if Config.remember_window_size == "0x0":
            self.remember_window_size_var.set(0)
        else:
            self.remember_window_size_var.set(1)


    def settings_gui_set_chart_data_history_func(self):
        """
        Trim/Add performance data lists (cpu_usage_percent_ave, ram_usage_percent, ...)
        when "chart_data_history" preference is changed.
        """

        # Get current chart_data_history length which is same for all performance data lists (cpu_usage_percent_ave, ram_usage_percent, ...).
        chart_data_history_current = len(Performance.cpu_usage_percent_ave)
        chart_data_history_new = Config.chart_data_history

        # Trim beginning part of the lists if new "chart_data_history" value is smaller than the old value.
        if chart_data_history_current > chart_data_history_new:

            length_difference = chart_data_history_current - chart_data_history_new

            # "max_cpu_usage_list", "max_cpu_usage_process_name_list", "max_cpu_usage_process_pid_list" lists
            Performance.max_cpu_usage_list = Performance.max_cpu_usage_list[length_difference:]
            Performance.max_cpu_usage_process_name_list = Performance.max_cpu_usage_process_name_list[length_difference:]
            Performance.max_cpu_usage_process_pid_list = Performance.max_cpu_usage_process_pid_list[length_difference:]

            Performance.system_performance_data_dict_prev["cpu_usage_percent_ave"] = Performance.system_performance_data_dict_prev["cpu_usage_percent_ave"][length_difference:]

            # "cpu_usage_percent_per_core" list
            for device in Performance.logical_core_list:
                Performance.system_performance_data_dict_prev["cpu_usage_percent_per_core"][device] = Performance.system_performance_data_dict_prev["cpu_usage_percent_per_core"][device][length_difference:]

            # "ram_usage_percent" and "swap_usage_percent" lists
            Performance.system_performance_data_dict_prev["ram_usage_percent"] = Performance.system_performance_data_dict_prev["ram_usage_percent"][length_difference:]
            Performance.system_performance_data_dict_prev["swap_usage_percent"] = Performance.system_performance_data_dict_prev["swap_usage_percent"][length_difference:]

            # "disk_read_speed" and "disk_write_speed" lists
            for device in Performance.disk_list:
                Performance.system_performance_data_dict_prev["disk_read_speed"][device] = Performance.system_performance_data_dict_prev["disk_read_speed"][device][length_difference:]
                Performance.system_performance_data_dict_prev["disk_write_speed"][device] = Performance.system_performance_data_dict_prev["disk_write_speed"][device][length_difference:]

            # "network_receive_speed" and "network_send_speed" lists
            for device in Performance.network_card_list:
                Performance.system_performance_data_dict_prev["network_receive_speed"][device] = Performance.system_performance_data_dict_prev["network_receive_speed"][device][length_difference:]
                Performance.system_performance_data_dict_prev["network_send_speed"][device] = Performance.system_performance_data_dict_prev["network_send_speed"][device][length_difference:]

            # "gpu_load_list", "gpu_memory_list", "gpu_encoder_load_list", "gpu_decoder_load_list" lists
            if "selected" in MainWindow.gpu_tb.state():
                from .Gpu import Gpu
                Gpu.gpu_load_list = Gpu.gpu_load_list[length_difference:]
                Gpu.gpu_memory_list = Gpu.gpu_memory_list[length_difference:]
                Gpu.gpu_encoder_load_list = Gpu.gpu_encoder_load_list[length_difference:]
                Gpu.gpu_decoder_load_list = Gpu.gpu_decoder_load_list[length_difference:]

            # Process Details window CPU, memory (RSS), disk read speed and disk write speed lists
            if MainWindow.processes_tab_main_frame.winfo_children() != []:
                from .ProcessesDetails import ProcessesDetails
                for process_details_object in ProcessesDetails.processes_details_object_list:
                    process_details_object.process_cpu_usage_list = process_details_object.process_cpu_usage_list[length_difference:]
                    process_details_object.process_ram_usage_list = process_details_object.process_ram_usage_list[length_difference:]
                    process_details_object.process_disk_read_speed_list = process_details_object.process_disk_read_speed_list[length_difference:]
                    process_details_object.process_disk_write_speed_list = process_details_object.process_disk_write_speed_list[length_difference:]

        # Add list of zeroes to the beginning part of the lists if new "chart_data_history" value is bigger than the old value.
        if chart_data_history_current < chart_data_history_new:

            # Generate list of zeroes for adding to the beginning of the lists.
            list_to_add = [0] * (chart_data_history_new - chart_data_history_current)

            # "cpu_usage_percent_ave" list
            Performance.system_performance_data_dict_prev["cpu_usage_percent_ave"] = list_to_add + Performance.system_performance_data_dict_prev["cpu_usage_percent_ave"]

            # Generate list of dashes for adding to the beginning of some of the lists.
            list_to_add_dashes = ["-"] * (chart_data_history_new - chart_data_history_current)
            # "max_cpu_usage_list", "max_cpu_usage_process_name_list", "max_cpu_usage_process_pid_list" lists
            Performance.max_cpu_usage_list = list_to_add + Performance.max_cpu_usage_list
            Performance.max_cpu_usage_process_name_list = list_to_add_dashes + Performance.max_cpu_usage_process_name_list
            Performance.max_cpu_usage_process_pid_list = list_to_add_dashes + Performance.max_cpu_usage_process_pid_list

            # "cpu_usage_percent_per_core" list
            for device in Performance.logical_core_list:
                Performance.system_performance_data_dict_prev["cpu_usage_percent_per_core"][device] = list_to_add + Performance.system_performance_data_dict_prev["cpu_usage_percent_per_core"][device]

            # "ram_usage_percent" and "swap_usage_percent" lists
            Performance.system_performance_data_dict_prev["ram_usage_percent"] = list_to_add + Performance.system_performance_data_dict_prev["ram_usage_percent"]
            Performance.system_performance_data_dict_prev["swap_usage_percent"] = list_to_add + Performance.system_performance_data_dict_prev["swap_usage_percent"]

            # "disk_read_speed" and "disk_write_speed" lists
            for device in Performance.disk_list:
                Performance.system_performance_data_dict_prev["disk_read_speed"][device] = list_to_add + Performance.system_performance_data_dict_prev["disk_read_speed"][device]
                Performance.system_performance_data_dict_prev["disk_write_speed"][device] = list_to_add + Performance.system_performance_data_dict_prev["disk_write_speed"][device]

            # "network_receive_speed" and "network_send_speed" lists
            for device in Performance.network_card_list:
                Performance.system_performance_data_dict_prev["network_receive_speed"][device] = list_to_add + Performance.system_performance_data_dict_prev["network_receive_speed"][device]
                Performance.system_performance_data_dict_prev["network_send_speed"][device] = list_to_add + Performance.system_performance_data_dict_prev["network_send_speed"][device]

            # "gpu_load_list", "gpu_memory_list", "gpu_encoder_load_list", "gpu_decoder_load_list" lists
            if "selected" in MainWindow.gpu_tb.state():
                from .Gpu import Gpu
                Gpu.gpu_load_list = list_to_add + Gpu.gpu_load_list
                Gpu.gpu_memory_list = list_to_add + Gpu.gpu_memory_list
                Gpu.gpu_encoder_load_list = list_to_add + Gpu.gpu_encoder_load_list
                Gpu.gpu_decoder_load_list = list_to_add + Gpu.gpu_decoder_load_list

            # Process Details window CPU, memory (RSS), disk read speed and disk write speed lists
            if MainWindow.processes_tab_main_frame.winfo_children() != []:
                from .ProcessesDetails import ProcessesDetails
                for process_details_object in ProcessesDetails.processes_details_object_list:
                    process_details_object.process_cpu_usage_list = list_to_add + process_details_object.process_cpu_usage_list
                    process_details_object.process_ram_usage_list = list_to_add + process_details_object.process_ram_usage_list
                    process_details_object.process_disk_read_speed_list = list_to_add + process_details_object.process_disk_read_speed_list
                    process_details_object.process_disk_write_speed_list = list_to_add + process_details_object.process_disk_write_speed_list


    def settings_gui_apply_settings_immediately_func(self):
        """
        Apply settings for all opened tabs (since application start) without waiting update interval.
        If "initial_already_run" variable is set as "0", initial and loop functions of the relevant
        tab will be run in the next main loop if the tab is already opened or these functions will be run
        immediately when the relevant tab is switched on even if it is opened before the reset.
        """

        try:
            from .MainWindow import Summary
            Summary.initial_already_run = 0
        except ImportError:
            pass

        try:
            from .MainWindow import Cpu
            Cpu.initial_already_run = 0
        except ImportError:
            pass

        try:
            from .MainWindow import Memory
            Memory.initial_already_run = 0
        except ImportError:
            pass

        try:
            from .MainWindow import Disk
            Disk.initial_already_run = 0
        except ImportError:
            pass

        try:
            from .MainWindow import Network
            Network.initial_already_run = 0
        except ImportError:
            pass

        try:
            from .MainWindow import Gpu
            Gpu.initial_already_run = 0
        except ImportError:
            pass

        try:
            from .MainWindow import Sensors
            Sensors.initial_already_run = 0
        except ImportError:
            pass

        try:
            from .MainWindow import Processes
            Processes.initial_already_run = 0
        except ImportError:
            pass

        try:
            from .MainWindow import Users
            Users.initial_already_run = 0
        except ImportError:
            pass

        try:
            from .MainWindow import Services
            Services.initial_already_run = 0
        except ImportError:
            pass

        try:
            from .MainWindow import System
            System.initial_already_run = 0
        except ImportError:
            pass

        MainWindow.main_gui_tab_loop()


    def settings_gui_default_tab_func(self):
        """
        Save default main tab and performace tab sub-tab when "Remember last opened tabs" option is enabled.
        """

        if "selected" in MainWindow.performance_tb.state():
            Config.default_main_tab = 0
        if "selected" in MainWindow.processes_tb.state():
            Config.default_main_tab = 1
        if "selected" in MainWindow.users_tb.state():
            Config.default_main_tab = 2
        if "selected" in MainWindow.services_tb.state():
            Config.default_main_tab = 3
        if "selected" in MainWindow.system_tb.state():
            Config.default_main_tab = 4

        if "selected" in MainWindow.summary_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 0
        if "selected" in MainWindow.cpu_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 1
        if "selected" in MainWindow.memory_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 2
        if "selected" in MainWindow.disk_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 3
        if "selected" in MainWindow.network_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 4
        if "selected" in MainWindow.gpu_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 5
        if "selected" in MainWindow.sensors_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 6


    def on_reset_all_settings_button_clicked(self):
        """
        Generate messagedialog GUI.
        """

        answer = messagebox.askyesno("Reset all settings of the application", "Do you want to reset all settings to defaults?", parent=self.settings_window)

        if answer == True:
            self.reset_all_settings_func()
        else:
            pass


    def reset_all_settings_func(self):
        """
        Function for resetting all settings of the application.
        """

        Config.config_default_reset_all_func()
        Config.config_save_func()
        self.general_settings_set_gui()

        # Reset "Light/Dark theme" setting.
        MainWindow.light_dark_theme()

        # Length of performance data lists (cpu_usage_percent_ave, ram_usage_percent_ave, ...)
        # have to be set after "chart_data_history" setting is reset in order to avoid errors.
        self.settings_gui_set_chart_data_history_func()

        # Apply selected CPU core, disk, network card changes
        Performance.performance_set_selected_cpu_core_func()
        Performance.performance_set_selected_disk_func()
        Performance.performance_set_selected_network_card_func()
        # Apply selected GPU changes
        try:
            from .MainWindow import Gpu
            Libsysmon.gpu_set_selected_gpu(Gpu.selected_gpu, Gpu.default_gpu, Gpu.gpu_list)
        # Prevent errors because "gpu_get_gpu_list_and_set_selected_gpu_func" module requires
        # some modules in the Gpu module. They are imported if Gpu tab is switched on.
        except ImportError:
            pass

        # Reset selected device on the list between Performance tab sub-tab list.
        if Config.performance_tab_current_sub_tab != -1:
            MainWindow.main_gui_device_selection_list()

        # Apply changes immediately (without waiting update interval).
        self.settings_gui_apply_settings_immediately_func()


    # ***********************************************************************************************
    #                                           Summary
    # ***********************************************************************************************

    def summary_settings_tab_gui(self):

        global Summary
        from .Summary import Summary

        # Frame
        frame = ttk.Frame(self.frame_summary_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        # Label (Graph - Show)
        label = Common.bold_label(frame, _tr("Graph - Show"))
        label.grid(row=1, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (GPU Usage)0
        self.summary_gpu_usage_var = tk.IntVar()
        self.summary_gpu_usage_cb = Common.checkbutton(frame, _tr("GPU Usage"), self.summary_gpu_usage_var, self.on_summary_gpu_usage_cb_toggled)
        self.summary_gpu_usage_cb.grid(row=1, column=0, sticky="w", padx=0, pady=0)

        # Label - (This increases CPU usage.)
        label = ttk.Label(frame, text=_tr("This increases CPU usage."))
        label.grid(row=2, column=0, padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=3, column=0, sticky="ew", padx=0, pady=10)

        # Button (Reset)
        self.reset_summary_settings_button = Common.reset_button(frame)
        self.reset_summary_settings_button.grid(row=4, column=0, padx=0, pady=0)

        # Connect signals
        self.settings_window.after(1, self.summary_settings_set_gui)
        self.reset_summary_settings_button.config(command=self.on_reset_summary_settings_button_clicked)


    def on_summary_gpu_usage_cb_toggled(self):
        Config.summary_show_gpu_usage = self.summary_gpu_usage_var.get()
        Common.save_tab_settings(Summary)

    def on_reset_summary_settings_button_clicked(self):
        Config.config_default_performance_summary_func()
        Config.config_save_func()
        Common.update_tab_and_menu_gui(self.summary_settings_set_gui, Summary)

    def summary_settings_set_gui(self):
        self.summary_gpu_usage_var.set(Config.summary_show_gpu_usage)


    # ***********************************************************************************************
    #                                           CPU
    # ***********************************************************************************************

    def cpu_settings_tab_gui(self):

        global Cpu
        from .Cpu import Cpu

        # Frame
        frame = ttk.Frame(self.frame_cpu_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        # Label (Graph - Show)
        label = Common.bold_label(frame, _tr("Graph - Show"))
        label.grid(row=0, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (CPU Usage (Average))
        self.cpu_usage_average_var = tk.IntVar()
        self.cpu_usage_average_rb = Common.radiobutton(frame, _tr("CPU Usage (Average)"), self.cpu_usage_average_var, 0, self.on_cpu_usage_average_rb_toggled)
        self.cpu_usage_average_rb.grid(row=1, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (CPU Usage (Per Core))
        self.cpu_usage_average_rb = Common.radiobutton(frame, _tr("CPU Usage (Per Core)"), self.cpu_usage_average_var, 1, self.on_cpu_usage_average_rb_toggled)
        self.cpu_usage_average_rb.grid(row=2, column=0, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=3, column=0, sticky="ew", padx=0, pady=10)

        # CheckButton (Show processes using max CPU)
        self.show_processes_using_max_cpu_var = tk.IntVar()
        self.show_processes_using_max_cpu_cb = Common.checkbutton(frame, _tr("Show processes using max CPU"), self.show_processes_using_max_cpu_var, self.on_show_processes_using_max_cpu_cb_toggled)
        self.show_processes_using_max_cpu_cb.grid(row=4, column=0, sticky="w", padx=0, pady=0)

        # Label - precision (CPU)
        label = ttk.Label(frame, text=_tr("This increases CPU usage.") + "\n" + "(" + _tr("for all tabs") + ")")
        label.grid(row=5, column=0, padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=6, column=0, sticky="ew", padx=0, pady=10)

        # Label (Cache)
        label = Common.bold_label(frame, _tr("Cache"))
        label.grid(row=7, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (CPU Socket)
        self.cpu_cache_var = tk.StringVar()
        self.cpu_cache_socket_rb = Common.radiobutton(frame, _tr("CPU Socket"), self.cpu_cache_var, "socket", self.on_cpu_cache_type_rb_toggled)
        self.cpu_cache_socket_rb.grid(row=8, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (Selected CPU Core)
        self.cpu_cache_cpu_core_rb = Common.radiobutton(frame, _tr("Selected CPU Core"), self.cpu_cache_var, "core", self.on_cpu_cache_type_rb_toggled)
        self.cpu_cache_cpu_core_rb.grid(row=9, column=0, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=10, column=0, sticky="ew", padx=0, pady=10)

        # Button (Reset)
        self.reset_cpu_settings_button = Common.reset_button(frame)
        self.reset_cpu_settings_button.grid(row=11, column=0, padx=0, pady=0)

        # Connect signals
        self.settings_window.after(1, self.cpu_settings_set_gui)
        self.reset_cpu_settings_button.config(command=self.on_reset_cpu_settings_button_clicked)


    def on_cpu_usage_average_rb_toggled(self):
        Config.show_cpu_usage_per_core = self.cpu_usage_average_var.get()
        Common.save_tab_settings(Cpu)

    def on_show_processes_using_max_cpu_cb_toggled(self):
        Config.show_processes_using_max_cpu = self.show_processes_using_max_cpu_var.get()
        Common.save_tab_settings(Cpu)

    def on_cpu_cache_type_rb_toggled(self):
        Config.show_cpu_cache_type = self.cpu_cache_var.get()
        Common.save_tab_settings(Cpu)

    def on_reset_cpu_settings_button_clicked(self):
        # Load default settings
        Config.config_default_performance_cpu_func()
        Config.config_save_func()
        Performance.performance_set_selected_cpu_core_func()
        # Reset device list between Performance tab sub-tabs because selected device is reset.
        #MainWindow.main_gui_device_selection_list()
        Common.update_tab_and_menu_gui(self.cpu_settings_set_gui, Cpu)

    def cpu_settings_set_gui(self):
        self.cpu_usage_average_var.set(Config.show_cpu_usage_per_core)
        self.show_processes_using_max_cpu_var.set(Config.show_processes_using_max_cpu)
        self.cpu_cache_var.set(Config.show_cpu_cache_type)


    # ***********************************************************************************************
    #                                           Memory
    # ***********************************************************************************************

    def memory_settings_tab_gui(self):

        global Memory
        from .Memory import Memory

        # Frame
        frame = ttk.Frame(self.frame_memory_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        # Label (Graph - Show)
        label = Common.bold_label(frame, _tr("Graph - Show"))
        label.grid(row=0, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # RadioButton (RAM)
        self.ram_usage_var = tk.IntVar()
        self.ram_usage_rb = Common.radiobutton(frame, _tr("RAM"), self.ram_usage_var, 0, self.on_memory_type_rb_toggled)
        self.ram_usage_rb.grid(row=1, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (Memory)
        self.memory_usage_rb = Common.radiobutton(frame, _tr("Memory"), self.ram_usage_var, 1, self.on_memory_type_rb_toggled)
        self.memory_usage_rb.grid(row=1, column=1, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=2, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Label (Data Unit)
        label = Common.bold_label(frame, _tr("Data Unit"))
        label.grid(row=3, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # Label - (Show data as powers of:)
        label = ttk.Label(frame, text=_tr("Show data as powers of") + ":")
        label.grid(row=4, column=0, columnspan=2, padx=0, pady=0)

        # RadioButton (1024)
        self.memory_data_power_of_var = tk.IntVar()
        self.memory_data_power_of_1024_rb = Common.radiobutton(frame, _tr("1024"), self.memory_data_power_of_var, 0, self.on_memory_data_power_of_rb_toggled)
        self.memory_data_power_of_1024_rb.grid(row=5, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (1000)
        self.memory_data_power_of_1000_rb = Common.radiobutton(frame, _tr("1000"), self.memory_data_power_of_var, 1, self.on_memory_data_power_of_rb_toggled)
        self.memory_data_power_of_1000_rb.grid(row=5, column=1, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=6, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Button (Reset)
        self.reset_memory_settings_button = Common.reset_button(frame)
        self.reset_memory_settings_button.grid(row=7, column=0, columnspan=2, padx=0, pady=0)

        # Connect signals
        self.settings_window.after(1, self.memory_settings_set_gui)
        self.reset_memory_settings_button.config(command=self.on_reset_memory_settings_button_clicked)


    def on_memory_type_rb_toggled(self):
        Config.show_memory_usage_per_memory = self.ram_usage_var.get()
        Common.save_tab_settings(Memory)

    def on_memory_data_power_of_rb_toggled(self):
        Config.performance_memory_data_unit = self.memory_data_power_of_var.get()
        Common.save_tab_settings(Memory)

    def on_reset_memory_settings_button_clicked(self):
        # Load default settings
        Config.config_default_performance_memory_func()
        Config.config_save_func()
        # Reset device list between Performance tab sub-tabs because selected device is reset.
        #MainWindow.main_gui_device_selection_list()
        Common.update_tab_and_menu_gui(self.memory_settings_set_gui, Memory)

    def memory_settings_set_gui(self):
        self.ram_usage_var.set(Config.show_memory_usage_per_memory)
        self.memory_data_power_of_var.set(Config.performance_memory_data_unit)


    # ***********************************************************************************************
    #                                           Disk
    # ***********************************************************************************************

    def disk_settings_tab_gui(self):

        global Disk
        from .Disk import Disk

        # Frame
        frame = ttk.Frame(self.frame_disk_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        # Label (Graph - Show)
        label = Common.bold_label(frame, _tr("Graph - Show"))
        label.grid(row=0, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # CheckButton (Read Speed)
        self.disk_read_speed_var = tk.IntVar()
        self.disk_read_speed_cb = Common.checkbutton(frame, _tr("Read Speed"), self.disk_read_speed_var, self.on_disk_read_speed_cb_toggled)
        self.disk_read_speed_cb.grid(row=1, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Write Speed)
        self.disk_write_speed_var = tk.IntVar()
        self.write_speed_cb = Common.checkbutton(frame, _tr("Write Speed"), self.disk_write_speed_var, self.on_disk_write_speed_cb_toggled)
        self.write_speed_cb.grid(row=1, column=1, sticky="w", padx=0, pady=0)

        # RadioButton (Selected Device)
        self.disk_selected_device_var = tk.IntVar()
        self.disk_selected_device_rb = Common.radiobutton(frame, _tr("Selected Device"), self.disk_selected_device_var, 0, self.on_disk_device_selection_rb_toggled)
        self.disk_selected_device_rb.grid(row=2, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (All Devices)
        self.disk_all_devices_rb = Common.radiobutton(frame, _tr("All Devices"), self.disk_selected_device_var, 1, self.on_disk_device_selection_rb_toggled)
        self.disk_all_devices_rb.grid(row=2, column=1, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=3, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Label (Data Unit)
        label = Common.bold_label(frame, _tr("Data Unit"))
        label.grid(row=4, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # Label - (Show data as powers of:)
        label = ttk.Label(frame, text=_tr("Show data as powers of") + ":")
        label.grid(row=5, column=0, columnspan=2, padx=0, pady=0)

        # RadioButton (1024)
        self.disk_data_power_of_var = tk.IntVar()
        self.disk_data_power_of_1024_rb = Common.radiobutton(frame, _tr("1024"), self.disk_data_power_of_var, 0, self.on_disk_data_power_of_rb_toggled)
        self.disk_data_power_of_1024_rb.grid(row=6, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (1000)
        self.disk_data_power_of_1000_rb = Common.radiobutton(frame, _tr("1000"), self.disk_data_power_of_var, 1, self.on_disk_data_power_of_rb_toggled)
        self.disk_data_power_of_1000_rb.grid(row=6, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Show speed units as multiples of bits)
        self.disk_data_bits_var = tk.IntVar()
        self.disk_data_bits_cb = Common.checkbutton(frame, _tr("Show speed units as multiples of bits"), self.disk_data_bits_var, self.on_disk_data_bits_cb_toggled)
        self.disk_data_bits_cb.grid(row=7, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=8, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Label (Data Unit)
        label = Common.bold_label(frame, _tr("Disk"))
        label.grid(row=9, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # CheckButton (Hide loop, ramdisk, zram disks)
        self.disk_hide_loop_ramdisk_zram_disks_var = tk.IntVar()
        self.hide_loop_ramdisk_zram_disks_cb = Common.checkbutton(frame, _tr("Hide loop, ramdisk, zram disks"), self.disk_hide_loop_ramdisk_zram_disks_var, self.on_hide_loop_ramdisk_zram_disks_cb_toggled)
        self.hide_loop_ramdisk_zram_disks_cb.grid(row=10, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=11, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Button (Reset)
        self.reset_disk_settings_button = Common.reset_button(frame)
        self.reset_disk_settings_button.grid(row=12, column=0, columnspan=2, padx=0, pady=0)

        # Connect signals
        self.settings_window.after(1, self.disk_settings_set_gui)
        self.reset_disk_settings_button.config(command=self.on_reset_disk_settings_button_clicked)


    def on_disk_read_speed_cb_toggled(self):
        Config.plot_disk_read_speed = self.disk_read_speed_var.get()
        Common.save_tab_settings(Disk)

    def on_disk_write_speed_cb_toggled(self):
        Config.plot_disk_write_speed = self.disk_write_speed_var.get()
        Common.save_tab_settings(Disk)

    def on_disk_device_selection_rb_toggled(self):
        Config.show_disk_usage_per_disk = self.disk_selected_device_var.get()
        Common.save_tab_settings(Disk)

    def on_disk_data_power_of_rb_toggled(self):
        Config.performance_disk_data_unit = self.disk_data_power_of_var.get()
        Common.save_tab_settings(Disk)

    def on_disk_data_bits_cb_toggled(self):
        Config.performance_disk_speed_bit = self.disk_data_bits_var.get()
        Common.save_tab_settings(Disk)

    def on_hide_loop_ramdisk_zram_disks_cb_toggled(self):
        Config.hide_loop_ramdisk_zram_disks = self.disk_hide_loop_ramdisk_zram_disks_var.get()
        Common.save_tab_settings(Disk)

    def on_reset_disk_settings_button_clicked(self):
        # Load default settings
        Config.config_default_performance_disk_func()
        Config.config_save_func()
        # Reset device list between Performance tab sub-tabs because selected device is reset.
        #MainWindow.main_gui_device_selection_list()
        Common.update_tab_and_menu_gui(self.disk_settings_set_gui, Disk)

    def disk_settings_set_gui(self):
        self.disk_read_speed_var.set(Config.plot_disk_read_speed)
        self.disk_write_speed_var.set(Config.plot_disk_write_speed)
        self.disk_selected_device_var.set(Config.show_disk_usage_per_disk)
        self.disk_data_power_of_var.set(Config.performance_disk_data_unit)
        self.disk_data_bits_var.set(Config.performance_disk_speed_bit)
        self.disk_hide_loop_ramdisk_zram_disks_var.set(Config.hide_loop_ramdisk_zram_disks)


    # ***********************************************************************************************
    #                                           Network
    # ***********************************************************************************************

    def network_settings_tab_gui(self):

        global Network
        from .Network import Network

        # Frame
        frame = ttk.Frame(self.frame_network_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        # Label (Graph - Show)
        label = Common.bold_label(frame, _tr("Graph - Show"))
        label.grid(row=0, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # CheckButton (Download Speed)
        self.network_download_speed_var = tk.IntVar()
        self.network_download_speed_cb = Common.checkbutton(frame, _tr("Download Speed"), self.network_download_speed_var, self.on_download_speed_cb_toggled)
        self.network_download_speed_cb.grid(row=1, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Upload Speed)
        self.network_upload_speed_var = tk.IntVar()
        self.network_upload_speed_cb = Common.checkbutton(frame, _tr("Upload Speed"), self.network_upload_speed_var, self.on_upload_speed_cb_toggled)
        self.network_upload_speed_cb.grid(row=1, column=1, sticky="w", padx=0, pady=0)

        # RadioButton (Selected Device)
        self.network_selected_device_var = tk.IntVar()
        self.network_selected_device_rb = Common.radiobutton(frame, _tr("Selected Device"), self.network_selected_device_var, 0, self.on_device_selection_rb_toggled)
        self.network_selected_device_rb.grid(row=2, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (All Devices)
        self.network_all_devices_rb = Common.radiobutton(frame, _tr("All Devices"), self.network_selected_device_var, 1, self.on_device_selection_rb_toggled)
        self.network_all_devices_rb.grid(row=2, column=1, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=3, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Label (Data Unit)
        label = Common.bold_label(frame, _tr("Data Unit"))
        label.grid(row=4, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # Label - (Show data as powers of:)
        label = ttk.Label(frame, text=_tr("Show data as powers of") + ":")
        label.grid(row=5, column=0, columnspan=2, padx=0, pady=0)

        # RadioButton (1024)
        self.network_data_power_of_var = tk.IntVar()
        self.network_data_power_of_1024_rb = Common.radiobutton(frame, _tr("1024"), self.network_data_power_of_var, 0, self.on_data_power_of_rb_toggled)
        self.network_data_power_of_1024_rb.grid(row=6, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (1000)
        self.network_data_power_of_1000_rb = Common.radiobutton(frame, _tr("1000"), self.network_data_power_of_var, 1, self.on_data_power_of_rb_toggled)
        self.network_data_power_of_1000_rb.grid(row=6, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Show speed units as multiples of bits)
        self.network_data_bits_var = tk.IntVar()
        self.network_data_bits_cb = Common.checkbutton(frame, _tr("Show speed units as multiples of bits"), self.network_data_bits_var, self.on_data_bits_cb_toggled)
        self.network_data_bits_cb.grid(row=7, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=8, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Button (Reset)
        self.reset_network_settings_button = Common.reset_button(frame)
        self.reset_network_settings_button.grid(row=9, column=0, columnspan=2, padx=0, pady=0)

        # Connect signals
        self.settings_window.after(1, self.network_settings_set_gui)
        self.reset_network_settings_button.config(command=self.on_reset_network_settings_button_clicked)


    def on_download_speed_cb_toggled(self):
        Config.plot_network_download_speed = self.network_download_speed_var.get()
        Common.save_tab_settings(Network)

    def on_upload_speed_cb_toggled(self):
        Config.plot_network_upload_speed = self.network_upload_speed_var.get()
        Common.save_tab_settings(Network)

    def on_device_selection_rb_toggled(self):
        Config.show_network_usage_per_network_card = self.network_selected_device_var.get()
        Common.save_tab_settings(Network)

    def on_data_power_of_rb_toggled(self):
        Config.performance_network_data_unit = self.network_data_power_of_var.get()
        Common.save_tab_settings(Network)

    def on_data_bits_cb_toggled(self):
        Config.performance_network_speed_bit = self.network_data_bits_var.get()
        Common.save_tab_settings(Network)

    def on_reset_network_settings_button_clicked(self):
        # Load default settings
        Config.config_default_performance_network_func()
        Config.config_save_func()
        # Reset device list between Performance tab sub-tabs because selected device is reset.
        #MainWindow.main_gui_device_selection_list()
        Common.update_tab_and_menu_gui(self.network_settings_set_gui, Network)

    def network_settings_set_gui(self):
        self.network_download_speed_var.set(Config.plot_network_download_speed)
        self.network_upload_speed_var.set(Config.plot_network_upload_speed)
        self.network_selected_device_var.set(Config.show_network_usage_per_network_card)
        self.network_data_power_of_var.set(Config.performance_network_data_unit)
        self.network_data_bits_var.set(Config.performance_network_speed_bit)


    # ***********************************************************************************************
    #                                           Sensors
    # ***********************************************************************************************

    def sensors_settings_tab_gui(self):

        global Sensors
        from .Sensors import Sensors

        # Frame
        frame = ttk.Frame(self.frame_sensors_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        # Label (Data Unit)
        label = Common.bold_label(frame, _tr("Data Unit"))
        label.grid(row=0, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # RadioButton (°C)
        self.temperature_unit_var = tk.StringVar()
        self.celsius_rb = Common.radiobutton(frame, _tr("°C"), self.temperature_unit_var, "celsius", self.on_temperature_unit_rb_toggled)
        self.celsius_rb.grid(row=1, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (°F)
        self.fahrenheit_rb = Common.radiobutton(frame, _tr("°F"), self.temperature_unit_var, "fahrenheit", self.on_temperature_unit_rb_toggled)
        self.fahrenheit_rb.grid(row=1, column=1, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=2, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Button (Reset)
        self.reset_sensors_settings_button = Common.reset_button(frame)
        self.reset_sensors_settings_button.grid(row=3, column=0, columnspan=2, padx=0, pady=0)

        # Connect signals
        self.settings_window.after(1, self.sensors_settings_set_gui)
        self.reset_sensors_settings_button.config(command=self.on_sensors_settings_reset_button_clicked)


    def on_temperature_unit_rb_toggled(self):
        Config.temperature_unit = self.temperature_unit_var.get()
        Common.save_tab_settings(Sensors)

    def on_sensors_settings_reset_button_clicked(self):
        # Load default settings
        Config.config_default_performance_sensors_func()
        Config.config_save_func()
        # Reset device list between Performance tab sub-tabs because selected device is reset.
        #MainWindow.main_gui_device_selection_list()
        Common.update_tab_and_menu_gui(self.sensors_settings_set_gui, Sensors)

    def sensors_settings_set_gui(self):
        self.temperature_unit_var.set(Config.temperature_unit)


    # ***********************************************************************************************
    #                                           Processes
    # ***********************************************************************************************

    def processes_settings_tab_gui(self):

        global Processes
        from .Processes import Processes

        # Frame
        frame = ttk.Frame(self.frame_processes_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        # Notebook
        style = ttk.Style()
        style.configure("horizontal.TNotebook", tabposition="n")

        notebook = ttk.Notebook(frame, style="horizontal.TNotebook")
        notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Button (Reset)
        self.reset_processes_settings_button = Common.reset_button(frame)
        self.reset_processes_settings_button.grid(row=1, column=0, columnspan=2, padx=0, pady=0)

        # View Tab
        self.frame_processes_view_tab = tk.Frame(notebook)
        notebook.add(self.frame_processes_view_tab, text=_tr("View"))
        #self.frame_summary_tab.grid_configure(ipadx=10, ipady=10)

        # Add/Remove Columns Tab
        self.frame_processes_add_remove_columns_tab = tk.Frame(notebook)
        notebook.add(self.frame_processes_add_remove_columns_tab, text=_tr("Add/Remove Columns"))

        # Connect signals
        self.settings_window.after(1, self.processes_settings_set_gui)
        self.reset_processes_settings_button.config(command=self.on_reset_processes_settings_button_clicked)

        # CheckButton (Show processes of all users)
        self.show_processes_of_all_users_var = tk.IntVar()
        self.show_processes_of_all_users_cb = Common.checkbutton(self.frame_processes_view_tab, _tr("Show processes of all users"), self.show_processes_of_all_users_var, self.on_show_processes_of_all_users_cb_toggled)
        self.show_processes_of_all_users_cb.grid(row=1, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # CheckButton (Hide kernel threads)
        self.hide_kernel_threads_var = tk.IntVar()
        self.hide_kernel_threads_cb = Common.checkbutton(self.frame_processes_view_tab, _tr("Hide kernel threads"), self.hide_kernel_threads_var, self.on_hide_kernel_threads_cb_toggled)
        self.hide_kernel_threads_cb.grid(row=2, column=0, columnspan=2, sticky="w", padx=(10,0), pady=0)

        # CheckButton (Show processes as tree)
        self.show_processes_as_tree_var = tk.IntVar()
        self.show_processes_as_tree_cb = Common.checkbutton(self.frame_processes_view_tab, _tr("Show processes as tree"), self.show_processes_as_tree_var, self.on_show_processes_as_tree_cb_toggled)
        self.show_processes_as_tree_cb.grid(row=3, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(self.frame_processes_view_tab, orient="horizontal")
        separator.grid(row=4, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Label - (CPU)
        label = ttk.Label(self.frame_processes_view_tab, text=_tr("CPU"))
        label.grid(row=5, column=0, columnspan=2, padx=0, pady=0)

        # CheckButton (Divide CPU usage by core count)
        self.processes_cpu_divide_by_core_var = tk.IntVar()
        self.processes_cpu_divide_by_core_cb = Common.checkbutton(self.frame_processes_view_tab, _tr("Divide CPU usage by core count"), self.processes_cpu_divide_by_core_var, self.on_processes_cpu_divide_by_core_cb_toggled)
        self.processes_cpu_divide_by_core_cb.grid(row=6, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # Label - (Memory)
        label = ttk.Label(self.frame_processes_view_tab, text=_tr("Memory"))
        label.grid(row=7, column=0, columnspan=2, padx=0, pady=0)

        # Label - (Show data as powers of:)
        label = ttk.Label(self.frame_processes_view_tab, text=_tr("Show data as powers of") + ":")
        label.grid(row=8, column=0, columnspan=2, padx=0, pady=0)

        # RadioButton (1024)
        self.processes_memory_data_power_of_var = tk.IntVar()
        self.memory_data_power_of_1024_rb = Common.radiobutton(self.frame_processes_view_tab, _tr("1024"), self.processes_memory_data_power_of_var, 0, self.on_memory_data_power_of_toggle)
        self.memory_data_power_of_1024_rb.grid(row=9, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (1000)
        self.memory_data_power_of_1000_rb = Common.radiobutton(self.frame_processes_view_tab, _tr("1000"), self.processes_memory_data_power_of_var, 1, self.on_memory_data_power_of_toggle)
        self.memory_data_power_of_1000_rb.grid(row=9, column=1, sticky="w", padx=0, pady=0)

        # Label - (Disk
        label = ttk.Label(self.frame_processes_view_tab, text=_tr("Disk"))
        label.grid(row=10, column=0, columnspan=2, padx=0, pady=0)

        # Label - (Show data as powers of:)
        label = ttk.Label(self.frame_processes_view_tab, text=_tr("Show data as powers of") + ":")
        label.grid(row=11, column=0, columnspan=32, padx=0, pady=0)

        # RadioButton (1024)
        self.processes_disk_data_power_of_var = tk.IntVar()
        self.disk_data_power_of_1024_rb = Common.radiobutton(self.frame_processes_view_tab, _tr("1024"), self.processes_disk_data_power_of_var, 0, self.on_disk_data_power_of_toggle)
        self.disk_data_power_of_1024_rb.grid(row=12, column=0, sticky="w", padx=0, pady=0)

        # RadioButton (1000)
        self.disk_data_power_of_1000_rb = Common.radiobutton(self.frame_processes_view_tab, _tr("1000"), self.processes_disk_data_power_of_var, 1, self.on_disk_data_power_of_toggle)
        self.disk_data_power_of_1000_rb.grid(row=12, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Show speed units as multiples of bits)
        self.show_speed_units_bytes_var = tk.IntVar()
        self.show_speed_units_bytes_cb = Common.checkbutton(self.frame_processes_view_tab, _tr("Show speed units as multiples of bits"), self.show_speed_units_bytes_var, self.on_show_speed_units_bytes_cb_toggle)
        self.show_speed_units_bytes_cb.grid(row=13, column=0, columnspan=2, sticky="w", padx=0, pady=0)

        # CheckButton (Name)
        self.processes_name_var = tk.IntVar()
        self.processes_name_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Name"), self.processes_name_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_name_cb.grid(row=1, column=0, sticky="w", padx=0, pady=0)
        self.processes_name_cb.config(state="disabled")

        # CheckButton (PID)
        self.processes_pid_var = tk.IntVar()
        self.processes_pid_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("PID"), self.processes_pid_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_pid_cb.grid(row=2, column=0, sticky="w", padx=0, pady=0)
        self.processes_pid_cb.config(state="disabled")

        # CheckButton (User)
        self.processes_user_var = tk.IntVar()
        self.processes_user_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("User"), self.processes_user_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_user_cb.grid(row=3, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Status)
        self.processes_status_var = tk.IntVar()
        self.processes_status_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Status"), self.processes_status_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_status_cb.grid(row=4, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (CPU)
        self.processes_cpu_var = tk.IntVar()
        self.processes_cpu_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("CPU"), self.processes_cpu_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_cpu_cb.grid(row=5, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Memory)
        self.processes_memory_var = tk.IntVar()
        self.processes_memory_cb  = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Memory"), self.processes_memory_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_memory_cb .grid(row=6, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Memory (RSS))
        self.processes_memory_rss_var = tk.IntVar()
        self.processes_memory_rss_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Memory (RSS)"), self.processes_memory_rss_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_memory_rss_cb.grid(row=7, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Memory (VMS))
        self.processes_memory_vms_var = tk.IntVar()
        self.processes_memory_vms_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Memory (VMS)"), self.processes_memory_vms_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_memory_vms_cb.grid(row=8, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Memory (Shared))
        self.processes_memory_shared_var = tk.IntVar()
        self.processes_memory_shared_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Memory (Shared)"), self.processes_memory_shared_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_memory_shared_cb.grid(row=9, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Read Data)
        self.processes_read_data_var = tk.IntVar()
        self.processes_read_data_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Read Data"), self.processes_read_data_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_read_data_cb.grid(row=10, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Written Data)
        self.processes_written_data_var = tk.IntVar()
        self.processes_written_data_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Written Data"), self.processes_written_data_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_written_data_cb.grid(row=11, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Read Speed)
        self.processes_read_speed_var = tk.IntVar()
        self.processes_read_speed_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Read Speed"), self.processes_read_speed_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_read_speed_cb.grid(row=12, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Write Speed)
        self.processes_write_speed_var = tk.IntVar()
        self.processes_write_speed_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Write Speed"), self.processes_write_speed_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_write_speed_cb.grid(row=1, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Priority)
        self.processes_nice_var = tk.IntVar()
        self.processes_nice_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Priority"), self.processes_nice_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_nice_cb.grid(row=2, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Threads)
        self.processes_threads_var = tk.IntVar()
        self.processes_threads_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Threads"), self.processes_threads_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_threads_cb.grid(row=3, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (PPID)
        self.processes_ppid_var = tk.IntVar()
        self.processes_ppid_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("PPID"), self.processes_ppid_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_ppid_cb.grid(row=4, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (UID)
        self.processes_uid_var = tk.IntVar()
        self.processes_uid_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("UID"), self.processes_uid_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_uid_cb.grid(row=5, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (GID)
        self.processes_gid_var = tk.IntVar()
        self.processes_gid_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("GID"), self.processes_gid_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_gid_cb.grid(row=6, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Start Time)
        self.processes_start_time_var = tk.IntVar()
        self.processes_start_time_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Start Time"), self.processes_start_time_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_start_time_cb.grid(row=7, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Command Line)
        self.processes_command_line_var = tk.IntVar()
        self.processes_command_line_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Command Line"), self.processes_command_line_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_command_line_cb.grid(row=8, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (CPU Time)
        self.processes_cpu_time_var = tk.IntVar()
        self.processes_cpu_time_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("CPU Time"), self.processes_cpu_time_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_cpu_time_cb.grid(row=9, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (CPU - Recursive)
        self.processes_cpu_recursive_var = tk.IntVar()
        self.processes_cpu_recursive_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("CPU") + " - " + _tr("Recursive"), self.processes_cpu_recursive_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_cpu_recursive_cb.grid(row=10, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Memory (RSS) - Recursive)
        self.processes_memory_rss_recursive_var = tk.IntVar()
        self.processes_memory_rss_recursive_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Memory (RSS)") + " - " + _tr("Recursive"), self.processes_memory_rss_recursive_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_memory_rss_recursive_cb.grid(row=11, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Memory - Recursive)
        self.processes_memory_recursive_var = tk.IntVar()
        self.processes_memory_recursive_cb = Common.checkbutton(self.frame_processes_add_remove_columns_tab, _tr("Memory") + " - " + _tr("Recursive"), self.processes_memory_recursive_var, self.on_processes_add_remove_checkbuttons_toggled)
        self.processes_memory_recursive_cb.grid(row=12, column=1, sticky="w", padx=0, pady=0)


    def on_reset_processes_settings_button_clicked(self):
        # Load default settings
        Config.config_default_processes_func()
        Config.config_save_func()
        # Reset device list between Performance tab sub-tabs because selected device is reset.
        #MainWindow.main_gui_device_selection_list()
        Common.update_tab_and_menu_gui(self.processes_settings_set_gui, Processes)

    def on_show_processes_of_all_users_cb_toggled(self):
        Config.show_processes_of_all_users = self.show_processes_of_all_users_var.get()
        Common.save_tab_settings(Processes)

    def on_hide_kernel_threads_cb_toggled(self):
        Config.hide_kernel_threads = self.hide_kernel_threads_var.get()
        Common.save_tab_settings(Processes)

    def on_show_processes_as_tree_cb_toggled(self):
        Config.show_processes_as_tree = self.show_processes_as_tree_var.get()
        Common.save_tab_settings(Processes)

    def on_processes_cpu_divide_by_core_cb_toggled(self):
        Config.processes_cpu_divide_by_core = self.processes_cpu_divide_by_core_var.get()
        Common.save_tab_settings(Processes)

    def on_memory_data_power_of_toggle(self):
        Config.processes_memory_data_unit = self.processes_memory_data_power_of_var.get()
        Common.save_tab_settings(Processes)

    def on_disk_data_power_of_toggle(self):
        Config.processes_disk_data_unit = self.processes_disk_data_power_of_var.get()
        Common.save_tab_settings(Processes)

    def on_show_speed_units_bytes_cb_toggle(self):
        Config.processes_disk_speed_bit = self.show_speed_units_bytes_var.get()
        Common.save_tab_settings(Processes)

    def on_processes_add_remove_checkbuttons_toggled(self):
        Config.processes_columns_shown = []
        if self.processes_name_var.get() == 1:
            Config.processes_columns_shown.append("name")
        if self.processes_pid_var.get() == 1:
            Config.processes_columns_shown.append("pid")
        if self.processes_user_var.get() == 1:
            Config.processes_columns_shown.append("username")
        if self.processes_status_var.get() == 1:
            Config.processes_columns_shown.append("status")
        if self.processes_cpu_var.get() == 1:
            Config.processes_columns_shown.append("cpu_usage")
        if self.processes_memory_var.get() == 1:
            Config.processes_columns_shown.append("memory")
        if self.processes_memory_rss_var.get() == 1:
            Config.processes_columns_shown.append("memory_rss")
        if self.processes_memory_vms_var.get() == 1:
            Config.processes_columns_shown.append("memory_vms")
        if self.processes_memory_shared_var.get() == 1:
            Config.processes_columns_shown.append("memory_shared")
        if self.processes_read_data_var.get() == 1:
            Config.processes_columns_shown.append("read_data")
        if self.processes_written_data_var.get() == 1:
            Config.processes_columns_shown.append("written_data")
        if self.processes_read_speed_var.get() == 1:
            Config.processes_columns_shown.append("read_speed")
        if self.processes_write_speed_var.get() == 1:
            Config.processes_columns_shown.append("write_speed")
        if self.processes_nice_var.get() == 1:
            Config.processes_columns_shown.append("nice")
        if self.processes_threads_var.get() == 1:
            Config.processes_columns_shown.append("threads")
        if self.processes_ppid_var.get() == 1:
            Config.processes_columns_shown.append("ppid")
        if self.processes_uid_var.get() == 1:
            Config.processes_columns_shown.append("uid")
        if self.processes_gid_var.get() == 1:
            Config.processes_columns_shown.append("gid")
        if self.processes_start_time_var.get() == 1:
            Config.processes_columns_shown.append("start_time")
        if self.processes_command_line_var.get() == 1:
            Config.processes_columns_shown.append("command_line")
        if self.processes_cpu_time_var.get() == 1:
            Config.processes_columns_shown.append("cpu_time")
        if self.processes_cpu_recursive_var.get() == 1:
            Config.processes_columns_shown.append("cpu_recursive")
        if self.processes_memory_rss_recursive_var.get() == 1:
            Config.processes_columns_shown.append("memory_rss_recursive")
        if self.processes_memory_recursive_var.get() == 1:
            Config.processes_columns_shown.append("memory_recursive")

        Common.save_tab_settings(Processes)


    def processes_settings_set_gui(self):
        self.show_processes_of_all_users_var.set(Config.show_processes_of_all_users)
        self.hide_kernel_threads_var.set(Config.hide_kernel_threads)
        self.show_processes_as_tree_var.set(Config.show_processes_as_tree)
        self.processes_cpu_divide_by_core_var.set(Config.processes_cpu_divide_by_core)
        self.processes_memory_data_power_of_var.set(Config.processes_memory_data_unit)
        self.processes_disk_data_power_of_var.set(Config.processes_disk_data_unit)
        self.show_speed_units_bytes_var.set(Config.processes_disk_speed_bit)

        if "name" in Config.processes_columns_shown:
            self.processes_name_var.set(1)
        else:
            self.processes_name_var.set(0)
        if "pid" in Config.processes_columns_shown:
            self.processes_pid_var.set(1)
        else:
            self.processes_pid_var.set(0)
        if "username" in Config.processes_columns_shown:
            self.processes_user_var.set(1)
        else:
            self.processes_user_var.set(0)
        if "status" in Config.processes_columns_shown:
            self.processes_status_var.set(1)
        else:
            self.processes_status_var.set(0)
        if "cpu_usage" in Config.processes_columns_shown:
            self.processes_cpu_var.set(1)
        else:
            self.processes_cpu_var.set(0)
        if "memory" in Config.processes_columns_shown:
            self.processes_memory_var.set(1)
        else:
            self.processes_memory_var.set(0)
        if "memory_rss" in Config.processes_columns_shown:
            self.processes_memory_rss_var.set(1)
        else:
            self.processes_memory_rss_var.set(0)
        if "memory_vms" in Config.processes_columns_shown:
            self.processes_memory_vms_var.set(1)
        else:
            self.processes_memory_vms_var.set(0)
        if "memory_shared" in Config.processes_columns_shown:
            self.processes_memory_shared_var.set(1)
        else:
            self.processes_memory_shared_var.set(0)
        if "read_data" in Config.processes_columns_shown:
            self.processes_read_data_var.set(1)
        else:
            self.processes_read_data_var.set(0)
        if "written_data" in Config.processes_columns_shown:
            self.processes_written_data_var.set(1)
        else:
            self.processes_written_data_var.set(0)
        if "read_speed" in Config.processes_columns_shown:
            self.processes_read_speed_var.set(1)
        else:
            self.processes_read_speed_var.set(0)
        if "write_speed" in Config.processes_columns_shown:
            self.processes_write_speed_var.set(1)
        else:
            self.processes_write_speed_var.set(0)
        if "nice" in Config.processes_columns_shown:
            self.processes_nice_var.set(1)
        else:
            self.processes_nice_var.set(0)
        if "threads" in Config.processes_columns_shown:
            self.processes_threads_var.set(1)
        else:
            self.processes_threads_var.set(0)
        if "ppid" in Config.processes_columns_shown:
            self.processes_ppid_var.set(1)
        else:
            self.processes_ppid_var.set(0)
        if "uid" in Config.processes_columns_shown:
            self.processes_uid_var.set(1)
        else:
            self.processes_uid_var.set(0)
        if "gid" in Config.processes_columns_shown:
            self.processes_gid_var.set(1)
        else:
            self.processes_gid_var.set(0)
        if "start_time" in Config.processes_columns_shown:
            self.processes_start_time_var.set(1)
        else:
            self.processes_start_time_var.set(0)
        if "command_line" in Config.processes_columns_shown:
            self.processes_command_line_var.set(1)
        else:
            self.processes_command_line_var.set(0)
        if "cpu_time" in Config.processes_columns_shown:
            self.processes_cpu_time_var.set(1)
        else:
            self.processes_cpu_time_var.set(0)
        if "cpu_recursive" in Config.processes_columns_shown:
            self.processes_cpu_recursive_var.set(1)
        else:
            self.processes_cpu_recursive_var.set(0)
        if "memory_rss_recursive" in Config.processes_columns_shown:
            self.processes_memory_rss_recursive_var.set(1)
        else:
            self.processes_memory_rss_recursive_var.set(0)
        if "memory_recursive" in Config.processes_columns_shown:
            self.processes_memory_recursive_var.set(1)
        else:
            self.processes_memory_recursive_var.set(0)


    # ***********************************************************************************************
    #                                           Users
    # ***********************************************************************************************

    def users_settings_tab_gui(self):

        global Users
        from .Users import Users

        # Frame
        frame = ttk.Frame(self.frame_users_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)

        # CheckButton (User)
        self.users_user_var = tk.IntVar()
        self.users_user_cb = Common.checkbutton(frame, _tr("User"), self.users_user_var, self.on_users_add_remove_checkbuttons_toggled)
        self.users_user_cb.grid(row=0, column=0, sticky="w", padx=0, pady=0)
        self.users_user_cb.config(state="disabled")

        # CheckButton (Full Name)
        self.users_full_name_var = tk.IntVar()
        self.users_full_name_cb = Common.checkbutton(frame, _tr("Full Name"), self.users_full_name_var, self.on_users_add_remove_checkbuttons_toggled)
        self.users_full_name_cb.grid(row=1, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Logged In)
        self.users_logged_in_var = tk.IntVar()
        self.users_logged_in_cb = Common.checkbutton(frame, _tr("Logged In"), self.users_logged_in_var, self.on_users_add_remove_checkbuttons_toggled)
        self.users_logged_in_cb.grid(row=2, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (UID)
        self.users_uid_var = tk.IntVar()
        self.users_uid_cb = Common.checkbutton(frame, _tr("UID"),  self.users_uid_var, self.on_users_add_remove_checkbuttons_toggled)
        self.users_uid_cb.grid(row=3, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (GID)
        self.users_gid_var = tk.IntVar()
        self.users_gid_cb = Common.checkbutton(frame, _tr("GID"), self.users_gid_var, self.on_users_add_remove_checkbuttons_toggled)
        self.users_gid_cb.grid(row=4, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Processes)
        self.users_processes_var = tk.IntVar()
        self.users_processes_cb = Common.checkbutton(frame, _tr("Processes"), self.users_processes_var, self.on_users_add_remove_checkbuttons_toggled)
        self.users_processes_cb.grid(row=5, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Home Directory)
        self.users_home_directory_var = tk.IntVar()
        self.users_home_directory_cb = Common.checkbutton(frame, _tr("Home Directory"), self.users_home_directory_var, self.on_users_add_remove_checkbuttons_toggled)
        self.users_home_directory_cb.grid(row=0, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Group)
        self.users_group_var = tk.IntVar()
        self.users_group_cb = Common.checkbutton(frame, _tr("Group"), self.users_group_var, self.on_users_add_remove_checkbuttons_toggled)
        self.users_group_cb.grid(row=1, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Terminal)
        self.users_terminal_var = tk.IntVar()
        self.users_terminal_cb = Common.checkbutton(frame, _tr("Terminal"), self.users_terminal_var, self.on_users_add_remove_checkbuttons_toggled)
        self.users_terminal_cb.grid(row=2, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Start Time)
        self.users_start_time_var = tk.IntVar()
        self.users_start_time_cb = Common.checkbutton(frame, _tr("Start Time"), self.users_start_time_var, self.on_users_add_remove_checkbuttons_toggled)
        self.users_start_time_cb.grid(row=3, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (CPU)
        self.users_cpu_var = tk.IntVar()
        self.users_cpu_cb = Common.checkbutton(frame, _tr("CPU"), self.users_cpu_var, self.on_users_add_remove_checkbuttons_toggled)
        self.users_cpu_cb.grid(row=4, column=1, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=6, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Button (Reset)
        self.reset_users_settings_button = Common.reset_button(frame)
        self.reset_users_settings_button.grid(row=7, column=0, columnspan=2, padx=0, pady=(0, 10))

        # Connect signals
        self.settings_window.after(1, self.users_settings_set_gui)
        self.reset_users_settings_button.config(command=self.on_users_settings_reset_button_clicked)


    def on_users_settings_reset_button_clicked(self):
        # Load default settings
        Config.config_default_users_func()
        Config.config_save_func()
        # Reset device list between Performance tab sub-tabs because selected device is reset.
        #MainWindow.main_gui_device_selection_list()
        Common.update_tab_and_menu_gui(self.users_settings_set_gui, Users)

    def on_users_add_remove_checkbuttons_toggled(self):

        Config.users_columns_shown = []
        if self.users_user_var.get() == 1:
            Config.users_columns_shown.append("user_name")
        if self.users_full_name_var.get() == 1:
            Config.users_columns_shown.append("full_name")
        if self.users_logged_in_var.get() == 1:
            Config.users_columns_shown.append("logged_in")
        if self.users_uid_var.get() == 1:
            Config.users_columns_shown.append("uid")
        if self.users_gid_var.get() == 1:
            Config.users_columns_shown.append("gid")
        if self.users_processes_var.get() == 1:
            Config.users_columns_shown.append("process_count")
        if self.users_home_directory_var.get() == 1:
            Config.users_columns_shown.append("home_directory")
        if self.users_group_var.get() == 1:
            Config.users_columns_shown.append("group_name")
        if self.users_terminal_var.get() == 1:
            Config.users_columns_shown.append("terminal")
        if self.users_start_time_var.get() == 1:
            Config.users_columns_shown.append("log_in_time")
        if self.users_cpu_var.get() == 1:
            Config.users_columns_shown.append("cpu_usage")

        Common.save_tab_settings(Users)


    def users_settings_set_gui(self):
        if "user_name" in Config.users_columns_shown:
            self.users_user_var.set(1)
        else:
            self.users_user_var.set(0)
        if "full_name" in Config.users_columns_shown:
            self.users_full_name_var.set(1)
        else:
            self.users_full_name_var.set(0)
        if "logged_in" in Config.users_columns_shown:
            self.users_logged_in_var.set(1)
        else:
            self.users_logged_in_var.set(0)
        if "uid" in Config.users_columns_shown:
            self.users_uid_var.set(1)
        else:
            self.users_uid_var.set(0)
        if "gid" in Config.users_columns_shown:
            self.users_gid_var.set(1)
        else:
            self.users_gid_var.set(0)
        if "process_count" in Config.users_columns_shown:
            self.users_processes_var.set(1)
        else:
            self.users_processes_var.set(0)
        if "home_directory" in Config.users_columns_shown:
            self.users_home_directory_var.set(1)
        else:
            self.users_home_directory_var.set(0)
        if "terminal" in Config.users_columns_shown:
            self.users_group_var.set(1)
        else:
            self.users_group_var.set(0)
        if "log_in_time" in Config.users_columns_shown:
            self.users_terminal_var.set(1)
        else:
            self.users_terminal_var.set(0)
        if "cpu_usage" in Config.users_columns_shown:
            self.users_start_time_var.set(1)
        else:
            self.users_start_time_var.set(0)
        if "cpu_usage" in Config.users_columns_shown:
            self.users_cpu_var.set(1)
        else:
            self.users_cpu_var.set(0)


    # ***********************************************************************************************
    #                                           Services
    # ***********************************************************************************************

    def services_settings_tab_gui(self):

        global Services
        from .Services import Services

        # Frame
        frame = ttk.Frame(self.frame_services_tab)
        frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)


        # CheckButton (Name)
        self.services_name_var = tk.IntVar()
        self.services_name_cb = Common.checkbutton(frame, _tr("Name"), self.services_name_var, self.on_services_add_remove_checkbuttons_toggled)
        self.services_name_cb.grid(row=0, column=0, sticky="w", padx=0, pady=0)
        self.services_name_cb.config(state="disabled")

        # CheckButton (Status)
        self.services_status_var = tk.IntVar()
        self.services_status_cb = Common.checkbutton(frame, _tr("Status"), self.services_status_var, self.on_services_add_remove_checkbuttons_toggled)
        self.services_status_cb.grid(row=1, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Main PID)
        self.services_main_pid_var = tk.IntVar()
        self.services_main_pid_cb = Common.checkbutton(frame, _tr("Main PID"), self.services_main_pid_var, self.on_services_add_remove_checkbuttons_toggled)
        self.services_main_pid_cb.grid(row=2, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Active State)
        self.services_active_state_var = tk.IntVar()
        self.services_active_state_cb = Common.checkbutton(frame, _tr("Active State"), self.services_active_state_var, self.on_services_add_remove_checkbuttons_toggled)
        self.services_active_state_cb.grid(row=3, column=0, sticky="w", padx=0, pady=0)

        # CheckButton (Load State)
        self.services_load_state_var = tk.IntVar()
        self.services_load_state_cb = Common.checkbutton(frame, _tr("Load State"), self.services_load_state_var, self.on_services_add_remove_checkbuttons_toggled)
        self.services_load_state_cb.grid(row=0, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Sub State)
        self.sub_state_var = tk.IntVar()
        self.sub_state_cb = Common.checkbutton(frame, _tr("Sub State"), self.sub_state_var, self.on_services_add_remove_checkbuttons_toggled)
        self.sub_state_cb.grid(row=1, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Memory (RSS))
        self.memory_rss_var = tk.IntVar()
        self.memory_rss_cb = Common.checkbutton(frame, _tr("Memory (RSS)"), self.memory_rss_var, self.on_services_add_remove_checkbuttons_toggled)
        self.memory_rss_cb.grid(row=2, column=1, sticky="w", padx=0, pady=0)

        # CheckButton (Description)
        self.description_var = tk.IntVar()
        self.description_cb = Common.checkbutton(frame, _tr("Description"), self.description_var, self.on_services_add_remove_checkbuttons_toggled)
        self.description_cb.grid(row=3, column=1, sticky="w", padx=0, pady=0)

        # Separator
        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=4, column=0, columnspan=2, sticky="ew", padx=0, pady=10)

        # Button (Reset)
        self.reset_services_settings_button = Common.reset_button(frame)
        self.reset_services_settings_button.grid(row=5, column=0, columnspan=2, padx=0, pady=(0, 10))


        # Connect signals
        self.settings_window.after(1, self.services_settings_set_gui)
        self.reset_services_settings_button.config(command=self.on_reset_services_settings_button_clicked)


    def on_reset_services_settings_button_clicked(self):
        # Load default settings
        Config.config_default_services_func()
        Config.config_save_func()
        # Reset device list between Performance tab sub-tabs because selected device is reset.
        #MainWindow.main_gui_device_selection_list()
        Common.update_tab_and_menu_gui(self.services_settings_set_gui, Services)

    def on_services_add_remove_checkbuttons_toggled(self):

        Config.services_columns_shown = []
        if self.services_name_var.get() == 1:
            Config.services_columns_shown.append("service_name")
        if self.services_status_var.get() == 1:
            Config.services_columns_shown.append("unit_file_state")
        if self.services_main_pid_var.get() == 1:
            Config.services_columns_shown.append("main_pid")
        if self.services_active_state_var.get() == 1:
            Config.services_columns_shown.append("active_state")
        if self.services_load_state_var.get() == 1:
            Config.services_columns_shown.append("load_state")
        if self.sub_state_var.get() == 1:
            Config.services_columns_shown.append("sub_state")
        if self.memory_rss_var.get() == 1:
            Config.services_columns_shown.append("memory_current")
        if self.description_var.get() == 1:
            Config.services_columns_shown.append("description")

        Common.save_tab_settings(Services)


    def services_settings_set_gui(self):
        if "service_name" in Config.services_columns_shown:
            self.services_name_var.set(1)
        else:
            self.services_name_var.set(0)
        if "unit_file_state" in Config.services_columns_shown:
            self.services_status_var.set(1)
        else:
            self.services_status_var.set(0)
        if "main_pid" in Config.services_columns_shown:
            self.services_main_pid_var.set(1)
        else:
            self.services_main_pid_var.set(0)
        if "active_state" in Config.services_columns_shown:
            self.services_active_state_var.set(1)
        else:
            self.services_active_state_var.set(0)
        if "load_state" in Config.services_columns_shown:
            self.services_load_state_var.set(1)
        else:
            self.services_load_state_var.set(0)
        if "sub_state" in Config.services_columns_shown:
            self.sub_state_var.set(1)
        else:
            self.sub_state_var.set(0)
        if "memory_current" in Config.services_columns_shown:
            self.memory_rss_var.set(1)
        else:
            self.memory_rss_var.set(0)
        if "description" in Config.services_columns_shown:
            self.description_var.set(1)
        else:
            self.description_var.set(0)


SettingsWindow = SettingsWindow()


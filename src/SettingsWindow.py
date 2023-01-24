import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

import os

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from MainWindow import MainWindow
import Common


class SettingsWindow:

    def __init__(self):

        # Define data lists in order to add them into comboboxes.
        self.language_dict = {"system":_tr("System"), "cs.UTF-8":"Čeština", "de.UTF-8":"Deutsch",
                              "en_US.UTF-8":"English (US)", "es":"Español", "fa.UTF-8":"فارسی",
                              "fr.UTF-8": "Français", "hu.UTF-8":"Magyar", "pl.UTF-8":"Polski",
                              "pt_BR.UTF-8":"Português do Brasil", "pt_PT.UTF-8":"Português europeu",
                              "ru_RU.UTF-8":"Русский", "tr.UTF-8":"Türkçe"}
        self.gui_theme_dict = {"system":_tr("System"), "light":_tr("Light"), "dark":_tr("Dark")}
        self.update_interval_list = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 5.0, 10.0]
        self.chart_data_history_list = [30, 60, 90, 120, 150, 180, 300, 600, 1200]
        self.default_main_tab_list = [_tr("Performance"), _tr("Processes"), _tr("Users"), _tr("Services"), _tr("System")]
        self.performance_tab_default_sub_tab_list = [_tr("Summary"), _tr("CPU"), _tr("Memory"), _tr("Disk"), _tr("Network"), _tr("GPU"), _tr("Sensors")]

        # For translating the text that is used in ".desktop" file.
        _text = [_tr("System Monitor"), _tr("Task Manager")]

        self.window_gui()

        self.messagedialog_gui()

        self.gui_signals()


    def window_gui(self):
        """
        Generate window GUI.
        """

        # Window
        self.settings_window = Gtk.Window()
        self.settings_window.set_title(_tr("General Settings"))
        self.settings_window.set_icon_name("system-monitoring-center")
        self.settings_window.set_resizable(False)
        self.settings_window.set_transient_for(MainWindow.main_window)
        self.settings_window.set_modal(True)
        self.settings_window.set_hide_on_close(True)

        # Grid
        main_grid = Gtk.Grid()
        main_grid.set_hexpand(True)
        main_grid.set_column_spacing(3)
        main_grid.set_row_spacing(3)
        main_grid.set_margin_top(10)
        main_grid.set_margin_bottom(10)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        self.settings_window.set_child(main_grid)

        # Label (Language)
        label = Common.static_information_label_no_ellipsize(_tr("Language (Requires restart)") + ":")
        main_grid.attach(label, 0, 0, 1, 1)
        # DropDown (Language)
        item_list = list(self.language_dict.values())
        self.language_dd = Common.dropdown_and_model(item_list)
        main_grid.attach(self.language_dd, 1, 0, 1, 1)

        # Label (Light/Dark theme)
        label = Common.static_information_label_no_ellipsize(_tr("Light/Dark theme") + ":")
        main_grid.attach(label, 0, 1, 1, 1)
        # DropDown (Light/Dark theme)
        item_list = list(self.gui_theme_dict.values())
        self.light_dark_theme_dd = Common.dropdown_and_model(item_list)
        main_grid.attach(self.light_dark_theme_dd, 1, 1, 1, 1)

        # Separator
        separator = Common.settings_window_separator()
        main_grid.attach(separator, 0, 2, 2, 1)

        # Label (Update interval)
        label = Common.static_information_label_no_ellipsize(_tr("Update interval (seconds)") + ":")
        main_grid.attach(label, 0, 3, 1, 1)
        # DropDown (Update interval)
        item_list = self.update_interval_list
        self.update_interval_dd = Common.dropdown_and_model(item_list)
        main_grid.attach(self.update_interval_dd, 1, 3, 1, 1)

        # Label (Graph data history)
        label = Common.static_information_label_no_ellipsize(_tr("Graph data history") + ":")
        main_grid.attach(label, 0, 4, 1, 1)
        # DropDown (Graph data history)
        item_list = self.chart_data_history_list
        self.graph_data_history_dd = Common.dropdown_and_model(item_list)
        main_grid.attach(self.graph_data_history_dd, 1, 4, 1, 1)

        # Separator
        separator = Common.settings_window_separator()
        main_grid.attach(separator, 0, 5, 2, 1)

        # CheckButton (Show performance summary on headerbar)
        self.show_performance_summary_on_hb_cb = Common.checkbutton(_tr("Show performance summary on the headerbar"), None)
        main_grid.attach(self.show_performance_summary_on_hb_cb, 0, 6, 2, 1)

        # Separator
        separator = Common.settings_window_separator()
        main_grid.attach(separator, 0, 7, 2, 1)

        # CheckButton (Remember last opened tabs"
        self.remember_last_opened_tabs_cb = Common.checkbutton(_tr("Remember last opened tabs"), None)
        main_grid.attach(self.remember_last_opened_tabs_cb, 0, 8, 2, 1)

        # Grid (Default main tab and sub-tab)
        default_main_sub_tab_grid = Gtk.Grid()
        default_main_sub_tab_grid.set_column_spacing(5)
        default_main_sub_tab_grid.set_column_homogeneous(True)
        main_grid.attach(default_main_sub_tab_grid, 0, 9, 2, 1)
        # Label (Default main tab and sub-tab)
        label = Common.static_information_label_no_ellipsize(_tr("Default main tab and sub-tab") + ":")
        default_main_sub_tab_grid.attach(label, 0, 0, 2, 1)
        # DropDown (Default main tab)
        item_list = self.default_main_tab_list
        self.default_main_tab_dd = Common.dropdown_and_model(item_list)
        default_main_sub_tab_grid.attach(self.default_main_tab_dd, 0, 1, 1, 1)
        # DropDown (Default sub-tab)
        item_list = self.performance_tab_default_sub_tab_list
        self.default_sub_tab_dd = Common.dropdown_and_model(item_list)
        default_main_sub_tab_grid.attach(self.default_sub_tab_dd, 1, 1, 1, 1)

        # Separator
        separator = Common.settings_window_separator()
        main_grid.attach(separator, 0, 10, 2, 1)

        # CheckButton (Remember last selected devices)
        self.remember_last_selected_devices_cb = Common.checkbutton(_tr("Remember last selected devices"), None)
        main_grid.attach(self.remember_last_selected_devices_cb, 0, 11, 2, 1)

        # Separator
        separator = Common.settings_window_separator()
        main_grid.attach(separator, 0, 12, 2, 1)

        # CheckButton (Remember window size)
        self.remember_window_size_cb = Common.checkbutton(_tr("Remember window size"), None)
        main_grid.attach(self.remember_window_size_cb, 0, 13, 2, 1)

        # Separator
        separator = Common.settings_window_separator()
        main_grid.attach(separator, 0, 14, 2, 1)

        # Grid (Check for updates)
        self.check_for_updates_grid = Gtk.Grid()
        main_grid.attach(self.check_for_updates_grid, 0, 15, 2, 1)
        # CheckButton (Check for updates)
        self.check_for_updates_cb = Common.checkbutton(_tr("Check for updates automatically (PyPI only)"), None)
        self.check_for_updates_grid.attach(self.check_for_updates_cb, 0, 0, 1, 1)
        # Label (Check for updates)
        label = Common.static_information_label_no_ellipsize(_tr("(If the application is run without root privileges)"))
        self.check_for_updates_grid.attach(label, 0, 1, 1, 1)
        # Separator (Check for updates)
        separator = Common.settings_window_separator()
        self.check_for_updates_grid.attach(separator, 0, 16, 2, 1)

        # Button (Reset)
        self.reset_button = Common.reset_button()
        main_grid.attach(self.reset_button, 0, 17, 2, 1)

        # Separator
        separator = Common.settings_window_separator()
        main_grid.attach(separator, 0, 18, 2, 1)

        # Button (Reset all settings of the application)
        self.reset_all_settings_button = Gtk.Button()
        self.reset_all_settings_button.set_halign(Gtk.Align.CENTER)
        self.reset_all_settings_button.set_label(_tr("Reset all settings of the application"))
        self.reset_all_settings_button.add_css_class("destructive-action")
        main_grid.attach(self.reset_all_settings_button, 0, 19, 2, 1)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # Window signals
        self.settings_window.connect("show", self.on_settings_window_show)

        # Button signals
        self.reset_button.connect("clicked", self.on_reset_button_clicked)
        self.reset_all_settings_button.connect("clicked", self.on_reset_all_settings_button_clicked)


    def settings_connect_signals_func(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.language_dd.connect("notify::selected-item", self.on_selected_item_notify)
        self.light_dark_theme_dd.connect("notify::selected-item", self.on_selected_item_notify)
        self.update_interval_dd.connect("notify::selected-item", self.on_selected_item_notify)
        self.graph_data_history_dd.connect("notify::selected-item", self.on_selected_item_notify)
        self.show_performance_summary_on_hb_cb.connect("toggled", self.on_show_performance_summary_on_hb_cb_toggled)
        self.remember_last_opened_tabs_cb.connect("toggled", self.on_remember_last_opened_tabs_cb_toggled)
        self.default_main_tab_dd.connect("notify::selected-item", self.on_selected_item_notify)
        self.default_sub_tab_dd.connect("notify::selected-item", self.on_selected_item_notify)
        self.remember_last_selected_devices_cb.connect("toggled", self.on_remember_last_selected_devices_cb_toggled)
        self.remember_window_size_cb.connect("toggled", self.on_remember_window_size_cb_toggled)
        self.check_for_updates_cb.connect("toggled", self.on_check_for_updates_cb_toggled)


    def settings_disconnect_signals_func(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.language_dd.disconnect_by_func(self.on_selected_item_notify)
        self.light_dark_theme_dd.disconnect_by_func(self.on_selected_item_notify)
        self.update_interval_dd.disconnect_by_func(self.on_selected_item_notify)
        self.graph_data_history_dd.disconnect_by_func(self.on_selected_item_notify)
        self.show_performance_summary_on_hb_cb.disconnect_by_func(self.on_show_performance_summary_on_hb_cb_toggled)
        self.remember_last_opened_tabs_cb.disconnect_by_func(self.on_remember_last_opened_tabs_cb_toggled)
        self.default_main_tab_dd.disconnect_by_func(self.on_selected_item_notify)
        self.default_sub_tab_dd.disconnect_by_func(self.on_selected_item_notify)
        self.remember_last_selected_devices_cb.disconnect_by_func(self.on_remember_last_selected_devices_cb_toggled)
        self.remember_window_size_cb.disconnect_by_func(self.on_remember_window_size_cb_toggled)
        self.check_for_updates_cb.disconnect_by_func(self.on_check_for_updates_cb_toggled)


    def on_settings_window_show(self, widget):
        """
        Run code after window is shown.
        """

        # Hide "Check for updates" setting if the application is not installed as Python package.
        if Config.environment_type != "python_package":
            self.check_for_updates_grid.hide()

        # Set GUI widgets for showing current preferences of settings.
        try:
            self.settings_disconnect_signals_func()
        except TypeError:
            pass
        self.set_gui()
        self.settings_connect_signals_func()


    def on_show_performance_summary_on_hb_cb_toggled(self, widget):
        """
        Show/Hide performance summary on the window title.
        """

        # Add performance summary to the main window headerbar if preferred.
        if widget.get_active() == True:
            Config.performance_summary_on_the_headerbar = 1
            MainWindow.window_headerbar.pack_start(MainWindow.performance_summary_hb_grid)

        # Remove performance summary from the main window headerbar if preferred.
        if widget.get_active() == False:
            Config.performance_summary_on_the_headerbar = 0
            MainWindow.window_headerbar.remove(MainWindow.performance_summary_hb_grid)

        Config.config_save_func()


    def on_remember_last_opened_tabs_cb_toggled(self, widget):
        """
        Enable/Disable remembering last opened main tab and sub-tab.
        """

        # Get currently opened tabs and save them if preferred.
        if widget.get_active() == True:
            Config.remember_last_opened_tabs_on_application_start = 1
            self.default_main_tab_dd.set_sensitive(False)
            self.default_sub_tab_dd.set_sensitive(False)
            self.settings_gui_default_tab_func()

        # Set setting for not remembering las opened tabs if preferred.
        if widget.get_active() == False:
            Config.remember_last_opened_tabs_on_application_start = 0
            self.default_main_tab_dd.set_sensitive(True)
            self.default_sub_tab_dd.set_sensitive(True)

        Config.config_save_func()


    def on_selected_item_notify(self, widget, parameter):
        """
        Change update interval of the application, number of graph data points for graphs, default main tab and default sub-tab.
        Notify signal is sent when DropDown widget selection is changed.
        Currently GtkExpression parameter for DropDown can not be used because of PyGObject.
        """

        if widget == self.language_dd:
            Config.language = list(self.language_dict.keys())[widget.get_selected()]

        if widget == self.light_dark_theme_dd:
            Config.light_dark_theme = list(self.gui_theme_dict.keys())[widget.get_selected()]

        if widget == self.update_interval_dd:
            Config.update_interval = self.update_interval_list[widget.get_selected()]

        if widget == self.graph_data_history_dd:
            Config.chart_data_history = self.chart_data_history_list[widget.get_selected()]

        if widget == self.default_main_tab_dd:
            Config.default_main_tab = widget.get_selected()

        if widget == self.default_sub_tab_dd:
            Config.performance_tab_default_sub_tab = widget.get_selected()

        Config.config_save_func()

        if widget == self.light_dark_theme_dd:
            MainWindow.light_dark_theme()

        if widget == self.update_interval_dd:
            self.settings_gui_apply_settings_immediately_func()

        if widget == self.graph_data_history_dd:
            self.settings_gui_set_chart_data_history_func()
            self.settings_gui_apply_settings_immediately_func()


    def on_remember_last_selected_devices_cb_toggled(self, widget):
        """
        Enable/Disable remembering last selected devices.
        """

        if widget.get_active() == True:
            Config.remember_last_selected_hardware = 1

        if widget.get_active() == False:
            Config.remember_last_selected_hardware = 0

        Config.config_save_func()


    def on_remember_window_size_cb_toggled(self, widget):
        """
        Enable/Disable remembering window size.
        """

        # Get window state (if full screen or not), window size (width, height) and save if preferred.
        if widget.get_active() == True:
            remember_window_size_value = 1
            main_window_state = MainWindow.main_window.is_maximized()
            if main_window_state == True:
                main_window_state = 1
            if main_window_state == False:
                main_window_state = 0
            main_window_width = MainWindow.main_window.get_width()
            main_window_height = MainWindow.main_window.get_height()
            Config.remember_window_size = [remember_window_size_value, main_window_state, main_window_width, main_window_height]

        # Reset window size/state settings if preferred.
        if widget.get_active() == False:
            remember_window_size_value = 0
            main_window_state = 0
            main_window_width = MainWindow.main_window.get_width()
            main_window_height = MainWindow.main_window.get_height()
            Config.remember_window_size = [remember_window_size_value, main_window_state, main_window_width, main_window_height]

        Config.config_save_func()


    def on_check_for_updates_cb_toggled(self, widget):
        """
        Enable/Disable checking updates.
        """

        if widget.get_active() == True:
            Config.check_for_updates_automatically = 1

        if widget.get_active() == False:
            Config.check_for_updates_automatically = 0

        Config.config_save_func()


    def on_reset_button_clicked(self, widget):
        """
        Reset settings on the "Settings" window.
        """

        Config.config_default_general_general_func()
        Config.config_save_func()
        # Set GUI objects of the Settings window without disconnecting signals
        # of the widgets in order to use these signals to reset the settings.
        self.set_gui()

        # Length of performance data lists (cpu_usage_percent_ave, ram_usage_percent_ave, ...)
        # have to be set after "chart_data_history" setting is reset in order to avoid errors.
        self.settings_gui_set_chart_data_history_func()

        # Apply selected CPU core, disk, network card changes
        Performance.performance_set_selected_cpu_core_func()
        Performance.performance_set_selected_disk_func()
        Performance.performance_set_selected_network_card_func()
        # Apply selected GPU changes
        try:
            from MainWindow import Gpu
            Gpu.gpu_set_selected_gpu_func()
        # Prevent errors because "gpu_get_gpu_list_and_set_selected_gpu_func" module requires
        # some modules in the Gpu module. They are imported if Gpu tab is switched on.
        except ImportError:
            pass

        # Apply changes immediately (without waiting update interval).
        self.settings_gui_apply_settings_immediately_func()


    def on_reset_all_settings_button_clicked(self, widget):
        """
        Reset all settings of the application.
        """

        self.messagedialog.present()


    def on_messagedialog_response(self, widget, response):
        """
        Reset all settings of the application if "YES" button is clicked.
        """

        if response == Gtk.ResponseType.YES:
            self.reset_all_settings_func()

        self.messagedialog.hide()


    def reset_all_settings_func(self):
        """
        Function for resetting all settings of the application.
        """

        Config.config_default_reset_all_func()
        Config.config_save_func()
        self.settings_disconnect_signals_func()
        self.set_gui()
        self.settings_connect_signals_func()

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
            from MainWindow import Gpu
            Gpu.gpu_set_selected_gpu_func()
        # Prevent errors because "gpu_get_gpu_list_and_set_selected_gpu_func" module requires
        # some modules in the Gpu module. They are imported if Gpu tab is switched on.
        except ImportError:
            pass

        # Reset selected device on the list between Performance tab sub-tab list.
        if Config.performance_tab_current_sub_tab != -1:
            MainWindow.main_gui_device_selection_list()

        # Apply changes immediately (without waiting update interval).
        self.settings_gui_apply_settings_immediately_func()


    def set_gui(self):
        """
        Set GUI objects.
        """

        self.language_dd.set_selected(list(self.language_dict.keys()).index(Config.language))
        self.light_dark_theme_dd.set_selected(list(self.gui_theme_dict.keys()).index(Config.light_dark_theme))
        self.update_interval_dd.set_selected(self.update_interval_list.index(Config.update_interval))
        self.graph_data_history_dd.set_selected(self.chart_data_history_list.index(Config.chart_data_history))

        # Set GUI preferences for "show performance summary on the headerbar" setting
        if Config.performance_summary_on_the_headerbar == 1:
            self.show_performance_summary_on_hb_cb.set_active(True)
        if Config.performance_summary_on_the_headerbar == 0:
            self.show_performance_summary_on_hb_cb.set_active(False)

        # Set GUI preferences for "remember last opened tabs" setting
        if Config.remember_last_opened_tabs_on_application_start == 1:
            self.remember_last_opened_tabs_cb.set_active(True)
        if Config.remember_last_opened_tabs_on_application_start == 0:
            self.remember_last_opened_tabs_cb.set_active(False)

        # Set GUI preferences for "defult main tab" setting
        self.default_main_tab_dd.set_selected(Config.default_main_tab)
        if Config.remember_last_opened_tabs_on_application_start == 1:
            self.default_main_tab_dd.set_sensitive(False)
        if Config.remember_last_opened_tabs_on_application_start == 0:
            self.default_main_tab_dd.set_sensitive(True)

        # Set GUI preferences for "performance tab default sub-tab" setting
        self.default_sub_tab_dd.set_selected(Config.performance_tab_default_sub_tab)
        if Config.remember_last_opened_tabs_on_application_start == 1:
            self.default_sub_tab_dd.set_sensitive(False)
        if Config.remember_last_opened_tabs_on_application_start == 0:
            self.default_sub_tab_dd.set_sensitive(True)

        # Set GUI preferences for "remember last selected hardware" setting
        if Config.remember_last_selected_hardware == 1:
            self.remember_last_selected_devices_cb.set_active(True)
        if Config.remember_last_selected_hardware == 0:
            self.remember_last_selected_devices_cb.set_active(False)

        # Set GUI preferences for "remember window size" setting
        if Config.remember_window_size[0] == 1:
            self.remember_window_size_cb.set_active(True)
        if Config.remember_window_size[0] == 0:
            self.remember_window_size_cb.set_active(False)

        # Set GUI preferences for "check for updates automatically" setting
        if Config.check_for_updates_automatically == 1:
            self.check_for_updates_cb.set_active(True)
        if Config.check_for_updates_automatically == 0:
            self.check_for_updates_cb.set_active(False)


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

            # "cpu_usage_percent_ave" list
            Performance.cpu_usage_percent_ave = Performance.cpu_usage_percent_ave[length_difference:]

            # "cpu_usage_percent_per_core" list
            for device in Performance.logical_core_list:
                Performance.cpu_usage_percent_per_core[device] = Performance.cpu_usage_percent_per_core[device][length_difference:]

            # "ram_usage_percent" and "swap_usage_percent" lists
            Performance.ram_usage_percent = Performance.ram_usage_percent[length_difference:]
            Performance.swap_usage_percent = Performance.swap_usage_percent[length_difference:]

            # "disk_read_speed" and "disk_write_speed" lists
            for device in Performance.disk_list:
                Performance.disk_read_speed[device] = Performance.disk_read_speed[device][length_difference:]
                Performance.disk_write_speed[device] = Performance.disk_write_speed[device][length_difference:]

            # "network_receive_speed" and "network_send_speed" lists
            for device in Performance.network_card_list:
                Performance.network_receive_speed[device] = Performance.network_receive_speed[device][length_difference:]
                Performance.network_send_speed[device] = Performance.network_send_speed[device][length_difference:]

            # "gpu_load_list" list
            if MainWindow.gpu_tb.get_active() == True:
                from Gpu import Gpu
                Gpu.gpu_load_list = Gpu.gpu_load_list[length_difference:]

        # Add list of zeroes to the beginning part of the lists if new "chart_data_history" value is bigger than the old value.
        if chart_data_history_current < chart_data_history_new:

            # Generate list of zeroes for adding to the beginning of te lists.
            list_to_add = [0] * (chart_data_history_new - chart_data_history_current)

            # "cpu_usage_percent_ave" list
            Performance.cpu_usage_percent_ave = list_to_add + Performance.cpu_usage_percent_ave

            # "cpu_usage_percent_per_core" list
            for device in Performance.logical_core_list:
                Performance.cpu_usage_percent_per_core[device] = list_to_add + Performance.cpu_usage_percent_per_core[device]

            # "ram_usage_percent" and "swap_usage_percent" lists
            Performance.ram_usage_percent = list_to_add + Performance.ram_usage_percent
            Performance.swap_usage_percent = list_to_add + Performance.swap_usage_percent

            # "disk_read_speed" and "disk_write_speed" lists
            for device in Performance.disk_list:
                Performance.disk_read_speed[device] = list_to_add + Performance.disk_read_speed[device]
                Performance.disk_write_speed[device] = list_to_add + Performance.disk_write_speed[device]

            # "network_receive_speed" and "network_send_speed" lists
            for device in Performance.network_card_list:
                Performance.network_receive_speed[device] = list_to_add + Performance.network_receive_speed[device]
                Performance.network_send_speed[device] = list_to_add + Performance.network_send_speed[device]

            # "gpu_load_list" list
            if MainWindow.gpu_tb.get_active() == True:
                from Gpu import Gpu
                Gpu.gpu_load_list = list_to_add + Gpu.gpu_load_list


    def settings_gui_apply_settings_immediately_func(self):
        """
        Apply settings for all opened tabs (since application start) without waiting update interval.
        If "initial_already_run" variable is set as "0", initial and loop functions of the relevant
        tab will be run in the next main loop if the tab is already opened or these functionswill be run
        immediately when the relevant tab is switched on even if it is opened before the reset.
        """

        try:
            from MainWindow import Summary
            Summary.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainWindow import Cpu
            Cpu.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainWindow import Memory
            Memory.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainWindow import Disk
            Disk.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainWindow import Network
            Network.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainWindow import Gpu
            Gpu.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainWindow import Sensors
            Sensors.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainWindow import Processes
            Processes.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainWindow import Users
            Users.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainWindow import Services
            Services.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainWindow import System
            System.initial_already_run = 0
        except ImportError:
            pass

        MainWindow.main_gui_tab_loop()


    def settings_gui_default_tab_func(self):
        """
        Save default main tab and performace tab sub-tab when "Remember last opened tabs" option is enabled.
        """

        if MainWindow.performance_tb.get_active() == True:
            Config.default_main_tab = 0
        elif MainWindow.processes_tb.get_active() == True:
            Config.default_main_tab = 1
        elif MainWindow.users_tb.get_active() == True:
            Config.default_main_tab = 2
        elif MainWindow.services_tb.get_active() == True:
            Config.default_main_tab = 3
        elif MainWindow.system_tb.get_active() == True:
            Config.default_main_tab = 4

        if MainWindow.summary_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 0
        elif MainWindow.cpu_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 1
        elif MainWindow.memory_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 2
        elif MainWindow.disk_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 3
        elif MainWindow.network_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 4
        elif MainWindow.gpu_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 5
        elif MainWindow.sensors_tb.get_active() == True:
            Config.performance_tab_default_sub_tab = 6


    def messagedialog_gui(self):
        """
        Generate messagedialog GUI.
        """

        self.messagedialog = Gtk.MessageDialog(transient_for=self.settings_window,
                                               modal=True,
                                               title="",
                                               message_type=Gtk.MessageType.WARNING,
                                               buttons=Gtk.ButtonsType.YES_NO,
                                               text=_tr("Do you want to reset all settings to defaults?"),
                                               secondary_text=""
                                               )

        self.messagedialog.connect("response", self.on_messagedialog_response)


SettingsWindow = SettingsWindow()


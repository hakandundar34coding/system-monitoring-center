#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import os

from locale import gettext as _tr

from Config import Config
from Performance import Performance
from MainWindow import MainWindow


class SettingsWindow:

    def __init__(self):

        # Define data lists in order to add them into comboboxes.
        self.language_dict = {"system":_tr("System"), "cs.UTF-8":"čeština", "de.UTF-8":"Deutsch", "en_US.UTF-8":"English (US)", "fa.UTF-8":"فارسی", "hu.UTF-8":"Magyar", "pl.UTF-8":"polski", "pt_BR.UTF-8":"português do Brasil", "pt_PT.UTF-8":"português europeu", "ru_RU.UTF-8":"Русский", "tr.UTF-8":"Türkçe", "zh_CN.UTF-8":"汉语"}
        self.gui_theme_dict = {"system":_tr("System"), "light":_tr("Light"), "dark":_tr("Dark")}
        self.update_interval_list = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 5.0, 10.0]
        self.chart_data_history_list = [30, 60, 90, 120, 150, 180, 300, 600, 1200]
        self.default_main_tab_list = [_tr("Performance"), _tr("Processes"), _tr("Users"), _tr("Services"), _tr("System")]
        self.performance_tab_default_sub_tab_list = [_tr("Summary"), _tr("CPU"), _tr("Memory"), _tr("Disk"), _tr("Network"), _tr("GPU"), _tr("Sensors")]

        # Window GUI
        self.window_gui()

        # MessageDialog
        self.messagedialog_gui()

        # GUI signals
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

        # Label "Language"
        language_label = Gtk.Label()
        language_label.set_halign(Gtk.Align.START)
        language_label.set_label(_tr("Language (Requires restart)") + ":")
        main_grid.attach(language_label, 0, 0, 1, 1)

        # ComboBox "Language"
        self.language_cmb = Gtk.ComboBox()
        main_grid.attach(self.language_cmb, 1, 0, 1, 1)

        # Label "Light/Dark theme"
        language_label = Gtk.Label()
        language_label.set_halign(Gtk.Align.START)
        language_label.set_label(_tr("Light/Dark theme") + ":")
        main_grid.attach(language_label, 0, 1, 1, 1)

        # ComboBox "Light/Dark theme"
        self.light_dark_theme_cmb = Gtk.ComboBox()
        main_grid.attach(self.light_dark_theme_cmb, 1, 1, 1, 1)

        # Separator
        separator = Gtk.Separator()
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        main_grid.attach(separator, 0, 2, 2, 1)

        # Label "Update interval"
        update_interval_label = Gtk.Label()
        update_interval_label.set_halign(Gtk.Align.START)
        update_interval_label.set_label(_tr("Update interval (seconds)") + ":")
        main_grid.attach(update_interval_label, 0, 3, 1, 1)

        # ComboBox "Update interval"
        self.update_interval_cmb = Gtk.ComboBox()
        main_grid.attach(self.update_interval_cmb, 1, 3, 1, 1)

        # Label "Graph data history"
        graph_data_history_label = Gtk.Label()
        graph_data_history_label.set_halign(Gtk.Align.START)
        graph_data_history_label.set_label(_tr("Graph data history") + ":")
        main_grid.attach(graph_data_history_label, 0, 4, 1, 1)

        # ComboBox "Graph data history"
        self.graph_data_history_cmb = Gtk.ComboBox()
        main_grid.attach(self.graph_data_history_cmb, 1, 4, 1, 1)

        # Separator
        separator = Gtk.Separator()
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        main_grid.attach(separator, 0, 5, 2, 1)

        # CheckButton "Show performance summary on headerbar"
        self.show_performance_summary_on_hb_cb = Gtk.CheckButton()
        self.show_performance_summary_on_hb_cb.set_halign(Gtk.Align.START)
        self.show_performance_summary_on_hb_cb.set_label(_tr("Show performance summary on the headerbar"))
        main_grid.attach(self.show_performance_summary_on_hb_cb, 0, 6, 2, 1)

        # Separator
        separator = Gtk.Separator()
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        main_grid.attach(separator, 0, 7, 2, 1)

        # CheckButton "Remember last opened tabs"
        self.remember_last_opened_tabs_cb = Gtk.CheckButton()
        self.remember_last_opened_tabs_cb.set_halign(Gtk.Align.START)
        self.remember_last_opened_tabs_cb.set_label(_tr("Remember last opened tabs"))
        main_grid.attach(self.remember_last_opened_tabs_cb, 0, 8, 2, 1)

        # Grid "Default main tab and sub-tab"
        default_main_sub_tab_grid = Gtk.Grid()
        default_main_sub_tab_grid.set_column_spacing(5)
        default_main_sub_tab_grid.set_column_homogeneous(True)
        main_grid.attach(default_main_sub_tab_grid, 0, 9, 2, 1)

        # Label "Default main tab and sub-tab"
        default_main_sub_tab_label = Gtk.Label()
        default_main_sub_tab_label.set_halign(Gtk.Align.START)
        default_main_sub_tab_label.set_label(_tr("Default main tab and sub-tab") + ":")
        default_main_sub_tab_grid.attach(default_main_sub_tab_label, 0, 0, 2, 1)

        # ComboBox "Default main tab"
        self.default_main_tab_cmb = Gtk.ComboBox()
        default_main_sub_tab_grid.attach(self.default_main_tab_cmb, 0, 1, 1, 1)

        # ComboBox "Default sub-tab"
        self.default_sub_tab_cmb = Gtk.ComboBox()
        default_main_sub_tab_grid.attach(self.default_sub_tab_cmb, 1, 1, 1, 1)

        # Separator
        separator = Gtk.Separator()
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        main_grid.attach(separator, 0, 10, 2, 1)

        # CheckButton "Remember last selected devices"
        self.remember_last_selected_devices_cb = Gtk.CheckButton()
        self.remember_last_selected_devices_cb.set_halign(Gtk.Align.START)
        self.remember_last_selected_devices_cb.set_label(_tr("Remember last selected devices"))
        main_grid.attach(self.remember_last_selected_devices_cb, 0, 11, 2, 1)

        # Separator
        separator = Gtk.Separator()
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        main_grid.attach(separator, 0, 12, 2, 1)

        # CheckButton "Remember window size"
        self.remember_window_size_cb = Gtk.CheckButton()
        self.remember_window_size_cb.set_halign(Gtk.Align.START)
        self.remember_window_size_cb.set_label(_tr("Remember window size"))
        main_grid.attach(self.remember_window_size_cb, 0, 13, 2, 1)

        # Separator
        separator = Gtk.Separator()
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        main_grid.attach(separator, 0, 14, 2, 1)

        # Grid "Check for updates"
        self.check_for_updates_grid = Gtk.Grid()
        main_grid.attach(self.check_for_updates_grid, 0, 15, 2, 1)

        # CheckButton "Check for updates"
        self.check_for_updates_cb = Gtk.CheckButton()
        self.check_for_updates_cb.set_halign(Gtk.Align.START)
        self.check_for_updates_cb.set_label(_tr("Check for updates automatically (PyPI only)"))
        self.check_for_updates_grid.attach(self.check_for_updates_cb, 0, 0, 1, 1)

        # Label "Check for updates"
        check_for_updates_label = Gtk.Label()
        check_for_updates_label.set_halign(Gtk.Align.START)
        check_for_updates_label.set_label(_tr("(If the application is run without root privileges.)"))
        self.check_for_updates_grid.attach(check_for_updates_label, 0, 1, 1, 1)

        # Separator "Check for updates"
        separator = Gtk.Separator()
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        self.check_for_updates_grid.attach(separator, 0, 16, 2, 1)

        # Button "Reset"
        self.reset_button = Gtk.Button()
        self.reset_button.set_halign(Gtk.Align.CENTER)
        self.reset_button.set_label(_tr("Reset"))
        main_grid.attach(self.reset_button, 0, 17, 2, 1)

        # Separator
        separator = Gtk.Separator()
        separator.set_margin_top(5)
        separator.set_margin_bottom(5)
        main_grid.attach(separator, 0, 18, 2, 1)

        # Button "Reset all settings of the application to defaults"
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
        self.settings_window.connect("close-request", self.on_settings_window_close_request)
        self.settings_window.connect("show", self.on_settings_window_show)

        # Button signals
        self.reset_button.connect("clicked", self.on_reset_button_clicked)
        self.reset_all_settings_button.connect("clicked", self.on_reset_all_settings_button_clicked)


    def settings_connect_signals_func(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.language_cmb.connect("changed", self.on_language_cmb_changed)
        self.light_dark_theme_cmb.connect("changed", self.on_light_dark_theme_cmb_changed)
        self.update_interval_cmb.connect("changed", self.on_update_interval_cmb_changed)
        self.graph_data_history_cmb.connect("changed", self.on_graph_data_history_cmb_changed)
        self.show_performance_summary_on_hb_cb.connect("toggled", self.on_show_performance_summary_on_hb_cb_toggled)
        self.remember_last_opened_tabs_cb.connect("toggled", self.on_remember_last_opened_tabs_cb_toggled)
        self.default_main_tab_cmb.connect("changed", self.on_default_main_tab_cmb_changed)
        self.default_sub_tab_cmb.connect("changed", self.on_default_sub_tab_cmb_changed)
        self.remember_last_selected_devices_cb.connect("toggled", self.on_remember_last_selected_devices_cb_toggled)
        self.remember_window_size_cb.connect("toggled", self.on_remember_window_size_cb_toggled)
        self.check_for_updates_cb.connect("toggled", self.on_check_for_updates_cb_toggled)


    def settings_disconnect_signals_func(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.language_cmb.disconnect_by_func(self.on_language_cmb_changed)
        self.light_dark_theme_cmb.disconnect_by_func(self.on_light_dark_theme_cmb_changed)
        self.update_interval_cmb.disconnect_by_func(self.on_update_interval_cmb_changed)
        self.graph_data_history_cmb.disconnect_by_func(self.on_graph_data_history_cmb_changed)
        self.show_performance_summary_on_hb_cb.disconnect_by_func(self.on_show_performance_summary_on_hb_cb_toggled)
        self.remember_last_opened_tabs_cb.disconnect_by_func(self.on_remember_last_opened_tabs_cb_toggled)
        self.default_main_tab_cmb.disconnect_by_func(self.on_default_main_tab_cmb_changed)
        self.default_sub_tab_cmb.disconnect_by_func(self.on_default_sub_tab_cmb_changed)
        self.remember_last_selected_devices_cb.disconnect_by_func(self.on_remember_last_selected_devices_cb_toggled)
        self.remember_window_size_cb.disconnect_by_func(self.on_remember_window_size_cb_toggled)
        self.check_for_updates_cb.disconnect_by_func(self.on_check_for_updates_cb_toggled)


    def on_settings_window_close_request(self, widget):
        """
        Called when window close button (X) is clicked.
        """

        self.settings_window.hide()
        return True


    def on_settings_window_show(self, widget):
        """
        Run code after window is shown.
        """

        # Get current directory (which code of this application is in) and current user home directory (symlinks will be generated in).
        current_dir = os.path.dirname(os.path.realpath(__file__))
        current_user_homedir = os.environ.get('HOME')

        # Check if the application is a Python package and hide "update check setting widgets" if it is not a Python package.
        if current_dir.startswith("/usr/local/lib/") == False and current_dir.startswith(current_user_homedir + "/.local/lib/") == False:
            self.check_for_updates_grid.hide()

        # Set GUI widgets for showing current preferences of settings.
        try:
            self.settings_disconnect_signals_func()
        except TypeError:
            pass
        self.set_gui()
        self.settings_connect_signals_func()


    def on_language_cmb_changed(self, widget):
        """
        Set GUI language. This setting is applied after the application is restarted.
        """

        Config.language = list(self.language_dict.keys())[widget.get_active()]
        Config.config_save_func()


    def on_light_dark_theme_cmb_changed(self, widget):
        """
        Set light/dark theme for GUI.
        """

        light_dark_theme = list(self.gui_theme_dict.keys())[widget.get_active()]
        Config.light_dark_theme = light_dark_theme

        if light_dark_theme == "system":
            Gtk.Settings.get_default().reset_property("gtk-application-prefer-dark-theme")
        elif light_dark_theme == "light":
            Gtk.Settings.get_default().props.gtk_application_prefer_dark_theme = False
        elif light_dark_theme == "dark":
            Gtk.Settings.get_default().props.gtk_application_prefer_dark_theme = True

        Config.config_save_func()


    def on_update_interval_cmb_changed(self, widget):
        """
        Set update interval of the application.
        """

        Config.update_interval = self.update_interval_list[widget.get_active()]

        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
        self.settings_gui_apply_settings_immediately_func()


    def on_graph_data_history_cmb_changed(self, widget):
        """
        Set number of graph data points for graphs.
        """

        Config.chart_data_history = self.chart_data_history_list[widget.get_active()]

        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
        self.settings_gui_set_chart_data_history_func()
        self.settings_gui_apply_settings_immediately_func()


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
            self.combobox2003.set_sensitive(False)
            self.combobox2004.set_sensitive(False)
            self.settings_gui_default_tab_func()

        # Set setting for not remembering las opened tabs if preferred.
        if widget.get_active() == False:
            Config.remember_last_opened_tabs_on_application_start = 0
            self.combobox2003.set_sensitive(True)
            self.combobox2004.set_sensitive(True)

        Config.config_save_func()


    def on_default_main_tab_cmb_changed(self, widget):
        """
        Set default main tab.
        """

        # Get selected tab as default main tab and save it if preferred.
        Config.default_main_tab = widget.get_active()
        Config.config_save_func()


    def on_default_sub_tab_cmb_changed(self, widget):
        """
        Set default sub-tab.
        """

        # Get selected tab as Performance tab default sub-tab and save it if preferred.
        Config.performance_tab_default_sub_tab = widget.get_active()
        Config.config_save_func()


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
        # Set "General" tab of the Settings window without disconnecting signals of the widgets in order to use these signals to reset the settings.
        self.set_gui()

        # Length of performance data lists (cpu_usage_percent_ave, ram_usage_percent_ave, ...) have to be set after "chart_data_history" setting is reset in order to avoid errors.
        self.settings_gui_set_chart_data_history_func()

        # Apply selected CPU core, disk, network card changes
        Performance.performance_set_selected_cpu_core_func()
        Performance.performance_set_selected_disk_func()
        Performance.performance_set_selected_network_card_func()
        # Apply selected GPU changes
        try:
            from MainWindow import Gpu
            Gpu.gpu_set_selected_gpu_func()
        # "try-except" is used in order to avoid errors because "gpu_get_gpu_list_and_set_selected_gpu_func" module requires some modules in the Gpu module they are imported if Gpu tab is switched on.
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
        self.on_light_dark_theme_cmb_changed(self.light_dark_theme_cmb)

        # Length of performance data lists (cpu_usage_percent_ave, ram_usage_percent_ave, ...) have to be set after "chart_data_history" setting is reset in order to avoid errors.
        self.settings_gui_set_chart_data_history_func()

        # Apply selected CPU core, disk, network card changes
        Performance.performance_set_selected_cpu_core_func()
        Performance.performance_set_selected_disk_func()
        Performance.performance_set_selected_network_card_func()
        # Apply selected GPU changes
        try:
            from MainWindow import Gpu
            Gpu.gpu_set_selected_gpu_func()
        # "try-except" is used in order to avoid errors because "gpu_get_gpu_list_and_set_selected_gpu_func" module requires some modules in the Gpu module they are imported if Gpu tab is switched on.
        except ImportError:
            pass

        # Reset selected device on the list between Performance tab sub-tab list.
        MainWindow.main_gui_device_selection_list()

        # Apply changes immediately (without waiting update interval).
        self.settings_gui_apply_settings_immediately_func()


    def set_gui(self):
        """
        Set GUI items.
        """

        # Set GUI preferences for "language" setting
        language_ls = Gtk.ListStore()
        language_ls.set_column_types([str])
        self.language_cmb.set_model(language_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.language_cmb.clear()
        renderer_text = Gtk.CellRendererText()
        self.language_cmb.pack_start(renderer_text, True)
        self.language_cmb.add_attribute(renderer_text, "text", 0)
        for value in self.language_dict:
            value = self.language_dict[value]
            language_ls.append([value])
        self.language_cmb.set_active(list(self.language_dict.keys()).index(Config.language))

        # Set GUI preferences for "Light/Dark theme" setting
        light_dark_theme_ls = Gtk.ListStore()
        light_dark_theme_ls.set_column_types([str])
        self.light_dark_theme_cmb.set_model(light_dark_theme_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.light_dark_theme_cmb.clear()
        renderer_text = Gtk.CellRendererText()
        self.light_dark_theme_cmb.pack_start(renderer_text, True)
        self.light_dark_theme_cmb.add_attribute(renderer_text, "text", 0)
        for value in self.gui_theme_dict:
            value = self.gui_theme_dict[value]
            light_dark_theme_ls.append([value])
        self.light_dark_theme_cmb.set_active(list(self.gui_theme_dict.keys()).index(Config.light_dark_theme))

        # Set GUI preferences for "update interval" setting
        update_interval_ls = Gtk.ListStore()
        update_interval_ls.set_column_types([str])
        self.update_interval_cmb.set_model(update_interval_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.update_interval_cmb.clear()
        renderer_text = Gtk.CellRendererText()
        self.update_interval_cmb.pack_start(renderer_text, True)
        self.update_interval_cmb.add_attribute(renderer_text, "text", 0)
        for value in self.update_interval_list:
            update_interval_ls.append([str(value)])
        self.update_interval_cmb.set_active(self.update_interval_list.index(Config.update_interval))

        # Set GUI preferences for "chart data history" setting
        graph_data_history_ls = Gtk.ListStore()
        graph_data_history_ls.set_column_types([str])
        self.graph_data_history_cmb.set_model(graph_data_history_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.graph_data_history_cmb.clear()
        renderer_text = Gtk.CellRendererText()
        self.graph_data_history_cmb.pack_start(renderer_text, True)
        self.graph_data_history_cmb.add_attribute(renderer_text, "text", 0)
        for value in self.chart_data_history_list:
            graph_data_history_ls.append([str(value)])
        self.graph_data_history_cmb.set_active(self.chart_data_history_list.index(Config.chart_data_history))

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
        default_main_tab_ls = Gtk.ListStore()
        default_main_tab_ls.set_column_types([str])
        self.default_main_tab_cmb.set_model(default_main_tab_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.default_main_tab_cmb.clear()
        renderer_text = Gtk.CellRendererText()
        self.default_main_tab_cmb.pack_start(renderer_text, True)
        self.default_main_tab_cmb.add_attribute(renderer_text, "text", 0)
        for value in self.default_main_tab_list:
            default_main_tab_ls.append([value])
        self.default_main_tab_cmb.set_active(Config.default_main_tab)
        if Config.remember_last_opened_tabs_on_application_start == 1:
            self.default_main_tab_cmb.set_sensitive(False)
        if Config.remember_last_opened_tabs_on_application_start == 0:
            self.default_main_tab_cmb.set_sensitive(True)

        # Set GUI preferences for "performance tab default sub-tab" setting
        default_sub_tab_ls = Gtk.ListStore()
        default_sub_tab_ls.set_column_types([str])
        self.default_sub_tab_cmb.set_model(default_sub_tab_ls)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.default_sub_tab_cmb.clear()
        renderer_text = Gtk.CellRendererText()
        self.default_sub_tab_cmb.pack_start(renderer_text, True)
        self.default_sub_tab_cmb.add_attribute(renderer_text, "text", 0)
        for value in self.performance_tab_default_sub_tab_list:
            default_sub_tab_ls.append([value])
        self.default_sub_tab_cmb.set_active(Config.performance_tab_default_sub_tab)
        if Config.remember_last_opened_tabs_on_application_start == 1:
            self.default_sub_tab_cmb.set_sensitive(False)
        if Config.remember_last_opened_tabs_on_application_start == 0:
            self.default_sub_tab_cmb.set_sensitive(True)

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


    # ----------------------- Called for trimming/adding performance data lists (cpu_usage_percent_ave, ram_usage_percent, ...) for chart data history when "chart_data_history" preference is changed -----------------------
    def settings_gui_set_chart_data_history_func(self):

        chart_data_history_current = len(Performance.cpu_usage_percent_ave)                       # Get current chart_data_history length. This value is same for all performance data lists (cpu_usage_percent_ave, ram_usage_percent, ...).
        chart_data_history_new = Config.chart_data_history
        if chart_data_history_current > chart_data_history_new:                                   # Trim beginning part of the lists if new "chart_data_history" value is smaller than the old value.
            Performance.cpu_usage_percent_ave = Performance.cpu_usage_percent_ave[chart_data_history_current-chart_data_history_new:]    # "cpu_usage_percent_ave" list has no sub-lists and trimming is performed in this way.
            cpu_usage_percent_per_core_len = len(Performance.cpu_usage_percent_per_core)
            for i in range(cpu_usage_percent_per_core_len):
                Performance.cpu_usage_percent_per_core[i] = Performance.cpu_usage_percent_per_core[i][chart_data_history_current-chart_data_history_new:]    # "cpu_usage_percent_per_core" list has sub-lists and trimming is performed for every sub-lists (for every CPU core).
            Performance.ram_usage_percent = Performance.ram_usage_percent[chart_data_history_current-chart_data_history_new:]    # "ram_usage_percent" list has no sub-lists and trimming is performed in this way.
            disk_read_speed_len = len(Performance.disk_read_speed)
            for i in range(disk_read_speed_len):
                Performance.disk_read_speed[i] = Performance.disk_read_speed[i][chart_data_history_current-chart_data_history_new:]    # "disk_read_speed" list has sub-lists and trimming is performed for every sub-lists (for every disk).
                Performance.disk_write_speed[i] = Performance.disk_write_speed[i][chart_data_history_current-chart_data_history_new:]    # "disk_write_speed" list has sub-lists and trimming is performed for every sub-lists (for every disk).
            network_receive_speed_len = len(Performance.network_receive_speed)
            for i in range(network_receive_speed_len):
                Performance.network_receive_speed[i] = Performance.network_receive_speed[i][chart_data_history_current-chart_data_history_new:]    # "network_receive_speed" list has sub-lists and trimming is performed for every sub-lists (for every network card).
                Performance.network_send_speed[i] = Performance.network_send_speed[i][chart_data_history_current-chart_data_history_new:]    # "network_send_speed" list has sub-lists and trimming is performed for every sub-lists (for every network card).
            if MainWindow.radiobutton1005.get_active() == True:
                from Gpu import Gpu
                Gpu.fps_count = Gpu.fps_count[chart_data_history_current-chart_data_history_new:]     # "fps_count" list has no sub-lists and trimming is performed in this way.
        if chart_data_history_current < chart_data_history_new:                                   # Add list of zeroes to the beginning part of the lists if new "chart_data_history" value is bigger than the old value.
            list_to_add = [0] * (chart_data_history_new - chart_data_history_current)             # Generate list of zeroes for adding to the beginning of te lists.
            Performance.cpu_usage_percent_ave = list_to_add + Performance.cpu_usage_percent_ave   # "cpu_usage_percent_ave" list has no sub-lists and addition is performed in this way.
            cpu_usage_percent_per_core_len = len(Performance.cpu_usage_percent_per_core)
            for i in range(cpu_usage_percent_per_core_len):
                Performance.cpu_usage_percent_per_core[i] = list_to_add + Performance.cpu_usage_percent_per_core[i]     # "cpu_usage_percent_per_core" list has sub-lists and addition is performed for every sub-lists (for every CPU core).
            Performance.ram_usage_percent = list_to_add + Performance.ram_usage_percent           # "ram_usage_percent" list has no sub-lists and addition is performed in this way.
            disk_read_speed_len = len(Performance.disk_read_speed)
            for i in range(disk_read_speed_len):
                Performance.disk_read_speed[i] = list_to_add + Performance.disk_read_speed[i]     # "disk_read_speed" list has sub-lists and addition is performed for every sub-lists (for every disk).
                Performance.disk_write_speed[i] = list_to_add + Performance.disk_write_speed[i]   # "disk_write_speed" list has sub-lists and addition is performed for every sub-lists (for every disk).
            network_receive_speed_len = len(Performance.network_receive_speed)
            for i in range(network_receive_speed_len):
                Performance.network_receive_speed[i] = list_to_add + Performance.network_receive_speed[i]    # "network_receive_speed" list has sub-lists and addition is performed for every sub-lists (for every network card).
                Performance.network_send_speed[i] = list_to_add + Performance.network_send_speed[i]    # "network_send_speed" list has sub-lists and addition is performed for every sub-lists (for every network card).
            if MainWindow.radiobutton1005.get_active() == True:
                from Gpu import Gpu
                Gpu.fps_count = list_to_add + Gpu.fps_count                                       # "fps_count" list has no sub-lists and addition is performed in this way.


    # ----------------------- Called for applying settings for all opened tabs (since application start) without waiting update interval -----------------------
    def settings_gui_apply_settings_immediately_func(self):

        # If "initial_already_run" variable is set as "0", initial and loop functions of the relevant tab will be run in the next main loop if the tab is already opened or these functions will be run immediately when the relevant tab is switched on even if it is opened before the reset.
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


    # ----------------------- Called for saving default main tab and performace tab sub-tab when "Remember last opened tabs" option is enabled -----------------------
    def settings_gui_default_tab_func(self):

        if MainWindow.radiobutton1.get_active() == True:
            Config.default_main_tab = 0
        elif MainWindow.radiobutton2.get_active() == True:
            Config.default_main_tab = 1
        elif MainWindow.radiobutton3.get_active() == True:
            Config.default_main_tab = 2
        elif MainWindow.radiobutton6.get_active() == True:
            Config.default_main_tab = 3
        elif MainWindow.radiobutton8.get_active() == True:
            Config.default_main_tab = 4

        if MainWindow.radiobutton1007.get_active() == True:
            Config.performance_tab_default_sub_tab = 0
        elif MainWindow.radiobutton1001.get_active() == True:
            Config.performance_tab_default_sub_tab = 1
        elif MainWindow.radiobutton1002.get_active() == True:
            Config.performance_tab_default_sub_tab = 2
        elif MainWindow.radiobutton1003.get_active() == True:
            Config.performance_tab_default_sub_tab = 3
        elif MainWindow.radiobutton1004.get_active() == True:
            Config.performance_tab_default_sub_tab = 4
        elif MainWindow.radiobutton1005.get_active() == True:
            Config.performance_tab_default_sub_tab = 5
        elif MainWindow.radiobutton1006.get_active() == True:
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


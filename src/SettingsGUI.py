#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

from locale import gettext as _tr

from Config import Config
from MainGUI import MainGUI
from Performance import Performance


class SettingsGUI:

    def __init__(self):

        # Get GUI objects from file
        builder2001 = Gtk.Builder()
        builder2001.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/SettingsWindow.ui")

        # Get GUI objects
        self.window2001 = builder2001.get_object('window2001')
        self.button2002 = builder2001.get_object('button2002')
        self.button2004 = builder2001.get_object('button2004')
        self.combobox2001 = builder2001.get_object('combobox2001')
        self.combobox2002 = builder2001.get_object('combobox2002')
        self.combobox2003 = builder2001.get_object('combobox2003')
        self.combobox2004 = builder2001.get_object('combobox2004')
        self.combobox2005 = builder2001.get_object('combobox2005')
        self.checkbutton2001 = builder2001.get_object('checkbutton2001')
        self.checkbutton2002 = builder2001.get_object('checkbutton2002')
        self.checkbutton2003 = builder2001.get_object('checkbutton2003')
        self.checkbutton2012 = builder2001.get_object('checkbutton2012')
        self.checkbutton2013 = builder2001.get_object('checkbutton2013')
        self.grid2001 = builder2001.get_object('grid2001')

        # Set window properties
        self.window2001.set_transient_for(MainGUI.window1)
        self.window2001.set_modal(True)

        # Connect GUI signals
        self.window2001.connect("delete-event", self.on_window2001_delete_event)
        self.window2001.connect("show", self.on_window2001_show)
        self.button2002.connect("clicked", self.on_button2002_clicked)
        self.button2004.connect("clicked", self.on_button2004_clicked)

        # Define data lists in order to add them into comboboxes.
        self.update_interval_list = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 5.0, 10.0]
        self.chart_data_history_list = [30, 60, 90, 120, 150, 180, 300, 600, 1200]
        self.default_main_tab_list = [_tr("Performance"), _tr("Processes"), _tr("Users"), _tr("Services"), _tr("System")]
        self.performance_tab_default_sub_tab_list = [_tr("Summary"), _tr("CPU"), _tr("Memory"), _tr("Disk"), _tr("Network"), _tr("GPU"), _tr("Sensors")]

        # For translating the text that is used in ".desktop" file.
        _text = [_tr("System Monitor"), _tr("Task Manager")]


    # ----------------------- Called for connecting some of the signals in order to disconnect them for setting GUI -----------------------
    def settings_connect_signals_func(self):

        self.combobox2001.connect("changed", self.on_combobox2001_changed)
        self.combobox2002.connect("changed", self.on_combobox2002_changed)
        self.combobox2003.connect("changed", self.on_combobox2003_changed)
        self.combobox2004.connect("changed", self.on_combobox2004_changed)
        self.combobox2005.connect("changed", self.on_combobox2005_changed)
        self.checkbutton2001.connect("toggled", self.on_checkbutton2001_toggled)
        self.checkbutton2002.connect("toggled", self.on_checkbutton2002_toggled)
        self.checkbutton2003.connect("toggled", self.on_checkbutton2003_toggled)
        self.checkbutton2012.connect("toggled", self.on_checkbutton2012_toggled)
        self.checkbutton2013.connect("toggled", self.on_checkbutton2013_toggled)


    # ----------------------- Called for disconnecting some of the signals in order to connect them for setting GUI -----------------------
    def settings_disconnect_signals_func(self):

        self.combobox2001.disconnect_by_func(self.on_combobox2001_changed)
        self.combobox2002.disconnect_by_func(self.on_combobox2002_changed)
        self.combobox2003.disconnect_by_func(self.on_combobox2003_changed)
        self.combobox2004.disconnect_by_func(self.on_combobox2004_changed)
        self.combobox2005.disconnect_by_func(self.on_combobox2005_changed)
        self.checkbutton2001.disconnect_by_func(self.on_checkbutton2001_toggled)
        self.checkbutton2002.disconnect_by_func(self.on_checkbutton2002_toggled)
        self.checkbutton2003.disconnect_by_func(self.on_checkbutton2003_toggled)
        self.checkbutton2012.disconnect_by_func(self.on_checkbutton2012_toggled)
        self.checkbutton2013.disconnect_by_func(self.on_checkbutton2013_toggled)


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    def on_window2001_show(self, widget):

        # Get current directory (which code of this application is in) and current user home directory (symlinks will be generated in).
        current_dir = os.path.dirname(os.path.realpath(__file__))
        current_user_homedir = os.environ.get('HOME')

        # Check if the application is a Python package and hide "update check setting widgets" if it is not a Python package.
        if current_dir.startswith("/usr/local/lib/") == False and current_dir.startswith(current_user_homedir + "/.local/lib/") == False:
            self.grid2001.hide()

        # Set GUI widgets for showing current preferences of settings.
        try:
            self.settings_disconnect_signals_func()
        except TypeError:
            pass
        self.settings_gui_general_settings_tab_set_func()
        self.settings_connect_signals_func()


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window2001_delete_event(self, widget, event):

        self.window2001.hide()
        return True


    # ----------------------- "Update interval" Combobox -----------------------
    def on_combobox2001_changed(self, widget):

        Config.update_interval = self.update_interval_list[widget.get_active()]

        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
        self.settings_gui_apply_settings_immediately_func()


    # ----------------------- "Chart data history" Combobox -----------------------
    def on_combobox2002_changed(self, widget):

        Config.chart_data_history = self.chart_data_history_list[widget.get_active()]

        Config.config_save_func()

        # Apply changes immediately (without waiting update interval).
        self.settings_gui_set_chart_data_history_func()
        self.settings_gui_apply_settings_immediately_func()


    # ----------------------- "Show performance summary on the headerbar" Checkbutton -----------------------
    def on_checkbutton2001_toggled(self, widget):

        # Add performance summary to the main window headerbar if preferred.
        if widget.get_active() == True:
            Config.performance_summary_on_the_headerbar = 1
            MainGUI.headerbar1.pack_start(MainGUI.grid101)

        # Remove performance summary from the main window headerbar if preferred.
        if widget.get_active() == False:
            Config.performance_summary_on_the_headerbar = 0
            MainGUI.headerbar1.remove(MainGUI.grid101)

        Config.config_save_func()


    # ----------------------- "Remember last opened tabs" Checkbutton -----------------------
    def on_checkbutton2002_toggled(self, widget):

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


    # ----------------------- "Default main tab" Combobox -----------------------
    def on_combobox2003_changed(self, widget):

        # Get selected tab as default main tab and save it if preferred.
        Config.default_main_tab = widget.get_active()
        Config.config_save_func()


    # ----------------------- "Performance tab default sub-tab" Combobox -----------------------
    def on_combobox2004_changed(self, widget):

        # Get selected tab as Performance tab default sub-tab and save it if preferred.
        Config.performance_tab_default_sub_tab = widget.get_active()
        Config.config_save_func()


    # ----------------------- "Language" Combobox -----------------------
    def on_combobox2005_changed(self, widget):

        # Set application language. This setting is applicaed after the application is restarted.
        Config.language = list(Config.language_dict.keys())[widget.get_active()]
        Config.config_save_func()


    # ----------------------- "Remember last selected hardware" Checkbutton -----------------------
    def on_checkbutton2003_toggled(self, widget):

        if widget.get_active() == True:
            Config.remember_last_selected_hardware = 1

        if widget.get_active() == False:
            Config.remember_last_selected_hardware = 0

        Config.config_save_func()


    # ----------------------- "Remember window size" Checkbutton -----------------------
    def on_checkbutton2012_toggled(self, widget):

        # Get window state (if full screen or not), window size (width, height) and save if preferred.
        if widget.get_active() == True:
            remember_window_size_value = 1
            main_window_state = MainGUI.window1.is_maximized()
            if main_window_state == True:
                main_window_state = 1
            if main_window_state == False:
                main_window_state = 0
            main_window_width, main_window_height = MainGUI.window1.get_size()
            Config.remember_window_size = [remember_window_size_value, main_window_state, main_window_width, main_window_height]

        # Reset window size/state settings if preferred.
        if widget.get_active() == False:
            remember_window_size_value = 0
            main_window_state = 0
            main_window_width, main_window_height = MainGUI.window1.get_default_size()
            Config.remember_window_size = [remember_window_size_value, main_window_state, main_window_width, main_window_height]

        Config.config_save_func()


    # ----------------------- "Check for updates" Checkbutton -----------------------
    def on_checkbutton2013_toggled(self, widget):

        if widget.get_active() == True:
            Config.check_for_updates_automatically = 1

        if widget.get_active() == False:
            Config.check_for_updates_automatically = 0

        Config.config_save_func()


    # ----------------------- "Reset general settings to defaults" Button -----------------------
    def on_button2002_clicked(self, widget):

        Config.config_default_general_general_func()
        Config.config_save_func()
        # Set "General" tab of the Settings window without disconnecting signals of the widgets in order to use these signals to reset the settings.
        self.settings_gui_general_settings_tab_set_func()

        # Length of performance data lists (cpu_usage_percent_ave, ram_usage_percent_ave, ...) have to be set after "chart_data_history" setting is reset in order to avoid errors.
        self.settings_gui_set_chart_data_history_func()

        # Apply selected CPU core, disk, network card changes
        Performance.performance_set_selected_cpu_core_func()
        Performance.performance_set_selected_disk_func()
        Performance.performance_set_selected_network_card_func()
        # Apply selected GPU changes
        try:
            from MainGUI import Gpu
            Gpu.gpu_set_selected_gpu_func()
        # "try-except" is used in order to avoid errors because "gpu_get_gpu_list_and_set_selected_gpu_func" module requires some modules in the Gpu module they are imported if Gpu tab is switched on.
        except ImportError:
            pass

        # Apply changes immediately (without waiting update interval).
        self.settings_gui_apply_settings_immediately_func()


    # ----------------------- "Reset all settings of the application to defaults" Button -----------------------
    def on_button2004_clicked(self, widget):

        self.settings_gui_reset_all_settings_warning_dialog()

        if self.warning_dialog2001_response == Gtk.ResponseType.YES:

            Config.config_default_reset_all_func()
            Config.config_save_func()
            self.settings_disconnect_signals_func()
            self.settings_gui_general_settings_tab_set_func()
            self.settings_connect_signals_func()

            # Length of performance data lists (cpu_usage_percent_ave, ram_usage_percent_ave, ...) have to be set after "chart_data_history" setting is reset in order to avoid errors.
            self.settings_gui_set_chart_data_history_func()

            # Apply selected CPU core, disk, network card changes
            Performance.performance_set_selected_cpu_core_func()
            Performance.performance_set_selected_disk_func()
            Performance.performance_set_selected_network_card_func()
            # Apply selected GPU changes
            try:
                from MainGUI import Gpu
                Gpu.gpu_set_selected_gpu_func()
            # "try-except" is used in order to avoid errors because "gpu_get_gpu_list_and_set_selected_gpu_func" module requires some modules in the Gpu module they are imported if Gpu tab is switched on.
            except ImportError:
                pass

            # Reset selected device on the list between Performance tab sub-tab list.
            MainGUI.main_gui_device_selection_list_func()

            # Apply changes immediately (without waiting update interval).
            self.settings_gui_apply_settings_immediately_func()


    # ----------------------- Called for setting "General" tab GUI items -----------------------
    def settings_gui_general_settings_tab_set_func(self):

        # Set GUI preferences for "update interval" setting
        liststore2001 = Gtk.ListStore()
        liststore2001.set_column_types([str])
        self.combobox2001.set_model(liststore2001)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox2001.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox2001.pack_start(renderer_text, True)
        self.combobox2001.add_attribute(renderer_text, "text", 0)
        for value in self.update_interval_list:
            liststore2001.append([str(value)])
        self.combobox2001.set_active(self.update_interval_list.index(Config.update_interval))

        # Set GUI preferences for "chart data history" setting
        liststore2002 = Gtk.ListStore()
        liststore2002.set_column_types([str])
        self.combobox2002.set_model(liststore2002)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox2002.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox2002.pack_start(renderer_text, True)
        self.combobox2002.add_attribute(renderer_text, "text", 0)
        for value in self.chart_data_history_list:
            liststore2002.append([str(value)])
        self.combobox2002.set_active(self.chart_data_history_list.index(Config.chart_data_history))

        # Set GUI preferences for "show performance summary on the headerbar" setting
        if Config.performance_summary_on_the_headerbar == 1:
            self.checkbutton2001.set_active(True)
        if Config.performance_summary_on_the_headerbar == 0:
            self.checkbutton2001.set_active(False)

        # Set GUI preferences for "remember last opened tabs" setting
        if Config.remember_last_opened_tabs_on_application_start == 1:
            self.checkbutton2002.set_active(True)
        if Config.remember_last_opened_tabs_on_application_start == 0:
            self.checkbutton2002.set_active(False)

        # Set GUI preferences for "defult main tab" setting
        liststore2003 = Gtk.ListStore()
        liststore2003.set_column_types([str])
        self.combobox2003.set_model(liststore2003)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox2003.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox2003.pack_start(renderer_text, True)
        self.combobox2003.add_attribute(renderer_text, "text", 0)
        for value in self.default_main_tab_list:
            liststore2003.append([value])
        self.combobox2003.set_active(Config.default_main_tab)
        if Config.remember_last_opened_tabs_on_application_start == 1:
            self.combobox2003.set_sensitive(False)
        if Config.remember_last_opened_tabs_on_application_start == 0:
            self.combobox2003.set_sensitive(True)

        # Set GUI preferences for "performance tab default sub-tab" setting
        liststore2004 = Gtk.ListStore()
        liststore2004.set_column_types([str])
        self.combobox2004.set_model(liststore2004)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox2004.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox2004.pack_start(renderer_text, True)
        self.combobox2004.add_attribute(renderer_text, "text", 0)
        for value in self.performance_tab_default_sub_tab_list:
            liststore2004.append([value])
        self.combobox2004.set_active(Config.performance_tab_default_sub_tab)
        if Config.remember_last_opened_tabs_on_application_start == 1:
            self.combobox2004.set_sensitive(False)
        if Config.remember_last_opened_tabs_on_application_start == 0:
            self.combobox2004.set_sensitive(True)

        # Set GUI preferences for "language" setting
        liststore2005 = Gtk.ListStore()
        liststore2005.set_column_types([str])
        self.combobox2005.set_model(liststore2005)
        # Clear combobox in order to prevent adding the same items when the function is called again.
        self.combobox2005.clear()
        renderer_text = Gtk.CellRendererText()
        self.combobox2005.pack_start(renderer_text, True)
        self.combobox2005.add_attribute(renderer_text, "text", 0)
        for value in Config.language_dict:
            if value == "system":
                value = _tr(Config.language_dict[value])
            else:
                value = Config.language_dict[value]
            liststore2005.append([value])
        self.combobox2005.set_active(list(Config.language_dict.keys()).index(Config.language))

        # Set GUI preferences for "remember last selected hardware" setting
        if Config.remember_last_selected_hardware == 1:
            self.checkbutton2003.set_active(True)
        if Config.remember_last_selected_hardware == 0:
            self.checkbutton2003.set_active(False)

        # Set GUI preferences for "remember window size" setting
        if Config.remember_window_size[0] == 1:
            self.checkbutton2012.set_active(True)
        if Config.remember_window_size[0] == 0:
            self.checkbutton2012.set_active(False)

        # Set GUI preferences for "check for updates automatically" setting
        if Config.check_for_updates_automatically == 1:
            self.checkbutton2013.set_active(True)
        if Config.check_for_updates_automatically == 0:
            self.checkbutton2013.set_active(False)


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
            if MainGUI.radiobutton1005.get_active() == True:
                from Gpu import Gpu
                Gpu.gpu_load_list = Gpu.gpu_load_list[length_difference:]

            # Process Details window CPU, memory (RSS), disk read speed and disk write speed lists
            if MainGUI.grid2.get_child_at(0,0) != None:
                import ProcessesDetails
                for process_details_object in ProcessesDetails.processes_details_object_list:
                    process_details_object.process_cpu_usage_list = process_details_object.process_cpu_usage_list[length_difference:]
                    process_details_object.process_ram_usage_list = process_details_object.process_ram_usage_list[length_difference:]
                    process_details_object.process_disk_read_speed_list = process_details_object.process_disk_read_speed_list[length_difference:]
                    process_details_object.process_disk_write_speed_list = process_details_object.process_disk_write_speed_list[length_difference:]

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
            if MainGUI.radiobutton1005.get_active() == True:
                from Gpu import Gpu
                Gpu.gpu_load_list = list_to_add + Gpu.gpu_load_list

            # Process Details window CPU, memory (RSS), disk read speed and disk write speed lists
            if MainGUI.grid2.get_child_at(0,0) != None:
                import ProcessesDetails
                for process_details_object in ProcessesDetails.processes_details_object_list:
                    process_details_object.process_cpu_usage_list = list_to_add + process_details_object.process_cpu_usage_list
                    process_details_object.process_ram_usage_list = list_to_add + process_details_object.process_ram_usage_list
                    process_details_object.process_disk_read_speed_list = list_to_add + process_details_object.process_disk_read_speed_list
                    process_details_object.process_disk_write_speed_list = list_to_add + process_details_object.process_disk_write_speed_list


    # ----------------------- Called for applying settings for all opened tabs (since application start) without waiting update interval -----------------------
    def settings_gui_apply_settings_immediately_func(self):

        # If "initial_already_run" variable is set as "0", initial and loop functions of the relevant tab will be run in the next main loop if the tab is already opened or these functions will be run immediately when the relevant tab is switched on even if it is opened before the reset.
        try:
            from MainGUI import Summary
            Summary.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainGUI import Cpu
            Cpu.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainGUI import Memory
            Memory.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainGUI import Disk
            Disk.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainGUI import Network
            Network.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainGUI import Gpu
            Gpu.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainGUI import Sensors
            Sensors.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainGUI import Processes
            Processes.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainGUI import Users
            Users.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainGUI import Services
            Services.initial_already_run = 0
        except ImportError:
            pass

        try:
            from MainGUI import System
            System.initial_already_run = 0
        except ImportError:
            pass

        MainGUI.main_gui_tab_loop_func()


    # ----------------------- Called for saving default main tab and performace tab sub-tab when "Remember last opened tabs" option is enabled -----------------------
    def settings_gui_default_tab_func(self):

        if MainGUI.radiobutton1.get_active() == True:
            Config.default_main_tab = 0
        elif MainGUI.radiobutton2.get_active() == True:
            Config.default_main_tab = 1
        elif MainGUI.radiobutton3.get_active() == True:
            Config.default_main_tab = 2
        elif MainGUI.radiobutton6.get_active() == True:
            Config.default_main_tab = 3
        elif MainGUI.radiobutton8.get_active() == True:
            Config.default_main_tab = 4

        if MainGUI.radiobutton1007.get_active() == True:
            Config.performance_tab_default_sub_tab = 0
        elif MainGUI.radiobutton1001.get_active() == True:
            Config.performance_tab_default_sub_tab = 1
        elif MainGUI.radiobutton1002.get_active() == True:
            Config.performance_tab_default_sub_tab = 2
        elif MainGUI.radiobutton1003.get_active() == True:
            Config.performance_tab_default_sub_tab = 3
        elif MainGUI.radiobutton1004.get_active() == True:
            Config.performance_tab_default_sub_tab = 4
        elif MainGUI.radiobutton1005.get_active() == True:
            Config.performance_tab_default_sub_tab = 5
        elif MainGUI.radiobutton1006.get_active() == True:
            Config.performance_tab_default_sub_tab = 6


    # ----------------------- Called for showing a warning dialog for resetting all settings -----------------------
    def settings_gui_reset_all_settings_warning_dialog(self):

        warning_dialog2001 = Gtk.MessageDialog(transient_for=self.window2001, title="", flags=0, message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do you want to reset all settings to defaults?"))
        warning_dialog2001.format_secondary_text("")
        self.warning_dialog2001_response = warning_dialog2001.run()
        warning_dialog2001.destroy()


SettingsGUI = SettingsGUI()


#!/usr/bin/env python3

# ----------------------------------- Settings - Settings GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def settings_gui_import_func():

    global Gtk, Gdk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os


    global Config, MainGUI, Performance
    import Config, MainGUI, Performance


    # Import locale and gettext modules for defining translation texts which will be recognized by gettext application (will be run by programmer externally) and exported into a ".pot" file. 
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    import locale
    from locale import gettext as _tr

    # Define contstants for language translation support
    global application_name
    application_name = "system-monitoring-center"
    translation_files_path = "/usr/share/locale"
    system_current_language = os.environ.get("LANG")

    # Define functions for language translation support
    locale.bindtextdomain(application_name, translation_files_path)
    locale.textdomain(application_name)
    locale.setlocale(locale.LC_ALL, system_current_language)


# ----------------------------------- Settings - Settings GUI Function (contains the code of this module in order to avoid running them during module import and defines GUI objects and functions/signals) -----------------------------------
def settings_gui_func():

    # Settings tab GUI objects
    global builder2001, window2001
    global button2001, button2002, button2003, button2004
    global combobox2001, combobox2002, combobox2003, combobox2004
    global checkbutton2001, checkbutton2002, checkbutton2003, checkbutton2004, checkbutton2005, checkbutton2006
    global checkbutton2007, checkbutton2008, checkbutton2009, checkbutton2010, checkbutton2011, checkbutton2012
    global spinbutton2001


    # Settings tab GUI objects - get
    builder2001 = Gtk.Builder()
    builder2001.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/SettingsWindow.ui")

    window2001 = builder2001.get_object('window2001')
    button2001 = builder2001.get_object('button2001')
    button2002 = builder2001.get_object('button2002')
    button2003 = builder2001.get_object('button2003')
    button2004 = builder2001.get_object('button2004')
    combobox2001 = builder2001.get_object('combobox2001')
    combobox2002 = builder2001.get_object('combobox2002')
    combobox2003 = builder2001.get_object('combobox2003')
    combobox2004 = builder2001.get_object('combobox2004')
    checkbutton2001 = builder2001.get_object('checkbutton2001')
    checkbutton2002 = builder2001.get_object('checkbutton2002')
    checkbutton2003 = builder2001.get_object('checkbutton2003')
    checkbutton2004 = builder2001.get_object('checkbutton2004')
    checkbutton2005 = builder2001.get_object('checkbutton2005')
    checkbutton2006 = builder2001.get_object('checkbutton2006')
    checkbutton2007 = builder2001.get_object('checkbutton2007')
    checkbutton2008 = builder2001.get_object('checkbutton2008')
    checkbutton2009 = builder2001.get_object('checkbutton2009')
    checkbutton2010 = builder2001.get_object('checkbutton2010')
    checkbutton2011 = builder2001.get_object('checkbutton2011')
    checkbutton2012 = builder2001.get_object('checkbutton2012')
    spinbutton2001 = builder2001.get_object('spinbutton2001')


    # Settings tab GUI functions
    def on_window2001_delete_event(widget, event):
        window2001.hide()
        return True

    def on_window2001_show(widget):
        try:                                                                                  # No these signals are not connected on the first showing of the Settings Window. This error is not encountered on later "show window" operations during the application runtime. This "try-except" is used for avoiding errors in this situation.
            settings_disconnect_signals_func()                                                # Disconnect some of the GUI signals in order to avoid performing "settings" operations when GUI object preferences are set (for example a checkbox is set as enable/disabled for the current preference).
        except TypeError:
            pass
        settings_gui_set_func()                                                               # Set GUI objects appropriate with user preferences when Settings window is shown
        settings_connect_signals_func()                                                       # Connect GUI signals.

    def on_combobox2001_changed(widget):                                                      # "Update interval" GUI object signal
        Config.update_interval = update_interval_list[combobox2001.get_active()]
        Config.config_save_func()

    def on_combobox2002_changed(widget):                                                      # "Chart data history" GUI object signal
        Config.chart_data_history = chart_data_history_list[combobox2002.get_active()]
        Config.config_save_func()
        settings_gui_set_chart_data_history_func()

    def on_checkbutton2001_toggled(widget):                                                   # "Show performance summary on the headerbar" GUI object signal
        if checkbutton2001.get_active() == True:
            MainGUI.headerbar1.add(MainGUI.grid101)                                           # Add performance summary to the main window headerbar.
            Config.performance_summary_on_the_headerbar = 1
        if checkbutton2001.get_active() == False:
            MainGUI.headerbar1.remove(MainGUI.grid101)                                        # Remove performance summary from the main window headerbar.
            Config.performance_summary_on_the_headerbar = 0
        Config.config_save_func()

    def on_checkbutton2002_toggled(widget):                                                   # "Remember last opened tabs on application start" GUI object signal
        if checkbutton2002.get_active() == True:
            Config.remember_last_opened_tabs_on_application_start = 1
            combobox2003.set_sensitive(False)
            combobox2004.set_sensitive(False)
        if checkbutton2002.get_active() == False:
            Config.remember_last_opened_tabs_on_application_start = 0
            combobox2003.set_sensitive(True)
            combobox2004.set_sensitive(True)
        Config.config_save_func()

    def on_combobox2003_changed(widget):                                                      # "Default main tab" GUI object signal
        Config.default_main_tab = combobox2003.get_active()
        Config.config_save_func()

    def on_combobox2004_changed(widget):                                                      # "Performance tab default sub-tab" GUI object signal
        Config.performance_tab_default_sub_tab = combobox2004.get_active()
        Config.config_save_func()

    def on_checkbutton2003_toggled(widget):                                                   # "Remember last selected hardware" GUI object signal
        if checkbutton2003.get_active() == True:
            Config.remember_last_selected_hardware = 1
        if checkbutton2003.get_active() == False:
            Config.remember_last_selected_hardware = 0
        Config.config_save_func()

    def on_button2001_clicked(widget):                                                        # "Set background colors for all charts" GUI object signal
        if "colorchooserdialog1001" not in globals():
            global colorchooserdialog1001
            colorchooserdialog2001 = Gtk.ColorChooserDialog()
        red, blue, green, alpha = Config.chart_background_color_all_charts                    # Get current foreground color of the chart
        colorchooserdialog2001.set_rgba(Gdk.RGBA(red, blue, green, alpha))                    # Set current chart foregorund color as selected color of the dialog on dialog run
        dialog_response = colorchooserdialog2001.run()
        if dialog_response == Gtk.ResponseType.OK:
            selected_color = colorchooserdialog2001.get_rgba()
            Config.chart_background_color_all_charts = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]
            colorchooserdialog2001.hide()
            Config.config_save_func()
        if dialog_response == Gtk.ResponseType.CANCEL:
            colorchooserdialog2001.hide()

    def on_button2002_clicked(widget):                                                        # "Reset general settings to defaults" GUI object signal
        Config.config_default_general_general_func()
        Config.config_save_func()
        settings_gui_general_settings_tab_set_func()
        settings_gui_set_chart_data_history_func()                                        # Length of performance data lists (cpu_usage_percent_ave, ram_usage_percent_ave, ...) have to be set after "chart_data_history" setting is reset in order to avoid errors.
        Performance.performance_set_selected_cpu_core_func()                              # Call this function in order to apply selected CPU core changes
        Performance.performance_set_selected_disk_func()                                  # Call this function in order to apply selected disk changes
        Performance.performance_set_selected_network_card_func()                          # Call this function in order to apply selected network card changes
        Performance.performance_get_gpu_list_and_set_selected_gpu_func()                  # Call this function in order to apply selected GPU changes
        Performance.performance_foreground_initial_func()                                 # Call this function in order to apply changes immediately (without waiting update interval).
        Performance.performance_foreground_func()                                         # Call this function in order to apply changes immediately (without waiting update interval).

    def spinbutton2001_on_value_changed(widget):                                              # "Window transparency" GUI object signal
        Config.floating_summary_window_transparency = spinbutton2001.get_value()
        Config.config_save_func()

    def on_checkbutton2004_toggled(widget):                                                   # "Show/Hide Performance Information - CPU Usage Average" GUI object signal
        settings_gui_add_remove_floating_summary_performance_information_func()

    def on_checkbutton2005_toggled(widget):                                                   # "Show/Hide Performance Information - RAM Usage" GUI object signal
        settings_gui_add_remove_floating_summary_performance_information_func()

    def on_checkbutton2006_toggled(widget):                                                   # "Show/Hide Performance Information - Disk Read+Write Speed" GUI object signal
        settings_gui_add_remove_floating_summary_performance_information_func()

    def on_checkbutton2007_toggled(widget):                                                   # "Show/Hide Performance Information - Disk Read Speed" GUI object signal
        settings_gui_add_remove_floating_summary_performance_information_func()

    def on_checkbutton2008_toggled(widget):                                                   # "Show/Hide Performance Information - Disk Write Speed" GUI object signal
        settings_gui_add_remove_floating_summary_performance_information_func()

    def on_checkbutton2009_toggled(widget):                                                   # "Show/Hide Performance Information - Network Receive+Send Speed" GUI object signal
        settings_gui_add_remove_floating_summary_performance_information_func()

    def on_checkbutton2010_toggled(widget):                                                   # "Show/Hide Performance Information - Network Receive Speed" GUI object signal
        settings_gui_add_remove_floating_summary_performance_information_func()

    def on_checkbutton2011_toggled(widget):                                                   # "Show/Hide Performance Information - Network Send Speed" GUI object signal
        settings_gui_add_remove_floating_summary_performance_information_func()

    def on_checkbutton2012_toggled(widget):                                                   # "Show/Hide Performance Information - FPS" GUI object signal
        settings_gui_add_remove_floating_summary_performance_information_func()

    def on_button2003_clicked(widget):                                                        # "Reset floating summary window settings to defaults" GUI object signal
        Config.config_default_general_floating_summary_func()
        Config.config_save_func()
        settings_gui_floating_summary_settings_tab_set_func()

    def on_button2004_clicked(widget):                                                        # "Reset all settings of the application to defaults" button
        settings_gui_reset_all_settings_warning_dialog()
        if warning_dialog2001_response == Gtk.ResponseType.YES:
            Config.config_default_reset_all_func()
            Config.config_save_func()
            settings_gui_set_func()
            settings_gui_set_chart_data_history_func()                                        # Length of performance data lists (cpu_usage_percent_ave, ram_usage_percent_ave, ...) have to be set after "chart_data_history" setting is reset in order to avoid errors.
            Performance.performance_set_selected_cpu_core_func()                              # Call this function in order to apply selected CPU core changes
            Performance.performance_set_selected_disk_func()                                  # Call this function in order to apply selected disk changes
            Performance.performance_set_selected_network_card_func()                          # Call this function in order to apply selected network card changes
            Performance.performance_get_gpu_list_and_set_selected_gpu_func()                  # Call this function in order to apply selected GPU changes
            Performance.performance_foreground_initial_func()                                 # Call this function in order to apply changes immediately (without waiting update interval).
            Performance.performance_foreground_func()                                         # Call this function in order to apply changes immediately (without waiting update interval).
        if warning_dialog2001_response == Gtk.ResponseType.NO:
            pass                                                                              # Do nothing when "No" button is clicked. Dialog will be closed.


    # Settings tab GUI functions - connect
    window2001.connect("delete-event", on_window2001_delete_event)
    window2001.connect("show", on_window2001_show)
    button2001.connect("clicked", on_button2001_clicked)
    button2002.connect("clicked", on_button2002_clicked)
    button2003.connect("clicked", on_button2003_clicked)
    button2004.connect("clicked", on_button2004_clicked)


    # ----------------------------------- Settings - Settings GUI Connect Signals Function (connects signals of the some of the Settings Window GUI objects (selectable/changeable GUI objects) in order to prevent them preforming actions when GUI objects are set appropriate with user preferences.) -----------------------------------
    def settings_connect_signals_func():
        combobox2001.connect("changed", on_combobox2001_changed)
        combobox2002.connect("changed", on_combobox2002_changed)
        combobox2003.connect("changed", on_combobox2003_changed)
        combobox2004.connect("changed", on_combobox2004_changed)
        checkbutton2001.connect("toggled", on_checkbutton2001_toggled)
        checkbutton2002.connect("toggled", on_checkbutton2002_toggled)
        checkbutton2003.connect("toggled", on_checkbutton2003_toggled)
        checkbutton2004.connect("toggled", on_checkbutton2004_toggled)
        checkbutton2005.connect("toggled", on_checkbutton2005_toggled)
        checkbutton2006.connect("toggled", on_checkbutton2006_toggled)
        checkbutton2007.connect("toggled", on_checkbutton2007_toggled)
        checkbutton2008.connect("toggled", on_checkbutton2008_toggled)
        checkbutton2009.connect("toggled", on_checkbutton2009_toggled)
        checkbutton2010.connect("toggled", on_checkbutton2010_toggled)
        checkbutton2011.connect("toggled", on_checkbutton2011_toggled)
        checkbutton2012.connect("toggled", on_checkbutton2012_toggled)
        spinbutton2001.connect("value-changed", spinbutton2001_on_value_changed)


    # ----------------------------------- Settings - Settings GUI Disconnect Signals Function (disconnects signals of the some of the Settings Window GUI objects (selectable/changeable GUI objects) in order to prevent them preforming actions when GUI objects are set appropriate with user preferences.) -----------------------------------
    def settings_disconnect_signals_func():
        combobox2001.disconnect_by_func(on_combobox2001_changed)
        combobox2002.disconnect_by_func(on_combobox2002_changed)
        combobox2003.disconnect_by_func(on_combobox2003_changed)
        combobox2004.disconnect_by_func(on_combobox2004_changed)
        checkbutton2001.disconnect_by_func(on_checkbutton2001_toggled)
        checkbutton2002.disconnect_by_func(on_checkbutton2002_toggled)
        checkbutton2003.disconnect_by_func(on_checkbutton2003_toggled)
        checkbutton2004.disconnect_by_func(on_checkbutton2004_toggled)
        checkbutton2005.disconnect_by_func(on_checkbutton2005_toggled)
        checkbutton2006.disconnect_by_func(on_checkbutton2006_toggled)
        checkbutton2007.disconnect_by_func(on_checkbutton2007_toggled)
        checkbutton2008.disconnect_by_func(on_checkbutton2008_toggled)
        checkbutton2009.disconnect_by_func(on_checkbutton2009_toggled)
        checkbutton2010.disconnect_by_func(on_checkbutton2010_toggled)
        checkbutton2011.disconnect_by_func(on_checkbutton2011_toggled)
        checkbutton2012.disconnect_by_func(on_checkbutton2012_toggled)
        spinbutton2001.disconnect_by_func(spinbutton2001_on_value_changed)


# ----------------------------------- Settings - Settings GUI Set Function (sets Settings Window GUI objects appropriate with user preferences get from Config module) -----------------------------------
def settings_gui_set_func():
    settings_gui_general_settings_tab_set_func()
    settings_gui_floating_summary_settings_tab_set_func()


# ----------------------------------- Settings - Settings GUI General Settings Tab Set Function (sets Settings Window GUI objects appropriate with user preferences get from Config module) -----------------------------------
def settings_gui_general_settings_tab_set_func():
    # Set GUI preferences for "update interval" setting
    if "liststore2001" not in globals():
        global liststore2001, update_interval_list
        update_interval_list = [0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 5.0, 10.0]
        liststore2001 = Gtk.ListStore()
        liststore2001.set_column_types([str])
        combobox2001.set_model(liststore2001)
        renderer_text = Gtk.CellRendererText()
        combobox2001.pack_start(renderer_text, True)
        combobox2001.add_attribute(renderer_text, "text", 0)
        for value in update_interval_list:
            liststore2001.append([str(value)])
    combobox2001.set_active(update_interval_list.index(Config.update_interval))
    # Set GUI preferences for "chart data history" setting
    if "liststore2002" not in globals():
        global liststore2002, chart_data_history_list
        chart_data_history_list = [30, 60, 90, 120, 150, 180, 240, 480]
        liststore2002 = Gtk.ListStore()
        liststore2002.set_column_types([str])
        combobox2002.set_model(liststore2002)
        renderer_text = Gtk.CellRendererText()
        combobox2002.pack_start(renderer_text, True)
        combobox2002.add_attribute(renderer_text, "text", 0)
        for value in chart_data_history_list:
            liststore2002.append([str(value)])
    combobox2002.set_active(chart_data_history_list.index(Config.chart_data_history))
    # Set GUI preferences for "show performance summary on the headerbar" setting
    if Config.performance_summary_on_the_headerbar == 1:
        checkbutton2001.set_active(True)
    if Config.performance_summary_on_the_headerbar == 0:
        checkbutton2001.set_active(False)
    # Set GUI preferences for "remember last opened tabs on application start" setting
    if Config.remember_last_opened_tabs_on_application_start == 1:
        checkbutton2002.set_active(True)
    if Config.remember_last_opened_tabs_on_application_start == 0:
        checkbutton2002.set_active(False)
    # Set GUI preferences for "defult main tab" setting
    if "liststore2003" not in globals():
        global liststore2003, default_main_tab_list
        default_main_tab_list = [_tr("Performance"), _tr("Processes"), _tr("Users"), _tr("Storage"), _tr("Startup"), _tr("Services"), _tr("Environment Variables"), _tr("System")]
        liststore2003 = Gtk.ListStore()
        liststore2003.set_column_types([str])
        combobox2003.set_model(liststore2003)
        renderer_text = Gtk.CellRendererText()
        combobox2003.pack_start(renderer_text, True)
        combobox2003.add_attribute(renderer_text, "text", 0)
        for value in default_main_tab_list:
            liststore2003.append([value])
    combobox2003.set_active(Config.default_main_tab)
    # Set GUI preferences for "performance tab default sub-tab" setting
    if "liststore2004" not in globals():
        global liststore2004, performance_tab_default_sub_tab_list
        performance_tab_default_sub_tab_list = [_tr("CPU"), _tr("RAM"), _tr("Disk"), _tr("Network"), _tr("GPU"), _tr("Sensors")]
        liststore2004 = Gtk.ListStore()
        liststore2004.set_column_types([str])
        combobox2004.set_model(liststore2004)
        renderer_text = Gtk.CellRendererText()
        combobox2004.pack_start(renderer_text, True)
        combobox2004.add_attribute(renderer_text, "text", 0)
        for value in performance_tab_default_sub_tab_list:
            liststore2004.append([value])
    combobox2004.set_active(Config.performance_tab_default_sub_tab)
    # Set GUI preferences for "remember last selected hardware" setting
    if Config.remember_last_selected_hardware == 1:
        checkbutton2003.set_active(True)
    if Config.remember_last_selected_hardware == 0:
        checkbutton2003.set_active(False)


# ----------------------------------- Settings - Settings GUI Floating Summary Settings Tab Set Function (sets Settings Window GUI objects appropriate with user preferences get from Config module) -----------------------------------
def settings_gui_floating_summary_settings_tab_set_func():
    # Set GUI preferences for "window transparency" setting
    if "adjustment2001" not in globals():
        global adjustment2001
        adjustment2001 = Gtk.Adjustment().new(Config.floating_summary_window_transparency, 0.0, 1.0, 0.05, 0.1, 0.0)
        spinbutton2001.set_digits(2)
        spinbutton2001.set_adjustment(adjustment2001)
    adjustment2001.set_value(Config.floating_summary_window_transparency)
    # Set GUI preferences for "show/hide information" setting
    if 0 in Config.floating_summary_data_shown:
        checkbutton2004.set_active(True)
    if 0 not in Config.floating_summary_data_shown:
        checkbutton2004.set_active(False)
    if 1 in Config.floating_summary_data_shown:
        checkbutton2005.set_active(True)
    if 1 not in Config.floating_summary_data_shown:
        checkbutton2005.set_active(False)
    if 2 in Config.floating_summary_data_shown:
        checkbutton2006.set_active(True)
    if 2 not in Config.floating_summary_data_shown:
        checkbutton2006.set_active(False)
    if 3 in Config.floating_summary_data_shown:
        checkbutton2007.set_active(True)
    if 3 not in Config.floating_summary_data_shown:
        checkbutton2007.set_active(False)
    if 4 in Config.floating_summary_data_shown:
        checkbutton2008.set_active(True)
    if 4 not in Config.floating_summary_data_shown:
        checkbutton2008.set_active(False)
    if 5 in Config.floating_summary_data_shown:
        checkbutton2009.set_active(True)
    if 5 not in Config.floating_summary_data_shown:
        checkbutton2009.set_active(False)
    if 6 in Config.floating_summary_data_shown:
        checkbutton2010.set_active(True)
    if 6 not in Config.floating_summary_data_shown:
        checkbutton2010.set_active(False)
    if 7 in Config.floating_summary_data_shown:
        checkbutton2011.set_active(True)
    if 7 not in Config.floating_summary_data_shown:
        checkbutton2011.set_active(False)
    if 8 in Config.floating_summary_data_shown:
        checkbutton2012.set_active(True)
    if 8 not in Config.floating_summary_data_shown:
        checkbutton2012.set_active(False)


# ----------------------------------- Settings - Add/Remove Floating Summary Performance Information Function (adds/removes performance information for floating summary window) -----------------------------------
def settings_gui_add_remove_floating_summary_performance_information_func():

    Config.floating_summary_data_shown = []
    if checkbutton2004.get_active() == True:
        Config.floating_summary_data_shown.append(0)
    if checkbutton2005.get_active() == True:
        Config.floating_summary_data_shown.append(1)
    if checkbutton2006.get_active() == True:
        Config.floating_summary_data_shown.append(2)
    if checkbutton2007.get_active() == True:
        Config.floating_summary_data_shown.append(3)
    if checkbutton2008.get_active() == True:
        Config.floating_summary_data_shown.append(4)
    if checkbutton2009.get_active() == True:
        Config.floating_summary_data_shown.append(5)
    if checkbutton2010.get_active() == True:
        Config.floating_summary_data_shown.append(6)
    if checkbutton2011.get_active() == True:
        Config.floating_summary_data_shown.append(7)
    if checkbutton2012.get_active() == True:
        Config.floating_summary_data_shown.append(8)
    Config.config_save_func()


# ----------------------------------- Settings - Set Chart Data History Function (trim/adds performance data lists (cpu_usage_percent_ave, ram_usage_percent, ...) when user changes "chart_data_history" preference) -----------------------------------
def settings_gui_set_chart_data_history_func():

    chart_data_history_current = len(Performance.cpu_usage_percent_ave)                       # Get current chart_data_history length. This value is same for all performance data lists (cpu_usage_percent_ave, ram_usage_percent, ...).
    chart_data_history_new = Config.chart_data_history
    if chart_data_history_current > chart_data_history_new:                                   # Trim beginning part of the lists if new "chart_data_history" value is smaller than the old value.
        Performance.cpu_usage_percent_ave = Performance.cpu_usage_percent_ave[chart_data_history_current-chart_data_history_new:]    # "cpu_usage_percent_ave" list has no sub-lists and trimming is performed in this way.
        Performance.ram_usage_percent = Performance.ram_usage_percent[chart_data_history_current-chart_data_history_new:]    # "ram_usage_percent" list has no sub-lists and trimming is performed in this way.
        Performance.fps_count = Performance.fps_count[chart_data_history_current-chart_data_history_new:]    # "fps_count" list has no sub-lists and trimming is performed in this way.
        disk_read_speed_len = len(Performance.disk_read_speed)
        for i in range(disk_read_speed_len):
            Performance.disk_read_speed[i] = Performance.disk_read_speed[i][chart_data_history_current-chart_data_history_new:]    # "disk_read_speed" list has sub-lists and trimming is performed for every sub-lists (for every disk).
            Performance.disk_write_speed[i] = Performance.disk_write_speed[i][chart_data_history_current-chart_data_history_new:]    # "disk_write_speed" list has sub-lists and trimming is performed for every sub-lists (for every disk).
        network_receive_speed_len = len(Performance.network_receive_speed)
        for i in range(network_receive_speed_len):
            Performance.network_receive_speed[i] = Performance.network_receive_speed[i][chart_data_history_current-chart_data_history_new:]    # "network_receive_speed" list has sub-lists and trimming is performed for every sub-lists (for every network card).
            Performance.network_send_speed[i] = Performance.network_send_speed[i][chart_data_history_current-chart_data_history_new:]    # "network_send_speed" list has sub-lists and trimming is performed for every sub-lists (for every network card).
    if chart_data_history_current < chart_data_history_new:                                   # Add list of zeroes to the beginning part of the lists if new "chart_data_history" value is bigger than the old value.
        list_to_add = [0] * (chart_data_history_new - chart_data_history_current)             # Generate list of zeroes for adding to the beginning of te lists.
        Performance.cpu_usage_percent_ave = list_to_add + Performance.cpu_usage_percent_ave    # "cpu_usage_percent_ave" list has no sub-lists and addition is performed in this way.
        Performance.ram_usage_percent = list_to_add + Performance.ram_usage_percent           # "ram_usage_percent" list has no sub-lists and addition is performed in this way.
        Performance.fps_count = list_to_add + Performance.fps_count                           # "fps_count" list has no sub-lists and addition is performed in this way.
        disk_read_speed_len = len(Performance.disk_read_speed)
        for i in range(disk_read_speed_len):
            Performance.disk_read_speed[i] = list_to_add + Performance.disk_read_speed[i]     # "disk_read_speed" list has sub-lists and addition is performed for every sub-lists (for every disk).
            Performance.disk_write_speed[i] = list_to_add + Performance.disk_write_speed[i]    # "disk_write_speed" list has sub-lists and addition is performed for every sub-lists (for every disk).
        network_receive_speed_len = len(Performance.network_receive_speed)
        for i in range(network_receive_speed_len):
            Performance.network_receive_speed[i] = list_to_add + Performance.network_receive_speed[i]    # "network_receive_speed" list has sub-lists and addition is performed for every sub-lists (for every network card).
            Performance.network_send_speed[i] = list_to_add + Performance.network_send_speed[i]    # "network_send_speed" list has sub-lists and addition is performed for every sub-lists (for every network card).


# ----------------------------------- Settings - Reset All Settings Warning Dialog Function (shows an warning dialog when "Reset all settings of the application to defaults" button is clicked) -----------------------------------
def settings_gui_reset_all_settings_warning_dialog():

    warning_dialog2001 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Warning"), flags=0, message_type=Gtk.MessageType.WARNING,
    buttons=Gtk.ButtonsType.YES_NO, text=_tr("Reset All Settings?"), )
    warning_dialog2001.format_secondary_text(_tr("Do you want to reset all settings of the application to defaults?"))
    global warning_dialog2001_response
    warning_dialog2001_response = warning_dialog2001.run()
    warning_dialog2001.destroy()

#!/usr/bin/env python3

# ----------------------------------- MainGUI - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def main_gui_import_func():

    global Gtk, Gdk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os


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

# ----------------------------------- MainGUI - GUI Function (the code of this module in order to avoid running them during module import and defines GUI functions/signals) -----------------------------------
def main_gui_func():

    global builder
    global window1
    global headerbar1, menubutton1, grid101, label101, label102
    global grid10, stack1
    global radiobutton1, radiobutton2, radiobutton3, radiobutton4, radiobutton5, radiobutton6, radiobutton7, radiobutton8
    global grid1, grid2, grid3, grid4, grid5, grid6, grid7, grid8

    builder = Gtk.Builder()
    builder.set_translation_domain(application_name)                                          # For showing translated texts onthe Glade generated GTK GUI
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MainWindow.glade")

    window1 = builder.get_object('window1')

    headerbar1 = builder.get_object('headerbar1')
    menubutton1 = builder.get_object('menubutton1')

    grid101 = builder.get_object('grid101')
    label101 = builder.get_object('label101')
    label102 = builder.get_object('label102')

    grid10 = builder.get_object('grid10')
    stack1 = builder.get_object('stack1')
    radiobutton1 = builder.get_object('radiobutton1')
    radiobutton2 = builder.get_object('radiobutton2')
    radiobutton3 = builder.get_object('radiobutton3')
    radiobutton4 = builder.get_object('radiobutton4')
    radiobutton5 = builder.get_object('radiobutton5')
    radiobutton6 = builder.get_object('radiobutton6')
    radiobutton7 = builder.get_object('radiobutton7')
    radiobutton8 = builder.get_object('radiobutton8')
    grid1 = builder.get_object('grid1')
    grid2 = builder.get_object('grid2')
    grid3 = builder.get_object('grid3')
    grid4 = builder.get_object('grid4')
    grid5 = builder.get_object('grid5')
    grid6 = builder.get_object('grid6')
    grid7 = builder.get_object('grid7')
    grid8 = builder.get_object('grid8')


    def on_window1_destroy(widget):
        Gtk.main_quit()

    def on_window1_show(widget):                                                              # Some functions such a (hardware selection, performance backround function, main menu gui importing and setting popup menu (main menu) are run after main window is shown. This is due to decreasing window display delay.
        main_gui_main_function_run_func()                                                     # Run main tab function after initial showing main window (this function is also called when main tab checkbuttons are toggled).

    def on_radiobutton1_toggled(widget):                                                      # "Performance" radiobutton
        if radiobutton1.get_active() == True:
            main_gui_main_function_run_func()

    def on_radiobutton2_toggled(widget):                                                      # "Processes" radiobutton
        if radiobutton2.get_active() == True:
            main_gui_main_function_run_func()

    def on_radiobutton3_toggled(widget):                                                      # "Users" radiobutton
        if radiobutton3.get_active() == True:
            main_gui_main_function_run_func()

    def on_radiobutton4_toggled(widget):                                                      # "Storage" radiobutton
        if radiobutton4.get_active() == True:
            main_gui_main_function_run_func()


    def on_radiobutton5_toggled(widget):                                                      # "Startup" radiobutton
        if radiobutton5.get_active() == True:
            main_gui_main_function_run_func()

    def on_radiobutton6_toggled(widget):                                                      # "Services" radiobutton
        if radiobutton6.get_active() == True:
            main_gui_main_function_run_func()

    def on_radiobutton7_toggled(widget):                                                      # "Environment Variables" radiobutton
        if radiobutton7.get_active() == True:
            main_gui_main_function_run_func()

    def on_radiobutton8_toggled(widget):                                                      # "System" radiobutton
        if radiobutton8.get_active() == True:
            main_gui_main_function_run_func()


    window1.connect("destroy", on_window1_destroy)
    window1.connect("show", on_window1_show)
    radiobutton1.connect("toggled", on_radiobutton1_toggled)
    radiobutton2.connect("toggled", on_radiobutton2_toggled)
    radiobutton3.connect("toggled", on_radiobutton3_toggled)
    radiobutton4.connect("toggled", on_radiobutton4_toggled)
    radiobutton5.connect("toggled", on_radiobutton5_toggled)
    radiobutton6.connect("toggled", on_radiobutton6_toggled)
    radiobutton7.connect("toggled", on_radiobutton7_toggled)
    radiobutton8.connect("toggled", on_radiobutton8_toggled)


# ----------------------------------- MainGUI - Main Set Default Tab Function (switches to default main tab ((Performance, Processes, Users, Storage, Startup, Services, Environment Variables, OS)) on initial run when) -----------------------------------
def main_gui_default_main_tab_func():

    stack1.set_transition_duration(0)
    if Config.default_main_tab == 0:
         radiobutton1.set_active(True)
    if Config.default_main_tab == 1:
         radiobutton2.set_active(True)
    if Config.default_main_tab == 2:
         radiobutton3.set_active(True)
    if Config.default_main_tab == 3:
         radiobutton4.set_active(True)
    if Config.default_main_tab == 4:
         radiobutton5.set_active(True)
    if Config.default_main_tab == 5:
         radiobutton6.set_active(True)
    if Config.default_main_tab == 6:
         radiobutton7.set_active(True)
    if Config.default_main_tab == 7:
         radiobutton8.set_active(True)
    stack1.set_transition_duration(200)


# ----------------------------------- MainGUI - Main Function Run Function (runs main functions (Performance, Processes, Users, Storage, Startup, Services, Environment Variables, OS) when their stack page is selected) -----------------------------------
def main_gui_main_function_run_func():

    if Config.show_floating_summary == 1:                                                     # Show Floating Summary window appropriate with user preferences
        if "FloatingSummary" not in globals():
            global FloatingSummary
            import FloatingSummary
            FloatingSummary.floating_summary_import_func()
            FloatingSummary.floating_summary_initial_func()
        FloatingSummary.floating_summary_thread_run_func()
        FloatingSummary.floating_summary_window.show()

    if radiobutton1.get_active() == True:                                                     # It switches to "Performance" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid1)
        if 'PerformanceGUI' not in globals():                                                 # Check if "PerformanceGUI" module is imported. Therefore it is not reimported after switching "Performance" tab off and on if "PerformanceGUI" name is in globals(). It is not recognized after tab switch if it is not imported as global.
            global PerformanceGUI, PerformanceMenusGUI, ChartPlots
            import PerformanceGUI, PerformanceMenusGUI, ChartPlots
            PerformanceGUI.performance_gui_import_func()
            PerformanceGUI.performance_gui_func()
            PerformanceMenusGUI.performance_menus_import_func()
            PerformanceMenusGUI.performance_menus_gui_func()
            Performance.performance_foreground_thread_run_func()
            ChartPlots.chart_plots_import_func()
            ChartPlots.charts_gui_func()
            ChartPlots.chart_plots_drawingarea_signal_connect_thread_func()
        Performance.performance_foreground_initial_initial_func()

        if PerformanceGUI.radiobutton1001.get_active() == True:                               # It switches to "CPU" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1001)
        if PerformanceGUI.radiobutton1002.get_active() == True:                               # It switches to "RAM" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1002)
        if PerformanceGUI.radiobutton1003.get_active() == True:                               # It switches to "Disk" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1003)
        if PerformanceGUI.radiobutton1004.get_active() == True:                               # It switches to "Network" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1004)
        if PerformanceGUI.radiobutton1005.get_active() == True:                               # It switches to "GPU" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1005)
        if PerformanceGUI.radiobutton1006.get_active() == True:                               # It switches to "Sensors" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1006)
            if 'Sensors' not in globals():                                                    # Check if "Sensors" module is imported. Therefore it is not reimported after switching "Performance" tab off and on if "PerformanceGUI" name is in globals(). It is not recognized after tab switch if it is not imported as global.
                global Sensors
                import Sensors
                Sensors.sensors_import_func()
            Sensors.sensors_thread_run_func()

    if radiobutton2.get_active() == True:                                                     # It switches to "Processes" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid2)
        if 'ProcessesGUI' not in globals():                                                   # Check if "ProcessesGUI" module is imported. Therefore it is not reimported after switching "Processes" tab off and on if "ProcessesGUI" name is in globals(). It is not recognized after tab switch if it is not imported as global.
            import Processes, ProcessesGUI, ProcessesMenusGUI, ProcessesDetailsGUI, ProcessesDetails, ProcessesCustomPriorityGUI
            Processes.processes_import_func()
            ProcessesGUI.processes_gui_import_func()
            ProcessesGUI.processes_gui_func()
            ProcessesMenusGUI.processes_menus_import_func()
            ProcessesMenusGUI.processes_menus_gui_func()
            Processes.processes_thread_run_func()
            ProcessesDetailsGUI.processes_details_gui_import_function()
            ProcessesDetailsGUI.processes_details_gui_function()
            ProcessesDetails.processes_details_import_func()
            ProcessesCustomPriorityGUI.processes_custom_priority_import_func()
            ProcessesCustomPriorityGUI.processes_custom_priority_gui_func()

    if radiobutton3.get_active() == True:                                                     # It switches to "Users" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid3)
        if 'UsersGUI' not in globals():
            import Users, UsersGUI, UsersMenusGUI
            Users.users_import_func()
            UsersGUI.users_gui_import_func()
            UsersGUI.users_gui_func()
            UsersMenusGUI.users_menus_import_func()
            UsersMenusGUI.users_menus_gui_func()
            Users.users_thread_run_func()

    if radiobutton4.get_active() == True:                                                     # It switches to "Storage" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid4)
        import Storage, StorageGUI, StorageMenusGUI, StorageDetailsGUI, StorageDetails, StorageRenameGUI
        Storage.storage_import_func()
        StorageGUI.storage_gui_import_func()
        StorageGUI.storage_gui_func()
        StorageMenusGUI.storage_menus_import_func()
        StorageMenusGUI.storage_menus_gui_func()
        Storage.storage_thread_run_func()
        StorageDetailsGUI.storage_details_gui_import_function()
        StorageDetailsGUI.storage_details_gui_function()
        StorageDetails.storage_details_import_func()
        StorageRenameGUI.storage_rename_import_func()
        StorageRenameGUI.storage_rename_gui_func()

    if radiobutton5.get_active() == True:                                                     # It switches to "Startup" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid5)
        import Startup, StartupGUI, StartupMenusGUI, StartupNewItemGUI
        Startup.startup_import_func()
        StartupGUI.startup_gui_import_func()
        StartupGUI.startup_gui_func()
        StartupMenusGUI.startup_menus_import_func()
        StartupMenusGUI.startup_menus_gui_func()
        Startup.startup_thread_run_func()
        StartupNewItemGUI.startup_rename_import_func()
        StartupNewItemGUI.startup_rename_gui_func()

    if radiobutton6.get_active() == True:                                                     # It switches to "Services" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid6)
        import Services, ServicesGUI, ServicesMenusGUI, ServicesDetailsGUI, ServicesDetails
        Services.services_import_func()
        ServicesGUI.services_gui_import_func()
        ServicesGUI.services_gui_func()
        ServicesMenusGUI.services_menus_import_func()
        ServicesMenusGUI.services_menus_gui_func()
        ServicesDetailsGUI.services_details_gui_import_function()
        ServicesDetailsGUI.services_details_gui_function()
        ServicesDetails.services_details_import_func()
        Services.services_thread_run_func()

    if radiobutton7.get_active() == True:                                                     # It switches to "Environment Variables" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid7)
        import EnvironmentVariables, EnvironmentVariablesGUI, EnvironmentVariablesMenusGUI
        EnvironmentVariables.environment_variables_import_func()
        EnvironmentVariablesGUI.environment_variables_gui_import_func()
        EnvironmentVariablesGUI.environment_variables_gui_func()
        EnvironmentVariablesMenusGUI.environment_variables_menus_import_func()
        EnvironmentVariablesMenusGUI.environment_variables_menus_gui_func()
        EnvironmentVariables.environment_variables_thread_run_func()

    if radiobutton8.get_active() == True:                                                     # It switches to "System" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid8)
        import System, SystemGUI
        System.system_import_func()
        SystemGUI.system_gui_import_func()
        SystemGUI.system_gui_func()
        System.system_thread_run_func()



main_gui_import_func()
main_gui_func()

import Config                                                                                 # Import Config module which reads, saves and contains all read settings
Config.config_import_func()                                                                   # Start import operations of the module
Config.config_read_func()                                                                     # Start setting read operations of the module

import Performance                                                                            # Import Performance module which gets hardware/performance data and shows on the GUI
Performance.performance_import_func()
Performance.performance_background_thread_run_func()

import MainMenusDialogsGUI                                                                    # Import MainMenusDialogsGUI module which contains main menus/dialogs GUI obejcts and signals
MainMenusDialogsGUI.main_menus_gui_import_func()
MainMenusDialogsGUI.main_menus_gui_func()

menubutton1.set_popup(MainMenusDialogsGUI.menu1001m)                                          # Set popup menu (Main menu)
main_gui_default_main_tab_func()                                                              # Run default tab function after initial showing main window

# Show information for warning the user if the application has been run with root privileges. Information is shown just below the application window headerbar.
if os.geteuid() == 0:                                                                         # Check UID if it is "0". This means the application is run with root privileges.
    label_root_warning = Gtk.Label(label=_tr("Warning! The application has been run with root privileges, you may harm your system."))    # Generate a new label for the information. This label does not exist in the ".glade" UI file.
    # label_root_warning.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0.0, 1.0, 0.0, 1.0))
    label_root_warning.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))               # Set background color of the label.
    grid10.insert_row(0)                                                                      # Insert a row at top of the grid.
    grid10.attach(label_root_warning, 0, 0, 1, 1)                                             # Attach the label to the grid at (0, 0) position.
    label_root_warning.set_visible(True)                                                      # Set the label as visible.


window1.show_all()                                                                            # Show main window
Gtk.main()                                                                                    # Start main event which keeps GUI open until program is ended by user or programmatically.

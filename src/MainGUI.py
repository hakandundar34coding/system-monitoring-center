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
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MainWindow.ui")

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
        global Config
        import Config                                                                         # Import Config module which reads, saves and contains all read settings
        Config.config_import_func()                                                           # Start import operations of the module
        Config.config_read_func()                                                             # Start setting read operations of the module

        main_gui_main_function_run_func()                                                     # Run main tab function after initial showing main window (this function is also called when main tab checkbuttons are toggled).

        main_gui_default_main_tab_func()                                                      # Run default tab function after initial showing of the main window. This function have to be called after "main_gui_main_function_run_func" function in order to avoid errors else "Performance" tab functions/variables/data will not be defined.

        import MainMenusDialogsGUI                                                            # Import MainMenusDialogsGUI module which contains main menus/dialogs GUI obejcts and signals
        MainMenusDialogsGUI.main_menus_gui_import_func()
        MainMenusDialogsGUI.main_menus_gui_func()

        menubutton1.set_popup(MainMenusDialogsGUI.menu1001m)                                  # Set popup menu (Main menu)

        # Remove performance summary widgets from the main window headerbar. This summary exists in the .ui file (for easier GUI design/maintenance) and it is removed from the headerbar on application start appropriate with user preferences.
        if Config.performance_summary_on_the_headerbar == 0:
            headerbar1.remove(grid101)

        # Show information for warning the user if the application has been run with root privileges. Information is shown just below the application window headerbar.
        if os.geteuid() == 0:                                                                 # Check UID if it is "0". This means the application is run with root privileges.
            label_root_warning = Gtk.Label(label=_tr("Warning! The application has been run with root privileges, you may harm your system."))    # Generate a new label for the information. This label does not exist in the ".ui" UI file.
            # label_root_warning.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0.0, 1.0, 0.0, 1.0))
            label_root_warning.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))       # Set background color of the label.
            grid10.insert_row(0)                                                              # Insert a row at top of the grid.
            grid10.attach(label_root_warning, 0, 0, 1, 1)                                     # Attach the label to the grid at (0, 0) position.
            label_root_warning.set_visible(True)                                              # Set the label as visible.

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


# ----------------------------------- MainGUI - Main Set Default Tab Function (switches to default main tab ((Performance, Processes, Users, Storage, Startup, Services, Environment Variables, OS)) on initial run) -----------------------------------
def main_gui_default_main_tab_func():

    default_main_tab = Config.default_main_tab                                                # Local definition of this variable is made for lower CPU usage becuse this variable is used multiple times.
    stack1.set_transition_duration(0)
    if default_main_tab == 0:
         radiobutton1.set_active(True)
    if default_main_tab == 1:
         radiobutton2.set_active(True)
    if default_main_tab == 2:
         radiobutton3.set_active(True)
    if default_main_tab == 3:
         radiobutton4.set_active(True)
    if default_main_tab == 4:
         radiobutton5.set_active(True)
    if default_main_tab == 5:
         radiobutton6.set_active(True)
    if default_main_tab == 6:
         radiobutton7.set_active(True)
    if default_main_tab == 7:
         radiobutton8.set_active(True)
    stack1.set_transition_duration(200)


# ----------------------------------- MainGUI - Set Performance Tab Default Sub-Tab Function (switches to performance tab default sub-tab ((CPU, RAM, Disk, Network, GPU, Sensors)) on initial run) -----------------------------------
def main_gui_peformance_tab_default_sub_tab_func():

    performance_tab_default_sub_tab = Config.performance_tab_default_sub_tab                  # Local definition of this variable is made for lower CPU usage becuse this variable is used multiple times.
    PerformanceGUI.stack1001.set_transition_duration(0)
    if performance_tab_default_sub_tab == 0:
         PerformanceGUI.radiobutton1001.set_active(True)
    if performance_tab_default_sub_tab == 1:
         PerformanceGUI.radiobutton1002.set_active(True)
    if performance_tab_default_sub_tab == 2:
         PerformanceGUI.radiobutton1003.set_active(True)
    if performance_tab_default_sub_tab == 3:
         PerformanceGUI.radiobutton1004.set_active(True)
    if performance_tab_default_sub_tab == 4:
         PerformanceGUI.radiobutton1005.set_active(True)
    if performance_tab_default_sub_tab == 5:
         PerformanceGUI.radiobutton1006.set_active(True)
    PerformanceGUI.stack1001.set_transition_duration(200)


# ----------------------------------- MainGUI - Main Function Run Function (runs main functions (Performance, Processes, Users, Storage, Startup, Services, Environment Variables, OS) when their stack page is selected. All main tabs and performance tab sub-tabs switches are controlled in this function) -----------------------------------
def main_gui_main_function_run_func():

    remember_last_opened_tabs_on_application_start = Config.remember_last_opened_tabs_on_application_start    # Local definition of this variable is made for lower CPU usage becuse this variable is used multiple times.

    if radiobutton1.get_active() == True:                                                     # It switches to "Performance" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid1)
        if remember_last_opened_tabs_on_application_start == 1:
            Config.default_main_tab = 0
        if 'PerformanceGUI' not in globals():                                                 # Check if "PerformanceGUI" module is imported. Therefore it is not reimported after switching "Performance" tab off and on if "PerformanceGUI" name is in globals(). It is not recognized after tab switch if it is not imported as global.
            global Performance, PerformanceGUI, PerformanceMenusGUI, ChartPlots
            import Performance, PerformanceGUI, PerformanceMenusGUI, ChartPlots
            Performance.performance_import_func()
            Performance.performance_background_thread_run_func()
            PerformanceGUI.performance_gui_import_func()
            PerformanceGUI.performance_gui_func()
            PerformanceMenusGUI.performance_menus_import_func()
            PerformanceMenusGUI.performance_menus_gui_func()
            Performance.performance_foreground_thread_run_func()
            ChartPlots.chart_plots_import_func()
            ChartPlots.charts_gui_func()
            ChartPlots.chart_plots_drawingarea_signal_connect_thread_func()
            main_gui_peformance_tab_default_sub_tab_func()                                    # Run performance tab default sub-tab function after initial showing of the main window
        Performance.performance_foreground_initial_initial_func()

        if PerformanceGUI.radiobutton1001.get_active() == True:                               # It switches to "CPU" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1001)
            if remember_last_opened_tabs_on_application_start == 1:
                Config.performance_tab_default_sub_tab = 0
        if PerformanceGUI.radiobutton1002.get_active() == True:                               # It switches to "RAM" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1002)
            if remember_last_opened_tabs_on_application_start == 1:
                Config.performance_tab_default_sub_tab = 1
        if PerformanceGUI.radiobutton1003.get_active() == True:                               # It switches to "Disk" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1003)
            if remember_last_opened_tabs_on_application_start == 1:
                Config.performance_tab_default_sub_tab = 2
        if PerformanceGUI.radiobutton1004.get_active() == True:                               # It switches to "Network" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1004)
            if remember_last_opened_tabs_on_application_start == 1:
                Config.performance_tab_default_sub_tab = 3
        if PerformanceGUI.radiobutton1005.get_active() == True:                               # It switches to "GPU" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1005)
            if remember_last_opened_tabs_on_application_start == 1:
                Config.performance_tab_default_sub_tab = 4
        if PerformanceGUI.radiobutton1006.get_active() == True:                               # It switches to "Sensors" tab if relevant radiobutton is clicked.
            PerformanceGUI.stack1001.set_visible_child(PerformanceGUI.grid1006)
            if remember_last_opened_tabs_on_application_start == 1:
                Config.performance_tab_default_sub_tab = 5
            if 'Sensors' not in globals():                                                    # Check if "Sensors" module is imported. Therefore it is not reimported after switching "Performance" tab off and on if "PerformanceGUI" name is in globals(). It is not recognized after tab switch if it is not imported as global.
                global Sensors
                import Sensors
                Sensors.sensors_import_func()
            Sensors.sensors_thread_run_func()

    if radiobutton2.get_active() == True:                                                     # It switches to "Processes" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid2)
        if remember_last_opened_tabs_on_application_start == 1:
            Config.default_main_tab = 1
        if 'ProcessesGUI' not in globals():                                                   # Check if "ProcessesGUI" module is imported. Therefore it is not reimported after switching "Processes" tab off and on if "ProcessesGUI" name is in globals(). It is not recognized after tab switch if it is not imported as global.
            global Processes, ProcessesGUI, ProcessesMenusGUI, ProcessesDetailsGUI, ProcessesDetails, ProcessesCustomPriorityGUI
            import Processes, ProcessesGUI, ProcessesMenusGUI, ProcessesDetailsGUI, ProcessesDetails, ProcessesCustomPriorityGUI
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            Processes.processes_import_func()
            ProcessesGUI.processes_gui_import_func()
            ProcessesGUI.processes_gui_func()
            grid2.attach(ProcessesGUI.grid2101, 0, 0, 1, 1)                                   # Attach the grid to the grid (on the Main Window) at (0, 0) position.
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            ProcessesMenusGUI.processes_menus_import_func()
            ProcessesMenusGUI.processes_menus_gui_func()
            ProcessesDetailsGUI.processes_details_gui_import_function()
            ProcessesDetailsGUI.processes_details_gui_function()
            ProcessesDetails.processes_details_import_func()
            ProcessesCustomPriorityGUI.processes_custom_priority_import_func()
            ProcessesCustomPriorityGUI.processes_custom_priority_gui_func()
        Processes.processes_thread_run_func()

    if radiobutton3.get_active() == True:                                                     # It switches to "Users" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid3)
        if remember_last_opened_tabs_on_application_start == 1:
            Config.default_main_tab = 2
        if 'UsersGUI' not in globals():
            global Users, UsersGUI, UsersMenusGUI, UsersDetailsGUI, UsersDetails
            import Users, UsersGUI, UsersMenusGUI, UsersDetailsGUI, UsersDetails
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            Users.users_import_func()
            UsersGUI.users_gui_import_func()
            UsersGUI.users_gui_func()
            grid3.attach(UsersGUI.grid3101, 0, 0, 1, 1)                                       # Attach the grid to the grid (on the Main Window) at (0, 0) position.     
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            UsersMenusGUI.users_menus_import_func()
            UsersMenusGUI.users_menus_gui_func()
            UsersDetailsGUI.users_details_gui_import_function()
            UsersDetailsGUI.users_details_gui_function()
            UsersDetails.users_details_import_func()
        Users.users_thread_run_func()

    if radiobutton4.get_active() == True:                                                     # It switches to "Storage" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid4)
        if remember_last_opened_tabs_on_application_start == 1:
            Config.default_main_tab = 3
        if 'StorageGUI' not in globals():
            global Storage, StorageGUI, StorageMenusGUI, StorageDetailsGUI, StorageDetails, StorageRenameGUI
            import Storage, StorageGUI, StorageMenusGUI, StorageDetailsGUI, StorageDetails, StorageRenameGUI
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            Storage.storage_import_func()
            StorageGUI.storage_gui_import_func()
            StorageGUI.storage_gui_func()
            grid4.attach(StorageGUI.grid4101, 0, 0, 1, 1)                                     # Attach the grid to the grid (on the Main Window) at (0, 0) position.     
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            StorageMenusGUI.storage_menus_import_func()
            StorageMenusGUI.storage_menus_gui_func()
            StorageDetailsGUI.storage_details_gui_import_function()
            StorageDetailsGUI.storage_details_gui_function()
            StorageDetails.storage_details_import_func()
            StorageRenameGUI.storage_rename_import_func()
            StorageRenameGUI.storage_rename_gui_func()
        Storage.storage_thread_run_func()

    if radiobutton5.get_active() == True:                                                     # It switches to "Startup" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid5)
        if remember_last_opened_tabs_on_application_start == 1:
            Config.default_main_tab = 4
        if 'StartupGUI' not in globals():
            global Startup, StartupGUI, StartupMenusGUI, StartupNewItemGUI
            import Startup, StartupGUI, StartupMenusGUI, StartupNewItemGUI
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            Startup.startup_import_func()
            StartupGUI.startup_gui_import_func()
            StartupGUI.startup_gui_func()
            grid5.attach(StartupGUI.grid5101, 0, 0, 1, 1)                                     # Attach the grid to the grid (on the Main Window) at (0, 0) position.     
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            StartupMenusGUI.startup_menus_import_func()
            StartupMenusGUI.startup_menus_gui_func()
            StartupNewItemGUI.startup_new_item_import_func()
            StartupNewItemGUI.startup_new_item_gui_func()
        Startup.startup_thread_run_func()

    if radiobutton6.get_active() == True:                                                     # It switches to "Services" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid6)
        if remember_last_opened_tabs_on_application_start == 1:
            Config.default_main_tab = 5
        if 'ServicesGUI' not in globals():
            global Services, ServicesGUI, ServicesMenusGUI, ServicesDetailsGUI, ServicesDetails
            import Services, ServicesGUI, ServicesMenusGUI, ServicesDetailsGUI, ServicesDetails
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            Services.services_import_func()
            ServicesGUI.services_gui_import_func()
            ServicesGUI.services_gui_func()
            grid6.attach(ServicesGUI.grid6101, 0, 0, 1, 1)                                    # Attach the grid to the grid (on the Main Window) at (0, 0) position.     
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            ServicesMenusGUI.services_menus_import_func()
            ServicesMenusGUI.services_menus_gui_func()
            ServicesDetailsGUI.services_details_gui_import_function()
            ServicesDetailsGUI.services_details_gui_function()
            ServicesDetails.services_details_import_func()
        Services.services_thread_run_func()

    if radiobutton7.get_active() == True:                                                     # It switches to "Environment Variables" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid7)
        if remember_last_opened_tabs_on_application_start == 1:
            Config.default_main_tab = 6
        if 'EnvironmentVariablesGUI' not in globals():
            global EnvironmentVariables, EnvironmentVariablesGUI, EnvironmentVariablesMenusGUI, EnvironmentVariablesInputGUI
            import EnvironmentVariables, EnvironmentVariablesGUI, EnvironmentVariablesMenusGUI, EnvironmentVariablesInputGUI
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            EnvironmentVariables.environment_variables_import_func()
            EnvironmentVariablesGUI.environment_variables_gui_import_func()
            EnvironmentVariablesGUI.environment_variables_gui_func()
            grid7.attach(EnvironmentVariablesGUI.grid7101, 0, 0, 1, 1)                        # Attach the grid to the grid (on the Main Window) at (0, 0) position.     
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            EnvironmentVariablesMenusGUI.environment_variables_menus_import_func()
            EnvironmentVariablesMenusGUI.environment_variables_menus_gui_func()
            EnvironmentVariablesInputGUI.environment_variables_input_gui_import_func()
            EnvironmentVariablesInputGUI.environment_variables_input_gui_func()
        EnvironmentVariables.environment_variables_thread_run_func()

    if radiobutton8.get_active() == True:                                                     # It switches to "System" tab if relevant radiobutton is clicked.
        stack1.set_visible_child(grid8)
        if remember_last_opened_tabs_on_application_start == 1:
            Config.default_main_tab = 7
        if 'SystemGUI' not in globals():
            global System, SystemGUI
            import System, SystemGUI
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
            System.system_import_func()
            SystemGUI.system_gui_import_func()
            SystemGUI.system_gui_func()
            grid8.attach(SystemGUI.grid8101, 0, 0, 1, 1)                                      # Attach the grid to the grid (on the Main Window) at (0, 0) position.
            while Gtk.events_pending():                                                       # Used for more fluent tab switch.
                Gtk.main_iteration()
        System.system_thread_run_func()

    if Config.show_floating_summary == 1:                                                     # Show Floating Summary window appropriate with user preferences. Code below this statement have to be used after "Performance" tab functions, variables, data are defined and functions are run in order to avoid errors.
        if "FloatingSummary" not in globals():
            global FloatingSummary
            import FloatingSummary
            FloatingSummary.floating_summary_import_func()
            FloatingSummary.floating_summary_initial_func()
        FloatingSummary.floating_summary_thread_run_func()
        FloatingSummary.floating_summary_window.show()

    Config.config_save_func()


main_gui_import_func()
main_gui_func()


window1.show_all()                                                                            # Show main window
Gtk.main()                                                                                    # Start main event which keeps GUI open until program is ended by user or programmatically.

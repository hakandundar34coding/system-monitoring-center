#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib
import os

# "_tr" arbitrary variable will be recognized by gettext application for extracting texts to be translated
import locale
from locale import gettext as _tr

from Performance import Performance


# Define class
class MainGUI:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Configurations for language translation support
        locale.bindtextdomain("system-monitoring-center", os.path.dirname(os.path.realpath(__file__)) + "/../locale")
        locale.textdomain("system-monitoring-center")
        try:
            locale.setlocale(locale.LC_ALL, os.environ.get("LANG"))
        # Prevent errors if there are problems with language installations on the system. English language (language in the .ui files) is used in this situation.
        except Exception:
            pass

        # Generate symbolic links for GUI icons and application shortcut (.desktop file) in user folders if they are not generated.
        self.main_gui_application_system_integration_func()

        # Adapt to system color scheme (light/dark) on systems with newer versions than GTK3.
        self.main_gui_adapt_color_scheme_for_gtk4_based_systems_func()

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MainWindow.ui")

        # Get GUI objects
        self.window1 = builder.get_object('window1')
        self.headerbar1 = builder.get_object('headerbar1')
        self.button1 = builder.get_object('button1')
        self.grid10 = builder.get_object('grid10')
        self.stack1 = builder.get_object('stack1')
        self.radiobutton1 = builder.get_object('radiobutton1')
        self.radiobutton2 = builder.get_object('radiobutton2')
        self.radiobutton3 = builder.get_object('radiobutton3')
        self.radiobutton6 = builder.get_object('radiobutton6')
        self.radiobutton8 = builder.get_object('radiobutton8')
        self.grid1 = builder.get_object('grid1')
        self.grid2 = builder.get_object('grid2')
        self.grid3 = builder.get_object('grid3')
        self.grid5 = builder.get_object('grid5')
        self.grid6 = builder.get_object('grid6')
        self.grid8 = builder.get_object('grid8')
        # Get Main GUI - Performance tab GUI objects
        self.stack1001 = builder.get_object('stack1001')
        self.radiobutton1001 = builder.get_object('radiobutton1001')
        self.radiobutton1002 = builder.get_object('radiobutton1002')
        self.radiobutton1003 = builder.get_object('radiobutton1003')
        self.radiobutton1004 = builder.get_object('radiobutton1004')
        self.radiobutton1005 = builder.get_object('radiobutton1005')
        self.radiobutton1006 = builder.get_object('radiobutton1006')
        self.radiobutton1007 = builder.get_object('radiobutton1007')
        self.grid1001 = builder.get_object('grid1001')
        self.grid1002 = builder.get_object('grid1002')
        self.grid1003 = builder.get_object('grid1003')
        self.grid1004 = builder.get_object('grid1004')
        self.grid1005 = builder.get_object('grid1005')
        self.grid1006 = builder.get_object('grid1006')
        self.grid1007 = builder.get_object('grid1007')

        self.grid1010 = builder.get_object('grid1010')

        # Connect GUI signals
        self.window1.connect("destroy", self.on_window1_destroy)
        self.window1.connect("delete_event", self.on_window1_delete)
        self.window1.connect("show", self.on_window1_show)
        self.button1.connect("clicked", self.on_button1_clicked)


    # ----------------------- Called for connecting some of the signals in order to connect them after some code/functions to avoid running these signals -----------------------
    def main_gui_radiobuttons_connect_signals_func(self):

        # Connect Main GUI - Main tabs GUI signals
        self.radiobutton1.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)
        self.radiobutton2.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)
        self.radiobutton3.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)
        self.radiobutton6.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)
        self.radiobutton8.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)
        # Connect Main GUI - Performance tab GUI signals
        self.radiobutton1001.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)
        self.radiobutton1002.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)
        self.radiobutton1003.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)
        self.radiobutton1004.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)
        self.radiobutton1005.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)
        self.radiobutton1006.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)
        self.radiobutton1007.connect("toggled", self.on_main_gui_tab_radiobuttons_toggled)


    # ----------------------- Called for running code/functions when window is closed -----------------------
    def on_window1_destroy(self, widget):

        Gtk.main_quit()


    # ----------------------- Called for running code/functions when window is closed -----------------------
    # Window size is get by this event in order to get current window size. It gives pre-defined window size (it can be defined in the window .ui files) if ".get_size()" is used in "window destroy event" function.
    def on_window1_delete(self, widget, data=None):

        # Get window state (if full screen or not), window size (width, height) and save
        if Config.remember_window_size[0] == 1:
            main_window_state = widget.is_maximized()
            if main_window_state == True:
                main_window_state = 1
            if main_window_state == False:
                main_window_state = 0
            main_window_width, main_window_height = widget.get_size()
            remember_window_size_value = Config.remember_window_size[0]
            Config.remember_window_size = [remember_window_size_value, main_window_state, main_window_width, main_window_height]
            Config.config_save_func()


    # ----------------------- Called for running code/functions when GUI is shown -----------------------
    # Some functions (such as hardware selection, performance backround function, main menu gui importing, etc.) are run after main window is shown in order to reduce window display delay.
    def on_window1_show(self, widget):

        # Hide Services tab if systemd is not used on the system.
        try:
            with open("/proc/1/comm") as reader:
                process_name = reader.read().strip()
            if process_name != "systemd":
                self.radiobutton6.set_visible(False)
        except Exception:
            pass

        # Read and get config data
        global Config
        from Config import Config

        # Resize/set state (full screen or not) of the main window if "remember window size" option is enabled.
        remember_window_size = Config.remember_window_size
        if remember_window_size[0] == 1:
            if remember_window_size[1] == 1:
                widget.maximize()
            if remember_window_size[1] == 0:
                widget.resize(remember_window_size[2], remember_window_size[3])

        # Run "Performance" module in order to provide performance data to Performance tab and performance summary on the headerbar.
        global Performance
        from Performance import Performance
        # Function is run directly without using "GLib.idle_add([function_name])" in order to avoid errors which are given if another threads (such as threads in CPU module) run before this function is finished.
        Performance.performance_background_initial_func()

        # Add performance summary widgets to the main window headerbar.
        if Config.performance_summary_on_the_headerbar == 1:
            from PerformanceSummaryHeaderbar import PerformanceSummaryHeaderbar
            self.headerbar1.pack_start(PerformanceSummaryHeaderbar.grid101)

        # Define these settings (they are not saved to file) in order to avoid error on the first call of "main_gui_tab_loop_func" function.
        Config.current_main_tab = -1
        Config.performance_tab_current_sub_tab = -1

        # Start loop function to run loop functions of opened tabs to get data of them.
        self.main_gui_tab_loop_func()

        # Run default tab function after main window is shown.
        self.main_gui_default_tab_func()

        # Connect main gui radiobuttons signals after switching to default tab (by using "main_gui_default_tab_func") in order to avoid running functions during this switches.
        self.main_gui_radiobuttons_connect_signals_func()

        # Run main tab function after main window is shown (this function is also called when main tab checkbuttons are toggled).
        self.main_gui_tab_switch_func()

        # Show information for warning the user if the application has been run with root privileges (if UID=0). Information is shown just below the application window headerbar.
        if os.geteuid() == 0:
            # Generate a new label for the information. This label does not exist in the ".ui" UI file.
            label_root_warning = Gtk.Label(label=_tr("Warning! The application has been run with root privileges, you may harm your system."))
            css = b"label {background: rgba(100%,0%,0%,1.0);}"
            style_provider = Gtk.CssProvider()
            style_provider.load_from_data(css)
            label_root_warning.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
            self.grid10.insert_row(0)
            # Attach the label to the grid at (0, 0) position.
            self.grid10.attach(label_root_warning, 0, 0, 1, 1)
            label_root_warning.set_visible(True)

        # Check if there is a newer version of the software if relevant setting is enabled and the application is a Python package (directory is in "/usr/local/lib/..." or in "/home/[user_name]/.local/lib/...".
        # New version can not be checked if the application is run with root privileges. BEcause "pip" does not run "index" command in this situation.
        if Config.check_for_updates_automatically == 1:

            # Get current directory (which code of this application is in) and current user home directory (symlinks will be generated in).
            current_dir = os.path.dirname(os.path.realpath(__file__))
            current_user_homedir = os.environ.get('HOME')

            # Check if the application is a Python package.
            if current_dir.startswith("/usr/local/lib/") == True or current_dir.startswith(current_user_homedir + "/.local/lib/") == True:
                # Run the function in a separate thread in order to avoid blocking the GUI because "pip ..." command runs about 1 seconds.
                from threading import Thread
                Thread(target=self.main_update_check_func, daemon=True).start()


    # ----------------------- Called for adapting to system color scheme on systems with newer versions than GTK3. -----------------------
    def main_gui_adapt_color_scheme_for_gtk4_based_systems_func(self):

        gi.require_version('Gio', '2.0')
        from gi.repository import Gio

        schema_source =  Gio.SettingsSchemaSource.get_default()
        if_scheme_installed = Gio.SettingsSchemaSource.lookup(schema_source, "org.gnome.desktop.interface", False)

        # Check if "org.gnome.desktop.interface" scheme ("gsettings-desktop-schemas" package) is installed on the system. It gives error, it can not be prevent by using "try-except" and GUI is not shown if it is not installed.
        if if_scheme_installed != None:
            gio_settings = Gio.Settings.new("org.gnome.desktop.interface")
            # Check if "color-scheme" is in the settings. This value is not in the settings if the system uses a desktop environment based on GTK4. It gives error, it can not be prevent by using "try-except" and GUI is not shown if it is not installed.
            if "color-scheme" in gio_settings:
                system_scheme = gio_settings.get_string("color-scheme")
                # Switch to dark theme if the system uses it.
                if system_scheme == "prefer-dark":
                    Gtk.Settings.get_default().props.gtk_application_prefer_dark_theme = True


    # ----------------------- Check if there is a newer version on PyPI -----------------------
    def main_update_check_func(self):

        import time, subprocess

        # Wait 5 seconds before running the command in order to avoid high CPU usage at the beginning of the measurement.
        time.sleep(5)

        # Run the command to get installed and latest versions of the application.
        try:
            pip_index_output = (subprocess.check_output(["pip", "index", "versions", "system-monitoring-center"], stderr=subprocess.STDOUT, shell=False)).decode().strip().split("\n")
        except Exception:
            return

        # Get installed and latest versions of the application by processing the command output.
        current_version = "-"
        last_version = "-"
        for line in pip_index_output:
            if "INSTALLED" in line:
                current_version = line.split("INSTALLED:")[1].strip()
            if "LATEST" in line:
                last_version = line.split("LATEST:")[1].strip()

        # Show an information label with a green background just below the headerbar if there is a newer version on PyPI.
        if current_version != last_version:
            # Show the notification information on the label by using "GLib.idle_add" in order to avoid problems (bugs, data corruption, etc.) because of threading (GTK is not thread-safe).
            GLib.idle_add(self.main_update_check_gui_notification_func)


    # ----------------------- Show a notification label on the GUI if there is a newer version on PyPI -----------------------
    def main_update_check_gui_notification_func(self):

        # Generate a new label for the information. This label does not exist in the ".ui" UI file.
        label_new_version_information = Gtk.Label(label=_tr("There is a newer version on PyPI."))
        css = b"label {background: rgba(24%,70%,45%,1.0);}"
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        label_new_version_information.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.grid10.insert_row(0)
        # Attach the label to the grid at (0, 0) position.
        self.grid10.attach(label_new_version_information, 0, 0, 1, 1)
        label_new_version_information.set_visible(True)


    # ----------------------- "Main Menu" Button -----------------------
    def on_button1_clicked(self, widget):

        from MainMenusDialogs import MainMenusDialogs
        MainMenusDialogs.popover1001p.set_relative_to(widget)
        MainMenusDialogs.popover1001p.set_position(Gtk.PositionType.BOTTOM)
        MainMenusDialogs.popover1001p.popup()


    # ----------------------- "Performance, Processes, Users, Services, System, CPU, Memory, Disk, Network, GPU, Sensors" Radiobuttons -----------------------
    def on_main_gui_tab_radiobuttons_toggled(self, widget):

        if widget.get_active() == True:
            self.main_gui_tab_switch_func()


    # ----------------------------------- MainGUI - Default Tab Function (switches to default tab on initial run) -----------------------------------
    def main_gui_default_tab_func(self):

        default_main_tab = Config.default_main_tab
        if default_main_tab == 0:
             self.radiobutton1.set_active(True)
        elif default_main_tab == 1:
             self.radiobutton2.set_active(True)
        elif default_main_tab == 2:
             self.radiobutton3.set_active(True)
        elif default_main_tab == 3:
             self.radiobutton6.set_active(True)
        elif default_main_tab == 4:
             self.radiobutton8.set_active(True)

        performance_tab_default_sub_tab = Config.performance_tab_default_sub_tab
        if performance_tab_default_sub_tab == 0:
             self.radiobutton1007.set_active(True)
        elif performance_tab_default_sub_tab == 1:
             self.radiobutton1001.set_active(True)
        elif performance_tab_default_sub_tab == 2:
             self.radiobutton1002.set_active(True)
        elif performance_tab_default_sub_tab == 3:
             self.radiobutton1003.set_active(True)
        elif performance_tab_default_sub_tab == 4:
             self.radiobutton1004.set_active(True)
        elif performance_tab_default_sub_tab == 5:
             self.radiobutton1005.set_active(True)
        elif performance_tab_default_sub_tab == 6:
             self.radiobutton1006.set_active(True)


    # ----------------------------------- MainGUI - Main Function Run Function (runs main functions (Performance, Processes, etc.) when their stack page is selected) -----------------------------------
    def main_gui_tab_switch_func(self):

        # Local definition of this variable is made for lower CPU usage becuse this variable is used multiple times.
        remember_last_opened_tabs_on_application_start = Config.remember_last_opened_tabs_on_application_start

        # Switch to "Performance" tab
        if self.radiobutton1.get_active() == True:
            self.stack1.set_visible_child(self.grid1)
            if remember_last_opened_tabs_on_application_start == 1:
                # No need to save Config values after this value is defined. Because save operation is performed for Performance tab sub-tabs (CPU, Memory, Disk, Network, GPU, Sensors tabs).
                Config.default_main_tab = 0
            # This value is used in order to detect the current tab without checking GUI obejects for lower CPU usage. This value is not saved.
            Config.current_main_tab = 0

            # Switch to "Summary" tab
            if self.radiobutton1007.get_active() == True:
                self.stack1001.set_visible_child(self.grid1007)
                if remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 0
                    Config.config_save_func()
                # This value is used in order to detect the current tab without checking GUI obejects for lower CPU usage. This value is not saved.
                Config.performance_tab_current_sub_tab = 0
                # Attach the grid to the grid (on the Main Window) at (0, 0) position if not attached.
                if self.grid1007.get_child_at(0,0) == None:
                    global Summary
                    from Summary import Summary
                    self.grid1007.attach(Summary.grid1701, 0, 0, 1, 1)
                # Run initial function of the module if this is the first loop of the module.
                if Summary.initial_already_run == 0:
                    GLib.idle_add(Summary.summary_initial_func)
                # Run loop Summary loop function in order to get data without waiting update interval.
                GLib.idle_add(Summary.summary_loop_func)
                # Show device selection list on a listbox between radiobuttons of Performance tab sub-tabs.
                self.main_gui_device_selection_list_func()
                return

            # Switch to "CPU" tab
            if self.radiobutton1001.get_active() == True:
                self.stack1001.set_visible_child(self.grid1001)
                if remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 1
                    Config.config_save_func()
                # This value is used in order to detect the current tab without checking GUI obejects for lower CPU usage. This value is not saved.
                Config.performance_tab_current_sub_tab = 1
                # Attach the grid to the grid (on the Main Window) at (0, 0) position if not attached.
                if self.grid1001.get_child_at(0,0) == None:
                    global Cpu
                    from Cpu import Cpu
                    self.grid1001.attach(Cpu.grid1101, 0, 0, 1, 1)
                # Run initial function of the module if this is the first loop of the module.
                if Cpu.initial_already_run == 0:
                    GLib.idle_add(Cpu.cpu_initial_func)
                # Run loop Cpu loop function in order to get data without waiting update interval.
                GLib.idle_add(Cpu.cpu_loop_func)
                # Show device selection list on a listbox between radiobuttons of Performance tab sub-tabs.
                self.main_gui_device_selection_list_func()
                return

            # Switch to "Memory" tab
            elif self.radiobutton1002.get_active() == True:
                self.stack1001.set_visible_child(self.grid1002)
                if remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 2
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 2
                if self.grid1002.get_child_at(0,0) == None:
                    global Memory
                    from Memory import Memory
                    self.grid1002.attach(Memory.grid1201, 0, 0, 1, 1)
                if Memory.initial_already_run == 0:
                    GLib.idle_add(Memory.memory_initial_func)
                GLib.idle_add(Memory.memory_loop_func)
                self.main_gui_device_selection_list_func()
                return

            # Switch to "Disk" tab
            elif self.radiobutton1003.get_active() == True:
                self.stack1001.set_visible_child(self.grid1003)
                if remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 3
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 3
                if self.grid1003.get_child_at(0,0) == None:
                    global Disk
                    from Disk import Disk
                    self.grid1003.attach(Disk.grid1301, 0, 0, 1, 1)
                if Disk.initial_already_run == 0:
                    GLib.idle_add(Disk.disk_initial_func)
                GLib.idle_add(Disk.disk_loop_func)
                self.main_gui_device_selection_list_func()
                return

            # Switch to "Network" tab
            elif self.radiobutton1004.get_active() == True:
                self.stack1001.set_visible_child(self.grid1004)
                if remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 4
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 4
                if self.grid1004.get_child_at(0,0) == None:
                    global Network
                    from Network import Network
                    self.grid1004.attach(Network.grid1401, 0, 0, 1, 1)
                if Network.initial_already_run == 0:
                    GLib.idle_add(Network.network_initial_func)
                GLib.idle_add(Network.network_loop_func)
                self.main_gui_device_selection_list_func()
                return

            # Switch to "GPU" tab
            elif self.radiobutton1005.get_active() == True:
                self.stack1001.set_visible_child(self.grid1005)
                if remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 5
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 5
                if self.grid1005.get_child_at(0,0) == None:
                    global Gpu
                    from Gpu import Gpu
                    self.grid1005.attach(Gpu.grid1501, 0, 0, 1, 1)
                if Gpu.initial_already_run == 0:
                    GLib.idle_add(Gpu.gpu_initial_func)
                GLib.idle_add(Gpu.gpu_loop_func)
                try:
                    self.main_gui_device_selection_list_func()
                except AttributeError:
                    pass
                return

            # Switch to "Sensors" tab
            elif self.radiobutton1006.get_active() == True:
                self.stack1001.set_visible_child(self.grid1006)
                if remember_last_opened_tabs_on_application_start == 1:
                    Config.performance_tab_default_sub_tab = 6
                    Config.config_save_func()
                Config.performance_tab_current_sub_tab = 6
                if 'Sensors' not in globals():
                    global Sensors
                    import Sensors
                    Sensors.sensors_import_func()
                    Sensors.sensors_gui_func()
                    self.grid1006.attach(Sensors.grid1601, 0, 0, 1, 1)
                if Sensors.initial_already_run == 0:
                    Sensors.sensors_initial_func()
                Sensors.sensors_loop_func()
                self.main_gui_device_selection_list_func()
                return

        # Switch to "Processes" tab
        elif self.radiobutton2.get_active() == True:
            self.stack1.set_visible_child(self.grid2)
            if remember_last_opened_tabs_on_application_start == 1:
                Config.default_main_tab = 1
                Config.config_save_func()
            Config.current_main_tab = 1
            if 'Processes' not in globals():
                global Processes
                import Processes
                Processes.processes_import_func()
                Processes.processes_gui_func()
                self.grid2.attach(Processes.grid2101, 0, 0, 1, 1)
            if Processes.initial_already_run == 0:
                Processes.processes_initial_func()
            Processes.processes_loop_func()
            return

        # Switch to "Users" tab
        elif self.radiobutton3.get_active() == True:
            self.stack1.set_visible_child(self.grid3)
            if remember_last_opened_tabs_on_application_start == 1:
                Config.default_main_tab = 2
                Config.config_save_func()
            Config.current_main_tab = 2
            if 'Users' not in globals():
                global Users
                import Users
                Users.users_import_func()
                Users.users_gui_func()
                self.grid3.attach(Users.grid3101, 0, 0, 1, 1)
            if Users.initial_already_run == 0:
                Users.users_initial_func()
            Users.users_loop_func()
            return

        # Switch to "Services" tab
        elif self.radiobutton6.get_active() == True:
            self.stack1.set_visible_child(self.grid6)
            if remember_last_opened_tabs_on_application_start == 1:
                Config.default_main_tab = 3
                Config.config_save_func()
            Config.current_main_tab = 3
            if 'Services' not in globals():
                global Services
                import Services
                Services.services_import_func()
                Services.services_gui_func()
                self.grid6.attach(Services.grid6101, 0, 0, 1, 1)
            if Services.initial_already_run == 0:
                Services.services_initial_func()
            return

        # Switch to "System" tab
        elif self.radiobutton8.get_active() == True:
            self.stack1.set_visible_child(self.grid8)
            if remember_last_opened_tabs_on_application_start == 1:
                Config.default_main_tab = 4
                Config.config_save_func()
            Config.current_main_tab = 4
            if self.grid8.get_child_at(0,0) == None:
                global System
                from System import System
                self.grid8.attach(System.grid8101, 0, 0, 1, 1)
            if System.initial_already_run == 0:
                GLib.idle_add(System.system_initial_func)
            return


    # ----------------------- Add device list into listbox between the Performance tab sub-tab radiobuttons -----------------------
    def main_gui_device_selection_list_func(self):

        # Delete previous scrolledwindow and widgets in it in order to add new one again. Otherwise, removing all of the listbox rows requires removing them one by one.
        try:
            self.scrolledwindow1001.destroy()
        # Prevent error if this is the first tab switch and there is no scrolledwindow.
        except AttributeError:
            pass

        # Define variables for device list, selected device number and row number to be used for adding scrolledwindow into the grid.
        performance_tab_current_sub_tab = Config.performance_tab_current_sub_tab
        # Check if Summary tab is selected.
        if performance_tab_current_sub_tab == 0:
            device_list = [_tr("Summary")]
            selected_device_number = 0
            listbox_row_number = 1
            tooltip_text = ""

        # Check if CPU tab is selected.
        elif performance_tab_current_sub_tab == 1:
            device_list = Performance.logical_core_list_system_ordered
            selected_device_number = Performance.selected_cpu_core_number
            listbox_row_number = 3
            tooltip_text = _tr("CPU core selection affects only frequency and cache memory information.")

        # Check if Memory tab is selected.
        elif performance_tab_current_sub_tab == 2:
            device_list = [_tr("RAM") + "-" + _tr("Swap Memory")]
            selected_device_number = 0
            listbox_row_number = 5
            tooltip_text = ""

        # Check if Disk tab is selected.
        elif performance_tab_current_sub_tab == 3:
            device_list_full = Performance.disk_list_system_ordered
            device_list = []
            for device in device_list_full:
                # Do not add the device into the listbox and skip to the next loop if "hide_loop_ramdisk_zram_disks" option is enabled and device is a loop, ramdisk or zram device.
                if Config.hide_loop_ramdisk_zram_disks == 1:
                    if device.startswith("loop") == True or device.startswith("ram") == True or device.startswith("zram") == True:
                        continue
                device_list.append(device)
            # "selected_device_number" for Disk tab is get in a different way. Because device list may be changed if "hide_loop_ramdisk_zram_disks" option is enabled.
            selected_device_number = device_list.index(Performance.disk_list_system_ordered[Performance.selected_disk_number])
            listbox_row_number = 7
            tooltip_text = ""

        # Check if Network tab is selected.
        elif performance_tab_current_sub_tab == 4:
            device_list = Performance.network_card_list
            selected_device_number = Performance.selected_network_card_number
            listbox_row_number = 9
            tooltip_text = ""

        # Check if GPU tab is selected.
        elif performance_tab_current_sub_tab == 5:
            device_list = Gpu.gpu_list
            selected_device_number = Gpu.selected_gpu_number
            listbox_row_number = 11
            tooltip_text = ""

        # Check if Sensors tab is selected.
        elif performance_tab_current_sub_tab == 6:
            return

        # Generate new widgets.
        self.scrolledwindow1001 = Gtk.ScrolledWindow()
        scrolledwindow1001 = self.scrolledwindow1001
        viewport1001 = Gtk.Viewport()
        listbox1001 = Gtk.ListBox()

        # Set properties of the scrolledwindow.
        scrolledwindow1001.set_size_request(-1, 130)
        scrolledwindow1001.set_margin_left(8)
        scrolledwindow1001.set_tooltip_text(tooltip_text)

        # Run function when a row is clicked on the listbox.
        def on_row_activated(widget, row):

            # Get selected device name.
            selected_device = device_list[row.get_index()]

            # Check if Summary tab is selected.
            if performance_tab_current_sub_tab == 0:
                pass

            # Check if CPU tab is selected.
            elif performance_tab_current_sub_tab == 1:
                # Set selected device.
                Config.selected_cpu_core = selected_device
                Performance.performance_set_selected_cpu_core_func()

                # Apply changes immediately (without waiting update interval).
                Cpu.cpu_initial_func()
                Cpu.cpu_loop_func()
                Config.config_save_func()

            # Check if Memory tab is selected.
            elif performance_tab_current_sub_tab == 2:
                pass

            # Check if Disk tab is selected.
            elif performance_tab_current_sub_tab == 3:
                Config.selected_disk = selected_device
                Performance.performance_set_selected_disk_func()

                # Apply changes immediately (without waiting update interval).
                Disk.disk_initial_func()
                Disk.disk_loop_func()
                Config.config_save_func()

            # Check if Network tab is selected.
            elif performance_tab_current_sub_tab == 4:
                Config.selected_network_card = selected_device
                Performance.performance_set_selected_network_card_func()

                # Apply changes immediately (without waiting update interval).
                Network.network_initial_func()
                Network.network_loop_func()
                Config.config_save_func()

            # Check if GPU tab is selected.
            elif performance_tab_current_sub_tab == 5:
                Config.selected_gpu = selected_device
                Gpu.gpu_get_gpu_list_and_boot_vga_func()

                # Apply changes immediately (without waiting update interval).
                Gpu.gpu_initial_func()
                Gpu.gpu_loop_func()
                Config.config_save_func()

            # Check if Sensors tab is selected.
            elif performance_tab_current_sub_tab == 6:
                pass

        # Add devices into listbox.
        for device in device_list:
            row = Gtk.ListBoxRow()
            grid = Gtk.Grid()
            label = Gtk.Label()
            label.set_label(device)
            grid.attach(label, 0, 0, 1, 1)
            # Also add disk usage percentage label next to device name if this is Disk tab.
            if performance_tab_current_sub_tab == 3:
                disk_mount_point = Disk.disk_mount_point_func(device)
                _, _, _, _, _, disk_usage_percent = Disk.disk_disk_capacity_size_available_free_used_usage_percent_func(disk_mount_point)
                label = Gtk.Label()
                label.set_sensitive(False)
                if disk_mount_point == "-":
                    label.set_label(f'  (-%)')
                else:
                    label.set_label(f'  ({disk_usage_percent:.0f}%)')
                grid.attach(label, 1, 0, 1, 1)
            row.add(grid)
            listbox1001.add(row)

        # Connect signal for the listbox.
        listbox1001.connect("row-activated", on_row_activated)

        # Add widgets into the grid in main GUI module.
        viewport1001.add(listbox1001)
        scrolledwindow1001.add(viewport1001)
        self.grid1010.attach(scrolledwindow1001, 0, listbox_row_number, 1, 1)
        try:
            listbox1001.select_row(listbox1001.get_children()[selected_device_number])
        # Prevent error if a disk is hidden by changing the relevant option while it was selected. There is no need to update the list from this function because it will be set as hidden in the list by another function (in Disk module) immediately.
        except IndexError:
            pass
        scrolledwindow1001.show_all()


    # ----------------------- Called for running loop functions of opened tabs to get data -----------------------
    # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to change the update interval and run the loop again without waiting ending the previous update interval.
    def main_gui_tab_loop_func(self, *args):

        # Destroy GLib source for preventing it repeating the function.
        try:
            self.main_glib_source.destroy()
        # "try-except" is used in order to prevent errors if this is first run of the function.
        except AttributeError:
            pass
        self.main_glib_source = GLib.timeout_source_new(Config.update_interval * 1000)

        current_main_tab = Config.current_main_tab
        performance_tab_current_sub_tab = Config.performance_tab_current_sub_tab

        Performance.performance_background_loop_func()

        if Config.performance_summary_on_the_headerbar == 1:
            from PerformanceSummaryHeaderbar import PerformanceSummaryHeaderbar
            GLib.idle_add(PerformanceSummaryHeaderbar.performance_summary_headerbar_loop_func)

        if current_main_tab == 0:
            if performance_tab_current_sub_tab == 0:
                GLib.idle_add(Summary.summary_loop_func)
            elif performance_tab_current_sub_tab == 1:
                GLib.idle_add(Cpu.cpu_loop_func)
            elif performance_tab_current_sub_tab == 2:
                GLib.idle_add(Memory.memory_loop_func)
            elif performance_tab_current_sub_tab == 3:
                GLib.idle_add(Disk.disk_loop_func)
            elif performance_tab_current_sub_tab == 4:
                GLib.idle_add(Network.network_loop_func)
            elif performance_tab_current_sub_tab == 5:
                GLib.idle_add(Gpu.gpu_loop_func)
            elif performance_tab_current_sub_tab == 6:
                GLib.idle_add(Sensors.sensors_loop_func)
        if current_main_tab == 1:
            GLib.idle_add(Processes.processes_loop_func)
        if current_main_tab == 2:
            GLib.idle_add(Users.users_loop_func)

        self.main_glib_source.set_callback(self.main_gui_tab_loop_func)
        # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
        self.main_glib_source.attach(GLib.MainContext.default())


    # ----------------------- Called for copying files for GUI icons and application shortcut (.desktop file) in user folders if they are not copied before. -----------------------
    def main_gui_application_system_integration_func(self):

        # Called for removing files.
        def remove_file(file):
            try:
                os.remove(file)
            except Exception:
                pass

        # Called for generating folders.
        def generate_folder(folder):
            try:
                os.makedirs(folder)
            except Exception:
                pass

        # Called for copying files.
        def copy_file(source, target):
            try:
                shutil.copy2(source, target)
            except Exception:
                pass

        # Get current directory (which code of this application is in) and current user home directory (files will be copied in).
        current_dir = os.path.dirname(os.path.realpath(__file__))
        current_user_homedir = os.environ.get('HOME')

        # Define folder list in the home directory for copying files in it.
        home_dir_folder_list = [current_user_homedir + "/.local/share/applications/",
                                current_user_homedir + "/.local/share/icons/hicolor/scalable/actions/",
                                current_user_homedir + "/.local/share/icons/hicolor/scalable/apps/"]

        # Generate folders to copy files in them if they are not generated before.
        for folder in home_dir_folder_list:
            if os.path.isdir(folder) == False:
                generate_folder(folder)

        # Get icon file paths in the home directory.
        icon_list_actions = [current_user_homedir + "/.local/share/icons/hicolor/scalable/actions/" + file for file in os.listdir(current_user_homedir + "/.local/share/icons/hicolor/scalable/actions/") if file.startswith("system-monitoring-center-")]
        icon_list_apps = [current_user_homedir + "/.local/share/icons/hicolor/scalable/apps/" + file for file in os.listdir(current_user_homedir + "/.local/share/icons/hicolor/scalable/apps/") if file.startswith("system-monitoring-center.svg")]
        icon_list_home = sorted(icon_list_actions + icon_list_apps)

        # Get icon file paths in the installation directory. These files are copied under this statement in order to avoid copying them if this is a system package which copies GUI images into "/usr/share/icons/..." folder during installation.
        try:
            icon_list_actions = [current_dir + "/../icons/hicolor/scalable/actions/" + file for file in os.listdir(current_dir + "/../icons/hicolor/scalable/actions/") if file.startswith("system-monitoring-center-")]
            icon_list_apps = [current_dir + "/../icons/hicolor/scalable/apps/" + file for file in os.listdir(current_dir + "/../icons/hicolor/scalable/apps/") if file.startswith("system-monitoring-center.svg")]
            icon_list_current = sorted(icon_list_actions + icon_list_apps)

            # Copy .desktop file if it is not copied before.
            if os.path.isfile(current_user_homedir + "/.local/share/applications/com.github.hakand34.system-monitoring-center.desktop") == False:
                # Try to remove if there is a broken symlink of the file (symlink was generated in previous versions of the application).
                remove_file(current_user_homedir + "/.local/share/applications/com.github.hakand34.system-monitoring-center.desktop")
                # Import module for copying files
                import shutil
                copy_file(current_dir + "/../integration/com.github.hakand34.system-monitoring-center.desktop", current_user_homedir + "/.local/share/applications/")
        except Exception:
            icon_list_current = []

        # Check if number of icon files are different. Remove the files in the home directory and copy the files in the installation directory if they are different.
        if len(icon_list_home) != len(icon_list_current):

            # Import module for copying files
            import shutil

            for file in icon_list_home:
                remove_file(file)

            for file in icon_list_current:
                copy_file(file, current_user_homedir + "/.local/share/icons/hicolor/scalable/" + file.split("/")[-2] + "/")


# Generate object
MainGUI = MainGUI()


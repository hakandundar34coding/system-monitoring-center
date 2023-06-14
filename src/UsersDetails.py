import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gtk, GLib

import os
import time
import subprocess
from datetime import datetime

from locale import gettext as _tr

from .Config import Config
from .Users import Users
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common


class UsersDetails:

    def __init__(self):

        self.window_gui()


    def window_gui(self):
        """
        Generate window GUI.
        """

        # Window
        self.user_details_window = Gtk.Window()
        self.user_details_window.set_default_size(350, 330)
        self.user_details_window.set_title(_tr("User"))
        self.user_details_window.set_icon_name("system-monitoring-center")
        self.user_details_window.set_transient_for(MainWindow.main_window)
        self.user_details_window.set_modal(True)
        self.user_details_window.set_hide_on_close(True)

        self.main_tab_gui()

        self.gui_signals()


    def main_tab_gui(self):
        """
        Generate labels on the main (single) tab.
        """

        # ScrolledWindow
        scrolledwindow = Common.window_main_scrolledwindow()
        self.user_details_window.set_child(scrolledwindow)

        # Viewport
        viewport = Gtk.Viewport()
        scrolledwindow.set_child(viewport)

        # Grid
        grid = Common.window_main_grid()
        scrolledwindow.set_child(grid)

        # Label (User)
        label = Common.static_information_label(_tr("User"))
        grid.attach(label, 0, 0, 1, 1)
        # Label (User)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 0, 1, 1)
        # Label (User)
        self.user_label = Common.dynamic_information_label()
        grid.attach(self.user_label, 2, 0, 1, 1)

        # Label (Full Name)
        label = Common.static_information_label(_tr("Full Name"))
        grid.attach(label, 0, 1, 1, 1)
        # Label (Full Name)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 1, 1, 1)
        # Label (Full Name)
        self.full_name_label = Common.dynamic_information_label()
        grid.attach(self.full_name_label, 2, 1, 1, 1)

        # Label (Logged In)
        label = Common.static_information_label(_tr("Logged In"))
        grid.attach(label, 0, 2, 1, 1)
        # Label (Logged In)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 2, 1, 1)
        # Label (Logged In)
        self.logged_in_label = Common.dynamic_information_label()
        grid.attach(self.logged_in_label, 2, 2, 1, 1)

        # Label (UID)
        label = Common.static_information_label(_tr("UID"))
        grid.attach(label, 0, 3, 1, 1)
        # Label (UID)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 3, 1, 1)
        # Label (UID)
        self.uid_label = Common.dynamic_information_label()
        grid.attach(self.uid_label, 2, 3, 1, 1)

        # Label (GID)
        label = Common.static_information_label(_tr("GID"))
        grid.attach(label, 0, 4, 1, 1)
        # Label (GID)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 4, 1, 1)
        # Label (GID)
        self.gid_label = Common.dynamic_information_label()
        grid.attach(self.gid_label, 2, 4, 1, 1)

        # Label (Processes)
        label = Common.static_information_label(_tr("Processes"))
        grid.attach(label, 0, 5, 1, 1)
        # Label (Processes)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 5, 1, 1)
        # Label (Processes)
        self.processes_label = Common.dynamic_information_label()
        grid.attach(self.processes_label, 2, 5, 1, 1)

        # Label (Home Directory)
        label = Common.static_information_label(_tr("Home Directory"))
        grid.attach(label, 0, 6, 1, 1)
        # Label (Home Directory)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 6, 1, 1)
        # Label (Home Directory)
        self.home_directory_label = Common.dynamic_information_label()
        grid.attach(self.home_directory_label, 2, 6, 1, 1)

        # Label (Group)
        label = Common.static_information_label(_tr("Group"))
        grid.attach(label, 0, 7, 1, 1)
        # Label (Group)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 7, 1, 1)
        # Label (Group)
        self.group_label = Common.dynamic_information_label()
        grid.attach(self.group_label, 2, 7, 1, 1)

        # Label (Terminal)
        label = Common.static_information_label(_tr("Terminal"))
        grid.attach(label, 0, 8, 1, 1)
        # Label (Terminal)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 8, 1, 1)
        # Label (Terminal)
        self.terminal_label = Common.dynamic_information_label()
        grid.attach(self.terminal_label, 2, 8, 1, 1)

        # Label (Start Time)
        label = Common.static_information_label(_tr("Start Time"))
        grid.attach(label, 0, 9, 1, 1)
        # Label (Start Time)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 9, 1, 1)
        # Label (Start Time)
        self.start_time_label = Common.dynamic_information_label()
        grid.attach(self.start_time_label, 2, 9, 1, 1)

        # Label (CPU)
        label = Common.static_information_label(_tr("CPU"))
        grid.attach(label, 0, 10, 1, 1)
        # Label (CPU)
        label = Common.static_information_label(":")
        grid.attach(label, 1, 10, 1, 1)
        # Label (CPU)
        self.cpu_label = Common.dynamic_information_label()
        grid.attach(self.cpu_label, 2, 10, 1, 1)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # Window signals
        self.user_details_window.connect("close-request", self.on_user_details_window_delete_event)
        self.user_details_window.connect("show", self.on_user_details_window_show)


    def on_user_details_window_delete_event(self, widget):
        """
        Called when window is closed.
        """

        self.update_window_value = 0
        self.user_details_window.set_visible(False)
        return True


    def on_user_details_window_show(self, widget):
        """
        Run code after window is shown.
        """

        try:
            # Delete "update_interval" variable in order to let the code to run initial function.
            # Otherwise, data from previous user (if it was viewed) will be used.
            del self.update_interval
        except AttributeError:
            pass

        # This value is checked for repeating the function for getting the user data.
        self.update_window_value = 1

        self.users_details_run_func()


    def users_details_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.users_data_dict_prev = {}

        self.system_boot_time = Common.get_system_boot_time()


    def users_details_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        # Get right clicked user UID and username
        selected_user_uid = Users.selected_user_uid
        selected_username = Users.selected_username

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        users_cpu_precision = Config.users_cpu_precision

        # Set window title
        self.user_details_window.set_title(_tr("User") + ": " + selected_username)

        # Get user information
        users_data_dict = Common.users_information(self.users_data_dict_prev, self.system_boot_time)
        self.users_data_dict_prev = dict(users_data_dict)
        human_user_uid_list = users_data_dict["human_user_uid_list"]

        try:
            user_data_dict = users_data_dict[selected_user_uid]
        # Prevent error if user account is deleted while its detail window is open.
        except KeyError:
            self.update_window_value = 0
            self.user_details_window.set_visible(False)
            return

        # Set label text
        self.user_label.set_label(user_data_dict["username"])
        self.full_name_label.set_label(user_data_dict["full_name"])
        if user_data_dict["logged_in"] == True:
            selected_user_logged_in = _tr("Yes")
        else:
            selected_user_logged_in = _tr("No")
        self.logged_in_label.set_label(selected_user_logged_in)
        self.uid_label.set_label(str(selected_user_uid))
        self.gid_label.set_label(str(user_data_dict["gid"]))
        self.processes_label.set_label(str(user_data_dict["process_count"]))
        self.home_directory_label.set_label(user_data_dict["home_dir"])
        self.group_label.set_label(user_data_dict["group_name"])
        self.terminal_label.set_label(user_data_dict["terminal"])
        selected_user_process_start_time = user_data_dict["log_in_time"]
        if selected_user_process_start_time != 0:
            self.start_time_label.set_label(datetime.fromtimestamp(selected_user_process_start_time).strftime("%H:%M:%S %d.%m.%Y"))
        if selected_user_process_start_time == 0:
            self.start_time_label.set_label("-")
        self.cpu_label.set_label(f'{user_data_dict["total_cpu_usage"]:.{users_cpu_precision}f} %')


    def users_details_run_func(self, *args):
        """
        Run initial and loop functions of user details window.
        "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()".
        "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to change the update interval and
        run the loop again without waiting ending the previous update interval.
        """

        if hasattr(UsersDetails, "update_interval") == False:
            GLib.idle_add(self.users_details_initial_func)

        # Destroy GLib source for preventing it repeating the function.
        try:
            self.main_glib_source.destroy()
        # "try-except" is used in order to prevent errors if this is first run of the function.
        except AttributeError:
            pass
        self.update_interval = Config.update_interval
        self.main_glib_source = GLib.timeout_source_new(self.update_interval * 1000)

        if self.update_window_value == 1:
            GLib.idle_add(self.users_details_loop_func)
            self.main_glib_source.set_callback(self.users_details_run_func)
            # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.
            self.main_glib_source.attach(GLib.MainContext.default())


UsersDetails = UsersDetails()


import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .Config import Config
from .Users import Users
from .MainWindow import MainWindow
from . import Common

_tr = Config._tr


class UsersMenu:

    def __init__(self):

        self.menu_gui()


    def menu_gui(self):
        """
        Generate menu GUI.
        """

        # Popover
        self.menu_po = Gtk.Popover()

        # Grid (main)
        main_grid = Common.menu_main_grid()
        self.menu_po.set_child(main_grid)

        # Label - menu title (Users)
        label = Common.menu_title_label(_tr("Users"))
        main_grid.attach(label, 0, 0, 1, 1)

        # Notebook
        notebook = Gtk.Notebook()
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)
        main_grid.attach(notebook, 0, 1, 1, 1)

        # Tab pages and ScrolledWindow
        # "Add/Remove Columns" tab
        label = Gtk.Label()
        label.set_label(_tr("Add/Remove Columns"))
        self.grid_add_remove_columns_tab = Gtk.Grid()
        self.grid_add_remove_columns_tab.set_margin_top(15)
        self.grid_add_remove_columns_tab.set_margin_bottom(5)
        self.grid_add_remove_columns_tab.set_margin_start(5)
        self.grid_add_remove_columns_tab.set_margin_end(5)
        self.grid_add_remove_columns_tab.set_row_spacing(5)
        notebook.append_page(self.grid_add_remove_columns_tab, label)

        # Button (Reset)
        self.reset_button = Common.reset_button()
        main_grid.attach(self.reset_button, 0, 2, 1, 1)

        # "Add/Remove Columns" tab GUI
        self.add_remove_columns_tab_gui()

        # GUI signals
        self.gui_signals()


    def add_remove_columns_tab_gui(self):
        """
        Generate "Add/Remove Columns" tab GUI objects.
        """

        # Grid
        grid = Gtk.Grid()
        grid.set_margin_top(5)
        grid.set_margin_bottom(5)
        grid.set_margin_start(5)
        grid.set_margin_end(5)
        grid.set_column_spacing(10)
        grid.set_row_spacing(3)
        self.grid_add_remove_columns_tab.attach(grid, 0, 0, 1, 1)

        # Label - tab title (Add/Remove Columns)
        label = Common.title_label(_tr("Add/Remove Columns"))
        grid.attach(label, 0, 0, 2, 1)

        # CheckButton (User)
        self.user_cb = Common.checkbutton(_tr("User"), None)
        self.user_cb.set_active(True)
        self.user_cb.set_sensitive(False)
        grid.attach(self.user_cb, 0, 1, 1, 1)

        # CheckButton (Full Name)
        self.full_name_cb = Common.checkbutton(_tr("Full Name"), None)
        grid.attach(self.full_name_cb, 0, 2, 1, 1)

        # CheckButton (Logged In)
        self.logged_in_cb = Common.checkbutton(_tr("Logged In"), None)
        grid.attach(self.logged_in_cb, 0, 3, 1, 1)

        # CheckButton (UID)
        self.uid_cb = Common.checkbutton(_tr("UID"), None)
        grid.attach(self.uid_cb, 0, 4, 1, 1)

        # CheckButton (GID)
        self.gid_cb = Common.checkbutton(_tr("GID"), None)
        grid.attach(self.gid_cb, 0, 5, 1, 1)

        # CheckButton (Processes)
        self.processes_cb = Common.checkbutton(_tr("Processes"), None)
        grid.attach(self.processes_cb, 0, 6, 1, 1)

        # CheckButton (Home Directory)
        self.home_directory_cb = Common.checkbutton(_tr("Home Directory"), None)
        grid.attach(self.home_directory_cb, 1, 1, 1, 1)

        # CheckButton (Group)
        self.group_cb = Common.checkbutton(_tr("Group"), None)
        grid.attach(self.group_cb, 1, 2, 1, 1)

        # CheckButton (Terminal)
        self.terminal_cb = Common.checkbutton(_tr("Terminal"), None)
        grid.attach(self.terminal_cb, 1, 3, 1, 1)

        # CheckButton (Start Time)
        self.start_time_cb = Common.checkbutton(_tr("Start Time"), None)
        grid.attach(self.start_time_cb, 1, 4, 1, 1)

        # CheckButton (CPU)
        self.cpu_cb = Common.checkbutton(_tr("CPU"), None)
        grid.attach(self.cpu_cb, 1, 5, 1, 1)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        self.menu_po.connect("show", self.on_menu_po_show)
        self.reset_button.connect("clicked", self.on_reset_button_clicked)


    def connect_signals(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.user_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.full_name_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.logged_in_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.uid_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.gid_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.processes_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.home_directory_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.group_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.terminal_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.start_time_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)
        self.cpu_cb.connect("toggled", self.on_add_remove_checkbuttons_toggled)


    def disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.user_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.full_name_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.logged_in_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.uid_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.gid_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.processes_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.home_directory_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.group_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.terminal_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.start_time_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)
        self.cpu_cb.disconnect_by_func(self.on_add_remove_checkbuttons_toggled)


    def on_menu_po_show(self, widget):
        """
        Run code when customizations menu popover is shown.
        """
 
        try:
            self.disconnect_signals()
        except TypeError:
            pass
        self.set_gui()
        self.connect_signals()


    def on_reset_button_clicked(self, widget):
        """
        Reset customizations.
        """

        # Load default settings
        Config.config_default_users_func()
        Config.config_save_func()

        Common.update_tab_and_menu_gui(self, Users)


    def on_add_remove_checkbuttons_toggled(self, widget):
        """
        Run a function for adding/removing columns to treeview.
        """

        self.add_remove_columns()


    def set_gui(self):
        """
        Set GUI items.
        """

        # Set GUI objects on Add/Remove Column tab
        if 0 in Config.users_treeview_columns_shown:
            self.user_cb.set_active(True)
        else:
            self.user_cb.set_active(False)
        if 1 in Config.users_treeview_columns_shown:
            self.full_name_cb.set_active(True)
        else:
            self.full_name_cb.set_active(False)
        if 2 in Config.users_treeview_columns_shown:
            self.logged_in_cb.set_active(True)
        else:
            self.logged_in_cb.set_active(False)
        if 3 in Config.users_treeview_columns_shown:
            self.uid_cb.set_active(True)
        else:
            self.uid_cb.set_active(False)
        if 4 in Config.users_treeview_columns_shown:
            self.gid_cb.set_active(True)
        else:
            self.gid_cb.set_active(False)
        if 5 in Config.users_treeview_columns_shown:
            self.processes_cb.set_active(True)
        else:
            self.processes_cb.set_active(False)
        if 6 in Config.users_treeview_columns_shown:
            self.home_directory_cb.set_active(True)
        else:
            self.home_directory_cb.set_active(False)
        if 7 in Config.users_treeview_columns_shown:
            self.group_cb.set_active(True)
        else:
            self.group_cb.set_active(False)
        if 8 in Config.users_treeview_columns_shown:
            self.terminal_cb.set_active(True)
        else:
            self.terminal_cb.set_active(False)
        if 9 in Config.users_treeview_columns_shown:
            self.start_time_cb.set_active(True)
        else:
            self.start_time_cb.set_active(False)
        if 10 in Config.users_treeview_columns_shown:
            self.cpu_cb.set_active(True)
        else:
            self.cpu_cb.set_active(False)


    def add_remove_columns(self):
        """
        Add/Remove columns to treeview.
        """

        Config.users_treeview_columns_shown = []

        if self.user_cb.get_active() == True:
            Config.users_treeview_columns_shown.append(0)
        if self.full_name_cb.get_active() == True:
            Config.users_treeview_columns_shown.append(1)
        if self.logged_in_cb.get_active() == True:
            Config.users_treeview_columns_shown.append(2)
        if self.uid_cb.get_active() == True:
            Config.users_treeview_columns_shown.append(3)
        if self.gid_cb.get_active() == True:
            Config.users_treeview_columns_shown.append(4)
        if self.processes_cb.get_active() == True:
            Config.users_treeview_columns_shown.append(5)
        if self.home_directory_cb.get_active() == True:
            Config.users_treeview_columns_shown.append(6)
        if self.group_cb.get_active() == True:
            Config.users_treeview_columns_shown.append(7)
        if self.terminal_cb.get_active() == True:
            Config.users_treeview_columns_shown.append(8)
        if self.start_time_cb.get_active() == True:
            Config.users_treeview_columns_shown.append(9)
        if self.cpu_cb.get_active() == True:
            Config.users_treeview_columns_shown.append(10)

        # Apply changes immediately (without waiting update interval).
        Common.treeview_column_order_width_row_sorting(None, None, Users)

        Common.save_tab_settings(Users)


UsersMenu = UsersMenu()


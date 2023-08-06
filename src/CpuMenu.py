import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Gdk

from .Config import Config
from .Cpu import Cpu
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common

_tr = Config._tr


class CpuMenu:

    def __init__(self):

        self.name = "CpuMenu"

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

        # Label - menu title (CPU)
        label = Common.menu_title_label(_tr("CPU"))
        main_grid.attach(label, 0, 0, 1, 1)

        # Label (Graph - Show)
        label = Common.title_label(_tr("Graph - Show"))
        main_grid.attach(label, 0, 1, 1, 1)

        # CheckButton (CPU Usage (Average))
        self.cpu_usage_average_cb = Common.checkbutton(_tr("CPU Usage (Average)"), None)
        main_grid.attach(self.cpu_usage_average_cb, 0, 2, 1, 1)

        # CheckButton (CPU Usage (Per Core))
        self.cpu_usage_per_core_cb = Common.checkbutton(_tr("CPU Usage (Per Core)"), self.cpu_usage_average_cb)
        main_grid.attach(self.cpu_usage_per_core_cb, 0, 3, 1, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 4, 1, 1)

        # CheckButton (Show processes using max CPU)
        self.show_processes_using_max_cpu_cb = Common.checkbutton(_tr("Show processes using max CPU"), None)
        main_grid.attach(self.show_processes_using_max_cpu_cb, 0, 5, 1, 1)

        # Label (This increases CPU usage.)
        label = Common.static_information_label(_tr("This increases CPU usage."))
        label.set_margin_start(25)
        main_grid.attach(label, 0, 6, 1, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 7, 1, 1)

        # Button (Graph Color)
        self.graph_color_button = Common.graph_color_button(self)
        main_grid.attach(self.graph_color_button, 0, 8, 1, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 9, 1, 1)

        # Label - title (Precision)
        label = Common.title_label(_tr("Precision"))
        main_grid.attach(label, 0, 10, 1, 1)

        # Label - precision (CPU)
        label = Gtk.Label()
        label.set_label(_tr("CPU"))
        label.set_halign(Gtk.Align.CENTER)
        main_grid.attach(label, 0, 11, 1, 1)

        # DropDown - precision (CPU)
        item_list = ['0', '0.0', '0.00', '0.000']
        self.cpu_precision_dd = Common.dropdown_and_model(item_list)
        main_grid.attach(self.cpu_precision_dd, 0, 12, 1, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 13, 1, 1)

        # Label (Cache)
        label = Common.title_label(_tr("Cache"))
        main_grid.attach(label, 0, 14, 1, 1)

        # CheckButton (CPU Usage (Average))
        self.cpu_cache_socket_cb = Common.checkbutton(_tr("Socket"), None)
        main_grid.attach(self.cpu_cache_socket_cb, 0, 15, 1, 1)

        # CheckButton (CPU Usage (Per Core))
        self.cpu_cache_core_cb = Common.checkbutton(_tr("Selected Core"), self.cpu_cache_socket_cb)
        main_grid.attach(self.cpu_cache_core_cb, 0, 16, 1, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 17, 1, 1)

        # Button (Reset)
        self.reset_button = Common.reset_button()
        main_grid.attach(self.reset_button, 0, 18, 1, 1)

        # Connect signals
        self.menu_po.connect("show", self.on_menu_po_show)
        self.reset_button.connect("clicked", self.on_reset_button_clicked)


    def connect_signals(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.cpu_usage_average_cb.connect("toggled", self.on_cpu_usage_cb_toggled)
        self.cpu_usage_per_core_cb.connect("toggled", self.on_cpu_usage_cb_toggled)
        self.cpu_precision_dd.connect("notify::selected-item", self.on_selected_item_notify)
        self.show_processes_using_max_cpu_cb.connect("toggled", self.on_show_processes_using_max_cpu_cb_toggled)
        self.cpu_cache_socket_cb.connect("toggled", self.on_cpu_cache_cb_toggled)
        self.cpu_cache_core_cb.connect("toggled", self.on_cpu_cache_cb_toggled)


    def disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.cpu_usage_average_cb.disconnect_by_func(self.on_cpu_usage_cb_toggled)
        self.cpu_usage_per_core_cb.disconnect_by_func(self.on_cpu_usage_cb_toggled)
        self.cpu_precision_dd.disconnect_by_func(self.on_selected_item_notify)
        self.show_processes_using_max_cpu_cb.disconnect_by_func(self.on_show_processes_using_max_cpu_cb_toggled)
        self.cpu_cache_socket_cb.disconnect_by_func(self.on_cpu_cache_cb_toggled)
        self.cpu_cache_core_cb.disconnect_by_func(self.on_cpu_cache_cb_toggled)


    def on_menu_po_show(self, widget):
        """
        Run code when menu is shown.
        """

        try:
            self.disconnect_signals()
        except TypeError:
            pass
        self.set_gui()
        self.connect_signals()


    def on_cpu_usage_cb_toggled(self, widget):
        """
        Change CPU usage type.
        """

        if widget.get_active() == True:
            if widget == self.cpu_usage_average_cb:
                Config.show_cpu_usage_per_core = 0
                self.show_processes_using_max_cpu_cb.set_sensitive(True)
            if widget == self.cpu_usage_per_core_cb:
                Config.show_cpu_usage_per_core = 1
                self.show_processes_using_max_cpu_cb.set_sensitive(False)

        Common.save_tab_settings(Cpu)


    def on_selected_item_notify(self, widget, parameter):
        """
        Change CPU usage percent precision.
        Notify signal is sent when DropDown widget selection is changed.
        Currently GtkExpression parameter for DropDown can not be used because of PyGObject.
        """

        Config.performance_cpu_usage_percent_precision = widget.get_selected()

        Common.save_tab_settings(Cpu)


    def on_show_processes_using_max_cpu_cb_toggled(self, widget):
        """
        Show/Hide processes that consume max CPU resources.
        """

        if widget.get_active() == True:
            Config.show_processes_using_max_cpu = 1
        else:
            Config.show_processes_using_max_cpu = 0

        Common.save_tab_settings(Cpu)


    def on_cpu_cache_cb_toggled(self, widget):
        """
        Show CPU cache memory values per socket/core.
        """

        if widget.get_active() == True:
            if widget == self.cpu_cache_socket_cb:
                Config.show_cpu_cache_type = "socket"
            if widget == self.cpu_cache_core_cb:
                Config.show_cpu_cache_type = "core"

        Common.save_tab_settings(Cpu)


    def on_reset_button_clicked(self, widget):
        """
        Reset all tab settings.
        """

        # Load default settings
        Config.config_default_performance_cpu_func()
        Config.config_save_func()
        Performance.performance_set_selected_cpu_core_func()

        # Reset device list between Performance tab sub-tabs because selected device is reset.
        MainWindow.main_gui_device_selection_list()

        Common.update_tab_and_menu_gui(self, Cpu)


    def set_gui(self):
        """
        Set menu GUI items.
        """

        # Select checkbutton appropriate for CPU usage chart setting
        if Config.show_cpu_usage_per_core == 0:
            self.cpu_usage_average_cb.set_active(True)
            self.show_processes_using_max_cpu_cb.set_sensitive(True)
        if Config.show_cpu_usage_per_core == 1:
            self.cpu_usage_per_core_cb.set_active(True)
            self.show_processes_using_max_cpu_cb.set_sensitive(False)

        self.cpu_precision_dd.set_selected(Config.performance_cpu_usage_percent_precision)

        # Set active checkbutton if "Show processes using max CPU" option is enabled.
        if Config.show_processes_using_max_cpu == 1:
            self.show_processes_using_max_cpu_cb.set_active(True)
        if Config.show_processes_using_max_cpu == 0:
            self.show_processes_using_max_cpu_cb.set_active(False)

        # Select checkbutton appropriate for CPU cache type setting
        if Config.show_cpu_cache_type == "socket":
            self.cpu_cache_socket_cb.set_active(True)
        if Config.show_cpu_cache_type == "core":
            self.cpu_cache_core_cb.set_active(True)


CpuMenu = CpuMenu()


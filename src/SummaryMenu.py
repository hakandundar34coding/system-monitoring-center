import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .Config import Config
from .Summary import Summary
from . import Common

_tr = Config._tr


class SummaryMenu:

    def __init__(self):

        self.name = "SummaryMenu"

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

        # Label - menu title (Summary)
        label = Common.menu_title_label(_tr("Summary"))
        main_grid.attach(label, 0, 0, 2, 1)

        # Label (Graph - Show)
        label = Common.title_label(_tr("Graph - Show"))
        main_grid.attach(label, 0, 1, 2, 1)

        # CheckButton (GPU Usage)
        self.gpu_usage_cb = Common.checkbutton(_tr("GPU Usage"), None)
        main_grid.attach(self.gpu_usage_cb, 0, 2, 2, 1)

        # Label (This increases CPU usage.)
        label = Common.static_information_label(_tr("This increases CPU usage."))
        label.set_margin_start(25)
        main_grid.attach(label, 0, 3, 2, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 4, 2, 1)

        # Button (Reset)
        self.reset_button = Common.reset_button()
        main_grid.attach(self.reset_button, 0, 5, 2, 1)

        # Connect signals
        self.reset_button.connect("clicked", self.on_reset_button_clicked)
        self.menu_po.connect("show", self.on_menu_po_show)


    def connect_signals(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.gpu_usage_cb.connect("toggled", self.on_gpu_usage_cb_toggled)


    def disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.gpu_usage_cb.disconnect_by_func(self.on_gpu_usage_cb_toggled)


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


    def on_gpu_usage_cb_toggled(self, widget):
        """
        Show/Hide GPU usage percentage graphics.
        """

        if widget.get_active() == True:
            Config.summary_show_gpu_usage = 1
        if widget.get_active() == False:
            Config.summary_show_gpu_usage = 0

        Common.save_tab_settings(Summary)


    def on_reset_button_clicked(self, widget):
        """
        Reset all tab settings.
        """

        # Load default settings
        Config.config_default_performance_summary_func()
        Config.config_save_func()

        Common.update_tab_and_menu_gui(self, Summary)


    def set_gui(self):
        """
        Set menu GUI items.
        """

        # Set active checkbuttons if disk read speed/disk write speed values are "1".
        if Config.summary_show_gpu_usage == 1:
            self.gpu_usage_cb.set_active(True)
        if Config.summary_show_gpu_usage == 0:
            self.gpu_usage_cb.set_active(False)


SummaryMenu = SummaryMenu()


import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .Config import Config
from .Sensors import Sensors
from . import Common

_tr = Config._tr


class SensorsMenu:

    def __init__(self):

        self.name = "SensorsMenu"

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

        # Label - menu title (Sensors)
        label = Common.menu_title_label(_tr("Sensors"))
        main_grid.attach(label, 0, 0, 2, 1)

        # Label (Data Unit)
        label = Common.title_label(_tr("Data Unit"))
        main_grid.attach(label, 0, 1, 2, 1)

        # Label (Temperature)
        label = Gtk.Label()
        label.set_label(_tr("Temperature"))
        label.set_halign(Gtk.Align.CENTER)
        main_grid.attach(label, 0, 2, 1, 1)

        # CheckButton (Celsius)
        self.temperature_unit_celsius_cb = Common.checkbutton(_tr("Celsius"), None)
        main_grid.attach(self.temperature_unit_celsius_cb, 0, 3, 1, 1)

        # CheckButton (Fahrenheit)
        self.temperature_unit_fahrenheit_cb = Common.checkbutton(_tr("Fahrenheit"), self.temperature_unit_celsius_cb)
        main_grid.attach(self.temperature_unit_fahrenheit_cb, 0, 4, 1, 1)

        # Separator
        separator = Common.menu_separator()
        main_grid.attach(separator, 0, 5, 2, 1)

        # Button (Reset)
        self.reset_button = Common.reset_button()
        main_grid.attach(self.reset_button, 0, 6, 2, 1)

        # Connect signals
        self.reset_button.connect("clicked", self.on_reset_button_clicked)
        self.menu_po.connect("show", self.on_menu_po_show)


    def connect_signals(self):
        """
        Connect some of the signals to be able to disconnect them for setting GUI.
        """

        self.temperature_unit_celsius_cb.connect("toggled", self.on_temperature_unit_cb_toggled)
        self.temperature_unit_fahrenheit_cb.connect("toggled", self.on_temperature_unit_cb_toggled)


    def disconnect_signals(self):
        """
        Disconnect some of the signals for setting GUI.
        """

        self.temperature_unit_celsius_cb.disconnect_by_func(self.on_temperature_unit_cb_toggled)
        self.temperature_unit_fahrenheit_cb.disconnect_by_func(self.on_temperature_unit_cb_toggled)


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


    def on_temperature_unit_cb_toggled(self, widget):
        """
        Set temperature units.
        """

        if widget.get_active() == True:
            if widget == self.temperature_unit_celsius_cb:
                Config.temperature_unit = "celsius"
            if widget == self.temperature_unit_fahrenheit_cb:
                Config.temperature_unit = "fahrenheit"

        Common.save_tab_settings(Sensors)


    def on_reset_button_clicked(self, widget):
        """
        Reset all tab settings.
        """

        # Load default settings
        Config.config_default_performance_sensors_func()
        Config.config_save_func()

        Common.update_tab_and_menu_gui(self, Sensors)


    def set_gui(self):
        """
        Set menu GUI items.
        """

        # Select checkbutton appropriate for temperature unit setting
        if Config.temperature_unit == "celsius":
            self.temperature_unit_celsius_cb.set_active(True)
        if Config.temperature_unit == "fahrenheit":
            self.temperature_unit_fahrenheit_cb.set_active(False)


SensorsMenu = SensorsMenu()


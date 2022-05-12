#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import subprocess

from locale import gettext as _tr

from Config import Config
import Services


# Define class
class ServicesMenuRightClick:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ServicesMenuRightClick.ui")

        # Get GUI objects
        self.menu6101m = builder.get_object('menu6101m')
        self.menuitem6101m = builder.get_object('menuitem6101m')
        self.menuitem6102m = builder.get_object('menuitem6102m')
        self.menuitem6103m = builder.get_object('menuitem6103m')
        self.menuitem6104m = builder.get_object('menuitem6104m')
        self.menuitem6105m = builder.get_object('menuitem6105m')
        self.menuitem6106m = builder.get_object('menuitem6106m')
        self.checkmenuitem6107m = builder.get_object('checkmenuitem6107m')
        self.menuitem6108m = builder.get_object('menuitem6108m')

        # Connect GUI signals
        self.menuitem6101m.connect("activate", self.on_service_manage_items_activate)
        self.menuitem6102m.connect("activate", self.on_service_manage_items_activate)
        self.menuitem6103m.connect("activate", self.on_service_manage_items_activate)
        self.menuitem6104m.connect("activate", self.on_service_manage_items_activate)
        self.menuitem6105m.connect("activate", self.on_service_manage_items_activate)
        self.menuitem6106m.connect("activate", self.on_service_manage_items_activate)
        # Handler id is defined in order to block signals of the checkmenuitem while setting menu item.
        self.checkmenuitem6107m_handler_id = self.checkmenuitem6107m.connect("toggled", self.on_service_manage_items_activate)
        self.menuitem6108m.connect("activate", self.on_menuitem6108m_activate)


    # ----------------------- "Start" item -----------------------
    def on_service_manage_items_activate(self, widget):

        # Get right clicked service name.
        service_name = Services.selected_service_name

        # If "Start" item is clicked.
        if widget == self.menuitem6101m:
            service_manage_command = ["systemctl", "start", service_name]

        # If "Stop" item is clicked.
        if widget == self.menuitem6102m:
            service_manage_command = ["systemctl", "stop", service_name]

        # If "Restart" item is clicked.
        if widget == self.menuitem6103m:
            service_manage_command = ["systemctl", "restart", service_name]

        # If "Reload" item is clicked.
        if widget == self.menuitem6104m:
            service_manage_command = ["systemctl", "reload", service_name]

        # If "Enable" item is clicked.
        if widget == self.menuitem6105m:
            service_manage_command = ["systemctl", "enable", service_name]

        # If "Disable" item is clicked.
        if widget == self.menuitem6106m:
            service_manage_command = ["systemctl", "disable", service_name]

        # If "Mask" item is clicked and it is checked.
        if widget == self.checkmenuitem6107m and widget.get_active() == True:
            service_manage_command = ["systemctl", "mask", service_name]

        # If "Mask" item is clicked and it is unchecked.
        if widget == self.checkmenuitem6107m and widget.get_active() == False:
            service_manage_command = ["systemctl", "unmask", service_name]

        # Manage the right clicked service and show an information dialog if there is output messages (warnings/errors).
        try:
            (subprocess.check_output(service_manage_command, stderr=subprocess.STDOUT, shell=False)).decode()
        except subprocess.CalledProcessError as e:
            self.services_action_warning_dialog(e.output.decode("utf-8").strip())
        return


    # ----------------------- "Details" item -----------------------
    def on_menuitem6108m_activate(self, widget):

        from ServicesDetails import ServicesDetails
        ServicesDetails.window6101w.show()


    # ----------------------- Called for activating/deactivating "Enable/Disable" checkmenuitem -----------------------
    def services_set_checkmenuitem_func(self):

        service_name = Services.selected_service_name

        service_status = (subprocess.check_output(["systemctl", "show", service_name, "--property=UnitFileState"], shell=False)).decode().strip().split("=")[1]

        with self.checkmenuitem6107m.handler_block(self.checkmenuitem6107m_handler_id):
            if service_status == "masked":
                self.checkmenuitem6107m.set_active(True)
            if service_status != "masked":
                self.checkmenuitem6107m.set_active(False)


    # ----------------------------------- Services - Service Action Warning Dialog Function (shows a warning dialog when an output text is obtained during service actions (start, stop, reload, etc.)) -----------------------------------
    def services_action_warning_dialog(self, dialog_text):

        warning_dialog6101 = Gtk.MessageDialog(transient_for=Services.grid6101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.CLOSE, text=_tr("Information"))
        warning_dialog6101.format_secondary_text(dialog_text)
        self.warning_dialog6101_response = warning_dialog6101.run()
        warning_dialog6101.destroy()


# Generate object
ServicesMenuRightClick = ServicesMenuRightClick()


#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import subprocess

from locale import gettext as _tr

from Config import Config
import Users


# Define class
class UsersMenuRightClick:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersMenuRightClick.ui")

        # Get GUI objects
        self.menu3101m = builder.get_object('menu3101m')
        self.menuitem3101m = builder.get_object('menuitem3101m')
        self.menuitem3102m = builder.get_object('menuitem3102m')

        # Connect GUI signals
        self.menuitem3101m.connect("activate", self.on_menuitem3101m_activate)
        self.menuitem3102m.connect("activate", self.on_menuitem3102m_activate)


    # ----------------------- "End User Session" item -----------------------
    def on_menuitem3101m_activate(self, widget):

        # Get right clicked username and UID
        selected_username = str(Users.selected_username)
        selected_user_uid = str(Users.selected_user_uid)

        self.users_end_user_session_warning_dialog(selected_username, selected_user_uid)

        if self.dialog3101_response == Gtk.ResponseType.YES:
            try:
                (subprocess.check_output(["pkexec", "pkill", "-9", "--uid", selected_user_uid], stderr=subprocess.STDOUT, shell=False)).decode()
            except Exception:
                pass


    # ----------------------- "Details" item -----------------------
    def on_menuitem3102m_activate(self, widget):

        from UsersDetails import UsersDetails
        UsersDetails.window3101w.show()


    # ----------------------------------- Users - End User Session Warning Dialog Function -----------------------------------
    def users_end_user_session_warning_dialog(self, selected_username, selected_user_uid):

        dialog3101 = Gtk.MessageDialog(transient_for=Users.grid3101.get_toplevel(), title="", flags=0, message_type=Gtk.MessageType.WARNING,
        buttons=Gtk.ButtonsType.YES_NO, text=_tr("Do you want to end session of this user?"))
        dialog3101.format_secondary_text(_tr("This action will end all processes of the user immediately and may cause data loss.") +
                                             "\n\n" + _tr("This operation may lock current user account on some systems. You can unlock it by entering user password.") +
                                             "\n\n    " + _tr("User") + ": " + selected_username +
                                             "\n    " + _tr("UID") + ": " + selected_user_uid)
        self.dialog3101_response = dialog3101.run()
        dialog3101.destroy()


# Generate object
UsersMenuRightClick = UsersMenuRightClick()


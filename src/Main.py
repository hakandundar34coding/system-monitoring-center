#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="com.github.hakand34.system-monitoring-center", **kwargs)
        self.window = None

    def do_activate(self):
        # Allow opening single instance of the application.
        if not self.window:
            from MainGUI import MainGUI
            self.window = MainGUI.window1
            self.window.set_application(self)
            self.window.show_all()
            Gtk.main()


app = Application()
app.run(None)


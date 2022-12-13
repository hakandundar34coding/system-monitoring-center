#!/usr/bin/env python3

import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class SMCApplication(Gtk.Application):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, application_id="io.github.hakandundar34coding.system-monitoring-center")
        self.connect('activate', self.on_activate)
        self.main_window = None

    def on_activate(self, app):
        # Allow opening single instance of the application.
        if not self.main_window:
            from MainWindow import MainWindow
            self.main_window = MainWindow.main_window
            self.main_window.set_application(self)
            self.main_window.present()


app = SMCApplication()
app.run(None)


#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class SMCApplication(Gtk.Application):

    def __init__(self):
        super().__init__(application_id="io.github.hakandundar34coding.system-monitoring-center")
        self.connect('activate', self.on_activate)
        self.main_window = None

    def on_activate(self, app):
        # Allow opening single instance of the application.
        if not self.main_window:
            from .MainWindow import MainWindow
            self.main_window = MainWindow.main_window
            self.main_window.set_application(self)
            self.main_window.present()


localedir = None
def main(_localedir):
    global localedir
    localedir = _localedir
    app = SMCApplication()
    return app.run(None)

if __name__ == '__main__':
    app = SMCApplication()
    app.run(None)


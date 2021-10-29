#!/usr/bin/env python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

from MainGUI import window1

class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="tr.org.pardus.system-monitoring-center", flags=Gio.ApplicationFlags.NON_UNIQUE, **kwargs)
        self.window = None

    def do_activate(self):
        self.window = window1


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

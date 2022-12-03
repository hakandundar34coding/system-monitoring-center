#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from locale import gettext as _tr

from Performance import Performance
import Common


class Summary:

    def __init__(self):

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_grid = Common.tab_grid()

        # Label (Summary)
        label = Common.tab_title_label(_tr("Summary"))
        self.tab_grid.attach(label, 0, 0, 1, 1)

        # Summary tab drawingarea
        self.da_summary = Gtk.DrawingArea()
        self.da_summary.set_hexpand(True)
        self.da_summary.set_vexpand(True)
        self.tab_grid.attach(self.da_summary, 0, 1, 1, 1)

        self.da_summary.set_draw_func(Performance.performance_summary_chart_draw)


    def summary_initial_func(self):
        """
        Initial code.
        """

        self.initial_already_run = 1


    def summary_loop_func(self):
        """
        Draw graphics for showing performance data.
        """

        self.da_summary.queue_draw()


Summary = Summary()


#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Pango

from locale import gettext as _tr

from Performance import Performance


class Summary:

    def __init__(self):

        # Tab GUI
        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        # Grid (tab)
        self.tab_grid = Gtk.Grid()
        self.tab_grid.set_row_spacing(10)
        self.tab_grid.set_margin_top(2)
        self.tab_grid.set_margin_bottom(2)
        self.tab_grid.set_margin_start(2)
        self.tab_grid.set_margin_end(2)

        # Bold and 2x label atributes
        attribute_list_bold_2x = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        attribute_list_bold_2x.insert(attribute)
        attribute = Pango.attr_scale_new(2.0)
        attribute_list_bold_2x.insert(attribute)

        # Label (Summary)
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        label.set_attributes(attribute_list_bold_2x)
        label.set_label(_tr("Summary"))
        self.tab_grid.attach(label, 0, 0, 1, 1)

        # Summary tab drawingarea
        self.da_summary = Gtk.DrawingArea()
        self.da_summary.set_hexpand(True)
        self.da_summary.set_vexpand(True)
        self.tab_grid.attach(self.da_summary, 0, 1, 1, 1)

        # Connect functions
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


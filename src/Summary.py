#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Pango

from locale import gettext as _tr

from Performance import Performance


class Summary:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Summary tab GUI
        self.summary_tab_gui()

        # "0" value of "initial_already_run" variable means that initial function is not run before or
        # tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    def summary_tab_gui(self):
        """
        Generate Summary tab GUI.
        """

        # Summary tab grid
        self.summary_tab_grid = Gtk.Grid()
        self.summary_tab_grid.set_row_spacing(10)
        self.summary_tab_grid.set_margin_top(2)
        self.summary_tab_grid.set_margin_bottom(2)
        self.summary_tab_grid.set_margin_start(2)
        self.summary_tab_grid.set_margin_end(2)

        # Bold and 2x label atributes
        self.attribute_list_bold_2x = Pango.AttrList()
        attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
        self.attribute_list_bold_2x.insert(attribute)
        attribute = Pango.attr_scale_new(2.0)
        self.attribute_list_bold_2x.insert(attribute)

        # Summary tab name label
        summary_tab_name_label = Gtk.Label()
        summary_tab_name_label.set_halign(Gtk.Align.START)
        summary_tab_name_label.set_attributes(self.attribute_list_bold_2x)
        summary_tab_name_label.set_label(_tr("Summary"))
        self.summary_tab_grid.attach(summary_tab_name_label, 0, 0, 1, 1)

        # Summary tab drawingarea
        self.summary_tab_drawingarea = Gtk.DrawingArea()
        self.summary_tab_drawingarea.set_hexpand(True)
        self.summary_tab_drawingarea.set_vexpand(True)
        self.summary_tab_grid.attach(self.summary_tab_drawingarea, 0, 1, 1, 1)

        # Connect functions
        self.summary_tab_drawingarea.set_draw_func(Performance.performance_summary_chart_draw)


    def summary_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.initial_already_run = 1


    def summary_loop_func(self):
        """
        Draw graphics for showing performance data.
        """

        self.summary_tab_drawingarea.queue_draw()


Summary = Summary()


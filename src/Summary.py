#!/usr/bin/env python3

# Import modules
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os

from Performance import Performance


# Define class
class Summary:

    # ----------------------- Always called when object is generated -----------------------
    def __init__(self):

        # Get GUI objects from file
        builder = Gtk.Builder()
        builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/SummaryTab.ui")

        # Get GUI objects
        self.grid1701 = builder.get_object('grid1701')
        self.drawingarea1701 = builder.get_object('drawingarea1701')

        # Get chart functions from another module and define as local objects for lower CPU usage.
        self.performance_summary_chart_draw_func = Performance.performance_summary_chart_draw_func

        # Connect GUI signals
        self.drawingarea1701.connect("draw", self.performance_summary_chart_draw_func)

        # "0" value of "initial_already_run" variable means that initial function is not run before or tab settings are reset from general settings and initial function have to be run.
        self.initial_already_run = 0


    # ----------------------------------- Summary - Initial Function (contains initial code which which is not wanted to be run in every loop) -----------------------------------
    def summary_initial_func(self):

        self.initial_already_run = 1


    # ----------------------------------- Summary - Draw Performance Data Function -----------------------------------
    def summary_loop_func(self):

        # Draw performance data.
        self.drawingarea1701.queue_draw()


# Generate object
Summary = Summary()


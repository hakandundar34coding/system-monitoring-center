#!/usr/bin/env python3

# ----------------------------------- ChartPlots - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def chart_plots_import_func():

    global Gtk, GLib, Thread

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    from threading import Thread


    global MainGUI, Config, Performance
    import MainGUI, Config, Performance


# ----------------------------------- ChartPlots - ChartPlots GUI Function (draws chart by using a drawing area -This function is called automatically when there is changes/updates on the same window such as window resize, tab change, button click, widget updates, mouse hover on some widgets, window maximize/minimize, etc.-) -----------------------------------
def charts_gui_func():

    global drawingarea101, drawingarea102
    drawingarea101 = MainGUI.builder.get_object('drawingarea101')
    drawingarea102 = MainGUI.builder.get_object('drawingarea102')




# ----------------------------------- ChartPlots - Plot Drawingarea Signal Connect Function (connects drawing area signals) ----------------------------------- 
def chart_plots_drawingarea_signal_connect_func():

    # These drawingarea signals are connected via a repeated threaded function in order to avoid "not defined" error for some variables in "Performance" module.
    # Some "Performance" module background and foreground function threads are checked if they are not alive before running this function.
    # Drawingarea functions run very fast and they could not find some variables in the first "Performance" module loop even if drawingarea function signals are connected
    # just after running "Performance" module foreground functions. This "thread not alive check" solution helps avoiding this errors.
    # This thread control is performed in every 1 milliseconds. Signals are connected if they are not alive.



# ----------------------------------- ChartPlots - Drawingarea Signal Connect Loop Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def chart_plots_drawingarea_signal_connect_loop_func():

    if not Performance.performance_background_initial_thread.is_alive():
        if not Performance.performance_foreground_initial_thread.is_alive():
            GLib.idle_add(chart_plots_drawingarea_signal_connect_func)
            return
    GLib.timeout_add(1, chart_plots_drawingarea_signal_connect_loop_func)


# ----------------------------------- ChartPlots - Thread Run Function (starts execution of the threads) -----------------------------------
def chart_plots_drawingarea_signal_connect_thread_func():

    chart_plots_drawingarea_signal_connect_thread = Thread(target=chart_plots_drawingarea_signal_connect_loop_func, daemon=True)
    chart_plots_drawingarea_signal_connect_thread.start()

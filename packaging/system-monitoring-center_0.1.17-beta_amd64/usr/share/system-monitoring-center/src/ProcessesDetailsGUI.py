# ----------------------------------- Processes - Processes Details Window GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def processes_details_gui_import_function():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global ProcessesDetails
    import ProcessesDetails


# ----------------------------------- Processes - Processes Details Window GUI Function (the code of this module in order to avoid running them during module import and defines "Processes Details" window GUI objects and functions/signals) -----------------------------------
def processes_details_gui_function():

    # Processes Details window GUI objects
    global builder2101w, window2101w, notebook2101w
    global label2101w, label2102w, label2103w, label2104w, label2105w, label2106w, label2107w, label2108w, label2109w, label2110w
    global label2111w, label2112w, label2113w, label2114w, label2115w, label2116w, label2117w, label2118w, label2119w, label2120w
    global label2121w, label2122w, label2123w, label2124w, label2125w, label2126w, label2127w, label2128w, label2129w, label2130w
    global label2131w, label2132w, label2133w, label2134w, label2135w, label2136w, label2137w, label2138w, label2139w, label2140w
    global label2141w, label2142w, label2143w


    # Processes Details window GUI objects - get
    builder2101w = Gtk.Builder()
    builder2101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ProcessesDetailsWindow.ui")

    window2101w = builder2101w.get_object('window2101w')

    notebook2101w = builder2101w.get_object('notebook2101w')

    # Process Details window "Summary" tab GUI objects
    label2101w = builder2101w.get_object('label2101w')
    label2102w = builder2101w.get_object('label2102w')
    label2103w = builder2101w.get_object('label2103w')
    label2104w = builder2101w.get_object('label2104w')
    label2105w = builder2101w.get_object('label2105w')
    label2106w = builder2101w.get_object('label2106w')
    label2107w = builder2101w.get_object('label2107w')
    label2108w = builder2101w.get_object('label2108w')
    label2109w = builder2101w.get_object('label2109w')
    label2110w = builder2101w.get_object('label2110w')
    label2111w = builder2101w.get_object('label2111w')
    label2112w = builder2101w.get_object('label2112w')
    label2113w = builder2101w.get_object('label2113w')
    label2114w = builder2101w.get_object('label2114w')
    label2115w = builder2101w.get_object('label2115w')

    # Process Details window "CPU and RAM" tab GUI objects
    label2116w = builder2101w.get_object('label2116w')
    label2117w = builder2101w.get_object('label2117w')
    label2118w = builder2101w.get_object('label2118w')
    label2119w = builder2101w.get_object('label2119w')
    label2120w = builder2101w.get_object('label2120w')
    label2121w = builder2101w.get_object('label2121w')
    label2122w = builder2101w.get_object('label2122w')
    label2123w = builder2101w.get_object('label2123w')
    label2124w = builder2101w.get_object('label2124w')
    label2125w = builder2101w.get_object('label2125w')
    label2126w = builder2101w.get_object('label2126w')
    label2127w = builder2101w.get_object('label2127w')

    # Process Details window "Disk and Path" tab GUI objects
    label2128w = builder2101w.get_object('label2128w')
    label2129w = builder2101w.get_object('label2129w')
    label2130w = builder2101w.get_object('label2130w')
    label2131w = builder2101w.get_object('label2131w')
    label2132w = builder2101w.get_object('label2132w')
    label2133w = builder2101w.get_object('label2133w')
    label2134w = builder2101w.get_object('label2134w')
    label2135w = builder2101w.get_object('label2135w')
    label2136w = builder2101w.get_object('label2136w')
    label2137w = builder2101w.get_object('label2137w')

    # Process Details window "Network" tab GUI objects
    label2138w = builder2101w.get_object('label2138w')
    label2139w = builder2101w.get_object('label2139w')
    label2140w = builder2101w.get_object('label2140w')
    label2141w = builder2101w.get_object('label2141w')
    label2142w = builder2101w.get_object('label2142w')
    label2143w = builder2101w.get_object('label2143w')


    # Processes Details window GUI functions
    def on_window2101w_delete_event(widget, event):
        window2101w.hide()
        return True

    def on_window2101w_show(widget):
        processes_details_gui_reset_function()                                                # Call this function in order to reset Processes Details window. Data from previous process remains visible (for a short time) until getting and showing new process data if window is closed and opened for an another process. Also last selected tab remains same because window is made hidden when close button is clicked.


    # Processes Details window GUI functions - connect
    window2101w.connect("delete-event", on_window2101w_delete_event)
    window2101w.connect("show", on_window2101w_show)


# ----------------------------------- Processes - Processes Details Window GUI Reset Function (resets Processes Details window) -----------------------------------
def processes_details_gui_reset_function():

    notebook2101w.set_current_page(0)                                                         # Set fist page (Summary tab) of the notebook
    label2101w.set_text("--")
    label2102w.set_text("--")
    label2103w.set_text("--")
    label2104w.set_text("--")
    label2105w.set_text("--")
    label2106w.set_text("--")
    label2107w.set_text("--")
    label2108w.set_text("--")
    label2109w.set_text("--")
    label2110w.set_text("--")
    label2111w.set_text("--")
    label2112w.set_text("--")
    label2113w.set_text("--")
    label2114w.set_text("--")
    label2115w.set_text("--")
    label2116w.set_text("--")
    label2117w.set_text("--")
    label2118w.set_text("--")
    label2119w.set_text("--")
    label2120w.set_text("--")
    label2121w.set_text("--")
    label2122w.set_text("--")
    label2123w.set_text("--")
    label2124w.set_text("--")
    label2125w.set_text("--")
    label2126w.set_text("--")
    label2127w.set_text("--")
    label2128w.set_text("--")
    label2129w.set_text("--")
    label2130w.set_text("--")
    label2131w.set_text("--")
    label2132w.set_text("--")
    label2133w.set_text("--")
    label2134w.set_text("--")
    label2135w.set_text("--")
    label2136w.set_text("--")
    label2137w.set_text("--")
    label2138w.set_text("--")
    label2139w.set_text("--")
    label2140w.set_text("--")
    label2141w.set_text("--")
    label2142w.set_text("--")
    label2143w.set_text("--")

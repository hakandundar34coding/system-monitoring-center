# ----------------------------------- Services - Services Details Window GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def services_details_gui_import_function():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global ServicesDetails
    import ServicesDetails


# ----------------------------------- Services - Services Details Window GUI Function (the code of this module in order to avoid running them during module import and defines "Services Details" window GUI objects and functions/signals) -----------------------------------
def services_details_gui_function():

    # Services Details window GUI objects
    global builder6101w, window6101w, notebook6101w
    global label6101w, label6102w, label6103w, label6104w, label6105w, label6106w, label6107w, label6108w, label6109w, label6110w
    global label6111w, label6112w, label6113w, label6114w, label6115w, label6116w, label6117w, label6118w, label6119w, label6120w
    global label6121w, label6122w


    # Services Details window GUI objects - get
    builder6101w = Gtk.Builder()
    builder6101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ServicesDetailsWindow.glade")

    window6101w = builder6101w.get_object('window6101w')

    notebook6101w = builder6101w.get_object('notebook6101w')

    # Service Details window "General" tab GUI objects
    label6101w = builder6101w.get_object('label6101w')
    label6102w = builder6101w.get_object('label6102w')
    label6103w = builder6101w.get_object('label6103w')
    label6104w = builder6101w.get_object('label6104w')
    label6105w = builder6101w.get_object('label6105w')
    label6106w = builder6101w.get_object('label6106w')
    label6107w = builder6101w.get_object('label6107w')
    label6108w = builder6101w.get_object('label6108w')
    label6109w = builder6101w.get_object('label6109w')
    label6110w = builder6101w.get_object('label6110w')
    label6111w = builder6101w.get_object('label6111w')
    label6112w = builder6101w.get_object('label6112w')
    label6113w = builder6101w.get_object('label6113w')
    label6114w = builder6101w.get_object('label6114w')
    label6115w = builder6101w.get_object('label6115w')
    label6116w = builder6101w.get_object('label6116w')
    label6117w = builder6101w.get_object('label6117w')
    label6118w = builder6101w.get_object('label6118w')

    # Service Details window "Dependencies" tab GUI objects
    label6119w = builder6101w.get_object('label6119w')
    label6120w = builder6101w.get_object('label6120w')
    label6121w = builder6101w.get_object('label6121w')
    label6122w = builder6101w.get_object('label6122w')


    # Services Details window GUI functions
    def on_window6101w_delete_event(widget, event):
        window6101w.hide()
        return True

    def on_window6101w_show(widget):
        services_details_gui_reset_function()                                                 # Call this function in order to reset Services Details window. Data from previous service remains visible (for a short time) until getting and showing new service data if window is closed and opened for an another service. Also last selected tab remains same because window is made hidden when close button is clicked.


    # Services Details window GUI functions - connect
    window6101w.connect("delete-event", on_window6101w_delete_event)
    window6101w.connect("show", on_window6101w_show)


# ----------------------------------- Services - Services Details Window GUI Reset Function (resets Services Details window) -----------------------------------
def services_details_gui_reset_function():

    notebook6101w.set_current_page(0)                                                          # Set fist page (Summary tab) of the notebook
    label6101w.set_text("--")
    label6102w.set_text("--")
    label6103w.set_text("--")
    label6104w.set_text("--")
    label6105w.set_text("--")
    label6106w.set_text("--")
    label6107w.set_text("--")
    label6108w.set_text("--")
    label6109w.set_text("--")
    label6110w.set_text("--")
    label6111w.set_text("--")
    label6112w.set_text("--")
    label6113w.set_text("--")
    label6114w.set_text("--")
    label6115w.set_text("--")
    label6116w.set_text("--")
    label6117w.set_text("--")
    label6118w.set_text("--")
    label6119w.set_text("--")
    label6120w.set_text("--")
    label6121w.set_text("--")
    label6122w.set_text("--")

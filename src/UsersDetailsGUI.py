# ----------------------------------- Users - Users Details Window GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def users_details_gui_import_function():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    # Import locale and gettext modules for defining translation texts which will be recognized by gettext application (will be run by programmer externally) and exported into a ".pot" file. 
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    import locale
    from locale import gettext as _tr

    # Define contstants for language translation support
    global application_name
    application_name = "system-monitoring-center"
    translation_files_path = "/usr/share/locale"
    system_current_language = os.environ.get("LANG")

    # Define functions for language translation support
    locale.bindtextdomain(application_name, translation_files_path)
    locale.textdomain(application_name)
    locale.setlocale(locale.LC_ALL, system_current_language)


# ----------------------------------- Users - Users Details Window GUI Function (the code of this module in order to avoid running them during module import and defines "Users Details" window GUI objects and functions/signals) -----------------------------------
def users_details_gui_function():

    # Users Details window GUI objects
    global builder3101w, window3101w
    global label3101w, label3102w, label3103w, label3104w, label3105w, label3106w, label3107w, label3108w, label3109w, label3110w
    global label3111w, label3112w, label3113w, label3114w


    # Users Details window GUI objects - get
    builder3101w = Gtk.Builder()
    builder3101w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/UsersDetailsWindow.ui")

    window3101w = builder3101w.get_object('window3101w')


    # Users Details window GUI objects
    label3101w = builder3101w.get_object('label3101w')
    label3102w = builder3101w.get_object('label3102w')
    label3103w = builder3101w.get_object('label3103w')
    label3104w = builder3101w.get_object('label3104w')
    label3105w = builder3101w.get_object('label3105w')
    label3106w = builder3101w.get_object('label3106w')
    label3107w = builder3101w.get_object('label3107w')
    label3108w = builder3101w.get_object('label3108w')
    label3109w = builder3101w.get_object('label3109w')
    label3110w = builder3101w.get_object('label3110w')
    label3111w = builder3101w.get_object('label3111w')
    label3112w = builder3101w.get_object('label3112w')
    label3113w = builder3101w.get_object('label3113w')
    label3114w = builder3101w.get_object('label3114w')


    # Users Details window GUI functions
    def on_window3101w_delete_event(widget, event):
        window3101w.hide()
        return True

    def on_window3101w_show(widget):
        users_details_gui_reset_function()                                                    # Call this function in order to reset Users Details window. Data from previous user remains visible (for a short time) until getting and showing new user data if window is closed and opened for an another user because window is made hidden when close button is clicked.


    # Users Details window GUI functions - connect
    window3101w.connect("delete-event", on_window3101w_delete_event)
    window3101w.connect("show", on_window3101w_show)


# ----------------------------------- Users - Users Details Window GUI Reset Function (resets Users Details window) -----------------------------------
def users_details_gui_reset_function():
    window3101w.set_title(_tr("User Details"))                                               # Reset window title
    window3101w.set_icon_name("system-monitoring-center-user-symbolic")                       # Reset window icon
    label3101w.set_text("--")
    label3102w.set_text("--")
    label3103w.set_text("--")
    label3104w.set_text("--")
    label3105w.set_text("--")
    label3106w.set_text("--")
    label3107w.set_text("--")
    label3108w.set_text("--")
    label3109w.set_text("--")
    label3110w.set_text("--")
    label3111w.set_text("--")
    label3112w.set_text("--")
    label3113w.set_text("--")
    label3114w.set_text("--")

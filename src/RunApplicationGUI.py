#!/usr/bin/env python3

# ----------------------------------- RunApplication - RunApplication Window GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def run_application_gui_import_func():

    global Gtk, Gdk, os, Thread

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    import os
    from threading import Thread


    global RunApplication
    import RunApplication


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


# ----------------------------------- RunApplication - RunApplication Window GUI Function (the code of this module in order to avoid running them during module import and defines "Sensors" tab menu/popover GUI objects and functions/signals) -----------------------------------
def run_application_gui_func():

    global window1001w
    global grid1001w, searchentry1001w, image1001w, button1001w, checkbutton1001w, checkbutton1002w, checkbutton1003w


    builder1001w = Gtk.Builder()
    builder1001w.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/RunApplicationWindow.glade")

    window1001w = builder1001w.get_object('window1001w')
    grid1001w = builder1001w.get_object('grid1001w')
    searchentry1001w = builder1001w.get_object('searchentry1001w')
    image1001w = builder1001w.get_object('image1001w')
    button1001w = builder1001w.get_object('button1001w')
    checkbutton1001w = builder1001w.get_object('checkbutton1001w')
    checkbutton1002w = builder1001w.get_object('checkbutton1002w')
    checkbutton1003w = builder1001w.get_object('checkbutton1003w')


    def on_window1001w_delete_event(widget, event):
        window1001w.hide()
        return True

    def on_window1001w_show(widget):
        pass

    def on_checkbutton1003w_toggled(widget):                                                  # "Run with external GPU" GUI object
        if checkbutton1003w.get_active() == True:                                             # "DRI_PRIME=1" command is used in order to run program with the external GPU. Other options are disabled when this option is enabled because this command does not work with other commands like "x-terminal-emulator -e " and "pkexec ".
            checkbutton1001w.set_active(False)
            checkbutton1001w.set_sensitive(False)
            checkbutton1002w.set_active(False)
            checkbutton1002w.set_sensitive(False)
        if checkbutton1003w.get_active() == False:
            checkbutton1001w.set_sensitive(True)
            checkbutton1002w.set_sensitive(True)

    def on_searchentry1001w_search_changed(widget):                                           # This function is run on every text changes in the search entry
            searchentry1001w.modify_fg(Gtk.StateFlags.NORMAL, None)
            selected_application_name = searchentry1001w.get_text()
            # Try to show application icon when search text matches with an application name. Show a default icon if application has no icon.
            if selected_application_name in RunApplication.application_name_list:
                try:
                    image1001w.set_from_gicon(RunApplication.application_icon_list[RunApplication.application_name_list.index(selected_application_name)], 6)
                except:
                    image1001w.set_from_pixbuf(RunApplication.pixbuf_for_no_icon_apps)
            # Show "edit-find" icon if there is no match between search text and any application name.
            if selected_application_name not in RunApplication.application_name_list:
                image1001w.set_from_pixbuf(Gtk.IconTheme.get_default().load_icon("system-monitoring-center-search-symbolic", 48, 0))

    def on_button1001w_clicked(widget):                                                       # "Run" button
        selected_application_name = searchentry1001w.get_text()
        if checkbutton1001w.get_active() == True:
            run_in_terminal = "x-terminal-emulator -e "
        if checkbutton1001w.get_active() == False:
            run_in_terminal = ""
        if checkbutton1002w.get_active() == True:
            run_as_root = "pkexec "
        if checkbutton1002w.get_active() == False:
            run_as_root = ""
        if checkbutton1003w.get_active() == True:
            run_with_selected_gpu = "DRI_PRIME=1 "
        if checkbutton1003w.get_active() == False:
            run_with_selected_gpu = ""
        def run_application():                                                                # Running action is performed in a separate thread for letting rest of the function code to be run without waiting closing the new opened application.
            try:
                os.system(run_with_selected_gpu + run_in_terminal + run_as_root + RunApplication.application_executable_list[RunApplication.application_name_list.index(selected_application_name)])
            except ValueError:                                                                # Convert color of the search entry into red if there is no match between search text and any application name.
                searchentry1001w.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))
        run_application_thread = Thread(target=run_application, daemon=True).start()          # Application is run in another thread in order not to wait end of the run which occurs in single threaded code execution.


    window1001w.connect("delete-event", on_window1001w_delete_event)
    window1001w.connect("show", on_window1001w_show)
    checkbutton1003w.connect("toggled", on_checkbutton1003w_toggled)
    searchentry1001w.connect("search-changed", on_searchentry1001w_search_changed)
    button1001w.connect("clicked", on_button1001w_clicked)

    # Show information for warning the user if the application has been run with root privileges. Information is shown just below the application window headerbar.
    if os.geteuid() == 0:                                                                     # Check UID if it is "0". This means the application is run with root privileges.
        label_root_warning = Gtk.Label(label=_tr("Warning! The application has been run with root privileges, you may harm your system.\n Also programs which are run with this application will be run with root privileges."))    # Generate a new label for the information. This label does not exist in the ".glade" UI file.
        # label_root_warning.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(0.0, 1.0, 0.0, 1.0))
        label_root_warning.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse("red"))           # Set background color of the label.
        grid1001w.insert_row(0)                                                               # Insert a row at top of the grid.
        grid1001w.attach(label_root_warning, 0, 0, 3, 1)                                      # Attach the label to the grid at (0, 0) position. Grid containig the label has 3 cell in the horizontal axis and width of the label is set as 3 in order to fit the label with the width of the window.
        label_root_warning.set_margin_bottom(10)                                              # Set a margin between the label and the widget below it for looking of the widgets.
        label_root_warning.set_visible(True)                                                  # Set the label as visible.

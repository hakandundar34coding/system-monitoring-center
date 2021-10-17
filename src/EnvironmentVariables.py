#!/usr/bin/env python3

# ----------------------------------- EnvironmentVariables - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def environment_variables_import_func():

    global Gtk, Gdk, GLib, Thread, subprocess, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib
    from threading import Thread
    import subprocess
    import os


    global Config, MainGUI
    import Config, MainGUI


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


# ----------------------------------- EnvironmentVariables - EnvironmentVariables GUI Function (the code of this module in order to avoid running them during module import and defines "EnvironmentVariables" tab GUI objects and functions/signals) -----------------------------------
def environment_variables_gui_func():

    # Environment Variables tab GUI objects
    global grid7101, treeview7101, searchentry7101, button7101
    global radiobutton7101, radiobutton7102, radiobutton7103
    global label7101


    # Environment Variables tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.set_translation_domain(application_name)                                          # For showing translated texts onthe Glade generated GTK GUI
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/EnvironmentVariablesTab.ui")

    # Environment Variables tab GUI objects - get
    grid7101 = builder.get_object('grid7101')
    treeview7101 = builder.get_object('treeview7101')
    searchentry7101 = builder.get_object('searchentry7101')
    button7101 = builder.get_object('button7101')
    radiobutton7101 = builder.get_object('radiobutton7101')
    radiobutton7102 = builder.get_object('radiobutton7102')
    radiobutton7103 = builder.get_object('radiobutton7103')
    label7101 = builder.get_object('label7101')


    # Environment Variables tab GUI functions
    def on_treeview7101_button_press_event(widget, event):
        if event.button == 3:                                                                 # Open Environment Variables tab right click menu if mouse is right clicked on the treeview (and on any variable, otherwise menu will not be shown) and the mouse button is pressed.
            environment_variables_open_right_click_menu_func(event)

    def on_treeview7101_button_release_event(widget, event):
        if event.button == 1:                                                                 # Run the following function if mouse is left clicked on the treeview and the mouse button is released.
            environment_variables_treeview_column_order_width_row_sorting_func()

    def on_searchentry7101_changed(widget):
        radiobutton7101.set_active(True)
        environment_variables_treeview_filter_search_func()

    def on_button7101_clicked(widget):                                                        # "Environment Variables Tab Customizations" button
        if 'EnvironmentVarMenuCustomizations' not in globals():                               # Check if "EnvironmentVarMenuCustomizations" module is imported. Therefore it is not reimported on every right click operation.
            global EnvironmentVarMenuCustomizations
            import EnvironmentVarMenuCustomizations
            EnvironmentVarMenuCustomizations.environment_variables_menu_customizations_import_func()
            EnvironmentVarMenuCustomizations.environment_variables_menu_customizations_gui_func()
        EnvironmentVarMenuCustomizations.popover7101p.popup()

    def on_radiobutton7101_toggled(widget):                                                   # "Show all environment/shell variables" radiobutton
        if radiobutton7101.get_active() == True:
            searchentry7101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            environment_variables_treeview_filter_show_all_func()

    def on_radiobutton7102_toggled(widget):                                                   # "Show all environment variables" radiobutton
        if radiobutton7102.get_active() == True:
            searchentry7101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            environment_variables_treeview_filter_show_all_func()
            environment_variables_treeview_filter_environment_variables_logged_in_only()

    def on_radiobutton7103_toggled(widget):                                                   # "Show all shell variables" radiobutton
        if radiobutton7103.get_active() == True:
            searchentry7101.set_text("")                                                      # Changing "Show all ..." radiobuttons override treestore row visibilities. Searchentry text is reset in order to avoid frustrations.
            environment_variables_treeview_filter_show_all_func()
            environment_variables_treeview_filter_environment_variables_logged_out_only()



    # Environment Variables tab GUI functions - connect
    treeview7101.connect("button-press-event", on_treeview7101_button_press_event)
    treeview7101.connect("button-release-event", on_treeview7101_button_release_event)
    searchentry7101.connect("changed", on_searchentry7101_changed)
    button7101.connect("clicked", on_button7101_clicked)
    radiobutton7101.connect("toggled", on_radiobutton7101_toggled)
    radiobutton7102.connect("toggled", on_radiobutton7102_toggled)
    radiobutton7103.connect("toggled", on_radiobutton7103_toggled)


    # Environment Variables Tab - Treeview Properties
    treeview7101.set_activate_on_single_click(True)                                           # This command used for activating rows and column header buttons on single click. Column headers have to clicked twice (or clicked() command have to be used twice) for the first sorting operation if this is not used.
    treeview7101.set_fixed_height_mode(True)                                                  # This command is used for lower CPU usage when treeview is updated. It prevents calculating of the row heights on every update. To be able to use this command, "'column'.set_sizing(2)" command have to be used for all columns when adding them into treeview.
    treeview7101.set_headers_clickable(True)
    treeview7101.set_show_expanders(False)
    treeview7101.set_enable_search(True)                                                      # This command is used for searching by pressing on a key on keyboard or by using "Ctrl + F" shortcut.
    treeview7101.set_search_column(1)                                                         # This command used for searching by using entry.
    treeview7101.set_tooltip_column(1)


# ----------------------------------- Environment Variables - Open Right Click Menu Function (gets right clicked variable name and opens right click menu) -----------------------------------
def environment_variables_open_right_click_menu_func(event):

    try:                                                                                      # "try-except" is used in order to prevent errors when right clicked on an empty area on the treeview.
        path, _, _, _ = treeview7101.get_path_at_pos(int(event.x), int(event.y))
    except TypeError:
        return   
    model = treeview7101.get_model()
    treeiter = model.get_iter(path)
    if treeiter is not None:
        global selected_variable_value, selected_variable_type
        selected_variable_value = variable_list[environment_variables_data_rows.index(model[treeiter][:])]    # "[:]" is used in order to copy entire list to be able to use it for getting index in the "environment_variables_data_rows" list to use it getting name of the variable.
        selected_variable_type = variable_type_list[variable_list.index(selected_variable_value)]
        if 'EnvironmentVarMenuRightClick' not in globals():                                   # Check if "EnvironmentVarMenuRightClick" module is imported. Therefore it is not reimported on every right click operation.
            global EnvironmentVarMenuRightClick
            import EnvironmentVarMenuRightClick
            EnvironmentVarMenuRightClick.environment_variables_menu_right_click_import_func()
            EnvironmentVarMenuRightClick.environment_variables_menu_right_click_gui_func()
            if selected_variable_type == _tr("Environment Variable") or selected_variable_type == _tr("Environment & Shell Variable"):    # Perform following oprations if variable is not shell variable.
                EnvironmentVarMenuRightClick.menuitem7102m.set_sensitive(True)                # Set "Edit Environment Variable" item as sensitive
                EnvironmentVarMenuRightClick.menuitem7102m.set_tooltip_text("")               # Delete "Edit Environment Variable" item tooltip text
                EnvironmentVarMenuRightClick.menuitem7103m.set_sensitive(True)                # Set "Delete Environment Variable" item as sensitive
                EnvironmentVarMenuRightClick.menuitem7103m.set_tooltip_text("")               # Delete "Delete Environment Variable" item tooltip text
            if selected_variable_type == _tr("Shell Variable"):                               # Perform following oprations if variable is shell variable.
                EnvironmentVarMenuRightClick.menuitem7102m.set_sensitive(False)               # Set "Edit Environment Variable" item as insensitive
                EnvironmentVarMenuRightClick.menuitem7102m.set_tooltip_text(_tr("Shell variables cannot be edited."))    # Set "Edit Environment Variable" item tooltip text
                EnvironmentVarMenuRightClick.menuitem7103m.set_sensitive(False)               # Set "Delete Environment Variable" item as insensitive
                EnvironmentVarMenuRightClick.menuitem7103m.set_tooltip_text(_tr("Shell variables cannot be deleted."))    # Set "Delete Environment Variable" item tooltip text
        EnvironmentVarMenuRightClick.menu7101m.popup(None, None, None, None, event.button, event.time)


# ----------------------------------- Environment Variables - Initial Function (contains initial code which defines some variables and gets data which is not wanted to be run in every loop) -----------------------------------
def environment_variables_initial_func():

    # data list explanation:
    # environment_variables_data_list = [
    #                                   [treeview column number, treeview column title, internal column count, cell renderer count, treeview column sort column id, [data type 1, data type 2, ...], [cell renderer type 1, cell renderer type 2, ...], [cell attribute 1, cell attribute 2, ...], [cell renderer data 1, cell renderer data 2, ...], [cell left/right alignment 1, cell left/right alignment 2, ...], [set expand 1 {if cell will allocate unused space} cell expand 2, ...], [cell function 1, cell function 2, ...]]
    #                                   .
    #                                   .
    #                                   ]
    global environment_variables_data_list
    environment_variables_data_list = [
                                      [0, _tr('Variable'), 2, 1, 2, [bool, str], ['internal_column', 'CellRendererText'], ['no_cell_attribute', 'text'], [0, 1], ['no_cell_alignment', 0.0], ['no_set_expand', False], ['no_cell_function', 'no_cell_function']],
                                      [1, _tr('Value'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                                      [2, _tr('Variable Type'), 2, 2, 2, [str, str], ['CellRendererPixbuf', 'CellRendererText'], ['icon_name', 'text'], [0, 1], [0.0, 0.0], [False, False], ['no_cell_function', 'no_cell_function']]
                                      ]

    global environment_variables_data_rows_prev, varible_list_prev, piter_list, environment_variables_treeview_columns_shown_prev, environment_variables_data_row_sorting_column_prev, environment_variables_data_row_sorting_order_prev, environment_variables_data_column_order_prev, environment_variables_data_column_widths_prev
    environment_variables_data_rows_prev = []
    varible_list_prev = []
    piter_list = []
    environment_variables_treeview_columns_shown_prev = []
    environment_variables_data_row_sorting_column_prev = ""
    environment_variables_data_row_sorting_order_prev = ""
    environment_variables_data_column_order_prev = []
    environment_variables_data_column_widths_prev = []

    global environment_variable_image, shell_variable_image, environment_shell_variable_image
    environment_variable_image = "system-monitoring-center-environment-variables-symbolic"    # Will be used as image of the environment_variables
    shell_variable_image = "system-monitoring-center-terminal-symbolic"                       # Will be used as image of the shell_variables
    environment_shell_variable_image = "system-monitoring-center-environment-shell-variable-symbolic"    # Will be used as image of the both environment and shell_variables


    global filter_column
    filter_column = environment_variables_data_list[0][2] - 1                                 # Search filter is "Variable". "-1" is used because "processes_data_list" has internal column count and it has to be converted to Python index. For example, if there are 3 internal columns but index is 2 for the last internal column number for the relevant treeview column.


# ----------------------------------- Environment Variables - Get EnvironmentVariables Data Function (gets environment_variables data, adds into treeview and updates it) -----------------------------------
def environment_variables_loop_func():

    # Get GUI obejcts one time per floop instead of getting them multiple times
    global treeview7101

    # Prevent running the function if application is run with root privileges. Othserwise errors are encountered and additional work may be done for handling them.
    if os.geteuid() == 0:
        label7101.set_text(_tr("Listing environment/shell variables is not supported when application is run with root privileges."))
        return

    # Prevent running the function if application is run from bash/terminal. Othserwise errors are encountered and additional work may be done for handling them.
    # Get PID of the application, get PPID of the application (from PID), get name of the parent process of the application (from PPID), check if this name is "bash" in order to control if the application is run from terminal (bash). This situation occurs if application is run from code instead of shortcut (.desktop file) of the application. Because application process name is "python" or "Main" instead of "system-monitoring-center" in this situation.
    pid_of_application = os.getpid()
    with open("/proc/" + str(pid_of_application) + "/stat") as reader:                        # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
        ppid_of_application = reader.read().split()[-49]                                      # Process data is get by negative indexes because file content is split by " " (empty space) character and also process name could contain empty space character which may result confusion getting correct process data. In other words empty space character count may not be same for all process "stat" files and process name it at the second place in the file. Reading process data of which turn is later than process name by using negative index is a reliable method.
    with open("/proc/" + ppid_of_application + "/comm") as reader:
        parent_process_name = reader.read().strip()
    if parent_process_name == "bash":
        label7101.set_text(_tr("Listing environment/shell variables is not supported when application is run in terminal."))
        return
    # Parent process name may be "system-monitoring-center" if application is run from its ".desktop" file. In this situation, parent process of this process and its name is get. Finally name check for this process name is made (if name is "bash").
    if parent_process_name.startswith("system-monitori") == True:                             # Process name is used as "system-monitori" because linux kernel gives first 16 (15) characters of the process name and there is no need for getting full name of the process in this case.
        with open("/proc/" + ppid_of_application + "/stat") as reader:                        # Similar information with the "/proc/stat" file is also in the "/proc/status" file but parsing this file is faster since data in this file is single line and " " delimited.  For information about "/proc/stat" psedo file, see "https://man7.org/linux/man-pages/man5/proc.5.html".
            ppid_of_application = reader.read().split()[-49]
        with open("/proc/" + ppid_of_application + "/comm") as reader:
            parent_process_name = reader.read().strip()
        if parent_process_name == "bash":
            label7101.set_text(_tr("Listing environment/shell variables is not supported when application is run in terminal."))
            return

    # Define global variables and get treeview columns, sort column/order, column widths, etc.
    global environment_variables_treeview_columns_shown
    global environment_variables_treeview_columns_shown_prev, environment_variables_data_row_sorting_column_prev, environment_variables_data_row_sorting_order_prev, environment_variables_data_column_order_prev, environment_variables_data_column_widths_prev
    environment_variables_treeview_columns_shown = Config.environment_variables_treeview_columns_shown
    environment_variables_data_row_sorting_column = Config.environment_variables_data_row_sorting_column
    environment_variables_data_row_sorting_order = Config.environment_variables_data_row_sorting_order
    environment_variables_data_column_order = Config.environment_variables_data_column_order
    environment_variables_data_column_widths = Config.environment_variables_data_column_widths

    # Define global variables and empty lists for the current loop
    global environment_variables_data_rows, environment_variables_data_rows_prev, variable_list, variable_list_prev, variable_type_list
    environment_variables_data_rows = []
    variable_list = []
    variable_type_list = []

    # Get environment variabes and shell variables
    printenv_output_lines = subprocess.check_output("/bin/bash -i -c printenv", shell=True).strip().decode().split("_=")[0].split("\n")    # Variables with name starting with "_" are not get. "-i" is used in order to get variables which are get from "printenv" command typed by human user. Otherwise there are different results.
    set_output_lines = subprocess.check_output("/bin/bash -i -c set", shell=True).decode().split("_=")[0].split("\n")    # Variables with name starting with "_" are not get. "-i" is used in order to get variables which are get from "printenv" command typed by human user. Otherwise there are different results.

    # Join Environment and Shell Variables in a list (variable_list). Shell variables output (from "set" command) also contains environment variables. These are removed for preventing dublicated variables.
    variable_list = list(printenv_output_lines)
    for line in set_output_lines:
        if line not in printenv_output_lines:
            variable_list.append(line)
    try:
        variable_list.remove("")
    except ValueError:
        pass
    variable_list = sorted(variable_list)

    # Get variables data (specific information by processing the data get previously)
    for variable in variable_list:
        variable_split = variable.split("=")
        # Get variable type (environment variable/shell variable). This data will be used for filtering (search, etc.) variables.
        if variable in printenv_output_lines and variable not in set_output_lines:
            variable_type = _tr("Environment Variable")
            variable_type_image = environment_variable_image
        if variable in set_output_lines and variable not in printenv_output_lines:
            variable_type = _tr("Shell Variable")
            variable_type_image = shell_variable_image
        if variable in printenv_output_lines and variable in set_output_lines:
            variable_type = _tr("Environment & Shell Variable")
            variable_type_image = environment_shell_variable_image
        variable_type_list.append(variable_type)
        # Append variable name
        environment_variables_data_row = [True, variable_split[0]]                            # Variable visibility data (on treeview) which is used for showing/hiding variable when variables in specific type (environment/shell variable) is preferred to be shown or variable search feature is used from the GUI.
        # Append variable value
        if 1 in environment_variables_treeview_columns_shown:
            environment_variables_data_row.append('='.join(variable_split[1:]))               # There may be more than "=" in the VARIABLE=VALUE string. String later than first "=" is get as value.
        # Append variable type icon and variable type
        if 2 in environment_variables_treeview_columns_shown:
            environment_variables_data_row.extend((variable_type_image, variable_type))
        # Append all data of the variables into a list which will be appended into a treestore for showing the data on a treeview.
        environment_variables_data_rows.append(environment_variables_data_row)

    # Add/Remove treeview columns appropriate for user preferences
    treeview7101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    if environment_variables_treeview_columns_shown != environment_variables_treeview_columns_shown_prev:    # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        for column in treeview7101.get_columns():                                             # Remove all columns in the treeview.
            treeview7101.remove_column(column)
        for i, column in enumerate(environment_variables_treeview_columns_shown):
            if environment_variables_data_list[column][0] in environment_variables_treeview_columns_shown:
                cumulative_sort_column_id = cumulative_sort_column_id + environment_variables_data_list[column][2]
            environment_variables_treeview_column = Gtk.TreeViewColumn(environment_variables_data_list[column][1])    # Define column (also column title is defined)
            for i, cell_renderer_type in enumerate(environment_variables_data_list[column][6]):
                cumulative_internal_data_id = cumulative_internal_data_id + 1
                if cell_renderer_type == "internal_column":                                   # Continue to next loop to avoid generating a cell renderer for internal column (internal columns are not shon on the treeview and they do not have cell renderers).
                    continue
                if cell_renderer_type == "CellRendererPixbuf":                                # Define cell renderer
                    cell_renderer = Gtk.CellRendererPixbuf()
                if cell_renderer_type == "CellRendererText":                                  # Define cell renderer
                    cell_renderer = Gtk.CellRendererText()
                cell_renderer.set_alignment(environment_variables_data_list[column][9][i], 0.5)    # Vertical alignment is set 0.5 in order to leave it as unchanged.
                environment_variables_treeview_column.pack_start(cell_renderer, environment_variables_data_list[column][10][i])    # Set if column will allocate unused space
                environment_variables_treeview_column.add_attribute(cell_renderer, environment_variables_data_list[column][7][i], cumulative_internal_data_id)
                if environment_variables_data_list[column][11][i] != "no_cell_function":
                    environment_variables_treeview_column.set_cell_data_func(cell_renderer, environment_variables_data_list[column][11][i], func_data=cumulative_internal_data_id)    # Define cell function which sets cell data precision and/or data unit
            environment_variables_treeview_column.set_sizing(2)                               # Set column sizing (2 = auto sizing which is required for "treeview7101.set_fixed_height_mode(True)" command that is used for lower treeview CPU consumption because row heights are not calculated for every row).
            environment_variables_treeview_column.set_sort_column_id(cumulative_sort_column_id)    # Be careful with lists contain same element more than one.
            environment_variables_treeview_column.set_resizable(True)                         # Set columns resizable by the user when column title button edge handles are dragged.
            environment_variables_treeview_column.set_reorderable(True)                       # Set columns reorderable by the user when column title buttons are dragged.
            environment_variables_treeview_column.set_min_width(40)                           # Set minimum column widths as "40 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            environment_variables_treeview_column.connect("clicked", on_column_title_clicked)    # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
            treeview7101.append_column(environment_variables_treeview_column)                 # Append column into treeview

        # Get column data types for appending environment variables data into treestore
        environment_variables_data_column_types = []
        for column in sorted(environment_variables_treeview_columns_shown):
            internal_column_count = len(environment_variables_data_list[column][5])
            for internal_column_number in range(internal_column_count):
                environment_variables_data_column_types.append(environment_variables_data_list[column][5][internal_column_number])    # Get column types (int, bool, float, str, etc.)

        # Define a treestore (for storing treeview data in it), a treemodelfilter (for search filtering), treemodelsort (for row sorting when column title buttons are clicked)
        global treestore7101                                                                  # Define as global variable because treestore is generated in statement and will not be defined in every loop and it will be used outside the statement.
        treestore7101 = Gtk.TreeStore()
        treestore7101.set_column_types(environment_variables_data_column_types)               # Set column types of the columns which will be appended into treestore
        treemodelfilter7101 = treestore7101.filter_new()
        treemodelfilter7101.set_visible_column(0)                                             # Column "0" of the treestore will be used for column visibility information (True or False)
        treemodelsort7101 = Gtk.TreeModelSort(treemodelfilter7101)
        treeview7101.set_model(treemodelsort7101)
        variable_list_prev = []                                                               # Redefine (clear) "variable_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
        global piter_list
        piter_list = []
    treeview7101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
    if environment_variables_treeview_columns_shown_prev != environment_variables_treeview_columns_shown or environment_variables_data_column_order_prev != environment_variables_data_column_order:
        environment_variables_treeview_columns = treeview7101.get_columns()                   # Get shown columns on the treeview in order to use this data for reordering the columns.
        environment_variables_treeview_columns_modified = treeview7101.get_columns()
        treeview_column_titles = []
        for column in environment_variables_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for order in reversed(sorted(environment_variables_data_column_order)):               # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
            if environment_variables_data_column_order.index(order) <= len(environment_variables_treeview_columns) - 1 and environment_variables_data_column_order.index(order) in environment_variables_treeview_columns_shown:
                column_number_to_move = environment_variables_data_column_order.index(order)
                column_title_to_move = environment_variables_data_list[column_number_to_move][1]
                column_to_move = environment_variables_treeview_columns[treeview_column_titles.index(column_title_to_move)]
                column_title_to_move = column_to_move.get_title()
                for data in environment_variables_data_list:
                    if data[1] == column_title_to_move:
                        treeview7101.move_column_after(column_to_move, None)                  # Column is moved at the beginning of the treeview if "None" is used.

    # Sort environment variable rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
    if environment_variables_treeview_columns_shown_prev != environment_variables_treeview_columns_shown or environment_variables_data_row_sorting_column_prev != environment_variables_data_row_sorting_column or environment_variables_data_row_sorting_order != environment_variables_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
        environment_variables_treeview_columns = treeview7101.get_columns()                   # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_column_titles = []
        for column in environment_variables_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i in range(10):
            if environment_variables_data_row_sorting_column in environment_variables_treeview_columns_shown:
                for data in environment_variables_data_list:
                    if data[0] == environment_variables_data_row_sorting_column:
                        column_title_for_sorting = data[1]
            if environment_variables_data_row_sorting_column not in environment_variables_treeview_columns_shown:
                column_title_for_sorting = environment_variables_data_list[0][1]
            column_for_sorting = environment_variables_treeview_columns[treeview_column_titles.index(column_title_for_sorting)]
            column_for_sorting.clicked()                                                      # For row sorting.
            if environment_variables_data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                break

    # Set column widths if there are changes since last loop.
    if environment_variables_treeview_columns_shown_prev != environment_variables_treeview_columns_shown or environment_variables_data_column_widths_prev != environment_variables_data_column_widths:
        environment_variables_treeview_columns = treeview7101.get_columns()
        treeview_column_titles = []
        for column in environment_variables_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i, environment_variables_data in enumerate(environment_variables_data_list):
            for j, column_title in enumerate(treeview_column_titles):
                if column_title == environment_variables_data[1]:
                   column_width = environment_variables_data_column_widths[i]
                   environment_variables_treeview_columns[j].set_fixed_width(column_width)    # Set column width in pixels. Fixed width is unset if value is "-1".

    # Get new/deleted(ended) environment variables for updating treestore/treeview
    variable_list_prev_set = set(variable_list_prev)
    variable_list_set = set(variable_list)
    deleted_variables = sorted(list(variable_list_prev_set - variable_list_set))
    new_variables = sorted(list(variable_list_set - variable_list_prev_set))
    existing_variables = sorted(list(variable_list_set.intersection(variable_list_prev)))
    updated_existing_environment_variables_index = [[variable_list.index(i), variable_list_prev.index(i)] for i in existing_variables]    # "c = set(a).intersection(b)" is about 19% faster than "c = set(a).intersection(set(b))"
    environment_variables_data_rows_row_length = len(environment_variables_data_rows[0])

    # Append/Remove/Update environment variables data into treestore
    treeview7101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    global variable_search_text, filter_column
    if len(piter_list) > 0:
        for i, j in updated_existing_environment_variables_index:
            if environment_variables_data_rows[i] != environment_variables_data_rows_prev[j]:
                for k in range(1, environment_variables_data_rows_row_length):                # Start from "1" in order to set first element (treeview row visibility data) as "True" in every loop.
                    if environment_variables_data_rows_prev[j][k] != environment_variables_data_rows[i][k]:
                        treestore7101.set_value(piter_list[j], k, environment_variables_data_rows[i][k])
    if len(deleted_variables) > 0:
        for variable in reversed(sorted(list(deleted_variables))):
            treestore7101.remove(piter_list[variable_list_prev.index(variable)])
            piter_list.remove(piter_list[variable_list_prev.index(variable)])
    if len(new_variables) > 0:
        for variable in new_variables:
            # /// Start /// This block of code is used for determining if the newly added variable will be shown on the treeview (user search actions and/or search customizations and/or "Show all environment/shell variables" preference affect variable visibility).
            if radiobutton7102.get_active() == True and variable_type_list[variable_list.index(variable)] != True:    # Hide variable (set the visibility value as "False") if "Show all environment variables" option is selected on the GUI and variable visibility is not "True".
                environment_variables_data_rows[variable_list.index(variable)][0] = False
            if radiobutton7103.get_active() == True and variable_type_list[variable_list.index(variable)] == True:    # Hide variable (set the visibility value as "False") if "Show all shell variables" option is selected on the GUI and variable visibility is "True".
                environment_variables_data_rows[variable_list.index(variable)][0] = False
            if searchentry7101.get_text() != "":
                variable_search_text = searchentry7101.get_text()
                variable_data_text_in_model = environment_variables_data_rows[variable_list.index(variable)][filter_column]
                if variable_search_text not in str(variable_data_text_in_model).lower():      # Hide variable (set the visibility value as "False") if search text (typed into the search entry) is not in the appropriate column of the variable data.
                    environment_variables_data_rows[variable_list.index(variable)][0] = False
            # \\\ End \\\ This block of code is used for determining if the newly added variable will be shown on the treeview (user search actions and/or search customizations and/or "Show all environment/shell variables" preference affect variable visibility).
            piter_list.insert(variable_list.index(variable), treestore7101.insert(None, variable_list.index(variable), environment_variables_data_rows[variable_list.index(variable)]))    # "insert" have to be used for appending element into both "piter_list" and "treestore" in order to avoid data index problems which are caused by sorting of variable names (this sorting is performed for getting list differences).
    treeview7101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    variable_list_prev = variable_list                                                        # For using values in the next loop
    environment_variables_data_rows_prev = environment_variables_data_rows
    environment_variables_treeview_columns_shown_prev = environment_variables_treeview_columns_shown
    environment_variables_data_row_sorting_column_prev = environment_variables_data_row_sorting_column
    environment_variables_data_row_sorting_order_prev = environment_variables_data_row_sorting_order
    environment_variables_data_column_order_prev = environment_variables_data_column_order
    environment_variables_data_column_widths_prev = environment_variables_data_column_widths

    # Get number of shell variables and number of all variables and show these information on the GUI label
    shell_variable_count = variable_type_list.count(_tr("Shell Variable")) + variable_type_list.count(_tr("Environment & Shell Variable"))
    environment_variable_count = variable_type_list.count(_tr("Environment Variable")) + variable_type_list.count(_tr("Environment & Shell Variable"))
    number_of_all_variables = len(variable_type_list)
    label7101.set_text(_tr("Total: ") + str(number_of_all_variables) + _tr(" persistent variables (") + str(environment_variable_count) + _tr(" environment variables, ") + str(shell_variable_count) + _tr(" shell variables)"))    # f strings have lower CPU usage than joining method but strings are joinied by by this method because gettext could not be worked with Python f strings.


# ----------------------------------- Environment Variables Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def environment_variables_initial_thread_func():

    GLib.idle_add(environment_variables_initial_func)


# ----------------------------------- Environment Variables Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def environment_variables_loop_thread_func(*args):                                            # "*args" is used in order to prevent "" warning and obtain a repeated function by using "GLib.timeout_source_new()". "GLib.timeout_source_new()" is used instead of "GLib.timeout_add()" to be able to prevent running multiple instances of the functions at the same time when a tab is switched off and on again in the update_interval time. Using "return" with "GLib.timeout_add()" is not enough in this repetitive tab switch case. "GLib.idle_add()" is shorter but programmer has less control.

    if MainGUI.radiobutton7.get_active() == True:
        global environment_variables_glib_source, update_interval                             # GLib source variable name is defined as global to be able to destroy it if tab is switched back in update_interval time.
        try:                                                                                  # "try-except" is used in order to prevent errors if this is first run of the function.
            environment_variables_glib_source.destroy()                                       # Destroy GLib source for preventing it repeating the function.
        except NameError:
            pass
        update_interval = Config.update_interval
        environment_variables_glib_source = GLib.timeout_source_new(update_interval * 1000)
        GLib.idle_add(environment_variables_loop_func)
        environment_variables_glib_source.set_callback(environment_variables_loop_thread_func)
        environment_variables_glib_source.attach(GLib.MainContext.default())                  # Attach GLib.Source to MainContext. Therefore it will be part of the main loop until it is destroyed. A function may be attached to the MainContext multiple times.


# ----------------------------------- Environment Variables Thread Run Function (starts execution of the threads) -----------------------------------
def environment_variables_thread_run_func():

    if "environment_variables_data_rows" not in globals():                                    # To be able to run initial thread for only one time
        environment_variables_initial_thread = Thread(target=environment_variables_initial_thread_func, daemon=True)
        environment_variables_initial_thread.start()
        environment_variables_initial_thread.join()
    environment_variables_loop_thread = Thread(target=environment_variables_loop_thread_func, daemon=True)
    environment_variables_loop_thread.start()


# ----------------------------------- Environment Variables - Treeview Filter Show All Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def environment_variables_treeview_filter_show_all_func():

    for piter in piter_list:
        treestore7101.set_value(piter, 0, True)


# ----------------------------------- Environment Variables - Treeview Filter Show All Environment Variables Items Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def environment_variables_treeview_filter_environment_variables_logged_in_only():

    for piter in piter_list:
        if variable_type_list[piter_list.index(piter)] == _tr("Shell Variable"):
            treestore7101.set_value(piter, 0, False)


# ----------------------------------- Environment Variables - Treeview Filter Show All Shell Variables Items Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def environment_variables_treeview_filter_environment_variables_logged_out_only():

    for piter in piter_list:
        if variable_type_list[piter_list.index(piter)] == _tr("Environment Variable"):
            treestore7101.set_value(piter, 0, False)


# ----------------------------------- Environment Variables - Treeview Filter Search Function (updates treeview shown rows when text typed into entry) -----------------------------------
def environment_variables_treeview_filter_search_func():

    global filter_column
    variable_search_text = searchentry7101.get_text().lower()
    # Set visible/hidden variables
    for piter in piter_list:
        treestore7101.set_value(piter, 0, False)
        variable_data_text_in_model = treestore7101.get_value(piter, filter_column)
        if variable_search_text in str(variable_data_text_in_model).lower():
            treestore7101.set_value(piter, 0, True)


# ----------------------------------- Environment Variables - Column Title Clicked Function (gets treeview column number (id) and row sorting order by being triggered by Gtk signals) -----------------------------------
def on_column_title_clicked(widget):

    environment_variables_data_row_sorting_column_title = widget.get_title()                  # Get column title which will be used for getting column number
    for data in environment_variables_data_list:
        if data[1] == environment_variables_data_row_sorting_column_title:
            Config.environment_variables_data_row_sorting_column = data[0]                    # Get column number
    Config.environment_variables_data_row_sorting_order = int(widget.get_sort_order())        # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    Config.config_save_func()


# ----------------------------------- Environment Variables - Treeview Column Order-Width Row Sorting Function (gets treeview column order/widths and row sorting) -----------------------------------
def environment_variables_treeview_column_order_width_row_sorting_func():
    # Columns in the treeview are get one by one and appended into "environment_variables_data_column_order". "environment_variables_data_column_widths" list elements are modified for widths of every columns in the treeview. Length of these list are always same even if columns are removed, appended and column widths are changed. Only values of the elements (element indexes are always same with "environment_variables_data") are changed if column order/widths are changed.
    environment_variables_treeview_columns = treeview7101.get_columns()
    treeview_column_titles = []
    for column in environment_variables_treeview_columns:
        treeview_column_titles.append(column.get_title())
    for i, environment_variables_data in enumerate(environment_variables_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == environment_variables_data[1]:
                Config.environment_variables_data_column_order[i] = j
                Config.environment_variables_data_column_widths[i] = environment_variables_treeview_columns[j].get_width()
                break
    Config.config_save_func()

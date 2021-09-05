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


    global Config, MainGUI, EnvironmentVariablesGUI, EnvironmentVariablesMenusGUI
    import Config, MainGUI, EnvironmentVariablesGUI, EnvironmentVariablesMenusGUI


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

    global environment_variable_image, shell_variable_image
    environment_variable_image = "system-monitoring-center-environment-variables-symbolic"    # Will be used as image of the environment_variables
    shell_variable_image = "system-monitoring-center-terminal-symbolic"                       # Will be used as image of the shell_variables

    environment_variable_type_text_list = [_tr("Environment Variable"), _tr("Shell Variable")]    # This list is defined in order to make English variable type information to be translated into other languages.


# ----------------------------------- Environment Variables - Get EnvironmentVariables Data Function (gets environment_variables data, adds into treeview and updates it) -----------------------------------
def environment_variables_loop_func():

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
    printenv_output_lines = subprocess.check_output("printenv", shell=True, executable='/bin/bash').strip().decode().split("_=")[0].split("\n")    # Variables with name starting with "_" are not get.
    set_output_lines = subprocess.check_output("set", shell=True, executable='/bin/bash').strip().decode().split("_=")[0].split("\n")    # Variables with name starting with "_" are not get.

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
        if variable in printenv_output_lines:
            variable_type = "Environment Variable"
            variable_type_image = environment_variable_image
        if variable not in printenv_output_lines:
            variable_type = "Shell Variable"
            variable_type_image = shell_variable_image
        variable_type_list.append(variable_type)
        # Append variable name
        environment_variables_data_row = [True, variable_split[0]]                            # Variable visibility data (on treeview) which is used for showing/hiding variable when variables in specific type (environment/shell variable) is preferred to be shown or variable search feature is used from the GUI.
        # Append variable value
        if 1 in environment_variables_treeview_columns_shown:
            environment_variables_data_row.append(variable_split[1])
        # Append variable type icon and variable type
        if 2 in environment_variables_treeview_columns_shown:
            environment_variables_data_row.extend((variable_type_image, variable_type))
        # Append all data of the variables into a list which will be appended into a treestore for showing the data on a treeview.
        environment_variables_data_rows.append(environment_variables_data_row)

    # Add/Remove treeview columns appropriate for user preferences
    EnvironmentVariablesGUI.treeview7101.freeze_child_notify()                                # For lower CPU consumption by preventing treeview updates on content changes/updates.
    if environment_variables_treeview_columns_shown != environment_variables_treeview_columns_shown_prev:    # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        for column in EnvironmentVariablesGUI.treeview7101.get_columns():                     # Remove all columns in the treeview.
            EnvironmentVariablesGUI.treeview7101.remove_column(column)
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
            EnvironmentVariablesGUI.treeview7101.append_column(environment_variables_treeview_column)    # Append column into treeview

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
        EnvironmentVariablesGUI.treeview7101.set_model(treemodelsort7101)
        variable_list_prev = []                                                               # Redefine (clear) "variable_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.
        global piter_list
        piter_list = []
    EnvironmentVariablesGUI.treeview7101.thaw_child_notify()                                  # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
    if environment_variables_treeview_columns_shown_prev != environment_variables_treeview_columns_shown or environment_variables_data_column_order_prev != environment_variables_data_column_order:
        environment_variables_treeview_columns = EnvironmentVariablesGUI.treeview7101.get_columns()    # Get shown columns on the treeview in order to use this data for reordering the columns.
        environment_variables_treeview_columns_modified = EnvironmentVariablesGUI.treeview7101.get_columns()
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
                        EnvironmentVariablesGUI.treeview7101.move_column_after(column_to_move, None)    # Column is moved at the beginning of the treeview if "None" is used.

    # Sort environment variable rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
    if environment_variables_treeview_columns_shown_prev != environment_variables_treeview_columns_shown or environment_variables_data_row_sorting_column_prev != environment_variables_data_row_sorting_column or environment_variables_data_row_sorting_order != environment_variables_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
        environment_variables_treeview_columns = EnvironmentVariablesGUI.treeview7101.get_columns()    # Get shown columns on the treeview in order to use this data for reordering the columns.
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
        environment_variables_treeview_columns = EnvironmentVariablesGUI.treeview7101.get_columns()
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
    EnvironmentVariablesGUI.treeview7101.freeze_child_notify()                                # For lower CPU consumption by preventing treeview updates on content changes/updates.
    global variable_search_text, filter_variable_type, filter_column
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
            if EnvironmentVariablesGUI.radiobutton7102.get_active() == True and variable_type_list[variable_list.index(variable)] != True:    # Hide variable (set the visibility value as "False") if "Show all environment variables" option is selected on the GUI and variable visibility is not "True".
                environment_variables_data_rows[variable_list.index(variable)][0] = False
            if EnvironmentVariablesGUI.radiobutton7103.get_active() == True and variable_type_list[variable_list.index(variable)] == True:    # Hide variable (set the visibility value as "False") if "Show all shell variables" option is selected on the GUI and variable visibility is "True".
                environment_variables_data_rows[variable_list.index(variable)][0] = False
            if EnvironmentVariablesGUI.searchentry7101.get_text() != "":
                variable_data_text_in_model = environment_variables_data_rows[variable_list.index(variable)][filter_column]
                varible_type_in_model = variable_type_list[variable_list.index(variable)]
                if variable_search_text not in str(variable_data_text_in_model).lower():      # Hide variable (set the visibility value as "False") if search text (typed into the search entry) is not in the appropriate column of the variable data.
                    environment_variables_data_rows[variable_list.index(variable)][0] = False
                if varible_type_in_model not in filter_variable_type:                         # Hide variable (set the visibility value as "False") if visibility data of the variable is not in the filter_variable_type (this list is constructed by using user preferred options on the "Environment Variable Search Customizations" tab).
                    environment_variables_data_rows[variable_list.index(variable)][0] = False
            # \\\ End \\\ This block of code is used for determining if the newly added variable will be shown on the treeview (user search actions and/or search customizations and/or "Show all environment/shell variables" preference affect variable visibility).
            piter_list.insert(variable_list.index(variable), treestore7101.insert(None, variable_list.index(variable), environment_variables_data_rows[variable_list.index(variable)]))    # "insert" have to be used for appending element into both "piter_list" and "treestore" in order to avoid data index problems which are caused by sorting of variable names (this sorting is performed for getting list differences).
    EnvironmentVariablesGUI.treeview7101.thaw_child_notify()                                  # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    variable_list_prev = variable_list                                                        # For using values in the next loop
    environment_variables_data_rows_prev = environment_variables_data_rows
    environment_variables_treeview_columns_shown_prev = environment_variables_treeview_columns_shown
    environment_variables_data_row_sorting_column_prev = environment_variables_data_row_sorting_column
    environment_variables_data_row_sorting_order_prev = environment_variables_data_row_sorting_order
    environment_variables_data_column_order_prev = environment_variables_data_column_order
    environment_variables_data_column_widths_prev = environment_variables_data_column_widths

    # Get number of shell variables and number of all variables and show these information on the GUI label
    shell_variable_count = variable_type_list.count("Shell Variable")
    number_of_all_variables = len(variable_type_list)
    EnvironmentVariablesGUI.label7101.set_text(_tr("Total: ") + str(number_of_all_variables) + _tr(" variables (") + str(shell_variable_count) + _tr(" environment variables, ") + str(number_of_all_variables-shell_variable_count) + _tr(" shell variables)"))    # f strings have lower CPU usage than joining method but strings are joinied by by this method because gettext could not be worked with Python f strings.


# ----------------------------------- Environment Variables Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def environment_variables_initial_thread_func():

    GLib.idle_add(environment_variables_initial_func)


# ----------------------------------- Environment Variables Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def environment_variables_loop_thread_func():

    GLib.idle_add(environment_variables_loop_func)
    if MainGUI.radiobutton7.get_active() is True:                                             # "is/is not" is about 15% faster than "==/!="
        global update_interval
        update_interval = Config.update_interval
        GLib.timeout_add(update_interval * 1000, environment_variables_loop_thread_func)


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


# ----------------------------------- Environment Variables - Treeview Filter Show All Enabled (Visible) Environment Variables Items Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def environment_variables_treeview_filter_environment_variables_logged_in_only():

    for piter in piter_list:
        if variable_type_list[piter_list.index(piter)] != "Environment Variable":
            treestore7101.set_value(piter, 0, False)


# ----------------------------------- Environment Variables - Treeview Filter Show All Disabled (Hidden) Environment Variables Items Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def environment_variables_treeview_filter_environment_variables_logged_out_only():

    for piter in piter_list:
        if variable_type_list[piter_list.index(piter)] != "Shell Variable":
            treestore7101.set_value(piter, 0, False)


# ----------------------------------- Environment Variables - Treeview Filter Search Function (updates treeview shown rows when text typed into entry) -----------------------------------
def environment_variables_treeview_filter_search_func():

    # Determine filtering column (Service name, load state, active state, etc.) for hiding/showing variables by using search text typed into search entry.
    global variable_search_text, filter_variable_type, filter_column
    environment_variables_treeview_columns_shown_sorted = sorted(environment_variables_treeview_columns_shown)
    if EnvironmentVariablesMenusGUI.radiobutton7101p2.get_active() == True:
        if 0 in environment_variables_treeview_columns_shown:                                 # "0" is treeview column number
            filter_column = 1                                                                 # Append internal column number (1) of "variable" for filtering
    if EnvironmentVariablesMenusGUI.radiobutton7102p2.get_active() == True:
        if 1 in environment_variables_treeview_columns_shown:                                 # "1" is treeview column number
            filter_column = 2                                                                 # Append internal column number (2) of "value" for filtering
    # Variable could be shown/hidden for environment/shell variable type. Preferred visibility data is determined here.
    filter_variable_type = []
    if EnvironmentVariablesMenusGUI.checkbutton7102p2.get_active() == True:
        filter_variable_type.append("Environment Variable")
    if EnvironmentVariablesMenusGUI.checkbutton7103p2.get_active() == True:
        filter_variable_type.append("Shell Variable")

    variable_search_text = EnvironmentVariablesGUI.searchentry7101.get_text().lower()
    # Set visible/hidden variables
    for piter in piter_list:
        treestore7101.set_value(piter, 0, False)
        variable_data_text_in_model = treestore7101.get_value(piter, filter_column)
        if variable_search_text in str(variable_data_text_in_model).lower():
            treestore7101.set_value(piter, 0, True)
            variable_type_in_model = variable_type_list[piter_list.index(piter)]
            if variable_type_in_model not in filter_variable_type:
                treestore7101.set_value(piter, 0, False)


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
    environment_variables_treeview_columns = EnvironmentVariablesGUI.treeview7101.get_columns()
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

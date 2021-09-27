#!/usr/bin/env python3

# ----------------------------------- Services - Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def services_import_func():

    global Gtk, Gdk, GLib, GObject, Thread, subprocess, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib, GObject
    from threading import Thread
    import subprocess
    import os


    global Config, MainGUI, ServicesGUI, ServicesMenusGUI
    import Config, MainGUI, ServicesGUI, ServicesMenusGUI


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


# ----------------------------------- Services - Initial Function (contains initial code which defines some variables and gets data which is not wanted to be run in every loop) -----------------------------------
def services_initial_func():

    # data list explanation:
    # services_data_list = [
    #                      [treeview column number, treeview column title, internal column count, cell renderer count, treeview column sort column id, [data type 1, data type 2, ...], [cell renderer type 1, cell renderer type 2, ...], [cell attribute 1, cell attribute 2, ...], [cell renderer data 1, cell renderer data 2, ...], [cell left/right alignment 1, cell left/right alignment 2, ...], [set expand 1 {if cell will allocate unused space} cell expand 2, ...], [cell function 1, cell function 2, ...]]
    #                      .
    #                      .
    #                      ]
    global services_data_list
    services_data_list = [
                         [0, _tr('Service Name'), 3, 2, 3, [bool, str, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'icon_name', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
                         [1, _tr('State'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                         [1, _tr('Main PID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                         [1, _tr('Active State'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                         [1, _tr('Load State'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                         [1, _tr('Sub-State'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                         [1, _tr('Memory (RSS)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_ram]],
                         [1, _tr('Description'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']]
                         ]

    services_define_data_unit_converter_variables_func()                                      # This function is called in order to define data unit conversion variables before they are used in the function that is called from following code.

    global services_data_rows_prev, service_list_prev, piter_list, services_treeview_columns_shown_prev, services_data_row_sorting_column_prev, services_data_row_sorting_order_prev, services_data_column_order_prev, services_data_column_widths_prev
    services_data_rows_prev = []
    service_list_prev = []
    piter_list = []
    services_treeview_columns_shown_prev = []
    services_data_row_sorting_column_prev = ""
    services_data_row_sorting_order_prev = ""
    services_data_column_order_prev = []
    services_data_column_widths_prev = []

    global services_image
    services_image = "system-monitoring-center-services-symbolic"                             # Will be used as image of the services
    services_loop_func()

    service_state_list = [_tr("enabled"), _tr("disabled"), _tr("masked"), _tr("unmasked"), _tr("static"), _tr("generated"), _tr("enabled-runtime"), _tr("indirect"), _tr("active"), _tr("inactive"), _tr("loaded"), _tr("dead"), _tr("exited"), _tr("running")]    # This list is defined in order to make English service state names to be translated into other languages.
    services_other_text_list = [_tr("yes"), _tr("no")]                                        # This list is defined in order to make English service information to be translated into other languages.


# ----------------------------------- Services - Get Services Data Function (gets services data, adds into treeview and updates it) -----------------------------------
def services_loop_func():

    # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
    global services_ram_swap_data_precision, services_ram_swap_data_unit
    services_ram_swap_data_precision = Config.services_ram_swap_data_precision
    services_ram_swap_data_unit = Config.services_ram_swap_data_unit

    # Define global variables and get treeview columns, sort column/order, column widths, etc.
    global services_treeview_columns_shown
    global services_treeview_columns_shown_prev, services_data_row_sorting_column_prev, services_data_row_sorting_order_prev, services_data_column_order_prev, services_data_column_widths_prev
    services_treeview_columns_shown = Config.services_treeview_columns_shown
    services_data_row_sorting_column = Config.services_data_row_sorting_column
    services_data_row_sorting_order = Config.services_data_row_sorting_order
    services_data_column_order = Config.services_data_column_order
    services_data_column_widths = Config.services_data_column_widths

    # Get service file names and define global variables and empty lists for the current loop
    global services_data_rows, services_data_rows_prev, service_list, service_list_prev, service_loaded_not_loaded_list
    services_data_rows = []
    service_list = []
    service_loaded_not_loaded_list = []

    # Service files (Unit files) are in the "/etc/systemd/system/" and "/usr/lib/systemd/system/autovt@.service" directories. But the first directory contains links to the service files in the second directory. Thus, service files get from the second directory.
    service_unit_file_list = [filename for filename in os.listdir("/usr/lib/systemd/system/") if filename.endswith(".service")]    # Get file names which ends withs ".service".
    service_files_from_run_systemd_list = [filename.split("invocation:")[1] for filename in os.listdir("/run/systemd/units/")]    # "/run/systemd/units/" directory contains loaded and non-dead services.

    for file in service_unit_file_list[:]:                                                    # "[:]" is used for iterating over copy of the list because elements are removed during iteration. Otherwise incorrect operations (incorrect element removals) are performed on the list.
        if os.path.islink("/usr/lib/systemd/system/" + file) == True and os.path.realpath("/usr/lib/systemd/system/" + file) != "/dev/null":    # Some service files are link to other ".service" files in the same directory. These links are removed from the list. Not all link files are removed. Link files with "/dev/null" are kept in the list.
            service_unit_file_list.remove(file)

    # Get all service names (joining service names from "systemctl list-unit-files ..." and "systemctl list-units ..."). Some services are run multiple times. For example there is one instance of "user@.service" from ""systemctl list-unit-files ..." command but there are two loaded services (user@1000.service and user@1001.service) per logged in user. There are several examples for this situation. "user@.service" is removed from list, "user@1000.service" and "user@1001.service" appended into list for getting information for all services correctly.
    for service_unit_file in service_unit_file_list:
        if "@" not in service_unit_file:
            service_list.append(service_unit_file)
            continue
        if "@" in service_unit_file:
            service_unit_file_split = service_unit_file.split("@")[0]
            for service_loaded in service_files_from_run_systemd_list:
                if "@" in service_loaded and service_unit_file_split == service_loaded.split("@")[0]:
                    service_list.append(service_loaded)
                    continue
    service_list = sorted(service_list)

    # Generate "unit_files_command_parameter_list". This list will be used for constructing commandline for getting service data per service file.
    unit_files_command_parameter_list = ["LoadState"]                                         # This information is always get for filtering service, etc. Also it prevents errors if every columns other than service name are preferred not to be shown. It gives errors if no property is specified with "systemctl show [service_name] --property=" command.
    if 1 in services_treeview_columns_shown:
        unit_files_command_parameter_list.append("UnitFileState")
    if 2 in services_treeview_columns_shown:
        unit_files_command_parameter_list.append("MainPID")
    if 3 in services_treeview_columns_shown:
        unit_files_command_parameter_list.append("ActiveState")
    if 5 in services_treeview_columns_shown:
        unit_files_command_parameter_list.append("SubState")
    if 6 in services_treeview_columns_shown:
        unit_files_command_parameter_list.append("MemoryCurrent")
    if 7 in services_treeview_columns_shown:
        unit_files_command_parameter_list.append("Description")
    unit_files_command_parameter_list = ",".join(unit_files_command_parameter_list)           # Join strings with "," between them.
    # Construct command for getting service information for all services
    unit_files_command = ""
    for service in service_list:
        unit_files_command = unit_files_command + "\nsystemctl show " + service + " --property=" + unit_files_command_parameter_list + "\necho *split_line*"

    # Get service data per service file in one attempt in order to obtain lower CPU usage. Because information from all service files will be get by one commandline operation and will be parsed later.
    systemctl_show_command_lines = subprocess.check_output(unit_files_command, shell=True).decode().strip().split("\n*split_line*\n")

    # Get services data (specific information by processing the data get previously)
    for i, service in enumerate(service_list):
        systemctl_show_command_lines_split = systemctl_show_command_lines[i].split("\n")
        # Get service "loaded/not loaded" status. This data will be used for filtering (search, etc.) services.
        service_load_state = "-"                                                              # Initial value of "service_load_state" variable. This value will be used if "service_load_state" could not be detected.
        for line in systemctl_show_command_lines_split:
            if "LoadState=" in line:
                service_load_state = _tr(line.split("=")[1].capitalize())                     # "_tr([value])" is used for using translated string.
                if service_load_state == _tr("Loaded"):
                    service_loaded_not_loaded_list.append(True)
                    break
                if service_load_state != _tr("Loaded"):
                    service_loaded_not_loaded_list.append(False)
        # Append service icon and service name
        services_data_row = [True, services_image, service]                                   # Service visibility data (on treeview) which is used for showing/hiding service when services in specific type (enabled/disabled) is preferred to be shown or service search feature is used from the GUI.
        # Append service unit file state
        if 1 in services_treeview_columns_shown:
            for line in systemctl_show_command_lines_split:
                if "UnitFileState=" in line:
                    service_state = _tr(line.split("=")[1].capitalize())                      # "_tr([value])" is used for using translated string.
                    break
            services_data_row.append(service_state)
        # Append service unit file state
        if 2 in services_treeview_columns_shown:
            for line in systemctl_show_command_lines_split:
                if "MainPID=" in line:
                    service_main_pid = int(line.split("=")[1])
                    break
            services_data_row.append(service_main_pid)
        # Append service unit file state
        if 3 in services_treeview_columns_shown:
            for line in systemctl_show_command_lines_split:
                if "ActiveState=" in line:
                    service_active_state = _tr(line.split("=")[1].capitalize())               # "_tr([value])" is used for using translated string.
                    break
            services_data_row.append(service_active_state)
        # Append service unit file state (it has been get previously)
        if 4 in services_treeview_columns_shown:
            services_data_row.append(service_load_state)
        # Append service unit file state
        if 5 in services_treeview_columns_shown:
            for line in systemctl_show_command_lines_split:
                if "SubState=" in line:
                    service_sub_state = _tr(line.split("=")[1].capitalize())                  # "_tr([value])" is used for using translated string.
                    break
            services_data_row.append(service_sub_state)
        # Append service unit file state
        if 6 in services_treeview_columns_shown:
            for line in systemctl_show_command_lines_split:
                if "MemoryCurrent=" in line:
                    service_memory_current = line.split("=")[1]
                    if service_memory_current.startswith("["):
                        service_memory_current = -9999                                        # "-9999" value is used as "service_memory_current" value if memory value is get as "[not set]". Code will recognize this value and show "-" information in this situation. This negative integer value is used instead of string value because this data colmn of the treestore is an integer typed column.
                    else:
                        service_memory_current = int(service_memory_current)
                    break
            services_data_row.append(service_memory_current)
        # Append service unit file state
        if 7 in services_treeview_columns_shown:
            for line in systemctl_show_command_lines_split:
                if "Description=" in line:
                    service_description = line.split("=")[1]
                    break
            services_data_row.append(service_description)
        # Append all data of the services into a list which will be appended into a treestore for showing the data on a treeview.
        services_data_rows.append(services_data_row)

    # Add/Remove treeview columns appropriate for user preferences
    ServicesGUI.treeview6101.freeze_child_notify()                                            # For lower CPU consumption by preventing treeview updates on content changes/updates.
    if services_treeview_columns_shown != services_treeview_columns_shown_prev:               # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        for column in ServicesGUI.treeview6101.get_columns():                                 # Remove all columns in the treeview.
            ServicesGUI.treeview6101.remove_column(column)
        for i, column in enumerate(services_treeview_columns_shown):
            if services_data_list[column][0] in services_treeview_columns_shown:
                cumulative_sort_column_id = cumulative_sort_column_id + services_data_list[column][2]
            services_treeview_column = Gtk.TreeViewColumn(services_data_list[column][1])      # Define column (also column title is defined)
            for i, cell_renderer_type in enumerate(services_data_list[column][6]):
                cumulative_internal_data_id = cumulative_internal_data_id + 1
                if cell_renderer_type == "internal_column":                                   # Continue to next loop to avoid generating a cell renderer for internal column (internal columns are not shon on the treeview and they do not have cell renderers).
                    continue
                if cell_renderer_type == "CellRendererPixbuf":                                # Define cell renderer
                    cell_renderer = Gtk.CellRendererPixbuf()
                if cell_renderer_type == "CellRendererText":                                  # Define cell renderer
                    cell_renderer = Gtk.CellRendererText()
                cell_renderer.set_alignment(services_data_list[column][9][i], 0.5)            # Vertical alignment is set 0.5 in order to leave it as unchanged.
                services_treeview_column.pack_start(cell_renderer, services_data_list[column][10][i])    # Set if column will allocate unused space
                services_treeview_column.add_attribute(cell_renderer, services_data_list[column][7][i], cumulative_internal_data_id)
                if services_data_list[column][11][i] != "no_cell_function":
                    services_treeview_column.set_cell_data_func(cell_renderer, services_data_list[column][11][i], func_data=cumulative_internal_data_id)    # Define cell function which sets cell data precision and/or data unit
            services_treeview_column.set_sizing(2)                                            # Set column sizing (2 = auto sizing which is required for "treeview6101.set_fixed_height_mode(True)" command that is used for lower treeview CPU consumption because row heights are not calculated for every row).
            services_treeview_column.set_sort_column_id(cumulative_sort_column_id)            # Be careful with lists contain same element more than one.
            services_treeview_column.set_resizable(True)                                      # Set columns resizable by the user when column title button edge handles are dragged.
            services_treeview_column.set_reorderable(True)                                    # Set columns reorderable by the user when column title buttons are dragged.
            services_treeview_column.set_min_width(40)                                        # Set minimum column widths as "40 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            services_treeview_column.connect("clicked", on_column_title_clicked)              # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
            ServicesGUI.treeview6101.append_column(services_treeview_column)                  # Append column into treeview

        # Get column data types for appending services data into treestore
        services_data_column_types = []
        for column in sorted(services_treeview_columns_shown):
            internal_column_count = len(services_data_list[column][5])
            for internal_column_number in range(internal_column_count):
                services_data_column_types.append(services_data_list[column][5][internal_column_number])    # Get column types (int, bool, float, str, etc.)

        # Define a treestore (for storing treeview data in it), a treemodelfilter (for search filtering), treemodelsort (for row sorting when column title buttons are clicked)
        global treestore6101                                                                  # Define as global variable because treestore is generated in statement and will not be defined in every loop and it will be used outside the statement.
        treestore6101 = Gtk.TreeStore()
        treestore6101.set_column_types(services_data_column_types)                            # Set column types of the columns which will be appended into treestore
        treemodelfilter6101 = treestore6101.filter_new()
        treemodelfilter6101.set_visible_column(0)                                             # Column "0" of the treestore will be used for column visibility information (True or False)
        treemodelsort6101 = Gtk.TreeModelSort(treemodelfilter6101)
        ServicesGUI.treeview6101.set_model(treemodelsort6101)
        service_list_prev = []                                                                # Redefine (clear) "service_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.        global piter_list
        piter_list = []
    ServicesGUI.treeview6101.thaw_child_notify()                                              # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
    if services_treeview_columns_shown_prev != services_treeview_columns_shown or services_data_column_order_prev != services_data_column_order:
        services_treeview_columns = ServicesGUI.treeview6101.get_columns()                    # Get shown columns on the treeview in order to use this data for reordering the columns.
        services_treeview_columns_modified = ServicesGUI.treeview6101.get_columns()
        treeview_column_titles = []
        for column in services_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for order in reversed(sorted(services_data_column_order)):                            # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
            if services_data_column_order.index(order) <= len(services_treeview_columns) - 1 and services_data_column_order.index(order) in services_treeview_columns_shown:
                column_number_to_move = services_data_column_order.index(order)
                column_title_to_move = services_data_list[column_number_to_move][1]
                column_to_move = services_treeview_columns[treeview_column_titles.index(column_title_to_move)]
                column_title_to_move = column_to_move.get_title()
                for data in services_data_list:
                    if data[1] == column_title_to_move:
                        ServicesGUI.treeview6101.move_column_after(column_to_move, None)      # Column is moved at the beginning of the treeview if "None" is used.

    # Sort service rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
    if services_treeview_columns_shown_prev != services_treeview_columns_shown or services_data_row_sorting_column_prev != services_data_row_sorting_column or services_data_row_sorting_order != services_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
        services_treeview_columns = ServicesGUI.treeview6101.get_columns()                    # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_column_titles = []
        for column in services_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i in range(10):
            if services_data_row_sorting_column in services_treeview_columns_shown:
                for data in services_data_list:
                    if data[0] == services_data_row_sorting_column:
                        column_title_for_sorting = data[1]
            if services_data_row_sorting_column not in services_treeview_columns_shown:
                column_title_for_sorting = services_data_list[0][1]
            column_for_sorting = services_treeview_columns[treeview_column_titles.index(column_title_for_sorting)]
            column_for_sorting.clicked()                                                      # For row sorting.
            if services_data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                break

    # Set column widths if there are changes since last loop.
    if services_treeview_columns_shown_prev != services_treeview_columns_shown or services_data_column_widths_prev != services_data_column_widths:
        services_treeview_columns = ServicesGUI.treeview6101.get_columns()
        treeview_column_titles = []
        for column in services_treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i, services_data in enumerate(services_data_list):
            for j, column_title in enumerate(treeview_column_titles):
                if column_title == services_data[1]:
                   column_width = services_data_column_widths[i]
                   services_treeview_columns[j].set_fixed_width(column_width)                 # Set column width in pixels. Fixed width is unset if value is "-1".

    # Get new/deleted(ended) services for updating treestore/treeview
    service_list_prev_set = set(service_list_prev)
    service_list_set = set(service_list)
    deleted_services = sorted(list(service_list_prev_set - service_list_set))
    new_services = sorted(list(service_list_set - service_list_prev_set))
    existing_services = sorted(list(service_list_set.intersection(service_list_prev)))
    updated_existing_services_index = [[service_list.index(i), service_list_prev.index(i)] for i in existing_services]    # "c = set(a).intersection(b)" is about 19% faster than "c = set(a).intersection(set(b))"
    services_data_rows_row_length = len(services_data_rows[0])

    # Append/Remove/Update services data into treestore
    ServicesGUI.treeview6101.freeze_child_notify()                                            # For lower CPU consumption by preventing treeview updates on content changes/updates.
    global service_search_text, filter_service_type, filter_column
    if len(piter_list) > 0:
        for i, j in updated_existing_services_index:
            if services_data_rows[i] != services_data_rows_prev[j]:
                for k in range(1, services_data_rows_row_length):                             # Start from "1" in order to set first element (treeview row visibility data) as "True" in every loop.
                    if services_data_rows_prev[j][k] != services_data_rows[i][k]:
                        treestore6101.set_value(piter_list[j], k, services_data_rows[i][k])
    if len(deleted_services) > 0:
        for service in reversed(sorted(list(deleted_services))):
            treestore6101.remove(piter_list[service_list_prev.index(service)])
            piter_list.remove(piter_list[service_list_prev.index(service)])
    if len(new_services) > 0:
        for service in new_services:
            # /// Start /// This block of code is used for determining if the newly added service will be shown on the treeview (user search actions and/or search customizations and/or "Show all loaded/non-loaded services" preference affect service visibility).
            if ServicesGUI.radiobutton6102.get_active() == True and service_loaded_not_loaded_list[service_list.index(service)] != True:    # Hide service (set the visibility value as "False") if "Show all loaded/non-loaded services" option is selected on the GUI and service visibility is not "True".
                services_data_rows[service_list.index(service)][0] = False
            if ServicesGUI.radiobutton6103.get_active() == True and service_loaded_not_loaded_list[service_list.index(service)] == True:    # Hide service (set the visibility value as "False") if "Show all loaded/non-loaded services" option is selected on the GUI and service visibility is "True".
                services_data_rows[service_list.index(service)][0] = False
            if ServicesGUI.searchentry6101.get_text() != "":
                service_data_text_in_model = services_data_rows[service_list.index(service)][filter_column]
                service_state_in_model = service_loaded_not_loaded_list[service_list.index(service)]
                if service_search_text not in str(service_data_text_in_model).lower():        # Hide service (set the visibility value as "False") if search text (typed into the search entry) is not in the appropriate column of the service data.
                    services_data_rows[service_list.index(service)][0] = False
                if service_state_in_model not in filter_service_type:                         # Hide service (set the visibility value as "False") if visibility data of the service is not in the filter_service_type (this list is constructed by using user preferred options on the "Service Search Customizations" tab).
                    services_data_rows[service_list.index(service)][0] = False
            # \\\ End \\\ This block of code is used for determining if the newly added service will be shown on the treeview (user search actions and/or search customizations and/or "Show all loaded/non-loaded services" preference affect service visibility).
            piter_list.insert(service_list.index(service), treestore6101.insert(None, service_list.index(service), services_data_rows[service_list.index(service)]))    # "insert" have to be used for appending element into both "piter_list" and "treestore" in order to avoid data index problems which are caused by sorting of ".service" file names (this sorting is performed for getting list differences).
    ServicesGUI.treeview6101.thaw_child_notify()                                              # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    service_list_prev = service_list                                                          # For using values in the next loop
    services_data_rows_prev = services_data_rows
    services_treeview_columns_shown_prev = services_treeview_columns_shown
    services_data_row_sorting_column_prev = services_data_row_sorting_column
    services_data_row_sorting_order_prev = services_data_row_sorting_order
    services_data_column_order_prev = services_data_column_order
    services_data_column_widths_prev = services_data_column_widths

    # Get number of visible services and number of all services and show these information on the GUI label
    loaded_service_count = service_loaded_not_loaded_list.count(True)
    number_of_all_services = len(service_loaded_not_loaded_list)
    ServicesGUI.label6101.set_text(_tr("Total: ") + str(number_of_all_services) + _tr(" services (") + str(loaded_service_count) + _tr(" loaded, ") + str(number_of_all_services-loaded_service_count) + _tr(" non-loaded)"))    # f strings have lower CPU usage than joining method but strings are joinied by by this method because gettext could not be worked with Python f strings.


# ----------------------------------- Services - Treeview Cell Functions (defines functions for treeview cell for setting data precisions and/or data units) -----------------------------------
def cell_data_function_ram(tree_column, cell, tree_model, iter, data):
    cell_data = tree_model.get(iter, data)[0]
    if cell_data == -9999:
        cell.set_property('text', "-")
    if cell_data != -9999:
        cell.set_property('text', f'{services_data_unit_converter_func(cell_data, services_ram_swap_data_unit, services_ram_swap_data_precision)}')


# ----------------------------------- Services Initial Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def services_initial_thread_func():

    GLib.idle_add(services_initial_func)


# ----------------------------------- Services Loop Thread Function (runs the code in the function as threaded in order to avoid blocking/slowing down GUI operations and other operations) -----------------------------------
def services_loop_thread_func():

    GLib.idle_add(services_loop_func)
    if MainGUI.radiobutton6.get_active() is True:                                             # "is/is not" is about 15% faster than "==/!="
        global update_interval
        update_interval = Config.update_interval
        GLib.timeout_add(update_interval * 1000, services_loop_thread_func)


# ----------------------------------- Services Thread Run Function (starts execution of the threads) -----------------------------------
def services_thread_run_func():

#     if "services_data_rows" not in globals():                                               # To be able to run initial thread for only one time
    services_initial_thread = Thread(target=services_initial_thread_func, daemon=True)
    services_initial_thread.start()
    services_initial_thread.join()
#     services_loop_thread = Thread(target=services_loop_thread_func, daemon=True)
#     services_loop_thread.start()
#         services_one_time_thread = Thread(target=services_loop_func, daemon=True)             # Getting and showing service data operations are not repeated (they are performed only one time) because getting service data takes a long time (nearly 1 second on a Core i7-2630QM 4-cored notebook PC). Data could be refreshed by user demand from the GUI.
#         services_one_time_thread.start()


# ----------------------------------- Services - Treeview Filter Show All Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def services_treeview_filter_show_all_func():

    for piter in piter_list:
        treestore6101.set_value(piter, 0, True)


# ----------------------------------- Services - Treeview Filter Show All Enabled (Visible) Services Items Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def services_treeview_filter_services_loaded_only():

    for piter in piter_list:
        if service_loaded_not_loaded_list[piter_list.index(piter)] != True:
            treestore6101.set_value(piter, 0, False)


# ----------------------------------- Services - Treeview Filter Show All Disabled (Hidden) Services Items Function (updates treeview shown rows when relevant button clicked) -----------------------------------
def services_treeview_filter_services_not_loaded_only():

    for piter in piter_list:
        if service_loaded_not_loaded_list[piter_list.index(piter)] == True:
            treestore6101.set_value(piter, 0, False)


# ----------------------------------- Services - Treeview Filter Search Function (updates treeview shown rows when text typed into entry) -----------------------------------
def services_treeview_filter_search_func():

    # Determine filtering column (Service name, load state, active state, etc.) for hiding/showing services by using search text typed into search entry.
    global service_search_text, filter_service_type, filter_column
    services_treeview_columns_shown_sorted = sorted(services_treeview_columns_shown)
    if ServicesMenusGUI.radiobutton6101p2.get_active() == True:
        if 0 in services_treeview_columns_shown:                                              # "0" is treeview column number
            filter_column = 2                                                                 # Append internal column number (2) of "service name" for filtering
    if ServicesMenusGUI.radiobutton6102p2.get_active() == True:
        if 1 in services_treeview_columns_shown:                                              # "1" is treeview column number
            filter_column = 3                                                                 # Append internal column number (3) of "state" for filtering
    if ServicesMenusGUI.radiobutton6103p2.get_active() == True:
        if 2 in services_treeview_columns_shown:                                              # "2" is treeview column number
            filter_column = 4                                                                 # Append internal column number (4) of "main PID" for filtering
    if ServicesMenusGUI.radiobutton6104p2.get_active() == True:
        if 3 in services_treeview_columns_shown:                                              # "3" is treeview column number
            filter_column = 5                                                                 # Append internal column number (5) of "active state" for filtering
    if ServicesMenusGUI.radiobutton6105p2.get_active() == True:
        if 4 in services_treeview_columns_shown:                                              # "4" is treeview column number
            filter_column = 6                                                                 # Append internal column number (6) of "load state" for filtering
    if ServicesMenusGUI.radiobutton6106p2.get_active() == True:
        if 5 in services_treeview_columns_shown:                                              # "5" is treeview column number
            filter_column = 7                                                                 # Append internal column number (7) of "sub-state" for filtering
    if ServicesMenusGUI.radiobutton6107p2.get_active() == True:
        if 7 in services_treeview_columns_shown:                                              # "7" is treeview column number
            filter_column = 9                                                                 # Append internal column number (9) of "description" for filtering
    # Service could be shown/hidden for loaded/not loaded (non-loaded) service unit file state. Preferred visibility data is determined here.
    filter_service_type = []
    if ServicesMenusGUI.checkbutton6102p2.get_active() == True:
        filter_service_type.append(True)
    if ServicesMenusGUI.checkbutton6103p2.get_active() == True:
        filter_service_type.append(False)

    service_search_text = ServicesGUI.searchentry6101.get_text().lower()
    # Set visible/hidden services
    for piter in piter_list:
        treestore6101.set_value(piter, 0, False)
        service_data_text_in_model = treestore6101.get_value(piter, filter_column)
        if service_search_text in str(service_data_text_in_model).lower():
            treestore6101.set_value(piter, 0, True)
            service_load_state_in_model = service_loaded_not_loaded_list[piter_list.index(piter)]
            if service_load_state_in_model not in filter_service_type:
                treestore6101.set_value(piter, 0, False)


# ----------------------------------- Services - Column Title Clicked Function (gets treeview column number (id) and row sorting order by being triggered by Gtk signals) -----------------------------------
def on_column_title_clicked(widget):

    services_data_row_sorting_column_title = widget.get_title()                               # Get column title which will be used for getting column number
    for data in services_data_list:
        if data[1] == services_data_row_sorting_column_title:
            Config.services_data_row_sorting_column = data[0]                                 # Get column number
    Config.services_data_row_sorting_order = int(widget.get_sort_order())                     # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    Config.config_save_func()


# ----------------------------------- Services - Treeview Column Order-Width Row Sorting Function (gets treeview column order/widths and row sorting) -----------------------------------
def services_treeview_column_order_width_row_sorting_func():
    # Columns in the treeview are get one by one and appended into "services_data_column_order". "services_data_column_widths" list elements are modified for widths of every columns in the treeview. Length of these list are always same even if columns are removed, appended and column widths are changed. Only values of the elements (element indexes are always same with "services_data") are changed if column order/widths are changed.
    services_treeview_columns = ServicesGUI.treeview6101.get_columns()
    treeview_column_titles = []
    for column in services_treeview_columns:
        treeview_column_titles.append(column.get_title())
    for i, services_data in enumerate(services_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == services_data[1]:
                Config.services_data_column_order[i] = j
                Config.services_data_column_widths[i] = services_treeview_columns[j].get_width()
                break
    Config.config_save_func()


# ----------------------------------- Services - Define Data Unit Converter Variables Function (contains data unit variables) -----------------------------------
def services_define_data_unit_converter_variables_func():

    global data_unit_list

    # Calculated values are used in order to obtain lower CPU usage, because this dictionary will be used very frequently.

    # Unit Name    Abbreviation    bytes   
    # byte         B               1
    # kilobyte     KB              1024
    # megabyte     MB              1.04858E+06
    # gigabyte     GB              1.07374E+09
    # terabyte     TB              1.09951E+12
    # petabyte     PB              1.12590E+15
    # exabyte      EB              1.15292E+18

    # Unit Name    Abbreviation    bytes    
    # bit          b               8
    # kilobit      Kb              8192
    # megabit      Mb              8,38861E+06
    # gigabit      Gb              8,58993E+09
    # terabit      Tb              8,79609E+12
    # petabit      Pb              9,00720E+15
    # exabit       Eb              9,22337E+18

    data_unit_list = [[0, 0, _tr("Auto-Byte")], [1, 1, "B"], [2, 1024, "KiB"], [3, 1.04858E+06, "MiB"], [4, 1.07374E+09, "GiB"],
                      [5, 1.09961E+12, "TiB"], [6, 1.12590E+15, "PiB"], [7, 1.15292E+18, "EiB"],
                      [8, 0, _tr("Auto-bit")], [9, 8, "b"], [10, 8192, "Kib"], [11, 8.38861E+06, "Mib"], [12, 8.58993E+09, "Gib"],
                      [13, 8.79609E+12, "Tib"], [14, 9.00720E+15, "Pib"], [15, 9.22337E+18, "Eib"]]


# ----------------------------------- Services - Data Unit Converter Function (converts byte and bit data units) -----------------------------------
def services_data_unit_converter_func(data, unit, precision):

    global data_unit_list
    if unit == 0 or unit == 8:
        unit_counter = unit + 1
        while data > 1024:
            unit_counter = unit_counter + 1
            data = data/1024
        unit = data_unit_list[unit_counter][2]
        return f'{data:.{precision}f} {unit}'

    data = data / data_unit_list[unit][1]
    unit = data_unit_list[unit][2]
    return f'{data:.{precision}f} {unit}'

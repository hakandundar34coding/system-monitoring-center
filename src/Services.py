#!/usr/bin/env python3

# ----------------------------------- Services - Import Function -----------------------------------
def services_import_func():

    global Gtk, Gdk, GLib, GObject, subprocess, os

    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('GLib', '2.0')
    gi.require_version('Gdk', '3.0')
    gi.require_version('GObject', '2.0')
    from gi.repository import Gtk, Gdk, GLib, GObject
    import subprocess
    import os


    global Config, Performance
    from Config import Config
    from Performance import Performance

    global _tr
    from locale import gettext as _tr


# ----------------------------------- Services - Services GUI Function -----------------------------------
def services_gui_func():

    # Services tab GUI objects
    global grid6101, treeview6101, searchentry6101, button6101, button6102

    # Services tab GUI objects - get from file
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/ServicesTab.ui")

    # Services tab GUI objects - get
    grid6101 = builder.get_object('grid6101')
    treeview6101 = builder.get_object('treeview6101')
    searchentry6101 = builder.get_object('searchentry6101')
    button6101 = builder.get_object('button6101')
    button6102 = builder.get_object('button6102')

    # Services tab GUI functions - connect
    treeview6101.connect("button-press-event", on_treeview6101_button_press_event)
    treeview6101.connect("button-release-event", on_treeview6101_button_release_event)
    searchentry6101.connect("changed", on_searchentry6101_changed)
    button6101.connect("clicked", on_button6101_clicked)
    button6102.connect("clicked", on_button6102_clicked)

    # Services Tab - Treeview Properties
    treeview6101.set_activate_on_single_click(True)
    treeview6101.set_fixed_height_mode(True)
    treeview6101.set_headers_clickable(True)
    treeview6101.set_show_expanders(False)
    treeview6101.set_enable_search(True)
    treeview6101.set_search_column(2)
    treeview6101.set_tooltip_column(2)

    global initial_already_run
    initial_already_run = 0


# --------------------------------- Called for running code/functions when button is pressed on the treeview ---------------------------------
def on_treeview6101_button_press_event(widget, event):

    # Get right/double clicked row data
    try:                                                                                  # "try-except" is used in order to prevent errors when right clicked on an empty area on the treeview.
        path, _, _, _ = treeview6101.get_path_at_pos(int(event.x), int(event.y))
    except TypeError:
        return
    model = treeview6101.get_model()
    treeiter = model.get_iter(path)

    # Get right/double clicked service name
    if treeiter == None:
        return
    global selected_service_name
    try:
        selected_service_name = service_list[services_data_rows.index(model[treeiter][:])]
    except ValueError:
        return

    # Open right click menu if right clicked on a row
    if event.button == 3:
        from ServicesMenuRightClick import ServicesMenuRightClick
        ServicesMenuRightClick.menu6101m.popup_at_pointer()
        ServicesMenuRightClick.services_set_checkmenuitem_func()

    # Open details window if double clicked on a row
    if event.type == Gdk.EventType._2BUTTON_PRESS:
        from ServicesDetails import ServicesDetails
        ServicesDetails.window6101w.show()


# --------------------------------- Called for running code/functions when button is released on the treeview ---------------------------------
def on_treeview6101_button_release_event(widget, event):

    # Check if left mouse button is used
    if event.button == 1:
        services_treeview_column_order_width_row_sorting_func()


# --------------------------------- Called for searching items when searchentry text is changed ---------------------------------
def on_searchentry6101_changed(widget):

    global filter_column
    service_search_text = searchentry6101.get_text().lower()
    # Set visible/hidden services
    for piter in piter_list:
        treestore6101.set_value(piter, 0, False)
        service_data_text_in_model = treestore6101.get_value(piter, filter_column)
        if service_search_text in str(service_data_text_in_model).lower():
            treestore6101.set_value(piter, 0, True)


# --------------------------------- Called for showing Services tab customization menu when button is clicked ---------------------------------
def on_button6101_clicked(widget):

    from ServicesMenuCustomizations import ServicesMenuCustomizations
    ServicesMenuCustomizations.popover6101p.set_relative_to(button6101)
    ServicesMenuCustomizations.popover6101p.set_position(1)
    ServicesMenuCustomizations.popover6101p.popup()


# --------------------------------- Called for reloading the data on the Services tab if "Refresh" button is clicked ---------------------------------
def on_button6102_clicked(widget):

    services_loop_func()


# ----------------------------------- Services - Initial Function -----------------------------------
def services_initial_func():

    global services_data_list
    services_data_list = [
                         [0, _tr('Name'), 3, 2, 3, [bool, str, str], ['internal_column', 'CellRendererPixbuf', 'CellRendererText'], ['no_cell_attribute', 'icon_name', 'text'], [0, 1, 2], ['no_cell_alignment', 0.0, 0.0], ['no_set_expand', False, False], ['no_cell_function', 'no_cell_function', 'no_cell_function']],
                         [1, _tr('State'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                         [2, _tr('Main PID'), 1, 1, 1, [int], ['CellRendererText'], ['text'], [0], [1.0], [False], ['no_cell_function']],
                         [3, _tr('Active State'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                         [4, _tr('Load State'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                         [5, _tr('Sub-State'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']],
                         [6, _tr('Memory (RSS)'), 1, 1, 1, [GObject.TYPE_INT64], ['CellRendererText'], ['text'], [0], [1.0], [False], [cell_data_function_ram]],
                         [7, _tr('Description'), 1, 1, 1, [str], ['CellRendererText'], ['text'], [0], [0.0], [False], ['no_cell_function']]
                         ]

    # Define data unit conversion function objects in for lower CPU usage.
    global performance_define_data_unit_converter_variables_func, performance_define_data_unit_converter_variables_func, performance_data_unit_converter_func
    performance_define_data_unit_converter_variables_func = Performance.performance_define_data_unit_converter_variables_func
    performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

    # Define data unit conversion variables before they are used.
    performance_define_data_unit_converter_variables_func()

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

    service_state_list = [_tr("Enabled"), _tr("Disabled"), _tr("Masked"), _tr("Unmasked"), _tr("Static"), _tr("Generated"), _tr("Enabled-runtime"), _tr("Indirect"), _tr("Active"), _tr("Inactive"), _tr("Loaded"), _tr("Dead"), _tr("Exited"), _tr("Running")]    # This list is defined in order to make English service state names to be translated into other languages. String names are capitalized here as they are capitalized in the code by using ".capitalize()" in order to use translated strings.
    services_other_text_list = [_tr("Yes"), _tr("No")]                                        # This list is defined in order to make English service information to be translated into other languages.

    global filter_column
    filter_column = services_data_list[0][2] - 1                                              # Search filter is "Service Name". "-1" is used because "processes_data_list" has internal column count and it has to be converted to Python index. For example, if there are 3 internal columns but index is 2 for the last internal column number for the relevant treeview column.

    global initial_already_run
    initial_already_run = 1

    services_loop_func()


# ----------------------------------- Services - Get Services Data Function -----------------------------------
def services_loop_func():

    update_interval = Config.update_interval

    # Get GUI obejcts one time per floop instead of getting them multiple times
    global treeview6101

    # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
    global services_memory_data_precision, services_memory_data_unit
    services_memory_data_precision = Config.services_memory_data_precision
    services_memory_data_unit = Config.services_memory_data_unit

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
    # There is no "/usr/lib/systemd/system/" on some ARM systems (and also on older distributions) and "/lib/systemd/system/" is used in this case. On newer distributions "/usr/lib/systemd/system/" is a symlink to "/lib/systemd/system/".
    # On ARM systems, also "/usr/lib/systemd/system/" folder may be used after installling some applications. In this situation this folder will be a real path.
    service_unit_file_list_usr_lib_systemd = []
    service_unit_file_list_lib_systemd = []
    if os.path.isdir("/usr/lib/systemd/system/") == True:
        service_unit_files_dir = "/usr/lib/systemd/system/"
        service_unit_file_list_usr_lib_systemd = [filename for filename in os.listdir(service_unit_files_dir) if filename.endswith(".service")]    # Get file names which ends withs ".service".
    if os.path.realpath("/lib/systemd/system/") + "/" == "/lib/systemd/system/":
        service_unit_files_dir = "/lib/systemd/system/"
        service_unit_file_list_lib_systemd = [filename for filename in os.listdir(service_unit_files_dir) if filename.endswith(".service")]    # Get file names which ends withs ".service".

    # Merge service file lists from different folders.
    service_unit_file_list = service_unit_file_list_usr_lib_systemd + service_unit_file_list_lib_systemd

    try:
        service_files_from_run_systemd_list = [filename.split("invocation:", 1)[1] for filename in os.listdir("/run/systemd/units/")]    # "/run/systemd/units/" directory contains loaded and non-dead services.
    except FileNotFoundError:
        service_files_from_run_systemd_list = []

    for file in service_unit_file_list[:]:                                                    # "[:]" is used for iterating over copy of the list because elements are removed during iteration. Otherwise incorrect operations (incorrect element removals) are performed on the list.
        if os.path.islink(service_unit_files_dir + file) == True and os.path.realpath(service_unit_files_dir + file) != "/dev/null":    # Some service files are link to other ".service" files in the same directory. These links are removed from the list. Not all link files are removed. Link files with "/dev/null" are kept in the list.
            service_unit_file_list.remove(file)

    # Get all service names (joining service names from "systemctl list-unit-files ..." and "systemctl list-units ..."). Some services are run multiple times. For example there is one instance of "user@.service" from ""systemctl list-unit-files ..." command but there are two loaded services (user@1000.service and user@1001.service) per logged in user. There are several examples for this situation. "user@.service" is removed from list, "user@1000.service" and "user@1001.service" appended into list for getting information for all services correctly.
    for service_unit_file in service_unit_file_list:
        if "@" not in service_unit_file:
            service_list.append(service_unit_file)
            continue
        else:
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
    unit_files_command = ["systemctl", "show", "--property=" + unit_files_command_parameter_list]
    for service in service_list:
        unit_files_command.append(service)

    # Get number of online logical CPU cores (this operation is repeated in every loop because number of online CPU cores may be changed by user.
    try:
        number_of_logical_cores = os.sysconf("SC_NPROCESSORS_ONLN")                           # To be able to get number of online logical CPU cores first try  a faster way: using "SC_NPROCESSORS_ONLN" variable.
    except ValueError:
        with open("/proc/cpuinfo") as reader:                                                 # As a second try, count number of online logical CPU cores by reading from /proc/cpuinfo file.
            proc_cpuinfo_lines = reader.read().split("\n")
        number_of_logical_cores = 0
        for line in proc_cpuinfo_lines:
            if line.startswith("processor"):
                number_of_logical_cores = number_of_logical_cores + 1

    # Get services bu using single process (instead of multiprocessing) if the system has 1 or 2 CPU cores.
    if number_of_logical_cores in [1, 2]:
        # Get service data per service file in one attempt in order to obtain lower CPU usage. Because information from all service files will be get by one commandline operation and will be parsed later.
        try:
            systemctl_show_command_lines = (subprocess.check_output(unit_files_command, shell=False)).decode().strip().split("\n\n")
        # Prevent errors if "systemd" is not used on the system.
        except Exception:
            return
    # Get services bu using multiple processes (multiprocessing) if the system has more than 2 CPU cores.
    if number_of_logical_cores > 2:
        import ServicesGetMultProc
        systemctl_show_command_lines = ServicesGetMultProc.start_processes_func(number_of_logical_cores, unit_files_command)

    # Get services data (specific information by processing the data get previously)
    for i, service in enumerate(service_list):
        systemctl_show_command_lines_split = systemctl_show_command_lines[i]
        # Get service "loaded/not loaded" status. This data will be used for filtering (search, etc.) services.
        service_load_state = "-"                                                              # Initial value of "service_load_state" variable. This value will be used if "service_load_state" could not be detected.
        service_load_state = systemctl_show_command_lines_split.split("LoadState=", 1)[1].split("\n", 1)[0].capitalize()
        if service_load_state == "Loaded":
            service_loaded_not_loaded_list.append(True)
        else:
            service_loaded_not_loaded_list.append(False)
        # Append service icon and service name
        services_data_row = [True, services_image, service]                                   # Service visibility data (on treeview) which is used for showing/hiding service when services in specific type (enabled/disabled) is preferred to be shown or service search feature is used from the GUI.
        # Append service unit file state
        if 1 in services_treeview_columns_shown:
            service_state = _tr(systemctl_show_command_lines_split.split("UnitFileState=", 1)[1].split("\n", 1)[0].capitalize())    # "_tr([value])" is used for using translated string.
            services_data_row.append(service_state)
        # Append service main PID
        if 2 in services_treeview_columns_shown:
            service_main_pid = int(systemctl_show_command_lines_split.split("MainPID=", 1)[1].split("\n", 1)[0].capitalize())
            services_data_row.append(service_main_pid)
        # Append service active state
        if 3 in services_treeview_columns_shown:
            service_active_state = _tr(systemctl_show_command_lines_split.split("ActiveState=", 1)[1].split("\n", 1)[0].capitalize())
            services_data_row.append(service_active_state)
        # Append service load state (it has been get previously)
        if 4 in services_treeview_columns_shown:
            services_data_row.append(_tr(service_load_state))
        # Append service substate
        if 5 in services_treeview_columns_shown:
            service_sub_state = _tr(systemctl_show_command_lines_split.split("SubState=", 1)[1].split("\n", 1)[0].capitalize())
            services_data_row.append(service_sub_state)
        # Append service current memory
        if 6 in services_treeview_columns_shown:
            service_memory_current = systemctl_show_command_lines_split.split("MemoryCurrent=", 1)[1].split("\n", 1)[0].capitalize()
            if service_memory_current.startswith("["):
                service_memory_current = -9999                                                # "-9999" value is used as "service_memory_current" value if memory value is get as "[not set]". Code will recognize this value and show "-" information in this situation. This negative integer value is used instead of string value because this data colmn of the treestore is an integer typed column.
            else:
                service_memory_current = int(service_memory_current)
            services_data_row.append(service_memory_current)
        # Append service description
        if 7 in services_treeview_columns_shown:
            service_description = systemctl_show_command_lines_split.split("Description=", 1)[1].split("\n", 1)[0].capitalize()
            services_data_row.append(service_description)
        # Append all data of the services into a list which will be appended into a treestore for showing the data on a treeview.
        services_data_rows.append(services_data_row)

    # Add/Remove treeview columns appropriate for user preferences
    treeview6101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    if services_treeview_columns_shown != services_treeview_columns_shown_prev:               # Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if column numbers are changed. Because once treestore data types (str, int, etc) are defined, they can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal can not be performed.
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        for column in treeview6101.get_columns():                                             # Remove all columns in the treeview.
            treeview6101.remove_column(column)
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
            services_treeview_column.set_min_width(50)                                        # Set minimum column widths as "50 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            services_treeview_column.connect("clicked", on_column_title_clicked)              # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
            treeview6101.append_column(services_treeview_column)                              # Append column into treeview

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
        treeview6101.set_model(treemodelsort6101)
        service_list_prev = []                                                                # Redefine (clear) "service_list_prev" list. Thus code will recognize this and data will be appended into treestore and piter_list from zero.        global piter_list
        global piter_list
        piter_list = []
    treeview6101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or user has reset column order from customizations.
    if services_treeview_columns_shown_prev != services_treeview_columns_shown or services_data_column_order_prev != services_data_column_order:
        services_treeview_columns = treeview6101.get_columns()                                # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_column_titles = []
        for column in services_treeview_columns:
            treeview_column_titles.append(column.get_title())
        services_data_column_order_scratch = []
        for column_order in services_data_column_order:
            if column_order != -1:
                services_data_column_order_scratch.append(column_order)
        for order in reversed(sorted(services_data_column_order_scratch)):                    # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
            if services_data_column_order.index(order) in services_treeview_columns_shown:
                column_number_to_move = services_data_column_order.index(order)
                column_title_to_move = services_data_list[column_number_to_move][1]
                column_to_move = services_treeview_columns[treeview_column_titles.index(column_title_to_move)]
                treeview6101.move_column_after(column_to_move, None)                          # Column is moved at the beginning of the treeview if "None" is used.

    # Sort service rows if user has changed row sorting column and sorting order (ascending/descending) by clicking on any column title button on the GUI.
    if services_treeview_columns_shown_prev != services_treeview_columns_shown or services_data_row_sorting_column_prev != services_data_row_sorting_column or services_data_row_sorting_order != services_data_row_sorting_order_prev:    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid reordering/sorting in every loop.
        services_treeview_columns = treeview6101.get_columns()                                # Get shown columns on the treeview in order to use this data for reordering the columns.
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
        services_treeview_columns = treeview6101.get_columns()
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
    treeview6101.freeze_child_notify()                                                        # For lower CPU consumption by preventing treeview updates on content changes/updates.
    global service_search_text, filter_column
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
        on_searchentry6101_changed(searchentry6101)                                           # Update search results.
    if len(new_services) > 0:
        for service in new_services:
            piter_list.insert(service_list.index(service), treestore6101.insert(None, service_list.index(service), services_data_rows[service_list.index(service)]))    # "insert" have to be used for appending element into both "piter_list" and "treestore" in order to avoid data index problems which are caused by sorting of ".service" file names (this sorting is performed for getting list differences).
        on_searchentry6101_changed(searchentry6101)                                           # Update search results.
    treeview6101.thaw_child_notify()                                                          # Have to be used after "freeze_child_notify()" if it is used. It lets treeview to update when its content changes.

    service_list_prev = service_list                                                          # For using values in the next loop
    services_data_rows_prev = services_data_rows
    services_treeview_columns_shown_prev = services_treeview_columns_shown
    services_data_row_sorting_column_prev = services_data_row_sorting_column
    services_data_row_sorting_order_prev = services_data_row_sorting_order
    services_data_column_order_prev = services_data_column_order
    services_data_column_widths_prev = services_data_column_widths

    # Show number of services on the searchentry as placeholder text
    searchentry6101.set_placeholder_text(_tr("Search...") + "                    " + "(" + _tr("Services") + ": " + str(len(service_loaded_not_loaded_list)) + ")")


# ----------------------------------- Services - Treeview Cell Functions -----------------------------------
def cell_data_function_ram(tree_column, cell, tree_model, iter, data):
    cell_data = tree_model.get(iter, data)[0]
    if cell_data == -9999:
        cell.set_property('text', "-")
    if cell_data != -9999:
        cell.set_property('text', f'{performance_data_unit_converter_func("data", "none", cell_data, services_memory_data_unit, services_memory_data_precision)}')


# ----------------------------------- Services - Column Title Clicked Function -----------------------------------
def on_column_title_clicked(widget):

    services_data_row_sorting_column_title = widget.get_title()                               # Get column title which will be used for getting column number
    for data in services_data_list:
        if data[1] == services_data_row_sorting_column_title:
            Config.services_data_row_sorting_column = data[0]                                 # Get column number
    Config.services_data_row_sorting_order = int(widget.get_sort_order())                     # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    Config.config_save_func()


# ----------------------------------- Services - Treeview Column Order-Width Row Sorting Function -----------------------------------
def services_treeview_column_order_width_row_sorting_func():

    services_treeview_columns = treeview6101.get_columns()
    treeview_column_titles = []
    for column in services_treeview_columns:
        treeview_column_titles.append(column.get_title())

    services_data_column_order = [-1] * len(services_data_list)
    services_data_column_widths = [-1] * len(services_data_list)

    services_treeview_columns_last_index = len(services_treeview_columns)-1

    for i, services_data in enumerate(services_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == services_data[1]:
                column_index = treeview_column_titles.index(services_data[1])
                services_data_column_order[i] = column_index
                if j != services_treeview_columns_last_index:
                    services_data_column_widths[i] = services_treeview_columns[column_index].get_width()

    Config.services_data_column_order = list(services_data_column_order)
    Config.services_data_column_widths = list(services_data_column_widths)
    Config.config_save_func()


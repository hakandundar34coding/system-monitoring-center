import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('Gio', '2.0')
gi.require_version('GObject', '2.0')
from gi.repository import Gtk, Gdk, GLib, Gio, GObject

import os
import subprocess

from locale import gettext as _tr

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon


class Services:

    def __init__(self):

        self.tab_gui()

        self.initial_already_run = 0


    def tab_gui(self):
        """
        Generate tab GUI.
        """

        self.tab_grid = Common.tab_grid()

        self.tab_title_grid()

        self.tab_info_grid()

        # Label (Note: This tab is not reloaded automatically. Manually reload for changes.)
        label = Common.static_information_label_no_ellipsize(_tr("Note: This tab is not reloaded automatically. Manually reload for changes."))
        self.tab_grid.attach(label, 0, 2, 1, 1)

        self.gui_signals()

        self.right_click_menu()


    def tab_title_grid(self):
        """
        Generate tab name label, refresh button, searchentry.
        """

        # Grid (tab title)
        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        self.tab_grid.attach(grid, 0, 0, 1, 1)

        # Label (Services)
        label = Common.tab_title_label(_tr("Services"))
        grid.attach(label, 0, 0, 1, 1)

        # SearchEntry
        self.searchentry = Common.searchentry(self.on_searchentry_changed)
        grid.attach(self.searchentry, 1, 0, 1, 1)

        # Button (refresh tab)
        self.refresh_button = Common.refresh_button(self.on_refresh_button_clicked)
        grid.attach(self.refresh_button, 2, 0, 1, 1)


    def tab_info_grid(self):
        """
        Generate information GUI objects.
        """

        # ScrolledWindow
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.tab_grid.attach(scrolledwindow, 0, 1, 1, 1)

        # TreeView
        self.treeview = Gtk.TreeView()
        self.treeview.set_activate_on_single_click(True)
        self.treeview.set_show_expanders(False)
        self.treeview.set_fixed_height_mode(True)
        self.treeview.set_headers_clickable(True)
        self.treeview.set_enable_search(True)
        self.treeview.set_search_column(2)
        self.treeview.set_tooltip_column(2)
        scrolledwindow.set_child(self.treeview)


    def gui_signals(self):
        """
        Connect GUI signals.
        """

        # Treeview signals
        self.treeview.connect("columns-changed", Common.on_columns_changed)

        # Treeview mouse events.
        treeview_mouse_event = Gtk.GestureClick()
        treeview_mouse_event.connect("pressed", self.on_treeview_pressed)
        treeview_mouse_event.connect("released", self.on_treeview_released)
        self.treeview.add_controller(treeview_mouse_event)

        treeview_mouse_event_right_click = Gtk.GestureClick()
        treeview_mouse_event_right_click.set_button(3)
        treeview_mouse_event_right_click.connect("pressed", self.on_treeview_pressed)
        self.treeview.add_controller(treeview_mouse_event_right_click)

        # SeachEntry focus action and accelerator
        Common.searchentry_focus_action_and_accelerator(MainWindow)

        # Right click menu actions
        # "Start" action
        action = Gio.SimpleAction.new("services_start_service", None)
        action.connect("activate", self.on_service_manage_items_activate)
        MainWindow.main_window.add_action(action)
        # "Stop" action
        action = Gio.SimpleAction.new("services_stop_service", None)
        action.connect("activate", self.on_service_manage_items_activate)
        MainWindow.main_window.add_action(action)
        # "Restart" action
        action = Gio.SimpleAction.new("services_restart_service", None)
        action.connect("activate", self.on_service_manage_items_activate)
        MainWindow.main_window.add_action(action)
        # "Reload" action
        action = Gio.SimpleAction.new("services_reload_service", None)
        action.connect("activate", self.on_service_manage_items_activate)
        MainWindow.main_window.add_action(action)
        # "Enable" action
        action = Gio.SimpleAction.new("services_enable_service", None)
        action.connect("activate", self.on_service_manage_items_activate)
        MainWindow.main_window.add_action(action)
        # "Disable" action
        action = Gio.SimpleAction.new("services_disable_service", None)
        action.connect("activate", self.on_service_manage_items_activate)
        MainWindow.main_window.add_action(action)
        # "Mask" action
        self.mask_service_action = Gio.SimpleAction.new_stateful("services_mask_service", None, GLib.Variant("b", False))
        self.mask_service_action.connect("activate", self.on_service_manage_items_activate)
        MainWindow.main_window.add_action(self.mask_service_action)
        # "Details" action
        action = Gio.SimpleAction.new("services_details", None)
        action.connect("activate", self.on_service_details_item_activate)
        MainWindow.main_window.add_action(action)


    def right_click_menu(self):
        """
        Generate right click menu GUI.
        """

        # Menu models
        service_manage_menu_section = Gio.Menu.new()
        service_manage_menu_section.append(_tr("Start"), "win.services_start_service")
        service_manage_menu_section.append(_tr("Stop"), "win.services_stop_service")
        service_manage_menu_section.append(_tr("Restart"), "win.services_restart_service")
        service_manage_menu_section.append(_tr("Reload"), "win.services_reload_service")
        service_manage_menu_section.append(_tr("Enable"), "win.services_enable_service")
        service_manage_menu_section.append(_tr("Disable"), "win.services_disable_service")

        mask_service_menu_item = Gio.MenuItem()
        mask_service_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_LABEL, GLib.Variant("s", _tr("Mask")))
        mask_service_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_ACTION, GLib.Variant("s", "win.services_mask_service"))
        #mask_service_menu_item.set_attribute_value(Gio.MENU_ATTRIBUTE_TARGET, GLib.Variant("b", False))
        service_manage_menu_section.append_item(mask_service_menu_item)
        service_manage_menu_section_item = Gio.MenuItem.new()
        service_manage_menu_section_item.set_section(service_manage_menu_section)

        details_menu_section = Gio.Menu.new()
        details_menu_section.append(_tr("Details"), "win.services_details")
        details_menu_section_item = Gio.MenuItem.new()
        details_menu_section_item.set_section(details_menu_section)

        right_click_menu_model = Gio.Menu.new()
        right_click_menu_model.append_item(service_manage_menu_section_item)
        right_click_menu_model.append_item(details_menu_section_item)

        # Popover menu
        self.right_click_menu_po = Gtk.PopoverMenu()
        self.right_click_menu_po.set_menu_model(right_click_menu_model)
        #self.right_click_menu_po.set_parent(self.treeview)
        self.right_click_menu_po.set_parent(MainWindow.main_window)
        self.right_click_menu_po.set_position(Gtk.PositionType.BOTTOM)
        self.right_click_menu_po.set_has_arrow(False)


    def set_mask_menu_option(self):
        """
        Set "Mask" option on the right click menu.
        """

        # Get selected service name
        service_name = self.selected_service_name

        # Get service "masked/unmasked" state
        command_list = ["systemctl", "show", service_name, "--property=UnitFileState"]
        if Libsysmon.get_environment_type() == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        self.service_mask_status = (subprocess.check_output(command_list, shell=False)).decode().strip().split("=")[1]

        # Set menu option
        if self.service_mask_status == "masked":
            self.mask_service_action.set_state(GLib.Variant("b", True))
        else:
            self.mask_service_action.set_state(GLib.Variant("b", False))


    def on_service_manage_items_activate(self, action, parameter):
        """
        Start, stop, restart, enable, disable, mask (hide), unmask services.
        """

        # Get right clicked service name.
        service_name = self.selected_service_name

        environment_type = Libsysmon.get_environment_type()

        # "Start" service
        if action.get_name() == "services_start_service":
            command_list = ["systemctl", "start", service_name]
            if environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list

        # "Stop" service
        if action.get_name() == "services_stop_service":
            command_list = ["systemctl", "stop", service_name]
            if environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list

        # "Restart" service
        if action.get_name() == "services_restart_service":
            command_list = ["systemctl", "restart", service_name]
            if environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list

        # "Reload" service
        if action.get_name() == "services_reload_service":
            command_list = ["systemctl", "reload", service_name]
            if environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list

        # "Enable" service
        if action.get_name() == "services_enable_service":
            command_list = ["systemctl", "enable", service_name]
            if environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list

        # "Disable" service
        if action.get_name() == "services_disable_service":
            command_list = ["systemctl", "disable", service_name]
            if environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list

        # "Mask/Unmask" service 
        if action.get_name() == "services_mask_service":
            if self.service_mask_status == "masked":
                command_list = ["systemctl", "unmask", service_name]
            else:
                command_list = ["systemctl", "mask", service_name]
            if environment_type == "flatpak":
                command_list = ["flatpak-spawn", "--host"] + command_list

        # Manage the right clicked service and show an information dialog if there is output messages (warnings/errors).
        try:
            systemctl_run = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE))
            #systemctl_output = systemctl_run.stdout.decode().strip()
            systemctl_error = systemctl_run.stderr.decode().strip()
        except Exception:
            return

        message_text = _tr("Information")
        secondary_text = systemctl_error
        if secondary_text != "":
            self.messagedialog_gui(message_text, secondary_text)


    def messagedialog_gui(self, message_text, secondary_text):
        """
        Generate messagedialog GUI and show it.
        """

        messagedialog = Gtk.MessageDialog(transient_for=MainWindow.main_window,
                                               modal=True,
                                               title="",
                                               message_type=Gtk.MessageType.INFO,
                                               buttons=Gtk.ButtonsType.CLOSE,
                                               text=message_text,
                                               secondary_text=secondary_text
                                               )

        messagedialog.connect("response", self.on_messagedialog_response)
        messagedialog.present()


    def on_messagedialog_response(self, widget, response):
        """
        Hide the dialog if "OK" button is clicked.
        """

        if response == Gtk.ResponseType.OK:
            pass

        messagedialog = widget
        messagedialog.set_visible(False)


    def on_service_details_item_activate(self, action, parameter):
        """
        Show process details window.
        """

        from .ServicesDetails import ServicesDetails
        ServicesDetails.service_details_window.present()


    def on_searchentry_changed(self, widget):
        """
        Called by searchentry when text is changed.
        """

        service_search_text = self.searchentry.get_text().lower()
        # Set visible/hidden services
        for piter in self.piter_list:
            self.treestore.set_value(piter, 0, False)
            service_data_text_in_model = self.treestore.get_value(piter, self.filter_column)
            if service_search_text in str(service_data_text_in_model).lower():
                self.treestore.set_value(piter, 0, True)


    def on_treeview_pressed(self, event, count, x, y):
        """
        Mouse single right click and double left click events (button press).
        Right click menu is opened when right clicked. Details window is shown when double clicked.
        """

        # Convert coordinates for getting path.
        x_bin, y_bin = self.treeview.convert_widget_to_bin_window_coords(x,y)

        # Get right/double clicked row data
        try:
            path, _, _, _ = self.treeview.get_path_at_pos(int(x_bin), int(y_bin))
        # Prevent errors when right clicked on an empty area on the treeview.
        except TypeError:
            return
        model = self.treeview.get_model()
        treeiter = model.get_iter(path)

        # Get right/double clicked service name
        if treeiter == None:
            return
        try:
            self.selected_service_name = self.service_list[self.tab_data_rows.index(model[treeiter][:])]
        except ValueError:
            return

        # Show right click menu if right clicked on a row
        if int(event.get_button()) == 3:
            rectangle = Gdk.Rectangle()
            rectangle.x = int(x)
            rectangle.y = int(y)
            rectangle.width = 1
            rectangle.height = 1
            # Convert teeview coordinates to window coordinates. Because popovermenu is set for window instead of treeview.
            treeview_x_coord, treeview_y_coord = self.treeview.translate_coordinates(MainWindow.main_window,0,0)
            rectangle.x = rectangle.x + treeview_x_coord
            rectangle.y = rectangle.y + treeview_y_coord

            # New coordinates have to be set for popovermenu on every popup.
            self.right_click_menu_po.set_pointing_to(rectangle)
            self.right_click_menu_po.popup()
            self.set_mask_menu_option()

        # Show details window if double clicked on a row
        if int(event.get_button()) == 1 and int(count) == 2:
            from .ServicesDetails import ServicesDetails
            ServicesDetails.service_details_window.present()


    def on_treeview_released(self, event, count, x, y):
        """
        Mouse single left click event (button release).
        Update teeview column/row width/sorting/order.
        """

        # Check if left mouse button is used
        if int(event.get_button()) == 1:
            pass


    def on_refresh_button_clicked(self, widget):
        """
        Refresh data on the tab.
        """

        self.services_loop_already_run = 0

        self.services_loop_func()


    def services_initial_func(self):
        """
        Initial code which which is not wanted to be run in every loop.
        """

        self.row_data_list = [
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
        global performance_data_unit_converter_func
        performance_data_unit_converter_func = Performance.performance_data_unit_converter_func

        self.tab_data_rows_prev = []
        self.service_list_prev = []
        self.piter_list = []
        self.treeview_columns_shown_prev = []
        self.data_row_sorting_column_prev = ""
        self.data_row_sorting_order_prev = ""
        self.data_column_order_prev = []
        self.data_column_widths_prev = []

        service_state_translation_list = [_tr("Enabled"), _tr("Disabled"), _tr("Masked"), _tr("Unmasked"), _tr("Static"), _tr("Generated"), _tr("Enabled-runtime"), _tr("Indirect"), _tr("Active"), _tr("Inactive"), _tr("Loaded"), _tr("Dead"), _tr("Exited"), _tr("Running")]
        services_other_text_translation_list = [_tr("Yes"), _tr("No")]

        self.filter_column = self.row_data_list[0][2] - 1

        self.initial_already_run = 1


    def services_loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        # Switch to System tab and prevent errors if systemd is not used on the system.
        if Config.init_system != "systemd":
            MainWindow.performance_tb.set_active(True)
            return

        # Prevent running rest of the code if Services tab is opened again.
        # Because running this function requires more than a few seconds on some systems.
        try:
            if self.services_loop_already_run == 1:
                return
        except AttributeError:
            pass
        self.services_loop_already_run = 1

        # Get GUI obejcts one time per floop instead of getting them multiple times
        global services_treeview

        # Get configrations one time per floop instead of getting them multiple times in every loop which causes high CPU usage.
        global services_memory_data_precision, services_memory_data_unit
        services_memory_data_precision = Config.services_memory_data_precision
        services_memory_data_unit = Config.services_memory_data_unit

        # Define global variables and get treeview columns, sort column/order, column widths, etc.
        self.treeview_columns_shown = Config.services_treeview_columns_shown
        self.data_row_sorting_column = Config.services_data_row_sorting_column
        self.data_row_sorting_order = Config.services_data_row_sorting_order
        self.data_column_order = Config.services_data_column_order
        self.data_column_widths = Config.services_data_column_widths
        # For obtaining lower CPU usage
        treeview_columns_shown = self.treeview_columns_shown
        treeview_columns_shown = set(treeview_columns_shown)

        # Service files (Unit files) are in the "/etc/systemd/system/" and "/usr/lib/systemd/system/autovt@.service" directories. But the first directory contains links to the service files in the second directory. Thus, service files get from the second directory.
        # There is no "/usr/lib/systemd/system/" on some ARM systems (and also on older distributions) and "/lib/systemd/system/" is used in this case. On newer distributions "/usr/lib/systemd/system/" is a symlink to "/lib/systemd/system/".
        # On ARM systems, also "/usr/lib/systemd/system/" folder may be used after installling some applications. In this situation this folder will be a real path.
        environment_type = Libsysmon.get_environment_type()
        service_unit_file_list_usr_lib_systemd = []
        service_unit_file_list_lib_systemd = []
        if environment_type == "flatpak":
            if os.path.isdir("/var/run/host/usr/lib/systemd/system/") == True:
                service_unit_files_dir = "/var/run/host/usr/lib/systemd/system/"
                service_unit_file_list_usr_lib_systemd = [filename for filename in os.listdir(service_unit_files_dir) if filename.endswith(".service")]
            # There is no access to "/run" folder of the host OS in Flatpak environment.
            if (subprocess.check_output(["flatpak-spawn", "--host", "realpath", "/lib/systemd/system/"], shell=False)).decode().strip() + "/" == "/lib/systemd/system/":
                service_unit_files_dir = "/lib/systemd/system/"
                service_unit_file_list_lib_systemd_scratch = (subprocess.check_output(["flatpak-spawn", "--host", "ls", service_unit_files_dir], shell=False)).decode().strip().split()
                service_unit_file_list_lib_systemd = []
                for file in service_unit_file_list_lib_systemd_scratch:
                    if file.endswith(".service") == True:
                        service_unit_file_list_lib_systemd.append(file)
        else:
            if os.path.isdir("/usr/lib/systemd/system/") == True:
                service_unit_files_dir = "/usr/lib/systemd/system/"
                service_unit_file_list_usr_lib_systemd = [filename for filename in os.listdir(service_unit_files_dir) if filename.endswith(".service")]
            if os.path.realpath("/lib/systemd/system/") + "/" == "/lib/systemd/system/":
                service_unit_files_dir = "/lib/systemd/system/"
                service_unit_file_list_lib_systemd = [filename for filename in os.listdir(service_unit_files_dir) if filename.endswith(".service")]

        # Merge service file lists from different folders.
        service_unit_file_list = service_unit_file_list_usr_lib_systemd + service_unit_file_list_lib_systemd

        try:
            if environment_type == "flatpak":
                # There is no access to "/run" folder of the host OS in Flatpak environment.
                service_files_from_run_systemd_list = (subprocess.check_output(["flatpak-spawn", "--host", "ls", "/run/systemd/units/"], shell=False)).decode().strip().split()
            else:
                service_files_from_run_systemd_list = [filename.split("invocation:", 1)[-1] for filename in os.listdir("/run/systemd/units/")]    # "/run/systemd/units/" directory contains loaded and non-dead services.
        except FileNotFoundError:
            service_files_from_run_systemd_list = []

        if environment_type == "flatpak":
            service_unit_files_dir_scratch = service_unit_files_dir.split("/var/run/host")[-1]
            service_unit_file_real_path_list = (subprocess.check_output(["flatpak-spawn", "--host", "ls", "-l", service_unit_files_dir_scratch], shell=False)).decode().strip().split("\n")
            for service_file in service_unit_file_real_path_list:
                if " -> " in service_file and "/dev/null" not in service_file:
                    file = service_file.split(" -> ")[0].split()[-1].strip()
                    if file in service_unit_file_list:
                        service_unit_file_list.remove(file)
        else:
            for file in service_unit_file_list[:]:                                                # "[:]" is used for iterating over copy of the list because elements are removed during iteration. Otherwise incorrect operations (incorrect element removals) are performed on the list.
                if os.path.islink(service_unit_files_dir + file) == True and os.path.realpath(service_unit_files_dir + file) != "/dev/null":    # Some service files are link to other ".service" files in the same directory. These links are removed from the list. Not all link files are removed. Link files with "/dev/null" are kept in the list.
                    service_unit_file_list.remove(file)

        # Get all service names (joining service names from "systemctl list-unit-files ..." and "systemctl list-units ..."). Some services are run multiple times. For example there is one instance of "user@.service" from ""systemctl list-unit-files ..." command but there are two loaded services (user@1000.service and user@1001.service) per logged in user. There are several examples for this situation. "user@.service" is removed from list, "user@1000.service" and "user@1001.service" appended into list for getting information for all services correctly.
        service_list = []
        for service_unit_file in service_unit_file_list:
            if "@" not in service_unit_file:
                service_list.append(service_unit_file)
                continue
            else:
                service_unit_file_split = service_unit_file.split("@")[0]
                for service_loaded in service_files_from_run_systemd_list:
                    if "@" in service_loaded:
                        service_loaded = service_loaded.split("invocation:")[-1]
                        if service_unit_file_split == service_loaded.split("@")[0]:
                            service_list.append(service_loaded)
                            continue
        service_list = sorted(service_list)

        # Generate "unit_files_command_parameter_list". This list will be used for constructing commandline for getting service data per service file.
        unit_files_command_parameter_list = ["LoadState"]                                         # This information is always get for filtering service, etc. Also it prevents errors if every columns other than service name are preferred not to be shown. It gives errors if no property is specified with "systemctl show [service_name] --property=" command.
        if 1 in treeview_columns_shown:
            unit_files_command_parameter_list.append("UnitFileState")
        if 2 in treeview_columns_shown:
            unit_files_command_parameter_list.append("MainPID")
        if 3 in treeview_columns_shown:
            unit_files_command_parameter_list.append("ActiveState")
        if 5 in treeview_columns_shown:
            unit_files_command_parameter_list.append("SubState")
        if 6 in treeview_columns_shown:
            unit_files_command_parameter_list.append("MemoryCurrent")
        if 7 in treeview_columns_shown:
            unit_files_command_parameter_list.append("Description")
        unit_files_command_parameter_list = ",".join(unit_files_command_parameter_list)           # Join strings with "," between them.
        # Construct command for getting service information for all services
        if environment_type == "flatpak":
            unit_files_command = ["flatpak-spawn", "--host", "systemctl", "show", "--property=" + unit_files_command_parameter_list]
        else:
            unit_files_command = ["systemctl", "show", "--property=" + unit_files_command_parameter_list]
        for service in service_list:
            unit_files_command.append(service)

        # Get number of online logical CPU cores (this operation is repeated in every loop because number of online CPU cores may be changed by user and this may cause wrong calculation of CPU usage percent data of the processes even if this is a very rare situation.)
        number_of_logical_cores = Libsysmon.get_number_of_logical_cores()

        # Get services bu using single process (instead of multiprocessing) if the system has 1 or 2 CPU cores.
        if number_of_logical_cores < 3:
            # Get service data per service file in one attempt in order to obtain lower CPU usage. Because information from all service files will be get by one commandline operation and will be parsed later.
            try:
                systemctl_show_command_lines = (subprocess.check_output(unit_files_command, shell=False)).decode().strip().split("\n\n")
            # Prevent errors if "systemd" is not used on the system.
            except Exception:
                return
        # Get services bu using multiple processes (multiprocessing) if the system has more than 2 CPU cores.
        else:
            from . import ServicesGetMultProc
            systemctl_show_command_lines = ServicesGetMultProc.start_processes_func(number_of_logical_cores, unit_files_command)

        # Get services data (specific information by processing the data get previously)
        tab_data_rows = []
        for i, service in enumerate(service_list):
            systemctl_show_command_lines_split = systemctl_show_command_lines[i]
            # Get service "loaded/not loaded" status. This data will be used for filtering (search, etc.) services.
            service_load_state = "-"                                                              # Initial value of "service_load_state" variable. This value will be used if "service_load_state" could not be detected.
            service_load_state = systemctl_show_command_lines_split.split("LoadState=", 1)[1].split("\n", 1)[0].capitalize()
            # Append service image and service name
            tab_data_row = [True, "system-monitoring-center-services-symbolic", service]
            # Append service unit file state
            if 1 in treeview_columns_shown:
                service_state = _tr(systemctl_show_command_lines_split.split("UnitFileState=", 1)[1].split("\n", 1)[0].capitalize())    # "_tr([value])" is used for using translated string.
                tab_data_row.append(service_state)
            # Append service main PID
            if 2 in treeview_columns_shown:
                service_main_pid = int(systemctl_show_command_lines_split.split("MainPID=", 1)[1].split("\n", 1)[0].capitalize())
                tab_data_row.append(service_main_pid)
            # Append service active state
            if 3 in treeview_columns_shown:
                service_active_state = _tr(systemctl_show_command_lines_split.split("ActiveState=", 1)[1].split("\n", 1)[0].capitalize())
                tab_data_row.append(service_active_state)
            # Append service load state (it has been get previously)
            if 4 in treeview_columns_shown:
                tab_data_row.append(_tr(service_load_state))
            # Append service substate
            if 5 in treeview_columns_shown:
                service_sub_state = _tr(systemctl_show_command_lines_split.split("SubState=", 1)[1].split("\n", 1)[0].capitalize())
                tab_data_row.append(service_sub_state)
            # Append service current memory
            if 6 in treeview_columns_shown:
                service_memory_current = systemctl_show_command_lines_split.split("MemoryCurrent=", 1)[1].split("\n", 1)[0].capitalize()
                if service_memory_current.startswith("["):
                    service_memory_current = -9999                                                # "-9999" value is used as "service_memory_current" value if memory value is get as "[not set]". Code will recognize this value and show "-" information in this situation. This negative integer value is used instead of string value because this data colmn of the treestore is an integer typed column.
                else:
                    service_memory_current = int(service_memory_current)
                tab_data_row.append(service_memory_current)
            # Append service description
            if 7 in treeview_columns_shown:
                service_description = systemctl_show_command_lines_split.split("Description=", 1)[1].split("\n", 1)[0].capitalize()
                tab_data_row.append(service_description)
            # Append all data of the services into a list which will be appended into a treestore for showing the data on a treeview.
            tab_data_rows.append(tab_data_row)

        self.tab_data_rows = tab_data_rows
        self.service_list = service_list

        # Convert set to list (it was set before getting process information)
        treeview_columns_shown = sorted(list(treeview_columns_shown))

        reset_row_unique_data_list_prev = Common.treeview_add_remove_columns()
        if reset_row_unique_data_list_prev == "yes":
            self.service_list_prev = []
        Common.treeview_reorder_columns_sort_rows_set_column_widths()

        rows_data_dict = {}

        # Prevent errors if no rows are found.
        if len(tab_data_rows[0]) == 0:
            return

        deleted_rows, new_rows, updated_existing_row_index = Common.get_new_deleted_updated_rows(service_list, self.service_list_prev)
        Common.update_treestore_rows(rows_data_dict, deleted_rows, new_rows, updated_existing_row_index, service_list, self.service_list_prev, 0)
        Common.searchentry_update_placeholder_text()

        self.service_list_prev = service_list
        self.tab_data_rows_prev = tab_data_rows
        self.treeview_columns_shown_prev = treeview_columns_shown
        self.data_row_sorting_column_prev = self.data_row_sorting_column
        self.data_row_sorting_order_prev = self.data_row_sorting_order
        self.data_column_order_prev = self.data_column_order
        self.data_column_widths_prev = self.data_column_widths


# ----------------------------------- Services - Treeview Cell Functions -----------------------------------
def cell_data_function_ram(tree_column, cell, tree_model, iter, data):
    cell_data = tree_model.get(iter, data)[0]
    if cell_data == -9999:
        cell.set_property('text', "-")
    if cell_data != -9999:
        cell.set_property('text', f'{performance_data_unit_converter_func("data", "none", cell_data, services_memory_data_unit, services_memory_data_precision)}')


Services = Services()


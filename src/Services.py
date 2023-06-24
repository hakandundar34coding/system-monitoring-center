import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('Gio', '2.0')
gi.require_version('GObject', '2.0')
from gi.repository import Gtk, Gdk, GLib, Gio, GObject

import os
import subprocess

from .Config import Config
from .Performance import Performance
from .MainWindow import MainWindow
from . import Common
from . import Libsysmon

_tr = Config._tr


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
        self.treeview.connect("columns-changed", Common.on_columns_changed, self)

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

        self.service_mask_status = Libsysmon.get_service_mask_state(service_name)

        # Set menu option
        if self.service_mask_status == "masked":
            self.mask_service_action.set_state(GLib.Variant("b", True))
        else:
            self.mask_service_action.set_state(GLib.Variant("b", False))


    def on_service_manage_items_activate(self, action, parameter):
        """
        Start, stop, restart, enable, disable, mask (hide), unmask services.
        """

        # Get right clicked service name
        service_name = self.selected_service_name

        if action.get_name() == "services_start_service":
            action_name = "start"
        elif action.get_name() == "services_stop_service":
            action_name = "stop"
        elif action.get_name() == "services_restart_service":
            action_name = "restart"
        elif action.get_name() == "services_reload_service":
            action_name = "reload"
        elif action.get_name() == "services_enable_service":
            action_name = "enable"
        elif action.get_name() == "services_disable_service":
            action_name = "disable"
        elif action.get_name() == "services_mask_service":
            if self.service_mask_status != "masked":
                action_name = "mask"
            elif self.service_mask_status == "masked":
                action_name = "unmask"

        systemctl_error = Libsysmon.manage_service(service_name, action_name)

        # Show information dialog if there are errors in the command output.
        if systemctl_error != "-":
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

        self.loop_func()


    def initial_func(self):
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


    def loop_func(self):
        """
        Get and show information on the GUI on every loop.
        """

        if self.initial_already_run == 0:
            self.initial_func()

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

        rows_data_dict = Libsysmon.get_services_information()
        self.rows_data_dict_prev = dict(rows_data_dict)
        service_list = rows_data_dict["service_list"]

        # Get and append process data
        tab_data_rows = []
        for service_name in service_list:
            row_data_dict = rows_data_dict[service_name]
            tab_data_row = [True, "system-monitoring-center-services-symbolic", service_name]
            if 1 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["unit_file_state"])
            if 2 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["main_pid"])
            if 3 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["active_state"])
            if 4 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["load_state"])
            if 5 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["sub_state"])
            if 6 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["memory_current"])
            if 7 in treeview_columns_shown:
                tab_data_row.append(row_data_dict["description"])

            # Append process data into a list
            tab_data_rows.append(tab_data_row)

        self.tab_data_rows = tab_data_rows
        self.service_list = service_list

        # Convert set to list (it was set before getting process information)
        treeview_columns_shown = sorted(list(treeview_columns_shown))

        reset_row_unique_data_list_prev = Common.treeview_add_remove_columns(self)
        if reset_row_unique_data_list_prev == "yes":
            self.service_list_prev = []
        Common.treeview_reorder_columns_sort_rows_set_column_widths(self)

        rows_data_dict = {}

        # Prevent errors if no rows are found.
        if len(tab_data_rows[0]) == 0:
            return

        deleted_rows, new_rows, updated_existing_row_index = Common.get_new_deleted_updated_rows(service_list, self.service_list_prev)
        Common.update_treestore_rows(self, rows_data_dict, deleted_rows, new_rows, updated_existing_row_index, service_list, self.service_list_prev, 0)
        Common.searchentry_update_placeholder_text(self)

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
    if cell_data == -1:
        cell.set_property('text', "-")
    if cell_data != -1:
        cell.set_property('text', f'{performance_data_unit_converter_func("data", "none", cell_data, services_memory_data_unit, services_memory_data_precision)}')


Services = Services()


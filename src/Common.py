import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Gio', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, Gio, GObject, Pango

import os
import subprocess
import time
import sys

from locale import gettext as _tr

from .Config import Config
from .Performance import Performance


# Define constants
# For many systems CPU ticks 100 times in a second. Wall clock time could be get if CPU times are multiplied with this value or vice versa.
number_of_clock_ticks = os.sysconf("SC_CLK_TCK")
# This value is used for converting memory page values into byte values.
# This value depends on architecture (also sometimes depends on machine model). Default value is 4096 Bytes (4 KiB) for most processors.
memory_page_size = os.sysconf("SC_PAGE_SIZE")

# This list is used in order to show full status of the process. For more information, see: "https://man7.org/linux/man-pages/man5/proc.5.html".
process_status_dict = {"R": "Running", "S": "Sleeping", "D": "Waiting", "I": "Idle", "Z": "Zombie", "T": "Stopped", "t": "Tracing Stop", "X": "Dead"}
# Define process status text list for translation
process_status_list = [_tr("Running"), _tr("Sleeping"), _tr("Waiting"), _tr("Idle"), _tr("Zombie"), _tr("Stopped")]


def get_tab_object():
    """
    Get object of the current tab.
    """

    if Config.current_main_tab == 0:
        if Config.performance_tab_current_sub_tab == 0:
            from .Summary import Summary
            TabObject = Summary
        elif Config.performance_tab_current_sub_tab == 1:
            from .Cpu import Cpu
            TabObject = Cpu
        elif Config.performance_tab_current_sub_tab == 2:
            from .Memory import Memory
            TabObject = Memory
        elif Config.performance_tab_current_sub_tab == 3:
            from .Disk import Disk
            TabObject = Disk
        elif Config.performance_tab_current_sub_tab == 4:
            from .Network import Network
            TabObject = Network
        elif Config.performance_tab_current_sub_tab == 5:
            from .Gpu import Gpu
            TabObject = Gpu
        elif Config.performance_tab_current_sub_tab == 6:
            from .Sensors import Sensors
            TabObject = Sensors
    elif Config.current_main_tab == 1:
        from .Processes import Processes
        TabObject = Processes
    elif Config.current_main_tab == 2:
        from .Users import Users
        TabObject = Users
    elif Config.current_main_tab == 3:
        from .Services import Services
        TabObject = Services
    elif Config.current_main_tab == 4:
        from .System import System
        TabObject = System

    return TabObject


class ListStoreItem(GObject.Object):
    __gtype_name__ = 'ListStoreItem'

    def __init__(self, item_name):
        super().__init__()

        self._item_name = item_name

    @GObject.Property
    def item_name(self):
        return self._item_name


def dropdown_model(item_list):
    """
    Generate a model (ListStore) and add items to model.
    """

    model = Gio.ListStore(item_type=ListStoreItem)
    for line_data in item_list:
        model.append(ListStoreItem(item_name=line_data))

    return model


def dropdown_signal_list_item_factory():
    """
    Generate and connect DropDown signals.
    """

    factory = Gtk.SignalListItemFactory()
    factory.connect("setup", on_list_item_factory_setup)
    factory.connect("bind", on_list_item_factory_bind)

    return factory


def on_list_item_factory_setup(factory, list_item):
    """
    Generate child widget of the list item.
    This widget can be simple or complex widget.
    """

    label = Gtk.Label()
    label.set_halign(Gtk.Align.START)
    list_item.set_child(label)


def on_list_item_factory_bind(factory, list_item):
    """
    Bind the list item to the row widget.
    """

    label = list_item.get_child()
    list_data = list_item.get_item()
    label.set_label(str(list_data.item_name))


def main_tab_togglebutton(text, image_name):
    """
    Generate main tab ToggleButton and its widgets.
    """

    # ToggleButton
    togglebutton = Gtk.ToggleButton()
    togglebutton.set_group(None)

    # Grid
    grid = Gtk.Grid.new()
    grid.set_row_homogeneous(True)
    grid.set_halign(Gtk.Align.CENTER)
    grid.set_valign(Gtk.Align.CENTER)
    togglebutton.set_child(grid)

    # Image
    image = Gtk.Image()
    image.set_from_icon_name(image_name)
    image.set_pixel_size(24)
    grid.attach(image, 0, 0, 1, 1)

    # Label
    label = Gtk.Label()
    label.set_label(text)
    grid.attach(label, 0, 1, 1, 1)

    return togglebutton


def sub_tab_togglebutton(text, image_name):
    """
    Generate Performance tab sub-tab ToggleButton and its widgets.
    """

    # ToggleButton
    togglebutton = Gtk.ToggleButton()
    togglebutton.set_group(None)

    # Grid
    grid = Gtk.Grid.new()
    grid.set_column_spacing(3)
    grid.set_valign(Gtk.Align.CENTER)
    grid.set_margin_top(2)
    grid.set_margin_bottom(2)
    togglebutton.set_child(grid)

    # Image
    image = Gtk.Image()
    image.set_from_icon_name(image_name)
    image.set_pixel_size(24)
    grid.attach(image, 0, 0, 1, 1)

    # Label
    label = Gtk.Label()
    label.set_label(text)
    grid.attach(label, 1, 0, 1, 1)

    return togglebutton


def reset_button():
    """
    Generate "Reset" button for menus and settings window.
    """

    button = Gtk.Button()
    button.set_label(_tr("Reset"))
    button.set_halign(Gtk.Align.CENTER)

    return button


def refresh_button(function):
    """
    Generate "Refresh" button.
    """

    refresh_button = Gtk.Button()
    refresh_button.set_tooltip_text(_tr("Refresh the data on this tab"))
    refresh_button.set_hexpand(True)
    refresh_button.set_halign(Gtk.Align.END)
    refresh_button.set_valign(Gtk.Align.CENTER)
    refresh_button.set_icon_name("view-refresh-symbolic")

    refresh_button.connect("clicked", function)

    return refresh_button


def graph_color_button():
    """
    Generate "Graph Color" button for menus.
    """

    button = Gtk.Button()
    button.set_label(_tr("Graph Color"))
    button.set_halign(Gtk.Align.CENTER)

    button.connect("clicked", on_graph_color_button_clicked)

    return button


def on_graph_color_button_clicked(widget):
    """
    Change graph foreground color.
    Also get current foreground color of the graph and set it as selected color of the dialog.
    """

    # Generate a ColorChooserDialog
    main_window = widget.get_root()
    menu_colorchooserdialog(main_window)

    # Get graph color of the tab
    if Config.current_main_tab == 0:
        if Config.performance_tab_current_sub_tab == 1:
            tab_graph_color = Config.chart_line_color_cpu_percent
            from .CpuMenu import CpuMenu
            current_menu_po = CpuMenu.menu_po
        elif Config.performance_tab_current_sub_tab == 2:
            tab_graph_color = Config.chart_line_color_memory_percent
            from .MemoryMenu import MemoryMenu
            current_menu_po = MemoryMenu.menu_po
        elif Config.performance_tab_current_sub_tab == 3:
            tab_graph_color = Config.chart_line_color_disk_speed_usage
            from .DiskMenu import DiskMenu
            current_menu_po = DiskMenu.menu_po
        elif Config.performance_tab_current_sub_tab == 4:
            tab_graph_color = Config.chart_line_color_network_speed_data
            from .NetworkMenu import NetworkMenu
            current_menu_po = NetworkMenu.menu_po
        elif Config.performance_tab_current_sub_tab == 5:
            tab_graph_color = Config.chart_line_color_fps
            from .GpuMenu import GpuMenu
            current_menu_po = GpuMenu.menu_po

    # Set selected color on the ColorChooserDialog
    color = Gdk.RGBA()
    color.red, color.green, color.blue, color.alpha = tab_graph_color
    colorchooserdialog.set_rgba(color)

    # Show the ColorChooserDialog
    current_menu_po.popdown()
    colorchooserdialog.present()


def menu_colorchooserdialog(main_window):
    """
    Generate ColorChooserDialog.
    """

    if 'colorchooserdialog' not in globals():
        global colorchooserdialog
        colorchooserdialog = Gtk.ColorChooserDialog().new(title=_tr("Graph Color"), parent=main_window)
        colorchooserdialog.set_modal(True)

        colorchooserdialog.connect("response", on_colorchooserdialog_response)


def on_colorchooserdialog_response(widget, response):
    """
    Get selected color, apply it to graph and save it.
    Dialog have to be hidden for "Cancel" response.
    """

    colorchooserdialog.set_visible(False)

    if response == Gtk.ResponseType.OK:

        # Get the selected color
        selected_color = colorchooserdialog.get_rgba()
        tab_graph_color = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        # Set graph color of the tab and apply changes immediately (without waiting update interval)
        if Config.current_main_tab == 0:
            if Config.performance_tab_current_sub_tab == 1:
                Config.chart_line_color_cpu_percent = tab_graph_color
                from .Cpu import Cpu
                Cpu.cpu_initial_func()
                Cpu.cpu_loop_func()
            elif Config.performance_tab_current_sub_tab == 2:
                Config.chart_line_color_memory_percent = tab_graph_color
                from .Memory import Memory
                Memory.memory_initial_func()
                Memory.memory_loop_func()
            elif Config.performance_tab_current_sub_tab == 3:
                Config.chart_line_color_disk_speed_usage = tab_graph_color
                from .Disk import Disk
                Disk.disk_initial_func()
                Disk.disk_loop_func()
            elif Config.performance_tab_current_sub_tab == 4:
                Config.chart_line_color_network_speed_data = tab_graph_color
                from .Network import Network
                Network.network_initial_func()
                Network.network_loop_func()
            elif Config.performance_tab_current_sub_tab == 5:
                Config.chart_line_color_fps = tab_graph_color
                from .Gpu import Gpu
                Gpu.gpu_initial_func()
                Gpu.gpu_loop_func()
        Config.config_save_func()


def drawingarea(drawing_function, drawingarea_tag):
    """
    Generate DrawingArea, set drawing function and connect mouse events.
    """

    drawingarea = Gtk.DrawingArea()
    drawingarea.set_hexpand(True)
    drawingarea.set_vexpand(True)

    # Set drawing function
    if drawingarea_tag == "da_summary":
        drawingarea.set_draw_func(drawing_function)
    else:
        drawingarea.set_draw_func(drawing_function, drawingarea_tag)

    # Drawingarea mouse events
    if drawingarea_tag in ["da_cpu_usage", "da_memory_usage", "da_disk_speed", "da_network_speed", "da_gpu_usage",
                           "processes_details_da_cpu_usage", "processes_details_da_memory_usage", "processes_details_da_disk_speed"]:
        drawingarea_mouse_event = Gtk.EventControllerMotion()
        drawingarea_mouse_event.connect("enter", Performance.performance_line_charts_enter_notify_event)
        drawingarea_mouse_event.connect("leave", Performance.performance_line_charts_leave_notify_event)
        drawingarea_mouse_event.connect("motion", Performance.performance_line_charts_motion_notify_event)
        drawingarea.add_controller(drawingarea_mouse_event)

    return drawingarea


def dropdown_and_model(item_list):
    """
    Generate DropDown and its model.
    """

    dropdown = Gtk.DropDown()

    # Model
    model = dropdown_model(item_list)
    factory = dropdown_signal_list_item_factory()
    dropdown.set_model(model)
    dropdown.set_factory(factory)

    return dropdown


def text_attribute_bold_2x():
    """
    Define text attributes for bold and 2x labels.
    """

    global attribute_list_bold_2x

    attribute_list_bold_2x = Pango.AttrList()
    attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
    attribute_list_bold_2x.insert(attribute)
    attribute = Pango.attr_scale_new(2.0)
    attribute_list_bold_2x.insert(attribute)


def text_attribute_bold():
    """
    Define text attributes for bold labels.
    """

    global attribute_list_bold

    attribute_list_bold = Pango.AttrList()
    attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
    attribute_list_bold.insert(attribute)


def text_attribute_bold_underlined():
    """
    Define text attributes for bold and underlined labels.
    """

    global attribute_list_bold_underlined

    attribute_list_bold_underlined = Pango.AttrList()
    attribute = Pango.attr_weight_new(Pango.Weight.BOLD)
    attribute_list_bold_underlined.insert(attribute)
    attribute = Pango.attr_underline_new(Pango.Underline.SINGLE)
    attribute_list_bold_underlined.insert(attribute)


def text_attribute_small_size():
    """
    Define text attributes for small size (10000 point) labels.
    """

    global attribute_list_small_size

    # Small label atributes
    attribute_list_small_size = Pango.AttrList()
    attribute = Pango.attr_size_new(10000)
    attribute_list_small_size.insert(attribute)


def tab_title_label(text):
    """
    Generate tab title Label.
    """

    if 'attribute_list_bold_2x' not in globals():
        text_attribute_bold_2x()

    # Label
    label = Gtk.Label()
    label.set_halign(Gtk.Align.START)
    label.set_margin_end(60)
    label.set_attributes(attribute_list_bold_2x)
    label.set_label(text)

    return label


def title_label(text):
    """
    Generate title Label.
    """

    if 'attribute_list_bold' not in globals():
        text_attribute_bold()

    label = Gtk.Label()
    label.set_attributes(attribute_list_bold)
    label.set_label(text)
    label.set_halign(Gtk.Align.START)

    return label


def menu_title_label(text):
    """
    Generate menu title Label.
    """

    if 'attribute_list_bold' not in globals():
        text_attribute_bold()

    label = Gtk.Label()
    label.set_attributes(attribute_list_bold)
    label.set_label(text)
    label.set_halign(Gtk.Align.CENTER)
    label.set_margin_bottom(10)

    return label


def device_vendor_model_label():
    """
    Generate device vendor model information Label.
    """

    if 'attribute_list_bold' not in globals():
        text_attribute_bold()

    label = Gtk.Label()
    label.set_halign(Gtk.Align.START)
    label.set_selectable(True)
    label.set_ellipsize(Pango.EllipsizeMode.END)
    label.set_attributes(attribute_list_bold)
    label.set_label("--")

    return label


def device_kernel_name_label():
    """
    Generate device kernel name information Label.
    """

    label = Gtk.Label()
    label.set_halign(Gtk.Align.START)
    label.set_selectable(True)
    label.set_ellipsize(Pango.EllipsizeMode.END)
    label.set_label("--")

    return label


def static_information_label(text):
    """
    Generate static information Label. This label is not updated.
    """

    label = Gtk.Label()
    label.set_label(text)
    label.set_ellipsize(Pango.EllipsizeMode.END)
    label.set_halign(Gtk.Align.START)

    return label


def static_information_label_no_ellipsize(text):
    """
    Generate static information Label. This label is not updated.
    """

    label = Gtk.Label()
    label.set_label(text)
    label.set_halign(Gtk.Align.START)

    return label


def dynamic_information_label():
    """
    Generate dynamic information Label. This label is updated by the code.
    """

    if 'attribute_list_bold' not in globals():
        text_attribute_bold()

    label = Gtk.Label()
    label.set_selectable(True)
    label.set_attributes(attribute_list_bold)
    label.set_label("--")
    label.set_ellipsize(Pango.EllipsizeMode.END)
    label.set_halign(Gtk.Align.START)

    return label


def clickable_label(text, function):
    """
    Generate clickable Label. Mouse cursor is changed when mouse hover action is performed.
    """

    if 'attribute_list_bold_underlined' not in globals():
        text_attribute_bold_underlined()

    label = Gtk.Label()
    label.set_attributes(attribute_list_bold_underlined)
    label.set_label(text)
    label.set_ellipsize(Pango.EllipsizeMode.END)
    label.set_halign(Gtk.Align.START)
    cursor_link = Gdk.Cursor.new_from_name("pointer")
    label.set_cursor(cursor_link)

    # Label mouse events. Definition of separate events are required for different widgets.
    mouse_event = Gtk.GestureClick()
    mouse_event.connect("released", function)
    label.add_controller(mouse_event)

    return label


def da_upper_lower_label(text, alignment):
    """
    Generate Label above or below DrawingArea.
    """

    label = Gtk.Label()
    label.set_halign(alignment)
    label.add_css_class("dim-label")
    label.set_label(text)

    return label


def performance_summary_headerbar_label(text):
    """
    Generate Label for performance summary on the window headerbar.
    """

    if 'attribute_list_small_size' not in globals():
        text_attribute_small_size()

    label = Gtk.Label()
    label.set_attributes(attribute_list_small_size)
    label.set_halign(Gtk.Align.START)
    label.set_label(text)

    return label


def menu_separator():
    """
    Generate horizontal separator for menus.
    """

    separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    separator.set_margin_top(3)
    separator.set_margin_bottom(3)

    return separator


def settings_window_separator():
    """
    Generate horizontal separator for menus.
    """

    separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    separator.set_margin_top(5)
    separator.set_margin_bottom(5)

    return separator


def performance_info_grid():
    """
    Generate grid for performance information labels, drawingareas (bar), etc. on CPU, Disk, Network, GPU tabs.
    """

    grid = Gtk.Grid()
    grid.set_column_homogeneous(True)
    grid.set_row_homogeneous(True)
    grid.set_column_spacing(12)
    grid.set_row_spacing(10)

    return grid


def performance_info_right_grid():
    """
    Generate grid for performance information labels (right side) on CPU, Disk, Network, GPU tabs.
    """

    grid = Gtk.Grid()
    grid.set_column_homogeneous(True)
    grid.set_row_homogeneous(True)
    grid.set_column_spacing(2)
    grid.set_row_spacing(4)

    return grid


def tab_grid():
    """
    Generate tab Grid (root widget of the tab in the tab module).
    """

    tab_grid = Gtk.Grid()
    tab_grid.set_row_spacing(10)
    tab_grid.set_margin_top(2)
    tab_grid.set_margin_bottom(2)
    tab_grid.set_margin_start(2)
    tab_grid.set_margin_end(2)

    return tab_grid


def menu_main_grid():
    """
    Generate menu main Grid.
    """

    main_grid = Gtk.Grid()
    main_grid.set_row_spacing(2)
    main_grid.set_margin_top(2)
    main_grid.set_margin_bottom(2)
    main_grid.set_margin_start(2)
    main_grid.set_margin_end(2)

    return main_grid


def window_main_grid():
    """
    Generate window main Grid.
    """

    main_grid = Gtk.Grid.new()
    main_grid.set_margin_top(10)
    main_grid.set_margin_bottom(10)
    main_grid.set_margin_start(10)
    main_grid.set_margin_end(10)
    main_grid.set_column_spacing(10)
    main_grid.set_row_spacing(5)

    return main_grid


def window_main_scrolledwindow():
    """
    Generate window main ScroledWindow.
    """

    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_has_frame(True)
    scrolledwindow.set_hexpand(True)
    scrolledwindow.set_vexpand(True)
    scrolledwindow.set_margin_top(10)
    scrolledwindow.set_margin_bottom(10)
    scrolledwindow.set_margin_start(10)
    scrolledwindow.set_margin_end(10)

    return scrolledwindow


def style_provider_scrolledwindow_separator():
    """
    Define style provider for ScrolledWindow and Separator on for styled information.
    """

    global style_provider_scrolledwindow, style_provider_separator

    # Define style provider for scrolledwindow for border radius.
    style_provider_scrolledwindow = Gtk.CssProvider()
    try:
        css = b"scrolledwindow {border-radius: 8px 8px 8px 8px;}"
        style_provider_scrolledwindow.load_from_data(css)
    except Exception:
        css = "scrolledwindow {border-radius: 8px 8px 8px 8px;}"
        style_provider_scrolledwindow.load_from_data(css, len(css))

    # Add separators for showing lines with contrast colors between some the performance data and set color of the separators.
    style_provider_separator = Gtk.CssProvider()
    try:
        css = b"separator {background: rgba(50%,50%,50%,0.6);}"
        style_provider_separator.load_from_data(css)
    except Exception:
        css = "separator {background: rgba(50%,50%,50%,0.6);}"
        style_provider_separator.load_from_data(css, len(css))


def styled_information_scrolledwindow(text1, tooltip1, text2, tooltip2):
    """
    Generate styled information ScrolledWindow (grid, labels, separators on it).
    """

    if 'style_provider_scrolledwindow' not in globals() or 'style_provider_separator' not in globals():
        style_provider_scrolledwindow_separator()

    # ScrolledWindow (text1 and text2)
    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_has_frame(True)
    scrolledwindow.get_style_context().add_provider(style_provider_scrolledwindow, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    scrolledwindow.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)

    # Grid (text1 and text2)
    grid = Gtk.Grid()
    grid.set_column_homogeneous(True)
    grid.set_row_spacing(3)
    grid.set_margin_top(5)
    grid.set_margin_bottom(5)
    grid.set_margin_start(5)
    grid.set_margin_end(5)
    grid.set_valign(Gtk.Align.CENTER)
    scrolledwindow.set_child(grid)

    # Label (text1)
    label = static_information_label(text1)
    if tooltip1 != None:
        label.set_tooltip_text(tooltip1)
    label.set_halign(Gtk.Align.CENTER)
    grid.attach(label, 0, 0, 1, 1)

    # Label (text2)
    label = static_information_label(text2)
    if tooltip2 != None:
        label.set_tooltip_text(tooltip2)
    label.set_halign(Gtk.Align.CENTER)
    grid.attach(label, 1, 0, 1, 1)

    # Separator
    separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    separator.set_halign(Gtk.Align.CENTER)
    separator.set_valign(Gtk.Align.CENTER)
    separator.set_size_request(60, -1)
    separator.get_style_context().add_provider(style_provider_separator, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    grid.attach(separator, 0, 1, 1, 1)

    # Separator
    separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    separator.set_halign(Gtk.Align.CENTER)
    separator.set_valign(Gtk.Align.CENTER)
    separator.set_size_request(60, -1)
    separator.get_style_context().add_provider(style_provider_separator, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    grid.attach(separator, 1, 1, 1, 1)

    # Label (text1)
    label1 = dynamic_information_label()
    label1.set_halign(Gtk.Align.CENTER)
    grid.attach(label1, 0, 2, 1, 1)

    # Label (text2)
    label2 = dynamic_information_label()
    label2.set_halign(Gtk.Align.CENTER)
    grid.attach(label2, 1, 2, 1, 1)

    return scrolledwindow, label1, label2


def searchentry(function):
    """
    Generate SearchEntry.
    """

    searchentry = Gtk.SearchEntry()
    searchentry.props.placeholder_text = _tr("Search...")
    searchentry.set_max_width_chars(100)
    searchentry.set_hexpand(True)
    searchentry.set_halign(Gtk.Align.CENTER)
    searchentry.set_valign(Gtk.Align.CENTER)

    searchentry.connect("changed", function)

    return searchentry


def searchentry_focus_action_and_accelerator(main_window_object):
    """
    Define action and accelerator for SearchEntry widgets.
    """

    MainWindow = main_window_object

    # Prevent defining action and accelerator if they were defined before.
    action = MainWindow.main_window.lookup_action("searchentry_focus")
    if action != None:
        return

    # SearchEntry focus action
    action = Gio.SimpleAction.new("searchentry_focus", None)
    action.connect("activate", searchentry_grab_focus)
    MainWindow.main_window.add_action(action)

    # Accelerator for SearchEntry focus action
    application = MainWindow.main_window.get_application()
    application.set_accels_for_action("win.searchentry_focus", ["<Control>F"])


def searchentry_grab_focus(action, parameter):
    """
    Sets focus for the SearchEntry. This function is called if "Ctrl+F" buttons are pressed.
    """

    # Get SearchEntry for focusing. This function is called on veery tab.
    # Because the accelerator is defined for window for a simpler code.
    if Config.current_main_tab == 0 and Config.performance_tab_current_sub_tab == 6:
        from .Sensors import Sensors
        searchentry = Sensors.searchentry
    elif Config.current_main_tab == 1:
        from .Processes import Processes
        searchentry = Processes.searchentry
    elif Config.current_main_tab == 2:
        from .Users import Users
        searchentry = Users.searchentry
    elif Config.current_main_tab == 3:
        from .Services import Services
        searchentry = Services.searchentry
    else:
        return

    searchentry.grab_focus()


def searchentry_update_placeholder_text():
    """
    Update placeholder text (row count) on SearchEntry.
    """

    TabObject = get_tab_object()
    searchentry = TabObject.searchentry
    tab_data_rows = TabObject.tab_data_rows

    # Get row type
    if Config.current_main_tab == 0 and Config.performance_tab_current_sub_tab == 6:
        row_type = _tr("Sensors")
    elif Config.current_main_tab == 1:
        row_type = _tr("Processes")
    elif Config.current_main_tab == 2:
        row_type = _tr("Users")
    elif Config.current_main_tab == 3:
        row_type = _tr("Services")

    searchentry.props.placeholder_text = _tr("Search...") + "                    " + "(" + row_type + ": " + str(len(tab_data_rows)) + ")"


def checkbutton(text, group_cb):
    """
    Generate CheckButton or RadioButton.
    """

    checkbutton = Gtk.CheckButton()
    checkbutton.set_halign(Gtk.Align.START)
    checkbutton.set_label(text)
    if group_cb != None:
        checkbutton.set_group(group_cb)

    return checkbutton


def set_label_spinner(label, spinner, label_data):
    """
    Stop and hide spinner and show set label text.
    """

    spinner.stop()
    spinner.set_visible(False)
    label.set_label(f'{label_data}')


def treeview_add_remove_columns():
    """
    Add/Remove treeview columns appropriate for user preferences.
    Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if
    column numbers are changed. Because once treestore data types (str, int, etc) are defined, they
    can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal
    can not be performed.
    """

    TabObject = get_tab_object()
    treeview = TabObject.treeview
    row_data_list = TabObject.row_data_list
    treeview_columns_shown_prev = TabObject.treeview_columns_shown_prev

    # Get treeview columns shown
    if Config.current_main_tab == 0 and Config.performance_tab_current_sub_tab == 6:
        treeview_columns_shown = Config.sensors_treeview_columns_shown
    elif Config.current_main_tab == 1:
        treeview_columns_shown = Config.processes_treeview_columns_shown
    elif Config.current_main_tab == 2:
        treeview_columns_shown = Config.users_treeview_columns_shown
    elif Config.current_main_tab == 3:
        treeview_columns_shown = Config.services_treeview_columns_shown

    # Add/Remove treeview columns if they are changed since the last loop.
    reset_row_unique_data_list_prev = "no"
    if treeview_columns_shown != treeview_columns_shown_prev:
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        # Remove all columns in the treeview.
        for column in treeview.get_columns():
            treeview.remove_column(column)
        for i, column in enumerate(treeview_columns_shown):
            if row_data_list[column][0] in treeview_columns_shown:
                cumulative_sort_column_id = cumulative_sort_column_id + row_data_list[column][2]
            # Define column (also column title is defined)
            treeview_column = Gtk.TreeViewColumn(row_data_list[column][1])
            for i, cell_renderer_type in enumerate(row_data_list[column][6]):
                cumulative_internal_data_id = cumulative_internal_data_id + 1
                # Continue to next loop to avoid generating a cell renderer for internal column
                # (internal columns are not shown on the treeview and they do not have cell renderers).
                if cell_renderer_type == "internal_column":
                    continue
                # Define cell renderer
                if cell_renderer_type == "CellRendererPixbuf":
                    cell_renderer = Gtk.CellRendererPixbuf()
                if cell_renderer_type == "CellRendererText":
                    cell_renderer = Gtk.CellRendererText()
                if cell_renderer_type == "CellRendererToggle":
                    cell_renderer = Gtk.CellRendererToggle()
                # Vertical alignment is set 0.5 in order to leave it as unchanged.
                cell_renderer.set_alignment(row_data_list[column][9][i], 0.5)
                # Set if column will allocate unused space
                treeview_column.pack_start(cell_renderer, row_data_list[column][10][i])
                treeview_column.add_attribute(cell_renderer, row_data_list[column][7][i], cumulative_internal_data_id)
                if row_data_list[column][11][i] != "no_cell_function":
                    treeview_column.set_cell_data_func(cell_renderer, row_data_list[column][11][i], func_data=cumulative_internal_data_id)    # Define cell function which sets cell data precision and/or data unit
            treeview_column.set_sizing(2)                                           # Set column sizing (2 = auto sizing which is required for "treeview.set_fixed_height_mode(True)" command that is used for lower treeview CPU consumption because row heights are not calculated for every row).
            treeview_column.set_sort_column_id(cumulative_sort_column_id)           # Be careful with lists contain same element more than one.
            treeview_column.set_resizable(True)                                     # Set columns resizable by the user when column title button edge handles are dragged.
            treeview_column.set_reorderable(True)                                   # Set columns reorderable by the user when column title buttons are dragged.
            treeview_column.set_min_width(50)                                       # Set minimum column widths as "50 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            treeview_column.connect("clicked", on_column_title_clicked)             # Connect signal for column title button clicks. Getting column ordering and row sorting will be performed by using this signal.
            treeview_column.connect("notify::width", treeview_column_order_width_row_sorting)
            treeview.append_column(treeview_column)                                 # Append column into treeview

        # Get column data types for appending row data into treestore
        data_column_types = []
        for column in sorted(treeview_columns_shown):
            internal_column_count = len(row_data_list[column][5])
            for internal_column_number in range(internal_column_count):
                data_column_types.append(row_data_list[column][5][internal_column_number])    # Get column types (int, bool, float, str, etc.)

        # Define a treestore (for storing treeview data in it), a treemodelfilter (for search filtering),
        # treemodelsort (for row sorting when column title buttons are clicked)
        TabObject.treestore = Gtk.TreeStore()
        TabObject.treestore.set_column_types(data_column_types)                     # Set column types of the columns which will be appended into treestore
        treemodelfilter = TabObject.treestore.filter_new()
        treemodelfilter.set_visible_column(0)                                       # Column "0" of the treestore will be used for column visibility information (True or False)
        treemodelsort = Gtk.TreeModelSort().new_with_model(treemodelfilter)
        treeview.set_model(treemodelsort)
        TabObject.piter_list = []
        reset_row_unique_data_list_prev = "yes"                                     # For redefining (clear) "pid_list_prev, human_user_uid_list_prev, service_list_prev" lists. Thus code will recognize this and data will be appended into treestore and piter_list from zero.

    return reset_row_unique_data_list_prev


def get_new_deleted_updated_rows(row_id_list, row_id_list_prev):
    """
    Get new/deleted/updated rows for updating treestore/treeview.
    """

    row_id_list_prev_set = set(row_id_list_prev)
    row_id_list_set = set(row_id_list)
    deleted_rows = sorted(list(row_id_list_prev_set - row_id_list_set))
    new_rows = sorted(list(row_id_list_set - row_id_list_prev_set))
    existing_rows = sorted(list(row_id_list_set.intersection(row_id_list_prev)))
    # "c = set(a).intersection(b)" is about 19% faster than "c = set(a).intersection(set(b))"
    updated_existing_row_index = [[row_id_list.index(i), row_id_list_prev.index(i)] for i in existing_rows]

    return deleted_rows, new_rows, updated_existing_row_index


def update_treestore_rows(rows_data_dict, deleted_rows, new_rows, updated_existing_row_index, row_id_list, row_id_list_prev, show_rows_as_tree=0):
    """
    Add/Remove/Update treestore rows.
    """

    TabObject = get_tab_object()
    treestore = TabObject.treestore
    piter_list = TabObject.piter_list
    searchentry = TabObject.searchentry
    on_searchentry_changed = TabObject.on_searchentry_changed
    tab_data_rows = TabObject.tab_data_rows
    tab_data_rows_prev = TabObject.tab_data_rows_prev

    if Config.current_main_tab == 1:
        show_processes_of_all_users = TabObject.show_processes_of_all_users

    tab_data_rows_row_length = len(tab_data_rows[0])
    if len(piter_list) > 0:
        for i, j in updated_existing_row_index:
            if tab_data_rows[i] != tab_data_rows_prev[j]:
                # Start from "1" in order to set first element (treeview row visibility data) as "True" in every loop.
                for k in range(1, tab_data_rows_row_length):
                    if tab_data_rows_prev[j][k] != tab_data_rows[i][k]:
                        treestore.set_value(piter_list[j], k, tab_data_rows[i][k])
    if len(deleted_rows) > 0:
        for row in reversed(sorted(list(deleted_rows))):
            treestore.remove(piter_list[row_id_list_prev.index(row)])
            piter_list.remove(piter_list[row_id_list_prev.index(row)])
        # Update search results
        on_searchentry_changed(searchentry)
    if len(new_rows) > 0:
        for row in new_rows:
            pid_index = row_id_list.index(row)
            if show_rows_as_tree == 1:
                row_data_dict = rows_data_dict[row]
                parent_row = row_data_dict["ppid"]
                if parent_row == 0:                                                           # Row ppid was set as "0" if it has no parent row. Row is set as tree root (this root has no relationship between root user) row if it has no ppid (parent row). Treeview tree indentation is first level for the tree root row.
                    piter_list.append(treestore.append(None, tab_data_rows[pid_index]))
                else:
                    if show_processes_of_all_users == 1:                                      # Row appended under tree root row or another row if "Show [ROWS] as tree" option is preferred.
                        piter_list.append(treestore.append(piter_list[row_id_list.index(parent_row)], tab_data_rows[pid_index]))
                    if show_processes_of_all_users == 0 and parent_row not in row_id_list:    # Row is appended into treeview as tree root row if "Show [ROWS] of all users" is not preferred and row ppid not in row_id_list.
                        piter_list.append(treestore.append(None, tab_data_rows[pid_index]))
                    if show_processes_of_all_users == 0 and parent_row in row_id_list:        # Row is appended into treeview under tree root row or another row if "Show [ROWS] of all users" is preferred and row ppid is in row_id_list.
                        piter_list.append(treestore.append(piter_list[row_id_list.index(parent_row)], tab_data_rows[pid_index]))
            else:                                                                             # All rows are appended into treeview as tree root row if "Show [ROWS] as tree" is not preferred. Thus rows are listed as list structure instead of tree structure.
                piter_list.insert(pid_index, treestore.insert(None, pid_index, tab_data_rows[pid_index]))
        # Update search results
        on_searchentry_changed(searchentry)


def treeview_reorder_columns_sort_rows_set_column_widths():
    """
    Reorder TreeView columns, sort TreeView rows and set TreeView columns.
    """

    TabObject = get_tab_object()
    treeview = TabObject.treeview
    row_data_list = TabObject.row_data_list
    treeview_columns_shown = TabObject.treeview_columns_shown
    data_column_order = TabObject.data_column_order
    data_row_sorting_column = TabObject.data_row_sorting_column
    data_row_sorting_order = TabObject.data_row_sorting_order
    data_column_widths = TabObject.data_column_widths
    treeview_columns_shown_prev = TabObject.treeview_columns_shown_prev
    data_column_order_prev = TabObject.data_column_order_prev
    data_row_sorting_column_prev = TabObject.data_row_sorting_column_prev
    data_row_sorting_order_prev = TabObject.data_row_sorting_order_prev
    data_column_widths_prev = TabObject.data_column_widths_prev

    # Reorder columns if this is the first loop (columns are appended into treeview as unordered) or
    # user has reset column order from customizations.
    if treeview_columns_shown_prev != treeview_columns_shown or data_column_order_prev != data_column_order:
        # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_columns = treeview.get_columns()
        treeview_column_titles = []
        for column in treeview_columns:
            treeview_column_titles.append(column.get_title())
        data_column_order_scratch = []
        for column_order in data_column_order:
            if column_order != -1:
                data_column_order_scratch.append(column_order)
        # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
        for order in reversed(sorted(data_column_order_scratch)):
            if data_column_order.index(order) in treeview_columns_shown:
                column_number_to_move = data_column_order.index(order)
                column_title_to_move = row_data_list[column_number_to_move][1]
                column_to_move = treeview_columns[treeview_column_titles.index(column_title_to_move)]
                # Column is moved at the beginning of the treeview if "None" is used.
                treeview.move_column_after(column_to_move, None)

    # Sort rows if user has changed row sorting column and sorting order (ascending/descending) by clicking
    # on any column title button on the GUI.
    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid
    # reordering/sorting in every loop.
    if treeview_columns_shown_prev != treeview_columns_shown or \
       data_row_sorting_column_prev != data_row_sorting_column or \
       data_row_sorting_order != data_row_sorting_order_prev:
        # Get shown columns on the treeview in order to use this data for reordering the columns.
        treeview_columns = treeview.get_columns()
        treeview_column_titles = []
        for column in treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i in range(10):
            if data_row_sorting_column in treeview_columns_shown:
                for data in row_data_list:
                    if data[0] == data_row_sorting_column:
                        column_title_for_sorting = data[1]
            if data_row_sorting_column not in treeview_columns_shown:
                column_title_for_sorting = row_data_list[0][1]
            column_for_sorting = treeview_columns[treeview_column_titles.index(column_title_for_sorting)]
            column_for_sorting.clicked()                                                      # For row sorting.
            if data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                break

    # Set column widths if there are changes since last loop.
    if treeview_columns_shown_prev != treeview_columns_shown or data_column_widths_prev != data_column_widths:
        treeview_columns = treeview.get_columns()
        treeview_column_titles = []
        for column in treeview_columns:
            treeview_column_titles.append(column.get_title())
        for i, row_data in enumerate(row_data_list):
            for j, column_title in enumerate(treeview_column_titles):
                if column_title == row_data[1]:
                   column_width = data_column_widths[i]
                   # Set column width in pixels. Fixed width is unset if value is "-1".
                   treeview_columns[j].set_fixed_width(column_width)


def treeview_column_order_width_row_sorting(widget=None, parameter=None):
    """
    Get and save column order/width, row sorting.
    Columns in the treeview are get one by one and appended into "data_column_order".
    "data_column_widths" list elements are modified for widths of every columns in the treeview.
    Length of these list are always same even if columns are removed, appended and column widths are changed.
    Only values of the elements (element indexes are always same with "row_data_list") are changed if column order/widths are changed.
    """

    TabObject = get_tab_object()
    treeview = TabObject.treeview
    row_data_list = TabObject.row_data_list

    # Get previous column order and widths
    if Config.current_main_tab == 0 and Config.performance_tab_current_sub_tab == 6:
        data_column_order_prev = Config.sensors_data_column_order
        data_column_widths_prev = Config.sensors_data_column_widths
    elif Config.current_main_tab == 1:
        data_column_order_prev = Config.processes_data_column_order
        data_column_widths_prev = Config.processes_data_column_widths
    elif Config.current_main_tab == 2:
        data_column_order_prev = Config.users_data_column_order
        data_column_widths_prev = Config.users_data_column_widths
    elif Config.current_main_tab == 3:
        data_column_order_prev = Config.services_data_column_order
        data_column_widths_prev = Config.services_data_column_widths

    # Get new column order and widths
    treeview_columns = treeview.get_columns()
    treeview_column_titles = []
    for column in treeview_columns:
        treeview_column_titles.append(column.get_title())

    data_column_order = [-1] * len(row_data_list)
    data_column_widths = [-1] * len(row_data_list)

    treeview_columns_last_index = len(treeview_columns)-1

    for i, row_data in enumerate(row_data_list):
        for j, column_title in enumerate(treeview_column_titles):
            if column_title == row_data[1]:
                column_index = treeview_column_titles.index(row_data[1])
                data_column_order[i] = column_index
                if j != treeview_columns_last_index:
                    data_column_widths[i] = treeview_columns[column_index].get_width()

    # Prevent saving settings if column order and widths are not changed.
    if data_column_order == data_column_order_prev and data_column_widths == data_column_widths_prev:
        return

    # Save new column order and widths
    if Config.current_main_tab == 1:
        Config.processes_data_column_order = list(data_column_order)
        Config.processes_data_column_widths = list(data_column_widths)
    elif Config.current_main_tab == 2:
        Config.users_data_column_order = list(data_column_order)
        Config.users_data_column_widths = list(data_column_widths)
    elif Config.current_main_tab == 3:
        Config.services_data_column_order = list(data_column_order)
        Config.services_data_column_widths = list(data_column_widths)

    Config.config_save_func()


def on_column_title_clicked(widget):
    """
    Get and save column sorting order.
    """

    TabObject = get_tab_object()
    row_data_list = TabObject.row_data_list

    # Get column title which will be used for getting column number
    data_row_sorting_column_title = widget.get_title()
    for data in row_data_list:
        if data[1] == data_row_sorting_column_title:
            # Get column number
            data_row_sorting_column = data[0]

    # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    data_row_sorting_order = int(widget.get_sort_order())

    # Save new column order and widths
    if Config.current_main_tab == 1:
        Config.processes_data_row_sorting_column = data_row_sorting_column
        Config.processes_data_row_sorting_order = data_row_sorting_order
    elif Config.current_main_tab == 2:
        Config.users_data_row_sorting_column = data_row_sorting_column
        Config.users_data_row_sorting_order = data_row_sorting_order
    elif Config.current_main_tab == 3:
        Config.services_data_row_sorting_column = data_row_sorting_column
        Config.services_data_row_sorting_order = data_row_sorting_order

    Config.config_save_func()


def on_columns_changed(widget):
    """
    Called if number of columns changed.
    """

    TabObject = get_tab_object()
    treeview = TabObject.treeview

    # Get treeview columns shown
    if Config.current_main_tab == 0 and Config.performance_tab_current_sub_tab == 6:
        treeview_columns_shown = Config.sensors_treeview_columns_shown
    elif Config.current_main_tab == 1:
        treeview_columns_shown = Config.processes_treeview_columns_shown
    elif Config.current_main_tab == 2:
        treeview_columns_shown = Config.users_treeview_columns_shown
    elif Config.current_main_tab == 3:
        treeview_columns_shown = Config.services_treeview_columns_shown

    treeview_columns = treeview.get_columns()
    if len(treeview_columns_shown) != len(treeview_columns):
        return
    if treeview_columns[0].get_width() == 0:
        return
    treeview_column_order_width_row_sorting()


def processes_information(process_list=[], processes_of_user="all", cpu_usage_divide_by_cores="yes", detail_level="medium", processes_data_dict_prev={}, system_boot_time=0, username_uid_dict={}):
    """
    Get process information of all/specified processes.
    """

    global number_of_clock_ticks, memory_page_size, process_status_dict

    # Get usernames and UIDs
    if username_uid_dict == {}:
        username_uid_dict = get_username_uid_dict()

    # Get current username which will be used for determining processes from only this user or other users.
    current_user_name = os.environ.get('USER')

    # Redefine core count division number if "Divide CPU usage by core count" option is disabled.
    if cpu_usage_divide_by_cores == "yes":
        core_count_division_number = number_of_logical_cores()
    else:
        core_count_division_number = 1

    # Get system boot time
    if system_boot_time == 0:
        system_boot_time = get_system_boot_time()

    # Read information from procfs files. "/proc/[PID]/smaps" file is not read for all processes. Because reading and
    # processing "/proc/[PID]/smaps" file data for all processes (about 250 processes) requires nearly 1 second on a 4 core CPU (i7-2630QM).
    cat_output_split, global_time, global_cpu_time_all = read_process_information(process_list, detail_level)

    # Define lists for getting process information from command output.
    processes_data_dict = {}
    if processes_data_dict_prev != {}:
        pid_list_prev = processes_data_dict_prev["pid_list"]
        ppid_list_prev = processes_data_dict_prev["ppid_list"]
        process_cpu_times_prev = processes_data_dict_prev["process_cpu_times"]
        disk_read_write_data_prev = processes_data_dict_prev["disk_read_write_data"]
        global_cpu_time_all_prev = processes_data_dict_prev["global_cpu_time_all"]
        global_time_prev = processes_data_dict_prev["global_time"]
    else:
        pid_list_prev = []
        ppid_list_prev = []
        process_cpu_times_prev = {}
        disk_read_write_data_prev = {}
    pid_list = []
    ppid_list = []
    username_list = []
    cmdline_list = []
    process_cpu_times = {}
    disk_read_write_data = {}

    # Get process information from command output.
    cat_output_split_iter = iter(cat_output_split)
    for process_data_stat_statm_status in cat_output_split_iter:
        # Also get second part of the data of the current process.
        if detail_level == "medium":
            process_data_io_cmdline = next(cat_output_split_iter)
        # Also get second and third part of the data of the current process.
        elif detail_level == "high":
            process_data_io_cmdline = next(cat_output_split_iter)
            process_data_smaps = next(cat_output_split_iter)

        # Get process information from "/proc/[PID]/stat" file
        # Skip to next loop if one of the stat, statm, status files is not read.
        try:
            stat_file, statm_file, status_file = process_data_stat_statm_status.split("\n", 2)
        except ValueError:
            continue
        if status_file.startswith("Name:") == False or "" in (stat_file, statm_file, status_file):
            continue
        stat_file_split = stat_file.split()

        # Get PID
        try:
            pid = int(stat_file_split[0])
        except IndexError:
            break

        ppid = int(stat_file_split[-49])
        status = process_status_dict[stat_file_split[-50]]
        # Get process CPU time in user mode (utime + stime)
        cpu_time_user = int(stat_file_split[-39])
        cpu_time_kernel = int(stat_file_split[-38])
        cpu_time = cpu_time_user + cpu_time_kernel
        # Get process RSS (resident set size) memory pages and multiply with memory_page_size in order to convert the value into bytes.
        memory_rss = int(stat_file_split[-29]) * memory_page_size
        # Get process VMS (virtual memory size) memory (this value is in bytes unit).
        memory_vms = int(stat_file_split[-30])
        # Elapsed time between system boot and process start time (measured in clock ticks and need to be divided by sysconf(_SC_CLK_TCK) for converting to wall clock time)
        start_time = (int(stat_file_split[-31]) / number_of_clock_ticks) + system_boot_time
        nice = int(stat_file_split[-34])
        number_of_threads = int(stat_file_split[-33])

        # Get process information from "/proc/[PID]/status" file
        name = status_file.split("Name:\t", 1)[1].split("\n", 1)[0]
        # There are 4 values in the Uid line and first one (real user id = RUID) is get from this file.
        uid = int(status_file.split("\nUid:\t", 1)[1].split("\n", 1)[0].split("\t", 1)[0])
        # There are 4 values in the Gid line and first one (real GID) is get from this file.
        gid = int(status_file.split("\nGid:\t", 1)[1].split("\n", 1)[0].split("\t", 1)[0])

        # Get username
        try:
            username = username_uid_dict[uid]
        except KeyError:
            username = str(uid)

        # Skip to next process information if process information of current user is wanted.
        if processes_of_user == "current" and username != current_user_name:
            continue

        # Get process information from "/proc/[PID]/statm" file
        statm_file_split = statm_file.split()
        # Get shared memory pages and multiply with memory_page_size in order to convert the value into bytes.
        memory_shared = int(statm_file_split[2]) * memory_page_size
        # Get memory
        memory = memory_rss - memory_shared

        # Get process information from "/proc/[PID]/io" and "/proc/[PID]/cmdline" files
        if detail_level == "medium" or detail_level == "high":
            if process_data_io_cmdline.startswith("rchar") == True:
                try:
                    io_cmdline_files_split = process_data_io_cmdline.split("\n", 7)
                    cmdline_file = io_cmdline_files_split[-1]
                except ValueError:
                    io_cmdline_files_split = process_data_io_cmdline.split("\n")
                    cmdline_file = ""
                read_data = int(io_cmdline_files_split[4].split(":")[1])
                written_data = int(io_cmdline_files_split[5].split(":")[1])
            else:
                read_data = 0
                written_data = 0
                cmdline_file = process_data_io_cmdline
                io_cmdline_files_split = "-"

            # "cmdline" content may contain "\x00". They are replaced with " ". Otherwise, file content may be get as "".
            command_line = cmdline_file.replace("\x00", " ")
            if command_line == "":
                command_line = f'[{name}]'

        # Get process information from "/proc/[PID]/smaps" file and other files that are processed previously.
        if detail_level == "high":
            # Get process USS (unique set size) memory and swap memory and convert them to bytes
            process_data_smaps_split = process_data_smaps.split("\n")
            private_clean = 0
            private_dirty = 0
            memory_swap = 0
            for line in process_data_smaps_split:
                if "Private_Clean:" in line:
                    private_clean = private_clean + int(line.split(":")[1].split()[0].strip())
                elif "Private_Dirty:" in line:
                    private_dirty = private_dirty + int(line.split(":")[1].split()[0].strip())
                elif line.startswith("Swap:"):
                    memory_swap = memory_swap + int(line.split(":")[1].split()[0].strip())
            memory_uss = (private_clean + private_dirty) * 1024
            memory_swap = memory_swap * 1024

            # Get other CPU time information (children_user, children_kernel, io_wait)
            cpu_time_children_user = int(stat_file_split[-37])
            cpu_time_children_kernel = int(stat_file_split[-36])
            cpu_time_io_wait = int(stat_file_split[-11])

            # Get numbers of CPU cores that process is run on.
            cpu_numbers = int(stat_file_split[-14])

            # Get UIDs (real, effective, saved)
            uids = status_file.split("\nUid:\t", 1)[1].split("\n", 1)[0].split("\t")
            uid_real, uid_effective, uid_saved = int(uids[0]), int(uids[1]), int(uids[2])

            # Get GIDs (real, effective, saved)
            gids = status_file.split("\nGid:\t", 1)[1].split("\n", 1)[0].split("\t")
            gid_real, gid_effective, gid_saved = int(gids[0]), int(gids[1]), int(gids[2])

            # Get number of context switches (voluntary and nonvoluntary)
            ctx_switches_voluntary = int(status_file.split("\nvoluntary_ctxt_switches:\t", 1)[1].split("\n", 1)[0])
            ctx_switches_nonvoluntary = int(status_file.split("\nnonvoluntary_ctxt_switches:\t", 1)[1].split("\n", 1)[0])

            # Get read count and write count
            if io_cmdline_files_split != "-":
                read_count = int(io_cmdline_files_split[2].split(":")[1])
                write_count = int(io_cmdline_files_split[3].split(":")[1])
            else:
                read_count = 0
                write_count = 0

        # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters
        # (it is counted as 15). "/proc/[PID]/cmdline" file is read and it is split by the last "/" character 
        # (not all process cmdlines have this) in order to obtain full process name.
        if detail_level == "medium" or detail_level == "high":
            process_name_from_status = name
            if len(name) == 15:
                name = command_line.split("/")[-1].split(" ")[0]
                if name.startswith(process_name_from_status) == False:
                    name = command_line.split(" ")[0].split("/")[-1]
                    if name.startswith(process_name_from_status) == False:
                        name = process_name_from_status

        # Get CPU usage by using CPU times
        process_cpu_time = cpu_time
        process_cpu_times[pid] = process_cpu_time
        try:
            process_cpu_time_prev = process_cpu_times_prev[pid]
        except KeyError:
            # There is no "process_cpu_time_prev" value and get it from "process_cpu_time" if this is first loop of the process.
            process_cpu_time_prev = process_cpu_time
            # Subtract "1" CPU time (a negligible value) if this is first loop of the process.
            global_cpu_time_all_prev = global_cpu_time_all - 1
        cpu_usage = (process_cpu_time - process_cpu_time_prev) / (global_cpu_time_all - global_cpu_time_all_prev) * 100 / core_count_division_number

        # Get disk read speed and disk write speed
        if detail_level == "medium" or detail_level == "high":
            disk_read_write_data[pid] = (read_data, written_data)
            try:
                read_data_prev, written_data_prev = disk_read_write_data_prev[pid]
                update_interval = global_time - global_time_prev
            except (KeyError, NameError) as e:
                # Make read_data_prev and written_data_prev equal to read_data for giving "0" disk read/write speed values
                # if this is first loop of the process
                read_data_prev = read_data
                written_data_prev = written_data
                update_interval = 1
            read_speed = (read_data - read_data_prev) / update_interval
            write_speed = (written_data - written_data_prev) / update_interval

        pid_list.append(pid)
        ppid_list.append(ppid)
        if detail_level == "medium" or detail_level == "high":
            cmdline_list.append(command_line)
        username_list.append(username)

        # Add process data to a sub-dictionary
        if detail_level == "low":
            process_data_dict = {
                                "name" : name,
                                "username" : username,
                                "status" : status,
                                "cpu_time" : cpu_time,
                                "cpu_usage" : cpu_usage,
                                "memory_rss" : memory_rss,
                                "memory_vms" : memory_vms,
                                "memory_shared" : memory_shared,
                                "memory" : memory,
                                "nice" : nice,
                                "number_of_threads" : number_of_threads,
                                "ppid" : ppid,
                                "uid" : uid,
                                "gid" : gid,
                                "start_time" : start_time,
                                }
        elif detail_level == "medium":
            process_data_dict = {
                                "name" : name,
                                "username" : username,
                                "status" : status,
                                "cpu_time" : cpu_time,
                                "cpu_usage" : cpu_usage,
                                "memory_rss" : memory_rss,
                                "memory_vms" : memory_vms,
                                "memory_shared" : memory_shared,
                                "memory" : memory,
                                "read_data" : read_data,
                                "written_data" : written_data,
                                "read_speed" : read_speed,
                                "write_speed" : write_speed,
                                "nice" : nice,
                                "number_of_threads" : number_of_threads,
                                "ppid" : ppid,
                                "uid" : uid,
                                "gid" : gid,
                                "start_time" : start_time,
                                "command_line" : command_line
                                }
        elif detail_level == "high":
            process_data_dict = {
                                "name" : name,
                                "username" : username,
                                "status" : status,
                                "cpu_time" : cpu_time,
                                "cpu_usage" : cpu_usage,
                                "memory_rss" : memory_rss,
                                "memory_vms" : memory_vms,
                                "memory_shared" : memory_shared,
                                "memory" : memory,
                                "memory_uss" : memory_uss,
                                "memory_swap" : memory_swap,
                                "read_data" : read_data,
                                "written_data" : written_data,
                                "read_speed" : read_speed,
                                "write_speed" : write_speed,
                                "nice" : nice,
                                "number_of_threads" : number_of_threads,
                                "ppid" : ppid,
                                "uid" : uid,
                                "gid" : gid,
                                "start_time" : start_time,
                                "command_line" : command_line,
                                "memory_uss": memory_uss,
                                "memory_swap": memory_swap,
                                "cpu_time_user": cpu_time_user,
                                "cpu_time_kernel": cpu_time_kernel,
                                "cpu_time_children_user": cpu_time_children_user,
                                "cpu_time_children_kernel": cpu_time_children_kernel,
                                "cpu_time_io_wait": cpu_time_io_wait,
                                "cpu_numbers": cpu_numbers,
                                "uid_real" : uid_real,
                                "uid_effective" : uid_effective,
                                "uid_saved" : uid_saved,
                                "gid_real" : gid_real,
                                "gid_effective" : gid_effective,
                                "gid_saved" : gid_saved,
                                "ctx_switches_voluntary": ctx_switches_voluntary,
                                "ctx_switches_nonvoluntary": ctx_switches_nonvoluntary,
                                "read_count": read_count,
                                "write_count": write_count
                                }

        # Add process sub-dictionary to dictionary
        processes_data_dict[pid] = process_data_dict

    # Add process related lists and variables for returning them for using them (for using some them as previous data in the next loop).
    processes_data_dict["pid_list"] = pid_list
    processes_data_dict["ppid_list"] = ppid_list
    processes_data_dict["username_list"] = username_list
    processes_data_dict["cmdline_list"] = cmdline_list
    processes_data_dict["process_cpu_times"] = process_cpu_times
    processes_data_dict["disk_read_write_data"] = disk_read_write_data
    processes_data_dict["global_cpu_time_all"] = global_cpu_time_all
    processes_data_dict["global_time"] = global_time

    return processes_data_dict


def read_process_information(process_list, detail_level="medium"):
    """
    Read information from procfs files.
    """

    # Get environment type
    environment_type = environment_type_detection()

    # Get process PIDs
    if process_list == []:
        command_list = ["ls", "/proc/"]
        if environment_type == "flatpak":
            command_list = ["flatpak-spawn", "--host"] + command_list
        ls_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()
        pid_list = []
        for pid in ls_output.split():
            if pid.isdigit() == True:
                pid_list.append(pid)
        pid_list = sorted(pid_list, key=int)
    else:
        pid_list = process_list

    # Get process information from procfs files. "/proc/version" file content is used as separator text.
    command_list = ["env", "LANG=C", "cat"]
    command_list.append('/proc/version')
    if environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    if detail_level == "low":
        for pid in pid_list:
            command_list.extend((
                                f'/proc/{pid}/stat',
                                f'/proc/{pid}/statm',
                                f'/proc/{pid}/status',
                                '/proc/version'
                                ))
    elif detail_level == "medium":
        for pid in pid_list:
            command_list.extend((
                                f'/proc/{pid}/stat',
                                f'/proc/{pid}/statm',
                                f'/proc/{pid}/status',
                                '/proc/version',
                                f'/proc/{pid}/io',
                                f'/proc/{pid}/cmdline',
                                '/proc/version'
                                ))
    elif detail_level == "high":
        for pid in pid_list:
            command_list.extend((
                                f'/proc/{pid}/stat',
                                f'/proc/{pid}/statm',
                                f'/proc/{pid}/status',
                                '/proc/version',
                                f'/proc/{pid}/io',
                                f'/proc/{pid}/cmdline',
                                '/proc/version',
                                f'/proc/{pid}/smaps',
                                '/proc/version'
                                ))
    # Get time just before "/proc/[PID]/stat" file is read in order to calculate an average value.
    time_before = time.time()
    #cat_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)).stdout.strip()
    cat_output = subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    # Get time just after "/proc/[PID]/stat" file is read in order to calculate an average value.
    time_after = time.time()
    # Calculate average values of "global_time" and "global_cpu_time_all".
    global_time = (time_before + time_after) / 2
    global_cpu_time_all = global_time * number_of_clock_ticks
    try:
        cat_output = cat_output.decode().strip()
    except UnicodeDecodeError:
        system_encoding = sys.getfilesystemencoding()
        cat_output = cat_output.decode(system_encoding).strip()

    # Get separator text
    separator_text = cat_output.split("\n", 1)[0]

    cat_output_split = cat_output.split(separator_text + "\n")
    # Delete first empty element
    del cat_output_split[0]

    return cat_output_split, global_time, global_cpu_time_all


def get_application_name_image_dict():
    """
    Get application names and images. Process name will be searched in "application_image_dict" list.
    """

    application_image_dict = {}

    # Get ".desktop" file names
    application_file_list = [file for file in os.listdir("/usr/share/applications/") if file.endswith(".desktop")]

    # Get application name and image information
    for application in application_file_list:

        # "encoding="utf-8"" is used for preventing "UnicodeDecodeError" errors during reading the file content if "C" locale is used.
        try:
            with open("/usr/share/applications/" + application, encoding="utf-8") as reader:
                application_file_content = reader.read()
        except PermissionError:
            continue

        # Do not include application name or icon name if any of them is not found in the .desktop file.
        if "Exec=" not in application_file_content or "Icon=" not in application_file_content:
            continue

        # Get application exec data
        application_exec = application_file_content.split("Exec=", 1)[1].split("\n", 1)[0].split("/")[-1].split(" ")[0]
        # Splitting operation above may give "sh" as application name and this may cause confusion between "sh" process
        # and splitted application exec (for example: sh -c "gdebi-gtk %f"sh -c "gdebi-gtk %f").
        # This statement is used to avoid from this confusion.
        if application_exec == "sh":
            application_exec = application_file_content.split("Exec=", 1)[1].split("\n", 1)[0]

        # Get application image name data
        application_image = application_file_content.split("Icon=", 1)[1].split("\n", 1)[0]

        """# Get "desktop_application/application" information
        if "NoDisplay=" in application_file_content:
            desktop_application_value = application_file_content.split("NoDisplay=", 1)[1].split("\n", 1)[0]
            if desktop_application_value == "true":
                application_type = "application"
            if desktop_application_value == "false":
                application_type = "desktop_application"
        else:
            application_type = "desktop_application"
        """

        application_image_dict[application_exec] = application_image

    return application_image_dict


def number_of_logical_cores():
    """
    Get number of online logical cores.
    """

    try:
        # First try a faster way: using "SC_NPROCESSORS_ONLN" variable.
        number_of_logical_cores = os.sysconf("SC_NPROCESSORS_ONLN")
    except ValueError:
        # As a second try, count by reading from "/proc/cpuinfo" file.
        with open("/proc/cpuinfo") as reader:
            proc_cpuinfo_lines = reader.read().split("\n")
        number_of_logical_cores = 0
        for line in proc_cpuinfo_lines:
            if line.startswith("processor"):
                number_of_logical_cores = number_of_logical_cores + 1

    return number_of_logical_cores


def get_system_boot_time():
    """
    Get system boot time.
    """

    with open("/proc/stat") as reader:
        stat_lines = reader.read().split("\n")
    for line in stat_lines:
        if "btime " in line:
            system_boot_time = int(line.split()[1].strip())

    return system_boot_time


def get_username_uid_dict():
    """
    Get usernames and UIDs.
    """

    environment_type = environment_type_detection()

    if environment_type == "flatpak":
        with open("/var/run/host/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")
    else:
        with open("/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")

    username_uid_dict = {}
    for line in etc_passwd_lines:
        line_splitted = line.split(":", 3)
        username_uid_dict[int(line_splitted[2])] = line_splitted[0]

    return username_uid_dict


def get_etc_passwd_dict():
    """
    Get username, UID, user full name, user termninal information from "/etc/passwd" file.
    """

    environment_type = environment_type_detection()

    if environment_type == "flatpak":
        with open("/var/run/host/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")
    else:
        with open("/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")

    etc_passwd_dict = {}
    for line in etc_passwd_lines:
        line_split = line.split(":", 6)
        uid = int(line_split[2])
        etc_passwd_sub_dict = {
                               "username" : line_split[0],
                               "gid" : int(line_split[3]),
                               "full_name" : line_split[4],
                               "home_dir" : line_split[5],
                               "terminal" : line_split[6]
                               }
        etc_passwd_dict[uid] = etc_passwd_sub_dict

    return etc_passwd_dict


def get_etc_group_dict():
    """
    Get user group name, GID information from "/etc/group" file.
    """

    environment_type = environment_type_detection()

    if environment_type == "flatpak":
        with open("/var/run/host/etc/group") as reader:
            etc_group_lines = reader.read().strip().split("\n")
    else:
        with open("/etc/group") as reader:
            etc_group_lines = reader.read().strip().split("\n")

    etc_group_dict = {}
    for line in etc_group_lines:
        line_split = line.split(":", 3)
        gid = int(line_split[2])
        etc_group_sub_dict = {
                             "user_group_name" : line_split[0]
                             }
        etc_group_dict[gid] = etc_group_sub_dict

    return etc_group_dict


def users_information(users_data_dict_prev={}, system_boot_time=0, username_uid_dict={}):
    """
    Get user information of all/specified users.
    """

    process_list = []
    processes_of_user = "all"
    cpu_usage_divide_by_cores = "yes"
    detail_level = "low"

    # Define lists for getting user information from command output.
    users_data_dict = {}
    if users_data_dict_prev != {}:
        uid_list_prev = users_data_dict_prev["uid_list"]
        processes_data_dict_prev = users_data_dict_prev["processes_data_dict_prev"]
        pid_list_prev = processes_data_dict_prev["pid_list"]
        ppid_list_prev = processes_data_dict_prev["ppid_list"]
        process_cpu_times_prev = processes_data_dict_prev["process_cpu_times"]
        disk_read_write_data_prev = processes_data_dict_prev["disk_read_write_data"]
        global_cpu_time_all_prev = processes_data_dict_prev["global_cpu_time_all"]
        global_time_prev = processes_data_dict_prev["global_time"]
    else:
        uid_list_prev = []
        processes_data_dict_prev = {}
        pid_list_prev = []
        ppid_list_prev = []
        process_cpu_times_prev = {}
        disk_read_write_data_prev = {}
    uid_list = []
    human_user_uid_list = []
    pid_list = []
    ppid_list = []
    username_list = []
    cmdline_list = []
    process_cpu_times = {}
    disk_read_write_data = {}

    # Get process information fo getting logged in, CPU usage percentage, log in time and process count information.
    processes_data_dict = processes_information(process_list, processes_of_user, cpu_usage_divide_by_cores, detail_level, processes_data_dict_prev, system_boot_time, username_uid_dict)
    processes_data_dict_prev = dict(processes_data_dict)

    # Get user and user group information of all users
    etc_passwd_dict = get_etc_passwd_dict()
    etc_group_dict = get_etc_group_dict()

    # Get logged in users list
    logged_in_users_list = processes_data_dict["username_list"]

    # Get UIDs, CPU usage percentages and start times of all processes
    user_process_cpu_usage_start_time_dict = {}
    for pid in processes_data_dict["pid_list"]:
        process_data_dict = processes_data_dict[pid]
        uid = process_data_dict["uid"]
        uid_list.append(uid)
        user_process_cpu_usage_start_time_sub_dict = {
                                                     "uid" : uid,
                                                     "cpu_usage" : process_data_dict["cpu_usage"],
                                                     "start_time" : process_data_dict["start_time"]
                                                     }
        user_process_cpu_usage_start_time_dict[pid] = user_process_cpu_usage_start_time_sub_dict

    # Get user information for all human users
    for uid in etc_passwd_dict.keys():
        etc_passwd_sub_dict = etc_passwd_dict[uid]
        # Get information for only human users
        if uid >= 1000 and uid != 65534:
            human_user_uid_list.append(uid)
            username = etc_passwd_sub_dict["username"]
            if uid in uid_list:
                logged_in = True
            else:
                logged_in = False
            gid = etc_passwd_sub_dict["gid"]
            group_name = etc_group_dict[gid]["user_group_name"]
            full_name = etc_passwd_sub_dict["full_name"]
            home_dir = etc_passwd_sub_dict["home_dir"]
            terminal = etc_passwd_sub_dict["terminal"]

            # Get user processes
            cpu_usage_list = []
            start_time_list = []
            for pid in user_process_cpu_usage_start_time_dict:
                user_process_cpu_usage_start_time_sub_dict = user_process_cpu_usage_start_time_dict[pid]
                user_uid = user_process_cpu_usage_start_time_sub_dict["uid"]
                if user_uid == uid:
                    cpu_usage_list.append(user_process_cpu_usage_start_time_sub_dict["cpu_usage"])
                    start_time_list.append(user_process_cpu_usage_start_time_sub_dict["start_time"])
            if cpu_usage_list == []:
                total_cpu_usage = 0
            else:
                total_cpu_usage = sum(cpu_usage_list)
            if start_time_list == []:
                log_in_time = 0
            else:
                log_in_time = min(start_time_list)
            process_count = len(cpu_usage_list)

            # Add user data to a sub-dictionary
            user_data_dict = {
                             "username" : username,
                             "gid" : gid,
                             "group_name" : group_name,
                             "full_name" : full_name,
                             "logged_in" : logged_in,
                             "home_dir" : home_dir,
                             "terminal" : terminal,
                             "total_cpu_usage" : total_cpu_usage,
                             "log_in_time" : log_in_time,
                             "process_count" : process_count
                             }

            # Add user sub-dictionary to dictionary
            users_data_dict[uid] = user_data_dict

    # Add user related lists and variables for returning them for using them (for using some them as previous data in the next loop).
    users_data_dict["uid_list"] = uid_list
    users_data_dict["human_user_uid_list"] = human_user_uid_list
    users_data_dict["processes_data_dict_prev"] = processes_data_dict_prev

    return users_data_dict


def users_groups_func():
    """
    Get users and user groups.
    """

    environment_type = environment_type_detection()

    # Read all users
    if environment_type == "flatpak":
        with open("/var/run/host/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")
    else:
        with open("/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")

    # Read all user groups
    if environment_type == "flatpak":
        with open("/var/run/host/etc/group") as reader:
            etc_group_lines = reader.read().strip().split("\n")
    else:
        with open("/etc/group") as reader:
            etc_group_lines = reader.read().strip().split("\n")

    user_group_names = []
    user_group_ids = []
    for line in etc_group_lines:
        line_split = line.split(":")
        user_group_names.append(line_split[0])
        user_group_ids.append(line_split[2])

    return etc_passwd_lines, user_group_names, user_group_ids


def environment_type_detection():
    """
    Detect environment type (Flatpak or native).
    This information will be used for accessing host OS commands if the application is run in Flatpak environment.
    """

    application_flatpak_id = os.getenv('FLATPAK_ID')

    if application_flatpak_id != None:
        environment_type = "flatpak"
    else:
        environment_type = "native"

    return environment_type


def device_vendor_model(modalias_output):
    """
    Get device vendor and model information.
    Hardware database of "udev" is used if "hwdata" database is not found. "hwdata" database is updated frequently.
    If hardware database of "hwdata" is found:
      - It is used for PCI, virtio and USB devices.
      - Hardware database of "udev" is used for SDIO devices. This database is copied into "database" folder of the application.
    """

    # Define hardware database file directories.
    udev_database = "no"
    pci_usb_hardware_database_dir = "/usr/share/hwdata/"
    if Config.environment_type == "flatpak":
        pci_usb_hardware_database_dir = "/app/share/hwdata/"
    sdio_hardware_database_dir = os.path.dirname(os.path.realpath(__file__)) + "/../database/"

    # Define hardware database file directories for "udev" if "hwdata" is not installed.
    if os.path.isdir(pci_usb_hardware_database_dir) == False:
        udev_database = "yes"
        # Define "udev" hardware database file directory.
        udev_hardware_database_dir = "/usr/lib/udev/hwdb.d/"
        # Some older Linux distributions use "/lib/" instead of "/usr/lib/" but they are merged under "/usr/lib/" in newer versions.
        if os.path.isdir(udev_hardware_database_dir) == False:
            udev_hardware_database_dir = "/lib/udev/hwdb.d/"
        if Config.environment_type == "flatpak":
            udev_hardware_database_dir = os.path.dirname(os.path.realpath(__file__)) + "/../../../etc/udev/hwdb.d/"

    """# Example modalias file contents for testing.
    modalias_output_list = [
    "usb:v0B95p1790d0100dcFFdscFFdp00icFFiscFFip00in00",
    "virtio:d00000001v00001AF4",
    "sdio:c00v02D0d4324",
    "pci:v000010DEd00000DF4sv00001043sd00001642bc03sc00i00",
    "pci:v0000168Cd0000002Bsv00001A3Bsd00002C37bc02sc80i00",
    "pci:v000010ECd00008168sv00001043sd000016D5bc02sc00i00",
    "pci:v00008086d00000116sv00001043sd00001642bc03sc00i00",
    "pci:v00001B85d00006018sv00001B85sd00006018bc01sc08i02",
    "pci:v0000144Dd0000A808sv0000144Dsd0000A801bc01sc08i02",
    "of:NgpuT<NULL>Cnvidia,tegra210-gm20bCnvidia,gm20b",
    "of:NgpuT(null)Cbrcm,bcm2835-vc4",
    "scsi:t-0x05",
    "scsi:t-0x00"]"""

    # Determine device subtype.
    device_subtype, device_alias = modalias_output.split(":", 1)

    # Get device vendor, model if device subtype is PCI.
    if device_subtype == "pci":

        # Get device IDs from modalias file content.
        first_index = device_alias.find("v")
        last_index = first_index + 8 + 1
        device_vendor_id = device_alias[first_index:last_index]
        first_index = device_alias.find("d")
        last_index = first_index + 8 + 1
        device_model_id = device_alias[first_index:last_index]

        if udev_database == "no":
            # Get search texts
            search_text1 = "\n" + device_vendor_id[5:].lower() + "  "
            search_text2 = "\n\t" + device_model_id[5:].lower() + "  "

            # Read database file
            with open(pci_usb_hardware_database_dir + "pci.ids", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        if udev_database == "yes":
            # Get search texts
            search_text1 = "pci:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
            search_text2 = "pci:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

            # Read database file
            with open(udev_hardware_database_dir + "20-pci-vendor-model.hwdb", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        # Get device vendor, model names
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in rest_of_the_ids_file_output:
                device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
            else:
                device_model_name = "Unknown"
        else:
            device_vendor_name = "Unknown"
            device_model_name = "Unknown"

    # Get device vendor, model if device subtype is virtio.
    elif device_subtype == "virtio":

        # Get device IDs from modalias file content.
        first_index = device_alias.find("v")
        last_index = first_index + 8 + 1
        device_vendor_id = device_alias[first_index:last_index]
        first_index = device_alias.find("d")
        last_index = first_index + 8 + 1
        device_model_id = device_alias[first_index:last_index]
        # 1040 is added to device ID of virtio devices. 
        # For details: https://docs.oasis-open.org/virtio/virtio/v1.1/csprd01/virtio-v1.1-csprd01.html
        device_model_id = "d0000" + str(int(device_model_id.strip("d")) + 1040)

        if udev_database == "no":
            # Get search texts
            search_text1 = "\n" + device_vendor_id[5:].lower() + "  "
            search_text2 = "\n\t" + device_model_id[5:].lower() + "  "

            # Read database file
            with open(pci_usb_hardware_database_dir + "pci.ids", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        if udev_database == "yes":
            # Get search texts
            search_text1 = "pci:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
            search_text2 = "pci:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

            # Read database file
            with open(udev_hardware_database_dir + "20-pci-vendor-model.hwdb", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        # Get device vendor, model names
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in rest_of_the_ids_file_output:
                device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
            else:
                device_model_name = "Unknown"
        else:
            device_vendor_name = "Unknown"
            device_model_name = "Unknown"

    # Get device vendor, model if device subtype is USB.
    elif device_subtype == "usb":

        # Get device IDs from modalias file content.
        first_index = device_alias.find("v")
        last_index = first_index + 4 + 1
        device_vendor_id = device_alias[first_index:last_index]
        first_index = device_alias.find("p")
        last_index = first_index + 4 + 1
        device_model_id = device_alias[first_index:last_index]

        if udev_database == "no":
            # Get search texts
            search_text1 = "\n" + device_vendor_id[1:].lower() + "  "
            search_text2 = "\n\t" + device_model_id[1:].lower() + "  "

            # Read database file
            with open(pci_usb_hardware_database_dir + "usb.ids", encoding="utf-8", errors="ignore") as reader:
                ids_file_output = reader.read()

        if udev_database == "yes":
            # Get search texts
            search_text1 = "usb:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
            search_text2 = "usb:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

            # Read database file
            with open(udev_hardware_database_dir + "20-usb-vendor-model.hwdb", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        # Get device vendor, model names
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in rest_of_the_ids_file_output:
                device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
            else:
                device_model_name = "Unknown"
        else:
            device_vendor_name = "Unknown"
            device_model_name = "Unknown"

    # Get device vendor, model if device subtype is SDIO.
    elif device_subtype == "sdio":

        # Get device IDs from modalias file content.
        first_index = device_alias.find("v")
        last_index = first_index + 4 + 1
        device_vendor_id = device_alias[first_index:last_index]
        first_index = device_alias.find("d")
        last_index = first_index + 4 + 1
        device_model_id = device_alias[first_index:last_index]

        # Get search texts
        search_text1 = "sdio:" + "c*" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
        search_text2 = "sdio:" + "c*" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

        if udev_database == "no":
            # Read database file
            with open(sdio_hardware_database_dir + "/20-sdio-vendor-model.hwdb", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        if udev_database == "yes":
            # Read database file
            with open(udev_hardware_database_dir + "20-sdio-vendor-model.hwdb", encoding="utf-8") as reader:
                ids_file_output = reader.read()

        # Get device vendor, model names
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in rest_of_the_ids_file_output:
                device_model_name = rest_of_the_ids_file_output.split(search_text2, 1)[1].split("\n", 1)[0]
            else:
                device_model_name = "Unknown"
        else:
            device_vendor_name = "Unknown"
            device_model_name = "Unknown"

    # Get device vendor, model if device subtype is of.
    elif device_subtype == "of":

        device_vendor_name = device_vendor_id = device_alias.split("C", 1)[-1].split("C", 1)[0].split(",")[0].title()
        device_model_name = device_model_id = device_alias.split("C", 1)[-1].split("C", 1)[0].split(",")[1].title()

    # Get device vendor, model if device subtype is SCSI or IDE.
    elif device_subtype in ["scsi", "ide"]:

        device_vendor_name = device_vendor_id = "[scsi_or_ide_disk]"
        device_model_name = device_model_id = "[scsi_or_ide_disk]"

    # Set device vendor, model if device subtype is not known so far.
    else:
        device_vendor_name = device_vendor_id = "Unknown"
        device_model_name = device_model_id = "Unknown"

    return device_vendor_name, device_model_name, device_vendor_id, device_model_id


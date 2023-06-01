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


def processes_information(process_list=["all"], processes_of_user="all", cpu_usage_divide_by_cores="yes", processes_data_dict_prev={}, system_boot_time=0, username_uid_dict={}):

    # Get environment type
    environment_type = environment_type_detection()

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

    # Get process PIDs
    command_list = ["ls", "/proc/"]
    if environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    ls_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip()
    pid_list = []
    for pid in ls_output.split():
        if pid.isdigit() == True:
            pid_list.append(pid)
    pid_list = sorted(pid_list, key=int)

    # Get process information from procfs files. "/proc/version" file content is used as separator text.
    command_list = ["cat"]
    command_list.append('/proc/version')
    if environment_type == "flatpak":
        command_list = ["flatpak-spawn", "--host"] + command_list
    for pid in pid_list:
        # Get process information of specified processes.
        if process_list != ["all"] and pid not in process_list:
            continue
        command_list.extend((
        f'/proc/{pid}/stat',
        f'/proc/{pid}/statm',
        f'/proc/{pid}/status',
        '/proc/version',
        f'/proc/{pid}/io',
        f'/proc/{pid}/cmdline',
        '/proc/version'))
    # Get time just before "/proc/[PID]/stat" file is read in order to calculate an average value.
    time_before = time.time()
    cat_output = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)).stdout.strip()
    # Get time just after "/proc/[PID]/stat" file is read in order to calculate an average value.
    time_after = time.time()
    # Calculate average values of "global_time" and "global_cpu_time_all".
    global_time = (time_before + time_after) / 2
    global_cpu_time_all = global_time * number_of_clock_ticks

    # Get separator text
    separator_text = cat_output.split("\n", 1)[0]

    cat_output_split = cat_output.split(separator_text + "\n")
    # Delete first empty element
    del cat_output_split[0]

    # Get process information from command output.
    processes_data_dict = {}
    if processes_data_dict_prev != {}:
        pid_list_prev = processes_data_dict_prev["pid_list"]
        ppid_list_prev = processes_data_dict_prev["ppid_list"]
        global_process_cpu_times_prev = processes_data_dict_prev["global_process_cpu_times"]
        disk_read_write_data_prev = processes_data_dict_prev["disk_read_write_data"]
        global_cpu_time_all_prev = processes_data_dict_prev["global_cpu_time_all"]
        global_time_prev = processes_data_dict_prev["global_time"]
    else:
        pid_list_prev = []
        ppid_list_prev = []
        global_process_cpu_times_prev = []
        disk_read_write_data_prev = []
    pid_list = []
    ppid_list = []
    username_list = []
    cmdline_list = []
    global_process_cpu_times = []
    disk_read_write_data = []
    cat_output_split_iter = iter(cat_output_split)
    for process_data in cat_output_split_iter:
        # Get process information from "/proc/[PID]/stat" file
        # Skip to next loop if one of the stat, statm, status files is not read.
        try:
            stat_file, statm_file, status_file = process_data.split("\n", 2)
        except ValueError:
            process_data = next(cat_output_split_iter)
            continue
        if status_file.startswith("Name:") == False or "" in (stat_file, statm_file, status_file):
            process_data = next(cat_output_split_iter)
            continue
        stat_file_split = stat_file.split()
        try:
            pid = int(stat_file_split[0])
        except IndexError:
            break
        ppid = int(stat_file_split[-49])
        status = process_status_dict[stat_file_split[-50]]
        # Get process CPU time in user mode (utime + stime)
        cpu_time = int(stat_file_split[-39]) + int(stat_file_split[-38])
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
            process_data = next(cat_output_split_iter)
            continue

        # Get process information from "/proc/[PID]/statm" file
        statm_file_split = statm_file.split()
        # Get shared memory pages and multiply with memory_page_size in order to convert the value into bytes.
        memory_shared = int(statm_file_split[2]) * memory_page_size
        # Get memory
        memory = memory_rss - memory_shared

        # Get process information from "/proc/[PID]/io" and "/proc/[PID]/cmdline" files
        process_data = next(cat_output_split_iter)
        if process_data.startswith("rchar") == True:
            try:
                io_cmdline_files_split = process_data.split("\n", 7)
                cmdline_file = io_cmdline_files_split[-1]
            except ValueError:
                io_cmdline_files_split = process_data.split("\n")
                cmdline_file = ""
            read_data = int(io_cmdline_files_split[4].split(":")[1])
            written_data = int(io_cmdline_files_split[5].split(":")[1])
        else:
            read_data = 0
            written_data = 0
            cmdline_file = process_data

        # "cmdline" content may contain "\x00". They are replaced with " ". Otherwise, file content may be get as "".
        command_line = cmdline_file.replace("\x00", " ")
        if command_line == "":
            command_line = f'[{name}]'

        # Linux kernel trims process names longer than 16 (TASK_COMM_LEN, see: https://man7.org/linux/man-pages/man5/proc.5.html) characters
        # (it is counted as 15). "/proc/[PID]/cmdline/" file is read and it is split by the last "/" character 
        # (not all process cmdlines have this) in order to obtain full process name.
        process_name_from_status = name
        if len(name) == 15:
            name = command_line.split("/")[-1].split(" ")[0]
            if name.startswith(process_name_from_status) == False:
                name = command_line.split(" ")[0].split("/")[-1]
                if name.startswith(process_name_from_status) == False:
                    name = process_name_from_status

        # Get CPU usage by using CPU times
        process_cpu_time = cpu_time
        global_process_cpu_times.append((global_cpu_time_all, process_cpu_time))
        try:
            global_cpu_time_all_prev, process_cpu_time_prev = global_process_cpu_times_prev[pid_list_prev.index(pid)]
        except (ValueError, IndexError, UnboundLocalError) as e:
            # There is no "process_cpu_time_prev" value and get it from "process_cpu_time" if this is first loop of the process.
            process_cpu_time_prev = process_cpu_time
            # Subtract "1" CPU time (a negligible value) if this is first loop of the process.
            global_cpu_time_all_prev = global_process_cpu_times[-1][0] - 1
        process_cpu_time_difference = process_cpu_time - process_cpu_time_prev
        global_cpu_time_difference = global_cpu_time_all - global_cpu_time_all_prev
        cpu_usage = process_cpu_time_difference / global_cpu_time_difference * 100 / core_count_division_number

        # Get disk read speed and disk write speed
        try:
            read_data_prev, written_data_prev = disk_read_write_data_prev[pid_list_prev.index(pid)]
        except (ValueError, IndexError, UnboundLocalError) as e:
            # Make read_data_prev and written_data_prev equal to read_data for giving "0" disk read/write speed values
            # if this is first loop of the process
            read_data_prev = read_data
            written_data_prev = written_data
        disk_read_write_data.append((read_data, written_data))
        if pid not in pid_list_prev and disk_read_write_data_prev != []:
            disk_read_write_data_prev.append((read_data, written_data))
        # Prevent errors if this is first loop of the process.
        try:
            update_interval = global_time - global_time_prev
        except UnboundLocalError:
            update_interval = 1
        read_speed = (read_data - read_data_prev) / update_interval
        write_speed = (written_data - written_data_prev) / update_interval

        pid_list.append(pid)
        ppid_list.append(ppid)
        cmdline_list.append(command_line)
        username_list.append(username)

        # Add process data to a sub-dictionary
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

        # Add process sub-dictionary to dictionary
        processes_data_dict[pid] = process_data_dict

    # Add process related lists and variables for returning them for using them (for using some them as previous data in the next loop).
    processes_data_dict["pid_list"] = pid_list
    processes_data_dict["ppid_list"] = ppid_list
    processes_data_dict["username_list"] = username_list
    processes_data_dict["cmdline_list"] = cmdline_list
    processes_data_dict["global_process_cpu_times"] = global_process_cpu_times
    processes_data_dict["disk_read_write_data"] = disk_read_write_data
    processes_data_dict["global_cpu_time_all"] = global_cpu_time_all
    processes_data_dict["global_time"] = global_time

    return processes_data_dict


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
        command_list = ["flatpak-spawn", "--host"]
        command_list = command_list + ["cat", "/etc/passwd"]
        etc_passwd_lines = (subprocess.run(command_list, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)).stdout.decode().strip().split("\n")
    else:
        with open("/etc/passwd") as reader:
            etc_passwd_lines = reader.read().strip().split("\n")

    username_uid_dict = {}
    for line in etc_passwd_lines:
        line_splitted = line.split(":", 3)
        username_uid_dict[int(line_splitted[2])] = line_splitted[0]

    return username_uid_dict


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


import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Gio', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, Gio, GObject, Pango

import os

from locale import gettext as _tr

from Config import Config
from Performance import Performance


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
            from CpuMenu import CpuMenu
            current_menu_po = CpuMenu.menu_po
        elif Config.performance_tab_current_sub_tab == 2:
            tab_graph_color = Config.chart_line_color_memory_percent
            from MemoryMenu import MemoryMenu
            current_menu_po = MemoryMenu.menu_po
        elif Config.performance_tab_current_sub_tab == 3:
            tab_graph_color = Config.chart_line_color_disk_speed_usage
            from DiskMenu import DiskMenu
            current_menu_po = DiskMenu.menu_po
        elif Config.performance_tab_current_sub_tab == 4:
            tab_graph_color = Config.chart_line_color_network_speed_data
            from NetworkMenu import NetworkMenu
            current_menu_po = NetworkMenu.menu_po
        elif Config.performance_tab_current_sub_tab == 5:
            tab_graph_color = Config.chart_line_color_fps
            from GpuMenu import GpuMenu
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

    colorchooserdialog.hide()

    if response == Gtk.ResponseType.OK:

        # Get the selected color
        selected_color = colorchooserdialog.get_rgba()
        tab_graph_color = [selected_color.red, selected_color.green, selected_color.blue, selected_color.alpha]

        # Set graph color of the tab and apply changes immediately (without waiting update interval)
        if Config.current_main_tab == 0:
            if Config.performance_tab_current_sub_tab == 1:
                Config.chart_line_color_cpu_percent = tab_graph_color
                from Cpu import Cpu
                Cpu.cpu_initial_func()
                Cpu.cpu_loop_func()
            elif Config.performance_tab_current_sub_tab == 2:
                Config.chart_line_color_memory_percent = tab_graph_color
                from Memory import Memory
                Memory.memory_initial_func()
                Memory.memory_loop_func()
            elif Config.performance_tab_current_sub_tab == 3:
                Config.chart_line_color_disk_speed_usage = tab_graph_color
                from Disk import Disk
                Disk.disk_initial_func()
                Disk.disk_loop_func()
            elif Config.performance_tab_current_sub_tab == 4:
                Config.chart_line_color_network_speed_data = tab_graph_color
                from Network import Network
                Network.network_initial_func()
                Network.network_loop_func()
            elif Config.performance_tab_current_sub_tab == 5:
                Config.chart_line_color_fps = tab_graph_color
                from Gpu import Gpu
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
    if drawingarea_tag in ["da_cpu_usage", "da_memory_usage", "da_disk_speed_usage", "da_network_speed", "da_gpu_usage",
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
    css = b"scrolledwindow {border-radius: 8px 8px 8px 8px;}"
    style_provider_scrolledwindow = Gtk.CssProvider()
    style_provider_scrolledwindow.load_from_data(css)

    # Add separators for showing lines with contrast colors between some the performance data and set color of the separators.
    css = b"separator {background: rgba(50%,50%,50%,0.6);}"
    style_provider_separator = Gtk.CssProvider()
    style_provider_separator.load_from_data(css)


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


def scrolledwindow_searchentry(function):
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
    spinner.hide()
    label.set_label(f'{label_data}')


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


def device_vendor_model(modalias_output):
    """
    Get device vendor and model information.
    """

    # Define "udev" hardware database file directory.
    udev_hardware_database_dir = "/usr/lib/udev/hwdb.d/"
    # Some older Linux distributions use "/lib/" instead of "/usr/lib/" but they are merged under "/usr/lib/" in newer versions.
    if os.path.isdir(udev_hardware_database_dir) == False:
        udev_hardware_database_dir = "/lib/udev/hwdb.d/"
    if Config.environment_type == "flatpak":
        udev_hardware_database_dir = os.path.dirname(os.path.realpath(__file__)) + "/../../../etc/udev/hwdb.d/"

    # Example modalias file contents for testing.
    # modalias_output = "usb:v0B95p1790d0100dcFFdscFFdp00icFFiscFFip00in00"
    # modalias_output = "virtio:d00000001v00001AF4"
    # modalias_output = "sdio:c00v02D0d4324"
    # modalias_output = "pci:v000010DEd00000DF4sv00001043sd00001642bc03sc00i00"
    # modalias_output = "pci:v0000168Cd0000002Bsv00001A3Bsd00002C37bc02sc80i00"
    # modalias_output = "pci:v000010ECd00008168sv00001043sd000016D5bc02sc00i00"
    # modalias_output = "pci:v00008086d00000116sv00001043sd00001642bc03sc00i00"
    # modalias_output = "pci:v00001B85d00006018sv00001B85sd00006018bc01sc08i02"
    # modalias_output = "pci:v0000144Dd0000A808sv0000144Dsd0000A801bc01sc08i02"
    # modalias_output = "of:NgpuT<NULL>Cnvidia,tegra210-gm20bCnvidia,gm20b"    # NVIDIA Tegra GPU on N.Switch device
    # modalias_output = "of:NgpuT(null)Cbrcm,bcm2835-vc4"
    # modalias_output = "scsi:t-0x05"
    # modalias_output = "scsi:t-0x00"

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

        # Get search texts by using device IDs.
        search_text1 = "pci:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
        search_text2 = "pci:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

        # Read database file for PCI devices.
        with open(udev_hardware_database_dir + "20-pci-vendor-model.hwdb", encoding="utf-8") as reader:
            ids_file_output = reader.read()

        # Get device vendor, model names from device ID file content.
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in ids_file_output:
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

        # Get search texts by using device IDs.
        search_text1 = "pci:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
        search_text2 = "pci:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

        # Read database file for VIRTIO devices.
        with open(udev_hardware_database_dir + "20-pci-vendor-model.hwdb", encoding="utf-8") as reader:
            ids_file_output = reader.read()

        # Get device vendor, model names from device ID file content.
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in ids_file_output:
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

        # Get search texts by using device IDs.
        search_text1 = "usb:" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
        search_text2 = "usb:" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

        # Read database file for USB devices.
        with open(udev_hardware_database_dir + "20-usb-vendor-model.hwdb", encoding="utf-8") as reader:
            ids_file_output = reader.read()

        # Get device vendor, model names from device ID file content.
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in ids_file_output:
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

        # Get search texts by using device IDs.
        search_text1 = "sdio:" + "c*" + device_vendor_id + "*" + "\n ID_VENDOR_FROM_DATABASE="
        search_text2 = "sdio:" + "c*" + device_vendor_id + device_model_id + "*" + "\n ID_MODEL_FROM_DATABASE="

        # Read database file for SDIO devices.
        with open(udev_hardware_database_dir + "20-sdio-vendor-model.hwdb", encoding="utf-8") as reader:
            ids_file_output = reader.read()

        # Get device vendor, model names from device ID file content.
        if search_text1 in ids_file_output:
            rest_of_the_ids_file_output = ids_file_output.split(search_text1, 1)[1]
            device_vendor_name = rest_of_the_ids_file_output.split("\n", 1)[0]
            if search_text2 in ids_file_output:
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


import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')
gi.require_version('Gio', '2.0')
gi.require_version('GObject', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, Gio, GObject, Pango

import os
import gettext

from .Config import Config


def language_translation_support():
    """
    Configurations for language translation support.
    """

    from .Main import localedir
    if localedir == None:
        localedir = os.path.dirname(os.path.realpath(__file__)) + "/../po/locale"

    if Config.language == "system":
        application_language = os.environ.get("LANG")
    else:
        application_language = Config.language

    global _tr

    try:
        language = gettext.translation('system-monitoring-center', localedir=localedir, languages=[application_language])
        language.install()
        _tr = language.gettext
    # Prevent errors if there are problems with language installations on the system.
    except Exception:
        def _tr(text_for_translation):
            return text_for_translation

    Config._tr = _tr


def save_tab_settings(TabObject):
    """
    Save settings of the current tab.
    """

    TabObject.initial_func()
    TabObject.loop_func()
    Config.config_save_func()


def update_tab_and_menu_gui(MenuObject, TabObject):
    """
    Update current tab GUI and menu of the current tab.
    """

    TabObject.initial_func()
    TabObject.loop_func()

    try:
        MenuObject.disconnect_signals()
        MenuObject.set_gui()
        MenuObject.connect_signals()
    # Prevent errors if current tab menu does not have functions for
    # setting GUI, disconnecting and connecting signals.
    except AttributeError:
        pass


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
    label.set_ellipsize(Pango.EllipsizeMode.END)
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


def graph_color_button(TabMenuObject):
    """
    Generate "Graph Color" button for menus.
    """

    button = Gtk.Button()
    button.set_label(_tr("Graph Color"))
    button.set_halign(Gtk.Align.CENTER)

    button.connect("clicked", on_graph_color_button_clicked, TabMenuObject)

    return button


def on_graph_color_button_clicked(widget, TabMenuObject):
    """
    Change graph foreground color.
    Also get current foreground color of the graph and set it as selected color of the dialog.
    """

    # Generate a ColorChooserDialog
    main_window = widget.get_root()
    if 'colorchooserdialog' not in globals():
        global colorchooserdialog
        colorchooserdialog = Gtk.ColorChooserDialog().new(title=_tr("Graph Color"), parent=main_window)
        colorchooserdialog.set_modal(True)
    # Disconnect and connect ColorChooserDialog response signal to pass current tab object every time.
    try:
        colorchooserdialog.disconnect_by_func(on_colorchooserdialog_response)
    except TypeError:
        pass
    colorchooserdialog.connect("response", on_colorchooserdialog_response, TabMenuObject)

    # Get graph color of the tab
    if TabMenuObject.name == "CpuMenu":
        tab_graph_color = Config.chart_line_color_cpu_percent
    elif TabMenuObject.name == "MemoryMenu":
        tab_graph_color = Config.chart_line_color_memory_percent
    elif TabMenuObject.name == "DiskMenu":
        tab_graph_color = Config.chart_line_color_disk_speed_usage
    elif TabMenuObject.name == "NetworkMenu":
        tab_graph_color = Config.chart_line_color_network_speed_data
    elif TabMenuObject.name == "GpuMenu":
        tab_graph_color = Config.chart_line_color_fps

    # Set selected color on the ColorChooserDialog
    color = Gdk.RGBA()
    color.red, color.green, color.blue, color.alpha = tab_graph_color
    colorchooserdialog.set_rgba(color)

    # Show the ColorChooserDialog
    TabMenuObject.menu_po.popdown()
    colorchooserdialog.present()


def on_colorchooserdialog_response(widget, response, TabMenuObject):
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
        if TabMenuObject.name == "CpuMenu":
            Config.chart_line_color_cpu_percent = tab_graph_color
            from .Cpu import Cpu
            Cpu.initial_func()
            Cpu.loop_func()
        elif TabMenuObject.name == "MemoryMenu":
            Config.chart_line_color_memory_percent = tab_graph_color
            from .Memory import Memory
            Memory.initial_func()
            Memory.loop_func()
        elif TabMenuObject.name == "DiskMenu":
            Config.chart_line_color_disk_speed_usage = tab_graph_color
            from .Disk import Disk
            Disk.initial_func()
            Disk.loop_func()
        elif TabMenuObject.name == "NetworkMenu":
            Config.chart_line_color_network_speed_data = tab_graph_color
            from .Network import Network
            Network.initial_func()
            Network.loop_func()
        elif TabMenuObject.name == "GpuMenu":
            Config.chart_line_color_fps = tab_graph_color
            from .Gpu import Gpu
            Gpu.initial_func()
            Gpu.loop_func()
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
        from .Performance import Performance
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
    Define action and accelerator for focus of SearchEntry widgets. They will be called if "Ctrl+F" buttons are pressed.
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


def searchentry_update_placeholder_text(TabObject, row_type):
    """
    Update placeholder text (row count) on SearchEntry.
    """

    searchentry = TabObject.searchentry
    tab_data_rows = TabObject.tab_data_rows

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


def treeview_add_remove_columns(TabObject):
    """
    Add/Remove treeview columns appropriate for user preferences.
    Remove all columns, redefine treestore and models, set treestore data types (str, int, etc) if
    column numbers are changed. Because once treestore data types (str, int, etc) are defined, they
    can not be changed anymore. Thus column (internal data) order and column treeview column addition/removal
    can not be performed.
    """

    treeview = TabObject.treeview
    row_data_list = TabObject.row_data_list
    treeview_columns_shown_prev = TabObject.treeview_columns_shown_prev

    # Get treeview columns shown
    if TabObject.name == "Sensors":
        treeview_columns_shown = Config.sensors_treeview_columns_shown
    elif TabObject.name == "Processes":
        treeview_columns_shown = Config.processes_treeview_columns_shown
    elif TabObject.name == "Users":
        treeview_columns_shown = Config.users_treeview_columns_shown
    elif TabObject.name == "Services":
        treeview_columns_shown = Config.services_treeview_columns_shown

    # Add/Remove treeview columns if they are changed since the last loop.
    reset_row_unique_data_list_prev = "no"
    if treeview_columns_shown != treeview_columns_shown_prev:
        cumulative_sort_column_id = -1
        cumulative_internal_data_id = -1
        # Remove all treeview columns
        for column in treeview.get_columns():
            treeview.remove_column(column)
        # Append columns
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
            treeview_column.set_resizable(True)
            treeview_column.set_reorderable(True)
            treeview_column.set_min_width(50)                                       # Set minimum column widths as "50 pixels" which is useful for realizing the minimized column. Otherwise column title will be invisible.
            treeview_column.connect("clicked", on_column_title_clicked, TabObject)
            treeview_column.connect("notify::width", treeview_column_order_width_row_sorting, TabObject)
            treeview.append_column(treeview_column)

        # Get column data types (int, bool, float, str, etc.) for appending row data to treestore
        data_column_types = []
        for column in sorted(treeview_columns_shown):
            internal_column_count = len(row_data_list[column][5])
            for internal_column_number in range(internal_column_count):
                data_column_types.append(row_data_list[column][5][internal_column_number])

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


def get_sort_column_id_column_dict(row_data_list, treeview_columns_shown):
    """
    Get sort column ID - column dictionary of treeview columns.
    """

    sort_column_id_column_dict = {}
    cumulative_sort_column_id = -1
    for column in treeview_columns_shown:
        if row_data_list[column][0] in treeview_columns_shown:
            cumulative_sort_column_id = cumulative_sort_column_id + row_data_list[column][2]
            sort_column_id_column_dict[column] = cumulative_sort_column_id

    return sort_column_id_column_dict


def get_sort_column_id_list(treeview_columns):
    """
    Get sort column ID list of TreeView columns.
    """

    sort_column_id_list = []
    for column in treeview_columns:
        sort_column_id_list.append(column.get_sort_column_id())

    return sort_column_id_list


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


def update_treestore_rows(TabObject, rows_data_dict, deleted_rows, new_rows, updated_existing_row_index, row_id_list, row_id_list_prev, show_rows_as_tree=0, show_all_rows=1):
    """
    Add/Remove/Update treestore rows.
    """

    treestore = TabObject.treestore
    piter_list = TabObject.piter_list
    searchentry = TabObject.searchentry
    on_searchentry_changed = TabObject.on_searchentry_changed
    tab_data_rows = TabObject.tab_data_rows
    tab_data_rows_prev = TabObject.tab_data_rows_prev

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
                    if show_all_rows == 1:                                      # Row appended under tree root row or another row if "Show [ROWS] as tree" option is preferred.
                        piter_list.append(treestore.append(piter_list[row_id_list.index(parent_row)], tab_data_rows[pid_index]))
                    if show_all_rows == 0 and parent_row not in row_id_list:    # Row is appended into treeview as tree root row if "Show [ROWS] of all users" is not preferred and row ppid not in row_id_list.
                        piter_list.append(treestore.append(None, tab_data_rows[pid_index]))
                    if show_all_rows == 0 and parent_row in row_id_list:        # Row is appended into treeview under tree root row or another row if "Show [ROWS] of all users" is preferred and row ppid is in row_id_list.
                        piter_list.append(treestore.append(piter_list[row_id_list.index(parent_row)], tab_data_rows[pid_index]))
            else:                                                                             # All rows are appended into treeview as tree root row if "Show [ROWS] as tree" is not preferred. Thus rows are listed as list structure instead of tree structure.
                piter_list.insert(pid_index, treestore.insert(None, pid_index, tab_data_rows[pid_index]))
        # Update search results
        on_searchentry_changed(searchentry)


def treeview_reorder_columns_sort_rows_set_column_widths(TabObject):
    """
    Reorder TreeView columns, sort TreeView rows and set TreeView columns.
    """

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
        treeview_columns = treeview.get_columns()
        sort_column_id_column_dict = get_sort_column_id_column_dict(row_data_list, treeview_columns_shown)
        sort_column_id_list = get_sort_column_id_list(treeview_columns)
        data_column_order_scratch = []
        for column_order in data_column_order:
            if column_order != -1:
                data_column_order_scratch.append(column_order)
        # Reorder treeview columns by moving the last unsorted column at the beginning of the treeview.
        for order in reversed(sorted(data_column_order_scratch)):
            if data_column_order.index(order) in treeview_columns_shown:
                column_number_to_move = data_column_order.index(order)
                column_id_to_move = sort_column_id_column_dict[column_number_to_move]
                column_to_move = treeview_columns[sort_column_id_list.index(column_id_to_move)]
                # Column is moved at the beginning of the treeview if "None" is used.
                treeview.move_column_after(column_to_move, None)

    # Sort rows if user has changed row sorting column and sorting order (ascending/descending) by clicking
    # on any column title button on the GUI.
    # Reorder columns/sort rows if column ordering/row sorting has been changed since last loop in order to avoid
    # reordering/sorting in every loop.
    if treeview_columns_shown_prev != treeview_columns_shown or \
       data_row_sorting_column_prev != data_row_sorting_column or \
       data_row_sorting_order != data_row_sorting_order_prev:
        sort_column_id_column_dict = get_sort_column_id_column_dict(row_data_list, treeview_columns_shown)
        treeview_columns = treeview.get_columns()
        sort_column_id_list = get_sort_column_id_list(treeview_columns)
        if data_row_sorting_column in treeview_columns_shown:
            data_row_sorting_column_id = sort_column_id_column_dict[data_row_sorting_column]
        else:
            data_row_sorting_column_id = row_data_list[0][2]
        column_for_sorting = treeview_columns[sort_column_id_list.index(data_row_sorting_column_id)]
        # Set row sorting
        for i in range(4):
            column_for_sorting.clicked()
            if data_row_sorting_order == int(column_for_sorting.get_sort_order()):
                break

    # Set column widths if there are changes since last loop.
    if treeview_columns_shown_prev != treeview_columns_shown or data_column_widths_prev != data_column_widths:
        sort_column_id_column_dict = get_sort_column_id_column_dict(row_data_list, treeview_columns_shown)
        treeview_columns = treeview.get_columns()
        sort_column_id_list = get_sort_column_id_list(treeview_columns)
        for row_data in row_data_list:
            column_id = row_data[0]
            for j, sort_column_id in enumerate(sort_column_id_list):
                if column_id not in sort_column_id_column_dict:
                    continue
                if sort_column_id == sort_column_id_column_dict[column_id]:
                    column_width = data_column_widths[column_id]
                    # Set column width in pixels. Fixed width is unset if value is "-1".
                    treeview_columns[j].set_fixed_width(column_width)


def treeview_column_order_width_row_sorting(widget, parameter, TabObject):
    """
    Get and save column order/width, row sorting.
    Columns in the treeview are get one by one and appended into "data_column_order".
    "data_column_widths" list elements are modified for widths of every columns in the treeview.
    Length of these list are always same even if columns are removed, appended and column widths are changed.
    Only values of the elements (element indexes are always same with "row_data_list") are changed if column order/widths are changed.
    """

    treeview = TabObject.treeview
    row_data_list = TabObject.row_data_list
    treeview_columns_shown = TabObject.treeview_columns_shown

    # Get previous column order and widths
    if TabObject.name == "Sensors":
        data_column_order_prev = Config.sensors_data_column_order
        data_column_widths_prev = Config.sensors_data_column_widths
    elif TabObject.name == "Processes":
        data_column_order_prev = Config.processes_data_column_order
        data_column_widths_prev = Config.processes_data_column_widths
    elif TabObject.name == "Users":
        data_column_order_prev = Config.users_data_column_order
        data_column_widths_prev = Config.users_data_column_widths
    elif TabObject.name == "Services":
        data_column_order_prev = Config.services_data_column_order
        data_column_widths_prev = Config.services_data_column_widths

    sort_column_id_column_dict = get_sort_column_id_column_dict(row_data_list, treeview_columns_shown)

    # Get new column order and widths
    treeview_columns = treeview.get_columns()
    sort_column_id_list = get_sort_column_id_list(treeview_columns)

    data_column_order = [-1] * len(row_data_list)
    data_column_widths = [-1] * len(row_data_list)

    treeview_columns_last_index = len(treeview_columns)-1

    for row_data in row_data_list:
        column_id = row_data[0]
        for j, sort_column_id in enumerate(sort_column_id_list):
            if column_id not in sort_column_id_column_dict:
                continue
            if sort_column_id == sort_column_id_column_dict[column_id]:
                data_column_order[column_id] = j
                if j != treeview_columns_last_index:
                    data_column_widths[column_id] = treeview_columns[j].get_width()

    # Prevent saving settings if column order and widths are not changed.
    if data_column_order == data_column_order_prev and data_column_widths == data_column_widths_prev:
        return

    # Save new column order and widths
    if TabObject.name == "Processes":
        Config.processes_data_column_order = list(data_column_order)
        Config.processes_data_column_widths = list(data_column_widths)
    elif TabObject.name == "Users":
        Config.users_data_column_order = list(data_column_order)
        Config.users_data_column_widths = list(data_column_widths)
    elif TabObject.name == "Services":
        Config.services_data_column_order = list(data_column_order)
        Config.services_data_column_widths = list(data_column_widths)
    Config.config_save_func()


def on_column_title_clicked(widget, TabObject):
    """
    Get and save column sorting order.
    """

    treeview = TabObject.treeview
    row_data_list = TabObject.row_data_list
    treeview_columns_shown = TabObject.treeview_columns_shown
    data_row_sorting_column = TabObject.data_row_sorting_column

    sort_column_id_column_dict = get_sort_column_id_column_dict(row_data_list, treeview_columns_shown)
    treeview_columns = treeview.get_columns()
    sort_column_id_list = get_sort_column_id_list(treeview_columns)

    # Get column that is used for sorting
    data_row_sorting_column_id = widget.get_sort_column_id()
    for column in sort_column_id_column_dict.keys():
        if sort_column_id_column_dict[column] == data_row_sorting_column_id:
            data_row_sorting_column = column
            break

    # Convert Gtk.SortType (for example: <enum GTK_SORT_ASCENDING of type Gtk.SortType>) to integer (0: ascending, 1: descending)
    data_row_sorting_order = int(widget.get_sort_order())

    # Save new column order and widths
    if TabObject.name == "Processes":
        Config.processes_data_row_sorting_column = data_row_sorting_column
        Config.processes_data_row_sorting_order = data_row_sorting_order
    elif TabObject.name == "Users":
        Config.users_data_row_sorting_column = data_row_sorting_column
        Config.users_data_row_sorting_order = data_row_sorting_order
    elif TabObject.name == "Services":
        Config.services_data_row_sorting_column = data_row_sorting_column
        Config.services_data_row_sorting_order = data_row_sorting_order
    Config.config_save_func()


def on_columns_changed(widget, TabObject):
    """
    Called if number of columns changed.
    """

    treeview = TabObject.treeview

    # Get treeview columns shown
    if TabObject.name == "Sensors":
        treeview_columns_shown = Config.sensors_treeview_columns_shown
    elif TabObject.name == "Processes":
        treeview_columns_shown = Config.processes_treeview_columns_shown
    elif TabObject.name == "Users":
        treeview_columns_shown = Config.users_treeview_columns_shown
    elif TabObject.name == "Services":
        treeview_columns_shown = Config.services_treeview_columns_shown

    treeview_columns = treeview.get_columns()
    if len(treeview_columns_shown) != len(treeview_columns):
        return
    if treeview_columns[0].get_width() == 0:
        return
    treeview_column_order_width_row_sorting(widget, None, TabObject)


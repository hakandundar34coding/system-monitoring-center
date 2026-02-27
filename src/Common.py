import tkinter as tk
from tkinter import ttk
import tkinter.font

import os
import locale

from .Config import Config
from .Performance import Performance

_tr = Config._tr


def get_system_font():
    """
    Get system font and modified fonts.
    """

    global font_system, font_normal, font_bold_2x, font_bold_underlined, font_bold, font_underlined, font_small

    # Get system font
    font_system = tkinter.font.nametofont("TkDefaultFont")
    #font_system = tkinter.font.Font(family="Cantarell", size=11)
    #font_system_config = font_system.config()
    font_system_config = font_system.actual()
    font_system_family = font_system_config["family"]
    font_system_size = font_system_config["size"]
    font_system_weight = font_system_config["weight"]
    font_system_slant = font_system_config["slant"]
    font_system_underline = font_system_config["underline"]
    font_system_overstrike = font_system_config["overstrike"]

    font_scale = Config.font_scale

    # Get modified fonts
    font_normal = tkinter.font.Font(family=font_system_family, size=int(font_scale*font_system_size), weight=font_system_weight, slant=font_system_slant, underline=font_system_underline, overstrike=font_system_overstrike)
    font_bold_2x = tkinter.font.Font(family=font_system_family, size=int(font_scale*2*font_system_size), weight="bold", slant=font_system_slant, underline=font_system_underline, overstrike=font_system_overstrike)
    font_bold = tkinter.font.Font(family=font_system_family, size=int(font_scale*font_system_size), weight="bold", slant=font_system_slant, underline=font_system_underline, overstrike=font_system_overstrike)
    font_bold_underlined = tkinter.font.Font(family=font_system_family, size=int(font_scale*font_system_size), weight="bold", slant=font_system_slant, underline=1, overstrike=font_system_overstrike)
    font_underlined = tkinter.font.Font(family=font_system_family, size=int(font_scale*font_system_size), weight=font_system_weight, slant=font_system_slant, underline=1, overstrike=font_system_overstrike)
    font_small = tkinter.font.Font(family=font_system_family, size=int(font_scale*0.9*font_system_size), weight=font_system_weight, slant=font_system_slant, underline=font_system_underline, overstrike=font_system_overstrike)


def separate_thread(function, widget):
    """
    Run functions in a separate thread and show the result on the GUI.
    """

    import threading, queue

    # Generate queue for getting result
    queue = queue.Queue()
    check_if_finished(queue, widget)

    # Generate and start thread
    threading.Thread(target=function, args=(queue,), daemon=True).start()


def check_if_finished(_queue, widget):
    """
    Check the queue if there is a result.
    Get the result if the thread is finished or rerun the check function if the thread is not finished.
    """

    import queue
    try:
        result = _queue.get_nowait()
        widget.config(text=result)
    except queue.Empty:
        widget.after(100, check_if_finished, _queue, widget)


def main_tab_togglebutton(container, text, image_name, variable, value):
    """
    Generate main tab ToggleButton and its widgets.
    """

    # Image
    _image = tk.PhotoImage(file=image_name)
    _image = _image.subsample(2, 2)

    # ToggleButton
    _togglebutton = ttk.Radiobutton(container, image=_image, compound="top", text=text, style="Toggle.TButton", variable=variable, value=value)
    _togglebutton.image = _image

    if "font_system" not in globals():
        get_system_font()

    style = ttk.Style(container.winfo_toplevel())
    style.configure("Toggle.TButton", font=font_bold)
    #style.map("Toggle1.TButton", foreground=[('selected', 'cyan')])

    return _togglebutton


def sub_tab_togglebutton(container, text, image_name, variable, value):
    """
    Generate Performance tab sub-tab ToggleButton and its widgets.
    """

    # Image
    _image = tk.PhotoImage(file=image_name)
    _image = _image.subsample(2, 2)

    # ToggleButton
    _togglebutton = ttk.Radiobutton(container, image=_image, compound="left", text=text, style="Toggle_sub.TButton", variable=variable, value=value)
    _togglebutton.image = _image

    if "font_system" not in globals():
        get_system_font()

    style = ttk.Style(container.winfo_toplevel())
    style.configure("Toggle_sub.TButton", anchor="w", font=font_bold)
    style.map("Toggle_sub.TButton", foreground=[('selected', 'cyan')])

    return _togglebutton


def tab_main_frame(container):
    """
    Generate tab main frame.
    """

    _frame = ttk.Frame(container)
    _frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
    _frame.columnconfigure(0, weight=1)
    _frame.rowconfigure(0, weight=1)

    return _frame


def tab_title_label(container, text):
    """
    Generate tab title Label.
    """

    if "font_system" not in globals():
        get_system_font()

    _label = ttk.Label(container, text=text, font=font_bold_2x)
    _label.grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, 60), pady=0)

    return _label


def device_vendor_model_label(container):
    """
    Generate device vendor model information Label.
    """

    if "font_system" not in globals():
        get_system_font()

    _label = ttk.Label(container, text="--", font=font_bold)
    _label.grid(row=0, column=1, sticky="nw")

    return _label


def device_kernel_name_label(container):
    """
    Generate device kernel name information Label.
    """

    if "font_system" not in globals():
        get_system_font()

    _label = ttk.Label(container, text="--", font=font_normal)
    _label.grid(row=1, column=1, sticky="nw")

    return _label


def da_upper_lower_label(container, text):
    """
    Generate Label above or below DrawingArea.
    """

    if "font_system" not in globals():
        get_system_font()

    _label = ttk.Label(container, text=text, font=font_normal, foreground="gray")

    return _label


def static_information_label(container, text):
    """
    Generate static information Label. This label is not updated.
    """

    if "font_system" not in globals():
        get_system_font()

    _label = ttk.Label(container, text=text, font=font_normal, anchor='w')

    return _label


def dynamic_information_label(container):
    """
    Generate dynamic information Label. This label is updated by the code.
    """

    if "font_system" not in globals():
        get_system_font()

    _label = ttk.Label(container, text="--", font=font_bold)

    return _label


def dynamic_information_label_wrap(container):
    """
    Generate dynamic information Label. This label is updated by the code.
    """

    if "font_system" not in globals():
        get_system_font()

    _label = ttk.Label(container, text="--", font=font_bold, wraplength=400)

    return _label


def bold_label(container, text):
    """
    Generate bold Label.
    """

    if "font_system" not in globals():
        get_system_font()

    _label = ttk.Label(container, text=text, font=font_bold)

    return _label


def link_label(container, text, link):
    """
    Generate link Label.
    """

    if "font_system" not in globals():
        get_system_font()

    import webbrowser

    _label = ttk.Label(container, text=text, font=font_underlined, foreground="blue", cursor="hand2")
    _label.bind("<ButtonRelease-1>", lambda e:webbrowser.open_new(link))
    _tooltip = tooltip(_label, link)

    return _label


def clickable_label(container, function):
    """
    Generate clickable Label. Mouse cursor is changed when mouse hover action is performed.
    """

    if "font_system" not in globals():
        get_system_font()

    _label = ttk.Label(container, text=_tr("Show..."), font=font_bold_underlined, cursor="hand2")
    _label.bind("<ButtonRelease-1>", function)

    return _label


def headerbar_label(container, text):
    """
    Generate Label for window HeaderBar.
    """

    if "font_system" not in globals():
        get_system_font()

    _label = ttk.Label(container, text=text, font=font_small)

    return _label


def styled_information_scrolledwindow(container, text1, tooltip1, text2, tooltip2):
    """
    Generate styled information Frame (labels, separators on it).
    """

    # Frame (text1 and text2)
    _frame = ttk.Frame(container, style='Card.TFrame', padding=(6, 6, 6, 6))
    _frame.columnconfigure((0, 1), weight=1, uniform="equal")

    # Label (text1)
    _label = static_information_label(_frame, text1)
    _label.grid(row=0, column=0, padx=0, pady=(3, 0))

    # Tooltip (text1)
    if tooltip1 != None:
        _tooltip = tooltip(_label, tooltip1)

    # Label (text2)
    _label = static_information_label(_frame, text2)
    _label.grid(row=0, column=1, padx=0, pady=(3, 0))

    # Tooltip (text2)
    if tooltip2 != None:
        _tooltip = tooltip(_label, tooltip2)

    """_frame_for_separator = ttk.Frame(_frame, width=30, height=5)
    _frame_for_separator.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
    _frame_for_separator.columnconfigure(0, weight=1)"""

    # Separator (text1)
    _separator = ttk.Separator(_frame, orient="horizontal")
    _separator.grid(row=1, column=0, sticky="ew", padx=30, pady=2)

    # Separator (text2)
    _separator = ttk.Separator(_frame, orient="horizontal")
    _separator.grid(row=1, column=1, sticky="ew", padx=30, pady=2)

    # Label (text1)
    label1 = dynamic_information_label(_frame)
    label1.grid(row=2, column=0)

    # Label (text1)
    label2 = dynamic_information_label(_frame)
    label2.grid(row=2, column=1)

    return _frame, label1, label2


def window(parent_window, window_title):
    """
    Generate window and add frame.
    """

    window = tk.Toplevel(parent_window)
    # Keep the window on top of the main window
    window.wm_transient(parent_window)
    # Prevent usage of the main window
    try:
        window.grab_set()
    except tk.TclError:
        # Wait until window is shown. Otherwise it gives error if grab_set is used for windows that opened with double click.
        window.wait_visibility()
        window.grab_set()
    #window.resizable(False, False)
    window.title(window_title)
    window.minsize(300, 300)
    #self.disk_details_window.maxsize(300, 300)

    # Frame (Main)
    main_frame = ttk.Frame(window, style="Card.TFrame")
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    frame = ttk.Frame(main_frame)
    frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    return window, frame


def tooltip(widget, text):
    """
    Generate a tooltip for widgets.
    "overrideredirect" is used for hiding window decorations.
    "wraplength" is used for splitting long texts into multiple lines.
    "justify" is used for aligning the text if it is splitted.
    "background", "borderwidth" and "padx, pady" are used for showing a different colored border around the tooltip.
    """

    def on_enter(event):

        global _tooltip
        _tooltip = tk.Toplevel(background="gray")
        _tooltip.overrideredirect(True)
        _tooltip.geometry("+" + str(event.x_root+15) + "+" + str(event.y_root+10))

        _tooltip.bind('<ButtonPress>', destroy_tooltip)

        label = tk.Label(_tooltip, text=text, font=font_normal, borderwidth=8, wraplength=400, justify="left")
        label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)

    def destroy_tooltip(event):

        global _tooltip
        try:
            _tooltip.destroy()
        except (AttributeError, NameError):
            pass
        _tooltip = None

    if text != "":
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', destroy_tooltip)
        widget.bind("<ButtonPress>", destroy_tooltip)
        widget.bind("<Key>", destroy_tooltip)


def drawingarea(container, widget_name):
    """
    Generate drawingarea and connect signals.
    """

    _drawingarea = ttk.Label(container)
    _drawingarea.bind('<Enter>', lambda event: Performance.performance_line_charts_enter_notify_event(event, widget_name))
    _drawingarea.bind('<Leave>', lambda event: Performance.performance_line_charts_leave_notify_event(event, widget_name))
    _drawingarea.bind("<Motion>", lambda event: Performance.performance_line_charts_motion_notify_event(event, widget_name))

    return _drawingarea


def radiobutton(container, text, variable, value, command):

    _radiobutton = ttk.Radiobutton(container, text=text, variable=variable, value=value, command=command)

    style = ttk.Style()
    style.configure("TRadiobutton", font=font_normal)

    return _radiobutton


def checkbutton(container, text, variable, command):

    _checkbutton = ttk.Checkbutton(container, text=text, variable=variable, command=command)

    style = ttk.Style()
    style.configure("TCheckbutton", font=font_normal)

    return _checkbutton


def combobox(container):

    _combobox = ttk.Combobox(container, stat="readonly", font=font_normal)

    return _combobox


def button(container, text, command):

    _button = ttk.Button(container, text=text, command=command)

    style = ttk.Style()
    style.configure("TButton", font=font_normal)

    return _button


def refresh_button(container, image_name):

    _image = tk.PhotoImage(file=image_name)
    _image = _image.subsample(3, 3)
    _button = ttk.Button(container, image=_image)
    _button.image = _image
    _tooltip = tooltip(_button, _tr("Refresh the data on this tab"))

    return _button


def popover_update_position(menu_po, MainWindow):
    """
    Update Popover position fot matching it MenuButton after its GUI is generated.
    """

    # Get menubutton coordinates for using them for popover coordinates.
    menubutton_position_x = MainWindow.tab_menu_menubutton.winfo_rootx()
    menubutton_position_y = MainWindow.tab_menu_menubutton.winfo_rooty()
    menubutton_width = MainWindow.tab_menu_menubutton.winfo_width()
    menubutton_heigh = MainWindow.tab_menu_menubutton.winfo_height()

    popover_position_x = int(menubutton_position_x + menubutton_width / 2)
    popover_position_y = int(menubutton_position_y + menubutton_heigh + 5)

    # Update popover position by using its width.
    menu_po.update()
    menu_po_width = menu_po.winfo_width()
    menu_po_heigh = menu_po.winfo_height()
    popover_position_x = int(menubutton_position_x + menubutton_width / 2 - menu_po_width / 2)
    popover_position_y = int(menubutton_position_y + menubutton_heigh + 5)
    menu_po.geometry("+" + str(popover_position_x) + "+" + str(popover_position_y))


def save_tab_settings(TabObject):
    """
    Save settings of the current tab.
    """

    TabObject.initial_func()
    TabObject.loop_func()
    Config.config_save_func()


def update_tab_and_menu_gui(func, TabObject):
    """
    Update current tab GUI and menu of the current tab.
    """

    TabObject.initial_func()
    TabObject.loop_func()
    func()


def searchentry(container, TabObject):
    """
    Generate searchentry by using an Entry and define its variable for text changed event.
    """

    # Text variable of Entry
    _text_variable = tk.StringVar()
    _text_variable.trace_add("write", lambda name, index, mode, _text_variable=_text_variable: on_searchentry_changed(_text_variable, TabObject))

    # Entry
    _searchentry = ttk.Entry(container, textvariable=_text_variable, font=font_normal)
    _searchentry.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    _searchentry.delete(0, "end")
    #_searchentry.insert(0, " " + _tr("Search...") + " ")

    _searchentry.bind("<FocusIn>", lambda event: on_searchentry_focus_in(event, TabObject))
    _searchentry.bind("<FocusOut>", lambda event: on_searchentry_focus_out(event, TabObject))

    return _searchentry, _text_variable


def searchentry_focus(event):
    """
    Focus tab Eearchentry.
    """

    if Config.current_main_tab == 0:
        if Config.performance_tab_current_sub_tab == 6:
            from .Sensors import Sensors
            Sensors.searchentry.focus_set()
    elif Config.current_main_tab == 1:
        from .Processes import Processes
        Processes.searchentry.focus_set()
    elif Config.current_main_tab == 2:
        from .Users import Users
        Users.searchentry.focus_set()
    elif Config.current_main_tab == 3:
        from .Services import Services
        Services.searchentry.focus_set()


def on_searchentry_focus_in(event, TabObject):
    """
    Clear placeholder text if searchentry is focused in and placeholder text is in it.
    """

    # Get search text
    searchentry = TabObject.searchentry
    searchentry_text_var = TabObject.searchentry_text_var
    row_count = TabObject.row_count
    row_information = TabObject.row_information

    search_text = searchentry_text_var.get()
    placeholder_text = _tr("Search...") + "                    " + "(" + row_information + ": " + str(row_count) + ")"

    # Clear placeholder text if SearchEntry is clicked.
    if search_text == placeholder_text:
        searchentry.delete(0, "end")
    if search_text == "":
        searchentry.delete(0, "end")
    if search_text.startswith(_tr("Search...") + "                    " + "("):
        searchentry.delete(0, "end")


def on_searchentry_focus_out(event, TabObject):
    """
    Call searchentry placeholder text function for setting placeholder text without waiting tab loop funciton.
    """

    searchentry_placeholder_text(TabObject)


def on_searchentry_changed(searchentry_text_var, TabObject):
    """
    Called by searchentry when its text is changed.
    """

    searchentry = TabObject.searchentry
    searchentry_text_var = TabObject.searchentry_text_var
    row_count = TabObject.row_count
    row_information = TabObject.row_information

    search_text = searchentry_text_var.get()
    placeholder_text = _tr("Search...") + "                    " + "(" + row_information + ": " + str(row_count) + ")"

    """if search_text == "":
        return"""

    # Clear placeholder text if SearchEntry is clicked.
    if search_text.split("(")[0] == placeholder_text.split("(")[0]:
        return

    # Get search text
    search_text = searchentry_text_var.get().lower()

    treeview = TabObject.treeview
    selected_data_rows = TabObject.selected_data_rows
    piter_dict = TabObject.piter_dict

    # Detach all rows
    row_id_row_dict = {}
    for row in treeview.get_children():
        treeview.detach(row)

    # Search in names if current tab is not Processes tab.
    if TabObject.name != "Processes":
        # Reattach rows that contains search text
        for row in selected_data_rows:
            data_row_dict = selected_data_rows[row]
            if search_text in data_row_dict[0].lower():
                try:
                    treeview.reattach(piter_dict[row], "", "end")
                except KeyError:
                    pass

    # Do not run rest of the function if selected tab is not Processes tab.
    if TabObject.name != "Processes":
        sort_columns_on_every_loop(TabObject)
        return

    ppid_list = TabObject.ppid_list
    pid_list = TabObject.pid_list
    cmdline_list = TabObject.cmdline_list

    # Reattach rows that contains search text
    filtered_rows = {}
    for row in selected_data_rows:
        data_row_dict = selected_data_rows[row]
        pid = data_row_dict[Config.processes_columns_shown.index("pid")]
        pid_index = pid_list.index(pid)
        command_line = cmdline_list[pid_index]
        if TabObject.process_search_type == "all":
            if search_text in data_row_dict[0].lower() or search_text in command_line.lower() or search_text in str(pid):
                filtered_rows[row] = piter_dict[row]
                try:
                    treeview.reattach(piter_dict[row], "", "end")
                except KeyError:
                    pass
        if TabObject.process_search_type == "name":
            if search_text in data_row_dict[0].lower():
                filtered_rows[row] = piter_dict[row]
                try:
                    treeview.reattach(piter_dict[row], "", "end")
                except (KeyError, tk.TclError) as me:
                    pass
        if TabObject.process_search_type == "command_line":
            if search_text in command_line.lower():
                filtered_rows[row] = piter_dict[row]
                try:
                    treeview.reattach(piter_dict[row], "", "end")
                # tk.TclError is for preventing errors if computer is opened after suspend.
                except (KeyError, tk.TclError) as me:
                    pass
        if TabObject.process_search_type == "pid":
            if search_text in str(pid):
                filtered_rows[row] = piter_dict[row]
                try:
                    treeview.reattach(piter_dict[row], "", "end")
                # tk.TclError is for preventing errors if computer is opened after suspend.
                except (KeyError, tk.TclError) as me:
                    pass

    # Move rows to generate Treeview tree
    show_as_tree = TabObject.show_processes_as_tree
    if show_as_tree == 1:
        for row in list(filtered_rows.keys()):
            pid = row
            while pid != "0":
                piter = piter_dict[str(pid)]
                ppid = ppid_list[pid_list.index(int(pid))]
                if ppid != 0:
                    parent_piter = piter_dict[str(ppid)]
                if ppid == 0:
                    parent_piter = ""
                if pid not in filtered_rows:
                    filtered_rows[pid] = piter
                    treeview.reattach(piter, "", "end")
                #treeview.move(piter, parent_piter, 0)
                pid = str(ppid)

        for row_id, piter in piter_dict.items():
            if row_id in filtered_rows:
                try:
                    ppid = ppid_list[pid_list.index(int(row_id))]
                    parent_id = str(ppid)
                    if parent_id in filtered_rows and ppid != 0:
                        treeview.move(piter, piter_dict[parent_id], "end")
                    else:
                        treeview.move(piter, "", "end")
                # tk.TclError is for preventing errors if computer is opened after suspend.
                except (ValueError, IndexError, tk.TclError):
                    try:
                        treeview.move(piter, "", "end")
                    # For preventing errors if computer is opened after suspend.
                    except tk.TclError:
                        pass
            else:
                try:
                    treeview.detach(piter)
                except:
                    pass

    sort_columns_on_every_loop(TabObject)


def searchentry_placeholder_text(TabObject):
    """
    Show an update number of rows on the searchentry as placeholder text.
    Tkinter does not support placeholder text for Entry. Placeholder tetxt is set as Entry text.
    """

    # Get searchentry related information
    searchentry = TabObject.searchentry
    searchentry_text_var = TabObject.searchentry_text_var
    row_count = TabObject.row_count
    row_information = TabObject.row_information

    # Update searchentry placeholder text
    search_text = searchentry_text_var.get()
    placeholder_text = _tr("Search...") + "                    " + "(" + row_information + ": " + str(row_count) + ")"

    if search_text == "" and searchentry != searchentry.focus_get():
        searchentry.delete(0, "end")
        searchentry.insert(0, placeholder_text)
    if search_text == "" and searchentry == searchentry.focus_get():
        searchentry.delete(0, "end")
    """if search_text != "":
        searchentry.delete(0, "end")
        searchentry.insert(0, search_text)"""
    if search_text.split("(")[0] == placeholder_text.split("(")[0]:
        searchentry.delete(0, "end")
        searchentry.insert(0, placeholder_text)

    on_searchentry_changed(searchentry_text_var, TabObject)


def treeview(container, TabObject):
    """
    Generate treeview, vertical, horizontal scrollbars and their frame.
    """

    # Frame
    frame = ttk.Frame(container)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

    # TreeView
    treeview = ttk.Treeview(frame, selectmode="browse", padding=[-22,0,0,0])
    treeview.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    """treeview.bind('<ButtonPress>', treeview_button_press_event)
    treeview.bind('<ButtonRelease>', treeview_button_release_event)
    treeview.bind("<B1-Motion>", treeview_button1_motion_event)"""
    treeview.bind("<Button-1>", treeview_button1_press_event)
    treeview.bind("<B1-Motion>", treeview_button1_motion_event)
    treeview.bind("<ButtonRelease-1>", lambda event: treeview_button1_release_event(event, TabObject))
    treeview.bind("<Motion>", treeview_motion_event)
    treeview.bind('<Leave>', destroy_row_tooltip)
    treeview.bind('<Key>', destroy_row_tooltip)

    # Scrollbars (TreeView)
    scrollbar_vertical = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
    scrollbar_vertical.grid(row=0, column=1, sticky="ns", padx=0, pady=0)
    scrollbar_horizontal = ttk.Scrollbar(frame, orient="horizontal", command=treeview.xview)
    scrollbar_horizontal.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
    treeview.configure(yscrollcommand=scrollbar_vertical.set)
    treeview.configure(xscrollcommand=scrollbar_horizontal.set)

    # Define style for changing treeview row and title fonts.
    style = ttk.Style()
    style.configure("Treeview", font=font_normal)
    style.configure("Treeview.Heading", font=font_normal)

    return treeview, frame


def treeview_button1_press_event(event):

    treeview = event.widget
    region = treeview.identify_region(event.x, event.y)
    if region == "heading":
        column_id = treeview.identify_column(event.x)

        # Prevent dragging #0 column
        if column_id == "#0":
            return

        treeview._drag_column = column_id

        # Show window for drag and drop information
        treeview._drag_window = tk.Toplevel(treeview)
        treeview._drag_window.overrideredirect(True)

        label = tk.Label(treeview._drag_window, text=treeview.heading(column_id, "text"), bg="gray", fg="white", relief="raised", borderwidth=1, padx=5, pady=5)
        label.pack()

        treeview_button1_motion_event(event)


def treeview_button1_motion_event(event):

    # Move window when mouse is moved
    treeview = event.widget
    try:
        if treeview._drag_window:
            x = treeview.winfo_pointerx() + 10
            y = treeview.winfo_pointery() + 10
            treeview._drag_window.geometry(f"+{x}+{y}")
    # Prevent error if #0 column title is clicked first.
    except AttributeError:
        return


def treeview_button1_release_event(event, TabObject):

    treeview = event.widget
    try:
        if treeview._drag_window:
            treeview._drag_window.destroy()
            treeview._drag_window = None
    # Prevent error if #0 column title is clicked first.
    except AttributeError:
        return

    region = treeview.identify_region(event.x, event.y)
    if region == "heading" and treeview._drag_column:
        target_column = treeview.identify_column(event.x)
        if target_column != "#0" and target_column != treeview._drag_column:
            display_cols = list(treeview["displaycolumns"])
            if not display_cols or display_cols == ['#all']:
                display_cols = list(treeview["columns"])

            idx_source = int(treeview._drag_column.replace('#', '')) - 1
            idx_target = int(target_column.replace('#', '')) - 1
            col_to_move = display_cols.pop(idx_source)
            display_cols.insert(idx_target, col_to_move)
            treeview["displaycolumns"] = display_cols

            #idx_source = "#" + str(idx_source + 1)
            #idx_target = "#" + str(idx_target + 1)
            idx_source = treeview["columns"][idx_source]
            idx_target = treeview["columns"][idx_target]
            treeview.heading(idx_source, command=lambda: treeview_sort_column(treeview, idx_source, False, TabObject))
            treeview.heading(idx_target, command=lambda: treeview_sort_column(treeview, idx_target, False, TabObject))

    treeview._drag_column = None
    save_column_title_order(TabObject)


def save_column_title_order(TabObject):

    treeview = TabObject.treeview
    current_columns = list(treeview["displaycolumns"])
    if current_columns == ["#all"]:
        current_columns = list(treeview["columns"])
    current_columns.insert(0, TabObject.treeview_columns_shown[0])

    if Config.current_main_tab == 0:
        if Config.performance_tab_current_sub_tab == 6:
            Config.sensors_columns_shown = list(current_columns)
    elif Config.current_main_tab == 1:
        Config.processes_columns_shown = list(current_columns)
    elif Config.current_main_tab == 2:
        Config.users_columns_shown = list(current_columns)
    elif Config.current_main_tab == 3:
        Config.services_columns_shown = list(current_columns)

    Config.config_save_func()


def treeview_motion_event(event):
    """
    Call functions if mouse is moved.
    """

    treeview_row_tooltip(event)


def treeview_row_tooltip(event):
    """
    Generate tooltip for treeview row.
    Events for row tooltip are defined for Treeview.
    """

    global _treeview_tooltip, _previous_row

    widget = event.widget
    row = widget.identify_row(event.y)

    # Delete previous tooltip if this function is called before "_previous_row" is defined or
    # mouse arrow is above column title or empty area on treeview.
    try:
        if row != _previous_row or row == "":
            _treeview_tooltip.destroy()
            _treeview_tooltip = None
    except Exception:
        pass

    # Prevent generating a new tooltip if it is not changed (mouse arow is above the same row)
    # since the last function call.
    try:
        if _previous_row == row:
            return
    except Exception:
        pass

    _previous_row = row

    # Prevent errors if mouse arrow is above column title or empty area on treeview.
    # This is checked separately from check of tooltip destroy.
    if row == "":
        return

    # Get tooltip text (Process command line fo Processes tab and row name for the other tabs)
    """if Config.current_main_tab == 1:
        from .Processes import Processes
        selected_data_rows = Processes.selected_data_rows
        for unique_id in selected_data_rows:
            if selected_data_rows[unique_id]["piter"] == row:
                unique_id = str(unique_id)
                tool_tip_text = Processes.process_commandline_dict[unique_id]
    else:
        tool_tip_text = str(widget.item(row)["text"])"""
    tool_tip_text = str(widget.item(row)["text"])

    # Generate tooltip
    _treeview_tooltip = tk.Toplevel(background="gray")
    _treeview_tooltip.overrideredirect(True)
    _treeview_tooltip.geometry("+" + str(event.x_root+15) + "+" + str(event.y_root+10))
    _treeview_tooltip.bind('<ButtonPress>', destroy_row_tooltip)

    label = tk.Label(_treeview_tooltip, text=tool_tip_text, font=font_normal, borderwidth=8, wraplength=400, justify="left")
    label.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)


def destroy_row_tooltip(event):
    """
    Called for deleting Treeview row tooltips.
    """

    global _treeview_tooltip
    try:
        _treeview_tooltip.destroy()
        _treeview_tooltip = None
    except (tk.TclError, NameError, AttributeError) as e:
        pass


def add_columns_and_reset_rows_and_columns(TabObject):
    """
    Reset rows and columns if Treeview columns are changed.
    """

    treeview_columns_shown = TabObject.treeview_columns_shown
    treeview_columns_shown_prev = TabObject.treeview_columns_shown_prev
    treeview = TabObject.treeview

    if treeview_columns_shown != treeview_columns_shown_prev:
        for row in treeview.get_children():
            treeview.delete(row)
        #treeview["columns"] = []
        TabObject.piter_dict = {} 
        TabObject.row_id_list_prev = []

        add_treeview_columns(treeview, treeview_columns_shown, TabObject.column_dict, TabObject)


def add_treeview_columns(treeview, treeview_columns_shown, column_dict, TabObject):
    """
    Add treeview columns.
    """

    # Clear display columns in order to avoid "invalid column index" error.
    try:
        treeview.configure(displaycolumns="#all")
    except:
        pass

    treeview.configure(columns=[])

    column_id_list = []
    for i, column_shown in enumerate(treeview_columns_shown):
        if i == 0:
            column_id_list.append("#0")
        else:
            column_id_list.append(column_shown)
    # Do not add 0th column. It is added automatically.
    treeview["columns"] = column_id_list[1:]
    #treeview["displaycolumns"] = column_id_list[1:]

    for i, column_shown in enumerate(treeview_columns_shown):
        column_data = column_dict[column_shown]
        column_type = column_data["column_type"]
        column_title = column_data["column_title"]
        if column_type in [int, float]:
            column_alignment = "e"
        else:
            column_alignment = "w"
        column_id = column_id_list[i]
        if i == 0:
            width = 200
        else:
            width = 110
        treeview.column(column_id, anchor=column_alignment, width=width, stretch=False)
        treeview.heading(column_id, text=column_title, command=lambda c=column_id: treeview_sort_column(treeview, c, False, TabObject))


def get_new_removed_updated_rows(row_id_list, row_id_list_prev):
    """
    Append/Remove/Update treeview rows.
    """

    row_id_list_prev_set = set(row_id_list_prev)
    row_id_list_set = set(row_id_list)
    deleted_rows = sorted(list(row_id_list_prev_set - row_id_list_set))
    new_rows = sorted(list(row_id_list_set - row_id_list_prev_set))
    existing_rows = sorted(list(row_id_list_set.intersection(row_id_list_prev)))
    updated_existing_row_index = [[row_id_list.index(i), row_id_list_prev.index(i)] for i in existing_rows]

    return new_rows, deleted_rows, existing_rows


def add_remove_update_treeview_rows(treeview, piter_dict, selected_data_rows_prev, image_dict, selected_data_rows, data_rows_raw_dict, new_rows, deleted_rows, existing_rows, pid_list=None, ppid_list=None, show_as_tree=0):
    """
    Add, remove, update treeview rows.
    """

    # Update rows
    if len(existing_rows) > 0:
        for row in existing_rows:
            data_row_dict = selected_data_rows[row]
            data_row_dict_prev = selected_data_rows_prev[row]
            if data_row_dict != data_row_dict_prev:
                piter = piter_dict[row]
                try:
                    treeview.item(piter, image=image_dict[row], text=data_row_dict[0], values=tuple(data_row_dict[1:]), tags=data_rows_raw_dict[row][1:])
                # For preventing errors if computer is opened after suspend.
                except tk.TclError:
                    pass
    # Remove rows
    if len(deleted_rows) > 0:
        for row in deleted_rows:
            piter = piter_dict[row]
            try:
                treeview.delete(piter)
            # For preventing errors if computer is opened after suspend.
            except tk.TclError:
                pass
    # Add rows
    if len(new_rows) > 0:
        for row in new_rows:
            data_row_dict = selected_data_rows[row]
            piter = treeview.insert("", 'end', image=image_dict[row], text=data_row_dict[0], values=tuple(data_row_dict[1:]), tags=data_rows_raw_dict[row][1:], open=True)
            piter_dict[row] = piter
        # Move rows to generate Treeview tree
        if show_as_tree == 1:
            for row in piter_dict:
                piter = piter_dict[row]
                if int(row) not in pid_list:
                    continue
                ppid = ppid_list[pid_list.index(int(row))]
                # Also check if parent process is in current user processes in order to avoid errors 
                # if "show only current user processes" and "show processes as tree" options are checked at the same time.
                if ppid != 0 and str(ppid) in piter_dict:
                    parent_piter = piter_dict[str(ppid)]
                if ppid == 0:
                    parent_piter = ""
                try:
                    treeview.move(piter, parent_piter, 0)
                # Sometimes it can not insert a row as descendant of another row.
                except Exception:
                    continue
    #treeview.update()
    return piter_dict


def treeview_sort_column(treeview, column_id, reverse, TabObject):

    # Get all row data for the clicked column. Different code is used for 0th column and other columns.
    """if column_id == "#0":
        column_data = [(treeview.item(k, "text"), k) for k in treeview.get_children('')]
    else:
        column_data = [(treeview.set(k, column_id), k) for k in treeview.get_children('')]"""

    treeview_columns_shown = TabObject.treeview_columns_shown
    column_dict = TabObject.column_dict

    column_data = []
    for k in treeview.get_children(''):
        column_name_value = treeview.item(k, 'text')
        item_values = treeview.item(k, 'values')

        # -1 is for getting first column after column #0 (values #0).
        if column_id == "#0":
            column_index = 0
        else:
            if column_id in treeview_columns_shown:
                column_index = treeview_columns_shown.index(column_id)
            else:
                column_index = 0
        if column_index == 0:
            value = column_name_value
        else:
            value = item_values[column_index - 1]

        try:
            col_config = column_dict[treeview_columns_shown[column_index]]
            if col_config["converted_data"] == "yes":
                actual_value = float(treeview.item(k, 'tags')[column_index - 1])
            else:
                actual_value = str(value).lower()
        except (IndexError, KeyError):
            actual_value = 0


        column_data.append((actual_value, k))

    # Sort data depending on data type (int, float, str).
    try:
        # Sort column data for float or int
        column_data.sort(key=lambda t: float(t[0]), reverse=reverse)
    except ValueError:
        # Sort column data for string
        column_data.sort(key=lambda t: locale.strxfrm(t[0]), reverse=reverse)

    # Move rows for sorted order
    for index, (val, k) in enumerate(column_data):
        treeview.move(k, '', index)

    # Save sorting column and sorting order if one of them changed since last loop.

    save_column_order(TabObject, column_id, reverse)

    # Update command for sorting in reverse order when column title is clicked.
    try:
        treeview.heading(column_id, command=lambda: treeview_sort_column(treeview, column_id, not reverse, TabObject))
    except tk.TclError:
        # Exit if column is deleted.
        return


def save_column_order(TabObject, column_id, reverse):
    """
    Save sorting column and sorting order.
    """

    treeview_columns_shown = TabObject.treeview_columns_shown

    if column_id == "#0":
        sorting_column = treeview_columns_shown[0]
    else:
        sorting_column = column_id

    if reverse == True:
        sorting_order = 1
    if reverse == False:
        sorting_order = 0

    if Config.current_main_tab == 0:
        if Config.performance_tab_current_sub_tab == 6:
            Config.sensors_row_sorting_column = sorting_column
            Config.sensors_row_sorting_order = sorting_order
    elif Config.current_main_tab == 1:
        Config.processes_row_sorting_column = sorting_column
        Config.processes_row_sorting_order = sorting_order
    elif Config.current_main_tab == 2:
        Config.users_row_sorting_column = sorting_column
        Config.users_row_sorting_order = sorting_order
    elif Config.current_main_tab == 3:
        Config.services_row_sorting_column = sorting_column
        Config.services_row_sorting_order = sorting_order

    # Prevent saving config on every loops if there is no column or sorting change since last loop.
    if TabObject.row_sorting_column != TabObject.row_sorting_column_prev or TabObject.row_sorting_order != TabObject.row_sorting_order_prev:
        Config.config_save_func()

    # Update sort column title with arrow characters.
    column_list = TabObject.treeview["columns"]
    column_list = list(column_list) + ["#0"]

    # Clear indicator arrows from all columns.
    for column_id_to_clear in column_list:
        current_title = TabObject.treeview.heading(column_id_to_clear, "text")
        updated_title = current_title.strip("↓ ↑")
        TabObject.treeview.heading(column_id_to_clear, text=updated_title)

    if sorting_order == 0:
        column_sort_indicator = "↓"
    else:
        column_sort_indicator = "↑"

    if column_id not in TabObject.treeview["columns"]:
        column_id = "#0"
    # Add indicator arrows for sorting column.
    current_title = TabObject.treeview.heading(column_id, "text")
    updated_title = current_title.strip("↓ ↑") + "   " + column_sort_indicator
    TabObject.treeview.heading(column_id, text=updated_title)


def sort_columns_on_every_loop(TabObject):
    """
    Sütunlar her döngüde sıralanır. Sütun silinmişse hata oluşmasını engeller.
    """

    treeview = TabObject.treeview
    row_sorting_column = TabObject.row_sorting_column
    row_sorting_order = TabObject.row_sorting_order
    treeview_columns_shown = TabObject.treeview_columns_shown

    # Set first column as sorting column if sorting column is not in treeview columns.
    if row_sorting_column not in treeview_columns_shown:
        TabObject.row_sorting_column = treeview_columns_shown[0]
        row_sorting_column = TabObject.row_sorting_column

    all_column_names = list(TabObject.column_dict)
    column_index = all_column_names.index(row_sorting_column)

    if column_index == 0:
        column_id = "#0"
    else:
        column_id = row_sorting_column

    # Sort columns if sorting column is in treeview columns.
    current_columns = list(treeview["columns"]) + ["#0"]
    if column_id in current_columns:
        treeview_sort_column(treeview, column_id, row_sorting_order, TabObject)


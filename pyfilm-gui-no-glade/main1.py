#!/usr/bin/python3
#-*- coding:utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

class ListBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="{PyFilm}")
        self.set_border_width(10)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)

        proxy_label = Gtk.Label("Use Proxy", xalign=0)
        vbox.pack_start(proxy_label, True, True, 0)

        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER
        hbox.pack_start(switch, False, True, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Enable Automatic Update", xalign=0)
        check = Gtk.CheckButton()
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(check, False, True, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Date Format", xalign=0)
        combo = Gtk.ComboBoxText()
        combo.insert(0, "0", "24-hour")
        combo.insert(1, "1", "AM/PM")
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)

        listbox.add(row)

        self.link_liststore = Gtk.ListStore(str, int, str, str)
        self.link_list = [("0", 1,  "Watch Finding Dory 2016 CAM Busy Boyz mp4 - VoDLocker", "http://vodlocker.com/e87rys8iefuvhs"),
                 ("1", 2, "Watch Finding Dory 2016 CAM Busy Boyz mp4 - VoDLocker", "http://vodlocker.com/e87rys8iefuvhs" ),
                 ("2", 3, "Watch Finding Dory 2016 x264 AC3 CPG mkv - VoDLocker", "http://vodlocker.com/e87rys8iefuvhs"),
                 ("3", 4, "Watch Finding Dory 2016 CAM mp4 - VoDLocker", "http://vodlocker.com/e87rys8iefuvhs"),
                 ("4", 5, "Watch The Ellen Generes Show 2016 Finding Dory Week HDTV x264 ...", "http://vodlocker.com/e87rys8iefuvhs"),
                 ("5", 6, "Watch Jimmy Kimmel Live 2016 Game Night The Cast Finding Dory ...", "http://vodlocker.com/e87rys8iefuvhs"),
                 ("6", 7, "Watch Finding Nemo 2003 720p Blu Ray x264 YIFY mp4 - VoDLocker", "http://vodlocker.com/e87rys8iefuvhs")]

        for item in self.link_list:
            for link_ref in self.link_list:
                self.link_liststore.append(list(link_ref))

        self.treeview = Gtk.TreeView.new_with_model(self.link_list)
        for i, column_title in enumerate(["Software", "Release Year", "Programming Language"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
           
        self.link_select = self.link_liststore.get_selection()
        self.link_select.connect('changed', lambda widget, row: print(row.data))
        
        box_outer.pack_start(self.link_liststore, True, True, 0)
        self.link_liststore.show_all()

win = ListBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

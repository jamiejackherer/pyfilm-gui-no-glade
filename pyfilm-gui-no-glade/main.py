#!/usr/bin/python3
#-*- coding:utf-8 -*-


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#list of tuples for each software, containing the software name, initial release, and main programming languages used
software_list = [("0", 1,  "Watch Finding Dory 2016 CAM Busy Boyz mp4 - VoDLocker", "http://vodlocker.com/e87rys8iefuvhs"),
                 ("1", 2, "Watch Finding Dory 2016 CAM Busy Boyz mp4 - VoDLocker", "http://vodlocker.com/e87rys8iefuvhs" ),
                 ("2", 3, "Watch Finding Dory 2016 x264 AC3 CPG mkv - VoDLocker", "http://vodlocker.com/e87rys8iefuvhs"),
                 ("3", 4, "Watch Finding Dory 2016 CAM mp4 - VoDLocker", "http://vodlocker.com/e87rys8iefuvhs"),
                 ("4", 5, "Watch The Ellen Generes Show 2016 Finding Dory Week HDTV x264 ...", "http://vodlocker.com/e87rys8iefuvhs"),
                 ("5", 6, "Watch Jimmy Kimmel Live 2016 Game Night The Cast Finding Dory ...", "http://vodlocker.com/e87rys8iefuvhs"),
                 ("6", 7, "Watch Finding Nemo 2003 720p Blu Ray x264 YIFY mp4 - VoDLocker", "http://vodlocker.com/e87rys8iefuvhs")]

class TreeViewFilterWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="{PyFilm}")
        self.set_border_width(10)

        #Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.entry = Gtk.Entry()
        self.entry.set_text("Hello World")
        self.grid.attach(self.entry, 0, 0, 1, 1)
        
        #Creating the ListStore model
        self.software_liststore = Gtk.ListStore(str, int, str, str)
        for software_ref in software_list:
            self.software_liststore.append(list(software_ref))
        self.current_filter_language = None

        #Creating the filter, feeding it with the liststore model
        self.language_filter = self.software_liststore.filter_new()
        #setting the filter function, note that we're not using the
        self.language_filter.set_visible_func(self.language_filter_func)

        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        for i, column_title in enumerate(["Index", "Rank", "Title", "Link"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)
                       
        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 1, 5, 10)
        self.scrollable_treelist.add(self.treeview)

        self.select = self.treeview.get_selection()
        self.select.connect("changed", self.on_tree_selection_changed)

        #creating quit button, and setting up the event      
        self.quit_button = Gtk.Button(label = "Quit")
        self.quit_button.connect("clicked", self.on_quit_button_clicked)
        self.grid.attach(self.quit_button, 0, 2, 1, 1)

        self.show_all()

    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if self.current_filter_language is None or self.current_filter_language == "None":
            return True
        else:
            return model[iter][2] == self.current_filter_language

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        #we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        print("%s language selected!" % self.current_filter_language)
        #we update the filter, which updates in turn the view
        self.language_filter.refilter()

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter != None:
            print("You selected", model[treeiter][0], model[treeiter][1], model[treeiter][2])

    def on_quit_button_clicked(self, button):
        print("Quitting application")
        Gtk.main_quit()

win = TreeViewFilterWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

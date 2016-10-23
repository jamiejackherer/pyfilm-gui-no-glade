#!/usr/bin/python3
#-*- coding:utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from google import scrape_with_config, GoogleSearchError
from gettext import gettext as gt
import pandas as pd # for parsing results.csv
import gettext
import os
import sys

class pre_commands:
    def mk_download_directory():
        our_dir = os.environ["HOME"] + "/pyfilm-downloads/"
        os.environ["dir"] = our_dir
        if not os.path.exists(our_dir):
            print("Making directory:", our_dir)
            os.makedirs(our_dir)
        else:
            print("As we expected the directory", our_dir, "already exists")

    def startup_message():
            startup_message_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR,
                                    Gtk.ButtonsType.OK, "Welcome to {PyFilm}")
            startup_message_dialog.format_secondary_text("Thanks for choosing {PyFilm}.\n"
                                      "The only program to automatically "
                                      "download films to your computer.")
            startup_message_dialog.run()
            startup_message_dialog.destroy()
            print("INFO dialog closed")
            
pre_commands.mk_download_directory()
# disabled just to save time 
#pre_commands.startup_message()

class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.add(Gtk.Label(data))

class ListBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title = "{PyFilm}", height_request = 400, width_request = 200)
        self.set_border_width(10)

        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box_outer)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.box_outer.pack_start(self.listbox, True, True, 0)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.hbox.pack_start(self.vbox, True, True, 0)

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.search_entry_label = Gtk.Label("Enter title to search:", xalign=0)
        self.search_entry = Gtk.Entry()
        self.search_entry.connect("activate", self.on_search_button_clicked)
        self.hbox.pack_start(self.search_entry_label, True, True, 0)
        self.hbox.pack_start(self.search_entry, False, True, 0)
        self.search_entry.set_placeholder_text("e.g., the revanent 2016")
        self.search_entry_icon_name = "gtk-paste"
        self.search_entry.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY,
                                           self.search_entry_icon_name)
        self.search_entry.set_icon_tooltip_text(Gtk.EntryIconPosition.SECONDARY, "Click to paste from clipbord")
        
        self.search_entry.set_tooltip_text("Enter search keywords here.")
        self.listbox.add(self.row)
        
        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.proxy_label = Gtk.Label("Use Proxy", xalign=0)
        self.proxy_switch = Gtk.Switch()
        self.proxy_switch.props.valign = Gtk.Align.CENTER
        self.proxy_switch.connect("notify::active", self.on_proxy_switch_activated)
        self.proxy_switch.set_active(False)
        self.hbox.pack_start(self.proxy_label, True, True, 0)
        self.hbox.pack_start(self.proxy_switch, False, True, 0)
        self.listbox.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.cache_switch_label = Gtk.Label("Cache search results", xalign=0)
        self.cache_switch = Gtk.Switch()
        self.cache_switch.props.valign = Gtk.Align.CENTER
        self.cache_switch.connect("notify::active", self.on_cache_switch_activated)
        self.cache_switch.set_active(False)
        self.hbox.pack_start(self.cache_switch_label, True, True, 0)
        self.hbox.pack_start(self.cache_switch, False, True, 0)
        self.listbox.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.combobox_label = Gtk.Label("Number of result pages", xalign=0)
        pages = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.combobox = Gtk.ComboBoxText()
        self.combobox.set_entry_text_column(0)
        self.combobox.connect("changed", self.on_combobox_changed)
        for page in pages:
            self.combobox.append_text(page)
        self.hbox.pack_start(self.combobox_label, True, True, 0)
        self.hbox.pack_start(self.combobox, False, True, 0)
        self.listbox.add(self.row)
        
        # Our results are displayed in a listbox 
        self.results_list = Gtk.ListBox()
        csv_file = "results.csv"
        df = pd.read_csv(csv_file)
        vodlocker_link = df['link']
        link_id = df['title']
        items = link_id
        for item in items:
            self.results_list.add(ListBoxRowWithData(item))
        self.results_list.connect("row-activated", lambda widget, row: print("Selection from list: ", row.data))
        self.results_list.show_all()
        
        self.scrollable_treelist = Gtk.ScrolledWindow(height_request = 300, width_request = 400)
        self.scrollable_treelist.set_vexpand(True)
        self.box_outer.pack_start(self.scrollable_treelist, False, True, 0)
        self.scrollable_treelist.add(self.results_list)
        self.results_list.show_all()
        
        self.listbox_buttons = Gtk.ListBox()
        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.quit_button = Gtk.Button("Quit")
        self.quit_button.connect("clicked", self.on_quit_button_clicked)
        self.hbox.pack_start(self.quit_button, False, True, 0)
        self.listbox_buttons.add(self.row)

        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.search_button = Gtk.Button("Search")
        self.search_button.connect("clicked", self.on_search_button_clicked)
        self.hbox.pack_start(self.search_button, False, True, 0)
        self.listbox_buttons.add(self.row)
        
        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.download_button = Gtk.Button("Download")
        self.download_button.connect("clicked", self.on_download_button_clicked)
        self.hbox.pack_start(self.download_button, False, True, 0)
        self.listbox_buttons.add(self.row)
        
        self.row = Gtk.ListBoxRow()
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.row.add(self.hbox)
        self.spinner = Gtk.Spinner()
        self.hbox.pack_start(self.spinner, False, True, 0)
        self.listbox_buttons.add(self.row)
          
        self.box_outer.pack_start(self.listbox_buttons, True, True, 0)
        self.listbox_buttons.show_all()
    
    # Here we define our actions for various widgets such as our buttons
    def on_quit_button_clicked(self, button):
        print("Quitting application")
        Gtk.main_quit()
        
    def on_search_button_clicked(self, button):
        self.entrytext = self.search_entry.get_text()
        print("Search Button Clicked", self.entrytext)
        self.spinner.start()
        
                # prefix of search term
        site = "site:vodlocker.com " 
        # ask user for search term
        # TODO this needs to be from the entry box, use get_text() method
        keywords = site + self.entrytext
        print("We will search for : ", keywords)
        config = {
        'use_own_ip': True,                     # whether to use our own IP address 
        'keyword': keywords,
        'search_engines': ['google'],           # various configuration settings
        'num_pages_for_keyword': 1,
        'scrape_method': 'http',
        'do_caching': False,
        'num_results_per_page': 50,
        'log_level': 'CRITICAL',
        'output_filename': 'results.csv'        # file to save links to 
    #    'proxy_file': 'proxies.txt'            # file to load proixies from 
        }
        try:
            search = scrape_with_config(config)
        except GoogleSearchError as e:
            print(e)
            search_error_header = gt("Google Search Error")
            search_error_body = gt("There has been an error while searching Google "
                        "for the title you provided. ")
            search_error_dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.ERROR,
                                    Gtk.ButtonsType.OK, "")
            search_error_dialog.set_markup("<b><big>{0}</big></b>".format(search_error_header))
            search_error_dialog.format_secondary_text(search_error_body)
            search_error_dialog.run()
            search_error_dialog.destroy()
        self.spinner.stop()
        
    def on_download_button_clicked(self, button):
        print("Download Button Clicked")
        self.spinner.start()
        self.selected = self.results_list.get_selected()
        print("You selected", model[treeiter][0])
        self.spinner.stop()
        
    def paste_text(self, widget):
        text = self.clipboard.wait_for_text()
        if text != None:
            self.search_entry.set_text(text)
        else:
            print("No text on the clipboard.")
    
    def on_proxy_switch_activated(self, switch, gparam):
        if self.proxy_switch.get_active():
            state = "on"
        else:
            state = "off"
        print("Proxy switch was turned", state)
        
    def on_cache_switch_activated(self, switch, gparam):
        if self.cache_switch.get_active():
            state = "on"
        else:
            state = "off"
        print("Cache switch was turned", state)

    def on_combobox_changed(self, combo):
        number = combo.get_active_text()
        if number != None:
            print("Number of result pages to display: {0}".format(number))

win = ListBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

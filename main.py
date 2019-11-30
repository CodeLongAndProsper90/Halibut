
#!/usr/bin/env python3
import gi.repository
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit','3.0')
from gi.repository import Gtk, WebKit
import parse
"""
A simple web browser.
Based off of:
https://brobin.me/blog/2014/07/how-to-make-your-own-web-browser-in-python/
Created 11/28/19 (Thanksgiving!)
"""
class browser_win():

    def __init__(self):
        # Create window
        self.window = Gtk.Window()
        self.window.connect('destroy', self.close )
        self.window.set_default_size(360, 600)
        # Create navigation bar
        self.navigation_bar = Gtk.HBox()

        self.back = Gtk.ToolButton(Gtk.STOCK_GO_BACK)
        self.forward = Gtk.ToolButton(Gtk.STOCK_GO_FORWARD)
        self.refresh = Gtk.ToolButton(Gtk.STOCK_REFRESH)
        self.home = Gtk.ToolButton(Gtk.STOCK_HOME)
        self.search = Gtk.ToolButton(Gtk.STOCK_FIND)
        self.address_bar = Gtk.Entry()

        self.back.connect('clicked', self.go_back)
        self.forward.connect('clicked', self.go_forward)
        self.refresh.connect('clicked', self.refresh_page)
        self.home.connect('clicked', self.go_home)
        self.address_bar.connect('activate', self.load_page)

        self.navigation_bar.pack_start(self.back, False, False, 0)
        self.navigation_bar.pack_start(self.forward,False,False,0)
        self.navigation_bar.pack_start(self.refresh,False,False,0)
        self.navigation_bar.pack_start(self.home,False,False,0)
        self.navigation_bar.pack_start(self.address_bar,False,False,0)
        
        statusIcon = Gtk.StatusIcon()
        statusIcon.set_from_file('/usr/share/sd9-browser/icon.png')
        statusIcon.set_visible(True)


        # Create view for webpage
        self.view = Gtk.ScrolledWindow()
        self.webview = WebKit.WebView()
        last_page=parse.get_pkg_attr('last: ','config')
        self.webview.open(last_page)
        self.webview.connect('title-changed', self.change_title)
        self.webview.connect('load-committed', self.change_url)
        self.webview.connect('download-requested', self.download_requested)
        self.webview.connect('mime-type-policy-decision-requested', self.policy_decision_requested)
        self.view.add(self.webview)
        # Add everything and initialize
        self.container = Gtk.VBox()
        self.container.pack_start(self.navigation_bar, False,False,0)
        self.container.pack_start(self.view, True, True, 0)

        self.window.add(self.container)
        self.window.set_default_size(800,600)
        self.window.show_all()
        Gtk.main()

    def load_page(self, widget):
        address = self.address_bar.get_text()
        if address.startswith('s='):
            address= address.replace('s=','',1)
            address = 'https://google.com/search?q=' + address.replace(' ', '%20')
            self.webview.open(address)
        elif address.startswith('http://') or address.startswith('https://'):
            self.webview.open(address)
        else:
            address = 'http://' + address
            self.address_bar.set_text(address)
            self.webview.open(address)
    def change_title(self, widget, frame, title):
        self.window.set_title(title)
    def change_url(self, widget, frame):
        uri = frame.get_uri()
        self.address_bar.set_text(uri)

    def go_back(self, widget):
        self.webview.go_back()

    def go_forward(self, widget):
        self.webview.go_forward()

    def refresh_page(self, widget):
        self.webview.reload()
    def go_home(self, widget):
        from parse import get_pkg_attr
        try:
            hometxt = get_pkg_attr('home: ','config')
        except:
            hometxt='https://google.com'
        self.address_bar.set_text(hometxt)
        self.load_page(widget)

    def policy_decision_requested(self, view, frame, request, mimetype, policy_decision):
        if mimetype != 'text/html':
            policy_decision.download()
            return True

    def download_requested(self, view, download):
        import os
        import urllib
        name = download.get_suggested_filename()
        path = '~/Downloads'
        urllib.request.urlretrieve(download.get_uri(), path)  # urllib.request.urlretrieve
        return False
    def close(self,widget):
        addr = self.address_bar.get_text()
        parse.set_pkg_attrs('last: ','addr','conf')
        Gtk.main_quit()
        exit()
wow = browser_win()

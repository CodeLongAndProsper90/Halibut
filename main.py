
#!/usr/bin/python3
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

        self.backimg = Gtk.Image.new_from_file("back.png") #Make back icon
        self.back = Gtk.ToolButton() # Make back button
        self.back.set_icon_widget(self.backimg) # Bind the two
        
        #  make the foward button
        self.fowardimg = Gtk.Image.new_from_file("foward.png")
        self.forward = Gtk.ToolButton()
        self.forward.set_icon_widget(self.fowardimg)
       
        #  Make the reload button
        self.refreshimg = Gtk.Image.new_from_file("reload.png")
        self.refresh = Gtk.ToolButton()
        self.refresh.set_icon_widget(self.refreshimg)

        #  Make the home button 
        self.homeimg =  Gtk.Image.new_from_file("home.png")
        self.home = Gtk.ToolButton()
        self.home.set_icon_widget(self.homeimg)
        
        #  Make the search button
        self.searchimg = Gtk.Image.new_from_file("search.png")
        self.search = Gtk.ToolButton()
        self.search.set_icon_widget(self.searchimg)

        #  Make the address bar that you type the url in
        self.address_bar = Gtk.Entry()

        #  Connect the buttons to their respective functions
        self.back.connect('clicked', self.go_back)
        self.forward.connect('clicked', self.go_forward)
        self.refresh.connect('clicked', self.refresh_page)
        self.home.connect('clicked', self.go_home)
        self.search.connect('clicked',self.search_web)  
        self.address_bar.connect('activate', self.load_page)
        
        #  Load the buttons into the app
        
        self.navigation_bar.pack_start(self.back, False, False,  0)
        self.navigation_bar.pack_start(self.forward, False, False, 0)
        self.navigation_bar.pack_start(self.refresh, False, False, 0)
        self.navigation_bar.pack_start(self.home, False, False, 0)
        self.navigation_bar.pack_start(self.search, False, False, 0)
        self.navigation_bar.pack_start(self.address_bar, False, False, 0)
        

        # Create view for webpage
        self.view = Gtk.ScrolledWindow()
        self.webview = WebKit.WebView()
        last_page=parse.get_pkg_attr('last: ','config')
        self.webview.open(last_page)
        self.webview.connect('title-changed', self.change_title)
        self.webview.connect('load-committed', self.change_url)
        #  self.webview.connect('download-requested', self.download_requested)
        #  self.webview.connect('mime-type-policy-decision-requested', self.policy_decision_requested)
        self.view.add(self.webview)
        # Add everything and initialize
        self.container = Gtk.VBox()
        self.container.pack_start(self.navigation_bar, False,False,0)
        self.container.pack_start(self.view, True, True, 0)

        self.window.add(self.container)
        self.window.set_default_size(800,600)
        self.window.show_all()
        Gtk.main()
#  End auto-run code!
      def load_page(self, widget): #Handles loading of http and https webpages. Search_web handles google queires
        address = self.address_bar.get_text()
        self.window.set_title(f'Loading: {address}')
        if address.startswith('s='):
            
            
            address= address.replace('s=','',1)
            address = 'https://google.com/search?q=' + address.replace(' ', '%20')
            self.webview.open(address)
        elif address.startswith('http://') or address.startswith('https://'):
                  
            self.webview.open(address)
        else:
            
           
            address = 'https://' + address
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
            print(hometxt)
        except:
            hometxt='https://google.com'
        self.address_bar.set_text(hometxt)
        self.load_page(widget)

    #  def policy_decision_requested(self, view, frame, request, mimetype, policy_decision):
        #  if mimetype != 'text/html':
            #  policy_decision.download()
            #  return True
#  
    #  def download_requested(self, view, download):
        #  import os
        #  import urllib
        #  name = download.get_suggested_filename()
        #  path = '~/Downloads'
        #  urllib.request.urlretrieve(download.get_uri(), path)  # urllib.request.urlretrieve
        #  return False
    def search_web(self, widget):
            
        address = self.address_bar.get_text()
        address = 'https://google.com/search?q=' + address.replace(' ', '%20') 
        self.webview.open(address)
    def close(self,widget):
        addr = self.address_bar.get_text()
        parse.set_pkg_attr('last: ','addr','config')
        Gtk.main_quit()
        exit()
wow = browser_win()

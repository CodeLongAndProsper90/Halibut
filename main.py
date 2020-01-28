
#!/usr/bin/python3
import gi.repository
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2','4.0')
from gi.repository import Gtk, WebKit2
import parse
"""
A simple web browser.
Based off of:
https://brobin.me/blog/2014/07/how-to-make-your-own-web-browser-in-python/
Created 11/28/19 (Thanksgiving!)
assets/nexttab.png, assets/tabback.png Icon made by Flatpik from www.flaticon.com
assets/close.png made by Vectors Market www.flaticon.com
"""
class browser_win():

    def __init__(self):
        # Create window
        self.window = Gtk.Window()
        self.window.connect('destroy', self.close )
        self.window.set_default_size(360, 600)
        self.window.set_icon_from_file('assets/halibut2.png')
        # Create navigation bar
        self.navigation_bar = Gtk.HBox()

        self.backimg = Gtk.Image.new_from_file("assets/back.png") #Make back icon
        self.back = Gtk.ToolButton() # Make back button
        self.back.set_icon_widget(self.backimg) # Bind the two
        
        #  make the foward button
        self.fowardimg = Gtk.Image.new_from_file("assets/foward.png")
        self.forward = Gtk.ToolButton()
        self.forward.set_icon_widget(self.fowardimg)
       
        #  Make the reload button
        self.refreshimg = Gtk.Image.new_from_file("assets/reload.png")
        self.refresh = Gtk.ToolButton()
        self.refresh.set_icon_widget(self.refreshimg)

        #  Make the home button 
        self.homeimg =  Gtk.Image.new_from_file("assets/home.png")
        self.home = Gtk.ToolButton()
        self.home.set_icon_widget(self.homeimg)
        
        #  Make the search button
        self.searchimg = Gtk.Image.new_from_file("assets/search.png")
        self.search = Gtk.ToolButton()
        self.search.set_icon_widget(self.searchimg)

        self.nexttabimg = Gtk.Image.new_from_file("assets/nexttab.png")
        self.nexttab = Gtk.ToolButton()
        self.nexttab.set_icon_widget(self.nexttabimg)

        #This is the "tab back" button img

        self.lasttabimg = Gtk.Image.new_from_file("assets/tabback.png")
        self.lasttab = Gtk.ToolButton()
        self.lasttab.set_icon_widget(self.lasttabimg)


        self.closetabimg = Gtk.Image.new_from_file('assets/close.png')
        self.closetab = Gtk.ToolButton()
        self.closetab.set_icon_widget(self.closetabimg)

        #  Make the address bar that you type the url in
        
        self.tablbl = Gtk.Label()
        self.address_bar = Gtk.Entry()
        self.address_bar.set_property("width-request", 100) # Define default sive

        #  Connect the buttons to their respective functions
        self.back.connect('clicked', self.go_back) # Go back a page
        self.forward.connect('clicked', self.go_forward) # go foward a page
        self.refresh.connect('clicked', self.refresh_page) # Reload page
        self.home.connect('clicked', self.go_home) # GO to home page
        self.search.connect('clicked',self.search_web) # search the text ing the uri bar on google.com
        self.nexttab.connect('clicked', self.next_tab) # go to the next tab
        self.lasttab.connect('clicked', self.back_tab) # go back a tab
        self.closetab.connect('clicked', self.close_tab)
        self.address_bar.connect('activate', self.load_page)
        
        #  Load the buttons into the app
        # The False, False, 0 make the images work, but I don't why.
        # I suspect black magic...
        self.navigation_bar.pack_start(self.back, False, False,  0)
        self.navigation_bar.pack_start(self.forward, False, False, 0)
        self.navigation_bar.pack_start(self.refresh, False, False, 0)
        self.navigation_bar.pack_start(self.home, False, False, 0)
        self.navigation_bar.pack_start(self.search, False, False, 0)
        self.navigation_bar.pack_start(self.address_bar, False, False, 0)
        self.navigation_bar.pack_start(self.closetab, False, False, 0)
        
        self.navigation_bar.pack_start(self.lasttab, False, False, 0)
        
        self.navigation_bar.pack_start(self.closetab, False, False, 0)
        
        self.navigation_bar.pack_start(self.nexttab, False, False, 0)
        
        self.navigation_bar.pack_start(self.tablbl, False, False, 0)
        
        # Create view for webpage
        self.view = Gtk.ScrolledWindow()
        self.webview = WebKit2.WebView()
        self.go_home(None)
        last_page=parse.get_pkg_attr('last: ','config')
        self.webview.load_uri(last_page)
        # self.webview.connect('title-changed', self.change_title)
        # self.webview.connect('load-committed', self.change_url)
        #  self.webview.connect('download-requested', self.download_requested)
        #  self.webview.connect('mime-type-policy-decision-requested', self.policy_decision_requested)
        self.view.add(self.webview)
        # Add everything and initialize
        self.container = Gtk.VBox()
        self.container.pack_start(self.navigation_bar, False,False,0)
        self.container.pack_start(self.view, True, True, 0)

        self.window.add(self.container)
        self.window.set_default_size(800,600)
        self.tabs = ["https://google.com", "https://bing.com", "https://linux.org", 'https://copy.sh/v86']
        self.pos=0
        self.window.show_all()
        try:
            Gtk.main()
        except KeyboardInterrupt or EOFError:
        
            addr = self.address_bar.get_text()
            parse.set_pkg_attr('last: ',addr,'config')
            Gtk.main_quit()
            exit()
            
            #  End auto-run code!
    def load_page(self, widget): #Handles loading of http and https webpages. Search_web handles google queires
        address = self.address_bar.get_text()
        self.window.set_title(f'Loading: {address}')
        if address.startswith('s='):       
                
            address= address.replace('s=','',1)
            address = 'https://google.com/search?q=' + address.replace(' ', '%20')
            self.webview.open(address)
        elif address.startswith('http://') or address.startswith('https://'):              
            self.webview.load_uri(address)
        else:   
               
            address = 'https://' + address
            self.address_bar.set_text(address)
            self.webview.load_uri(address)

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
            self.homeloc = get_pkg_attr('home: ','config')
            print(self.homeloc)
        except:
            self.homeloc='https://google.com'
        self.address_bar.set_text(self.homeloc)
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
    def search_web(self, widget): #Queries google.com for the string in the addressbar
            
        address = self.address_bar.get_text()
        address = 'https://google.com/search?q=' + address.replace(' ', '%20') 
        self.webview.load_uri(address)
    def close(self,widget): 
        addr = self.address_bar.get_text()
        parse.set_pkg_attr('last: ',addr,'config')
        Gtk.main_quit()
        exit()
    def next_tab(self, widget):
      self.pos+=1
      if self.pos-1 > len(self.tabs)-1:
        self.tabs.append(self.homeloc)
        active = self.tabs[self.pos-1]

      else: 
        active = self.tabs[self.pos]
      print(active)
      self.address_bar.set_text(active)
      self.load_page(None)
      self.tablbl.set_label(f"Tab ({self.pos}/{len(self.tabs)})")

    def back_tab(self, widget):
      self.pos-=1
      # if self.pos > len(self.tabs)-1:
      active = self.tabs[self.pos]
      print(active)
      self.address_bar.set_text(active)
      self.load_page(None)
      self.tablbl.set_label(f"Tab ({self.pos}/{len(self.tabs)})")
    def close_tab(self, widget):
      print(len(self.tabs))
      if len(self.tabs) > 1:
        del self.tabs[self.pos]
        self.address_bar.set_text(self.tabs[self.pos])
        self.tablbl.set_label(f"Tab ({self.pos}/{len(self.tabs)})")
        self.load_page(None)


wow = browser_win()

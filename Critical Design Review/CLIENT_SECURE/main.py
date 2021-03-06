from readers.PN532_UART.ReaderThread import ReaderThread
from query.QueryThread import QueryThreader
from Watchdog import Watchdog
import gi, os, sys
import datetime

gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject, GdkPixbuf, Gdk
from pprint import pprint as pp

WORKINGDIR = os.getcwd()
tickPath = os.path.join(WORKINGDIR, "styles", "icons", "tick.png")
crossPath = os.path.join(WORKINGDIR, "styles", "icons", "cross.png")
defaultText = "Please identify yourself"


class Window(Gtk.Window):

    def __init__(self):
        if len(sys.argv) > 1:
            self.test = sys.argv[1] == "test"
        else:
            self.test = False

        # ---- User Variables ----
        self.dog = Watchdog(600, self.logout)
        self.uid = None
        
        # ----- Global window parameters -----
        Gtk.Window.__init__(self, title="UPC")

        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(20)
        self.set_resizable(False)

        # ----- CSS Style -----
        style_provider = Gtk.CssProvider()

        style_provider.load_from_path('./styles/css/styles.css')

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # ----- SetUp window parameters -----
        # Main box
        self.vlipbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.entry_ip = Gtk.Entry()
        self.entry_ip.set_text("localhost:8081")
        self.entry_ip.connect("key-release-event", self.on_key_ip_release)
        self.vlipbox.pack_start(self.entry_ip, True, True, 0)
        self.add(self.vlipbox)

        # ----- LogIn window parameters -----
        # Main box
        self.hloginbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        #self.add(self.hloginbox)
        self.vloginbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.hloginbox.pack_start(self.vloginbox, True, True, 0)
        self.hbuttonbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        # Label UID
        self.uid_label = Gtk.Label(label=defaultText, justify=Gtk.Justification.LEFT)
        self.vloginbox.pack_start(self.uid_label, True, True, 0)
        
        # Clear button
        self.clear_button = Gtk.Button(label="Clear")
        self.clear_button.connect("clicked", self.on_clear_clicked)
        self.hbuttonbox.pack_start(self.clear_button, True, True, 0)
        self.clear_button.set_name("clear_button")
        self.clear_button.set_sensitive(False)

        # OK button
        self.ok_button = Gtk.Button(label="Ok!")
        self.ok_button.connect("clicked", self.on_ok_clicked)
        self.hbuttonbox.pack_start(self.ok_button, True, True, 0)
        self.ok_button.set_name("ok_button")
        self.vloginbox.pack_start(self.hbuttonbox, True, True, 10)
        self.ok_button.set_sensitive(False)
        
        # Icon
        self.image = Gtk.Image()

        self.tick = GdkPixbuf.Pixbuf.new_from_file_at_size(tickPath, 40, 40)
        self.cross = GdkPixbuf.Pixbuf.new_from_file_at_size(crossPath, 40, 40)

        self.image.set_from_pixbuf(self.cross)
        self.image.set_name("imager_name")
        self.hloginbox.pack_start(self.image, True, True, 10)

        # ----- User window parameters -----
        # Main boxes
        self.vuserbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.huserbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.vuserbox.pack_start(self.huserbox, True, True, 0)

        # Labels
        self.greater_label = Gtk.Label(label="Welcome ", justify=Gtk.Justification.LEFT)
        self.huserbox.pack_start(self.greater_label, True, True, 0)

        self.username_label = Gtk.Label(justify=Gtk.Justification.LEFT)
        self.huserbox.pack_start(self.username_label, True, True, 0)
        self.username_label.set_name("username_label")

        # LogOut Button
        self.logout_button = Gtk.Button(label="Logout")
        self.logout_button.connect("clicked", self.on_logout_clicked)
        self.huserbox.pack_start(self.logout_button, False, False, 50)
        self.logout_button.set_name("logout_button")

        # TextBox + label
        self.entry = Gtk.Entry()
        self.entry.set_text("Type in your query")
        self.entry.connect("key-release-event", self.on_key_release)
        self.vuserbox.pack_start(self.entry, True, True, 20)
        self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic")
        self.message_label = Gtk.Label(label="Enter your querry", justify=Gtk.Justification.CENTER)
        self.message_label.set_name("padded_label")
        self.vuserbox.pack_start(self.message_label, True, True, 0)

        # Tree view and scrolled window
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_border_width(0)
        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)

        self.timetables_store = Gtk.ListStore(str, str, str, str, str)  # The last str holds the colour in hex
        self.marks_class_store = Gtk.ListStore(str, str, float, str)   # The last str holds the colour in hex
        self.tasks_class_store = Gtk.ListStore(str, str, str, str) 
        self.tree = Gtk.TreeView()
        self.scrolled_window.add(self.tree)

        self.scrolled_window.set_min_content_height(300)
        self.titles = {
                        "Timetables": ["day", "hour", "subject", "room"],
                        "Tasks": ["date", "subject", "name"],
                        "Marks": ["subject", "name", "mark"]
                        }

        # ----- Start the reader thread and set up the query thread -----
        self.reader = ReaderThread(self.test, self.on_uid)

        self.server = None
    
    def on_key_ip_release(self, widget, ev, data=None):
        """ Function connected to the key release of the ip entry, if it's escape, it clears the text and if it's enter
        it sets the ip
        :param widget: The entry itself
        :return:
        """
        if ev.keyval == Gdk.KEY_Escape:
            widget.set_text("")
            self.show_all()
        elif ev.keyval == Gdk.KEY_Return:  # Value for enter
            ip = widget.get_text().split(':')[0]
            port = widget.get_text().split(':')[1]
            print("created")
            self.server = QueryThreader(ip, port)
            self.remove(self.vlipbox)
            self.add(self.hloginbox)
            self.show_all()
            self.reader.startReader()
        
    def on_uid(self, UID):
        """ Handler for the ReaderThread module to change the label text and the image pixel source
        :param UID: User Identifier of the read card
        :return: None
        """
        self.uid = UID
        self.uid_label.set_text(UID.center(len(defaultText)))
        
        self.clear_button.set_sensitive(True)
        self.server.get_username(self.uid, self.on_username_label, True)

    def on_clear_clicked(self, widget):
        """ Function connected to the clicked signal of the clear button. Restores default values for the label and
        the image. Restarts de reader thread.
        :param widget: The button itself
        :return:
        """
        self.login_to_default()
        self.reader.startReader()

    def on_ok_clicked(self, widget):
        """ Function connected to the clicked signal of the ok button. Restores default values of the log in page,
        changes to teh user page and requests the user name to the server.
        :param widget: The button itself
        :return: None
        """
        self.dog.watch_start()
        self.login_to_default()
        self.remove(self.hloginbox)
        self.add(self.vuserbox)
        self.show_all()
        self.resize(400, 480)

    def on_username_label(self, username, args):
        """ Handler for the QueryThread module to change the label text and t
        :param username: Users full name
        :return: None
        """
        if username :
            self.image.set_from_pixbuf(self.tick)
            self.ok_button.set_sensitive(True)
            self.username_label.set_text(username[0]['user_name'])
        else:
            self.image.set_from_pixbuf(self.cross)
            self.uid_label.set_name("colection_label_error")

    def login_to_default(self):
        """ Restores default LogIn window parameters
        :param
        :return: None
        """
        self.uid_label.set_name("colection_label")
        self.uid_label.set_text("Please identify yourself")
        self.image.set_from_pixbuf(self.cross)
        self.ok_button.set_sensitive(False)
        self.clear_button.set_sensitive(False)

    def on_logout_clicked(self, widget):
        self.logout()
        
    def logout(self):
        """ Function connected to the clicked signal of the LogOut button. Restores default LogIn window
        :param widget: The button itself
        :return: None
        """
        self.entry.set_text("Type in your query")
        self.message_label.set_text("Enter your querry")
        self.user_to_default()
        self.remove(self.vuserbox)
        self.add(self.hloginbox)
        self.show_all()
        self.reader.startReader()
        self.message_label.set_name("padded_label")
        self.resize(232, 90)    # Apropiate values for teh login screen

    def on_key_release(self, widget, ev, data=None):
        """ Function connected to the key release of the entry, if it's escape, it clears the text and if it's enter
        it sends the command.
        :param widget: The entry itself
        :return:
        """
        self.dog.activity()
        if ev.keyval == Gdk.KEY_Escape:
            widget.set_text("")
            self.show_all()

        elif ev.keyval == Gdk.KEY_Return:  # Value for enter
            print(widget.get_text())
            self.server.send_query(self.on_tree, widget.get_text(), "Secure_" in widget.get_text() )
            print(self.get_size())

    def on_tree(self, data, type_of_query):
        """ Handler for all types of query that afect the tree view
        :param data: vector of dicts
        :return None
        """
        type_of_query  = type_of_query.replace("Secure_", "")
        if data == "Timeout error":
            self.message_label.set_text(data)
            self.message_label.set_name("colection_label_error")
        else:
            self.message_label.set_name("colection_label")
            self.message_label.set_text(type_of_query)
            if type_of_query == "Timetables":
                self.tree.set_model(self.timetables_store)
            elif type_of_query == "Marks" :
                self.tree.set_model(self.marks_class_store)
            elif type_of_query == "Tasks":
                self.tree.set_model(self.tasks_class_store)
            # Check if is the first time
            if len(self.timetables_store) == 0 and len(self.marks_class_store) == 0:
                self.vuserbox.pack_start(self.scrolled_window, True, True, 20)
                self.show_all()
            self._clear_tree_titles()
            self._set_tree_titles(data, type_of_query)
            self._set_store_data(data, type_of_query)

    def user_to_default(self):
        """ Restores default User window parameters
        :param
        :return: None
        """
        self._clear_tree_titles()
        self.timetables_store.clear()
        self.marks_class_store.clear()
        self.vuserbox.remove(self.scrolled_window)

    def _clear_tree_titles(self):
        """ Removes the titles from the tree
		    :param
		    :return: None
        """
        cols = self.tree.get_columns()
        for col in cols:
            self.tree.remove_column(col)

    def _set_store_data(self, data, type_of_query):
        """Sets the data to be displayed to the store and the colours
        :param: data: response for the server, a vector of rows (dictionaries)
        type_of_query: key foer the self.titles dict
        :return: None
        """
        dies ={0: "Dilluns", 1: "Dimarts", 2:"Dimecres", 3: "Dijous", 4: "Divendres", 5: "Dissabte", 6: "Diumenge"}
        if type_of_query == "Timetables":
            today_day = dies[datetime.date.today().weekday()]
            today_hour = datetime.datetime.today().hour
            print(today_hour, today_day)
            split_index=0
            for i in range(len(data)):
                for j in data[i].keys():
                    if data[i][j]==today_day and data[i]["hour"]>=today_hour and split_index==0:
                        split_index=i
                        print(split_index)
            aux=data[0:split_index]
            data=data[split_index:]
            data.extend(aux)
        print(data)
        for i, row in enumerate(data):
            aux = []
            for title in self.titles[type_of_query]:
                add_cell=row[title]
                if title=="date":
                    add_cell=add_cell.split("T")[0]
                elif title=="hour":
                    add_cell=str(datetime.timedelta(hours=row[title]))
                aux.append(add_cell)
                if i% 2 == 0:
                    background_color = "#fff"
                else:
                    background_color = "#bbb"
            self.tree.get_model().append(tuple(aux)+(background_color,))


    def _set_tree_titles(self, data, type_of_query):
        """Sets the titles of the data to be displayed to the store
        :param: type_of_query: key foer the self.titles dict
        :return: None
        """
        titles = self.titles[type_of_query]
        self.message_label.set_text(type_of_query)
        self.message_label.set_name("colection_label")
        self.tree.get_model().clear()
        for i, title in enumerate(titles):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=i) 
            column.pack_start(renderer, True)
            column.add_attribute(renderer, "text", i)
            column.add_attribute(renderer, "background", len(titles))
            self.tree.append_column(column)


if __name__ == '__main__':
    win = Window()
    win.show_all()
    Gtk.main()

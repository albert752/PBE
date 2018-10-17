from RFID import RFID
import gi
import threading
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject

class LogInWindow(Gtk.Window):

    def __init__(self):
        self.lector = RFID(True)

        Gtk.Window.__init__(self, title="UPC")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(20)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(self.vbox)

        self.label = Gtk.Label(label="Please identify yourself", justify=Gtk.Justification.LEFT)
        self.vbox.pack_start(self.label, True, True, 10)

        self.button = Gtk.Button(label="Clear")
        self.button.connect("clicked", self.on_button_clicked)
        self.vbox.pack_start(self.button, True, True, 10)

        self.show_all()

        self.thread = threading.Thread(target=self.updateLabel)
        self.thread.daemon = True
        self.thread.start()


    def updateLabel(self):
        while(True):
            self.lector.readThread(self.handler)

    def handler(self, UID):
        GLib.idle_add(self.label.set_text, UID)

    def on_button_clicked(self, widget):
        self.label.set_text("Please identify yourself")

if __name__ == '__main__':
    win = LogInWindow()
    Gtk.main()
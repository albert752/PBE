from RFID import RFID
import gi, os
import threading
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject, GdkPixbuf
WORKINGDIR = os.getcwd()

tickPath = os.path.join(WORKINGDIR, "data", "icons", "tick.png")
crossPath = os.path.join(WORKINGDIR, "data", "icons", "cross.png")
defaultText = "Please identify yourself"



class LogInWindow(Gtk.Window):

    def __init__(self):
        self.lector = RFID(True)

        Gtk.Window.__init__(self, title="UPC")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(20)

        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.add(self.hbox)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.hbox.pack_start(self.vbox, True, True, 10)

        self.label = Gtk.Label(label=defaultText, justify=Gtk.Justification.LEFT)
        self.vbox.pack_start(self.label, True, True, 10)

        self.button = Gtk.Button(label="Clear")
        self.button.connect("clicked", self.on_button_clicked)
        self.vbox.pack_start(self.button, True, True, 10)

        self.image = Gtk.Image()

        self.tick = GdkPixbuf.Pixbuf.new_from_file_at_size(tickPath, 40, 40)
        self.cross = GdkPixbuf.Pixbuf.new_from_file_at_size(crossPath, 40, 40)

        self.image.set_from_pixbuf(self.cross)
        self.hbox.pack_start(self.image, True, True, 10)
        self.show_all()

        self.lector.start(self.onUID)

    def onUID(self, UID):
        GLib.idle_add(self.label.set_text, UID.center(len(defaultText)))
        GLib.idle_add(self.image.set_from_pixbuf, self.tick)

    def on_button_clicked(self, widget):
        self.label.set_text("Please identify yourself")
        self.image.set_from_pixbuf(self.cross)


if __name__ == '__main__':
    win = LogInWindow()
    Gtk.main()
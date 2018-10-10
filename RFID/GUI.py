import threading
import time
import _thread
from RFID import RFID
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class MyWindow(Gtk.Window):
    labelText = "Please, Indentify yourself"
    _clear = True

    def __init__(self):
        # global labelText

        Gtk.Window.__init__(self, title="UPC LogIn")
        self.set_border_width(10)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.button1 = Gtk.Button(label="Clear")
        handler_id = self.button1.connect("clicked", self.on_button1_clicked)
        self.box.pack_end(self.button1, True, True, 10)

        # create an image
        image = Gtk.Image()
        # set the content of the image as the file filename.png
        image.set_from_file("./images/tick.png")
        # add the image to the window
        self.add(image)

        self.label = Gtk.Label(self.labelText)
        self.box.pack_end(self.label, True, True, 10)

    def on_button1_clicked(self, widget):
        self._clear = True
        self.label.set_label(self.labelText)

    def getClear(self):
        return self._clear

    def setClear(self, value):
        self._clear = value

def _readRFID():
    reader = RFID()
    uid = reader.read_uid()
    return uid

def _readUID():
    values = _readRFID()
    uid = values.split(" ")[8:]
    uid = "".join(uid).split("0x")
    uid = "".join(uid)
    return uid.upper()

def labelUpdater(win):
    while(True):
        if(win.getClear()):
            win.setClear(False)
            win.label.set_label(_readUID())


if __name__ == '__main__':
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    _thread.start_new_thread(labelUpdater, (win,))
    Gtk.main()

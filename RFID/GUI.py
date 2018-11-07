"""LogIn system GUI class

This module contains the implementation of the LogIn window.

Example:
    With an RFID reader:
        First of all, connect the RFID reader on the apropiate pins. Here there
        is a small table:

        | pn532 | RPi B3          |
        |-------|-----------------|
        |    5V | 5V (pin 4 or 2) |
        |   GND | GND (pin 6)     |
        |   SDA | SDA0 (pin3)     |
        |   SCL | SCL0 (pin5)     |

        Then run:

        $ python3 GUI.py


    Without an RFID reader
        If your purpose is just to test the app without a reader, you can do so
        by running this command:

        $ python3 GUI.py test

        It will automatically yield the same UID every 3s.
"""
from RFID import RFID
import gi, os, sys
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject, GdkPixbuf


WORKINGDIR = os.getcwd()
tickPath = os.path.join(WORKINGDIR, "data", "icons", "tick.png")
crossPath = os.path.join(WORKINGDIR, "data", "icons", "cross.png")
defaultText = "Please identify yourself"


class LogInWindow(Gtk.Window):

    """LogIn system GUI class

        Little window w/ a clear button a label and an image. Label and image change when the RFID is read and
        when the button is clicked.

    """

    def __init__(self):
        """ Creates the window layout as a horizontal bow with a vertical box and an image. The vertical box contains
        the label and the button. Also creates and  starts the RFID module.
        """
        if len(sys.argv) > 1:
            self.test = sys.argv[1]=="test"
        else:
            self.test = False
        self.lector = RFID(self.test)

        Gtk.Window.__init__(self, title="UPC")
        self.connect("destroy", Gtk.main_quit)
        self.set_border_width(20)
        self.set_resizable(False)

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
        """ Handler for the RFID module to change the label text and the image pixel source
        :param UID: User Identifier of the read card
        :return: None
        """
        self.label.set_text(UID.center(len(defaultText)))
        self.image.set_from_pixbuf(self.tick)

    def on_button_clicked(self, widget):
        """ Function connected to the clicked signal of the button. Restores default values for the label and
        the image.
        :param widget: The button itself
        :return:
        """
        self.label.set_text("Please identify yourself")
        self.image.set_from_pixbuf(self.cross)


if __name__ == '__main__':
    win = LogInWindow()
    Gtk.main()

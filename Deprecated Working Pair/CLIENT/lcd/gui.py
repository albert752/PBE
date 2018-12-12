import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import lcd


class LCDWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Label Example")
		self.set_size_request(-1, -1)
		
		self.box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		
		self.textview = Gtk.TextView()
		self.textview.set_monospace(True)
		self.textview.set_size_request(145,60)
		self.box.add(self.textview)
		
		self.textbuffer = self.textview.get_buffer()
		
		
		self.button = Gtk.Button(label="display")
		self.button.connect("clicked", self.on_button_clicked)
		self.box.add(self.button)
		
		
		self.add(self.box)
		
		self.connect("destroy",Gtk.main_quit)
		self.show_all()
		
			
	def on_button_clicked(self, widget):
		text=self.textbuffer.get_text(self.textbuffer.get_start_iter(), self.textbuffer.get_end_iter(), False)
		lcd.print_text(text)


def main():
	win= LCDWindow()
	Gtk.main()


if __name__ == "__main__":
	main()

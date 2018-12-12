import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


xim = [("Oranges", 5), ("Apples", 3), ("Bananas", 1), ("Tomatoes", 4), ("Cucumber", 1), ("potatoes", 10),
       ("apricot", 100)]

window = Gtk.Window()
window.connect("destroy", lambda q: Gtk.main_quit())
liststore = Gtk.ListStore(str, int, str)
for i in range(len(xim)):
    if i % 2 == 0:
        background_color = "#fff"
    else:
        background_color = "#bbb"
    liststore.append(xim[i] + (background_color,))

treeview = Gtk.TreeView(model=liststore)
window.add(treeview)
treeviewcolumn = Gtk.TreeViewColumn("Item")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
treeviewcolumn.pack_start(cellrenderertext, True)
treeviewcolumn.add_attribute(cellrenderertext, "text", 0)
treeviewcolumn.add_attribute(cellrenderertext, "background", 2)

treeviewcolumn = Gtk.TreeViewColumn("Quantity")
treeview.append_column(treeviewcolumn)
cellrenderertext = Gtk.CellRendererText()
treeviewcolumn.pack_start(cellrenderertext, True)
treeviewcolumn.add_attribute(cellrenderertext, "text", 1)
treeviewcolumn.add_attribute(cellrenderertext, "background", 2)

window.show_all()
Gtk.main()

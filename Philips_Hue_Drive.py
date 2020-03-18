#!/usr/bin/env python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf 
from hue_config import lamp_dict
from hue_class import HueLamp

for a, n in lamp_dict.items():
    globals()[n] = HueLamp(a, n)

class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        
        Gtk.Window.__init__(self, title="Box Test", application=app)
        #self.set_default_size(400, 400)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.MOUSE)
        self.settings = Gtk.Settings.get_default()
        self.settings.set_property("gtk-application-prefer-dark-theme", True)
        
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "Phlips Hue Drive"
        self.set_titlebar(self.hb)

        hue_button = Gtk.MenuButton()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("/home/walter/bluetooth/hue/hue_ble_gtk/bulb_icon.jpg", 40, 40, preserve_aspect_ratio=True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        hue_button.add(image)
        main_menu = Gtk.Menu()
        hue_button.set_popup(main_menu)
        self.hb.pack_start(hue_button)

        admin_menu_item = Gtk.MenuItem(label="Hue Admin")
        main_menu.append(admin_menu_item)

        admin_submenu = Gtk.Menu()
        admin_menu_item.set_submenu(admin_submenu)

        menuitem = Gtk.MenuItem(label="import new Bulb")
        admin_submenu.append(menuitem)
        menuitem = Gtk.MenuItem(label="show lamp_dict")
        admin_submenu.append(menuitem)
        menuitem = Gtk.MenuItem(label="set bulb name")
        admin_submenu.append(menuitem)
        menuitem = Gtk.MenuItem(label="transitiontime")
        admin_submenu.append(menuitem)
        quit_menuitem = Gtk.MenuItem(label="Quit")
        quit_menuitem.connect('activate', self.quit_menuitem_selected)
        admin_submenu.append(quit_menuitem)


        fun_menu_item = Gtk.MenuItem(label="Hue Fun")
        main_menu.append(fun_menu_item)

        fun_submenu = Gtk.Menu()
        fun_menu_item.set_submenu(fun_submenu)

        menuitem = Gtk.MenuItem(label="pass")
        fun_submenu.append(menuitem)
        menuitem = Gtk.MenuItem(label="pass")
        fun_submenu.append(menuitem)
        menuitem = Gtk.MenuItem(label="pass")
        fun_submenu.append(menuitem)
        menuitem = Gtk.MenuItem(label="pass")
        fun_submenu.append(menuitem)

        main_menu.show_all()
        
        self.vbox = Gtk.VBox(spacing=10)

        for lamp in lamp_dict.values():
            hl_obj = globals()[lamp]

            label_lamp = Gtk.Label()
            label_lamp.props.halign = Gtk.Align.START
            label_lamp.set_text(lamp)

            on_off_switch = Gtk.Switch()
            on_off_switch.props.valign = Gtk.Align.CENTER
            on_off_switch.props.halign = Gtk.Align.START
            on_off_switch.set_tooltip_text("Off <> On")
            if hl_obj.on_off_state() == "on":
                on_off_switch.set_active(True)
            else:
                on_off_switch.set_active(False)
            on_off_switch.connect("notify::active", self.on_off_switch_activated, lamp)

            #color_button = Gtk.ColorButton()

            label_mir = Gtk.Label()
            label_mir.set_text("mired")

            mir = Gtk.Adjustment(value=326, lower=153, upper=500, step_increment=20, page_increment=20, page_size=0)

            mir_spinbutton = Gtk.SpinButton(adjustment=mir)

            mir_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=mir)
            mir_scale.set_value_pos(Gtk.PositionType.RIGHT)
            mir_scale.set_value(hl_obj.mired_get())
            mir_scale.set_digits(0)
            mir_scale.set_hexpand(True)
            mir_scale.set_vexpand(False)
            mir_scale.connect("value-changed", self.mir_scale_moved, hl_obj)


            label_bri = Gtk.Label()
            label_bri.set_text("brightness")

            bri = Gtk.Adjustment(value=126, lower=1, upper=254, step_increment=10, page_increment=10, page_size=0)

            bri_spinbutton = Gtk.SpinButton(adjustment=bri)

            bri_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=bri)
            bri_scale.set_value_pos(Gtk.PositionType.RIGHT)
            bri_scale.set_value(hl_obj.brightness_get())
            bri_scale.set_digits(0)
            bri_scale.set_hexpand(True)
            bri_scale.set_vexpand(False)
            bri_scale.connect("value-changed", self.bri_scale_moved, hl_obj)

            grid = Gtk.Grid()
            grid.set_column_homogeneous(True)  # c  r  hs vs
            #grid.set_column_spacing(40)
            grid.attach(label_lamp,               0, 0, 1, 1)
            grid.attach(on_off_switch,            0, 1, 1, 1)
            grid.attach(label_mir,                1, 0, 1, 1)
            grid.attach(mir_scale,                2, 0, 1, 1)
            grid.attach(label_bri,                1, 1, 1, 1)
            grid.attach(bri_scale,                2, 1, 1, 1)

            self.vbox.pack_start(grid, True, True, 0)
            
        self.add(self.vbox)

    def quit_menuitem_selected(self, widget):
        app.quit()

    def on_off_switch_activated(self, widget, active, lamp):
        hl_obj = globals()[lamp]
        if widget.get_active():
            hl_obj.on_off_switch(1)
        else:
            hl_obj.on_off_switch(0)

    def mir_scale_moved(self, mir_scale, hl_obj):
            hl_obj.mired_set(int(mir_scale.get_value()))

    def bri_scale_moved(self, bri_scale, hl_obj):
            hl_obj.brightness_set(int(bri_scale.get_value()))

    def hue_button_clicked(self, widget):
        AdminWindow()

class AdminWindow(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.MOUSE)

        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "Phlips Hue Drive: Admin"
        self.set_titlebar(self.hb)

        hue_button = Gtk.Button()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("/home/walter/bluetooth/hue/hue_ble_gtk/bulb_icon.jpg", 40, 40, preserve_aspect_ratio=True)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        hue_button.add(image)
        self.hb.pack_start(hue_button)

        self.show_all()



class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MainWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)




#!/usr/bin/env python3


import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from hue_class import HueLamp
from hue_config import lamp_dict

for a, n in lamp_dict.items():
    globals()[n] = HueLamp(a, n)

class MyWindow(Gtk.Window):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Philips Hue Drive", application=app)
        self.set_default_size(400, 200)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.MOUSE)
        #self.maximize()

        menubar = Gtk.MenuBar()
        menubar.set_hexpand(True)

        hue_admin_menuitem = Gtk.MenuItem(label="Hue Admin")
        menubar.append(hue_admin_menuitem)
        
        menu = Gtk.Menu()
        hue_admin_menuitem.set_submenu(menu)

        menuitem = Gtk.MenuItem(label="manage new Bulb")
        menu.append(menuitem)
        menuitem = Gtk.MenuItem(label="show lamp_dict")
        menu.append(menuitem)
        menuitem = Gtk.MenuItem(label="set bulb name")
        menu.append(menuitem)
        menuitem = Gtk.MenuItem(label="transitiontime")
        menu.append(menuitem)
        self.quit_menuitem = Gtk.MenuItem(label="Quit")
        self.quit_menuitem.connect('activate', self.quit_menuitem_selected)
        menu.append(self.quit_menuitem)


        hue_fun_menuitem = Gtk.MenuItem(label="Hue Fun")
        menubar.append(hue_fun_menuitem)

        menu = Gtk.Menu()
        hue_fun_menuitem.set_submenu(menu)

        alert_menuitem = Gtk.MenuItem(label="alert")
        menu.append(alert_menuitem)
        menuitem = Gtk.MenuItem(label="mired")
        menu.append(menuitem)
        menuitem = Gtk.MenuItem(label="brightness")
        menu.append(menuitem)
        menuitem = Gtk.MenuItem(label="color")
        menu.append(menuitem)
        
        menu = Gtk.Menu()
        alert_menuitem.set_submenu(menu)

        self.ping_menuitem = Gtk.MenuItem(label="ping")
        self.ping_menuitem.connect("activate", self.ping_menuitem_selected)
        menu.append(self.ping_menuitem)
        self.blink_menuitem = Gtk.MenuItem(label="blink")
        self.blink_menuitem.connect("activate", self.blink_menuitem_selected)
        menu.append(self.blink_menuitem)
        self.stop_blinking_menuitem = Gtk.MenuItem(label="stop blinking")
        self.stop_blinking_menuitem.connect("activate", self.stop_blinking_menuitem_selected)
        menu.append(self.stop_blinking_menuitem)


        self.on_off_switch = Gtk.Switch()
        self.on_off_switch_set_state()
        self.on_off_switch.connect("notify::active", self.on_off_switch_activated)

        self.label_mir = Gtk.Label()
        self.label_mir.set_text("mired 153-500")

        mir = Gtk.Adjustment(value=326, lower=153, upper=500, step_increment=20, page_increment=20, page_size=0)

        self.mir_spinbutton = Gtk.SpinButton(adjustment=mir)
        #self.mir_spinbutton.connect("value-changed", self.mir_spinbutton_changed)

        self.mir_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=mir)
        self.mir_scale.set_value_pos(Gtk.PositionType.BOTTOM)
        self.mir_scale_set_state()
        self.mir_scale.set_digits(0)
        self.mir_scale.set_hexpand(True)
        self.mir_scale.set_vexpand(False)
        self.mir_scale.connect("value-changed", self.mir_scale_moved)


        self.label_bri = Gtk.Label()
        self.label_bri.set_text("brightness 1-254")

        bri = Gtk.Adjustment(value=126, lower=1, upper=254, step_increment=10, page_increment=10, page_size=0)

        self.bri_spinbutton = Gtk.SpinButton(adjustment=bri)
        #self.bri_spinbutton.connect("value-changed", self.bri_spinbutton_changed)

        self.bri_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=bri)
        self.bri_scale.set_value_pos(Gtk.PositionType.BOTTOM)
        self.bri_scale_set_state()
        self.bri_scale.set_digits(0)
        self.bri_scale.set_hexpand(True)
        self.bri_scale.set_vexpand(False)
        self.bri_scale.connect("value-changed", self.bri_scale_moved)


        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_row_homogeneous(False)
        grid.attach(menubar,                  0, 0, 2, 1)
        grid.attach(self.on_off_switch,       1, 1, 1, 1)
        grid.attach(self.label_mir,           0, 2, 1, 1)
        grid.attach(self.mir_spinbutton,      1, 3, 1, 1)
        grid.attach(self.mir_scale,           0, 3, 1, 1)
        grid.attach(self.label_bri,           0, 4, 1, 1)
        grid.attach(self.bri_spinbutton,      1, 5, 1, 1)
        grid.attach(self.bri_scale,           0, 5, 1, 1)
        self.add(grid)

    def ping_menuitem_selected(self, ping_menuitem):
        if self.ping_menuitem:
            for lamp in lamp_dict.values():
                hl_obj = globals()[lamp]
                hl_obj.alert_set(1)

    def blink_menuitem_selected(self, blink_menuitem):
        if self.blink_menuitem:
            for lamp in lamp_dict.values():
                hl_obj = globals()[lamp]
                hl_obj.alert_set(2)

    def stop_blinking_menuitem_selected(self, stop_blinking_menuitem):
        if self.stop_blinking_menuitem:
            for lamp in lamp_dict.values():
                hl_obj = globals()[lamp]
                hl_obj.alert_set(0)

    def quit_menuitem_selected(self, quit_menuitem):
        app.quit()

    def on_off_switch_set_state(self):
        for lamp in lamp_dict.values():
            hl_obj = globals()[lamp]
            if hl_obj.on_off_state() == "on":
                self.on_off_switch.set_active(True)
            else:
                self.on_off_switch.set_active(False)

    def on_off_switch_activated(self, switch, active):
        for lamp in lamp_dict.values():
            hl_obj = globals()[lamp]
            if self.on_off_switch.get_active():
                hl_obj.on_off_switch(1)
            else:
                hl_obj.on_off_switch(0)

    #def mir_spinbutton_changed(self, mir_spinbutton):
    #    print("mir_SpinButton value: %i" % (mir_spinbutton.get_value_as_int()))

    #def bri_spinbutton_changed(self, bri_spinbutton):
    #    print("bri_SpinButton value: %i" % (bri_spinbutton.get_value_as_int()))

    def mir_scale_set_state(self):
        for lamp in lamp_dict.values():
            hl_obj = globals()[lamp]
            val = hl_obj.mired_get()
            self.mir_scale.set_value(val)

    def mir_scale_moved(self, mir_scale):
        for lamp in lamp_dict.values():
            hl_obj = globals()[lamp]
            hl_obj.mired_set(int(mir_scale.get_value()))

    def bri_scale_set_state(self):
        for lamp in lamp_dict.values():
            hl_obj = globals()[lamp]
            val = hl_obj.brightness_get()
            self.bri_scale.set_value(val)

    def bri_scale_moved(self, bri_scale):
        for lamp in lamp_dict.values():
            hl_obj = globals()[lamp]
            hl_obj.brightness_set(int(bri_scale.get_value()))


class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)

app = MyApplication()
exit_status = app.run(sys.argv)

for lamp in lamp_dict.values():
    hl_obj = globals()[lamp]
    hl_obj.prop_chg_notify.kill()

sys.exit(exit_status)










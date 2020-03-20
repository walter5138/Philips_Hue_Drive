#!/usr/bin/env python3

import sys, os
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
        #self.set_default_size(40, 40)
        self.set_border_width(10)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.settings = Gtk.Settings.get_default()
        self.settings.set_property("gtk-application-prefer-dark-theme", True)
        
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title = "Philips Hue Drive"
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
        lamp_dict_mi = Gtk.MenuItem(label="show lamp_dict")
        lamp_dict_mi.connect('activate', self.lamp_dict_mi_selected)
        admin_submenu.append(lamp_dict_mi)
        quit_mi = Gtk.MenuItem(label="Quit")
        quit_mi.connect('activate', self.quit_menuitem_selected)
        admin_submenu.append(quit_mi)


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
            
            dynamic_grid = Gtk.Grid()
            
            mir_label = Gtk.Label()
            mir_label.set_text("mired")

            mir_adjust = Gtk.Adjustment(value=326, lower=153, upper=500, step_increment=20, page_increment=20, page_size=0)

            mir_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=mir_adjust)
            mir_scale.set_value_pos(Gtk.PositionType.RIGHT)
            mir_scale.set_value(hl_obj.mired_get())
            mir_scale.set_digits(0)
            mir_scale.set_hexpand(True)
            mir_scale.set_vexpand(False)
            mir_scale.connect("value-changed", self.mir_scale_moved, hl_obj)


            col_label = Gtk.Label()
            col_label.set_text("color")

            col_adjust = Gtk.Adjustment(value=326, lower=153, upper=500, step_increment=20, page_increment=20, page_size=0)

            col_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=col_adjust)
            col_scale.set_value_pos(Gtk.PositionType.RIGHT)
            #col_scale.set_value(hl_obj.color_get())
            col_scale.set_digits(0)
            col_scale.set_hexpand(True)
            col_scale.set_vexpand(False)
            #col_scale.connect("value-changed", self.mir_scale_moved, hl_obj)


            bri_label = Gtk.Label()
            bri_label.set_text("brightness")

            bri_adjust = Gtk.Adjustment(value=126, lower=1, upper=254, step_increment=10, page_increment=10, page_size=0)

            bri_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=bri_adjust)
            bri_scale.set_value_pos(Gtk.PositionType.RIGHT)
            bri_scale.set_value(hl_obj.brightness_get())
            bri_scale.set_digits(0)
            bri_scale.set_hexpand(True)
            bri_scale.set_vexpand(False)
            bri_scale.connect("value-changed", self.bri_scale_moved, hl_obj)


            tra_label = Gtk.Label()
            tra_label.set_text("transitiontime")

            tra_adjust = Gtk.Adjustment(value=1, lower=0, upper=4, step_increment=1, page_increment=1, page_size=0)

            tra_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=tra_adjust)
            tra_scale.set_value_pos(Gtk.PositionType.RIGHT)
            tra_scale.set_value(hl_obj.transitiontime_get())
            tra_scale.set_digits(0)
            tra_scale.set_hexpand(True)
            tra_scale.set_vexpand(False)
            tra_scale.connect("value-changed", self.tra_scale_moved, hl_obj)



            lamp_label = Gtk.Label()
            lamp_label.props.halign = Gtk.Align.START
            lamp_label.set_text(lamp)

            on_off_switch = Gtk.Switch()
            on_off_switch.props.valign = Gtk.Align.CENTER
            on_off_switch.props.halign = Gtk.Align.END
            on_off_switch.set_tooltip_text("Off <> On")
            if hl_obj.on_off_state() == "on":
                on_off_switch.set_active(True)
            else:
                on_off_switch.set_active(False)
            on_off_switch.connect("notify::active", self.on_off_switch_activated, hl_obj)

            lamp_menu_button = Gtk.MenuButton()
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("/home/walter/bluetooth/hue/hue_ble_gtk/bulb_icon.jpg", 28, 28, preserve_aspect_ratio=True)
            image = Gtk.Image.new_from_pixbuf(pixbuf)
            lamp_menu_button.add(image)
            lamp_menu_button.props.halign = Gtk.Align.START

            lamp_menu = Gtk.Menu()
            lamp_menu_button.set_popup(lamp_menu)

            admin_menu_item = Gtk.MenuItem(label="Hue Admin")
            lamp_menu.append(admin_menu_item)

            admin_submenu = Gtk.Menu()
            admin_menu_item.set_submenu(admin_submenu)
        
            menuitem = Gtk.MenuItem(label="set bulb name")
            admin_submenu.append(menuitem)

            transitiontime_cmi = Gtk.CheckMenuItem(label="transitiontime")
            transitiontime_cmi.connect("activate", self.transitiontime_cmi_selected, hl_obj, dynamic_grid, tra_label, tra_scale)
            admin_submenu.append(transitiontime_cmi)


            fun_menu_item = Gtk.MenuItem(label="Hue Fun")
            lamp_menu.append(fun_menu_item)

            fun_submenu = Gtk.Menu()
            fun_menu_item.set_submenu(fun_submenu)

            mired_rmi= Gtk.RadioMenuItem(label="mired")
            mired_rmi.connect("toggled", self.mired_rmi_selected, hl_obj, dynamic_grid, lamp_label, mir_label, mir_scale, col_label, col_scale)
            mired_rmi.set_active(True)
            fun_submenu.append(mired_rmi)
            color_rmi= Gtk.RadioMenuItem(label="color", group=mired_rmi)
            fun_submenu.append(color_rmi)
            brightness_cmi = Gtk.CheckMenuItem(label="brightness")
            brightness_cmi.connect("activate", self.brightness_cmi_selected, hl_obj, dynamic_grid, bri_label, bri_scale, on_off_switch, lamp_menu_button)
            brightness_cmi.set_active(True)
            fun_submenu.append(brightness_cmi)

            lamp_menu.show_all()

            dynamic_grid.set_border_width(0)
            dynamic_grid.set_column_homogeneous(True)
            #dynamic_grid.set_row_homogeneous(False)
            #dynamic_grid.set_column_spacing(40)
            #dynamic_grid.set_row_spacing(40)

            self.vbox.pack_start(dynamic_grid, False, False, 0)

        self.add(self.vbox)

    def lamp_dict_mi_selected(self, widget):
        message_dialog = Gtk.MessageDialog(parent=self, modal=True, destroy_with_parent=True, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.CLOSE, text="This shows the lamp_dict.")
        #message_dialog.set_decorated(False)
        message_dialog.set_title("lamp_dict")
        message_dialog.format_secondary_text("The lamp_dict shows the Bulbs recognized \nby the Philips Hue Drive App.\n\n%s" % str(lamp_dict))
        message_dialog.connect("response", self.dialog_response)
        message_dialog.show()
    def dialog_response(self, widget, response_id):
        if response_id == Gtk.ResponseType.CLOSE:
            widget.destroy()

    def on_off_switch_activated(self, widget, active, hl_obj):
        if widget.get_active():
            hl_obj.on_off_switch(1)
        else:
            hl_obj.on_off_switch(0)

    def mir_scale_moved(self, mir_scale, hl_obj):
        hl_obj.mired_set(int(mir_scale.get_value()))

    def bri_scale_moved(self, bri_scale, hl_obj):
        hl_obj.brightness_set(int(bri_scale.get_value()))

    def tra_scale_moved(self, tra_scale, hl_obj):
        hl_obj.transitiontime_set(int(tra_scale.get_value()))

    def quit_menuitem_selected(self, widget):
        app.quit()

    def mired_rmi_selected(self, widget, hl_obj, dynamic_grid, lamp_label, mir_label, mir_scale, col_label, col_scale):
        if widget.get_active():
            dynamic_grid.remove_row(0)
            dynamic_grid.insert_row(0)
            dynamic_grid.attach(lamp_label,               0, 0, 1, 1)
            dynamic_grid.attach(mir_label,                1, 0, 1, 1)
            dynamic_grid.attach(mir_scale,                2, 0, 1, 1)
            dynamic_grid.show_all()
        else:
            dynamic_grid.remove_row(0)
            dynamic_grid.insert_row(0)
            dynamic_grid.attach(lamp_label,               0, 0, 1, 1)
            dynamic_grid.attach(col_label,                1, 0, 1, 1)
            dynamic_grid.attach(col_scale,                2, 0, 1, 1)
            dynamic_grid.show_all()

    def brightness_cmi_selected(self, widget, hl_obj, dynamic_grid, bri_label, bri_scale, on_off_switch, lamp_menu_button):
        if widget.get_active():
            dynamic_grid.remove_row(1)
            dynamic_grid.insert_row(1)
            dynamic_grid.attach(on_off_switch,            0, 1, 1, 1)
            dynamic_grid.attach(lamp_menu_button,         0, 1, 1, 1)
            dynamic_grid.attach(bri_label,                1, 1, 1, 1)
            dynamic_grid.attach(bri_scale,                2, 1, 1, 1)
            dynamic_grid.show_all()
        else:
            dynamic_grid.remove_row(1)
            dynamic_grid.insert_row(1)
            dynamic_grid.attach(on_off_switch,            0, 1, 1, 1)
            dynamic_grid.attach(lamp_menu_button,         0, 1, 1, 1)
            dynamic_grid.show_all()
            
    def transitiontime_cmi_selected(self, widget, hl_obj, dynamic_grid, tra_label, tra_scale):
        if widget.get_active():
            dynamic_grid.attach(tra_label,                1, 2, 1, 1)
            dynamic_grid.attach(tra_scale,                2, 2, 1, 1)
            dynamic_grid.show_all()
        else:
            dynamic_grid.remove_row(2)
            self.resize(420, 90)



#    def __init__(self):
#
#        Gtk.Window.__init__(self)
#        self.set_border_width(10)
#        self.set_position(Gtk.WindowPosition.MOUSE)
#
#        self.hb = Gtk.HeaderBar()
#        self.hb.set_show_close_button(True)
#        self.hb.props.title = "Philips Hue Drive: Admin"
#        self.set_titlebar(self.hb)
#
#        hue_button = Gtk.Button()
#        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("/home/walter/bluetooth/hue/hue_ble_gtk/bulb_icon.jpg", 40, 40, preserve_aspect_ratio=True)
#        image = Gtk.Image.new_from_pixbuf(pixbuf)
#        hue_button.add(image)
#        self.hb.pack_start(hue_button)
#
#        self.show_all()



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




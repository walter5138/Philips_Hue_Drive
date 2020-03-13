#!/usr/bin/env python3

import dbus

systembus = dbus.SystemBus()

o_manager = dbus.Interface(systembus.get_object('org.bluez', '/'), 'org.freedesktop.DBus.ObjectManager') 
m_objects = o_manager.GetManagedObjects()

lamp_dict = {}

for obj_paths, obj_dict in m_objects.items():
    if "org.bluez.Device1" in obj_dict.keys():
        for interface, properties in obj_dict.items():
            if "Hue Lamp" in properties.values():
                for property, value in properties.items():
                    if property == "Address":
                        v = str(value)
                        x = v.replace(":", "_")
                    if property == "Alias":
                        y = str(value)
                lamp_dict[x] = y 

lamp_dict
#print(lamp_dict)
#lamp_dict = {'D8_3D_2A_15_BE_EE': 'lamp_kitchen', 'C3_95_FE_4E_96_7A': 'lamp_livingroom', 'D1_8D_C3_D5_5E_2F': 'lamp_homeoffice'}

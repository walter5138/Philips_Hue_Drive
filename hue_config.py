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
                for prop, value in properties.items():
                    if prop == "Address":
                        v = str(value)
                        x = v.replace(":", "_")
                    if prop == "Alias":
                        y = str(value)
                lamp_dict[x] = y 

lamp_dict

#print(lamp_dict)

#lamp_dict = {'D8_3D_2A_15_BE_EE': 'lamp_kitchen', 'C3_95_FE_4E_96_7A': 'lamp_livingroom', 'E0_B0_D8_EC_C7_66': 'lamp_homeoffice'}
#lamp_dict = {'D8_3D_2A_15_BE_EE': 'lamp_kitchen', 'E0_B0_D8_EC_C7_66': 'lamp_homeoffice'}
#lamp_dict = {'D8_3D_2A_15_BE_EE': 'lamp_kitchen', 'C3_95_FE_4E_96_7A': 'lamp_livingroom'}
#lamp_dict = {'C3_95_FE_4E_96_7A': 'lamp_livingroom', 'E0_B0_D8_EC_C7_66': 'lamp_homeoffice'}
#lamp_dict = {'E0_B0_D8_EC_C7_66': 'lamp_homeoffice'}

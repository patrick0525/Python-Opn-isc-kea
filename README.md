# Python-Opn-isc-kea (opnsense_isc_to_kea_reservations.py)

A xml migration of the isc-dhcp static leases to kea-dhcp reservations.

Reads the config-OPNsense*.xml file into a 
opnsense xml -> array of [json obj] -> opnsense xml

The output is merge.xml

Update:
Inital commit
    Add new random uuid per reservation
    Re-use subnet uuid for additional reservations

02232024
    Validate opnsense xml tag
    Validate inital kea reservation is missing
    Vslidate if reservation's uuid value is empty 












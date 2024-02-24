# Python-Opn-isc-kea (opnsense_isc_to_kea_reservations.py)

A xml migration of isc-dhcp static leases to kea-dhcp reservations.

Reads the config-OPNsense*.xml file into a 
isc xml -> array of [json obj] -> kea xml

The output is a merge.xml that re-loads and re-boots opnsense.

Updates:
Inital commit
    Migrate existing isc data into kea reservations
    Create new random uuid per reservation
    Re-use subnet uuid for additional reservations

02232024
    Validate opnsense xml tag
    Validate existence of inital kea reservation
    Validate if reservation's uuid value exist
    For invalid uuid use cases. Create a merge.xml
    that contain warning data.
     
















# Python-Opn-isc-kea (opnsense_isc_to_kea_reservations.py)

A xml migration of isc-dhcp static leases to kea-dhcp reservations.

Reads the config-OPNsense*.xml file into a 
isc xml -> into an array of [json obj] -> kea xml
-> merged back to config-OPNsense*.xml -> saved as merge.xml

Requires: System Configuration Restore of merge.xml.

Updates:
Inital commit
    Migrate existing isc static lease data into kea reservations
    Create a new random uuid per kea reservation
    Re-uses subnet uuid for all reservations

02232024
    Validate opnsense file using <opnsense> xml
    Validate existence of inital kea reservation
    Validate if reservation's uuid value exist
    For invalid uuid use cases, the merge.xml
    contains a <uuid> warning "YOU NEED TO CREATE 
    A VALID KEA RESERVATION"
    
02242024
    Terminates opnsense_isc_to_kea_reservations.py
    if <opnsense> tag is missing

     
















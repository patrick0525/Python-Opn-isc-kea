# Python-Opn-isc-kea (opnsense_isc_to_kea_reservations.py)

A xml migration of isc-dhcp static leases to kea-dhcp reservations.

Reads the config-OPNsense*.xml file -> into an
isc xml -> into an array of [json obj] -> into a kea xml
-> merges back to config-OPNsense*.xml -> saved as merge.xml
 (Original config-OPNsense*.xml remains unmodified)

Requires: System Configuration Restore of merge.xml.

Updates:

02172024 (inital commit)
02252024
   - Migrate existing isc static lease data into kea reservations
    - Create a new random \<reservation uuid> per kea reservation
    - Reuses existing kea subnet \<uuid> for all reservations: \<reservation uuid>

02232024
    - Validate opnsense file using \<opnsense> tag
    - Validate existence of inital kea \<reservation uuid> tag
    - Validate if reservation's uuid.text value exists
    - For invalid uuid use cases, the merge.xml
    contains a \<uuid> warning "YOU NEED TO CREATE 
    A VALID KEA RESERVATION"
    
02242024
    - Terminates opnsense_isc_to_kea_reservations.py
    if \<opnsense> tag is missing

02252024
   - Command line argument support and file name regex format matching

     opnsense_isc_to_kea_reservations.py [config-OPNsense*.xml]

     
















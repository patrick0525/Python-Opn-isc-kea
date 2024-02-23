# Python-Opn-isc-kea (opnsense_isc_to_kea_reservations.py)

An xml conversion/migration of opnsense from isc-dhcp static lease to kea-dhcp reservation.

Reads the config-OPNsense*.xml file into
opnsense xml -> array of [json obj] -> opnsense xml

opnsense kea-dhcp xml -adds new random uuid per device and re-uses users' subnet uuid

The output is merge.xml

Restore merge.xml and reboot

Done

# Python-Opn-isc-kea

An .xml conversion of opnsense from isc-dhcp static lease to kea-dhcp reservation.

Reads the conig-OPNsense*.xml file into
opnsense xml -> array of [json obj] -> opnsense xml

opnsense kea-dhcp xml -add new random uuid per device; re-used users' subnet uuid

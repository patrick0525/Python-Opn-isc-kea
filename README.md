# Python-Opn-isc-kea

An .xml conversion of opnsense from isc-dhcp static lease to kea-dhcp reservation.

Reads the config-OPNsense*.xml file into
opnsense xml -> array of [json obj] -> opnsense xml

opnsense kea-dhcp xml -adds new random uuid per device; re-uses users' subnet uuid

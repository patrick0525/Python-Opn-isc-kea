8:00AM
Problem Statement: 
Choosing the new kea-dhcp feature in opnsense 24.1 does not automatically migrate 
the isc-dhcp static leases as the kea-dhcp reservations. 
The intent of the python script is to patch an existing opnsense config already 
configured with at least one existing kea-dhcp reservation. Identifying and re-using the 
<subnet> uuid is required and user needs one kea reservation prior to 
executing opnsense_isc_to_kea_reservations.py 
Hopefully users will find it useful and prevent manual Gui data entry.


Prerequisites:
Python Code developed on a Windons and tested on W11 directories. (Python 3.12)
Basic Python knowledge
Optional: Notepad ++


Overview of Processing:
This python script converts config-OPNsense.localdomain-20240218111111.xml 
into a json array of static release objects which is then further converted 
into a output file containing a new section of kea-dhcp format delimited by <reservations>.
For every device in kea-dhcp, the python script will generate a new random 
uuid for every device and re-uses the user's <subnet> uuid.

See below:

      </reservations>
          <reservation uuid="6a688941-02f8-46aa-abc6-8121fa434809">
            <subnet>7046c7cb-a9fb-4a50-8a49-3b6e77d42809</subnet>
            <ip_address>192.168.1.100</ip_address>
            <hw_address>90:a1:b1:c1:d1:e11</hw_address>
            <hostname/>
            <description/>
       </reservations>
	   
	   
Sample Test Run on an exiting opnsense config:	   
Copy opnsense_isc_to_kea_reservations.py and 
config-OPNsense.localdomain-20240218111111.xml 
and config-OPNsense.localdomain-20240218000000.xml
into the same directory.

>>  python3 opnsense_isc_to_kea_reservations.py

Creates 
opnsense_isc_static_lease.json
opnsense_isc_static_lease_converted_to_kea_reservation.xml
merge.xml is the new config file that constains the new kea rservations

Try the beyond compare app to see the differences

Adding the kea reservation patch to the user's opnsense config file:
In the opnsense GUI, create and add a device in the kea-dhcp 
reservation tab and apply save. You have just created an uuid 
for the subnet. Save this config file. Opnsense admin: In the the *.py search 
[ADD YOUR CONFIG] and change input_file equal to 
your config-OPNsense.localdomain-2024*.xml Comment out the previous *.xml

>>  python3 opnsense_isc_to_kea_reservations.py

Creates 
opnsense_isc_static_lease.json
opnsense_isc_static_lease_converted_to_kea_reservation.xml
merge.xml is the new config file that constains the new kea rservations
 

Restore merge.xml and reboot

Update 02252024:
	Command line argument support and file name regex format matching
	>>  python3 opnsense_isc_to_kea_reservations.py [config-OPNsense*.xml]



Done

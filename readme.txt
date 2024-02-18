8:00AM
Problem Statement: 
Choosing the new kea-dhcp feature in opnsense 24.1 does not automatically migrate 
the isc-dhcp static leases to the kea-dhcp reservations. 
The intent of the python script is to patch an existing opnsense config already 
configured with at least one existing kea-dhcp reservation. Identifying and re-using the 
<subnet> uuid is required and needs to be added to the opnsense_isc_to_kea_reservations.py
to successfully create all the kea reservations. 
Hopefully users will find it useful and prevent manual Gui data entry.


Prerequisites:
Python Code developed on a Windons and tested on W11 directories. (Python 3.12)
Basic Python knowledge
Optional: Notepad ++


Overview of Processing:
This python script converts config-OPNsense.localdomain-20240218111111.xml 
into a kea-dhcp reservation(.xml)format adjunct file. The input .xml will be converted 
into a json array of static release objects which is then further converted 
into a output file containing a new section of kea-dhcp format delimited by <reservations>.
For every device in kea-dhcp, the python script will generate a new random 
uuid for every device and re-use the user's identified <subnet> uuid.

See below:

      </reservations>
          <reservation uuid="6a688941-02f8-46aa-abc6-8121fa434809">
            <subnet>7046c7cb-a9fb-4a50-8a49-3b6e77d42809</subnet>
            <ip_address>192.168.1.100</ip_address>
            <hw_address>90:a1:b1:c1:d1:e11</hw_address>
            <hostname/>
            <description/>
       </reservations>
	   
	   
Sample Test Run on an opnsense config:	   
Copy opnsense_isc_to_kea_reservations.py and 
config-OPNsense.localdomain-20240218111111.xml
into the same directory.

>>  python3 opnsense_isc_to_kea_reservations.py

Creates 
opnsense_isc_static_lease.json
opnsense_isc_static_lease_converted_to_kea_reservation.xml


Adding the patch to the opnsense config file:
In the opnsense GUI, create and add a device in the kea-dhcp reservation tab and apply save.
You have just created an uuid for the subnet. Save this  config file, open an editor
to identify your <subnet> unique uuid  </subnet>.
 
Edit the opnsense_isc_to_kea_reservations.py and add your unique subnet uuid. 
In the same directory run the modified opnsense_isc_to_kea_reservations.py and your current
config-OPNsense.localdomain-2024*.xml that contains your isc-dhcp static leases.
The *.py script will generate a new kea-dhcp format file as
opnsense_isc_static_lease_converted_to_kea_reservation.xml.

Cut and paste the new reservation .xml adjunct file into the existing kea-dhcp section of
your current config-OPNsense.localdomain-2024*.xml. Restore confg xml and reboot.

Done

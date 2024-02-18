# opnsense_isc_to_kea_reservations.py
# Initial Input opnsense_isc_dhcp_static_lease_data.xml
# Final Output opnsense_isc_static_lease_converted_to_kea_reservations.xml
# Module  are provided by python use pip to install 
import json
import uuid
import os
import xmltodict
import numpy as np

def convert_to_list(obj):
    obj_list = []
    for i in range(len(obj)):
        if i not in obj:
            return obj  # Return original dict if not an ordered list
        obj_list.append(obj[i])
    return obj_list


# Convert pfsense xml to json array of ojects
# Input  opnsense_isc_dhcp_static_lease_data.xml
# Output opnsense_isc_static_lease.json
def pfsense_xml_to_json(path,input,output):

    # open the input xml file and read
    # data into a python dictionary 
    # using xmltodict module

    input_file = os.path.join(path,input)
    print("Convert xml ", input_file, "to json objects")
    print("Output needs to be a single json array containing json objects")
    print("Format: [{object1},{object2},{object3}]")

    isExist = os.path.exists(input_file)
    print ("The input file exists:", isExist)

    with open (input_file) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())	
    # Clean-up the nested array 
    # and get to the dhcpd value
    long_list = (list(data_dict.values()))
    # print(long_list)
    # print("\n")

    # get to staticmap
    short_list = long_list[0]
    # print(short_list)
    # print("\n\n")

    # get to staticmap(key): json objects (values)
    # Need at least two isc dhco static leases in the .xml    
    inner_list = short_list['dhcpd']['lan']['staticmap']
    # print("\n")
    # print(inner_list)


    # Convert the dictionary to a json string with indentation 
    json_str = json.dumps(inner_list, indent=4)
    ##json_str = json.dumps(long_list, indent=4)
    # print (json_str)

    # Write only a json array to a file. If a single object put it into an array
    if isinstance(inner_list, dict) and 'mac' in inner_list:
        # make an array to hold one json object
        temp_list = [inner_list]
        print("This is an object\n")
        # print(temp_list)   
        json_str = json.dumps(temp_list, indent=4)
    else:
        # loads an array
        print("This is an array \n")
        
    # Test output
    print(json_str)
    
    # Specify the path to the output file 
    #output_file = rf'C:\Users\patri\Documents\python\GitHub3\opnsense_isc_static_lease.json'
    output_file = os.path.join(path,output)
    # Save the json representation of the structure 
    with open(output_file, 'w') as f: 
        # Write the JSON string to the file 
        f.write(json_str)
        
    # Print a confirmation message with the output file path 
    print("\njson saved to", output_file,"\n")


# Convert json array of ojects to opnsense xml
# Input  opnsense_isc_static_lease.json
# Output opnsense_isc_static_lease_converted_to_kea_reservations.xml
def json_to_opnsense_xml(path,input,output):
    # when json null appears it is set None which produces white space in the .xml
    null = None
    # input_file = open(rf'C:\Users\patri\Documents\python\GitHub3\opnsense_isc_static_lease.json', 'r')
    file = os.path.join(path,input)
    input_file = open(file, 'r')
         
    # loads only an array
    json_decode = json.load(input_file)
    
    # output_file = open(r'C:\Users\patri\Documents\python\GitHub3\opnsense_isc_static_lease_converted_to_kea_reservations.xml', 'w')
    output_file = os.path.join(path,output)
    output_file = open(output_file, 'w')
    result = []
    for item in json_decode:
        my_dict={}
        my_dict['mac']=item.get('mac')
        my_dict['ipaddr']=item.get('ipaddr')
        my_dict['hostname']=item.get('hostname')
        my_dict['descr']=item.get('descr')
    
        u = str(uuid.uuid4())
        #print (u)
    
        str1 =          "<reservations>\n"
    
        str2 =          "<reservation uuid=\""
        str2a =         "\">\n"
    
        #Identify subnet use static uuid
        str3 =          "<subnet>4e3016b1-b603-44bd-a361-b33c44333c98</subnet>\n"
    
        str4 =          "<ip_address>"
        str4a =         "</ip_address>\n"
    
        str5 =          "<hw_address>" 
        str5a =         "</hw_address>\n"
    
        str6 =          "<hostname>"
        str6a =         "</hostname>\n"
    
        str7 =          "<description>" 
        str7a =         "</description>\n"
    
        str8 =          "</reservation>\n"
        str9 =          "</reservations>\n"
    
        # write to file by looping
    
        #output_file.writelines(f"{'':>7}{str1}")

        output_file.writelines(f"{'':>10}{str2}{u}{str2a}")
        output_file.writelines(f"{'':>12}{str3}")
        output_file.writelines(f"{'':>12}{str4}{my_dict['ipaddr']}{str4a}")
        output_file.writelines(f"{'':>12}{str5}{my_dict['mac']}{str5a}")
    
        if (my_dict['hostname']== null):
            # end
            output_file.writelines(f"{'':>12}<hostname/>\n")
        else:
            # add info
            output_file.writelines(f"{'':>12}{str6}{my_dict['hostname']}</hostname>\n")
        # description
        if (my_dict['descr']== null):
            # end    
            output_file.writelines(f"{'':>12}<description/>\n")  
        else:
            # add info
            output_file.writelines(f"{'':>12}{str7}{my_dict['descr']}</description>\n")
        
        output_file.writelines(f"{'':>10}{str8}")
    
        #output_file.writelines(f"{'':>7}{str9}")

    # Close file
    output_file.close()

    # Checking if the data is written to file or not
    # display_output_file = rf'C:\Users\patri\Documents\python\GitHub3\opnsense_isc_static_lease_converted_to_kea_reservations.xml'
    # output_file = open(r'C:\Users\patri\Documents\python\GitHub3\opnsense_isc_static_lease_converted_to_kea_reservations.xml', 'r')
    display_output_file = os.path.join(path,output)
    output_file = open(display_output_file, 'r')
    
    print(output_file.read())
    output_file.close() 

    # Print a confirmation message with the output file path 
    print("Opnsense kea-dhcp xml saved to",display_output_file)



# Change working path
os.chdir(rf'C:\\Users\\patri\\Documents\\python\\GitHub3')
entry_path = (os.getcwd())

# Read pfsense config xml

# one static release
input_file  = "config-OPNsense.localdomain-20240218000000.xml"

# multiple static releases
#input_file  = "config-OPNsense.localdomain-20240218111111.xml"

output_file = "opnsense_isc_static_lease.json"
print("pfsense_xml_to_json\n[Path]                             Input File                  Output file")
print(entry_path,input_file,output_file,"\n")
pfsense_xml_to_json(entry_path,input_file,output_file)

# Output opnsense config xml
input_file  = "opnsense_isc_static_lease.json"
output_file = "opnsense_isc_static_lease_converted_to_kea_reservations.xml"
print("json_to_opnsense_xml\n[Path]                              Input File                  Output file")
print(entry_path,input_file,output_file,"\n")
json_to_opnsense_xml(entry_path,input_file,output_file)
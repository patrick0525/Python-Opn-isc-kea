# Copyright 2024 Patrick Moy (02/23/2024)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##############################################################################


# opnsense_isc_to_kea_reservations.py
#
# opnsense admin: copy opnsense_isc_to_kea_reservations.py and the two input_file
# into a directory
# input_file: config-OPNsense.localdomain-20240218111111.xml (This *.py uses this as a default)
# input_file: config-OPNsense.localdomain-20240218000000.xml
#
# >>>> python3 opnsense_isc_to_kea_reservations.py
#
# >>>>>> TO MODIFY YOUR opnsense CONFIG <<<<<<
# opnsense admin: Search for [ADD YOUR CONFIG] and change input_file and add 
# your config-OPNsense.localdomain-2024*.xml. Comment out the previous *.xml
# Re-run opnsense_isc_to_kea_reservations.py
#
# merge_file: merge.xml
# Module  are provided by python use pip to install 

import json
import uuid
import os
import sys
import xmltodict
import xml.etree.ElementTree as ET
#import lxml.etree as etree

# checking subnet uuid len and does it exist 
def has_len(obj):
    return hasattr(obj, '__len__')

# find subnet uuid from a working kea reservation in the input_file
def find_subnet_uuid(root_name):
    first_time = False
    for item in root_name.findall('.//subnet'):
    
        # Testing for missing uuid - False condition only
        if ( (has_len(item.text)) == False):
            print("WTF! Missing a valid kea subnet uuid. \nCheck config-OPNsense.localdomain-2024*.xml\n")
            item.text = "YOU NEED TO CREATE A VALID KEA RESERVATION"
            return item.text
            
        # uusi must char len =36
        if ((len(item.text) == 36) and (first_time == False)):
            print("Call find_subnet_uuid(): ", item.text)
            first_time = True
    return (item.text)    

# Convert json array of objects to a kea xml
# Input     opnsense_isc_static_lease.json
# Output opnsense_isc_static_lease_converted_to_kea_reservations.xml
#
# a kea reservation xml
#                   <reservation uuid="bd774270-c81d-468f-a0a4-26bba4d150d3">
#						<subnet>b2d692fb-fd9d-4bf7-84b7-eac29cca1692</subnet>
#						<ip_address>10.59.11.101</ip_address>
#						<hw_address>a1:b1:c1:d1:e1:f1</hw_address>
#						<hostname>DAD-DESKTOP</hostname>
#						<description>DAD-DESKTOP</description>
#					</reservation>

def json_to_opnsense_xml(path,input,output):
    
    file = os.path.join(path,input)
    input_file = open(file, 'r')

    # loads only a json array
    json_decode = json.load(input_file)
      
    r = ET.Element("reservations")
    for item in json_decode:
        
        # set reservation uuid
        reservation = ET.SubElement(r,"reservation")
        reservation.set('uuid',str(uuid.uuid4()))
    
        # get subnet uuid from the 1st kea reservation       
        temp = find_subnet_uuid(root1)
        print("---->", temp)
        if ((len(temp) < 36)):
           print("WTF! Missing a valid kea subnet uuid. \nCheck config-OPNsense.localdomain-2024*.xml\n")
           ET.SubElement(reservation,"subnet").text = "YOU NEED TO CREATE A VALID KEA RESERVATION"
        else:
           # Valid char len 36 subnet uuid, value and format
           ET.SubElement(reservation,"subnet").text = find_subnet_uuid(root1)
            
            
        # get info from json file
        ET.SubElement(reservation,"ip_address").text = str(item["ipaddr"])
        ET.SubElement(reservation,"hw_address").text = str(item["mac"])
        ET.SubElement(reservation,"hostname").text = str(item["hostname"])
        ET.SubElement(reservation,"description").text = str(item["descr"])

        kea_xml = ET.ElementTree(r)
        kea_xml.write(output)

    # Make 'Pretty' xml  
    tree = ET.parse(output)
    root = tree.getroot()
    ET.indent(tree, space="\t", level=0)
    print("\n", ET.tostring(root, encoding='utf8').decode('utf8'))

    # Save the pretty xml file 
    tree.write(output, xml_declaration=True, encoding='utf-8', method="xml")

    # Checking if the data is written to file or not
    output_file = os.path.join(path,output)
    read_output_file = open(output_file, 'r')
    print("\nchecking populated kea file for added reservations: \n")
    print(read_output_file.read())
    read_output_file.close()

    # Print a confirmation message with the output file path
    print("\nopnsense kea-dhcpd xml saved to",output_file,"\n\n")


# Convert config-OPNsense*.xml to json array of objects
# Input  config-OPNsense*.xml
# Output opnsense_isc_static_lease.json
#
#  a json array
# [
#    {
#        "mac": "a1:b1:c1:d1:e1:f1",
#        "ipaddr": "10.59.11.101",
#        "hostname": "DAD-DESKTOP",
#        "descr": "DAD-DESKTOP",
#        "winsserver": null,
#        "dnsserver": null,
#        "ntpserver": null
#    }
#]
def opnsense_xml_to_json(path,input,output):

    # open the input xml file and read
    # data into a python dictionary 
    # using xmltodict module

    input_file = os.path.join(path,input)
    print("Convert xml ", input_file, "to json objects")
    print("Output needs to be a single json array containing json objects")
    print("Format: [{object1},{object2},{object3}]")

    # Does the file exist
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
    #print("The...",short_list)
    # print("\n\n")

    
    # get to staticmap(key): json objects (values)
    # Need at least one isc dhcpd static leases in the xml    
    inner_list = short_list['dhcpd']['lan']['staticmap']
    #print("\n")
   
    # Convert the dictionary to a json string with indentation 
    json_str = json.dumps(inner_list, indent=4)
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
    print("Print json file. \n", json_str)
    
    # Specify the path to the output file 
    #output_file = rf'C:\Users\patri\Documents\python\GitHub4\opnsense_isc_static_lease.json'
    output_file = os.path.join(path, output)
    # Save the json representation of the structure 
    with open(output_file, 'w') as f: 
        # Write the JSON string to the file 
        f.write(json_str)
        
    # Print a confirmation message with the output file path 
    print("\njson saved to", output_file,"\n")


# Merge the original xml with the kea reservationabtion xml
def merge_files(entry_pathpath, input_file, kea_output_file, merge_file):
    print("Start -> Merge the xml files together")
    #print("doc1_file\n")
    #input_file = "config-OPNsense.localdomain-20240218111111.xml"
    # read config-OPNsense*.xml
    file1_path = os.path.join(entry_path, input_file)
    tree1 = ET.parse(file1_path)
    root1= tree1.getroot()
    print(file1_path)

    # read kea reservations xml
    #print("doc2_file\n")
    #kea_output_file = "opnsense_isc_static_lease_converted_to_kea_reservations.xml"
    file2_path = os.path.join(entry_path,kea_output_file)
    tree2 = ET.parse(file2_path)
    root2 = tree2.getroot()
    print(file2_path)

    # Merge file name is doc3_file
    #print("doc3_file\n")
    doc3_file = merge_file
    file3_path = os.path.join(entry_path,doc3_file)
    #print(file3_path)

    # Insert the one reservation from doc2_file into the doc1_file
    for item in root2.findall('reservation'):
        #print("found",item)
    
        # goto 1st doc1_file xml and find insertion field <reservations>
        #  and loop through doc2_file by inserting each reservation
        target = root1.find('.//reservations')    
        target.insert(0,item)
    
    # make xml pretty using correct idention    
    ET.indent(tree1, space="\t", level=0)

    # Save the merged xml file
    tree1.write(file3_path, xml_declaration=True, encoding='utf-8', method="xml")

    print("\nDone...the merged changes are in ",file3_path,"\n")


########################  Main  ########################

# Change working path to where the *.py is executing from
script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) 
print("The working path:", script_directory)
os.chdir(script_directory)
entry_path = (os.getcwd())

# Read opnsense cong file:  config-OPNsense*.xml
# Creates a isc-dhcpd static lease json file
#
#===================   [ADD YOUR CONFIG] SEE BELOW   ================================
#   NOTE: Each xml shall have one kea reservation
# one static release
#input_file  = "config-OPNsense.localdomain-20240218000000.xml"
#
# multiple static releases
input_file  = "config-OPNsense.localdomain-20240218111111.xml"
# input_file  = "[ADD YOUR CONFIG].xml"
#======================================================================
#
output_file = "opnsense_isc_static_lease.json"
print("Call opnsense_xml_to_json() \n[Path]                             Input File                  Output file")
print(entry_path,input_file, output_file,"\n")

# call procedure
opnsense_xml_to_json(entry_path, input_file, output_file)


# Reads a isc-dhcpd static lease json file
# Output opnsense kea reservation xml
kea_input_file  = "opnsense_isc_static_lease.json"
kea_output_file = "opnsense_isc_static_lease_converted_to_kea_reservations.xml"
print("Call json_to_opnsense_xml() \n[Path]                              Input File                  Output file")
print(entry_path, kea_input_file, kea_output_file,"\n\n")

#doc1_file = "config-OPNsense.localdomain-20240218111111.xml"
file1_path = os.path.join(entry_path, input_file) #doc1_file)
tree1 = ET.parse(file1_path)
root1= tree1.getroot()

#print("Found......",find_subnet_uuid(root1))

# call procedure
json_to_opnsense_xml(entry_path, kea_input_file, kea_output_file)


# Merge the original xml with the kea reservationabtion xml
# "config-OPNsense.localdomain-20240218000000.xml"
# "config-OPNsense.localdomain-20240218111111.xml"
orig = input_file
kea_xml = "opnsense_isc_static_lease_converted_to_kea_reservations.xml"
merge = "merge.xml"

# call procedure
print("Call merge_files() \n")
merge_files(entry_path, orig, kea_xml, merge)
    
    

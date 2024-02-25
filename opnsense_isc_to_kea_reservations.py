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
#
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
import re 
 
# checking subnet uuid for zero length which returns False
def has_len(obj):
    return hasattr(obj, '__len__')
    
    
# need to validate whether the value is a uuid or a subnet IP address
# using a rgex pattern match. Check for IP address pattern [xxx.xxx.xxx.xxx\xx]
def validate_uuid_rgex(uuid):
    #print(":::: ", uuid)
    pattern = r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2}"
    match = re.match(pattern,uuid)
    if bool(match):
        print("---> Missing valid inital kea reservation only has the subnet IP:", uuid)
        return False

# added command line argument support
def command_line_argument():
    # no arg call the default *.xml
    if (len(sys.argv) < 2):
        print("\n")
        print(python_script_name, "will process the default config-OPNsense*.xml","\n")
        #input_file  = "config-OPNsense.localdomain-20240218111111.xml"
        return ("use the orig input_file")
        
    elif (len(sys.argv) == 2):
        # command line one arg calls the *.xml as argument 1
        for i in range(1, len(sys.argv)):
            print(f'Argument {i}:', sys.argv[i])
            
            file_name_result = re.findall(r"^config-OPNsense\.localdomain-",sys.argv[i])
            print("Matching file name format: ", file_name_result)
            
            # date length is 14
            date_result = re.findall(r"\w{14}",sys.argv[i])
            print("Matching date format: ", date_result)
                   
            if (re.findall(r"^config-OPNsense\.localdomain-",sys.argv[i])) and (re.findall(r"\w{14}",sys.argv[i])):
                print("Yes, a regex patern match")
            else:
                print("No, a regex patern no match")
                sys.exit(1)
            
            print("\n")
            print(python_script_name, "will process", sys.argv[i],"\n")
            return (sys.argv[i])
    else:
        # command line for more than one arg 
        # calls the first *.xml as argument 1 and the second *.xml as argument 2
        # exits the program
        print(f"\nCould not parse.")
        for i in range(1, len(sys.argv)):
            print(f'Too many rgument {i}:', sys.argv[i])
        sys.exit(1)


# find subnet uuid from a working kea reservation in the input_file
def find_subnet_uuid(root_name):
    first_time = False
    correct_uuid_length = 36
    for item in root_name.findall('.//subnet'): 
        # test for missing text <uuid> </uuid> (testing False condition only)
        if ((has_len(item.text)) == False):
            print("WTF! Missing uuid value [Empty]. \nCheck config-OPNsense.localdomain-2024*.xml\n")
            item.text = "YOU NEED TO CREATE A VALID KEA RESERVATION"
            return item.text
            
        # uuid shall have correct uuid length
        if ((len(item.text) == correct_uuid_length) and (first_time == False)):
            print("Call find_subnet_uuid(): ", item.text)
            first_time = True
    return (item.text)    

# convert json array of objects to a kea xml
# Input     opnsense_isc_static_lease.json
# Output opnsense_isc_static_lease_converted_to_kea_reservations.xml
#
# a kea reservation xml
#                   <reservation uuid="bd774270-c81d-468f-a0a4-26bba4d150d3">
#                       <subnet>b2d692fb-fd9d-4bf7-84b7-eac29cca1692</subnet>
#                       <ip_address>10.59.11.101</ip_address>
#                       <hw_address>a1:b1:c1:d1:e1:f1</hw_address>
#                       <hostname>DAD-DESKTOP</hostname>
#                       <description>DAD-DESKTOP</description>
#                   </reservation>
def json_to_opnsense_xml(path,input,output):  
    file = os.path.join(path,input)
    input_file = open(file, 'r')

    # loads only a json array
    json_decode = json.load(input_file)
    
    # start xml tree 
    r = ET.Element("reservations")
    for item in json_decode:
        
        # set reservation uuid
        reservation = ET.SubElement(r,"reservation")
        reservation.set('uuid',str(uuid.uuid4()))
    
        # get subnet uuid from the 1st kea reservation       
        subnet_uuid = find_subnet_uuid(root1)
        uuid_validity = validate_uuid_rgex(subnet_uuid) 
        
        # an IP address is an invalid subnet uuid value
        if (uuid_validity == False):
           print("WTF! Missing a valid kea subnet uuid. \nCheck config-OPNsense.localdomain-2024*.xml\n")
           ET.SubElement(reservation,"subnet").text   = "YOU NEED TO CREATE A VALID KEA RESERVATION"
        else:
           # valid subnet uuid value
           print("--->", subnet_uuid)
           ET.SubElement(reservation,"subnet").text   = find_subnet_uuid(root1)
                     
        # get info from json file and populate xml tree
        ET.SubElement(reservation,"ip_address").text  = str(item["ipaddr"])
        ET.SubElement(reservation,"hw_address").text  = str(item["mac"])
        ET.SubElement(reservation,"hostname").text    = str(item["hostname"])
        ET.SubElement(reservation,"description").text = str(item["descr"])
        
        # construct tree object       
        kea_xml = ET.ElementTree(r)
        kea_xml.write(output)

    # make 'pretty' xml  
    tree = ET.parse(output)
    root = tree.getroot()
    ET.indent(tree, space = "\t", level=0)
    print("\n", ET.tostring(root, encoding='utf8').decode('utf8'))

    # save as a pretty xml file 
    tree.write(output, xml_declaration=True, encoding='utf-8', method="xml")

    # checking if the xml data is written to file or not
    output_file = os.path.join(path,output)
    read_output_file = open(output_file, 'r')
    print("\nchecking populated kea file for added reservations:\n")
    print(read_output_file.read())
    read_output_file.close()

    #print a confirmation message with the output file path
    print("\nopnsense kea-dhcpd xml saved to",output_file,"\n\n")


# convert config-OPNsense*.xml to json array of objects
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
    # xml data into a python dictionary 
    # using xmltodict module

    input_file = os.path.join(path,input)
    print("Convert xml ", input_file, "to json objects")
    print("Output needs to be a single json array containing json objects")
    print("Format: [{object1},{object2},{object3}]")

    # does the file exists
    isExist = os.path.exists(input_file)
    print ("The input file exists:", isExist)

    # validate whether input_file is an config-OPNsense*.xml file
    # check the <opnsense> tag
    tree0 = ET.parse(input_file)
    root1= tree0.getroot()
    if (root1.tag == "opnsense"):
        print("This is a config-OPNsense*.xmlfile with the correct tag ","<",root1.tag,">","\n")
        print("Starting: ", python_script_name,"\n\n")
    else:
        # terminate if not a config-OPNsense*.xmlfile.xml
        print("This is NOT a config-OPNsense*.xmlfile. Missing <opnsense> tag\n")
        print("Terminating: ", python_script_name,"\n\n")
        sys.exit(1)

    # loop through config-OPNsense*.xmlfile.xml
    with open (input_file) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())	
    # clean-up the nested array 
    # and get to the dhcpd value
    long_list = (list(data_dict.values()))
    #print(long_list)
    #print("\n")

    # get to <staticmap>
    short_list = long_list[0]
    #print("The...",short_list)
    #print("\n\n")

    
    # get to <staticmap>(key) find the key and insert the value 
    # into a json object
    # need at least one isc dhcpd static leases in the xml    
    inner_list = short_list['dhcpd']['lan']['staticmap']
    #print("\n")

    # write only a json array to a file. If a single object put it into an array
    # is the inner_list a type of dictionary?
    if isinstance(inner_list, dict) and 'mac' in inner_list:
        # make an array to hold one json object
        inner_list = [inner_list]
        print("This is an object\n")
        # this the is json array of one object    
    else:
        # loads an array
        print("This is an array\n")
        # this the is json array of objects
    
    # convert the dictionary to a json string with indentation 
    json_str = json.dumps(inner_list, indent=4)
    #print (json_str)
        
    # test output
    print("Print json file.\n", json_str)
    
    # specify the path to the output file 
    output_file = os.path.join(path, output)
    # save the json representation of the structure 
    with open(output_file, 'w') as f: 
        # Write the JSON string to the file 
        f.write(json_str)
        
    # print a confirmation message with the output file path 
    print("\njson saved to", output_file,"\n")


# merge the original xml with the kea reservation xml
def merge_files(entry_pathpath, input_file, kea_output_file, merge_file):
    print("Start -> Merge the xml files together")
    #input_file = "config-OPNsense.localdomain-20240218111111.xml"
    # read config-OPNsense*.xml
    orig_config_file_path = os.path.join(entry_path, input_file)
    tree1 = ET.parse(orig_config_file_path)
    root1= tree1.getroot()
    print(orig_config_file_path)

    # read kea reservations xml
    #kea_output_file = "opnsense_isc_static_lease_converted_to_kea_reservations.xml"
    kea_file_path = os.path.join(entry_path,kea_output_file)
    tree2 = ET.parse(kea_file_path)
    root2 = tree2.getroot()
   
    # merge file: merge.xml
    # location merge.xml
    merge_file_path = os.path.join(entry_path,merge_file)
    

    # loop and insert each reservation from kea_output_file 
    # into the orig_config_file
    for item in root2.findall('reservation'):
        #print("found",item)
    
        # goto 1st orig_config_file xml and find the start of the insertion field <reservations>
        # and loop through kea_output_file (item) by inserting each reservation
        target = root1.find('.//reservations')    
        target.insert(0,item)
    
    # make xml pretty and correct the idention    
    ET.indent(tree1, space = "\t", level=0)

    # write the merged xml file
    tree1.write(merge_file_path, xml_declaration=True, encoding='utf-8', method="xml")

    print("\nDone...the merged changes are in ",merge_file_path,"\n")


##################################   Main  ##################################

# python script name
python_script_name = "opnsense_isc_to_kea_reservations.py"



# change working path to where the *.py is executing from
script_directory = os.path.dirname(os.path.abspath(sys.argv[0])) 
print("The working path: ", script_directory,"\n")
os.chdir(script_directory)
entry_path = (os.getcwd())

# read opnsense config file: config-OPNsense*.xml
# create a isc-dhcpd static lease json file
#
#===================   [ADD YOUR CONFIG]     ================================
#   NOTE: Each xml shall have a isc-dhcpd static lease and a valid kea reservation
#
# one static lease
#input_file  = "config-OPNsense.localdomain-20240218000000.xml"
#
# multiple static leases
input_file  = "config-OPNsense.localdomain-20240218111111.xml"
#
# user defined static leases
#input_file  = "[ADD YOUR CONFIG].xml"
#
#===================   [ADD YOUR CONFIG]     ================================


#===================   [COMMAND LINE ARGUMENT SUPPORT] =================
#
# Supported:
# opnsense_isc_to_kea_reservations.py 
# opnsense_isc_to_kea_reservations.py [config-OPNsense*.xml]
#
#
# Not Supported:
# opnsense_isc_to_kea_reservations.py [config-OPNsense*.xml] [config-OPNsense*.xml] 
#
#
# use new config-OPNsense*.xml argument if passed in 
# otherwise opnsense_isc_to_kea_reservations.py by itself uses the default input_file
#
if not ( command_line_argument() == "use the orig input_file"):
    input_file = command_line_argument()


#===================   [COMMAND LINE ARGUMENT SUPPORT] =================


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

#orig_config_file = "config-OPNsense.localdomain-20240218111111.xml"
orig_config_file_path = os.path.join(entry_path, input_file)
tree1 = ET.parse(orig_config_file_path)
root1= tree1.getroot()

#print("Found......",find_subnet_uuid(root1))

# call procedure
json_to_opnsense_xml(entry_path, kea_input_file, kea_output_file)


# merge the original xml with the kea reservation xml
# "config-OPNsense.localdomain-20240218000000.xml"
# "config-OPNsense.localdomain-20240218111111.xml"
orig_xml  = input_file
kea_xml   = "opnsense_isc_static_lease_converted_to_kea_reservations.xml"
merge_xml = "merge.xml"

# call procedure
print("Call merge_files()\n")
merge_files(entry_path, orig_xml, kea_xml, merge_xml)
       

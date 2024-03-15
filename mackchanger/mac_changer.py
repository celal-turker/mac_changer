import re
import random
import subprocess
from optparse import OptionParser

def get_user_inputs():
    myopt = OptionParser()
    myopt.add_option("-i", "--interface", dest="interface", help="-i --interface")
    myopt.add_option("-m", "--mac", dest="macaddress", help="-m --mac")
    myopt.add_option("-r", "--random", dest="random", action="store_true", help="-r --random")
    (options, args) = myopt.parse_args()
    return options, args

def created_Mac():
    macList = []
    for i in range(1, 18):
        if i != 10:
            macList.append(str(i))
        else:
            for j in range(6):
                macList.append(chr(65 + j))
            break
    return macList

def get_new_mac(interface, macList):
    newMac = ""
    for _ in range(12):
        newMac += random.choice(macList)

    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()
    oldMac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result).group(0)
    
    return newMac, oldMac

def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def change_random_mac(interface, random_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", random_mac])
    subprocess.call(["ifconfig", interface, "up"])

def print_macs(interface, oldMac):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    newMac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result).group(0)
    print("Mac Address Changed ")
    if oldMac != newMac:
        print("Old Mac:", oldMac)
        print("New Mac:", newMac)
    else:
        print("Mac adresi değiştirilemedi")

user_input, args = get_user_inputs()

if user_input.random:
    created_mac = created_Mac()
    random_mac = get_new_mac(user_input.interface, created_mac)
    change_random_mac(user_input.interface, random_mac[0])  # random_mac[0] MAC adresini temsil eder
    print_macs(user_input.interface, random_mac[1])  # random_mac[1] eski MAC adresini temsil eder

elif user_input.macaddress:
    get_new_mac_tuple = get_new_mac(user_input.interface, created_Mac())
    change_mac(user_input.interface, user_input.macaddress)
    print_macs(user_input.interface, get_new_mac_tuple[1])  # get_new_mac_tuple[1] eski MAC adresini temsil eder

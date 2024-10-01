#!/usr/bin/env python3

# Automate SSH, Domain Name and RSA Configuration on Cisco IOS 

import getpass
import telnetlib

# Prompt for IP and other information
host = input('Enter IP address: ')
usrname = input('Enter Username: ')
password = getpass.getpass(prompt='Enter Password: ')

# Connect to the device
tn = telnetlib.Telnet(host)

# Log in and enter config mode
tn.read_until(b"Username: ")
tn.write(usrname.encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode('ascii') + b"\n")
tn.write(b"conf t\n")

# Configure SSH and Domain Name
tn.write(b"ip domain-name <domain name>\n")   # Replace <domain name> with your desired domain name
tn.write(b"crypto key generate rsa mod 1024\n")
tn.write(b"ip ssh version 2\n")

# Exit from config and logout
tn.write(b"end\n")
tn.write(b"exit\n")

print("Configuration complete!")
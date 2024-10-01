from netmiko import ConnectHandler

# Define device connection parameters
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
}

# Connect to the device
net_connect = ConnectHandler(**device)

# Define the VLAN configuration commands
vlan_config = [
    'vlan 10',
    'name VLAN10',
    'exit',
    'vlan 20',
    'name VLAN20',
    'exit',
    'interface vlan 10',
    'ip address 10.10.10.1 255.255.255.0',
    'no shut',
    'interface vlan 20',
    'ip address 20.20.20.1 255.255.255.0',
    'no shut',
]

# Send the VLAN configuration commands to the device
output = net_connect.send_config_set(vlan_config)

# Print the output
print(output)

# Close the connection
net_connect.disconnect()
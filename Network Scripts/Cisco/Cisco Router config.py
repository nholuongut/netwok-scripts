from netmiko import ConnectHandler

# Create a dictionary with the device information
device = {
    "host": "192.168.1.1",
    "username": "admin",
    "password": "password",
    "device_type": "cisco_ios",
}

# Connect to the device
net_connect = ConnectHandler(**device)

# Execute configuration commands on the device
net_connect.config_mode()
net_connect.send_command("interface FastEthernet0/1")
net_connect.send_command("no shutdown")

# Disconnect from the device
net_connect.disconnect()
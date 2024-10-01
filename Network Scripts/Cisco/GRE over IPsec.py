import paramiko

# Create SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to router
client.connect("router_ip", username="admin", password="password")

# Configure GRE over IPsec
config = [
    "interface Tunnel0",
    "ip address 10.0.0.1 255.255.255.0",
    "tunnel source FastEthernet0/0",
    "tunnel destination 1.1.1.1",
    "tunnel mode gre ip",
    "crypto map MYMAP",
]
for line in config:
    client.exec_command(line)

# Close SSH connection
client.close()
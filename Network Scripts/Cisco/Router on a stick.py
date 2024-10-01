import paramiko

# Create SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to router
client.connect("router_ip", username="admin", password="password")

# Configure Router on a stick
config = [
    "interface FastEthernet0/0",
    "no ip address",
    "no shut",
    "encapsulation dot1Q 1 native",
    "interface FastEthernet0/0.1",
    "encapsulation dot1Q 1",
    "ip address 10.0.0.1 255.255.255.0",
    "interface FastEthernet0/0.2",
    "encapsulation dot1Q 2",
    "ip address 10.0.1.1 255.255.255.0",
    "interface FastEthernet0/0.3",
    "encapsulation dot1Q 3",
    "ip address 10.0.2.1 255.255.255.0",
    "router eigrp 1",
    "network 10.0.0.0",
    "network 10.0.1.0",
    "network 10.0.2.0"
]

for line in config:
    client.exec_command(line)

# Close SSH connection
client.close()

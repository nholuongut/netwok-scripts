import ipaddress

# Get user input of CIDR notation
cidr_input = input("Enter CIDR notation (e.g. 192.168.0.0/24): ")

# Parse the CIDR notation into an IP network object
ip_network = ipaddress.ip_network(cidr_input)

# Display the subnet mask address
subnet_mask = ip_network.netmask
print(f"Subnet mask: {subnet_mask}")
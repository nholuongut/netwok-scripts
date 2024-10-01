import psutil

# Get the network interfaces of the local machine
interfaces = psutil.net_if_addrs()

# Iterate through the interfaces and print their information
for interface, info in interfaces.items():
    print(f"Interface: {interface}")
    for data in info:
        print(f"{data.family}: {data.address}")
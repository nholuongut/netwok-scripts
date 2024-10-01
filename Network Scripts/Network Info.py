import socket

# Get the hostname of the local machine
hostname = socket.gethostname()

# Get the IP address of the local machine
ip_address = socket.gethostbyname(hostname)

# Print the hostname and IP address
print(f"Hostname: {hostname}")
print(f"IP address: {ip_address}")
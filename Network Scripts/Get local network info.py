import subprocess

# Run the ipconfig command and get the output
output = subprocess.run(['ipconfig'], capture_output=True).stdout.decode('utf-8')

# Parse the output to get the IP address, subnet mask, and network address
for line in output.split('\n'):
    if 'IPv4 Address' in line:
        ip_address = line.split(':')[1].strip()
    elif 'Subnet Mask' in line:
        subnet_mask = line.split(':')[1].strip()
    elif 'Default Gateway' in line:
        network_address = line.split(':')[1].strip()

print(f'IP address: {ip_address}')
print(f'Subnet mask: {subnet_mask}')
print(f'Network address: {network_address}')
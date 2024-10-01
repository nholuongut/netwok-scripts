import paramiko
import os

# This example copies the new IOS image to the router's flash memory, verifies the image and installs it.

# Create SSH client
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to router
client.connect("router_ip", username="admin", password="password")

# Copy new IOS image to router
ftp_client=client.open_sftp()
ftp_client.put("path/to/new_ios_image.bin","flash:new_ios_image.bin")
ftp_client.close()

# Verify the new IOS image
stdin, stdout, stderr = client.exec_command("dir flash: | include new_ios_image.bin")
output = stdout.read().decode()
if "No such file or directory" in output:
    print("IOS image not found")
    exit()

# Install the new IOS image
stdin, stdout, stderr = client.exec_command("archive download-sw /overwrite /reload flash:new_ios_image.bin")
output = stdout.read().decode()
if "Are you sure you want to proceed" in output:
    stdin.write("y\n")
    stdin.flush()

# Close SSH connection
client.close()
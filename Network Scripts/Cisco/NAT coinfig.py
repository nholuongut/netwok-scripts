import paramiko

# Set the parameters for the SSH connection
host = "10.0.0.1"
username = "admin"
password = "secret"

# Establish the SSH connection
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=username, password=password)

# Send the NAT configuration commands to the router
stdin, stdout, stderr = ssh.exec_command("configure terminal")
stdin, stdout, stderr = ssh.exec_command("ip nat inside source list 1 interface GigabitEthernet0/0 overload")
stdin, stdout, stderr = ssh.exec_command("interface GigabitEthernet0/0")
stdin, stdout, stderr = ssh.exec_command("ip nat inside")
stdin, stdout, stderr = ssh.exec_command("interface GigabitEthernet0/1")
stdin, stdout, stderr = ssh.exec_command("ip nat outside")

# Close the SSH connection
ssh.close()
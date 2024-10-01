import paramiko
import time

class DellSwitchConfiguration:
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.ssh_client = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_client.connect(self.ip, username=self.username, password=self.password)
        except paramiko.ssh_exception.SSHException as e:
            raise ConnectionError(f"SSH connection to {self.ip} failed: {e}")

    def close(self):
        if self.ssh_client:
            self.ssh_client.close()

    def configure_switch(self, vlan_id, vlan_name, dhcp_pool):
        if not self.ssh_client:
            raise ValueError("SSH connection is not established. Call 'connect' first.")

        with self.ssh_client.invoke_shell() as ssh_shell:
            ssh_shell.send("configure terminal\n")
            time.sleep(0.5)

            # Add a new VLAN
            ssh_shell.send(f"vlan {vlan_id}\n")
            time.sleep(0.5)
            ssh_shell.send(f"name {vlan_name}\n")
            time.sleep(0.5)

            # Configure DHCP pool
            ssh_shell.send(f"ip dhcp pool {dhcp_pool}\n")
            time.sleep(0.5)
            ssh_shell.send("network 192.168.1.0 255.255.255.0\n")
            time.sleep(0.5)
            ssh_shell.send("default-router 192.168.1.1\n")
            time.sleep(0.5)

            ssh_shell.send("end\n")
            time.sleep(0.5)
            ssh_shell.send("write memory\n")
            time.sleep(1)

            output = ssh_shell.recv(65535).decode('utf-8')
            print(output)

    def view_switch_configuration(self):
        if not self.ssh_client:
            raise ValueError("SSH connection is not established. Call 'connect' first.")

        with self.ssh_client.invoke_shell() as ssh_shell:
            ssh_shell.send("show running-config\n")
            time.sleep(1)

            output = ssh_shell.recv(65535).decode('utf-8')
            print(output)

if __name__ == "__main__":
    # Replace these with your Dell switch credentials and IP address
    switch_ip = "your_switch_ip"
    switch_username = "your_username"
    switch_password = "your_password"

    new_vlan_id = 10
    new_vlan_name = "VLAN10"
    new_dhcp_pool = "DHCP_POOL_10"

    try:
        with DellSwitchConfiguration(switch_ip, switch_username, switch_password) as switch:
            switch.configure_switch(new_vlan_id, new_vlan_name, new_dhcp_pool)
            switch.view_switch_configuration()
    except ConnectionError as e:
        print("Connection Error:", e)
    except ValueError as e:
        print("Value Error:", e)
    except Exception as e:
        print("Error:", e)
import concurrent.futures
import paramiko

class MikroTikRouter:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.is_connected = False

    def connect(self):
        try:
            self.ssh_client.connect(self.hostname, username=self.username, password=self.password)
            self.is_connected = True
        except paramiko.AuthenticationException:
            print(f"Authentication failed for {self.hostname}. Check the username and password.")
        except paramiko.SSHException as e:
            print(f"An SSH error occurred while connecting to {self.hostname}: {e}")
        except Exception as e:
            print(f"An error occurred while connecting to {self.hostname}: {e}")

    def disconnect(self):
        self.ssh_client.close()
        self.is_connected = False

    def transfer_backup(self, local_file_path, remote_file_path):
        if not self.is_connected:
            print(f"Not connected to {self.hostname}. Skipping backup transfer.")
            return

        try:
            with self.ssh_client.open_sftp() as sftp_client:
                sftp_client.put(local_file_path, remote_file_path)

            print(f"Backup file '{local_file_path}' transferred to '{self.hostname}' as '{remote_file_path}' successfully.")
        except Exception as e:
            print(f"An error occurred while transferring backup to {self.hostname}: {e}")

    def create_backup(self, backup_file_name):
        if not self.is_connected:
            print(f"Not connected to {self.hostname}. Cannot create a backup.")
            return

        try:
            _, stdout, _ = self.ssh_client.exec_command(f"/system backup save name={backup_file_name}")
            result = stdout.read().decode().strip()

            if "configuration saved" in result.lower():
                print(f"Backup created on {self.hostname} with filename '{backup_file_name}' successfully.")
            else:
                print(f"Failed to create backup on {self.hostname}.")
        except Exception as e:
            print(f"An error occurred while creating backup on {self.hostname}: {e}")

    def check_backup_exists(self, backup_file_name):
        if not self.is_connected:
            print(f"Not connected to {self.hostname}. Cannot check backup existence.")
            return False

        try:
            _, stdout, _ = self.ssh_client.exec_command("/system backup print")
            backups = stdout.read().decode()
            return backup_file_name in backups
        except Exception as e:
            print(f"An error occurred while checking backup existence on {self.hostname}: {e}")
            return False

def main():
    # Router credentials
    router_credentials = [
        {"hostname": "router1_hostname_or_ip", "username": "router1_username", "password": "router1_password"},
        {"hostname": "router2_hostname_or_ip", "username": "router2_username", "password": "router2_password"},
        # Add more routers/switches here if needed
    ]

    # Local path of the backup file
    local_backup_file = "path/to/your/local/backup_file.rsc"

    # Remote path where the backup file will be placed on the router/switch
    remote_backup_file = "/backup/backup_file.rsc"  # Adjust this to the desired remote location

    with concurrent.futures.ThreadPoolExecutor() as executor:
        routers = [MikroTikRouter(**creds) for creds in router_credentials]

        # Connect to routers
        for router in routers:
            router.connect()

        # Use concurrent.futures to execute methods concurrently
        futures = []

        for router in routers:
            futures.append(executor.submit(router.transfer_backup, local_backup_file, remote_backup_file))
            futures.append(executor.submit(router.create_backup, "backup_file.rsc"))

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

        # Check backup existence
        for router in routers:
            exists = router.check_backup_exists("backup_file.rsc")
            if exists:
                print(f"Backup file 'backup_file.rsc' exists on {router.hostname}.")
            else:
                print(f"Backup file 'backup_file.rsc' does not exist on {router.hostname}.")

        # Disconnect from routers
        for router in routers:
            router.disconnect()

if __name__ == "__main__":
    main()
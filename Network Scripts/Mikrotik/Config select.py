import os
import paramiko
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

def get_mikrotik_config_files(folder_path):
    config_files = [f for f in os.listdir(folder_path) if f.endswith(".rsc")]
    return config_files

def display_config_files(config_files):
    print("Available MikroTik Configuration Files:")
    for idx, file in enumerate(config_files, start=1):
        print(f"{idx}. {file}")

def get_user_choice(config_files):
    while True:
        try:
            choice = int(input("Enter the number of the configuration file to apply: "))
            if 1 <= choice <= len(config_files):
                return config_files[choice - 1]
            else:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_router_credentials():
    router_ip = input("Enter the IP address of the MikroTik router: ")
    username = input("Enter your MikroTik username: ")
    password = input("Enter your MikroTik password: ")
    return router_ip, username, password

def establish_ssh_connection(hostname, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=username, password=password)
    return ssh_client

def send_configuration_data(ssh_client, config_data, router_ip):
    try:
        stdin, stdout, stderr = ssh_client.exec_command(config_data)
        error_message = stderr.read().decode().strip()
        if error_message:
            logging.error(f"Error occurred for {router_ip}: {error_message}")
        else:
            logging.info(f"Configuration applied successfully to {router_ip}.")
    except paramiko.SSHException as e:
        logging.error(f"SSH error occurred for {router_ip}: {e}")
    except Exception as e:
        logging.error(f"Error occurred for {router_ip}: {e}")

def apply_configuration_to_mikrotik(router_ip, username, password, config_file):
    try:
        ssh_client = establish_ssh_connection(router_ip, username, password)

        with open(config_file, 'r') as f:
            config_data = f.read()

        send_configuration_data(ssh_client, config_data, router_ip)
    except paramiko.AuthenticationException:
        logging.error(f"Authentication failed for {router_ip}. Please check your credentials.")
    except Exception as e:
        logging.error(f"Error occurred for {router_ip}: {e}")
    finally:
        ssh_client.close()

def main():
    folder_path = os.path.join(os.path.expanduser("~"), "Documents", "Mikrotik")
    config_files = get_mikrotik_config_files(folder_path)

    if not config_files:
        print("No MikroTik configuration files found in the 'Mikrotik' folder.")
        return

    display_config_files(config_files)
    chosen_config_file = get_user_choice(config_files)

    config_file_path = os.path.join(folder_path, chosen_config_file)

    if not os.path.exists(config_file_path):
        print("Selected configuration file does not exist.")
        return

    router_ip, username, password = get_router_credentials()

    # Configure logging to a file for a detailed log
    logging.basicConfig(filename='config_log.txt', level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

    with ThreadPoolExecutor() as executor:
        futures = []
        for config_file in config_files:
            future = executor.submit(apply_configuration_to_mikrotik, router_ip, username, password, os.path.join(folder_path, config_file))
            futures.append(future)

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"An error occurred during configuration application: {e}")

if __name__ == "__main__":
    main()
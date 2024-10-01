import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog
import paramiko

def compress_files(source_folder, destination_folder):
    try:
        shutil.make_archive(destination_folder, 'zip', source_folder)
        print(f"Files in '{source_folder}' compressed and saved to '{destination_folder}.zip'")
    except Exception as e:
        print(f"Error compressing files: {e}")

def move_files(source_folder, destination_folder):
    try:
        os.makedirs(destination_folder, exist_ok=True)
        for file in os.listdir(source_folder):
            file_path = os.path.join(source_folder, file)
            if os.path.isfile(file_path):
                shutil.move(file_path, destination_folder)
        print(f"Files moved from '{source_folder}' to '{destination_folder}'")
    except Exception as e:
        print(f"Error moving files: {e}")

def fetch_log_files(router_ip, router_username, router_password, remote_folder, local_folder):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(router_ip, username=router_username, password=router_password)

        # Create a new SFTP client to interact with the router's file system
        sftp_client = ssh_client.open_sftp()

        # Fetch log files from the MikroTik router
        for filename in sftp_client.listdir(remote_folder):
            remote_file_path = os.path.join(remote_folder, filename)
            local_file_path = os.path.join(local_folder, filename)
            sftp_client.get(remote_file_path, local_file_path)

        sftp_client.close()
        ssh_client.close()
        print(f"Log files fetched from '{remote_folder}' to '{local_folder}'")
    except Exception as e:
        print(f"Error fetching log files: {e}")

def send_logs_to_server(server_ip, server_username, server_password, local_folder, remote_folder):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server_ip, username=server_username, password=server_password)

        # Create a new SFTP client to interact with the remote server's file system
        sftp_client = ssh_client.open_sftp()

        # Upload the compressed log files to the remote server
        for filename in os.listdir(local_folder):
            local_file_path = os.path.join(local_folder, filename)
            remote_file_path = os.path.join(remote_folder, filename)
            sftp_client.put(local_file_path, remote_file_path)

        sftp_client.close()
        ssh_client.close()
        print(f"Log files sent from '{local_folder}' to '{remote_folder}' on the server.")
    except Exception as e:
        print(f"Error sending log files to server: {e}")

def check_folder_status(folder):
    # Add logic to check if the folder is filled (based on your requirement) and return True/False accordingly.
    # For example, you can check the number of files, size, or last modified date of files.
    return True

def pack_logs():
    recording_folder = "/log"  # Update this path based on the MikroTik log folder path

    # Fetching user input from GUI
    router_ip = router_ip_entry.get()
    router_username = router_username_entry.get()
    router_password = router_password_entry.get()
    local_folder = log_folder_entry.get()
    destination_folder = destination_folder_entry.get()
    server_ip = server_ip_entry.get()
    server_username = server_username_entry.get()
    server_password = server_password_entry.get()

    try:
        # Fetch log files from the MikroTik router
        fetch_log_files(router_ip, router_username, router_password, recording_folder, local_folder)
        compress_files(local_folder, destination_folder)

        # Send compressed log files to the log server
        send_logs_to_server(server_ip, server_username, server_password, destination_folder, "/remote/log")

        status_label.config(text="Logs packed and sent to the server successfully.")
    except Exception as e:
        status_label.config(text=f"Error packing and sending logs: {e}")

def choose_log_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        log_folder_entry.delete(0, tk.END)
        log_folder_entry.insert(0, folder_selected)

def choose_destination_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        destination_folder_entry.delete(0, tk.END)
        destination_folder_entry.insert(0, folder_selected)

def run_gui():
    root = tk.Tk()
    root.title("Log Packer")

    router_ip_label = tk.Label(root, text="Router IP:")
    router_ip_label.pack()
    router_ip_entry = tk.Entry(root)
    router_ip_entry.pack()

    router_username_label = tk.Label(root, text="Router Username:")
    router_username_label.pack()
    router_username_entry = tk.Entry(root)
    router_username_entry.pack()

    router_password_label = tk.Label(root, text="Router Password:")
    router_password_label.pack()
    router_password_entry = tk.Entry(root, show="•")
    router_password_entry.pack()

    log_folder_label = tk.Label(root, text="Local Log Folder:")
    log_folder_label.pack()
    log_folder_entry = tk.Entry(root)
    log_folder_entry.pack()

    browse_button = tk.Button(root, text="Browse", command=choose_log_folder)
    browse_button.pack()

    destination_folder_label = tk.Label(root, text="Destination Folder:")
    destination_folder_label.pack()
    destination_folder_entry = tk.Entry(root)
    destination_folder_entry.pack()

    destination_button = tk.Button(root, text="Browse", command=choose_destination_folder)
    destination_button.pack()

    server_ip_label = tk.Label(root, text="Log Server IP:")
    server_ip_label.pack()
    server_ip_entry = tk.Entry(root)
    server_ip_entry.pack()

    server_username_label = tk.Label(root, text="Log Server Username:")
    server_username_label.pack()
    server_username_entry = tk.Entry(root)
    server_username_entry.pack()

    server_password_label = tk.Label(root, text="Log Server Password:")
    server_password_label.pack()
    server_password_entry = tk.Entry(root, show="•")
    server_password_entry.pack()

    pack_button = tk.Button(root, text="Pack Logs", command=pack_logs)
    pack_button.pack()

    status_label = tk.Label(root, text="")
    status_label.pack()

    root.mainloop()

def main():
    threading.Thread(target=run_gui).start()

if __name__ == "__main__":
    main()
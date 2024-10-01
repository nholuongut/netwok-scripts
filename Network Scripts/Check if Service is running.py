import subprocess

def check_remote_service_status(remote_ip, service_name):
    try:
        # Run the SSH command to check the service status on the remote host
        ssh_command = ["ssh", remote_ip, "service", service_name, "status"]
        check_service = subprocess.check_output(ssh_command, universal_newlines=True).strip()
        
        if 'running' in check_service.lower():
            print(f'{service_name} service on {remote_ip} is running.')
        elif 'stopped' in check_service.lower():
            print(f'{service_name} service on {remote_ip} is stopped.')
        else:
            print(f'{service_name} service on {remote_ip} is in an unknown state.')

    except subprocess.CalledProcessError as e:
        print(f'[ERROR] Failed to execute SSH command: {e}')
    except Exception as e:
        print(f'[ERROR] {e}')

if __name__ == "__main__":
    remote_ip = "xxx.xxx.xxx.xxx"
    service_name = "Service_Name"
    check_remote_service_status(remote_ip, service_name)
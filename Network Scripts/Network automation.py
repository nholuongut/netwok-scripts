from cisco import CiscoDevice

def configure_cisco_device():
    try:
        # Connect to the Cisco device
        with CiscoDevice(host='192.168.1.1', username='admin', password='secret') as device:
            # Set the hostname of the device
            device.set_hostname('my-router')

            # Create a VLAN with ID 10 and name 'VLAN10'
            device.create_vlan(10, 'VLAN10')

            # Add a switchport to VLAN 10
            device.create_switchport(10)

            # Save the configuration
            device.save_config()

        print("Configuration successful.")
    except Exception as e:
        print("Error configuring the Cisco device:", e)

if __name__ == "__main__":
    configure_cisco_device()
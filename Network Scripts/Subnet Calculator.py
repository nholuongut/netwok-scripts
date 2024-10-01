import ipaddress

def get_network_details(network_str: str, subnet_mask_str: str) -> None:
    try:
        # Create an IPv4Network object
        network_address = ipaddress.IPv4Network(f"{network_str}/{subnet_mask_str}", strict=False)

        # Print the network details
        print("Network address:", network_address.network_address)
        print("Netmask:", network_address.netmask)
        print("Wildcard mask:", network_address.hostmask)
        print("Broadcast address:", network_address.broadcast_address)
        print("Number of hosts:", network_address.num_addresses - 2)  # Subtract 2 to exclude network and broadcast addresses
    except ValueError as e:
        print("Error:", e)

def main():
    # Get user input for network address and subnet mask
    network = input("Enter the network address: ")
    subnet_mask = input("Enter the subnet mask: ")

    get_network_details(network, subnet_mask)

if __name__ == "__main__":
    main()
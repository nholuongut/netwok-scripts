import tkinter as tk
import ipaddress

class SubnetCalculatorGUI:
    # Constants
    BG_COLOR = "#282c34"
    FG_COLOR = "white"
    BLUE_COLOR = "#61afef"

    def __init__(self, master):
        self.master = master
        master.title("Subnet Calculator")
        master.config(bg=self.BG_COLOR)

        # Create and place network address label and entry widget
        self.network_label = tk.Label(master, text="Network address:", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.network_label.grid(row=0, column=0, sticky="W")
        self.network_entry = tk.Entry(master, bg="white", fg="black")
        self.network_entry.grid(row=0, column=1)

        # Create and place subnet mask label and entry widget
        self.subnet_mask_label = tk.Label(master, text="Subnet mask:", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.subnet_mask_label.grid(row=1, column=0, sticky="W")
        self.subnet_mask_entry = tk.Entry(master, bg="white", fg="black")
        self.subnet_mask_entry.grid(row=1, column=1)

        # Create and place calculate button
        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate, bg=self.BLUE_COLOR, fg=self.FG_COLOR)
        self.calculate_button.grid(row=2, column=0, columnspan=2)

        # Create and place output labels
        self.network_address_label = tk.Label(master, text="Network address:", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.network_address_label.grid(row=3, column=0, sticky="W")
        self.netmask_label = tk.Label(master, text="Netmask:", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.netmask_label.grid(row=4, column=0, sticky="W")
        self.wildcard_mask_label = tk.Label(master, text="Wildcard mask:", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.wildcard_mask_label.grid(row=5, column=0, sticky="W")
        self.broadcast_address_label = tk.Label(master, text="Broadcast address:", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.broadcast_address_label.grid(row=6, column=0, sticky="W")
        self.num_hosts_label = tk.Label(master, text="Number of hosts:", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.num_hosts_label.grid(row=7, column=0, sticky="W")

        # Create and place output value labels
        self.network_address_value = tk.Label(master, text="", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.network_address_value.grid(row=3, column=1, sticky="W")
        self.netmask_value = tk.Label(master, text="", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.netmask_value.grid(row=4, column=1, sticky="W")
        self.wildcard_mask_value = tk.Label(master, text="", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.wildcard_mask_value.grid(row=5, column=1, sticky="W")
        self.broadcast_address_value = tk.Label(master, text="", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.broadcast_address_value.grid(row=6, column=1, sticky="W")
        self.num_hosts_value = tk.Label(master, text="", bg=self.BG_COLOR, fg=self.FG_COLOR)
        self.num_hosts_value.grid(row=7, column=1, sticky="W")

    def calculate(self):
        # Get network address and subnet mask input
        network_address_str = self.network_entry.get()
        subnet_mask_str = self.subnet_mask_entry.get()

        try:
            # Create an IPv4Network object
            network_address = ipaddress.IPv4Network(f"{network_address_str}/{subnet_mask_str}", strict=False)

            # Update output labels
            self.network_address_value.config(text=str(network_address.network_address))
            self.netmask_value.config(text=str(network_address.netmask))
            self.wildcard_mask_value.config(text=str(network_address.hostmask))
            self.broadcast_address_value.config(text=str(network_address.broadcast_address))
            self.num_hosts_value.config(text=str(network_address.num_addresses - 2))

        except ipaddress.AddressValueError:
            # Handle invalid input
            self.network_address_value.config(text="Invalid Input")
            self.netmask_value.config(text="Invalid Input")
            self.wildcard_mask_value.config(text="Invalid Input")
            self.broadcast_address_value.config(text="Invalid Input")
            self.num_hosts_value.config(text="Invalid Input")

# Create the root window and run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    subnet_calculator_gui = SubnetCalculatorGUI(root)
    root.mainloop()
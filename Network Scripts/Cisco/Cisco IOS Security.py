from netmiko import ConnectHandler

#parameters for the device
device = { 
    "host": 'router_ip', 
    "username": 'your_username', 
    "password": 'your_password', 
    'device_type': 'cisco_ios' 
}

#Establishing SSH connection    
connection = ConnectHandler(**device)

#Enable Telnet  
connection.send_config_set(['line vty 0 4', 'password mypassword','login','transport input telnet'])

#configuring Access List  
connection.send_config_set(['access-list 1 permit any_hostip'])

#Setting up a banner
connection.send_config_set(['banner motd "$ SeUrITy Is YoUrs !"'])

#closing the SSH connection
connection.disconnect()
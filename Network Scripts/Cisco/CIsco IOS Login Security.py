import telnetlib 

host = "192.168.1.1" 
username = "admin" 
password = "admin"

tn = telnetlib.Telnet(host) 
tn.read_until("Username: ") 
tn.write(username + "\n") 
if password: 
    tn.read_until("Password: ") 
    tn.write(password + "\n") 

# Enabling password authentication
tn.write("enable\n") 
tn.write("config t\n") 
tn.write("enable secret cisco\n") 
tn.write("line console 0\n") 
tn.write("password cisco\n") 
tn.write("login\n") 
tn.write("end\n") 

# Committing the changes
tn.write("wr\n") 
tn.write("exit\n") 

print(tn.read_all().decode('ascii')) 
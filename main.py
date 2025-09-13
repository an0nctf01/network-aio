import os , time
import subprocess , ipaddress , ping3 , socket , re
from concurrent.futures import ThreadPoolExecutor
from scapy.all import ARP, Ether, srp


print("Welcome To Network-AIO Tool made by an0nctf01")

print(r'''
                      /$$$$$$                        /$$      /$$$$$$   /$$$$$$    /$$  
                     /$$$_  $$                      | $$     /$$__  $$ /$$$_  $$ /$$$$  
  /$$$$$$  /$$$$$$$ | $$$$\ $$ /$$$$$$$   /$$$$$$$ /$$$$$$  | $$  \__/| $$$$\ $$|_  $$  
 |____  $$| $$__  $$| $$ $$ $$| $$__  $$ /$$_____/|_  $$_/  | $$$$    | $$ $$ $$  | $$  
  /$$$$$$$| $$  \ $$| $$\ $$$$| $$  \ $$| $$        | $$    | $$_/    | $$\ $$$$  | $$  
 /$$__  $$| $$  | $$| $$ \ $$$| $$  | $$| $$        | $$ /$$| $$      | $$ \ $$$  | $$  
|  $$$$$$$| $$  | $$|  $$$$$$/| $$  | $$|  $$$$$$$  |  $$$$/| $$      |  $$$$$$/ /$$$$$$
 \_______/|__/  |__/ \______/ |__/  |__/ \_______/   \___/  |__/       \______/ |______/
''')

time.sleep(3)
print("This AIO tool is mainly used for Network Troubleshooting Or Testing/Debugging.")
time.sleep(3)

print("1. Check Network Connectivity") 
print("2. Check Local Network Connect Devices") 
print("3. Change Local IP Address (Administrator Privileges Required)") 
print("4. Reset Windows Network Services (Administrator Privileges Required)")

user_choice = int(input("\nSelect Option 1-4: "))

print(f"You Picked Option Number {user_choice}")
time.sleep(2)

if user_choice == 1:
    os.system("cls")
    net_stat = ping3.ping("8.8.8.8")

    if net_stat is not None:
        print("✅ Network Has Internet Access")
        ping_time = int(input("How many pings? :"))
        print(f"Pinging 8.8.8.8 {ping_time} times:\n")
        for i in range(ping_time):
            result = subprocess.run(
                ["ping", "-n", "1", "8.8.8.8"],
                capture_output=True,
                text=True
            )
            for line in result.stdout.splitlines():
                if "time=" in line:
                    print(line.strip())
                    break
            time.sleep(1)
    else:
        print("❌ Network Has No Internet Access")


elif user_choice == 2:
    os.system("cls")
    print("Starting to Ping Local Network")
    
    local_ip = socket.gethostbyname(socket.gethostname())
    network = ipaddress.ip_network(local_ip + '/24', strict=False)
    print(f"Scanning subnet: {network}\n")

    for ip in network.hosts():
        subprocess.run(["ping", "-n", "1", "-w", "100", str(ip)],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)


    arp_output = subprocess.check_output("arp -a", text=True)
    pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+)\s+([-\w]+)")


    print("Active devices (IP — MAC — Hostname if available):")
    for ip, mac in pattern.findall(arp_output):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except:
            hostname = "Unknown"
        print(f"{ip} — {mac} — {hostname}")


elif user_choice == 3:
    os.system("cls")
    print("Option 3 selected (not implemented yet)")
    interface_name = "Ethernet" 
    new_ip = input("enter desired ip address")
    subnet_mask = input("enter desired subnet_mask")
    gateway = input("enter desired gateway")

    subprocess.run([
        "netsh", "interface", "ip", "set", "address",
        f"name={interface_name}", "static",
        new_ip, subnet_mask, gateway, "1"
    ], shell=True)

    subprocess.run(["ipconfig", "/flushdns"], shell=True)

    print(f"IP, DNS updated and DNS cache flushed for {interface_name}")

elif user_choice == 4:
    os.system("cls")
    print("Resetting Windows Network Services...")
  
def reset_network_services():
    commands = [
        
        ["netsh", "int", "ip", "reset"],
        ["netsh", "winsock", "reset"],
        ["ipconfig", "/release"],
        ["ipconfig", "/renew"],
        ["ipconfig", "/flushdns"],
        ["sc", "stop", "Dhcp"],
        ["sc", "start", "Dhcp"],
        ["sc", "stop", "Dnscache"],
        ["sc", "start", "Dnscache"],
        ["sc", "stop", "LanmanWorkstation"],
        ["sc", "start", "LanmanWorkstation"],
        ["sc", "stop", "Netman"],
        ["sc", "start", "Netman"],
    ]

    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to run: {' '.join(cmd)}")

    print("\n✅ Windows network services reset successfully!")
    print("⚠️ Some changes may require a reboot to take full effect.")

reset_network_services()    

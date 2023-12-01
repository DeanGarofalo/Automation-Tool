import paramiko
import os
import sys
# Again this is so wack that I have to do this.
current_directory = os.path.dirname(os.path.realpath(__file__))
project_directory = os.path.dirname(current_directory)
sys.path.append(project_directory)
from Stuff.Server import Server
import re

# These are the minimum specs that the program will check against. If they ever change, they can be updated right here and once.
##################################################################################
B_APP_SPECS = [
    {"Tier": "Low Traffic", "CPU": 4, "RAM": 16, "Disk": 250},
    {"Tier": "High Traffic", "CPU": 6, "RAM": 32, "Disk": 250},
    {"Tier": "Ultra Traffic", "CPU": 6, "RAM": 64, "Disk": 250}
]
B_APP_CONECT = [
    {"Tier": "Valid", "CPU": 4, "RAM": 8, "Disk": 250}
]
##################################################################################
##################################################################################
C_NOT_HA_SPECS = [
    {"Tier": "Limited capacity", "CPU": 8, "RAM": 16, "Disk": 210},
    {"Tier": "Full capacity", "CPU": 16, "RAM": 32, "Disk": 210},
]
C_HA_APP = [
    {"Tier": "Full capacity", "CPU": 16, "RAM": 16, "Disk": 210}
]
C_HA_REP = [
    {"Tier": "Full capacity", "CPU": 16, "RAM": 32, "Disk": 210}
]
##################################################################################
##################################################################################
D_APP_SPECS = [
    {"Tier": "Valid", "CPU": 4, "RAM": 16, "Disk": 160}
]
##################################################################################
##################################################################################
S_APP_SPECS = [
    {"Tier": "Valid", "CPU": 4, "RAM": 32, "Disk": 150}
]
##################################################################################

def main(servers: list[Server], what_app_is_this: str, deployment_type: str):
    
    match what_app_is_this:
        case "C":
            for server in servers:
                retrieved_specs = get_remote_specs(server)
                spec = check_specs_c_app(server, retrieved_specs, deployment_type)
                if spec == "None":
                    print(f"{server._hostname} does not meet minimum specification ⛔")
                if spec == "Limited capacity":
                    print(f"{server._hostname} is a Low capacity configuration ⚠️") 
                if spec == "Full capacity":
                    print(f"{server._hostname} meets minimum specification ✅")
        case "B":
            for server in servers:
                retrieved_specs = get_remote_specs(server)
                spec = check_specs_b_app(server, retrieved_specs)
                if spec == "None":
                    print(f"{server._hostname} does not meet minimum specification ⛔")
                if spec == "Valid":
                    print(f"{server._hostname} meets minimum specification ✅")
                if spec == "Low Traffic":
                    print(f"{server._hostname} is a Low Traffic configuration ⚠️")
                if spec == "High Traffic":
                    print(f"{server._hostname} is a High Traffic configuration ✅")
                if spec == "Ultra Traffic":
                    print(f"{server._hostname} is a Ultra Traffic configuration 🎆")
        case "S":
            for server in servers:
                retrieved_specs = get_remote_specs(server)
                spec = check_specs_s_app(server, retrieved_specs)
                if spec == "None":
                    print(f"{server._hostname} does not meet minimum specification ⛔")
                else:
                    print(f"{server._hostname} meets minimum specification ✅")
        case "D":
            for server in servers:
                retrieved_specs = get_remote_specs(server)
                spec = check_specs_d_app(server, retrieved_specs)
                if spec == "None":
                    print(f"{server._hostname} does not meet minimum specification ⛔")
                else:
                    print(f"{server._hostname} meets minimum specification ✅")
        case _:
            print("Unrecognized app. Exiting")
            return




# These can all be one function but it requires a bit more thought than I want to give it at the moment. 
# Come back to this later 
def check_specs_b_app(server: Server, fetched_specs: dict) -> str:
    max_spec = "None"
    if "Connector" in server._ha_type:
        for valid_spec in B_APP_CONECT:
            if fetched_specs["CPU"] >= valid_spec["CPU"] and fetched_specs["RAM"] >= valid_spec["RAM"] and fetched_specs["Disk"] >= valid_spec["Disk"]:
                max_spec = valid_spec["Tier"]
        return max_spec
    else:
        for valid_spec in B_APP_SPECS:
            if fetched_specs["CPU"] >= valid_spec["CPU"] and fetched_specs["RAM"] >= valid_spec["RAM"] and fetched_specs["Disk"] >= valid_spec["Disk"]:
                max_spec = valid_spec["Tier"]
    return max_spec
    
def check_specs_d_app(fetched_specs: dict) -> str:
    max_spec = "None"
    for valid_spec in D_APP_SPECS:
        if fetched_specs["CPU"] >= valid_spec["CPU"] and fetched_specs["RAM"] >= valid_spec["RAM"] and fetched_specs["Disk"] >= valid_spec["Disk"]:
            max_spec = valid_spec["Tier"]
    return max_spec

def check_specs_s_app(fetched_specs: dict) -> str:
    max_spec = "None"
    for valid_spec in S_APP_SPECS:
        if fetched_specs["CPU"] >= valid_spec["CPU"] and fetched_specs["RAM"] >= valid_spec["RAM"] and fetched_specs["Disk"] >= valid_spec["Disk"]:
            max_spec = valid_spec["Tier"]
    return max_spec

def check_specs_c_app(server: Server, fetched_specs: dict, deployment_type: str) -> str:
    max_spec = "None"
    # If its a HA we need to use the HA specs
    if "HA" in deployment_type:
        # Need to split HA's between Reporting servers and everything else
        if "Report" in server._ha_type:
            for valid_spec in C_HA_REP:
                if fetched_specs["CPU"] >= valid_spec["CPU"] and fetched_specs["RAM"] >= valid_spec["RAM"] and fetched_specs["Disk"] >= valid_spec["Disk"]:
                    max_spec = valid_spec["Tier"]
        else:
            for valid_spec in C_HA_APP:
                if fetched_specs["CPU"] >= valid_spec["CPU"] and fetched_specs["RAM"] >= valid_spec["RAM"] and fetched_specs["Disk"] >= valid_spec["Disk"]:
                    max_spec = valid_spec["Tier"]
    # Otherwise its an app or DB server
    else:
        for valid_spec in C_NOT_HA_SPECS:
            if fetched_specs["CPU"] >= valid_spec["CPU"] and fetched_specs["RAM"] >= valid_spec["RAM"] and fetched_specs["Disk"] >= valid_spec["Disk"]:
                max_spec = valid_spec["Tier"]
    return max_spec


#TODO redo this to just only take in localhost since im going to be using those tunnels
def get_remote_specs(server: Server) -> dict:
    try:
        # Establish a SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server.ip_address, port=22, username=server._username, password=server._password)

        # SSH commands to run
        commands = [
            "nproc",  # Get number of CPU cores
            "free -h | grep Mem | awk '{print$2}'",  # Get RAM size
            "df -h  --output=size --total | awk 'END {print $1}'"  # Get Disk space 
        ]
        hardware_specs = {}

        for command in commands:
            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read().decode("utf-8")
            hardware_specs[command] = output

        # Making it more readable later and trimming the human readable portion.
        # In reality I shoud really really not be doing it this way and just use bytes but I can't and won't learn how to count past 10 to convert that
        # and this is already steps above what I did in the older automation tool
        hardware_specs["CPU"] = hardware_specs.pop("nproc")
        hardware_specs["RAM"] = hardware_specs.pop("free -h | grep Mem | awk '{print$2}'")
        hardware_specs["Disk"] = hardware_specs.pop("df -h  --output=size --total | awk 'END {print $1}'")

        for key, value in hardware_specs.items():
            # Use regular expression to extract numeric part
            numeric_part = re.search(r'\d+(\.\d+)?', value)
            # Update the dict value with the numeric part as a string
            hardware_specs[key] = float(numeric_part.group()) if numeric_part else None

        return hardware_specs
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the SSH connection
        if ssh_client:
            ssh_client.close()




if __name__=="__main__":
    password = input("Enter vm password: ")
    test_Server = [Server("test-VM", "192.168.1.149", "Primary Reporting", "subnet1", 2, 2, "dean", password)]
    app = "C"
    deploy = "HA with Reporting"
    main(test_Server, app, deploy)
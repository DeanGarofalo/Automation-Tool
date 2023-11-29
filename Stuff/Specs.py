import paramiko
from openpyxl import load_workbook, worksheet
import os
import sys

# Again this is so wack that I have to do this.
current_directory = os.path.dirname(os.path.realpath(__file__))
project_directory = os.path.dirname(current_directory)
sys.path.append(project_directory)

from Stuff.Server import Server

#TODO redo this to just only take in localhost since im going to be using those tunnels
def get_remote_specs(ip: str, username: str, password: str):
    try:
        # Establish a SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip, port=22, username=username, password=password)

        # SSH commands to run
        commands = [
            "nproc",  # Get number of CPU cores
            "free -h | grep Mem | awk '{print$2}'",  # Get RAM size
            "df -h  --output=size --total | awk 'END {print $1}'"  # Get Disk space 
        ]

        hardware_info = {}

        for command in commands:
            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read().decode("utf-8")
            hardware_info[command] = output

        print("CPU:", hardware_info['nproc'])
        print("RAM:", hardware_info["free -h | grep Mem | awk '{print$2}'"])
        print("Disk", hardware_info["df -h  --output=size --total | awk 'END {print $1}'"])

        return hardware_info
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the SSH connection
        if ssh_client:
            ssh_client.close()

def main(server: Server, what_app_is_this: str, deployment_type: str):
    
    info = get_remote_specs(server.ip_address, server._username, server._password)
    
    #TODO Need the think about how im going to verify specs more. Some apps have very nuanced tiers of specs, so need to know the type of server and match it to specs but also make it easy to update and maintain
    # maybe a dict with the min spec and have that as a global constant here?
    # d app only has one config, 4+ cpu, 16+ ram, 100+ disk
    # c app has limited single which is 8+ cpu, 16+ ramn, 210+ disk
    # rep most be 8cpu, 16





if __name__=="__main__":
    test_Server = Server("test-VM", "192.168.1.149", "HA", "subnet1", 2, 2, "dean", "password")
    app = "C"
    deploy = "HA"
    main(test_Server, app, deploy)
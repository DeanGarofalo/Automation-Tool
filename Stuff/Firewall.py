import paramiko
import os
import sys
# Again this is so wack that I have to do this.
current_directory = os.path.dirname(os.path.realpath(__file__))
project_directory = os.path.dirname(current_directory)
sys.path.append(project_directory)
from Stuff.Server import Server

# These are the network port for each app. If they need to be updated they can be adjusted here. 
C_PORTS = ["22/tcp", "80/tcp", "450/tcp", "2181/tcp", "2888-3888/tcp", "3697/tcp", "4369/tcp", "5060/tcp", "6177/tcp", "6178/tcp", "6179/tcp", "6198/tcp", "6200-7999/tcp", "8006/tcp", "8007/tcp", "8008/tcp", "8009/tcp", "8011/tcp", "8070/tcp", "8080/tcp", "8081/tcp", "8086/tcp", "8087/tcp", "8089/tcp", "8093/tcp", "8097/tcp", "8098/tcp", "8099/tcp", "8985/tcp", "9092/tcp", "33337/tcp"]
B_PORTS = ["22/tcp", "80/tcp", "443/tcp", "1099/tcp", "2181/tcp", "3191/tcp", "4174/tcp", "4191/tcp", "6040/tcp", "6050/tcp", "7103/tcp", "7104-7124/tcp", "7200/tcp", "7201/tcp", "8099/tcp", "8443/tcp", "9092/tcp", "9093/tcp", "9200/tcp", "9300/tcp", "10161/tcp", "10162/tcp", "52233/tcp" ]
S_PORTS = ["443/tcp", "9080/tcp", "9180/tcp", "9192/tcp", "6443/tcp", "10250/tcp", "10251/tcp", "10252/tcp", "10255/tcp", "2379-2380/tcp", "30000-32767/tcp", "123/udp"] # this single udp port is an edge case which requires each port to specify /tcp now
D_PORTS = ["22/tcp", "80/tcp", "443/tcp", "5432/tcp", "8944/tcp", "8945/tcp"]


def run_firewall(server: Server, ports: list[str]):
    """Pretty self explanatory

    Args:
        server (Server): the server to connect to
        ports (list[str]): a list of strings. Each string is a newtork port to open. Strings instead of ints so I can handle ranges
    """
    try:
        # Establish a SSH connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(server.ip_address, port=22, username=server._username, password=server._password)

        for port_number in ports:
            # The firewall-cmd command to open each port
            command = f"sudo -S firewall-cmd --zone=public --add-port={port_number} --permanent"
            # Full disclousre, I'm not testing sudo, nor this function since my VM doesnt use firewalld. But I anticipate issues with sudo requiring the interactive password. So if I did see an issue I'd start with doing something like this:
            # command = f"echo {server._password} | sudo -S firewall-cmd --zone=public --add-port={port_number} --permanent"
            stdin, stdout, stderr = ssh_client.exec_command(command)
            # Check for any errors
            error_output = stderr.read().decode('utf-8')
            if error_output:
                print(f"Error opening port {port_number}: {error_output}")
            
        reload_command = "sudo -S firewall-cmd --reload"
        # reload_command = "echo {server._password} | sudo -S firewall-cmd --reload"
        ssh_client.exec_command(reload_command)
    except TimeoutError:
        print(f"Connetion timed out for {server.ip_address}\tDid not open firewall ports ⚠️")
    except OSError:
        print(f"Network is unreachable when attempting to ssh to {server.ip_address}\tDid not open firewall ports ⚠️")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssh_client.close()
    

def main(servers: list[Server], what_app_is_this: str):
    match what_app_is_this:
        case "B":
            for server in servers:
                run_firewall(server, B_PORTS)
        case "C":
            for server in servers:
                run_firewall(server, C_PORTS)
        case "S":
            for server in servers:
                run_firewall(server, S_PORTS)
        case "D":
            for server in servers:
                run_firewall(server, D_PORTS)
        case _:
            print("Currently there is no firewall script for:", what_app_is_this)



if __name__ == "__main__":
    main()
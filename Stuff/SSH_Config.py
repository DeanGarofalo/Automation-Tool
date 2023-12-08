import paramiko
import os
import sys
# Again this is so wack that I have to do this.
current_directory = os.path.dirname(os.path.realpath(__file__))
project_directory = os.path.dirname(current_directory)
sys.path.append(project_directory)
from Stuff.Server import Server



def generate_ssh_config(servers: list[Server], profile_name, jumpserver: Server):
    backdoor_username = "admin"
    ssh_port = '22'
    host_settings = f"""
Host {profile_name}
    HostName {jumpserver.ip_address}
    User {backdoor_username}
    Port {ssh_port}"""

    forward_settings = "\n".join([f"    LocalForward {server.port} {server.ip_address}:22" for server in servers])

    ssh_config_content = f"{host_settings}\n{forward_settings}\n"

    # Save to a file
    config_file_path = os.path.expanduser('~/.ssh/config')
    with open(config_file_path, 'a') as configfile:
        configfile.write(ssh_config_content)

    print(f'SSH config file created: {config_file_path}')

    




def main(list_of_servers: list[Server], profile_name: str, jumpserver: Server):
  
    generate_ssh_config(list_of_servers, profile_name, jumpserver)
   


if __name__ == "__main__":
    Test_List_of_Servers = [
    Server("DG1234", "192.168.1.1", "3N1D", "subnet1", 10, 20, "u", "p"),
    Server("DG1234", "192.168.1.1", "3N1D", "subnet1", 10, 20, "u", "p"),
    Server("DG1234", "192.168.1.1", "3N1D", "subnet1", 10, 20, "u", "p"),
    Server("DG1234", "192.168.1.1", "3N1D", "subnet2", 10, 20, "u", "p"),
    Server("DG1234", "192.168.1.1", "3N1D", "subnet2", 10, 20, "u", "p")
    ]
    for i in range(len(Test_List_of_Servers)):
        Test_List_of_Servers[i].port = i + 3000
    jumpserver = Server("test-vm", "192.168.1.149", "N/A", "N/A", 0, 0, "dean", "")
     
    main(Test_List_of_Servers, "test", jumpserver)
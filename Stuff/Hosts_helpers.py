import paramiko
import os
import sys

# Again this is so wack that I have to do this.
current_directory = os.path.dirname(os.path.realpath(__file__))
project_directory = os.path.dirname(current_directory)
sys.path.append(project_directory)

from Stuff.Server import Server

# not totally useless, can still use this if they have to provide a domain name manually because the search failed
def generate_fqdns(domain_name: str, list_of_servers: list[Server]) -> None:
    for server in list_of_servers:
        server.fqdn = server._hostname + "." + domain_name
       

def generate_hosts_file(list_of_servers: list[Server], debug_mode: bool) -> None:
    # Check if the hosts file exists, and delete it, if it does, because this would append to a old one if not done
    file_path="hosts"
    if os.path.exists(file_path):
        if debug_mode:
            print("Old hosts file exists, deleting and making a new one")
            os.remove(file_path)
    
    with open(file_path, 'w') as hosts_file:
        # throw in the localhost lines manually
        hosts_file.write("127.0.0.1\tlocalhost localhost.localdomain localhost6 localhost6.localdomain6\n")
        hosts_file.write("::1     \tlocalhost localhost.localdomain localhost6 localhost6.localdomain6\n")
        for server in list_of_servers:
            hosts_file.write(f"{server.ip_address}\t{server.fqdn}\t{server._hostname}\n")
        if debug_mode:
            print("Hosts file successfully created")

def copy_hosts_file(remote_server: Server, debug_mode: bool) -> None:
    path_of_temp_hosts_file = "hosts"
    remote_path='/etc/hosts'

    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the server
        if debug_mode:
            print(f"Attempting SSH with {remote_server.ip_address} using User:{remote_server._username} & Pass:{remote_server._password}")
        ssh.connect(remote_server.ip_address, username=remote_server._username, password=remote_server._password, timeout=10)

        # Copy the local hosts file to the remote server
        with open(path_of_temp_hosts_file, 'r') as local_file:
            if debug_mode:
                print("Attempting copy")
            ssh.exec_command(f'sudo sh -c "cat > {remote_path}"', stdin=local_file)
            if debug_mode:
                print("Host file deployed")
    except TimeoutError:
        print(f"Connetion timed out for {remote_server.ip_address}\tDid not deploy hosts file ⚠️")
    except OSError:
        print(f"Network is unreachable when attempting to ssh to {remote_server.ip_address}\tDid not deploy hosts file ⚠️")
    finally:
        # Close the SSH connection
        ssh.close()

def main(servers: list[Server], domain_name: str, deploy: bool, debug_mode: bool) -> None:
   
    # use domain and assign it fqdn domain for all servers 
    generate_fqdns(domain_name, servers)
 
    # make the host file in the local directory
    generate_hosts_file(servers, debug_mode)

    # Copy hosts file to each server
    if deploy:
        for server in servers:
            copy_hosts_file(server, debug_mode)


if __name__ == "__main__":
    # For Testing
    Test_List_of_Servers = [
        Server("DG1234", "192.168.8.3", "3N1D", "subnet1", 10, 20, "usernaem", "p123"),
        Server("DG1234", "192.168.8.4", "3N1D", "subnet1", 10, 20, "u", "p"),
        Server("DG1234", "192.168.8.5", "3N1D", "subnet1", 10, 20, "u", "p"),
        Server("DG1234", "192.168.8.6", "3N1D", "subnet2", 10, 20, "u", "p"),
        Server("DG1234", "192.168.8.7", "3N1D", "subnet2", 10, 20, "u", "p")
    ]
    test_fqdn = "fake.company.com"
    deploy = True
    debug = False

    main(Test_List_of_Servers, test_fqdn, deploy, debug)
    
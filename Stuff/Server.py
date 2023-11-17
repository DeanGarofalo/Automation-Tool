import ipaddress

class Server:
    
    
    def __init__(self, hostname: str, ip_address: ipaddress, ha_type: str, subnet: str, x_coord, y_coord ) -> None:
        self.hostname: str = hostname
        self.ip_address: ipaddress = ip_address
        self.ha_type: str = ha_type
        self.subnet: str = subnet
        self.x_coord = x_coord
        self.y_coord = y_coord

    def __str__(self):
        return f"""
Hostname: {self.hostname}
IP Address: {self.ip_address}
HA Type: {self.ha_type}
Subnet: {self.subnet}
X-coord: {self.x_coord}
Y-coord {self.y_coord}"""
    
    def connect():
        ...
        #interesting idea, do i add a connect function here or make that its own funciton that takes in a server?
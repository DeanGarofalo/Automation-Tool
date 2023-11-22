from ipaddress import IPv4Address #
from ipaddress import AddressValueError

class Server:
    
    
    def __init__(self, hostname: str, ip_address: IPv4Address, ha_type: str, subnet: str, x_coord: int, y_coord: int, username: str, password: str ) -> None:
        self._hostname: str = hostname.strip()
        self.ip_address: str = ip_address
        self._ha_type: str = ha_type.strip()
        self._subnet: str = subnet.strip()
        self._x_coord: int = x_coord
        self._y_coord: int = y_coord
        self._username: str = username
        self._password: str = password

    def __str__(self):
        return f"""
Hostname: {self._hostname}
IP Address: {self.ip_address}
HA Type: {self._ha_type}
Subnet: {self._subnet}
Username: {self._username}
Password: {self._password}
Coords: [{self._x_coord}, {self._y_coord}]
"""
    
    @property
    def ip_address(self) -> str:
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address: str) -> None:
        if not is_valid_ip(ip_address.replace(" ", "")):
            raise ValueError(f"Invalid IP of {ip_address.replace(' ' , '')}")
        self._ip_address = ip_address.replace(" ", "")

 # The logic here was to validate the IP by checking if it was in a IPv4 format AND a private address
 # But then I looked at old workbooks and remembered some IT departments do some wack **** and assign allocated public IP's on private internal networks
 # So I can't also deem it must be private, so this is just going to stay here and maybe I'll use it later to throw a warning to the user as a fyi
def is_private_ipv4(ip: IPv4Address):
    try:
         # Create an IPv4 address object
        ip_obj = IPv4Address(ip.replace(" ", ""))
        # Check if the address is in one of the private ranges
        return ip_obj.is_private
    except AddressValueError:
        return False
    
def is_valid_ip(ip: IPv4Address) -> bool:
    try:
        ip_obj = IPv4Address(ip.replace(" ", ""))
        return True
    except AddressValueError:
        return False
import ipaddress

from ipaddress import IPv4Address

class Server:
    
    
    def __init__(self, hostname: str, ip_address: IPv4Address, ha_type: str, subnet: str, x_coord, y_coord ) -> None:
        self._hostname: str = hostname
        self.ip_address: IPv4Address = ip_address
        self._ha_type: str = ha_type
        self._subnet: str = subnet
        self._x_coord = x_coord
        self._y_coord = y_coord

    def __str__(self):
        return f"""
Hostname: {self._hostname}
IP Address: {self.ip_address}
HA Type: {self._ha_type}
Subnet: {self._subnet}
X-coord: {self._x_coord}
Y-coord {self._y_coord}"""
    
    @property
    def ip_address(self) -> IPv4Address:
        return self.ip_address

    @ip_address.setter
    def ip_address(self, ip_address: IPv4Address) -> None:
        if is_private_ipv4(ip_address):
            self.ip_address = ip_address
        raise ValueError(f"Invalid IP of {ip_address}")


 
def is_private_ipv4(ip: IPv4Address):
    try:
         # Create an IPv4 address object
        ip_obj = ipaddress.IPv4Address(ip)

        # Check if the address is in one of the private ranges
        return ip_obj.is_private
    except ipaddress.AddressValueError:
        return False
from Stuff.Server import Server, is_private_ipv4
from ipaddress import IPv4Address
import pytest

def test_server_creation():
    hostname = "DG1234"
    ip_address = IPv4Address("192.168.1.1")
    ha_type = "3N2D"
    subnet = "subnet1"
    x_coord = 10
    y_coord = 20

    server_instance = Server(hostname, ip_address, ha_type, subnet, x_coord, y_coord)

    assert server_instance._hostname == hostname
    assert server_instance.ip_address == ip_address
    assert server_instance._ha_type == ha_type
    assert server_instance._subnet == subnet
    assert server_instance._x_coord == x_coord
    assert server_instance._y_coord == y_coord

def test_invalid_ip():
    with pytest.raises(ValueError):
        invalid_ip_address = IPv4Address("256.256.256.256")
        Server("DG1234", invalid_ip_address, "3N2D", "subnet", 10, 20)

def test_private_ip():
    valid_private_ip = IPv4Address("192.168.1.1")
    valid_server = Server("DG1234", valid_private_ip, "3N1D", "subnet1", 10, 20)

    assert valid_server.ip_address == valid_private_ip

def test_invalid_private_ip():
    with pytest.raises(ValueError):
        invalid_private_ip = IPv4Address("1.1.1.1")  
        Server("DG1234", invalid_private_ip, "3N1D", "subnet1", 10, 20)

def test_is_private_ipv4():
    assert is_private_ipv4(IPv4Address("192.168.1.1"))
    assert not is_private_ipv4(IPv4Address("1.1.1.1"))
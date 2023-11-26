from Stuff.Server import Server, is_private_ipv4, is_valid_ip
from ipaddress import IPv4Address
from ipaddress import AddressValueError
import pytest


Test_List_of_Servers = [
    Server("DG1234", "192.168.1.1", "3N1D", "subnet1", 10, 20, "u", "p"),
    Server("DG1234", "192.168.1.1", "3N1D", "subnet1", 10, 20, "u", "p"),
    Server("DG1234", "192.168.1.1", "3N1D", "subnet1", 10, 20, "u", "p"),
    Server("DG1234", "192.168.1.1", "3N1D", "subnet2", 10, 20, "u", "p"),
    Server("DG1234", "192.168.1.1", "3N1D", "subnet2", 10, 20, "u", "p")
]

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
        #rethink this test
        #Server("DG1234", invalid_ip_address, "3N2D", "subnet", 10, 20)

def test_private_ip():
    valid_private_ip = "192.168.1.1"
    valid_server = Server("DG1234", valid_private_ip, "3N1D", "subnet1", 10, 20, "u", "p")

    assert valid_server.ip_address == valid_private_ip

def test_invalid_private_ip():
    with pytest.raises(ValueError):
        invalid_private_ip = "1.1.1.1"  
        Server("DG1234", invalid_private_ip, "3N1D", "subnet1", 10, 20, "u", "p")

def test_is_private_ipv4():
    assert is_private_ipv4("192.168.1.1")
    assert not is_private_ipv4("1.1.1.1")

def test_is_an_ip():
    assert is_valid_ip("1.1.1.1") == True

def test_is_an_ip2():
    assert is_valid_ip("1.1.1.1") == True

def test_not_an_ip():
    assert is_valid_ip("1223.221.463.999") == False

def test_not_an_ip2():
    with pytest.raises(AddressValueError):
        is_valid_ip("123.4444.544.231")

def test_weird_167_condition():
    assert is_valid_ip("167") == False
    assert is_private_ipv4("167") == False


from Stuff.Server import Server
from Stuff.Specs import check_specs_b_app, check_specs_c_app, check_specs_d_app, check_specs_s_app

"""
These are all just checking against the specs listed in the dict for what the min spec is.
Testing the retrieval of the specs is hard because of the reliance on SSH.
Some apps have more specific requirments depending on the type of server and type of deployment, therefore more test cases.
"""

# a connector with the exact better than min spec
def test_b_connector_good():
    test_server = Server("DG1234", "10.10.10.10", "Connector", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 6, "RAM": 16, "Disk": 250}
    response = check_specs_b_app(test_server, specs)
    assert response == "Valid"
# a connector with low disk
def test_b_connector_bad_disk():
    test_server = Server("DG1234", "10.10.10.10", "Connector", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 6, "RAM": 16, "Disk": 200}
    response = check_specs_b_app(test_server, specs)
    assert response == "None"
# a connector with low ram
def test_b_connector_bad_ram():
    test_server = Server("DG1234", "10.10.10.10", "Connector", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 6, "RAM": 5, "Disk": 250}
    response = check_specs_b_app(test_server, specs)
    assert response == "None"
# a connector with the exact min spec
def test_b_connector_exact_spec():
    test_server = Server("DG1234", "10.10.10.10", "Connector", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 4, "RAM": 8, "Disk": 250}
    response = check_specs_b_app(test_server, specs)
    assert response == "Valid"
# test a B node with low traffic specs
def test_b_app_low():
    test_server = Server("DG1234", "10.10.10.10", "Node", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 4, "RAM": 16, "Disk": 250}
    response = check_specs_b_app(test_server, specs)
    assert response == "Low Traffic"
# test a B node with high traffic specs
def test_b_app_high():
    test_server = Server("DG1234", "10.10.10.10", "Node", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 7, "RAM": 33, "Disk": 251}
    response = check_specs_b_app(test_server, specs)
    assert response == "High Traffic"
# test a B node with ultra traffic specs
def test_b_app_ultra():
    test_server = Server("DG1234", "10.10.10.10", "Node", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 7, "RAM": 64, "Disk": 251}
    response = check_specs_b_app(test_server, specs)
    assert response == "Ultra Traffic"
# test a B node with bad specs
def test_b_app_bad():
    test_server = Server("DG1234", "10.10.10.10", "Node", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 7, "RAM": 64, "Disk": 200}
    response = check_specs_b_app(test_server, specs)
    assert response == "None"

# test C app with bad spec
def test_c_app_low_spec():
    test_server = Server("DG1234", "10.10.10.10", "Application Server", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 4, "RAM": 64, "Disk": 200}
    deployment_type = "Single Server"
    response = check_specs_c_app(test_server, specs, deployment_type)
    assert response == "None"
# test C app with good specs
def test_c_app_good_spec():
    test_server = Server("DG1234", "10.10.10.10", "Application Server", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 8, "RAM": 16, "Disk": 210}
    deployment_type = "Single Server"
    response = check_specs_c_app(test_server, specs, deployment_type)
    assert response == "Limited capacity"
# test C rep with good specs
def test_c_rep_good_spec1():
    test_server = Server("DG1234", "10.10.10.10", "Primary Reporting", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 8, "RAM": 17, "Disk": 210}
    deployment_type = "Single Server with Reporting"
    response = check_specs_c_app(test_server, specs, deployment_type)
    assert response == "Limited capacity"
# test C rep with bad specs
def test_c_rep_good_spec2():
    test_server = Server("DG1234", "10.10.10.10", "Primary Reporting", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 8, "RAM": 10, "Disk": 210}
    deployment_type = "Single Server with Reporting"
    response = check_specs_c_app(test_server, specs, deployment_type)
    assert response == "None"
# test C app with good specs for a ha
def test_c_app_ha_good_spec():
    test_server = Server("DG1234", "10.10.10.10", "Application Server", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 16, "RAM": 64, "Disk": 222}
    deployment_type = "HA with blah blah"
    response = check_specs_c_app(test_server, specs, deployment_type)
    assert response == "Full capacity"
# test C app with bad specs for a ha
def test_c_app_ha_low_spec():
    test_server = Server("DG1234", "10.10.10.10", "Application Server", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 4, "RAM": 64, "Disk": 200}
    deployment_type = "HA"
    response = check_specs_c_app(test_server, specs, deployment_type)
    assert response == "None"
# test C rep with bad specs in ha
def test_c_rep_ha_low_spec():
    test_server = Server("DG1234", "10.10.10.10", "Primary Reporting", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 16, "RAM": 24, "Disk": 250}
    deployment_type = "HA"
    response = check_specs_c_app(test_server, specs, deployment_type)
    assert response == "None"
# test C rep with good specs in ha
def test_c_rep_ha_good_spec():
    test_server = Server("DG1234", "10.10.10.10", "Primary Reporting", "subnet1", 1, 2, "user", "pass")
    specs = {"CPU": 16, "RAM": 36, "Disk": 250}
    deployment_type = "HA"
    response = check_specs_c_app(test_server, specs, deployment_type)
    assert response == "Full capacity"

# test D app with good specs
def test_d_app_good_spec():
    specs = {"CPU": 6, "RAM": 16, "Disk": 250}
    response = check_specs_d_app(specs)
    assert response != "None"
# test D app with bad specs
def test_d_app_bad_spec():
    specs = {"CPU": 4, "RAM": 8, "Disk": 250}
    response = check_specs_d_app(specs)
    assert response == "None"

# test S app with good specs
def test_s_app_good_specs():
    specs = {"CPU": 4, "RAM": 32, "Disk": 150}
    response = check_specs_s_app(specs)
    assert response != "None"
# test S app with bad specs
def test_s_app_bad_spec():
    specs = {"CPU": 6, "RAM": 31, "Disk": 150}
    response = check_specs_s_app(specs)
    assert response == "None"


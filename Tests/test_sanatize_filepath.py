from somepython import sanatize_filepath


def test_good_input():
    assert sanatize_filepath("/home/dean/test.xlsx") == "/home/dean/test.xlsx"

def test_tidle():
    assert sanatize_filepath("~/test.xlsx") == "/home/dean/test.xlsx"

def test_tilde_no_file():
    assert sanatize_filepath("~") == "/home/dean"

def test_emtpy():
    assert sanatize_filepath("") == "/home/dean/Programming/Automation-Tool/"

# I should respect the file type letter case 
def test_caps_extension():
    assert sanatize_filepath("/home/dean/test.XLSX") == "/home/dean/test.XLSX"

    
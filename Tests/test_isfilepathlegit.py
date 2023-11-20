from somepython import is_filepath_legit
## Bad inputs

# These two tests actually corrected my code
def test_not_excel():
    assert is_filepath_legit("not.xls") is False
def test_not_excel_full_path():
    assert is_filepath_legit("/home/dean/not.xls") is False

def test_not_excel_tilde():
    assert is_filepath_legit("~/not.xls") is False

# Good excel but we dont like the ~ so this test necesitates the sanatize_filepath function
def test_valid_excel_tilde():
    assert is_filepath_legit ("~/test.xlsx") is False

# Good excel but we dont like caps file extension necesitates the sanatize_filepath function
def test_valid_excel_Caps_extension():
    assert is_filepath_legit("test.XLSX") is False

def test_default():
    assert is_filepath_legit("") is False

#########################################################################################################

## Good inputs

def test_valid_excel():
    assert is_filepath_legit("test.xlsx") is True

def test_valid_excel_fullpath():
    assert is_filepath_legit("/home/dean/test.xlsx") is True

def test_caps_excel():
    assert is_filepath_legit("/home/dean/not.XLSX") is True



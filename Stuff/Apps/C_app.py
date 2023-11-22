from openpyxl import load_workbook
### I HATE python SO much for making me do this utter bs to import from a parent directory
import os
import sys
current_directory = os.path.dirname(os.path.realpath(__file__))
project_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.append(project_directory)
print(current_directory)
print(project_directory)
#from Stuff import Server
from Stuff.Server import Server, is_valid_ip
from Stuff.Apps.Helper_functions import is_cell_green, is_cell_orange, get_cell_fill_color

## These guys are the general assumption I make where the relevant data should be.
## Changing them widens or tightens the search area the count function runs on, and effect the speed and accuracy of the server discovery
MAX_ROW_RANGE = 28
MIN_ROW_RANGE = 7

MAX_COL_RANGE = 5
MIN_COL_RANGE = 1
# Change if the search area is too small its missing servers, or too big its grabbing other non relevant servers



def main():
    # Change to test whole program
    workbook = load_workbook(filename="/home/dean/test.xlsx", read_only=True)
    sheet_name = workbook["C"]
    test_list = []
    print("Counted:", count_C_app_servers(sheet_name, test_list, get_C_app_implementation_type(sheet_name)))
    
    
    
    
    
    # Test print out the list of Servers
    for server in test_list:
        print(server)


 


















  



def get_C_app_implementation_type(sheet_name) -> str:
    """
    Grabs the Implementation type cell
    This is important because I use it to validate the environment makes sense as in its a supported type of deployment,
    and helps filter out possible ambiguous servers that should not be looked at.

    Args:
        sheet_name (Openpyxl.Workbook.Sheet): Excel Workbook sheet

    Raises:
        ValueError: Throws a value error if we couldn't determine the implementation_type. So it must stop.

    Returns:
        str: Returns the implementation_type str var
    """
    implementation_type: str = ""
    implementation_type = str(sheet_name.cell(row = 3, column = 2).value)
    
    match implementation_type:
        case "Migration":
            print("Determined Implementation type as:", implementation_type)
            print("**************************************************************")
            print("Please Highlight New Servers Green aka \"Good input in excel\"")
            print("**************************************************************")
        case "Upgrade":
            print("Determined Implementation type as:", implementation_type)
        case "New":
            print("Determined Implementation type as:", implementation_type)
        case _:
            raise ValueError("Unable to determine Implementation type of this deployment\nEnsure that the drop down box in cell B3 is set.")
    return implementation_type
    

 
def count_C_app_servers(sheet_name, list_of_servers, implementation_type) -> int:
    """
    Counts the valid recongized servers and builds the Server object list

    Args:
        sheet_name (Openpyxl.Workbook.Sheet): Excel Workbook sheet
        list_of_servers (list): Empty list which will be a list of "Server" objects
        implementation_type (str): The string corresponding to the implementation type

    Returns:
        int: the number of servers counted
    """
    count = 0
    if implementation_type == "Migration":
        # check for green cells in counting because migrations have the old and new servers which would lead to ambiguous counts
        for row in range(MIN_ROW_RANGE, MAX_ROW_RANGE):
            for column in range(MIN_COL_RANGE, MAX_COL_RANGE):
                # If the cell is empty move along
                if sheet_name.cell(row, column).value != None:
                    if is_valid_ip(str(sheet_name.cell(row, column).value)) and is_cell_green(sheet_name, row, column):
                        # Debug
                        # print(str(sheet_name.cell(row, column).value), "Coord:", row, column)
                        list_of_servers.append(Server(sheet_name.cell(row, column-1).value, sheet_name.cell(row, column).value, sheet_name.cell(row, column+2).value, sheet_name.cell(row, column+1).value, row, column))
                        count += 1       
    else:
        for row in range(MIN_ROW_RANGE, MAX_ROW_RANGE):
            for column in range(MIN_COL_RANGE, MAX_COL_RANGE):
                # If the cell is empty move along
                if sheet_name.cell(row, column).value != None:
                    if is_valid_ip(str(sheet_name.cell(row, column).value)) and (is_cell_green(sheet_name, row, column) or is_cell_orange(sheet_name, row, column) ):
                        # Debug
                        # print(str(sheet_name.cell(row, column).value), "Coord:", row, column)
                        list_of_servers.append(Server(sheet_name.cell(row, column-1).value, sheet_name.cell(row, column).value, sheet_name.cell(row, column+2).value, sheet_name.cell(row, column+1).value, row, column))
                        count += 1
    #TODO double check the logic here^
    return count




























if __name__ =="__main__":
    main()
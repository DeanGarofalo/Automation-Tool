from openpyxl import load_workbook
# import openpyxl #might need other functions
### I HATE python SO much for making me do this utter bs to import from a parent directory
import os
import sys
current_directory = os.path.dirname(os.path.realpath(__file__))
project_directory = os.path.dirname(os.path.dirname(current_directory))
sys.path.append(project_directory)
print(current_directory)
print(project_directory)
from Stuff import Server
###

def get_C_app_implementation_type(sheet_name) -> str:
    implementation_type: str = ""
    # print(sheet_name['C18'].value)
    # print(sheet_name.max_row)
    # print(sheet_name.max_column)
    #Server.Server("Test", "192.168.1.1", "HA", "subnet1", 20, 30)
    # for value in sheet_name.iter_rows(min_row=1, max_row=23, min_col=1, max_col=17, values_only=True):
    #     print(value)
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



def count_C_app_servers(sheet_name, list_of_servers) -> int:
    count = 0
    for i in range(7, 28):
        for j in range(1, 5):
            if sheet_name.cell(i, j).value != None:
                if Server.is_valid_ip(str(sheet_name.cell(i, j).value)):
                    print(str(sheet_name.cell(i, j).value), "Coord:", i,j)
                    count += 1
    
    
    
    return count



def main():
    # Change to test whole program
    workbook = load_workbook(filename="/home/dean/test.xlsx", read_only=True)
    sheet_name = workbook["C"]
    print("Left function with:",get_C_app_implementation_type(sheet_name))
    test_list = []
    
    print(sheet_name.cell(2,2).value)

    print("Counted:", count_C_app_servers(sheet_name, test_list))
    
    # Testing traversal and object creation 
    Test = Server.Server("Test", "192.168.1.1", "HA", "subnet1", 20, 30)
    print(type(Test.ip_address))

    # for i in range(7, 28):
    #     for j in range(1, 5):
    #         if Server.is_valid_ip(str(sheet_name.cell(i, j).value)):
    #             print(str(sheet_name.cell(i, j).value), "Coord:", i,j)



if __name__ =="__main__":
    main()
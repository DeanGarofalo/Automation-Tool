"""
Since my code base got very, very messy in C#. I have to put some time into thinking about how this will be organzied.
Do I split each application into folders and classes within it? Sounds dumb
Do I design each helper function as a class and build the driver as a individual app or one big driver?
Or not think at all and start writing code until I see the problem. Likely.
"""

"""
High level functions i need:

☑️ Find_Apps():                     Discover what valid applications are in the workbook, and return those options back to the user to decide what they want to work on, and then launch that apps routine.
🚧 Server class(ip,,pass,etc):      Build the class for the server object for how ill store all the servers information im parsing excel for
Build_server_object():              Parse the workbook and build out a data structure of the servers found
Is_valid_config():                  Returns a boolean for if the config is valid or not. If its not valid exit and tell the user to fix the excel


These will be called after the user provides which app they want to work on.
    These will need to take in a int of the number of servers and possibly the type name in a cell
    Find_deployment_type_App-C():     Determine what type of deployment the app is.
    Find_deployment_type_App-B():
    Find_deployment_type_App-D():
    Find_deployment_type_App-S():

Helper functions I need:
    Count_servers():
    Is_valid_IPAddress():
    Is_valid_HA():      Basically look at the count servers output and compare it with what the excel cell says it should be and make sure they match
    Plus way way more

SSH functions I need:
    FTP function
    Firewall function should take in a app and maybe take those ports in as a global var?
    Bash command function
    More I'm forgetting at the moment

TODO ☑️ rewrite support commandline args, should see if i want to do it by hand or use argparse as well. Might be better off because its more versatile    
    
"""
from openpyxl import load_workbook
from Stuff.Server import Server
import argparse
import sys
import os

def main():
    # First driver to get the file as input, either through commandline argument on launch or through interactive user input
    parser = argparse.ArgumentParser(prog="Automation App", description="This script takes in a .XLSX file and run sysadmin like functions on its contents.")
    parser.add_argument('filename')
    parser.add_argument("-v", default=1, help="verbose logging", type=int)
    
    final_filename = ""   
    if len(sys.argv) >= 2:
        args = parser.parse_args()
        # Clean up filename for a few scenarios
        args.filename = sanatize_filepath(args.filename)
        if is_filepath_legit(args.filename):
                final_filename = args.filename
        else:
            while True:
                args.filename = input("Please enter the Excel file path to use: ")
                if is_filepath_legit(args.filename):
                    final_filename = args.filename
                    break
    else:
        print("No arguments provided.")
        while True:
            file_path = input("Please enter the Excel file path to use: ")
            file_path = sanatize_filepath(file_path)
            if is_filepath_legit(file_path):
                final_filename = file_path
                break
    # DEBUG
    print("File path:", final_filename)
    # Replace filename here with final_filename. Hardcoded to make my life easier for now.
    wb = load_workbook(filename = '/mnt/c/Users/dgame/Downloads/Excels/V2/test.xlsx', read_only=True)

    selected_app = Find_apps(wb)

    match selected_app:
        case "C" | "C5" | "CB" :
            sheet = wb[selected_app]
            # run C function
            # C(sheet)
            print("Run C")
            ...
        case "B":
            sheet = wb[selected_app]
            # run B function
            # B(sheet)
            print("Run B")
            ...
        case "S":
            sheet = wb[selected_app]
            # run S function
            # S(sheet)
            ...
        case _:
            raise ValueError("Invalid Sheet. Exiting")


    test_Server = Server("DG1234", "192.168.0.1", "HA2R", "subnet1", 22, 17)
    print(test_Server)

    print(sheet['C18'].value)
    print("Gotta start somewhere right?")



def sanatize_filepath(file_path: str) -> str:
    if str(file_path).startswith("~"):
        file_path = os.path.expanduser(file_path)
    # Check if its a local or relative path, if local add the full path to the filename
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.getcwd(), file_path)
    return file_path

def is_filepath_legit(file_path: str) -> bool:
    if os.path.exists(file_path) and os.path.isfile(file_path):
        if not str(file_path).lower().endswith(".xlsx"):
            print("Not an Excel file. Try again")
            return False
        else:
            return True
    else:
        print("Invalid file path or file does not exist. Please enter a valid file path.")
        return False





def Find_apps(workbook):
    # var with supported apps, maybe should be global instead of here?
    allowed_sheets = ["C", "C5", "D", "B", "S", "Networks", "VoIP"]

    # Get the sheet names
    sheet_names = workbook.sheetnames

    # Print the allowed sheet names with corresponding numbers
    print("Which application would you like to work on?")
    allowed_sheet_indices = []
    for i, name in enumerate(sheet_names, start=1):
        if name in allowed_sheets:
            allowed_sheet_indices.append(i)
            print(f"{len(allowed_sheet_indices)}. {name}")

    # Ask the user for input
    while True:
        try:
            selected_number = int(input("Enter the number of the sheet you want to use: "))
            # If input is in between a valid range
            if 1 <= selected_number <= len(allowed_sheet_indices):
                selected_sheet_index = allowed_sheet_indices[selected_number - 1]
                selected_sheet = sheet_names[selected_sheet_index - 1]
                break
            else:
                print("Invalid number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return selected_sheet








###############################################################         EOF          ###########################################################################################################################
if __name__ == "__main__":
    main()
# What is this?
This is my attempt at learning Python by reimagining one of my prior C# applications in Python minus a GUI.

# What does this do exactly?
The as aforementioned Automation-Tool would take in a specific type of formatted *"Excel"* file, and run *"operations"* based on a user's selected input through checkboxes on a Windows GUI.

Okay that's still pretty vague, can you be more specific? What's in the Excel and what are the operations it can do?

## The Excel file
Let's say you have a workbook of server credentials, filled with IP addresses, FQDN's, subnets, passwords, etc. And suppose each of those servers are various types of application servers which can be databases, unique applications, or smaller components of large horizontally scaled applications. The workbook provides a human readable format of a particular client's environment and its footprint. 

## The Operations
This tool was initially designed to automate some of the tedious work that someone would have to do in order to access a certain environment, like: 
- setup numerous SSH tunnels (through a created PuTTY profile)
- connecting and checking a deployed server's hardware specifications
- building and deploying a network _hosts_ file
- opening specific firewall ports for specific applications on each unique server
- launching a proprietary VPN which all SSH tunnels would be funneled through

There were also some optional features such as:
- Constructing a Super PuTTY template for each of the types of supported applications in their various deployment types. All of the SSH tunnels are created to support this in the creation of the PuTTY profile.
- An advanced mode which would let you manually specify a server and 
    - check specifications
    - deploy a file
    - run a generic firewall script
    - run a shell command
    - launch the proprietary VPN 

# Why
I will be attempting to recreate some if not most of this functionality as a learning experiment or until I get bored.

Since I really don't want to learn how to make a GUI again, this time the ideal is to run this as a command line script on the Excel file, have it grab the types of application servers recognized and then prompt the user via command line for what they want to do next. 

Since I'm going to be designing this in a Linux environment this time and not a Windows one, I may explore ditching PuTTY all together. TBD.

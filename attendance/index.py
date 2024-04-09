from register import *
from markattendance import *

# Define the menu
def print_menu():
    print("""
Enter number according to your choice
1. Register
2. Mark Attendance
3. Help
4. Exit
""")

# Run the program
while True:
    print_menu() # Print the menu

    option = int(input("Enter your choice: ")) # Get the user's choice

    if option == 1: # If the user wants to register
        register() # Call the register function

    elif option == 2: # If the user wants to mark attendance
        markattendance() # Call the markattendance function

    elif option == 3: # If the user wants help
        print("""\n\n
1. If you haven't created a profile, enter 1 and fill in the required details. You need to enter your name, class, jssid, and then look at the camera so that your photo can be saved.
2. If you have a profile, enter 2 and look at the camera. If your face is recognised by the program your attendance will marked automatically.\n
""") # Print the help information

    elif option == 4: # If the user wants to exit
        print("Thank you for using our program.".capitalize()) # Print a message
        break # Exit the program

    else: # If the user entered an invalid option
        print("Invalid option.") # Print a message
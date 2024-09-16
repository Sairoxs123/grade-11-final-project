from signup import *
from login import *
from change import *


print("<" + "=" * 15, "WELCOME TO OUR SECURITY SYSTEM", "=" * 15 + ">")


while True:
    print("""\nEnter numbers according to your choice of service
1. Create a profile
2. Login
3. Change security phrase
4. Help
5. Exit\n""")
    option = int(input("Enter your choice: "))

    if option == 1:
        signup()

    elif option == 2:
        login()

    elif option == 3:
        change()

    elif option == 4:
        print("""
1. If you haven't created a profile, enter 1 and fill in the required details. You need to enter your username, password, wait 5 seconds and then speak a security phrase of your choice which will be recorded.
2. If you have a profile, enter 2 and fill in the required details. You need to enter your username, password, wait 5 seconds and then speak the security phrase you registered with for verification.
""")

    elif option == 5:
        print("\nTHANK YOU FOR TRUSTING US AND USING OUR PROGRAM.\n")
        break

    else:
        print("Invalid option")


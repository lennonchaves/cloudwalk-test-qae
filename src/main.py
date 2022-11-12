# importing the module
import os
import log_parser
import log_deaths

# menu with options
while True:
    print("\t\tWELCOME to Quality Engineering Test - CloudWalk\t\t\t")

    print("\t-------------------------------------------------")

    print("Entering a option")

    print("""
        1. Log parsed and grouped information with player ranking
        2. Report of deaths grouped by death cause
        3. Exit""")

    option = int(input("Enter your choice: "))

    # perform the function according to the option selected
    if option == 1:
        # Log parsed and grouped information with player ranking
        log_parser.execute()
    elif option == 2:
        # Report of deaths grouped by death cause
        log_deaths.execute()
    elif option == 3:
        print("Exiting application")
        exit()
    else:
        print("Invalid entry")
    input("Press enter to continue")

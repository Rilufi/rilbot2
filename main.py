from twiiiiter import *
import traceback
import os

if __name__ == "__main__":
    try:
        username = os.environ.get("USER1")
        password = os.environ.get("PASS1")
        # Check if variables are set
        if username is None or password is None:
          print("Error: User credentials not set.")
          sys.exit(1)
        else:
        # Add these lines before the login attempt to print the values
        print(f"Username: {username}")
        print(f"Password: {password}")
        
        print("Hello world")
        if forever_loop == True:
            forever_loop(username, password)
        else:    
            main_one(username, password)
    except Exception as e:
        print("Bip Bip Elon Musk")
        if "Message: unknown error: net::ERR_INTERNET_DISCONNECTED" in str(e):
            print("No connection")
        else:
            print("Another type of error")
            print(traceback.format_exc())

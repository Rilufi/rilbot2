from twiiiiter import *
import traceback
import os

if __name__ == "__main__":
    try:
        username = os.environ["USER1"]
        password = os.environ["PASS1"]
        
        print("Hello world")
        if forever_looop == True:
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

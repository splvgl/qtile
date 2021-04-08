#!/usr/bin/python3
import subprocess

# a function that serves pacman a dot for every update you have

# max_dots is the maximum amount of dots to show, 
# any additional updates will be displayed as "…"

def pacman_dots():
    max_dots = 10
    # running update_cmd, storing stdout in list
    updates = subprocess.run("checkupdates", capture_output=True, text=True).stdout.split('\n')
    # generating outsting of dots
    dots = ""
    if updates == ['']:
        dots = "◦"
    else:
        for i in range(len(updates)-1):
            if i == max_dots:
                dots = "…" + dots
                break
            dots += "•"
    return dots

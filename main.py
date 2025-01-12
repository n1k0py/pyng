import os
import time
import platform
import subprocess
from itertools import cycle

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            output = result.stdout
            if platform.system().lower() == "windows":
                time_part = [line for line in output.split("\n") if "time=" in line][0]
                ms = int(time_part.split("time=")[1].split("ms")[0].strip())
            else:
                time_part = [line for line in output.split("\n") if "time=" in line][0]
                ms = float(time_part.split("time=")[1].split(" ")[0])
            return ms
        else:
            return None
    except Exception:
        return None

def display_ping_results(websites):
    states = [] 
    spinner = cycle(["-", "\\", "|", "/"])

    for _ in websites:
        states.append("Pinging...")

    while True: 
        for i, website in enumerate(websites):
            for _ in range(4): 
                os.system("cls" if os.name == "nt" else "clear")
                for j, state in enumerate(states):
                    print(f"{websites[j]:<20} {state}")
                states[i] = next(spinner)
                time.sleep(0.1)

            ping_result = ping(website)
            if ping_result is None:
                states[i] = "❌ (Failed)"
            else:
                emoji = "✅" if ping_result <= 500 else "⚠️"
                states[i] = f"{emoji} ({int(ping_result)}ms)"

        os.system("cls" if os.name == "nt" else "clear")
        for j, state in enumerate(states):
            print(f"{websites[j]:<20} {state}")
        time.sleep(2) 

if __name__ == "__main__":
    websites_to_ping = [
        "example.com",
        "google.com",
        "openai.com",
        "github.com",
        "wikipedia.org",
        "python.org",
        "stackoverflow.com",
    ]
    display_ping_results(websites_to_ping)

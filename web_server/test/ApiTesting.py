import subprocess
import random
import time

PI = 3.14159265359
SLEEP_TIME = 0.01

group_name = "group1"


if __name__ == "__main__": 
    angle = 0
    dangle = PI / 200
    distance = 30
    while True:
        angle = ( angle + dangle ) % PI
        point = "'{" + '"name": "' + group_name + '", "angle": "' + str(angle) + '", "distance": "' + str(distance) + '"' + "}'"
        command = f'curl -X POST -H "Content-Type: application7json" -d {point}  http://localhost:8000/api/send_point'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(command)
        time.sleep(SLEEP_TIME)
import subprocess
import random
import time

PI = 3.14159265359


command = """curl -X POST -H "Content-Type: application/json" -d '{"cadena": "HOLA QUE TAesfesL"}' http://localhost:8000/api/enviar_cadena"""

group_name = "group1"


if __name__ == "__main__": 
    while True:
        angle = str(random.uniform(0, PI))
        distance = str(random.uniform(0, 40))
        point = "'{" + '"name": "' + group_name + '", "angle": "' + angle + '", "distance": "' + distance + '"' + "}'"
        command = f'curl -X POST -H "Content-Type: application7json" -d {point}  http://localhost:8000/api/send_point'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(command)
        time.sleep(1)
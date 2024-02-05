from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import helper
import urllib.parse


IP = "localhost"
PORT = 8000

POINTS = {
    "group0": {
        "points": [ #distance in cm, angle in radiants
            {"distance": 3, "angle": helper.PI}, 
            {"distance": 3, "angle": helper.PI/2}, 
            {"distance": 3, "angle": 3*helper.PI/4},
            {"distance": 3, "angle": helper.PI/4},
            {"distance": 3, "angle": helper.PI2}, 

        ],
        "number_points": 4
    }
}


# Definir un manejador de solicitudes personalizado que herede de BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if parsed_url.path == '/api/get_points':
            group_name = query_params.get('group_name', [''])[0]

            
            if not group_name in POINTS.keys():
                return
                
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # Obtener la lista de cadenas y enviarla junto con la imagen
            response_data = POINTS[group_name]
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            return
        
            
        if self.path == '/':
            # Si la solicitud GET es para '/', servir el archivo index.html
            self.path = '/index.html'
        try:
            # Abre y lee el archivo solicitado
            with open('./src/' + self.path, 'rb') as file:
                content = file.read()
            # Envía la respuesta con el contenido del archivo
            self.send_response(200)
            self.send_header("Content-type", "text/" + self.path.split(".")[-1])
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            # Si el archivo no se encuentra, enviar una respuesta 404
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write('404 Not Found'.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(post_data)
            
            group_name = helper.validate_group_name(data.get('name', ''))
            angle = helper.validate_angle(data.get('angle', ''))
            distance = helper.validate_distance(data.get('distance', ''))

            if group_name and angle and distance:            
                response_message = f"Solicitud POST recibida con éxito. Group {group_name}, Angle {angle}, distance {distance}"
                helper.add_point(POINTS, group_name, angle, distance)
                
                
        except json.JSONDecodeError:
            response_message = "Error al decodificar JSON en la solicitud POST"

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_message.encode('utf-8'))
        print(POINTS)
        
        

# Configurar el servidor con el manejador de solicitudes personalizado
def run_server(ip = "", port=8000):
    server_address = (ip, port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Servidor en ejecución en el puerto {port}")
    httpd.serve_forever()

# Ejecutar el servidor en el puerto 8000 (puedes cambiarlo si lo deseas)
run_server(IP, PORT)



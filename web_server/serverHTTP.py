from http.server import BaseHTTPRequestHandler, HTTPServer
import json

IP = "localhost"
PORT = 8000


# Definir un manejador de solicitudes personalizado que herede de BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
    cadenas_recibidas = []
    
    def do_GET(self):
        if self.path == '/api/obtener_cadenas':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # Obtener la lista de cadenas y enviarla junto con la imagen
            response_data = {'cadenas_recibidas': RequestHandler.cadenas_recibidas}
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
            self.send_header("Content-type", "text/html")
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
            cadena = data.get('cadena', '')
            self.cadenas_recibidas.append(cadena)
            response_message = f"Solicitud POST recibida con éxito. Cadena recibida: {cadena}"
        except json.JSONDecodeError:
            response_message = "Error al decodificar JSON en la solicitud POST"

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_message.encode('utf-8'))
        
        print(self.cadenas_recibidas)
        

# Configurar el servidor con el manejador de solicitudes personalizado
def run_server(ip = "", port=8000):
    server_address = (ip, port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Servidor en ejecución en el puerto {port}")
    httpd.serve_forever()

# Ejecutar el servidor en el puerto 8000 (puedes cambiarlo si lo deseas)
run_server(IP, PORT)



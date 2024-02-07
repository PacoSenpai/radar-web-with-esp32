from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import helper
import urllib.parse

import concurrent.futures



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
        "points_number": 4
    }
}


# Definir un manejador de solicitudes personalizado que herede de BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):      
    
    def do_GET(self):
        self.server.logger.debug(f"Recived GET request from {self.client_address[0]}")

        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        self.server.logger.debug(f"Recived url {parsed_url}")
        
        #Do not enable search for files out the directory
        if ".." in parsed_url.path:
            return
        
        elif parsed_url.path == '/api/get_points':
            self._handle_api_get_points(query_params)
            return
            
        elif parsed_url.path == '/':
            # If the GET request is for '/', serve the file index.html
            parsed_url = parsed_url._replace(path='/index.html')
            
        self._send_file(parsed_url.path)

    def do_POST(self):
        self.server.logger.debug(f"Recived GET request from {self.client_address[0]}")
        
        parsed_url = urllib.parse.urlparse(self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        if parsed_url.path == "/api/send_point":
            response_message = self._handle_api_send_point(post_data)
        
        else:
            response_message = "Wrong POST Path. It should be /api/send_point."
            
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_message.encode('utf-8'))
          
    def _send_file(self, path: str):
        try:
            # Open and read the requested file
            with open('./src/' + path, 'rb') as file:
                content = file.read()

            # Send the response with the file content
            self.send_response(200)
            self.send_header("Content-type", "text/" + path.split(".")[-1])
            self.end_headers()
            self.wfile.write(content)
            
        except FileNotFoundError:
            # If the file is not in the sistem, send a 404 response
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write('404 Not Found'.encode("utf-8"))
    
    def _get_data_from_post_api(self, post_data: str):
        """Returns group_name, angle and distance from the post_data
        """
        data = json.loads(post_data)
        self.server.logger.debug(f"Data {data} recived")
        
        group_name = helper.validate_group_name(data.get('name', ''))
        angle = helper.validate_angle(data.get('angle', ''))
        distance = helper.validate_distance(data.get('distance', ''))
        
        return group_name, angle, distance

    def _handle_api_get_points(self, query_params: dict):
        """Function to handle the requests from the API getPoints
        """
        self.server.logger.debug("Get Points API request recived")
        
        group_name = query_params.get('group_name', [''])[0]
            
        if not group_name in POINTS.keys():
            self.server.logger.error(f"{group_name} not in POINTS group name's")
            return
        
        self.server.logger.debug(f"Group: {group_name}")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Get the list of points and send them
        response_data = POINTS[group_name]
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        
        # Restart its points
        POINTS[group_name] = {"points": [], "points_number": 0}

    def _handle_api_send_point(self, post_data: str):
        """Function to handle the requests from the API sendPoints
        """
        self.server.logger.debug("Send Points API request recived")
        
        try:
            group_name, angle, distance = self._get_data_from_post_api(post_data)
            
            if group_name and angle and distance:            
                response_message = f"Solicitud POST recibida con éxito. Group {group_name}, Angle {angle}, distance {distance}"
                helper.add_point(POINTS, group_name, angle, distance)
                
            else:
                
                response_message = "Wrong POST message. Group_name, angle or distance is not correct. Please check those values."
                
        except json.JSONDecodeError:
            response_message = "Error al decodificar JSON en la solicitud POST"
            
        return response_message
   
class CustomHTTPServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, logger, max_threads=16, ):
        self.logger = logger
        super().__init__(server_address, RequestHandlerClass)
   

# Configure the server with the personalized request handler
def run_server(ip = "localhost", port=8000):
    server_address = (ip, port)
    logger = helper.Logger(__name__)
    httpd = CustomHTTPServer(server_address, RequestHandler, logger)
    print(f"Server executing on port {port} and address {ip}")
    httpd.serve_forever()


if __name__ == '__main__':
    # Create a thread pool with 10 worker threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start the HTTP server
        start_server_thread = executor.submit(run_server, IP, PORT)

        # Wait for the HTTP server to start
        start_server_thread.result()


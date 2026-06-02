"""
Simple HTTP Server that supports writing to client_request.json
Needed because Python's http.server doesn't support PUT by default
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

class GameHTTPHandler(SimpleHTTPRequestHandler):
    """Custom handler that allows POST to update client_request.json"""
    
    def do_POST(self):
        """Handle POST requests to update client input"""
        if self.path == '/client_request.json':
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse and save the JSON data
                data = json.loads(post_data)
                with open('client_request.json', 'w') as f:
                    json.dump(data, f)
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
            except Exception as e:
                # Send error response
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f'Error: {e}'.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def end_headers(self):
        """Add CORS headers to all responses"""
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def run_server(port=8000):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, GameHTTPHandler)
    print(f"=== Game HTTP Server Starting ===")
    print(f"Serving on http://localhost:{port}")
    print(f"Open your browser to http://localhost:{port}")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

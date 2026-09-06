import http.server
import socketserver
import os

PORT = int(os.environ.get('PORT', 8000))

class VideoHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), VideoHTTPRequestHandler) as httpd:
        print(f'Serving cinematic deck at port {PORT}')
        httpd.serve_forever()

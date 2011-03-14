#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class HTTPHandler(BaseHTTPRequestHandler):
    def do_COMMAND(self, path):
        print(path)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('page.html', 'r') as f:
            self.wfile.write(f.read())
        if self.path != '/':
            self.do_COMMAND(self.path)

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.do_COMMAND(self.path)


def main():
    server = HTTPServer(('', 3000), HTTPHandler)
    print 'listening on 0.0.0.0:3000'
    server.serve_forever()

if __name__ == '__main__':
    main()

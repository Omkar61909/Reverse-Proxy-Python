from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class   (BaseHTTPRequestHandler):
    """In the following code we will insert headers in the request received by reverse_proxy 
    """
    
    def inject_auth(self, headers):
        headers['Authorizaion'] = 'Bearer secret'
        return headers 
           
    def parse_headers(self):
        req_header = {}
        for line in self.headers._headers:
            header_name = line[0]
            header_value = line[1]
            req_header[header_name] = header_value
        return self.inject_auth(req_header)

    def do_GET(self):
        updated_headers = self.parse_headers()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort),  )
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
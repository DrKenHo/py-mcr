from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from os import curdir, sep
import urllib
import mahtml
import re
from HTMLTags import *

import time

class myHandler(BaseHTTPRequestHandler):
   
    def do_GET(self):
        if re.match("/tiles/[bcdWD][123456789eswnrgw]\.png", self.path):
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.end_headers()
            filename = curdir + sep + self.path
            print filename
            f = open(curdir + sep + self.path, 'rb')
            self.wfile.write(f.read())
            f.close()
        else:
            self.printCustomHTTPResponse(200)
            query_string = urllib.unquote_plus(self.path)
            path, query = urllib.splitquery(query_string)
            print query_string, path, query
            parameters = dict(urllib.splitvalue(v) for v in query.split("&")) if query else {}
            print parameters
            if path == '/':
                self.printHelp()
            else:
                if path == '/form':
                    in_string = parameters['sit']
                else:
                    in_string = query_string[1:]
                self.wfile.write(mahtml.getAnswerOrError(in_string))

    def printHelp(self):
        fragment = H1("Help") + P("No situation given") + P(A("try this", href='/h 1234564567899b w 9b'))
        fragment = H1("Help") + P("No situation given") + P(A("Crazy", href='/c Weeee Wssss Wwwww Wnnnn h Dr w Dr'))
        fragment += FORM(INPUT(type="text", name="sit")+INPUT(type="submit", name="Go", value="Go"), 
                         method='get', action='form')
        self.wfile.write(str(fragment))

    def printBrowserHeaders(self):
        headers = self.headers.dict
        self.wfile.write("\n<ul>")
        for key, value in headers.items():
            self.wfile.write("\n<li><b>" + key + "</b>: ")
            self.wfile.write(value + "\n</li>\n")
        self.wfile.write("</ul>\n")

    def printCustomHTTPResponse(self, respcode):
        self.send_response(respcode)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

    def log_request(self, code='-', size='-'):
        user_agent = self.headers.dict['user-agent']
        self.log_message('"%s" %s %s %s',
                         self.requestline, str(code), str(size), user_agent)

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), myHandler)
        print 'Browse to http://localhost:%d/' % port
        while True:
            server.handle_request()
        #server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

# Even shorter:
"""
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write( "hello" )

    @staticmethod
    def serve_forever(port):
        HTTPServer(('', port), MyServer).serve_forever()

if __name__ == "__main__":
    MyServer.serve_forever(8080)

"""


"""
HTTPS development server for BubbleCurtain.
Uses a threaded HTTPServer with per-connection SSL wrapping.
"""
import os
import ssl
import sys
import http.server
import socketserver
import io

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
os.environ.setdefault("USE_SQLITE", "True")

import django
django.setup()

from django.core.handlers.wsgi import WSGIHandler

HOST = "0.0.0.0"
PORT = 8000

application = WSGIHandler()


class WSGIRequestHandler(http.server.BaseHTTPRequestHandler):
    """Minimal WSGI request handler."""

    def handle_one_request(self):
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                return

            # Build WSGI environ
            environ = {
                'REQUEST_METHOD': self.command,
                'SCRIPT_NAME': '',
                'PATH_INFO': self.path.split('?')[0],
                'QUERY_STRING': self.path.split('?')[1] if '?' in self.path else '',
                'SERVER_NAME': self.server.server_address[0],
                'SERVER_PORT': str(self.server.server_address[1]),
                'SERVER_PROTOCOL': self.request_version,
                'wsgi.version': (1, 0),
                'wsgi.url_scheme': 'https',
                'wsgi.input': self.rfile,
                'wsgi.errors': sys.stderr,
                'wsgi.multithread': True,
                'wsgi.multiprocess': False,
                'wsgi.run_once': False,
            }

            # Add headers
            for key, value in self.headers.items():
                key = key.upper().replace('-', '_')
                if key == 'CONTENT_TYPE':
                    environ['CONTENT_TYPE'] = value
                elif key == 'CONTENT_LENGTH':
                    environ['CONTENT_LENGTH'] = value
                else:
                    environ['HTTP_' + key] = value

            # Response handling
            response_started = []
            response_headers = []

            def start_response(status, headers, exc_info=None):
                response_started.append(status)
                response_headers.extend(headers)

            # Call Django
            result = application(environ, start_response)

            # Send response
            status_code = int(response_started[0].split(' ')[0])
            self.send_response(status_code)
            for name, value in response_headers:
                self.send_header(name, value)
            self.end_headers()

            for data in result:
                self.wfile.write(data)

            if hasattr(result, 'close'):
                result.close()

        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")

    def log_message(self, format, *args):
        sys.stderr.write(f"[HTTPS] {self.address_string()} {format % args}\n")


class ThreadedHTTPSServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("cert.pem", "key.pem")

    server = ThreadedHTTPSServer((HOST, PORT), WSGIRequestHandler)
    server.socket = context.wrap_socket(server.socket, server_side=True)

    print(f"\n  BubbleCurtain HTTPS server running")
    print(f"  Local:   https://localhost:{PORT}/")
    print(f"  Phone:   https://192.168.1.6:{PORT}/")
    print(f"  Capture: https://192.168.1.6:{PORT}/capture/")
    print(f"\n  On your phone: accept the certificate warning, then log in.\n")
    sys.stdout.flush()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()

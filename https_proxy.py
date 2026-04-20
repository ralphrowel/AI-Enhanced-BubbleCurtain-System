"""
HTTPS reverse proxy -> Django dev server.
Passes all headers/cookies/redirects through faithfully.
"""
import http.server
import http.client
import ssl
import socketserver
import sys

DJANGO_HOST = "127.0.0.1"
DJANGO_PORT = 8000
LISTEN_PORT = 8443


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_request(self):
        # Read request body if present
        body = None
        cl = self.headers.get("Content-Length")
        if cl:
            body = self.rfile.read(int(cl))

        # Connect to Django
        conn = http.client.HTTPConnection(DJANGO_HOST, DJANGO_PORT)
        try:
            # Forward all headers as-is
            headers = {k: v for k, v in self.headers.items()}
            conn.request(self.command, self.path, body=body, headers=headers)
            resp = conn.getresponse()

            # Send status line
            self.send_response_only(resp.status)

            # Forward ALL response headers (cookies, redirects, etc.)
            for key, val in resp.getheaders():
                if key.lower() == "transfer-encoding":
                    continue
                self.send_header(key, val)
            self.end_headers()

            # Forward body
            self.wfile.write(resp.read())
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"Proxy error: {e}".encode())
        finally:
            conn.close()

    do_GET = do_request
    do_POST = do_request
    do_PUT = do_request
    do_DELETE = do_request
    do_PATCH = do_request
    do_OPTIONS = do_request
    do_HEAD = do_request

    def log_message(self, fmt, *args):
        pass  # quiet


class ThreadedHTTPS(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("cert.pem", "key.pem")

    server = ThreadedHTTPS(("0.0.0.0", LISTEN_PORT), ProxyHandler)
    server.socket = context.wrap_socket(server.socket, server_side=True)

    print(f"\n  HTTPS proxy running on port {LISTEN_PORT} -> Django :{DJANGO_PORT}")
    print(f"  PC:    https://localhost:{LISTEN_PORT}/admin/")
    print(f"  Phone: https://192.168.1.6:{LISTEN_PORT}/admin/")
    print(f"  Phone: https://192.168.1.6:{LISTEN_PORT}/capture/\n")
    sys.stdout.flush()

    server.serve_forever()

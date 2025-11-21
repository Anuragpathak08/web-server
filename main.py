import socket
import re

HOST = "127.0.0.1"
PORT = 9000


def response(content_type,path):
    with open(path, "rb") as f:
        body = f.read()
    content_length = len(body)
    response = (
            f"HTTP/1.1 200 OK\r\n"
            f"Content-Type: text/{content_type}\r\n"
            f"Content-Length: {content_length}\r\n"
            f"\r\n"
            ).encode("utf-8") + body
    return response

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print("Listening on", PORT)

    while True:
        conn, addr = s.accept()
        with conn:
            request = conn.recv(2048)
            r = request.decode(errors="ignore").split("\n")[0]
            search = re.search(r"/\S+\.css",r )
            if search:
                conn.sendall(response("css",search.group(0)[1::]))
            else:
                conn.sendall(response("html", "index.html"))
            print("REQUEST:\n", s , request)
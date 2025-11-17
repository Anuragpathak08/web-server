import socket
HOST = "127.0.0.1"
PORT = 9000

with open("web-server/index.html", "rb") as f:
    body = f.read()

content_length = len(body)

response = (
    f"HTTP/1.1 200 OK\r\n"
    f"Content-Type: text/html\r\n"
    f"Content-Length: {content_length}\r\n"
    f"\r\n"
).encode("utf-8") + body

with socket.socket() as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print("Listening on", PORT)

    while True:
        conn, addr = s.accept()
        with conn:
            request = conn.recv(2048)
            print("REQUEST:\n", request.decode(errors="ignore"))

            conn.sendall(response)

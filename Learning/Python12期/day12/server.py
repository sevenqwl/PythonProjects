import socket


def handle_request(client):
    buf = client.recv(1024)
    client.send("HTTP/1.1 200 OK\r\n\r\n".encode())
    # client.send("ALEX".encode())
    # client.send("<h1 style='color: red;'> ALEX </h1>".encode())
    with open('template.html', 'r') as f:
        data = f.read().encode()
    client.send(data)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8005))
    sock.listen(5)

    while True:
        connection, address = sock.accept()
        handle_request(connection)
        sock.close()

if __name__ == "__main__":
    main()
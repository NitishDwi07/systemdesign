import socket

def run_server(port, message):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    print(f"Server running on port {port}...")

    while True:
        client_socket, _ = server_socket.accept()
        request = client_socket.recv(1024).decode()

        http_response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(message)}\r\n"
            "Connection: close\r\n"
            "Content-Type: text/plain\r\n"
            "\r\n"
            f"{message}"
        )

        client_socket.sendall(http_response.encode())
        client_socket.close()

if __name__ == "__main__":
    run_server(8082, "Hello from Server 2!")

# For Explanation refer to server1.py as both codes are same
#  with different ports and response body
import socket
import threading

BACKENDS = [("127.0.0.1", 8081), ("127.0.0.1", 8082)]
# Keeping track of which backendto send req.first for Round Robin
current_backend = 0
# Ensures safe updates to current backend when multiple client connects
lock = threading.Lock()


def get_next_backend():
    global current_backend
    #Round Robin Algorithm
    with lock: #Critical Section 
        backend = BACKENDS[current_backend]
        current_backend = (current_backend + 1) % len(BACKENDS)
    return backend


def handle_client(client_socket):
    #  Handles a single client request by forwarding it to a backend
    #  and sending back the backend’s response.
    backend_host, backend_port = get_next_backend()
    print(f"Forwarding request to backend {backend_host}:{backend_port}")

    #Connecting to Backend Server
    backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend_socket.connect((backend_host, backend_port))

    # --- Read full request from client ---
    request = b"" # Storing Request data
    client_socket.settimeout(1.0) # Timeout Condition
    try:
        while True: #Infinite Loop to Keep Reading
            chunk = client_socket.recv(4096) #Reading 4KB of data
            if not chunk:
                break
            request += chunk
    except socket.timeout:
        pass  # stop when no more data

    #If client Not Sending , Stop
    if not request:
        print("⚠️ No data received from client.")
        client_socket.close()
        backend_socket.close()
        return

    #Forward Client Request to backend
    backend_socket.sendall(request)

    # --- Read full response from backend ---
    response = b""
    backend_socket.settimeout(1.0)
    try:
        while True:
            chunk = backend_socket.recv(4096)
            if not chunk:
                break
            response += chunk
    except socket.timeout:
        pass

    # Force close connection (avoid keep-alive reuse)
    if b"Connection: keep-alive" in response:
        response = response.replace(b"Connection: keep-alive", b"Connection: close")

    #Send backend Response to Client ...
    client_socket.sendall(response)

    backend_socket.close()
    client_socket.close()
    print(f"✅ Response sent from backend {backend_host}:{backend_port}")


def run_load_balancer():
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lb_socket.bind(("127.0.0.1", 8080))
    lb_socket.listen(5)
    print("Load balancer running on port 8080...")

    while True:
        client_socket, addr = lb_socket.accept() # Accepting New Client
        print(f"Accepted connection from {addr}")
        # Creating a new thread to handle client request
        #  so LB can accept multiple at once
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()


if __name__ == "__main__":
    run_load_balancer()

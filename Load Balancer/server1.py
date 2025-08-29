#imports
import socket

def run_server(port, message):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating TCPSocket IVV4 , stream - based one...

    # Allowing immediate reuseing of the 8081 port after the program stops along with 
    # preventing "Adress Already in use" error with restarting quickly...
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #Binding the socket to local host and the 8081 port
    server_socket.bind(("127.0.0.1", port))

    # Starts listening for incoming connections ,queue size = 5
    server_socket.listen(5)
    print(f"Server running on port {port}...")

    while True:  # Infinite loop for multiple requests so that i can keep the server running always
        #accepting incoming client request
        client_socket, _ = server_socket.accept()
        # Receiving data from client max size upto -1024 bytes by data I mean response given by client and decoding it to binary
        request = client_socket.recv(1024).decode()

        # A HTTP response (status + headers + body)
        http_response = (
            "HTTP/1.1 200 OK\r\n"  #Status Line
            f"Content-Length: {len(message)}\r\n" # Length of Response Body
            "Connection: close\r\n" #Closing the response
            "Content-Type: text/plain\r\n" 
            "\r\n"
            f"{message}" #Here is my Response Body
        )

        # Sending the Full HTTP response
        client_socket.sendall(http_response.encode())
        #Closing the client Connection after responding...
        client_socket.close()

# Run server only if script is executed directly ,not imported as module
if __name__ == "__main__":
    run_server(8081, "Hello from Server 1!")


    

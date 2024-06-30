import socket
import threading

# Server configurations
udp_server_address = ("localhost", 9995)  # Address of the UDP server
tcp_server_address = ("localhost", 9994)  # Address of the TCP server
buffer_size = 1024  # Buffer size for receiving and sending data

# Create sockets for UDP and TCP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket

udp_socket.bind(
    ("localhost", 9996)
)  # Bind the UDP socket to port 9996 (Load Balancer UDP port)
tcp_socket.bind(
    ("localhost", 9997)
)  # Bind the TCP socket to port 9997 (Load Balancer TCP port)
tcp_socket.listen(5)  # Listen for incoming TCP connections

print("\nLoadbalancer up and listening on ports ...\n9996 (UDP) \n9997 (TCP)\n")


def handle_udp():
    """
    Handle UDP requests
    """
    while True:
        try:
            message, address = udp_socket.recvfrom(
                buffer_size
            )  # Receive UDP message from client
            print(
                f"Forwarding UDP message from Client: {address} to UDP Server: {udp_server_address}\n"
            )

            udp_socket.sendto(
                message, udp_server_address
            )  # Forward message to UDP server
            response, _ = udp_socket.recvfrom(
                buffer_size
            )  # Receive response from UDP server
            print(
                f"Forwarding response from UDP Server: {udp_server_address} to Client: {address}\n"
            )

            udp_socket.sendto(response, address)  # Send response back to client
        except Exception as e:
            print(f"Error handling UDP: {e}")


def handle_tcp(client_socket, address):
    """
    Handle TCP requests
    """
    try:
        while True:
            data = client_socket.recv(buffer_size)  # Receive TCP data from client
            if not data:
                break
            print(
                f"Forwarding TCP message from Client: {address} to TCP Server: {tcp_server_address}\n"
            )

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(tcp_server_address)  # Connect to TCP server
                s.sendall(data)  # Send data to TCP server
                response = s.recv(buffer_size)  # Receive response from TCP server

                print(
                    f"Forwarding response from TCP Server: {tcp_server_address} to Client: {address}\n"
                )

                client_socket.sendall(response)  # Send response back to client
    except Exception as e:
        print(f"Error handling TCP: {e}")
    finally:
        client_socket.close()  # Close the client socket


def start_tcp_thread():
    """
    Start a new thread to handle TCP connections
    """
    while True:
        client_socket, address = tcp_socket.accept()  # Accept incoming TCP connection
        thread = threading.Thread(target=handle_tcp, args=(client_socket, address))
        thread.start()  # Start a new thread to handle the connection


udp_thread = threading.Thread(target=handle_udp)  # Create a thread for UDP handling
tcp_thread = threading.Thread(
    target=start_tcp_thread
)  # Create a thread for TCP handling

udp_thread.start()  # Start the UDP thread
tcp_thread.start()  # Start the TCP thread

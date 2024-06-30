import socket


# Function to send a UDP message to a server
def send_udp_message(message, udp_server_ip, udp_server_port):
    # Create a UDP socket
    server_address_port = (udp_server_ip, udp_server_port)
    buffer_size = 1024

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send message to server
        client_socket.sendto(message.encode(), server_address_port)

        # Receive response from server
        response, _ = client_socket.recvfrom(buffer_size)
        print("\nResponse from UDP Server: {}".format(response.decode()))

    except Exception as e:
        print(f"Error communicating with UDP Server: {e}")

    finally:
        client_socket.close()


# Function to send a TCP message to a server
def send_tcp_message(message, tcp_server_hostname, tcp_server_port, request_type="GET"):
    server_address = (tcp_server_hostname, tcp_server_port)
    buffer_size = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(server_address)
            if request_type == "GET":
                # Send a GET request
                s.sendall(b"GET / HTTP/1.1\r\nHost: TCP-Server\r\n\r\n")
            elif request_type == "POST":
                # Send a POST request with the message
                headers = f"POST / HTTP/1.1\r\nHost: TCP-Server\r\nContent-Length: {len(message)}\r\n\r\n"
                s.sendall(headers.encode() + message.encode())
            elif request_type == "DELETE":
                # Send a DELETE request
                s.sendall(b"DELETE / HTTP/1.1\r\nHost: TCP-Server\r\n\r\n")

            response = s.recv(buffer_size)
            print(f"\nResponse from TCP Server: \n{response.decode()}")

        except Exception as e:
            print(f"Error communicating with TCP Server: {e}")


# Function to resolve a hostname from an IP address
def resolve_hostname(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)
        return hostname[0]
    except socket.herror:
        return None


# Function to get the port number for a service
def get_service_port(service_name, protocol="tcp"):
    try:
        port = socket.getservbyname(service_name, protocol)
        return port
    except OSError as e:
        print(f"Error retrieving service port: {e}")
        return None


# Function to input server details from the user
def input_server_details():
    while True:
        try:
            print()
            tcp_ip = input("Enter the TCP server IP address: ").strip()
            tcp_port = int(input("Enter the TCP server port number: ").strip())
            udp_server_ip = input("Enter the UDP server IP address: ").strip()
            udp_server_port = int(input("Enter the UDP server port number: ").strip())

            # Resolve the hostnames
            tcp_hostname = socket.gethostbyname(tcp_ip)
            udp_hostname = socket.gethostbyname(udp_server_ip)

            return (
                tcp_ip,
                tcp_port,
                udp_server_ip,
                udp_server_port,
                tcp_hostname,
                udp_hostname,
            )
        except (socket.gaierror, socket.timeout, ValueError, socket.error) as e:
            print(f"\nInvalid input or unable to connect to server: {e}.")
            print("\nPlease enter valid IP addresses and port numbers.")


if __name__ == "__main__":
    # Get the server details from the user
    tcp_ip, tcp_port, udp_server_ip, udp_server_port, tcp_hostname, udp_hostname = (
        input_server_details()
    )

    # Output the hostnames
    print(f"\nThe hostname for TCP server with IP ('{tcp_ip}') is: TCP-Server")
    print(f"The hostname for UDP server with IP ('{udp_server_ip}') is: UDP-Server")

    while True:
        print("\nChoose a Server to send a message to:")
        print("1. TCP Server\n2. UDP Server\n3. Get Service Information\n4. Exit")
        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == "4":
            print("Exiting Client!\n")
            break
        elif choice == "3":
            while True:
                print("\nService Information Options:")
                print(
                    "1. Continue getting service information\n2. Back to Server selection"
                )
                service_choice = input("Enter your choice (1/2): ").strip()

                if service_choice == "1":
                    service_name = input(
                        "Enter the service name (e.g. 'http', 'tftp'): "
                    ).strip()
                    port = get_service_port(service_name)
                    if port:
                        print(f"\nThe port for service '{service_name}' is {port}")
                        break  # Go back to server selection
                    else:
                        print(
                            f"\nInvalid service name '{service_name}'! Please try again."
                        )
                elif service_choice == "2":
                    break  # Go back to server selection
                else:
                    print("Invalid choice! Please enter 1 or 2.")
        elif choice == "2":
            while True:
                print("\nChoose a UDP Server request:")
                print("1. Enter a message\n2. Back to Server selection")
                udp_choice = input("Enter your choice (1/2): ").strip()

                if udp_choice == "1":
                    msg = input("Enter a message to send via UDP: ").strip()
                    send_udp_message(msg, udp_server_ip, udp_server_port)
                    break  # Go back to server selection
                elif udp_choice == "2":
                    break  # Go back to server selection
                else:
                    print("Invalid choice! Please enter 1 or 2.")
        elif choice == "1":
            while True:
                print("\nChoose a HTTP request type:")
                print("1. GET\n2. POST\n3. DELETE\n4. Back to Server selection")
                req_choice = input("Enter your choice (1/2/3/4): ").strip()

                if req_choice == "4":
                    break
                elif req_choice == "1":
                    send_tcp_message("", tcp_hostname, tcp_port)
                    break  # Go back to server selection
                elif req_choice == "2":
                    msg = input("Enter message to send via POST: ").strip()
                    send_tcp_message(msg, tcp_hostname, tcp_port, "POST")
                    break  # Go back to server selection
                elif req_choice == "3":
                    send_tcp_message("", tcp_hostname, tcp_port, "DELETE")
                    break  # Go back to server selection
                else:
                    print("Invalid choice! Please enter 1, 2, 3, or 4.")
        else:
            print("Invalid choice! Please enter 1, 2, 3, or 4.")

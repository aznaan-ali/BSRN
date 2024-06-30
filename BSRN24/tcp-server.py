import http.server
import argparse
import logging
import os

# List to store data received from clients
data_storage = []

# Path to the log file
logfile_path = None


class MyTCPHandler(http.server.BaseHTTPRequestHandler):
    # Override the log_message method to prevent default logging to stderr
    def log_message(self, format, *args):
        # Do nothing
        pass

    # Custom method to log messages to a file
    def log_to_file(self, message):
        if logfile_path:
            # Log the message to the file
            logging.info(message)

    # Override the send_response method to set the protocol version
    def send_response(self, code, message=None):
        self.protocol_version = "HTTP/1.1"
        super().send_response(code, message)

    # Handle GET requests
    def do_GET(self):
        # Get the client's IP address
        client_ip = self.client_address
        # Log the request
        message = "'GET' request received."
        log_message = f"Message from Client: {message}"
        client_ip_message = f"Client IP Address: {client_ip}"
        print(log_message)
        print(client_ip_message + "\n")
        self.log_to_file(log_message)
        self.log_to_file(client_ip_message + "\n")

        # Send a response with the stored data
        response = f"Stored Data: {data_storage}"
        encoded_response = response.encode()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(encoded_response)))
        self.end_headers()
        self.wfile.write(encoded_response)

    # Handle POST requests
    def do_POST(self):
        # Get the client's IP address
        client_ip = self.client_address
        # Get the content length of the request
        content_length = int(self.headers["Content-Length"])
        # Read the request data
        post_data = self.rfile.read(content_length).decode()

        # Log the request
        message = f"'POST' request received. Obtained Data: {post_data}"
        log_message = f"Message from Client: {message}"
        client_ip_message = f"Client IP Address: {client_ip}"
        print(log_message)
        print(client_ip_message + "\n")
        self.log_to_file(log_message)
        self.log_to_file(client_ip_message + "\n")

        # Store the received data
        data_storage.append(post_data)
        response = f"Data received and stored: {post_data}"
        encoded_response = response.encode()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(encoded_response)))
        self.end_headers()
        self.wfile.write(encoded_response)

    # Handle DELETE requests
    def do_DELETE(self):
        # Get the client's IP address
        client_ip = self.client_address
        # Log the request
        message = "'DELETE' request received."
        log_message = f"Message from Client: {message}"
        client_ip_message = f"Client IP Address: {client_ip}"
        print(log_message)
        print(client_ip_message + "\n")
        self.log_to_file(log_message)
        self.log_to_file(client_ip_message + "\n")

        # Clear the stored data
        data_storage.clear()
        response = b"All Data deleted from TCP Server!"
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


def run_server(
    server_class=http.server.HTTPServer,
    handler_class=MyTCPHandler,
    port=9994,
    logfile=None,
):
    global logfile_path

    # Loop until a valid log file path is provided
    while logfile:
        log_dir = os.path.dirname(logfile)
        if log_dir and not os.path.exists(log_dir):
            print(f"Error: The directory {log_dir} does not exist.")
        else:
            try:
                # Set up logging to the file
                logging.basicConfig(
                    filename=logfile,
                    level=logging.INFO,
                    format="%(asctime)s - %(message)s",
                )
                logfile_path = logfile
                break
            except Exception as e:
                print(f"\nError setting up logging: {e}")

        # Ask the user for a valid log file path
        logfile = input("\nPlease enter a valid log file path: ").strip()

    # Create the server
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"\nTCP Server up and listening ...\n")
    logging.info(f"TCP Server up and listening on IP localhost and {port}\n")
    if logfile_path:
        print(f"Logging to file: {logfile_path}\n")
    # Start the server
    httpd.serve_forever()


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Start a TCP server.")
    parser.add_argument("--logfile", type=str, help="Path to the log file")
    args = parser.parse_args()
    # Run the server
    run_server(logfile=args.logfile)

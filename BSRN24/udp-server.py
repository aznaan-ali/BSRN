import socket
import argparse
import logging
import os


# Function to set up logging
def setup_logging():
    # Loop until a valid log file path is entered
    while True:
        # Prompt user to enter a log file path
        logfile_path = input("\nPlease enter a valid log file path: ")
        # Get the directory of the log file path
        log_dir = os.path.dirname(logfile_path)
        # Check if the directory exists
        if log_dir and not os.path.exists(log_dir):
            # If the directory does not exist, print an error message and continue
            print(f"Error: The directory {log_dir} does not exist.")
            continue

        try:
            # Set up logging with the specified log file path
            logging.basicConfig(
                filename=logfile_path,
                level=logging.INFO,
                format="%(asctime)s - %(message)s",
            )
            # Return the log file path
            return logfile_path
        except Exception as e:
            # If there's an error setting up logging, print an error message and continue
            print(f"\nError setting up logging: {e}")
            continue


# Argument parser setup
parser = argparse.ArgumentParser(description="UDP Server")
# Add an argument for the log file path
parser.add_argument("--logfile", type=str, help="Path to the log file")
args = parser.parse_args()

# Initialize log file path to None
logfile_path = None

# Setup logging
if args.logfile:
    # If a log file path is specified, use it
    logfile_path = args.logfile
    log_dir = os.path.dirname(logfile_path)
    # Check if the directory exists
    if log_dir and not os.path.exists(log_dir):
        # If the directory does not exist, prompt user to enter a valid log file path
        print(f"Error: The directory {log_dir} does not exist.")
        logfile_path = setup_logging()
    else:
        # If the directory exists, set up logging with the specified log file path
        try:
            logging.basicConfig(
                filename=logfile_path,
                level=logging.INFO,
                format="%(asctime)s - %(message)s",
            )
        except Exception as e:
            # If there's an error setting up logging, prompt user to enter a valid log file path
            print(f"\nError setting up logging: {e}")
            logfile_path = setup_logging()

# Set up UDP server
localIP = "localhost"
localPort = 9995
bufferSize = 1024

# Create a datagram socket
UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("\nUDP Server up and listening...\n")
if logfile_path:
    # If logging is enabled, print a message indicating the log file path
    print(f"Logging to file: {logfile_path}\n")
    # Log a message indicating the server is up and listening
    logging.info(
        "UDP Server up and listening on IP %s and port %d \n", localIP, localPort
    )


# Custom log function
def log_to_file(message):
    # If logging is enabled, log the message
    if logfile_path:
        logging.info(message)


# Listen for incoming datagrams
while True:
    try:
        # Receive a datagram from a client
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

        # Extract the message and client address from the datagram
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        # Decode the message from bytes to string
        clientMsg = message.decode()
        # Get the client's IP address
        clientIP = "Client IP Address: {}".format(address)

        # Message to send back to the client
        msgFromServer = (
            f"UDP Server received your message! \nData received: {clientMsg}"
        )
        # Encode the message to bytes
        bytesToSend = str.encode(msgFromServer)

        # Output to terminal
        print("Message from Client: {}".format(clientMsg))
        print(clientIP + "\n")

        # Log to file if logging is enabled
        log_to_file("Message from Client: {}".format(clientMsg))
        log_to_file(clientIP + "\n")

        # Sending a reply to the client
        UDPServerSocket.sendto(bytesToSend, address)

    except Exception as e:
        # If there's an error during communication, print an error message
        print(f"Error during communication: {e}")
        # If logging is enabled, log the error
        if logfile_path:
            logging.error(f"Error during communication: {e}")

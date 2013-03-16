import socket                               # For socket connection
import argparse                             # For parsing command line arguments

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("Host", help="Host IP to connect to")
    parser.add_argument("Port", help="Port to connect to")
    parser.add_argument("Data", help="Dat to send")
    args = parser.parse_args()

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try: 
        # Connect to server and send data
        sock.connect((args.Host, int(args.Port)))
        sock.sendall(args.Data + "\n")

        # Receive data from the server and shut down
        received = sock.recv(1024)
    finally:
        sock.close()

    print "Sent:      {}".format(args.Data)
    print "Received:  {}".format(received)


if __name__ == "__main__":
    main()

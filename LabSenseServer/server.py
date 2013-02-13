import argparse                             # For parsing command line arguments
import SocketServer                         # For the socket server


class LabSenseTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # Receive the data
        data = self.request.recv(1024)
        print data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("Port", help="Port to serve tcp handler on.")

    args = parser.parse_args()

    HOST = ""
    server = SocketServer.TCPServer((HOST, int(args.Port)), LabSenseTCPHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()

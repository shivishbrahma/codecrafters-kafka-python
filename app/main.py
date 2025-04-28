import socket  # noqa: F401
from argparse import ArgumentParser
import time

def send_request(client_socket:socket.socket, addr):
    close = False
    while not close:
        message_size = 0
        correlation_id = 7
        client_socket.sendall(
            message_size.to_bytes(4, signed=True)
            +
            correlation_id.to_bytes(4, signed=True)
        )
        time.sleep(0.5)

    client_socket.close()

def start_server(server_socket: socket.socket):
    client_socket = None
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")
        send_request(client_socket, addr)


def main():
    server_socket = socket.create_server(("localhost", 9092), reuse_port=True)
    print(f"Starting server on {server_socket.getsockname()}")
    try:
        start_server(server_socket)
    except KeyboardInterrupt:
        print("\nServer is shutting down...")


if __name__ == "__main__":
    # parser = ArgumentParser()
    # args = parser.parse_args()

    main()

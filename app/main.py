import socket  # noqa: F401
from argparse import ArgumentParser
import time


def handle_request(request_buffer: bytes):
    res = bytes()
    correlation_id = int.from_bytes(request_buffer[8:12]).to_bytes(4, byteorder="big")
    message_size = len(correlation_id).to_bytes(4, byteorder="big")
    res += message_size
    res += correlation_id
    return res

def send_request(client_socket:socket.socket, addr):
    close = False
    while not close:
        req_buff = client_socket.recv(1024)
        if not req_buff:
            close = True
            break
        print(f"Received req from {addr}")
        client_socket.sendall(handle_request(req_buff))
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

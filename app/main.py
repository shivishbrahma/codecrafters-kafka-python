import socket  # noqa: F401
from argparse import ArgumentParser
import time
import threading
from .pub_server import handle_request

def send_request(client_socket:socket.socket, addr):
    close = False
    while not close:
        req_buff = client_socket.recv(1024)
        print(f"Received req from {addr}")
        if not req_buff:
            close = True
            break

        res = handle_request(req_buff)
        client_socket.sendall(res)
        # time.sleep(0.5)
    print("Client closed connection")
    client_socket.close()

def start_server(server_socket: socket.socket):
    client_socket = None
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")
        threading.Thread(target=send_request, args=(client_socket, addr)).start()


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

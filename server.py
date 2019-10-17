import click
import socket
import threading
import time


class ClientThread (threading.Thread):
    def __init__(self, sd):
        self.sd = sd

    def run(self):
        self.sd.sendall(b'hello ')
        # time.sleep(1)
        self.sd.sendall(b'world!\n')
        while True:
            data = self.sd.recv(1024)
            if not data:
                break
            broadcast(data)
        self.sd.close()
        clients.remove(self)

    def send(self, data):
        self.sd.sendall(data)


clients = set()
def broadcast(data):
    for client in clients:
        client.send(data)


@click.command()
@click.argument('port', type=click.INT)
def do_server(port):
    'simple program to listen on a socket and start a thread'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as ld:
        ld.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ld.bind(("", port))
        ld.listen(10)
        while True:
            (sd, addr) = ld.accept()
            ct = ClientThread(sd)
            clients.add(ct)
            ct.run()

if __name__ == '__main__':
    do_server()

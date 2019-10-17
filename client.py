#!/usr/bin/python3

import click
import socket

@click.command()
@click.argument('name')
@click.argument('host')
@click.argument('port', type=click.INT)
def do_client(name, host, port):
    print("opening connection to {}:{}".format(host, port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sd:
        sd.connect((host, port))
        sd.sendall(bytes(name + '\n', 'utf-8'))
        while True:
            data = sd.recv(4)
            if not data:
                break
            print(data)


if __name__ == "__main__":
    do_client()

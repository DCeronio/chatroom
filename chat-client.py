#!/usr/bin/python3
import click
import socket
import time
import threading
import sys
import signal
import _thread

class keepAliveThread (threading.Thread):
    def __init__(self, sd, aliveTime, recvTime):
        threading.Thread.__init__(self)
        self.sd = sd
        self.aliveTime = aliveTime
        self.recvTime = recvTime

    def run(self):
        while True:
            if (time.time() - self.recvTime) > 30.0:
                _thread.interrupt_main()
            elif (time.time() - self.aliveTime) >= 15.0:
                self.sd.send(bytes('alive:\n', 'utf-8'))
                self.aliveTime = time.time()


def findNamesFixData(txt, nameList, start):
    end = '\n'
    while True:
        c1 = txt.find(start)
        if c1 == -1:
            break
        c1 = c1 + len(start)
        c2 = txt.find(end, c1)
        name = txt[c1:c2]
        if name not in nameList and start == 'present: ':
            nameList.append(name)
        if start == 'left: ':
            nameList.remove(name)
            print(name + ' left')
        if start == 'joined: ':
            nameList.append(name)
            print(name + ' joined')
        txt = txt[:c1-len(start)] +  txt[c2 + len(end):]
        if 'present:\n' in txt:
            txt = txt.replace('present:\n', '')
    return txt, nameList


@click.command()
@click.argument('name')
@click.argument('host')
@click.argument('port', type=click.INT)
def do_client(name, host, port):
    print("opening connection to {}:{}".format(host, port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sd:
        sd.connect((host, port))
        currentTime = time.time()
        kat = keepAliveThread(sd, currentTime, currentTime)
        kat.setDaemon(True)  
        kat.start()
        presentList = []
        if '\n' in name:
            name = name.replace('\n', '')
        elif ':' in name:
                name = name.replace(':', '')
        sd.sendall(bytes(name + '\n', 'utf-8'))
        try:
            while True:        
                wantToSend = input(">>>").replace('\\n', '\n')
                if '\n' in wantToSend:
                    wantToSend = wantToSend.replace('\n', '')
                if wantToSend == "whoisthere:" or wantToSend == "/list":
                    sd.sendall(bytes(wantToSend + '\n' , 'utf-8'))
                else:
                    if ':' in wantToSend:
                        wantToSend = wantToSend.replace(':', '')
                    sd.sendall(bytes('mess: ' + wantToSend + '\n' , 'utf-8'))
                data = sd.recv(1024)
                dData = data.decode()
                if 'alive:\n' in dData:
                    kat.recvTime = time.time()
                    dData = dData.replace('alive:\n', '')
                if 'present:\n' in dData:
                    dData, presentList = findNamesFixData(dData, presentList, 'present:\n')
                    print('present: ', end='')
                    print(*presentList, sep=', ')
                if 'present: ' in dData:
                    dData, presentList = findNamesFixData(dData, presentList, 'present: ')
                if 'left: ' in dData:
                    dData, presentList = findNamesFixData(dData, presentList, 'left: ')
                if 'joined: ' in dData:
                    dData, presentList = findNamesFixData(dData, presentList, 'joined: ')    
                print(dData , end='')
        except KeyboardInterrupt:
            sd.close()
            print("[ClOSING]: Haven't heard from server in 30 seconds")
            sys.exit(1)


if __name__ == "__main__":
    do_client()

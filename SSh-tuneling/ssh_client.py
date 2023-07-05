from time import sleep
from platform import node, system, release; Node, System, Release = node(), system(), release() 
import os
import paramiko
import getpass

hostname = '192.168.131.1'
port = 2222
user = input("Enter the username => ")
passwd = getpass.getpass('Enter the password => ')

try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, port=port, username=user, password=passwd)

    while True:
        try:
            cmd = input("$> ")

            if cmd == 'exit': break
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read().decode())
        
        except KeyboardInterrupt:
            break

    client.close()

except Exception as err:
    print(str(err))


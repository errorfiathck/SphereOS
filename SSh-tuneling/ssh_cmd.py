import paramiko

def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())


if __name__ == '__main__':
    import getpass

    user = input("Username => ")
    password = getpass.getpass('Password => ')

    ip = input("Enter The Server IP => ")
    port = input("Enter The Server PORT => ")
    cmd = input("Enter Command or <CR> => ")
    ssh_command(ip, port, user, password, cmd)


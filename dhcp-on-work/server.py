import socket
import struct
from uuid import getnode as get_mac
from random import randint

def getMacInBytes():
    mac = str(hex(get_mac()))
    mac = mac[2:]
    while len(mac) < 12 :
        mac = '0' + mac
    macb = b''
    for i in range(0, 12, 2) :
        m = int(mac[i:i + 2], 16)
        macb += struct.pack('!B', m)
    return macb

class DHCPDiscover:
    def __init__(self):
        self.transactionID = b''
        for i in range(4):
            t = randint(0, 255)
            self.transactionID += struct.pack('!B', t) 

    def buildPacket(self):
        macb = getMacInBytes()
        packet = b''
        packet += b'\x01'   
        packet += b'\x01'  
        packet += b'\x06'  
        packet += b'\x00'  
        packet += self.transactionID 
        packet += b'\x00\x00'   
        packet += b'\x80\x00'   
        packet += b'\x00\x00\x00\x00'
        packet += b'\x00\x00\x00\x00'
        packet += b'\x00\x00\x00\x00'
        packet += b'\x00\x00\x00\x00'
      
        packet += macb
        packet += b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  
        packet += b'\x00' * 67  
        packet += b'\x00' * 125 
        packet += b'\x63\x82\x53\x63'
        packet += b'\x35\x01\x01'   

        packet += b'\x3d\x06' + macb
        packet += b'\x37\x03\x03\x01\x06'   
        packet += b'\xff'   
        return packet

class DHCPOffer:
    def __init__(self, data, transID):
        self.data = data
        self.transID = transID
        self.offerIP = ''
        self.nextServerIP = ''
        self.DHCPServerIdentifier = ''
        self.leaseTime = ''
        self.router = ''
        self.subnetMask = ''
        self.DNS = []
        self.unpack()
    
    def unpack(self):
        if self.data[4:8] == self.transID :
            self.offerIP = '.'.join(map(lambda x:str(x), data[16:20]))
            self.nextServerIP = '.'.join(map(lambda x:str(x), data[20:24]))  
            self.DHCPServerIdentifier = '.'.join(map(lambda x:str(x), data[245:249]))
            self.leaseTime = str(struct.unpack('!L', data[251:255])[0])
            self.router = '.'.join(map(lambda x:str(x), data[257:261]))
            self.subnetMask = '.'.join(map(lambda x:str(x), data[263:267]))
            dnsNB = int(data[268]/4)
            for i in range(0, 4 * dnsNB, 4):
                self.DNS.append('.'.join(map(lambda x:str(x), data[269 + i :269 + i + 4])))
                
    def printOffer(self):
        key = ['DHCP Server', 'Offered IP address', 'subnet mask', 'lease time (s)' , 'default gateway']
        val = [self.DHCPServerIdentifier, self.offerIP, self.subnetMask, self.leaseTime, self.router]
        for i in range(4):
            print('{0:20s} : {1:15s}'.format(key[i], val[i]))
        
        print('{0:20s}'.format('DNS Servers') + ' : ', end='')
        if self.DNS:
            print('{0:15s}'.format(self.DNS[0]))
        if len(self.DNS) > 1:
            for i in range(1, len(self.DNS)): 
                print('{0:22s} {1:15s}'.format(' ', self.DNS[i])) 

if __name__ == '__main__':
   
    dhcps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     
    dhcps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
    
    try:
        dhcps.bind(('', 68))    
    except Exception as e:
        print('port 68 in use...')
        dhcps.close()
        input('press any key to quit...')
        exit()
 

    discoverPacket = DHCPDiscover()
    dhcps.sendto(discoverPacket.buildPacket(), ('<broadcast>', 67))
    
    print('DHCP Discover sent waiting for reply...\n')
    

    dhcps.settimeout(3)
    try:
        while True:
            data = dhcps.recv(1024)
            offer = DHCPOffer(data, discoverPacket.transactionID)
            if offer.offerIP:
                offer.printOffer()
                break
    except socket.timeout as e:
        print(e)
    
    dhcps.close()  
    
    input('press any key to quit...')
    exit()
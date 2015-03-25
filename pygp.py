#! ./bin/python
#
# Minimal example of created an encrypted PGP message in python
# https://tools.ietf.org/html/rfc4880
# © 2015 b@Zi.iS GPLv2

import sys
import base64
import struct
import pyaes
import rsa
from random import SystemRandom

def random(len):
    rnd = SystemRandom()
    return bytes([rnd.randint(0,255) for x in range(len)])

def packet_len(p):
    if len(p) < 192:
        return bytes([len(p)])
    #TODO: support 3 and 4 octet lengths
    return bytes([((len(p) - 192) >> 8) + 192, (len(p)-192) % 256])

session_key = random(32)
rsa_key = rsa.PublicKey.load_pkcs1(open(sys.argv[1], 'rb').read())

out = b'\xC1' #New format Public-Key Encrypted Session Key Packet

p = b'\x03' #Version 3
p += b'\x00' * 8 #Whildcard keyid
p += b'\x01' #RSA public-key algo

m = b'\x09' #AES-256 symmetric encryption algo
m += session_key
m += struct.pack('>h', sum(bytearray(session_key)) % 65536)
m = rsa.encrypt(m, rsa_key)

p += struct.pack('>h', len(m) * 8)
p += m

out += packet_len(p)
out += p

out += b'\xc9' #New format Symmetrically Encrypted Data Packet

p = b'\xcb' #New format Literal data packet

msg = b'b' #binary
msg += b'\x08' #filename len
msg += b'_CONSOLE' #Special 'your eyes only'
msg += b'\x00' * 4 #No date
msg += sys.stdin.read().encode('ascii')

p += packet_len(msg)
p += msg

pre =  random(16) #We effectivly use an encryptied IV
pre += bytes([pre[-2]])
pre += bytes([pre[-2]])

aes = pyaes.AESModeOfOperationCFB(
    session_key,
    iv = b'\x00' * 16,
    segment_size = 16
)
buf = aes.encrypt(pre + b'\00' * 14)[:18] #First BS+2 of random

aes = pyaes.AESModeOfOperationCFB(
    session_key,
    iv = buf[2:],
    segment_size = 16
) #resync
buf += aes.encrypt(p + b'\00' * (16 - len(p) % 16))

out += packet_len(p)
out += buf[:len(p)+18]

print("-----BEGIN PGP MESSAGE-----")
print("Version: " + sys.argv[0] + " 0.0.1")
print()
print(base64.b64encode(out).decode('ascii') + "=")
print()
print("-----END PGP MESSAGE-----")

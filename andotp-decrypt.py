#!/usr/bin/env python3
from aes_gcm.aes_gcm import AES_GCM, InvalidTagException
from Crypto.Hash import SHA256
from os.path import basename
from getpass import getpass
import sys
import os

debug = False

def bytes2Hex(bytes):
    return '(%s) 0x%s' % (len(bytes), ''.join('{:02x}'.format(x) for x in bytes))

def usage():
    print("Usage: %s /path/to/otp_accounts.json.aes" % basename(sys.argv[0]))
    os._exit(0)

if len(sys.argv) != 2:
    usage()

input_file = sys.argv[1]
if not os.path.exists(input_file):
    print("Could not find input file: %s" % input_file)
    usage()

pw = getpass('andOTP passphrase:')
hash = SHA256.new(pw.strip().encode('UTF-8'))
symmetric_key = hash.digest()
if debug:
    print("Symmetric key: %s" % bytes2Hex(symmetric_key))

input_bytes = None
with open(input_file,'rb') as f:
    input_bytes = f.read()

# Raw data structure is IV[:12] + crypttext[12:-16] + auth_tag[-16:]
iv = input_bytes[:12]
crypttext = input_bytes[12:-16]
tag = input_bytes[-16:]
if debug:
    print("Input bytes: %", bytes2Hex(input_bytes))
    print("IV: %s" % bytes2Hex(iv))
    print("Crypttext: %s" % bytes2Hex(crypttext))
    print("Auth tag: %s" % bytes2Hex(tag))

aes = AES_GCM(symmetric_key)
try:
    dec = aes.decrypt(iv, crypttext, tag)
except InvalidTagException as e:
    print(e)
    print("The passphrase was probably wrong")
    os._exit(1)
if debug:
    print("Decrypted data: %s" % bytes2Hex(dec))

print(dec.decode('UTF-8'))

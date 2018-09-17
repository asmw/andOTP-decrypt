#!/usr/bin/env python3
"""andotp-decrypt.py

Usage:
  andotp-decrypt.py INPUT_FILE

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from os.path import basename
from getpass import getpass
import sys
import os
from docopt import docopt

debug = False

def bytes2Hex(bytes):
    return '(%s) 0x%s' % (len(bytes), ''.join('{:02x}'.format(x) for x in bytes))

def decrypt_aes(input_file):
    if not os.path.exists(input_file):
        print("Could not find input file: %s" % input_file)
        return None
    pw = getpass('andOTP AES passphrase:')
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
    try:
        aes = AES.new(symmetric_key, AES.MODE_GCM, nonce=iv)
    except AttributeError as e:
        print(e)
        print('Using \'pycryptodome\' instead of \'pycrypto\' should solve this issue.')
        sys.exit(1)
    try:
        dec = aes.decrypt_and_verify(crypttext, tag)
        if debug:
            print("Decrypted data: %s" % bytes2Hex(dec))
        return dec.decode('UTF-8')
    except InvalidTagException as e:
        print(e)
        print("The passphrase was probably wrong")
        return None

if __name__ == '__main__':
    arguments = docopt(__doc__, version='andotp-decrypt 0.1')

    print(decrypt_aes(arguments['INPUT_FILE']))





#!/usr/bin/env python3
"""andotp-decrypt.py

Usage:
  andotp-decrypt.py [-o] INPUT_FILE

Options:
  -h --help     Show this screen.
  --version     Show version.
  -o            Use old andOTP encryption format

"""

from aes_gcm.aes_gcm import AES_GCM, InvalidTagException
from Crypto.Hash import SHA256
from os.path import basename
from getpass import getpass
import sys
import os
import struct
import hashlib
from docopt import docopt

debug = False

def bytes2Hex(bytes):
    return '(%s) 0x%s' % (len(bytes), ''.join('{:02x}'.format(x) for x in bytes))

def decrypt_aes(input_file, old_format=False):
    if not os.path.exists(input_file):
        print("Could not find input file: %s" % input_file)
        return None
    # Read the backup password manually via a prompt if stdin is a tty,
    # otherwise read from stdin directly.
    if sys.stdin.isatty():
        pw = getpass('andOTP AES passphrase:')
    else:
        pw = sys.stdin.readline()
    pw = pw.strip().encode('UTF-8')
    input_bytes = None
    with open(input_file,'rb') as f:
        input_bytes = f.read()

    def decode(key, data):
        # Raw data structure is IV[:12] + crypttext[12:-16] + auth_tag[-16:]
        iv = data[:12]
        crypttext = data[12:-16]
        tag = data[-16:]
        if debug:
            print("Input bytes: %", bytes2Hex(data))
            print("IV: %s" % bytes2Hex(iv))
            print("Crypttext: %s" % bytes2Hex(crypttext))
            print("Auth tag: %s" % bytes2Hex(tag))

        aes = AES_GCM(key)
        try:
            dec = aes.decrypt(iv, crypttext, tag)
            if debug:
                print("Decrypted data: %s" % bytes2Hex(dec))
            return dec.decode('UTF-8')
        except InvalidTagException as e:
            print(e)
            print("The passphrase was probably wrong")
            return None

    if old_format:
        hash = SHA256.new(pw)
        symmetric_key = hash.digest()
        if debug:
            print("Symmetric key: %s" % bytes2Hex(symmetric_key))
        return decode(symmetric_key, input_bytes)

    # Raw data structure is iterations[:4] + salt[4:16] + data[16:]
    iterations = struct.unpack(">I", input_bytes[:4])[0]
    salt       = input_bytes[4:16]
    data       = input_bytes[16:]
    pbkdf2_key = hashlib.pbkdf2_hmac('sha1', pw, salt, iterations, 32)
    if debug:
        print("Iterations: %s" % iterations)
        print("Salt: %s" % bytes2Hex(salt))
        print("Pbkdf2 key: %s" % bytes2Hex(pbkdf2_key))
    return decode(pbkdf2_key, data)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='andotp-decrypt 0.1')

    print(decrypt_aes(arguments['INPUT_FILE'], arguments['-o']))





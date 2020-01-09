#!/usr/bin/env python3
"""andotp-decrypt.py

Usage:
andotp-decrypt.py [-o|--old] [--debug] [-h|--help] [--version] INPUT_FILE

Options:
-o --old      Use old encryption (andOTP <= 0.6.2)
--debug       Print debug info
-h --help     Show this screen.
--version     Show version.

"""

import os
import sys
import hashlib
import struct
from os.path import basename
from getpass import getpass

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from docopt import docopt

def bytes2Hex(bytes2encode):
    return '(%s) 0x%s' % (len(bytes2encode), ''.join('{:02x}'.format(x) for x in bytes2encode))

def decode(key, data, debug=False):
    """Decode function used for both the old and new style encryption"""
    # Raw data structure is IV[:12] + crypttext[12:-16] + auth_tag[-16:]
    iv = data[:12]
    crypttext = data[12:-16]
    tag = data[-16:]
    if debug:
        print("Input bytes: %", bytes2Hex(data))
        print("IV: %s" % bytes2Hex(iv))
        print("Crypttext: %s" % bytes2Hex(crypttext))
        print("Auth tag: %s" % bytes2Hex(tag))

    aes = AES.new(key, AES.MODE_GCM, nonce=iv)
    try:
        dec = aes.decrypt_and_verify(crypttext, tag)
        if debug:
            print("Decrypted data: %s" % bytes2Hex(dec))
        return dec.decode('UTF-8')
    except ValueError as e:
        print(e)
        print("The passphrase was probably wrong")
        return None

def decrypt_aes_new_format(password, input_file, debug=False):
    input_bytes = None
    with open(input_file, 'rb') as f:
        input_bytes = f.read()

    # Raw data structure is iterations[:4] + salt[4:16] + data[16:]
    iterations = struct.unpack(">I", input_bytes[:4])[0]
    salt       = input_bytes[4:16]
    data       = input_bytes[16:]
    pbkdf2_key = hashlib.pbkdf2_hmac('sha1', password, salt, iterations, 32)
    if debug:
        print("Iterations: %s" % iterations)
        print("Salt: %s" % bytes2Hex(salt))
        print("Pbkdf2 key: %s" % bytes2Hex(pbkdf2_key))

    return decode(pbkdf2_key, data, debug)

def decrypt_aes(password, input_file, debug=False):
    hash = SHA256.new(password)
    symmetric_key = hash.digest()
    if debug:
        print("Symmetric key: %s" % bytes2Hex(symmetric_key))
    input_bytes = None
    with open(input_file, 'rb') as f:
        input_bytes = f.read()

    return decode(symmetric_key, input_bytes, debug)

def get_password():
    # Read the backup password manually via a prompt if stdin is a tty,
    # otherwise read from stdin directly.
    if sys.stdin.isatty():
        pw = getpass('andOTP AES passphrase:')
    else:
        pw = sys.stdin.readline()
    return pw.strip().encode('UTF-8')

def main():
    arguments = docopt(__doc__, version='andotp-decrypt 0.1.0')
    input_file = arguments['INPUT_FILE']
    debug = arguments['--debug']
    old_encryption = arguments['--old']
    if not os.path.exists(input_file):
        print("Could not find input file: %s" % input_file)
        return None
    password = get_password()
    if old_encryption:
        print(decrypt_aes(password, input_file, debug))
    else:
        print(decrypt_aes_new_format(password, input_file, debug))
    
if __name__ == '__main__':
    main()

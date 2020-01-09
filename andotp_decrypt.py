#!/usr/bin/env python3
"""andotp-decrypt.py

Usage:
andotp-decrypt.py [--debug] [-h|--help] [--version] INPUT_FILE

Options:
--debug       Print debug info
-h --help     Show this screen.
--version     Show version.

"""

import os
import sys
from os.path import basename
from getpass import getpass

from Crypto.Cipher import AES
from Crypto.Hash import SHA256

from docopt import docopt

def bytes2Hex(bytes2encode):
    return '(%s) 0x%s' % (len(bytes2encode), ''.join('{:02x}'.format(x) for x in bytes2encode))

def decrypt_aes(input_file, debug):
    if not os.path.exists(input_file):
        print("Could not find input file: %s" % input_file)
        return None
    # Read the backup password manually via a prompt if stdin is a tty,
    # otherwise read from stdin directly.
    if sys.stdin.isatty():
        pw = getpass('andOTP AES passphrase:')
    else:
        pw = sys.stdin.readline()
    hash = SHA256.new(pw.strip().encode('UTF-8'))
    symmetric_key = hash.digest()
    if debug:
        print("Symmetric key: %s" % bytes2Hex(symmetric_key))
    input_bytes = None
    with open(input_file, 'rb') as f:
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

    aes = AES.new(symmetric_key, AES.MODE_GCM, nonce=iv)
    try:
        dec = aes.decrypt_and_verify(crypttext, tag)
        if debug:
            print("Decrypted data: %s" % bytes2Hex(dec))
        return dec.decode('UTF-8')
    except ValueError as e:
        print(e)
        print("The passphrase was probably wrong")
        return None

def main():
    arguments = docopt(__doc__, version='andotp-decrypt 0.1.0')
    print(decrypt_aes(arguments['INPUT_FILE'], arguments['--debug']))
    
if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""generate_code.py

Usage:
  generate_code.py ANDOTP_AES_BACKUP_FILE MATCH_STRING

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import sys
import pyotp
import fileinput
import json
import andotp_decrypt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='generate_code 0.1')

    text = andotp_decrypt.decrypt_aes(arguments['ANDOTP_AES_BACKUP_FILE'])
    if not text:
        print("Something went wrong while loading %s. Maybe the passphrase was wrong?" % arguments['ANDOTP_AES_BACKUP_FILE'])
        sys.exit(1)
    entries = json.loads(text)

    for entry in entries:
        label = entry['label']
        if entry['type'] == 'TOTP':
            if arguments["MATCH_STRING"].lower() in label.lower(): 
                totp = pyotp.TOTP(entry['secret'], interval=entry['period'])
                print("Matched: %s" % label)
                print(totp.now())
                sys.exit(0)
        else:
            print("Unsupported OTP type: %s" % entry["type"])
            sys.exit(2)
    print("No entry matching '%s' found" % arguments["MATCH_STRING"])

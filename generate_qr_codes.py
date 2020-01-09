#!/usr/bin/env python3
"""generate_qr_codes.py

Usage:
  generate_qr_codes.py [-o|--old] ANDOTP_AES_BACKUP_FILE

Options:
  -o --old      Use old encryption (andOTP <= 0.6.2)
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import sys
import pyotp
import pyqrcode
import fileinput
import json
import andotp_decrypt

def main():
    arguments = docopt(__doc__, version='generate_qr_codes 0.1')

    password = andotp_decrypt.get_password()
    text = None
    if arguments['--old']:
        text = andotp_decrypt.decrypt_aes(password, arguments['ANDOTP_AES_BACKUP_FILE'])
    else:
        text = andotp_decrypt.decrypt_aes_new_format(password, arguments['ANDOTP_AES_BACKUP_FILE'])

    if not text:
        print("Something went wrong while loading %s. Maybe the passphrase was wrong?" % arguments['ANDOTP_AES_BACKUP_FILE'])
        sys.exit(1)
    entries = json.loads(text)
    for entry in entries:
        url = None
        issuer = None
        label = entry['label']
        if " - " in label:
            issuer, label = label.split(" - ", 1)
        if entry['type'] == 'TOTP':
            totp = pyotp.TOTP(entry['secret'], interval=entry['period'])
            url = totp.provisioning_uri(label, issuer_name = issuer)
        elif entry['type'] == 'HOTP':
            totp = pyotp.TOTP(entry['secret'])
            url = totp.provisioning_uri(label, issuer_name = issuer)
        if url:
            img = pyqrcode.create(url)
            save_filename = "".join([c for c in label if c.isalpha() or c.isdigit() or c in "@_-"]).strip() + ".svg"
            img.svg(save_filename, scale=4, background='#fff')
            print("Code saved as: %s" % save_filename)

if __name__ == '__main__':
    main()

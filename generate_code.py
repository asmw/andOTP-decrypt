#!/usr/bin/env python3
"""generate_code.py

Usage:
  generate_code.py [-o|--old] [-a] [-i|--issuer] ANDOTP_AES_BACKUP_FILE MATCH_STRING

Options:
  -o --old      Use old encryption (andOTP <= 0.6.2)
  -a --all      Show all matches.
  -i --issuer   Match (and print) issuer in addition to labels.
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import sys
import pyotp
import fileinput
import json
import andotp_decrypt

def main():
    arguments = docopt(__doc__, version='generate_code 0.1')

    password = andotp_decrypt.get_password()
    text = None
    if arguments['--old']:
        text = andotp_decrypt.decrypt_aes(password, arguments['ANDOTP_AES_BACKUP_FILE'])
    else:
        text = andotp_decrypt.decrypt_aes_new_format(password, arguments['ANDOTP_AES_BACKUP_FILE'])

    if not text:
        print("Something went wrong while loading %s. Maybe the passphrase was wrong" \
                " or the input file is empty!" % arguments['ANDOTP_AES_BACKUP_FILE'])
        sys.exit(1)
    entries = json.loads(text)

    found = False
    for entry in entries:
        label = entry['label']
        issuer = entry['issuer']
        if entry['type'] == 'TOTP':
            match_string = arguments["MATCH_STRING"].lower()
            if (match_string in label.lower() or
                match_string in issuer.lower() and arguments['--issuer']):
                found = True
                totp = pyotp.TOTP(entry['secret'], interval=entry['period'])
                if arguments['--issuer'] and issuer != "":
                  output = "%s/%s" % (issuer, label)
                else:
                  output = "%s" % label
                print("Matched: %s" % output)
                print(totp.now())
                if not arguments["--all"]:
                    # The all flag wasn't provided, i.e. we only wanted one
                    # match, so we can exit.
                    sys.exit(0)
        else:
            print("Unsupported OTP type: %s" % entry["type"])
            sys.exit(2)
    if not found:
        print("No entry matching '%s' found" % arguments["MATCH_STRING"])

if __name__ == '__main__':
    main()

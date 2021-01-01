#!/usr/bin/env python3
"""generate_code.py

Usage:
  generate_code.py [-o|--old] [-a] ANDOTP_AES_BACKUP_FILE MATCH_STRING

Options:
  -o --old      Use old encryption (andOTP <= 0.6.2)
  -a --all      Show all matches.
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import sys
import pyotp
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
        print("Something went wrong while loading %s. Maybe the passphrase was wrong"
              " or the input file is empty." % arguments['ANDOTP_AES_BACKUP_FILE'])
        sys.exit(1)
    entries = json.loads(text)

    filtered_entries = andotp_decrypt.find_entries(entries, arguments["MATCH_STRING"], None if arguments["--all"] else 1)
    if len(filtered_entries) == 0:
        print("No entry matching '%s' found" % arguments["MATCH_STRING"])
        sys.exit(0)

    for entry in filtered_entries:
        if entry['type'] == 'TOTP':
            totp = pyotp.TOTP(entry['secret'], interval=entry['period'])
            print("Matched: %s" % andotp_decrypt.descriptor(entry))
            print(totp.now())
        else:
            print("Unsupported OTP type: %s" % entry["type"])
            sys.exit(2)


if __name__ == '__main__':
    main()

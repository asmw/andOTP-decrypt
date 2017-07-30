#!/usr/bin/env python3
import sys
import pyotp
import qrcode
import fileinput
import json

args = sys.argv[1:]

text = ""
for line in fileinput.input(args):
    text += line

entries = json.loads(text)

for entry in entries:
    totp = pyotp.TOTP(entry['secret'])
    url = totp.provisioning_uri(entry['label'])
    img = qrcode.make(url)
    safe_filename = "".join([c for c in entry['label'] if c.isalpha() or c.isdigit()]).strip() + ".png"
    img.save(safe_filename)
    print("Code saved as: %s" % safe_filename)

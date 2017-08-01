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
        img = qrcode.make(url)
        safe_filename = "".join([c for c in label if c.isalpha() or c.isdigit() or c in "@_-"]).strip() + ".png"
        img.save(safe_filename)
        print("Code saved as: %s" % safe_filename)

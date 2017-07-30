# andOTP-decrypt

Tools:
 - andotp-decrypt.py: A decryption tool for password-secured backups of the [andOTP](https://github.com/flocke/andOTP) two-factor android app.
   - Output is written to stdout
 - generate_qr_codes.py: A tool to generate new, scanable QR code images for every entry of a dump
   - Images are saved to the current working directory

## Requirements:
 - andotp-decrypt.py: Python 3 and pycrypto
 - generate_qr_codes.py: pyqrcode and pyotp

On debian/ubuntu this should work:
 - sudo apt-get install python3-crypto python3-pyotp python3-qrcode

## Usage:
 - Dump JSON to the console:
   - ./andotp-decrypt /path/to/otp_accounts.json.aes
 - Generate new QR codes:
   - ./andotp-decrypt /path/to/otp_accounts.json.aes | ./generate_qr_codes.py

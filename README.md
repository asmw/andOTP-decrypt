# andOTP-decrypt

Tools:
 - `andotp_decrypt.py`: A decryption tool for password-secured backups of the [andOTP](https://github.com/flocke/andOTP) two-factor android app.
   - Output is written to stdout
 - `generate_qr_codes.py`: A tool to generate new, scanable QR code images for every entry of a dump
   - Images are saved to the current working directory
 - `generate_code.py`: A tool to generate a TOTP token for an account in the backup

## Requirements:
 - `andotp_decrypt.py`: Python 3 and pycrypto
 - `generate_qr_codes.py` + `generate_code.py`: pyqrcode and pyotp

On debian/ubuntu this should work:
 - `sudo apt-get install python3-crypto python3-pyotp python3-qrcode python3-docopt`

## Setup:
 - To use `andotp_decrypt.py` you must clone this repository with `--recursive` (eg. `git clone --recursive https://github.com/asmw/andOTP-decrypt`)

## Usage:
 - Dump JSON to the console:
   - `./andotp_decrypt.py /path/to/otp_accounts.json.aes`
 - Generate new QR codes:
   - `./generate_qr_codes.py /path/to/otp_accounts.json.aes`
 - Generate a TOTP code for your google account:
   - `./generate_code.py /path/to/otp_accounts.json.aes google`

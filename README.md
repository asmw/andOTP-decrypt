# andOTP-decrypt

A backup decryptor for the [andOTP](https://github.com/andOTP/andOTP) Android app.

The tools in this package support the password based backup files of andOTP in both the current (0.6.3) old (0.6.2 and before) format.

Tools:

- `andotp_decrypt.py`: A decryption tool for password-secured backups of the [andOTP](https://github.com/flocke/andOTP) two-factor android app.
  - Output is written to stdout
- `generate_qr_codes.py`: A tool to generate new, scanable QR code images for every entry of a dump
  - Images are saved to the current working directory
- `generate_code.py`: A tool to generate a TOTP token for an account in the backup

## Installation

`pip install andotp-decrypt`

The tools will be installed as:

- `andotp_decrypt`
- `andotp_gencode`
- `andotp_qrcode`

## Development Setup

[Poetry](https://python-poetry.org/) install (recommended)

- Install poetry
  - `pip install poetry` (or use the recommended way from the website)
- Install everything else
  - `poetry install`
- Launch the virtualenv
  - `poetry shell`

Pip install

- `sudo pip3 install -r requirements.txt` 

On debian/ubuntu this should work:

- `sudo apt-get install python3-pycryptodome python3-pyotp python3-pyqrcode python3-pillow python3-docopt`

## Usage

- Dump JSON to the console:
  - `./andotp_decrypt.py /path/to/otp_accounts.json.aes`
- Generate new QR codes:
  - `./generate_qr_codes.py /path/to/otp_accounts.json.aes`
- Generate a TOTP code for your google account:
  - `./generate_code.py /path/to/otp_accounts.json.aes google`

## Thanks

Thank you for contributing!

- @alkuzad
- @ant9000
- @anthonycicc
- @erik-h
- @romed
- @rubenvdham
- @wornt
- @naums
- @marcopaganini

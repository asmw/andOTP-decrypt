# andOTP-decrypt

Tools:

- `andotp_decrypt.py`: A decryption tool for password-secured backups of the [andOTP](https://github.com/flocke/andOTP) two-factor android app.
  - Output is written to stdout
- `generate_qr_codes.py`: A tool to generate new, scanable QR code images for every entry of a dump
  - Images are saved to the current working directory
- `generate_code.py`: A tool to generate a TOTP token for an account in the backup

## Setup

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

- alkuzad
- ant9000
- anthonycicc
- erik-h
- romed
- rubenvdham
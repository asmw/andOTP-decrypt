# andOTP-decrypt

Tools:

- `andotp_decrypt.py`: A decryption tool for password-secured backups of the [andOTP](https://github.com/flocke/andOTP) two-factor android app.
  - Output is written to stdout
- `generate_qr_codes.py`: A tool to generate new, scanable QR code images for every entry of a dump
  - Images are saved to the current working directory
- `generate_code.py`: A tool to generate a TOTP token for an account in the backup

## Requirements

- `andotp_decrypt.py`: Python 3 and pycryptodome
- `generate_qr_codes.py` + `generate_code.py`: pyqrcode and pyotp

Poetry install (recommended)

- Install poetry
  - `pip install poetry`
- Install everything else
  - `poetry install`
- Launch the virtualenv
  - `poetry shell`

Pip install

- `sudo pip3 install -r requirements.txt` 

On debian/ubuntu this should work:

- `sudo apt-get install python3-cryptodome python3-pyotp python3-qrcode`

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
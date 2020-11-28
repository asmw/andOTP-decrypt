#!/bin/bash
set -e
echo 123456 | python ../andotp_decrypt.py accounts_new_123456.json.aes
echo 123456 | python ../generate_code.py accounts_new_123456.json.aes test
echo 123456 | python ../generate_qr_codes.py accounts_new_123456.json.aes

echo 123456 | python ../andotp_decrypt.py -o accounts_old_123456.json.aes
echo 123456 | python ../generate_code.py -o accounts_old_123456.json.aes test
echo 123456 | python ../generate_qr_codes.py -o accounts_old_123456.json.aes

echo 123456 | python ../andotp_decrypt.py emptyfile.json.aes
echo 123456 | python ../generate_code.py emptyfile.json.aes test
echo 123456 | python ../generate_qr_codes.py emptyfile.json.aes
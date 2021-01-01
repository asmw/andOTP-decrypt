#!/bin/bash
set -e

D="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
DATA_DIR=$(mktemp -d)

trap "echo 'Removing data dir'; rm -r $DATA_DIR;" exit

echo "Using directory $DATA_DIR"

cd $DATA_DIR

echo 123456 | python3 $D/../andotp_decrypt.py $D/accounts_new_123456.json.aes
echo 123456 | python3 $D/../generate_code.py $D/accounts_new_123456.json.aes test
echo 123456 | python3 $D/../generate_qr_codes.py $D/accounts_new_123456.json.aes

rm *.svg
echo 123456 | python3 $D/../andotp_decrypt.py -o $D/accounts_old_123456.json.aes
echo 123456 | python3 $D/../generate_code.py -o $D/accounts_old_123456.json.aes test
echo 123456 | python3 $D/../generate_qr_codes.py -o $D/accounts_old_123456.json.aes

rm *.svg
echo 123456 | python3 $D/../andotp_decrypt.py $D/accounts_issuer_123456.json.aes
echo 123456 | python3 $D/../generate_code.py $D/accounts_issuer_123456.json.aes test
echo 123456 | python3 $D/../generate_qr_codes.py $D/accounts_issuer_123456.json.aes
svgexpect=7
svgcount=$(ls *.svg | wc -l)
if [[ ! $svgcount -eq $svgexpect ]]; then
  echo "Error generating individual images, $svgcount images found, expected $svgexpect"
  ls -l *.svg
  exit 1
fi

rm *.svg
# This does not fail as it does not decode the data
echo 123456 | python3 $D/../andotp_decrypt.py $D/emptyfile.json.aes

# The following must all fail
if echo "123456" | python3 $D/../generate_code.py $D/emptyfile.json.aes test ; then exit 1; fi
if echo "123456" | python3 $D/../generate_qr_codes.py $D/emptyfile.json.aes ; then exit 1; fi

echo "123456" | python3 $D/../andotp_decrypt.py $D/garbage.json.aes
if echo "123456" | python3 $D/../generate_code.py $D/garbage.json.aes test ; then exit 1; fi
if echo "123456" | python3 $D/../generate_qr_codes.py $D/garbage.json.aes ; then exit 1; fi

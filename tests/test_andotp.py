import pytest
import andotp_decrypt as ad
import json
from functools import partial

file_password = b'123456'


@pytest.fixture
def json_with_issuer():
    data = ad.decrypt_aes_new_format(file_password, 'testdata/accounts_issuer_123456.json.aes')
    yield json.loads(data)


@pytest.fixture(params=[True, False])
def decryptor(request):
    if request.param:
        yield partial(ad.decrypt_aes, input_file='testdata/accounts_old_123456.json.aes')
    else:
        yield partial(ad.decrypt_aes_new_format, input_file='testdata/accounts_new_123456.json.aes')


@pytest.fixture
def decrypted_json(decryptor):
    yield json.loads(decryptor(file_password))


def test_decrypt(decryptor):
    # The payload in the file should be a JSON doc of 160 characters
    assert len(decryptor(file_password)) == 160


def test_wrong_password(decryptor, capsys):
    assert not decryptor(b'wrong password')
    assert capsys.readouterr().out == "MAC check failed\nThe passphrase was probably wrong\n"


def test_empty_file(capsys):
    test_file = 'testdata/emptyfile.json.aes'
    assert not ad.decrypt_aes_new_format(file_password, test_file)
    assert capsys.readouterr().out == "No data could be read. The input file is unreadable or empty\n"


def test_json(decryptor):
    data = json.loads(decryptor(file_password))
    assert len(data) == 1
    assert data[0]['label'] == 'test'


def test_missing_issuer(decrypted_json):
    """Issuer fields were not always included as separate
       fields in the JSON data. E.g. the sample backups
       for old and new encryption do not contain the field."""
    assert 'issuer' not in decrypted_json[0]


def test_existing_issuer_field(json_with_issuer):
    assert len(json_with_issuer) == 7
    for entry in json_with_issuer:
        assert 'issuer' in entry


def test_find_entries(json_with_issuer):
    asmw_matches = ad.find_entries(json_with_issuer, 'asmw.org')
    assert len(asmw_matches) == 3

    ACME_matches = ad.find_entries(json_with_issuer, 'acme')
    assert len(ACME_matches) == 2

    # Matches are case insensitive
    ACME_matches = ad.find_entries(json_with_issuer, 'ACME')
    assert len(ACME_matches) == 2


def test_find_by_tag(json_with_issuer):
    tag_matches = ad.find_entries(json_with_issuer, 'sometag')
    assert len(tag_matches) == 2


def test_find_limit(json_with_issuer):
    tag_matches = ad.find_entries(json_with_issuer, 'asmw', 1)
    assert len(tag_matches) == 1

    tag_matches = ad.find_entries(json_with_issuer, 'asmw', 2)
    assert len(tag_matches) == 2

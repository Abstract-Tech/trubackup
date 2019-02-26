from edxbackup.edx import extract_info
import json
import os


def test_extract_mysql():
    data = load_test_json()
    result = extract_info(data)
    assert result['mysql']
    assert result['mongo']


def load_test_json():
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, 'lms.auth.json')
    with open(filepath) as fh:
        return json.load(fh)

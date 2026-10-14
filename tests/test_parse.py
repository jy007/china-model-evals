from cme.parse import extract_json


def test_plain_json():
    assert extract_json('{"a": 1}') == {"a": 1}


def test_fenced_json_with_prose():
    text = 'Here you go:\n```json\n{"a": 2}\n```\nDone.'
    assert extract_json(text) == {"a": 2}


def test_numbers_with_commas_as_strings_are_left_to_caller():
    assert extract_json('{"a": "1,234"}') == {"a": "1,234"}


def test_unparseable_returns_none():
    assert extract_json("no json here") is None

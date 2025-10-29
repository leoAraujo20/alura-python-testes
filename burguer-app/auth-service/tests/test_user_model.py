import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user_model import serialize_user


def test_serialize_user_complete_data():
    user = {
        "email": "test@example.com",
        "name": "Test User",
        "address": "Rua 123",
        "role": "admin",
    }
    serialized = serialize_user(user)
    expected = {
        "email": "test@example.com",
        "name": "Test User",
        "address": "Rua 123",
        "role": "admin",
    }
    assert serialized == expected


def test_serialize_user_partial_data():
    user = {"email": "test@example.com", "name": "Test User"}
    serialized = serialize_user(user)
    expected = {
        "email": "test@example.com",
        "name": "Test User",
        "address": "",
        "role": "cliente",
    }
    assert serialized == expected


def test_serialize_user_integer():
    with pytest.raises(AttributeError):
        serialize_user(12345)


def test_test_serialize_user_string():
    with pytest.raises(AttributeError):
        serialize_user("invalid_user")


def test_serialize_user_none_dict():
    user = {
        "email": None,
        "name": None,
        "address": None,
        "role": None,
    }
    serialized = serialize_user(user)
    expected = {
        "email": None,
        "name": None,
        "address": None,
        "role": None,
    }
    assert serialized == expected


def test_serialize_user_empty_dict():
    user = {}
    serialized = serialize_user(user)
    expected = {
        "email": None,
        "name": "",
        "address": "",
        "role": "cliente",
    }
    assert serialized == expected


def test_serialize_user_unexpected_field_values():
    user = {
        "email": 123,
        "name": ["Test", "User"],
        "address": {"street": "Rua 123"},
        "role": None,
    }
    serialized = serialize_user(user)
    expected = {
        "email": 123,
        "name": ["Test", "User"],
        "address": {"street": "Rua 123"},
        "role": None,
    }
    assert serialized == expected


def test_serialize_user_extra_fields():
    user = {
        "email": "test@example.com",
        "name": "Test User",
        "address": "Rua 123",
        "role": "admin",
        "extra_field": "extra_value",
    }
    serialized = serialize_user(user)
    expected = {
        "email": "test@example.com",
        "name": "Test User",
        "address": "Rua 123",
        "role": "admin",
    }
    assert serialized == expected

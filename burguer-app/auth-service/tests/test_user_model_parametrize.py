import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user_model import serialize_user

test_data_no_error = [
    # test_serialize_user_complete_data
    (
        {
            "email": "test@example.com",
            "name": "Test User",
            "address": "Rua 123",
            "role": "admin",
        },
        {
            "email": "test@example.com",
            "name": "Test User",
            "address": "Rua 123",
            "role": "admin",
        },
    ),
    # test_serialize_user_missing_optional_fields
    (
        {
            "email": "test@example.com",
            "name": "Test User",
        },
        {
            "email": "test@example.com",
            "name": "Test User",
            "address": "",
            "role": "cliente",
        },
    ),
    # test_serialize_user_none_dict
    (
        {
            "email": None,
            "name": None,
            "address": None,
            "role": None,
        },
        {
            "email": None,
            "name": None,
            "address": None,
            "role": None,
        },
    ),
    # test_serialize_user_empty_dict
    (
        {},
        {
            "email": None,
            "name": "",
            "address": "",
            "role": "cliente",
        },
    ),
    # test_serialize_user_unexpected_field_values
    (
        {
            "email": 123,
            "name": ["Test", "User"],
            "address": {"street": "Rua 123"},
            "role": None,
        },
        {
            "email": 123,
            "name": ["Test", "User"],
            "address": {"street": "Rua 123"},
            "role": None,
        },
    ),
    # test_serialize_user_extra_fields
    (
        {
            "email": "test@example.com",
            "name": "Test User",
            "address": "Rua 123",
            "role": "admin",
            "extra_field": "extra_value",
        },
        {
            "email": "test@example.com",
            "name": "Test User",
            "address": "Rua 123",
            "role": "admin",
        },
    ),
]

@pytest.mark.parametrize("user, expected", test_data_no_error)
def test_serialize_user(user, expected):
    serialized = serialize_user(user)
    assert serialized == expected


# valores que devem gerar exceção ao serializar
test_data_error = [
    12345,
    "invalid_user",
    None,
    []
]


@pytest.mark.parametrize("invalid_value", test_data_error)
def test_serialize_user_raises_on_invalid_types(invalid_value):
    with pytest.raises(AttributeError):
        serialize_user(invalid_value)
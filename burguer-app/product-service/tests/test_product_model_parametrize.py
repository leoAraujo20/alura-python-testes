import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.product_model import serialize_product


test_data_no_error = [
    # test_serialize_product_complete_data
    (
        {
            "_id": "607f1f77bcf86cd799439011",
            "name": "Hamburger",
            "description": "Um delicioso hamburger artesanal",
            "category": "Sanduíches",
            "price": 15.99,
            "available": True,
            "ingredients": ["pão", "carne", "alface", "tomate", "queijo"],
        },
        {
            "id": "607f1f77bcf86cd799439011",
            "name": "Hamburger",
            "description": "Um delicioso hamburger artesanal",
            "category": "Sanduíches",
            "price": 15.99,
            "available": True,
            "ingredients": ["pão", "carne", "alface", "tomate", "queijo"],
        },
    ),
    # test_serialize_product_parse_id_to_string
    (
        {
            "_id": 123456789,
            "name": "Cheeseburger",
            "description": "Hamburger com queijo",
            "category": "Sanduíches",
            "price": 13.99,
            "available": False,
            "ingredients": ["pão", "carne", "queijo"],
        },
        {
            "id": "123456789",
            "name": "Cheeseburger",
            "description": "Hamburger com queijo",
            "category": "Sanduíches",
            "price": 13.99,
            "available": False,
            "ingredients": ["pão", "carne", "queijo"],
        },
    ),
    # test_serialize_product_missing_optional_fields
    (
        {
            "_id": "607f1f77bcf86cd799439012",
            "name": "Veggie Burger",
            "description": "Hamburger vegetariano saboroso",
            "category": "Sanduíches",
            "price": 12.99,
        },
        {
            "id": "607f1f77bcf86cd799439012",
            "name": "Veggie Burger",
            "description": "Hamburger vegetariano saboroso",
            "category": "Sanduíches",
            "price": 12.99,
            "available": True,
            "ingredients": [],
        },
    ),
    # test_serialize_product_none_dict
    (
        {
            "_id": None,
            "name": None,
            "description": None,
            "category": None,
            "price": None,
            "available": None,
            "ingredients": None,
        },
        {
            "id": "None",
            "name": None,
            "description": None,
            "category": None,
            "price": None,
            "available": None,
            "ingredients": None,
        },
    ),
    # test_serialize_product_empty_dict
    (
        {},
        {
            "id": "None",
            "name": None,
            "description": None,
            "category": None,
            "price": None,
            "available": True,
            "ingredients": [],
        },
    ),
    # test_serialize_product_unexpected_field_values
    (
        {
            "_id": 123,
            "name": ["Hamburger"],
            "description": {"text": "Delicious"},
            "category": None,
            "price": "free",
            "available": "yes",
            "ingredients": "all",
        },
        {
            "id": "123",
            "name": ["Hamburger"],
            "description": {"text": "Delicious"},
            "category": None,
            "price": "free",
            "available": "yes",
            "ingredients": "all",
        },
    ),
    # test_serialize_product_extra_fields
    (
        {
            "_id": "607f1f77bcf86cd799439013",
            "name": "Chicken Burger",
            "description": "Hamburger de frango suculento",
            "category": "Sanduíches",
            "price": 14.99,
            "available": False,
            "ingredients": ["pão", "frango", "alface", "maionese"],
            "extra_field": "extra_value",
        },
        {
            "id": "607f1f77bcf86cd799439013",
            "name": "Chicken Burger",
            "description": "Hamburger de frango suculento",
            "category": "Sanduíches",
            "price": 14.99,
            "available": False,
            "ingredients": ["pão", "frango", "alface", "maionese"],
        },
    ),
]


@pytest.mark.parametrize("product, expected", test_data_no_error)
def test_serialize_product(product, expected):
    serialized = serialize_product(product)
    assert serialized == expected


# valores que devem gerar exceção ao serializar
test_data_error = [
    12345,
    "invalid_product",
]


@pytest.mark.parametrize("invalid_value", test_data_error)
def test_serialize_product_raises_on_invalid_types(invalid_value):
    """Casos em que `serialize_product` deve levantar AttributeError para tipos inválidos."""
    with pytest.raises(AttributeError):
        serialize_product(invalid_value)
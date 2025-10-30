import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.product_model import serialize_product


def test_serialize_product_complete_data():
    product = {
        "_id": "607f1f77bcf86cd799439011",
        "name": "Hamburger",
        "description": "Um delicioso hamburger artesanal",
        "category": "Sanduíches",
        "price": 15.99,
        "available": True,
        "ingredients": ["pão", "carne", "alface", "tomate", "queijo"],
    }
    serialized = serialize_product(product)
    expected = {
        "id": "607f1f77bcf86cd799439011",
        "name": "Hamburger",
        "description": "Um delicioso hamburger artesanal",
        "category": "Sanduíches",
        "price": 15.99,
        "available": True,
        "ingredients": ["pão", "carne", "alface", "tomate", "queijo"],
    }
    assert serialized == expected


def test_serialize_product_parse_id_to_string():
    product = {
        "_id": 123456789,
        "name": "Cheeseburger",
        "description": "Hamburger com queijo",
        "category": "Sanduíches",
        "price": 13.99,
        "available": False,
        "ingredients": ["pão", "carne", "queijo"],
    }
    serialized = serialize_product(product)
    expected = {
        "id": "123456789",
        "name": "Cheeseburger",
        "description": "Hamburger com queijo",
        "category": "Sanduíches",
        "price": 13.99,
        "available": False,
        "ingredients": ["pão", "carne", "queijo"],
    }
    assert serialized == expected
    assert isinstance(serialized["id"], str)


def test_serialize_product_missing_optional_fields():
    product = {
        "_id": "607f1f77bcf86cd799439012",
        "name": "Veggie Burger",
        "description": "Hamburger vegetariano saboroso",
        "category": "Sanduíches",
        "price": 12.99,
    }
    serialized = serialize_product(product)
    expected = {
        "id": "607f1f77bcf86cd799439012",
        "name": "Veggie Burger",
        "description": "Hamburger vegetariano saboroso",
        "category": "Sanduíches",
        "price": 12.99,
        "available": True,
        "ingredients": [],
    }
    assert serialized == expected


def test_serialize_product_integer():
    with pytest.raises(AttributeError):
        serialize_product(12345)


def test_serialize_product_string():
    with pytest.raises(AttributeError):
        serialize_product("invalid_product")


def test_serialize_product_none_dict():
    product = {
        "_id": None,
        "name": None,
        "description": None,
        "category": None,
        "price": None,
        "available": None,
        "ingredients": None,
    }
    serialized = serialize_product(product)
    expected = {
        "id": "None",
        "name": None,
        "description": None,
        "category": None,
        "price": None,
        "available": None,
        "ingredients": None,
    }
    assert serialized == expected

def test_serialize_product_empty_dict():
    product = {}
    serialized = serialize_product(product)
    expected = {
        "id": "None",
        "name": None,
        "description": None,
        "category": None,
        "price": None,
        "available": True,
        "ingredients": [],
    }
    assert serialized == expected


def test_serialize_product_unexpected_field_values():
    product = {
        "_id": 123,
        "name": ["Hamburger"],
        "description": {"text": "Delicious"},
        "category": None,
        "price": "free",
        "available": "yes",
        "ingredients": "all",
    }
    serialized = serialize_product(product)
    expected = {
        "id": "123",
        "name": ["Hamburger"],
        "description": {"text": "Delicious"},
        "category": None,
        "price": "free",
        "available": "yes",
        "ingredients": "all",
    }
    assert serialized == expected


def test_serialize_product_extra_fields():
    product = {
        "_id": "607f1f77bcf86cd799439013",
        "name": "Chicken Burger",
        "description": "Hamburger de frango suculento",
        "category": "Sanduíches",
        "price": 14.99,
        "available": False,
        "ingredients": ["pão", "frango", "alface", "maionese"],
        "extra_field": "extra_value",
    }
    serialized = serialize_product(product)
    expected = {
        "id": "607f1f77bcf86cd799439013",
        "name": "Chicken Burger",
        "description": "Hamburger de frango suculento",
        "category": "Sanduíches",
        "price": 14.99,
        "available": False,
        "ingredients": ["pão", "frango", "alface", "maionese"],
    }
    assert serialized == expected
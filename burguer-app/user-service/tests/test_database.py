import os
import sys

from unittest.mock import MagicMock, patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_get_db_connection_success():
    with patch("pymongo.MongoClient") as mock_mongo_client:
        mock_db = MagicMock()
        mock_mongo_client.return_value.__getitem__.return_value = mock_db

        with patch("config.database.client", mock_mongo_client):
            from config.database import get_db
            db_instance = get_db()
            assert db_instance == mock_db
            assert db_instance is not None
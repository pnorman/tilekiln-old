from unittest import TestCase
from unittest.mock import patch

from tilekiln.database import Database
from tilekiln.definition import Definition


class TestDatabase(TestCase):
    @patch("psycopg2.connect")
    def test_generate(self, mock_connect):
        mock_connect.cursor.return_value.__enter__.return_value.\
            fetchone.return_value = (b"result",)

        db = Database(mock_connect)
        dfn = Definition("a", "sql", 0, 4)
        tilelayer = db.generate_tilelayer(dfn, (0, 0, 0))
        self.assertEqual(tilelayer, b"result")

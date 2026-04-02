from pathlib import Path
import sys

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import Column, Database, Table


@pytest.fixture
def users_table():
    table = Table("users")
    table.create_column("id", int)
    table.create_column("name", str)
    table.create_column("is_active", bool)
    return table


@pytest.fixture
def database_with_users(users_table):
    database = Database("app_db", metadata="test metadata")
    database.tables["users"] = users_table
    return database


class TestColumn:
    def test_initializes_with_name_and_dtype(self):
        column = Column("age", int)

        assert column.name == "age"
        assert column.dtype is int

    @pytest.mark.parametrize("dtype", [list, dict, tuple, set, object, bytes, None])
    def test_rejects_invalid_dtypes(self, dtype):
        with pytest.raises(ValueError, match="Invalid datatype"):
            Column("bad_column", dtype)

    @pytest.mark.parametrize("dtype", [int, str, float, bool])
    def test_accepts_all_supported_dtypes(self, dtype):
        column = Column("value", dtype)

        assert column.dtype is dtype

    def test_change_name_updates_name(self):
        column = Column("username", str)

        column.change_name("handle")

        assert column.name == "handle"

    def test_change_name_accepts_empty_string_in_current_behavior(self):
        column = Column("username", str)

        column.change_name("")

        assert column.name == ""


class TestTable:
    def test_initializes_empty(self):
        table = Table("users")

        assert table.name == "users"
        assert table.columns == {}
        assert table.rows == []

    def test_create_column_registers_column_and_returns_it(self):
        table = Table("users")

        column = table.create_column("name", str)

        assert column is table.columns["name"]
        assert column.name == "name"
        assert column.dtype is str

    def test_create_column_preserves_insertion_order(self):
        table = Table("users")

        table.create_column("id", int)
        table.create_column("name", str)
        table.create_column("score", float)

        assert list(table.columns) == ["id", "name", "score"]

    def test_add_row_accepts_valid_row(self, users_table):
        row = {"id": 1, "name": "Ada", "is_active": True}

        users_table.add_row(row)

        assert users_table.rows == [row]

    def test_add_row_allows_subset_of_defined_columns_in_current_behavior(self, users_table):
        row = {"id": 1}

        users_table.add_row(row)

        assert users_table.rows == [row]

    def test_add_row_rejects_unknown_column(self, users_table):
        with pytest.raises(ValueError, match="Column with column name email doesn't exist"):
            users_table.add_row({"id": 1, "name": "Ada", "email": "ada@example.com"})

    def test_add_multiple_rows_preserves_order(self, users_table):
        first = {"id": 1, "name": "Ada"}
        second = {"id": 2, "name": "Grace", "is_active": False}

        users_table.add_row(first)
        users_table.add_row(second)

        assert users_table.rows == [first, second]

    def test_list_columns_on_empty_table_prints_nothing(self, capsys):
        table = Table("users")

        table.list_columns()

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_list_columns_basic_output(self, users_table, capsys):
        users_table.list_columns()

        captured = capsys.readouterr()
        assert captured.out.splitlines() == [
            "0      id",
            "1      name",
            "2      is_active",
        ]

    def test_list_columns_detailed_output(self, users_table, capsys):
        users_table.list_columns(detailed=True)

        captured = capsys.readouterr()
        assert captured.out.splitlines() == [
            "0      id      <class 'int'>",
            "1      name      <class 'str'>",
            "2      is_active      <class 'bool'>",
        ]

    @pytest.mark.xfail(reason="Table.create_column silently overwrites duplicate column names")
    def test_create_column_should_reject_duplicate_column_name(self):
        table = Table("users")
        original = table.create_column("id", int)

        with pytest.raises(ValueError, match="already exists"):
            table.create_column("id", str)

        assert table.columns["id"] is original
        assert table.columns["id"].dtype is int

    @pytest.mark.xfail(reason="Table.add_row does not validate values against column dtypes")
    def test_add_row_should_validate_value_types(self, users_table):
        with pytest.raises(TypeError, match="id"):
            users_table.add_row({"id": "wrong-type", "name": "Ada", "is_active": True})

    @pytest.mark.xfail(reason="Table.add_row stores the original dict instead of a defensive copy")
    def test_add_row_should_not_allow_external_mutation_of_stored_rows(self, users_table):
        row = {"id": 1, "name": "Ada", "is_active": True}

        users_table.add_row(row)
        row["name"] = "Mutated after insert"

        assert users_table.rows[0]["name"] == "Ada"


class TestDatabase:
    def test_initializes_with_name_metadata_and_empty_tables(self):
        database = Database("app_db", metadata="testing")

        assert database.name == "app_db"
        assert database.metadata == "testing"
        assert database.tables == {}

    def test_create_table_registers_and_returns_table(self):
        database = Database("app_db")

        table = database.create_table("users")

        assert table is database.tables["users"]
        assert table.name == "users"
        assert table.columns == {}
        assert table.rows == []

    def test_create_table_rejects_duplicate_name_without_replacing_existing_table(self):
        database = Database("app_db")
        original = database.create_table("users")

        with pytest.raises(ValueError, match="Table with name users already exists"):
            database.create_table("users")

        assert database.tables["users"] is original

    def test_get_table_returns_existing_table(self, database_with_users):
        fetched = database_with_users.get_table("users")

        assert fetched is database_with_users.tables["users"]

    def test_get_table_raises_clear_error_for_missing_table(self):
        database = Database("app_db")

        with pytest.raises(ValueError, match="Table with name users does not exist in database app_db"):
            database.get_table("users")

    def test_list_tables_on_empty_database_prints_nothing(self, capsys):
        database = Database("app_db")

        database.list_tables()

        captured = capsys.readouterr()
        assert captured.out == ""

    def test_list_tables_basic_output(self, capsys):
        database = Database("app_db")
        database.create_table("users")
        database.create_table("orders")

        database.list_tables()

        captured = capsys.readouterr()
        assert captured.out.splitlines() == [
            "0      users",
            "1      orders",
        ]

    def test_list_tables_detailed_output(self, capsys):
        database = Database("app_db")
        users = database.create_table("users")
        users.create_column("id", int)
        users.create_column("name", str)

        database.list_tables(detailed=True)

        captured = capsys.readouterr()
        assert captured.out.splitlines() == [
            "0      users      2 columns",
        ]

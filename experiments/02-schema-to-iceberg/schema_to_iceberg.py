"""Throwaway prototype for ticket 02: schema.sql -> Iceberg tables.

DuckDB executes schema.sql in an in-memory database only to derive column
types; pyiceberg then creates the real tables in a datamap database (a SQLite
SqlCatalog plus Parquet data, all inside one folder).
"""
from pathlib import Path

import duckdb
import pyarrow as pa
from pyiceberg.catalog.sql import SqlCatalog

NAMESPACE = "datamap"


def arrow_schemas(schema_sql: str) -> dict[str, pa.Schema]:
    """Run schema.sql in memory and return one Arrow schema per table.

    DuckDB's Arrow export marks every field nullable, so NOT NULL is read back
    from DuckDB's own catalog (duckdb_columns) and applied to the fields.
    """
    con = duckdb.connect()  # in memory
    con.execute(schema_sql)
    required = {
        (t, c)
        for t, c in con.execute(
            "SELECT table_name, column_name FROM duckdb_columns() "
            "WHERE NOT is_nullable"
        ).fetchall()
    }
    tables = [r[0] for r in con.execute(
        "SELECT table_name FROM duckdb_tables() ORDER BY table_name").fetchall()]
    out = {}
    for table in tables:
        arrow = con.sql(f'SELECT * FROM "{table}"').to_arrow_table().schema
        out[table] = pa.schema(
            f.with_nullable((table, f.name) not in required) for f in arrow
        )
    con.close()
    return out


class NonConformingRows(ValueError):
    """Rows that schema.sql would reject (for example a wrong vector length)."""


def append_checked(schema_sql: Path, table, rows: pa.Table) -> None:
    """Append `rows` to the Iceberg `table` only if DuckDB accepts them into
    the same table built from schema.sql.

    Iceberg has no fixed-size list, so FLOAT[768] arrives as a plain list and
    Iceberg alone accepts a vector of any length. DuckDB still enforces the
    length (and NOT NULL and types), so inserting into an empty in-memory copy
    of the schema is the check.
    """
    name = table.name()[-1]
    con = duckdb.connect()
    con.execute(Path(schema_sql).read_text())
    try:
        con.register("incoming", rows)
        con.execute(f'INSERT INTO "{name}" BY NAME SELECT * FROM incoming')
    except duckdb.Error as e:
        raise NonConformingRows(f"{name}: {e}") from e
    finally:
        con.close()
    table.append(rows)


def create_datamap(schema_sql: Path, folder: Path) -> SqlCatalog:
    """Create the datamap database in `folder` with one Iceberg table per
    CREATE TABLE in `schema_sql`, and return its catalog."""
    folder = Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    catalog = SqlCatalog(
        NAMESPACE,
        uri=f"sqlite:///{folder / 'catalog.sqlite'}",
        warehouse=f"file://{folder}",
    )
    catalog.create_namespace_if_not_exists(NAMESPACE)
    for table, schema in arrow_schemas(Path(schema_sql).read_text()).items():
        catalog.create_table(f"{NAMESPACE}.{table}", schema=schema)
    return catalog

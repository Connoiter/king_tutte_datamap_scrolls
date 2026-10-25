"""Ticket 02 round trip: schema.sql -> DuckDB (in memory) -> pyiceberg tables
in a SQLite catalog + Parquet folder -> write a row -> read it back.

Throwaway prototype. Run: uv run pytest experiments/02-schema-to-iceberg
"""
from pathlib import Path

import pyarrow as pa
import pytest
from pyiceberg.types import FloatType, ListType

from schema_to_iceberg import NonConformingRows, append_checked, create_datamap

SCHEMA = Path(__file__).with_name("schema.sql")

ROWS = {
    "documents": [{"id": "d1", "text": "hello", "title": None, "url": None}],
    "embeddings": [{"id": "d1", "high_d": [0.5] * 768}],
    "points": [{"id": "d1", "x": None, "y": None, "cluster": None}],
    "clusters": [{"cluster": 7, "layer": 0, "parent": None, "label": None}],
}
REQUIRED = {
    "documents": {"id", "text"},
    "embeddings": {"id", "high_d"},
    "points": {"id"},
    "clusters": {"cluster", "layer"},
}


@pytest.fixture
def catalog(tmp_path):
    return create_datamap(SCHEMA, tmp_path / "datamap")


def test_creates_catalog_file_and_one_table_per_create(catalog, tmp_path):
    assert (tmp_path / "datamap" / "catalog.sqlite").is_file()
    assert {n for _, n in catalog.list_tables("datamap")} == set(ROWS)


@pytest.mark.parametrize("table", list(ROWS))
def test_row_round_trips(catalog, table):
    t = catalog.load_table(f"datamap.{table}")
    t.append(pa.Table.from_pylist(ROWS[table], schema=t.schema().as_arrow()))
    got = catalog.load_table(f"datamap.{table}").scan().to_arrow().to_pylist()
    assert got == ROWS[table]


@pytest.mark.parametrize("table", list(ROWS))
def test_nullability_preserved(catalog, table):
    fields = catalog.load_table(f"datamap.{table}").schema().fields
    assert {f.name for f in fields if f.required} == REQUIRED[table]


def test_vector_is_list_of_float32(catalog):
    f = catalog.load_table("datamap.embeddings").schema().find_field("high_d")
    assert isinstance(f.field_type, ListType)
    assert isinstance(f.field_type.element_type, FloatType)


def short_vector(t):
    return pa.Table.from_pylist(
        [{"id": "d2", "high_d": [0.5] * 3}], schema=t.schema().as_arrow())


def test_iceberg_alone_accepts_wrong_vector_length(catalog):
    # Finding, not a wish: Iceberg has no fixed-size list, so FLOAT[768]
    # loses its length and a 3-long vector is written without complaint.
    t = catalog.load_table("datamap.embeddings")
    t.append(short_vector(t))
    assert t.scan().to_arrow().num_rows == 1


def test_guarded_append_rejects_wrong_vector_length(catalog):
    t = catalog.load_table("datamap.embeddings")
    with pytest.raises(NonConformingRows):
        append_checked(SCHEMA, t, short_vector(t))
    assert t.scan().to_arrow().num_rows == 0


def test_guarded_append_writes_conforming_rows(catalog):
    t = catalog.load_table("datamap.embeddings")
    rows = pa.Table.from_pylist(ROWS["embeddings"], schema=t.schema().as_arrow())
    append_checked(SCHEMA, t, rows)
    assert t.scan().to_arrow().to_pylist() == ROWS["embeddings"]

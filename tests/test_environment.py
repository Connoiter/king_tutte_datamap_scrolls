"""Smoke test for the King Tutte pipeline environment (ticket 01).

Every library the default pipeline needs must import inside the repo's
`uv` environment on Apple Silicon. Run with: `uv run pytest`.
"""

import importlib

import pytest

PIPELINE_MODULES = [
    "duckdb",
    "pyarrow",
    "pyiceberg",
    "sentence_transformers",
    "umap",
    "toponymy",
    "fast_hdbscan",
    "datamapplot",
]


@pytest.mark.parametrize("module", PIPELINE_MODULES)
def test_pipeline_library_imports(module):
    importlib.import_module(module)


def test_pyiceberg_sqlite_sql_catalog_is_usable(tmp_path):
    from pyiceberg.catalog.sql import SqlCatalog

    catalog = SqlCatalog(
        "datamap",
        uri=f"sqlite:///{tmp_path / 'catalog.db'}",
        warehouse=f"file://{tmp_path}",
    )
    catalog.create_namespace("smoke")
    assert ("smoke",) in catalog.list_namespaces()


def test_toponymy_exposes_the_pieces_seshette_uses():
    from toponymy import ToponymyClusterer  # noqa: F401
    from toponymy.llm_wrappers import OllamaNamer  # noqa: F401

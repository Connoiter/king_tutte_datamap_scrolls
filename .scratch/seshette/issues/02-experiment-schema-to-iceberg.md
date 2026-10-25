# 02: Experiment: schema.sql to Iceberg tables

**Type:** prototype

**What to build:** Answer the spec's first untested assumption: can DuckDB execute a `schema.sql` of `CREATE TABLE` statements in memory and yield column types that pyiceberg can turn into real Iceberg tables in a datamap database (a SQLite catalog plus Parquet data), with no hand-translation of the schema? The vector column of the embeddings table is the hard case. Use a throwaway schema with one table per column kind the spec needs: text, optional text, floats, integers, and a fixed-length float vector. If the route fails, find and record the smallest fallback that keeps `schema.sql` as the single source of truth.

**Blocked by:** 01 (Python environment)

**Status:** resolved

- [x] A throwaway `schema.sql` covering every column kind, including the vector column, has been turned into Iceberg tables by the DuckDB → pyiceberg route, or the exact failure is recorded.
- [x] A row has been written to and read back from each table, including a vector.
- [x] Nullable columns stay nullable, so later scribes can fill them.
- [x] The findings are written under an `## Answer` heading in this file, and if they contradict the spec, the spec is updated (or a question raised for a human) before any ticket that depends on this one starts.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.

## Answer

- **The route works, with no hand-translation.** DuckDB 2.0.0 runs the throwaway `schema.sql` in an in-memory database; `SELECT * FROM <table>` on each empty table gives an Arrow schema (`to_arrow_table().schema`); pyiceberg 0.12.0 `SqlCatalog.create_table` takes that Arrow schema directly and assigns field ids. One row per table, including a 768-float vector, was written and read back unchanged. Prototype and test: `experiments/02-schema-to-iceberg/` (throwaway; `uv run pytest experiments/02-schema-to-iceberg`, 13 passed; the datamap folder goes to pytest's `tmp_path`).
- **Type mapping that came out** (DuckDB → Arrow from DuckDB → Iceberg → Arrow read back):
  - `VARCHAR` → `string` → `string` → `large_string`
  - `FLOAT` → `float` → `float` → `float`; `DOUBLE` → `double` → `double`
  - `INTEGER` → `int32` → `int`; `BIGINT` → `int64` → `long`
  - **`FLOAT[768]` → `fixed_size_list<float>[768]` → `list<float>` (plain list) → `large_list<float>`.** Iceberg has no fixed-size list type, so the length 768 is dropped. pyiceberg accepts the fixed-size Arrow type on create and on append (when the field nullability matches), but stores and returns a plain list.
- **Nullability: one fix needed.** DuckDB's Arrow export marks every field nullable, so `NOT NULL` is lost on that path. The prototype reads `is_nullable` from DuckDB's own `duckdb_columns()` (still derived from `schema.sql`) and sets it on the Arrow fields before `create_table`. With that, `NOT NULL` columns are Iceberg `required` and the rest `optional`; optional columns accept nulls, required ones reject them (`ArrowInvalid ... declared non-nullable but contains nulls`). The vector's list *elements* come out optional; DuckDB has no syntax to say otherwise.
- **What Iceberg enforces on append:** column types and required/optional must match the table exactly (so writers should build rows with `table.schema().as_arrow()`), extra columns are rejected, missing optional columns are allowed. **A vector of the wrong length (3 instead of 768) is accepted.**
- **Smallest fallback for the vector length** (keeps `schema.sql` the single source of truth): before appending, insert the rows into an empty in-memory DuckDB copy of `schema.sql` (`INSERT INTO t BY NAME SELECT * FROM incoming`). DuckDB enforces `FLOAT[768]` (`Cannot cast list with length 3 to array with length 768`), `NOT NULL` and types. The prototype's `append_checked` does this and is tested; the same DuckDB check also works as the "every table conforms to `schema.sql`" test.
- **Spec impact (for a human to decide; spec not edited):** the spec says the schema itself rejects data of the wrong shape (user story 22) and that Iceberg tables are created from `schema.sql`. That holds for column names, types and nullability, but **not for the vector length**: in the Iceberg tables `high_d` is an unbounded `list<float>`. Either the spec accepts that conformance for the vector length is a DuckDB check that scribes run on write (and the run tests run on the result), or it needs another mechanism. Also, `NOT NULL` needs the small `duckdb_columns()` step above; "pyiceberg creates the tables from the types DuckDB derives" is true only if "types" includes nullability read from DuckDB's catalog, not from its Arrow export.
- **Layout note:** with `warehouse=file://<folder>` and namespace `datamap`, data lands at `datamap/catalog.sqlite` and `datamap/datamap/<table>/{data,metadata}/`. Metadata and manifests hold absolute `file://` paths, as the spec already expects.

# 02: Experiment: schema.sql to Iceberg tables

**Type:** prototype

**What to build:** Answer the spec's first untested assumption: can DuckDB execute a `schema.sql` of `CREATE TABLE` statements in memory and yield column types that pyiceberg can turn into real Iceberg tables in a datamap database (a SQLite catalog plus Parquet data), with no hand-translation of the schema? The vector column of the embeddings table is the hard case. Use a throwaway schema with one table per column kind the spec needs: text, optional text, floats, integers, and a fixed-length float vector. If the route fails, find and record the smallest fallback that keeps `schema.sql` as the single source of truth.

**Blocked by:** 01 (Python environment)

**Status:** ready-for-agent

- [ ] A throwaway `schema.sql` covering every column kind, including the vector column, has been turned into Iceberg tables by the DuckDB → pyiceberg route, or the exact failure is recorded.
- [ ] A row has been written to and read back from each table, including a vector.
- [ ] Nullable columns stay nullable, so later scribes can fill them.
- [ ] The findings are written under an `## Answer` heading in this file, and if they contradict the spec, the spec is updated (or a question raised for a human) before any ticket that depends on this one starts.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.

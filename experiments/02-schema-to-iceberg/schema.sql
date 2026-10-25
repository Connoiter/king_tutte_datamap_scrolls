-- Throwaway schema for ticket 02: one table per column kind the spec needs.
-- NOT the Vectron Data Map Schema.
CREATE TABLE documents (
    id    VARCHAR NOT NULL,   -- text, required
    text  VARCHAR NOT NULL,   -- text, required
    title VARCHAR,            -- optional text
    url   VARCHAR             -- optional text
);
CREATE TABLE embeddings (
    id     VARCHAR NOT NULL,
    high_d FLOAT[768] NOT NULL  -- fixed-length float vector
);
CREATE TABLE points (
    id      VARCHAR NOT NULL,
    x       FLOAT,            -- floats, filled later
    y       DOUBLE,
    cluster INTEGER           -- integers, filled later
);
CREATE TABLE clusters (
    cluster BIGINT NOT NULL,
    layer   INTEGER NOT NULL,
    parent  BIGINT,
    label   VARCHAR
);

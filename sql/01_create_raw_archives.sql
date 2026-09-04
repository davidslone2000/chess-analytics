-- Load the raw jsons into my postgres database to be cleaned and transformed into a more usable format.

CREATE TABLE raw_archives(
    source_month DATE PRIMARY KEY,
    source_file TEXT NOT NULL, 
    raw_json JSONB NOT NULL, 
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'raw_archives'
ORDER BY ordinal_position;

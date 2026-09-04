import json
import psycopg
from pathlib import Path
from psycopg.types.json import Jsonb


def load_json_file(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data

raw_files = Path("data/raw").glob("*.json")

conn = psycopg.connect(
    dbname="chess_analytics",
    user="david",
    host="localhost",
    port=5432
)

cur = conn.cursor()

insert_query = """
INSERT INTO raw_archives (
    source_month,
    source_file,
    raw_json
)
VALUES (%s, %s, %s)
ON CONFLICT (source_month) DO NOTHING;
"""

for file_path in raw_files:
    data = load_json_file(file_path)
    source_file = file_path.name    
    source_month = source_file.replace("chess_games_", "").replace(".json", "")
    source_month = source_month.replace("_", "-") + "-01"

    cur.execute(
    insert_query,
    (source_month, source_file, Jsonb(data)))

    
    print(source_file, source_month)    

conn.commit()
conn.close()

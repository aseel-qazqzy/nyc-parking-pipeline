"""Load raw CSVs in data/ into the DuckDB source tables that the bronze models read from."""
import argparse
import os

import duckdb

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load(db_path: str) -> None:
    con = duckdb.connect(db_path)
    con.execute(f"""
        CREATE OR REPLACE TABLE parking_violation_codes AS
        SELECT * FROM read_csv_auto(
            '{os.path.join(DATA_DIR, "dof_parking_violation_codes.csv")}',
            normalize_names=true
        )
    """)
    con.execute(f"""
        CREATE OR REPLACE TABLE parking_violation_2023 AS
        SELECT * FROM read_csv_auto(
            '{os.path.join(DATA_DIR, "parking_violations_issued_fiscal_year_2023_sample.csv")}',
            normalize_names=true
        )
    """)
    con.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("db_path")
    args = parser.parse_args()
    load(args.db_path)

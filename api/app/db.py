"""Database access helpers.

Thin wrapper over psycopg. We open a connection per request rather than
using a pool -- the volumes here are small and a pool was more machinery
than the problem needed.
"""

import psycopg
from psycopg.rows import dict_row

from app.config import DATABASE_URL


def connect():
    """Open a new database connection with dict-style rows."""
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def query(sql: str, params: tuple = ()) -> list[dict]:
    """Run a SELECT and return all rows as a list of dictionaries."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()


def execute(sql: str, params: tuple = ()) -> None:
    """Run an INSERT/UPDATE/DELETE and commit it."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()

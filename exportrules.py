from pathlib import Path
from typing import Generator, Tuple

import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor, RealDictRow


def _get_export_dir() -> Path:
    export_dir: Path = Path(__file__).resolve().parent / "rules/"
    export_dir.mkdir(exist_ok=True)
    return export_dir


def _open_database_connection() -> Tuple[connection, RealDictCursor]:
    # qwitus_cotisations/modules/qwitus_cotisations/batch/batch/core/data.py
    # read_data_as_list_of_dicts
    conn = psycopg2.connect(
        database="dev_iso_prod_2023_04_06_anon",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432,
        cursor_factory=psycopg2.extras.RealDictCursor,
    )
    cur = conn.cursor()
    return conn, cur


def _fetch_rules(cur: RealDictCursor) -> Generator[RealDictRow, None, None]:
    cur.execute(r"SELECT name, short_name, type_, algorithm FROM rule_engine")
    for rule in cur:
        yield rule


def _rule_to_output_string(rule: RealDictRow) -> str:
    output: str = ""
    output += "# ---\n"
    for key in rule.keys():
        if key == "algorithm":
            continue
        column: str = key.replace("_", " ").strip().title()
        value: str = rule[key]
        output += f"# {column}: {value}\n"
    output += "# ---\n\n"
    output += rule["algorithm"].strip() + "\n"
    return output


def _close_database_connection(conn: connection, cur: RealDictCursor) -> None:
    cur.close()
    conn.close()


def main() -> None:
    export_dir: Path = _get_export_dir()
    conn, cur = _open_database_connection()
    rule: RealDictRow
    for rule in _fetch_rules(cur):
        rule_name: str = rule["short_name"]
        out_file: str = str(export_dir / rule_name) + ".py"
        with open(out_file, "w") as f:
            f.write(_rule_to_output_string(rule))
    _close_database_connection(conn, cur)


if __name__ == "__main__":
    main()

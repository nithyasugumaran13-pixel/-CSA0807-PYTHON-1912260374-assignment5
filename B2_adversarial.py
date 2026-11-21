
import csv
import sqlite3
from pathlib import Path

# B2 - ENGINEER ADVERSARIAL DATA

BASE = Path(__file__).parent
TEST_FOLDER = BASE / "adversarial_inputs"
TEST_FOLDER.mkdir(exist_ok=True)

REQUIRED_COLUMNS = {"station", "date", "pm25"}


# Create four problematic input files
def create_test_files():

    (TEST_FOLDER / "missing_column.csv").write_text(
        "station,date\nAdyar,2026-10-01\n",
        encoding="utf-8"
    )

    (TEST_FOLDER / "wrong_delimiter.csv").write_text(
        "station;date;pm25\nAdyar;2026-10-01;48\n",
        encoding="utf-8"
    )

    (TEST_FOLDER / "different_encoding.csv").write_text(
        "station,date,pm25\nCafé,2026-10-01,48\n",
        encoding="utf-16"
    )

    (TEST_FOLDER / "empty.csv").write_text(
        "",
        encoding="utf-8"
    )


# Validate input CSV files
def inspect_file(path):

    if path.stat().st_size == 0:
        return "REJECTED: Empty file"

    try:
        try:
            file = path.open(
                "r", encoding="utf-8-sig", newline=""
            )
            file.read(1)
            file.seek(0)

        except UnicodeDecodeError:
            file = path.open(
                "r", encoding="utf-16", newline=""
            )

        with file:

            sample = file.read(2048)
            file.seek(0)

            try:
                dialect = csv.Sniffer().sniff(
                    sample, delimiters=",;\t"
                )
            except csv.Error:
                dialect = csv.excel

            reader = csv.DictReader(
                file, dialect=dialect
            )

            columns = set(reader.fieldnames or [])
            missing = REQUIRED_COLUMNS - columns

            if missing:
                return f"REJECTED: Missing columns {sorted(missing)}"

            rows = list(reader)

            return (
                f"ACCEPTED: {len(rows)} rows, "
                f"delimiter={dialect.delimiter!r}"
            )

    except (UnicodeError, OSError, csv.Error) as error:
        return f"REJECTED: {error}"


# Complete Code TODOs: SQLite insertion and parameterised query
def complete_sql_todos():

    readings = [
        ("Adyar", "2026-10-01", 48.0),
        ("Guindy", "2026-10-01", 95.0),
        ("Guindy", "2026-10-03", 121.0),
        ("Adyar", "2026-10-04", 60.0)
    ]

    con = sqlite3.connect(":memory:")

    con.execute("""
        CREATE TABLE aq (
            station TEXT,
            day TEXT,
            pm25 REAL
        )
    """)

    # TODO 1: Insert all readings using ONE executemany call
    con.executemany(
        "INSERT INTO aq VALUES (?, ?, ?)",
        readings
    )
    con.commit()

    # TODO 2: Parameterised SELECT query
    def station_average(name):

        result = con.execute(
            "SELECT AVG(pm25) FROM aq WHERE station = ?",
            (name,)
        ).fetchone()

        return result[0]

    print("\nCOMPLETE THE CODE")
    print("-----------------")

    print(
        station_average("Adyar"),
        station_average("Guindy")
    )

    print(
        station_average("Adyar' OR '1'='1")
    )

    con.close()


# SQL injection demonstration
def sql_injection_test():

    con = sqlite3.connect(":memory:")

    con.execute(
        "CREATE TABLE aq (station TEXT, pm25 REAL)"
    )

    con.executemany(
        "INSERT INTO aq VALUES (?, ?)",
        [
            ("Adyar", 48.0),
            ("Guindy", 95.0),
            ("Salem", 25.0),
            ("O'Brien Station", 33.0)
        ]
    )

    print("\nSQL INJECTION TEST")
    print("------------------")

    # Unsafe query using string concatenation
    name = "O'Brien Station"

    unsafe_query = (
        "SELECT * FROM aq WHERE station = '" + name + "'"
    )

    try:
        print(con.execute(unsafe_query).fetchall())
    except sqlite3.Error as error:
        print("Unsafe query error:", error)

    # Injection attempt
    attack = "Adyar' OR '1'='1"

    unsafe_attack = (
        "SELECT * FROM aq WHERE station = '" + attack + "'"
    )

    print(
        "Unsafe injection result:",
        con.execute(unsafe_attack).fetchall()
    )

    # Safe parameterised query
    safe_result = con.execute(
        "SELECT * FROM aq WHERE station = ?",
        (attack,)
    ).fetchall()

    print("Safe injection result:", safe_result)

    con.close()


# Simple sentiment scorer for adversarial sentences
def sentiment_score(text):

    positive = {
        "good", "clean", "fast", "helpful", "improved"
    }

    negative = {
        "bad", "dirty", "slow", "rude", "smoke", "broken"
    }

    negators = {"not", "never", "no"}

    words = (
        text.lower()
        .replace(".", " ")
        .replace(",", " ")
        .split()
    )

    total = 0

    for i, word in enumerate(words):

        if word in positive:
            value = 1
        elif word in negative:
            value = -1
        else:
            value = 0

        if i > 0 and words[i - 1] in negators:
            value *= -1

        total += value

    return total


def main():

    print("B2 - ADVERSARIAL DATA TESTING")
    print("============================")

    create_test_files()

    print("\nFILE VALIDATION")
    print("---------------")

    filenames = [
        "missing_column.csv",
        "wrong_delimiter.csv",
        "different_encoding.csv",
        "empty.csv"
    ]

    for filename in filenames:

        path = TEST_FOLDER / filename

        print(filename, ":", inspect_file(path))

    complete_sql_todos()

    sql_injection_test()

    print("\nSENTIMENT STRESS TEST")
    print("---------------------")

    cases = [
        "The road is clean and service is fast.",
        "Great, another day breathing factory smoke.",
        "The service is not bad.",
        "The service is not not good.",
        "The park is clean but the bus is slow.",
        "The app is broken but staff are helpful."
    ]

    for sentence in cases:

        print(
            sentiment_score(sentence),
            "|",
            sentence
        )

    print("\nOBSERVATIONS")
    print("------------")
    print("Missing columns must be rejected.")
    print("Wrong delimiters require format detection.")
    print("Different encodings require correct decoding.")
    print("Empty files must be rejected.")
    print("Parameterized queries protect against SQL injection.")
    print("Lexicon sentiment has difficulty understanding sarcasm.")
    print("Mixed opinions and double negatives can produce incorrect scores.")


if __name__ == "__main__":
    main()

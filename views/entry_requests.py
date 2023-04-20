import sqlite3
from models import Entry, Mood


def get_all_entries():
    """Using SQL database to get all entries"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.mood_id,
            e.date,
            e.entry,
            m.label         
        FROM Entry e
        Join Mood m
            ON m.id = e.mood_id
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['mood_id'],row['date'], row['entry'], )

            mood = Mood(row['id'], row['label'], )
            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    return entries

def get_entries_by_term(searched_term):
    """Using SQL database to get searched entries"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label         
        FROM Entry e
        Join Mood m
            ON m.id = e.mood_id
            WHERE e.entry LIKE ?
        """,(f'%{searched_term}%',))

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['mood_id'],row['date'], row['entry'],)

            mood = Mood(row['id'], row['label'], )
            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    return entries

def get_single_entry(id):
    """New single entry request for SQL"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date         
        FROM Entry e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'],
                data['mood_id'], data['date'])

        return entry.__dict__

def create_entry(new_entry):
    """Add to SQL database"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO "Entry"
            ( concept, entry, mood_id, date )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date'], ))

        id = db_cursor.lastrowid
        new_entry['id'] = id

    return new_entry

def delete_entry(id):
    """Delete from SQL"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Entry
        WHERE id = ?
        """, (id, ))

def update_entry(id, new_entry):
    """UPDATE in SQL"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entry
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
        WHERE id = ?
        """,
        (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

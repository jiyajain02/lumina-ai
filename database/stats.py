import sqlite3

DB_PATH = "database/lumina.db"


def add_xp(username, xp_to_add):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM study_stats WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    if user is None:

        cursor.execute(
            """
            INSERT INTO study_stats
            (username, xp, streak, total_sessions)
            VALUES (?, ?, ?, ?)
            """,
            (username, xp_to_add, 0, 1)
        )

    else:

        cursor.execute(
            """
            UPDATE study_stats
            SET xp = xp + ?,
                total_sessions = total_sessions + 1
            WHERE username = ?
            """,
            (xp_to_add, username)
        )

    conn.commit()
    conn.close()


def get_stats(username):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT xp, streak, total_sessions
        FROM study_stats
        WHERE username=?
        """,
        (username,)
    )

    stats = cursor.fetchone()

    conn.close()

    return stats
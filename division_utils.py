from database import connect


def get_division(level, points):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT division
    FROM division_rules
    WHERE level=?
    AND ? BETWEEN min_points AND max_points
    """, (level, points))

    row = cur.fetchone()

    conn.close()

    if row:
        return row[0]

    return "UNKNOWN"


def get_rules(level):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT id,
           division,
           min_points,
           max_points
    FROM division_rules
    WHERE level=?
    ORDER BY min_points
    """, (level,))

    rows = cur.fetchall()

    conn.close()

    return rows


def update_rule(rule_id, minimum, maximum):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE division_rules
    SET min_points=?,
        max_points=?
    WHERE id=?
    """, (
        minimum,
        maximum,
        rule_id
    ))

    conn.commit()
    conn.close()
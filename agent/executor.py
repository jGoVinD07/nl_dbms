def execute_sql(cursor, conn, sql):
    """
    Execute SQL and return (success, results_or_error).
    Handles SELECT separately from DML/DDL.
    To add result formatting (CSV, tables), modify this file.
    """
    try:
        cursor.execute(sql)

        if sql.upper().startswith("SELECT"):
            rows = cursor.fetchall()
            return True, rows
        else:
            conn.commit()
            return True, None

    except Exception as e:
        conn.rollback()
        return False, str(e)

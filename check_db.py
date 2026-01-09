import sqlite3

conn = sqlite3.connect("todoapp.db")
cursor = conn.cursor()

def print_table(name):
    cursor.execute(f"PRAGMA table_info({name});")
    columns = [col[1] for col in cursor.fetchall()]
    cursor.execute(f"SELECT * FROM {name};")
    rows = cursor.fetchall()
    print(f"\n{name.upper()}:")
    for row in rows:
        print({col: val for col, val in zip(columns, row)})

for table in ['user', 'task']:
    print_table(table)

conn.close()

import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("DELETE FROM django_migrations WHERE app='account';")
conn.commit()
print('Orphaned account migrations removed.')
conn.close() 
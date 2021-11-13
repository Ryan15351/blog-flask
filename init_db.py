import sqlite3

conexao = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conexao.executescript(f.read())

cur = conexao.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
    ('First Post', 'Content for the first post')
    )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')

)

conexao.commit()
conexao.close()
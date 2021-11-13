from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import sqlite3


def get_db_conection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
def get_post(post_id):
    conn = get_db_conection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


#<<Parte do Flask>>#


app = Flask(__name__)
app.config['SECRET_KEY'] = 'palavra'


@app.route('/home')
def screen_home():
    conn = get_db_conection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        titulo = request.form['title']
        conteudo = request.form['content']

        if not titulo:
            flash('Não se esqueça de colocar um Título na sua postagem!!!')
        else:
            conn = get_db_conection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (titulo, conteudo))
            conn.commit()
            conn.close()
            return redirect(url_for('screen_home'))

    return render_template('create.html')    



@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        titulo = request.form['title']
        conteudo = request.form['content']

        if not titulo:
            flash('Insira um Título válido!!!')
        else:
            conn = get_db_conection()
            conn.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (titulo, conteudo, id))
            conn.commit()
            conn.close()
            flash('Sucesso ao Criar sua postagem!!')
            return redirect(url_for('screen_home'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_conection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" Sucesso ao deletar sua postagem!!'.format(post['title']))
    return redirect(url_for('screen_home'))

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
from datetime import datetime

from pytz import timezone
from flask import (
    Blueprint,
    abort,
    render_template,
    request,
    redirect,
    url_for,
    g,
    flash,
)

from .auth import login_required
from .db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, updated, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Body is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)' ' VALUES (?, ?, ?)',
                (title, body, g.user['id']),
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('blog/create.html')


@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    post = (
        get_db()
        .execute(
            'SELECT p.id, title, body, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?',
            (id,),
        )
        .fetchone()
    )
    if post is None:
        abort(404)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Body is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, updated = ? WHERE id = ?',
                (
                    title,
                    body,
                    datetime.now(timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),
                    id,
                ),
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('blog/edit.html', post=post)


@bp.route('/delete/<int:id>', methods=('DELETE',))
@login_required
def delete(id):
    db = get_db()
    post = db.execute(
        'SELECT id FROM post WHERE id = ?',
        (id,),
    ).fetchone()
    if post is None:
        abort(404)

    res = db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    if res.rowcount == 0:
        flash('Post not found.')
        return redirect(url_for('index'))

    return {'message': 'success'}

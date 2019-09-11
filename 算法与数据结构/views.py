# coding=utf8

import base64
import functools
from contextlib import contextmanager

from flask import (
    Flask,
    jsonify,
    request
)
from psycopg2.extras import NamedTupleCursor
from psycopg2.pool import ThreadedConnectionPool

app = Flask(__name__)


def login_required(func):
    @functools.wraps(func)
    def route_endpoint(*args, **kwargs):
        headers = dict(request.headers)
        if 'Token' not in headers:
            return jsonify({'state': -1, 'error': 'may be you should login and use token to request.'})
        _token = base64.b64decode(headers['Token'].encode()).decode().split(':')
        with pool_execute() as cur:
            cur.execute('select id, login, access_token, is_admin from res_users where login = %s', (_token[0],))
            data = cur.fetchone()
        if data.access_token != headers['Token']:
            print(data.access_token, headers['Token'])
            return jsonify({'state': -1, 'error': 'your session is expired.'})
        request.environ.update({'user': data})
        return func(*args, **kwargs)

    return route_endpoint


def session_info(user, update_session=None):
    val = {'id': user.id, 'login': user.login, 'is_admin': user.is_admin, 'session_id': user.access_token}
    if update_session:
        session_id = base64.b64encode(':'.join([str(user.login), str(time.time())]).encode()).decode()
        update_session.execute('update res_users set access_token = %s where id = %s', (session_id, user.id))
        val.update({'session_id': session_id})
    return val


pg_pool = ThreadedConnectionPool(minconn=1, maxconn=10, dbname='auth_manager', user='interview', password='interview')


@contextmanager
def pool_execute():
    conn = pg_pool.getconn()
    cur = conn.cursor(cursor_factory=NamedTupleCursor)
    yield cur
    conn.commit()
    cur.close()
    pg_pool.putconn(conn)


@app.route('/api/login', methods=['GET', 'POST'])
def authenticate():
    auth_encode = request.headers['Authorization'].split(' ')[-1]
    uid, pw = base64.b64decode(auth_encode.encode()).decode().split(':')
    with pool_execute() as cur:
        cur.execute('select * from res_users where login = %s', (uid,))
        user_obj = cur.fetchone()
        if not user_obj:
            return jsonify({'state': -1, 'error': 'no such user'})
        if user_obj.password != pw:
            return jsonify({'state': -1, 'error': 'login error.'})
        result = jsonify({'state': 1, 'msg': session_info(user_obj, cur)})
        return result


@app.route('/api/blog', methods=['GET', 'POST'])
@login_required
def content_search():
    user_obj = request.environ['user']
    if request.method == 'GET':
        with pool_execute() as cur:
            cur.execute('select users.login as name, article.contents as content, article.id as content_id '
                        'from res_contents article '
                        'left join res_users users on (users.id = article.user_id)')
            contents = cur.fetchall()
        blog_contents = [{'name': rs.name, 'article': rs.content, 'id': rs.content_id} for rs in contents]
        return jsonify({'state': 1, 'msg': blog_contents})
    else:
        with pool_execute() as cur:
            cur.execute('insert into res_contents (contents, user_id) values (%s, %s)',
                        (request.json['data'], user_obj.id))
        return jsonify({'state': 1, 'msg': '新建文章{0}成功'.format(request.json['data'])})


@app.route('/api/blog/<int:content_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def content_publish(content_id):
    user_obj = request.environ['user']
    is_admin = user_obj.is_admin
    if request.method == 'GET':
        with pool_execute() as cur:
            cur.execute('select * from res_contents where id = %s', (content_id,))
            data = cur.fetchone()
        if not data:
            return jsonify({'state': -1, 'error': 'no such article'})
        return jsonify({'state': 1, 'msg': data.contents})
    elif request.method == 'PUT':  # 更新
        with pool_execute() as cur:
            cur.execute('select * from res_contents where id = %s', (content_id,))
            data = cur.fetchone()
        if not (is_admin or (data.user_id == user_obj.id)):
            return jsonify({'state': -1, 'error': 'you only can modify own article'})
        with pool_execute() as cur:
            cur.execute('update res_contents set contents = %s where id = %s', (request.json['data'], content_id))
        return jsonify({'state': 1, 'msg': '更新文章{0}成功'.format(request.json['data'])})
    elif request.method == 'DELETE':
        with pool_execute() as cur:
            cur.execute('select * from res_contents where id = %s', (content_id,))
            data = cur.fetchone()
        if not data:
            return jsonify({'state': -1, 'error': '没有此文章'})
        blog = data.contents
        if not (is_admin or (data.user_id == user_obj.id)):
            return jsonify({'state': -1, 'error': 'you only can delete own article'})
        with pool_execute() as cur:
            cur.execute('delete from res_contents where id = %s', (content_id,))
        return jsonify({'state': 1, 'msg': '删除文章{0}成功'.format(blog)})
    return jsonify({'state': -1, 'error': '方法未实现'})

# coding=utf8

from flask import (
    Flask,
    g
)
from flask_restful import reqparse, abort, Api, Resource

from .models import pool_execute
from .utils import session_info, login_required

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('data')
parser.add_argument('login')
parser.add_argument('password')


class Session(Resource):
    @login_required
    def get(self):
        return {'id': g.user.id, 'login': g.user.login, 'session_id': g.user.access_token,
                'is_admin': g.user.is_admin}, 200

    def post(self):
        args = parser.parse_args()
        login = args.get('login')
        pw = args.get('password')
        if not (login and pw):
            return {'error': '登录失败'}, 401
        with pool_execute(True) as cur:
            cur.execute('select * from res_users where login = %s', (login,))
            user_obj = cur.fetchone()
            if not user_obj:
                return {'error': '对账或密码错误'}, 401
            if user_obj.password != pw:
                return {'error': '对账或密码错误'}, 401
            result = session_info(user_obj, cur)
        return result, 201


class Content(Resource):
    @login_required
    def get(self, content_id):
        with pool_execute() as cur:
            cur.execute('select * from res_contents where id = %s', (content_id,))
            data = cur.fetchone()
        if not data:
            abort(404, message="content {} doesn't exist".format(content_id))
        return {'content_id': data.id, 'contents': data.contents, 'user_id': data.user_id}, 200

    @login_required
    def put(self, content_id):
        user_obj = g.user
        is_admin = user_obj.is_admin
        args = parser.parse_args()
        with pool_execute(True) as cur:
            cur.execute('select * from res_contents where id = %s', (content_id,))
            data = cur.fetchone()
            if not data:
                abort(404, error="content {} doesn't exist".format(content_id))
            if not (is_admin or (data.user_id == user_obj.id)):
                abort(403, error="you are not permit")
            cur.execute('update res_contents set contents = %s where id = %s', (args['data'], content_id))
        return {'content_id': data.id, 'contents': args['data'], 'user_id': data.user_id}, 201

    @login_required
    def delete(self, content_id):
        user_obj = g.user
        is_admin = user_obj.is_admin
        with pool_execute(True) as cur:
            cur.execute('select * from res_contents where id = %s', (content_id,))
            data = cur.fetchone()
            if not data:
                abort(404, error="content {} doesn't exist".format(content_id))
            if not (is_admin or (data.user_id == user_obj.id)):
                abort(403, error="you are not permit")
            cur.execute('delete from res_contents where id = %s', (content_id,))
        return '', 204


class ContentList(Resource):
    @login_required
    def get(self):
        with pool_execute() as cur:
            cur.execute('select users.login as name, article.contents as content, article.id as content_id '
                        'from res_contents article '
                        'left join res_users users on (users.id = article.user_id)')
            contents = cur.fetchall()
        blog_contents = [{'name': rs.name, 'article': rs.content, 'id': rs.content_id} for rs in contents]
        return blog_contents, 200

    @login_required
    def post(self):
        user_obj = g.user
        args = parser.parse_args()
        with pool_execute(True) as cur:
            cur.execute('insert into res_contents (contents, user_id) values (%s, %s) returning id',
                        (args['data'], user_obj.id))
            data = cur.fetchone()
        return {'content_id': data.id, 'contents': args['data'], 'user_id': user_obj.id}, 201


api.add_resource(Session, '/api/session')
api.add_resource(ContentList, '/api/contents')
api.add_resource(Content, '/api/contents/<int:content_id>')

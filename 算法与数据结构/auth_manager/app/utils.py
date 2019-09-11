# coding=utf8

import base64
import functools
import time

from flask import request, g

from .models import pool_execute


def login_required(func):
    @functools.wraps(func)
    def route_endpoint(*args, **kwargs):
        headers = dict(request.headers)
        if 'Token' not in headers:
            return {'error': '登录失败'}, 401
        _token = base64.b64decode(headers['Token'].encode()).decode().split(':')
        with pool_execute() as cur:
            cur.execute('select id, login, access_token, is_admin from res_users where login = %s', (_token[0],))
            data = cur.fetchone()
        if (not data) or (data.access_token != headers['Token']):
            return {'error': '登录失败'}, 401
        g.user = data
        return func(*args, **kwargs)

    return route_endpoint


def session_info(user, update_session=None):
    val = {'id': user.id, 'login': user.login, 'is_admin': user.is_admin, 'session_id': user.access_token}
    if update_session:
        session_id = base64.b64encode(':'.join([str(user.login), str(time.time())]).encode()).decode()
        update_session.execute('update res_users set access_token = %s where id = %s', (session_id, user.id))
        val.update({'session_id': session_id})
    return val

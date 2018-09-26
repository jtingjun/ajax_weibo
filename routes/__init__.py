import os.path

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from models.session import Session
from models.user import User
from models.weibo import Weibo
from models.comment import Comment
from utils import log

import random
import json

from flask import (
    request,
    url_for,
    current_app,
    jsonify,
    redirect,
)
from functools import wraps


def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def initialized_environment():
    parent = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(parent, 'templates')
    loader = FileSystemLoader(path)
    e = Environment(loader=loader)
    return e


class Template:
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        template = cls.e.get_template(filename)
        return template.render(*args, **kwargs)


def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.find_by(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.find_by(id=user_id)
            return u
    else:
        return User.guest()


def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def formatted_header(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} OK GUA\r\n'.format(code)
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def html_response(body, headers=None):
    h = {
        'Content-Type': 'text/html',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_header(headers)
    r = header + '\r\n' + body
    return r.encode()


def json_response(data, headers=None):
    """
    本函数返回 json 格式的 body 数据
    前端的 ajax 函数就可以用 JSON.parse 解析出格式化的数据
    """
    h = {
        'Content-Type': 'application/json',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_header(headers)
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode()


def login_required(route_function):
    @wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u.is_guest():
            log('游客用户')
            redirection = redirect(url_for('user.login_view'))
            response = current_app.make_response(redirection)
            return response
        else:
            log('登录用户', route_function)
            return route_function()

    return f


def weibo_owner_required(route_function):
    @wraps(route_function)
    def f():
        u = current_user()
        if 'id' in request.args:
            weibo_id = request.args['id']
        else:
            form = request.get_json()
            log('weibo form', form)
            weibo_id = form['id']
        w = Weibo.find_by(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function()
        else:
            d = dict(
                message="您没有此操作的权限！"
            )
            return jsonify(d)

    return f


def comment_owner_required(route_function):
    @wraps(route_function)
    def f():
        u = current_user()
        if 'id' in request.args:
            comment_id = request.args['id']
        else:
            form = request.get_json()
            log('comment form', form)
            comment_id = form['id']

        c = Comment.find_by(id=int(comment_id))
        weibo_id = c.weibo_id
        w = Weibo.find_by(id=int(weibo_id))
        # 用户id和评论用户id一致或与微博所有者id一致则可执行
        if c.user_id == u.id or w.user_id == u.id:
            return route_function()
        else:
            d = dict(
                message="您没有此操作的权限！"
            )
            return jsonify(d)

    return f

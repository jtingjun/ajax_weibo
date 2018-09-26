from utils import log
from routes import current_user
from models.weibo import Weibo
from models.comment import Comment
from routes.__init__ import (
    login_required,
    weibo_owner_required,
    comment_owner_required,
)

from flask import (
    Blueprint,
    request,
    jsonify,
)


bp = Blueprint('api_weibo', __name__)


@bp.route('/api/weibo/all')
@login_required
def all():
    weibos = []
    ws = Weibo.all()
    for w in ws:
        # 获得每个weibo对应的评论
        cs = w.comments()
        comments = []
        w_username = w.user().username
        # 序列化comment并为每个评论添加用户名
        for c in cs:
            username = c.user().username
            c = c.json()
            c['username'] = username
            comments.append(c)

        w = w.json()
        # 将评论插入到对应的微博字典中
        w['comments'] = comments
        w['username'] = w_username
        weibos.append(w)

    return jsonify(weibos)


@bp.route('/api/weibo/add', methods=['POST'])
@login_required
def add():
    form = request.get_json()
    u = current_user()
    w = Weibo.add(form, u.id)
    w.username = u.username
    return jsonify(w.json())


@bp.route('/api/weibo/delete')
@weibo_owner_required
@login_required
def delete():
    weibo_id = int(request.args['id'])
    Weibo.delete(weibo_id)
    d = dict(
        message="成功删除 weibo"
    )
    return jsonify(d)


@bp.route('/api/weibo/update', methods=['POST'])
@weibo_owner_required
@login_required
def update():
    """
    用于增加新 weibo 的路由函数
    """
    form = request.get_json()
    log('api weibo update form', form)
    w = Weibo.update(**form)
    return jsonify(w.json())


@bp.route('/api/comment/add', methods=['POST'])
@login_required
def add_comment():
    """
    用于增加新 comment 的路由函数
    """
    form = request.get_json()
    u = current_user()
    c = Comment.add(form, u.id)
    username = c.user().username
    c = c.json()
    c['username'] = username
    return jsonify(c)


@bp.route('/api/comment/delete')
@comment_owner_required
@login_required
def delete_comment():
    comment_id = int(request.args['id'])
    Comment.delete(comment_id)
    d = dict(
        message="成功删除 comment"
    )
    return jsonify(d)


@bp.route('/api/comment/update', methods=['POST'])
@comment_owner_required
@login_required
def update_comment():
    """
    用于更新 comment 的路由函数
    """
    form = request.get_json()
    c = Comment.update(**form)
    return jsonify(c.json())


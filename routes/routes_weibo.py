from models.comment import Comment
from models.weibo import Weibo
from routes import (
    redirect,
    Template,
    current_user,
    html_response,
    login_required,
)
from utils import log
from flask import (
    render_template,
    Blueprint,
    request,
)


bp = Blueprint('route_weibo', __name__)


@bp.route('/weibo/index')
@login_required
def index():
    """
    weibo 首页的路由函数
    """
    u = current_user()
    weibos = Weibo.find_all(user_id=u.id)
    return render_template('weibo_index.html', weibos=weibos, user=u)


def add():
    """
    用于增加新 weibo 的路由函数
    """
    u = current_user()
    form = request.form
    Weibo.add(form, u.id)
    return redirect('/weibo/index')


def delete():
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)
    return redirect('/weibo/index')


def edit():
    weibo_id = int(request.query['id'])
    w = Weibo.find_by(id=weibo_id)
    body = Template.render('weibo_edit.html', weibo=w)
    return html_response(body)


def update():
    """
    用于增加新 weibo 的路由函数
    """
    form = request.form
    Weibo.update(form)
    return redirect('/weibo/index')


def same_user_required(route_function):
    def f(request):
        log('same_user_required')
        u = current_user()
        if 'id' in request.query:
            weibo_id = request.query['id']
        else:
            weibo_id = request.form()['id']
        w = Weibo.find_by(id=int(weibo_id))

        if w.user_id == u.id:
            return route_function(request)
        else:
            return redirect('/weibo/index')

    return f


def comment_add():
    u = current_user()
    form = request.form
    weibo = Weibo.find_by(id=int(form['weibo_id']))

    c = Comment(form)
    c.user_id = u.id
    c.weibo_id = weibo.id
    c.save()
    log('comment add', c, u, form)

    return redirect('/weibo/index')

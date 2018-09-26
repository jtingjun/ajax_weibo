from urllib.parse import unquote_plus

from models.session import Session
from routes import (
    current_user,
    random_string,
)

from utils import log
from models.user import User

from flask import (
    render_template,
    Blueprint,
    url_for,
    request,
    redirect,
    current_app,
)


bp = Blueprint('user', __name__)


@bp.route('/user/login', methods=['POST'])
def login():
    """
    登录页面的路由函数
    """
    form = request.form

    u, result = User.login(form)
    session_id = random_string()
    form = dict(
        session_id=session_id,
        user_id=u.id,
    )
    Session.new(form)

    redirection = redirect(url_for('user.login_view', result='{}'.format(result)))
    response = current_app.make_response(redirection)
    response.set_cookie('session_id', session_id, path='/')

    return response


@bp.route('/user/login/view', methods=['GET'])
def login_view():
    u = current_user()
    result = request.args.get('result', '')
    result = unquote_plus(result)

    return render_template(
        'login.html',
        username=u.username,
        result=result,
    )


@bp.route('/user/register', methods=['POST'])
def register():
    """
    注册页面的路由函数
    """
    form = request.form

    u, result = User.register(form)
    log('register post', result)

    redirection = redirect(url_for('user.register_view', result='{}'.format(result)))
    response = current_app.make_response(redirection)
    return response


@bp.route('/user/register/view', methods=['GET'])
def register_view():
    result = request.args.get('result', '')
    result = unquote_plus(result)

    return render_template('register.html', result=result)

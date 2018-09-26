from models import Model
from models.comment import Comment
from models.user import User


class Weibo(Model):
    """
    微博类
    """
    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', None)

    @classmethod
    def add(cls, form, user_id):
        w = Weibo(form)
        w.user_id = user_id
        w.save()
        return w

    def user(self):
        u = User.find_by(id=self.user_id)
        return u

    def comments(self):
        cs = Comment.find_all(weibo_id=self.id)
        return cs
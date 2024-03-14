from functools import wraps
from app.models.models import User

from flask import session, redirect


def login_required(func):
    @wraps(func)
    def login_check(*args, **kwargs):

        if 'user_id' in session:
            user = User.query.filter_by(id=session['user_id']).first()
            if user:
                result = func(*args, **kwargs)
                return result

        return redirect('/login')

    return login_check
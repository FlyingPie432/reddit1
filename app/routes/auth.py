from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models.wtfforms import UserForm
from app.models.models import User, db
from app.utils.bcrypt import bcrypt
from app.utils.sessions import session

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/home')
@auth_bp.route('/')
def index():
    return render_template('index.html', title='Home Page')


@auth_bp.route('/user/<name>')
def user_profile(name):
    return render_template('user.html', name=name, title='User Profile')


@auth_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            color = form.color.data if form.color.data else None  # Return None if color is not provided
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(name=form.name.data, email=form.email.data, color=color, password_hash=hashed_password)
            new_user.save_db()
        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        form.color.data = ""
    our_users = User.query.order_by(User.date_added)
    flash("User added successfully", 'success')
    return render_template('add_user.html', form=form, title='Add User', name=name, our_users=our_users)


@auth_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    form = UserForm()
    name_to_update = User.query.get_or_404(id)
    if request.method == 'POST':
        name_to_update.name = request.form.get('name')
        name_to_update.email = request.form.get('email')
        name_to_update.color = request.form.get('color')

        try:
            db.session.commit()
            flash("User Updated Successfully", 'success')
            return redirect(url_for('auth.add_user'))
        except:
            flash("An error occurred while updating the user", 'error')
    return render_template('update.html', form=form, name_to_update=name_to_update)


@auth_bp.route("/delete/<int:id>", methods=['GET', 'POST'])
def delete(id):
    user_to_delete = User.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted Successfully', 'success')
        our_users = User.query.order_by(User.date_added)
        return render_template('add_user.html', form=form, name=name, our_users=our_users)
    except:
        flash('Whooops! There was a problem while deleting user, try again!', 'error')
        return render_template('add_user.html', form=form, name=name, our_users=our_users)

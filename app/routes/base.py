from flask import Blueprint, render_template, flash
from app.models.wtfforms import NameForm, PostForm
from app.models.models import Posts, db
save = Posts()
base_bp = Blueprint('base', __name__)


@base_bp.route('/name', methods=['GET', 'POST'])
def name_form():
    form = NameForm()
    name = None
    if form.validate_on_submit():
        name = form.name.data
        flash("Form Submitted Successfully", "success")
    return render_template('name.html', form=form, name=name, title='Name')


from flask import redirect, url_for


@base_bp.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(
            title=form.title.data,
            author=form.author.data,
            content=form.content.data,
            slug=form.slug.data,
            submit=form.submit.data
        )

        # Saving to database
        save.save_db(post)

        flash('Post has been created successfully', 'success')
        return redirect(url_for('base.post_page'))  # Redirect to the post_page route after successful submission

    return render_template('posts/add_post.html', form=form, title='Add Post')


@base_bp.route('/post_page', methods=['GET', 'POST'])
def post_page():
    posts = Posts.query.all()
    return render_template('posts/posts.html', title='Blog Posts', posts=posts)

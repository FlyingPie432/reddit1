from flask import Blueprint, render_template, flash, redirect, url_for
from app.models.wtfforms import NameForm, PostForm
from app.models.models import Posts, db

base_bp = Blueprint('base', __name__)


@base_bp.route('/name', methods=['GET', 'POST'])
def name_form():
    form = NameForm()
    name = None
    if form.validate_on_submit():
        name = form.name.data
        flash("Form Submitted Successfully", "success")
    return render_template('name.html', form=form, name=name, title='Name')


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
        db.session.add(post)
        db.session.commit()

        flash('Post has been created successfully', 'success')
        return redirect(url_for('base.post_page'))  # Redirect to the post_page route after successful submission

    return render_template('posts/add_post.html', form=form, title='Add Post')


@base_bp.route('/post_page', methods=['GET', 'POST'])
def post_page():
    posts = Posts.query.all()
    return render_template('posts/posts.html', posts=posts)


@base_bp.route('/post_page/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('posts/post.html', post=post, title=f"Post{id}")


@base_bp.route('/edit-post/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()
        flash('Post has been updated successfully', 'success')
        return redirect(url_for('base.post_page'))  # Redirect to the post_page route after successful update

    return render_template('posts/edit_post.html', form=form, title='Edit Post', post=post)


@base_bp.route('/delete-post/<int:id>')
def delete_post(id):
    post = Posts.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    flash('Post Has Been Deleted', 'success')
    return redirect(url_for('base.post_page'))

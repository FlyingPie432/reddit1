from flask import Blueprint, render_template, flash
from app.models.wtfforms import NameForm

base_bp = Blueprint('base', __name__)


@base_bp.route('/name', methods=['GET', 'POST'])
def name_form():
    form = NameForm()
    name = None
    if form.validate_on_submit():
        name = form.name.data
        flash("Form Submitted Successfully", "success")
    return render_template('name.html', form=form, name=name, title='Name')




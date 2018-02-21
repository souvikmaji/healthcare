from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required

from app import db
from app.models.user_models import UserProfileForm
from app.models.medicine_models import UserMedicine, AddMedicineForm

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/')
def home_page():
    return render_template('pages/home_page.html')


@main_blueprint.route('/user')
@login_required
def user_page():
    return render_template('pages/user_page.html')


@main_blueprint.route('/user/add_medicine', methods=['GET', 'POST'])
@login_required
def user_add_medicine_page():
    form = AddMedicineForm(request.form)
    if form.validate_on_submit():
        medicine = UserMedicine(medicine_name=form.medicine_name.data)
        current_user.medicines.append(medicine)
        db.session.commit()
        return redirect(url_for('main.user_medicines_page'))

    return render_template('pages/user_add_medicine_page.html', form=form)

@main_blueprint.route('/user/medicines', methods=['GET'])
@login_required
def user_medicines_page():
    return render_template('pages/user_medicines_page.html', user=current_user)

@main_blueprint.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    form = UserProfileForm(request.form)

    if form.validate_on_submit():
        form.populate_obj(current_user)         # Copy form fields to user_profile fields
        db.session.commit()
        return redirect(url_for('main.home_page'))

    return render_template('pages/user_profile_page.html',
                           form=form)

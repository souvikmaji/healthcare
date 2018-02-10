from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required

from app import db
from app.models.user_models import UserProfileForm, AddMedicineForm, UserMedicine

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
    if request.method == 'POST' and form.validate():
        medicine = UserMedicine(medicine_name=form.medicine_name.data)
        current_user.medicines.append(medicine)
        db.session.commit()
        return 'data saved. check db'

    return render_template('pages/user_add_medicine_page.html', form=form)


@main_blueprint.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html',
                           form=form)

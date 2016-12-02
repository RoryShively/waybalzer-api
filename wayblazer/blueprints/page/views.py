import csv

from flask import (
    Blueprint,
    flash,
    redirect,
    url_for,
    render_template)

from flask_login import login_required

from wayblazer.extensions import db
from wayblazer.blueprints.page.forms import CSVForm
from wayblazer.blueprints.company.models import Company, Address
from wayblazer.blueprints.employee.models import Employee, PersonalPhone

page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
def home():
    return render_template('page/home.html')


@page.route('/csv-upload', methods=['GET', 'POST'])
@login_required
def csv_upload():
    form = CSVForm()

    if form.validate_on_submit():
        # This prevents circular imports from celery.
        # from wayblazer.blueprints.page.tasks import upload_csv

        # TODO: Get this to work with celery task instead of blocking upload
        # upload_csv.delay(filename=filename, form=form)

        file = form.csv.data
        file_data = file.read().decode("utf-8")
        file_lines = file_data.splitlines()

        reader = csv.DictReader(file_lines)
        for row in reader:

            company = Company.query.filter_by(
                name=row.get('company_name')).first()

            if not company:
                # Create company instance.
                company = Company(
                    name=row.get('company_name'),
                    web=row.get('company_web'),
                    phone=row.get('company_phone1'),
                )

                # Create address instance.
                address = Address(
                    route=row.get('company_address'),
                    city=row.get('company_city'),
                    county=row.get('company_county'),
                    state=row.get('company_state'),
                    zip=row.get('company_zip'),
                )

                # Add address to company's addresses.
                company.addresses.append(address)

                # Add model instances to db session.
                db.session.add(address)
                db.session.add(company)

            # Create employee instance.
            employee = Employee(
                first_name=row.get('employee_first_name'),
                last_name=row.get('employee_last_name'),
                email=row.get('personal_email'),
                company=company
            )

            phone = PersonalPhone.query.filter_by(
                number=row.get('personal_phone2')).first()

            if not phone:
                phone = PersonalPhone(
                    number=row.get('personal_phone2'),
                )

            phone.employees.append(employee)

            # A employee instance to db session.
            db.session.add(employee)

        # Commit Session to db.
        db.session.commit()

        flash('Your CSV is being uploaded now', 'success')
        return redirect(url_for('page.csv_upload'))
    else:
        filename = None

    return render_template('page/csv.html', form=form, filename=filename)


@page.route('/rest-docs')
def rest_docs():
    return render_template('page/rest-docs.html')


@page.route('/questions')
def questions():
    return render_template('page/questions.html')

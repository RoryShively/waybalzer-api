from flask import (
    Blueprint,
    flash,
    redirect,
    url_for,
    render_template)

from flask_login import login_required

from werkzeug.utils import secure_filename
from wayblazer.blueprints.page.forms import CSVForm

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
        from wayblazer.blueprints.page.tasks import upload_csv

        filename = secure_filename(form.csv.data.filename)

        # TODO: Get this to work with celery task instead of blocking upload
        # upload_csv.delay(filename=filename, form=form)
        form.csv.data.save('uploads/csv/' + filename)

        flash('Your CSV is being uploaded now', 'success')
        return redirect(url_for('page.csv_upload'))
    else:
        filename = None

    return render_template('page/csv.html', form=form, filename=filename)

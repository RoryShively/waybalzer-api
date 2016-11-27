from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed


class CSVForm(FlaskForm):

    csv = FileField("Upload a CSV file", validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV only'),
    ])

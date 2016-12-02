from wayblazer.app import create_celery_app


celery = create_celery_app()


@celery.task()
def upload_csv(filename, form):
    """
    Upload a csv file to `uploads/csv/`.

    :param filename: Name of uploaded file.
    :param data: File data
    :return: None
    """
    form.csv.data.save('uploads/csv/' + filename)

    return None

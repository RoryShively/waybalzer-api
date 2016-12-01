from wayblazer.app import create_app


# create_app().run(host='localhost', port=5000)

# from wayblazer.extensions import db
# from wayblazer.blueprints.user.models import User
# from wayblazer.blueprints.company.models import Company
# # from wayblazer.blueprints.employee.models import Employee
#
#
# app = create_app()
# db.app = app
#
# db.drop_all()
# db.create_all()


app = create_app()

if __name__ == "__main__":
    app.run(host='localhost', port=5000)

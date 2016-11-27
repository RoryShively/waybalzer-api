from flask import url_for


class TestPage:
    def test_home_page(self, client):
        """Home page should respond with a success 200"""

        response = client.get(url_for('page.home'))
        assert response.status_code == 200

    def test_csv_upload_page(self, client):
        response = client.get(url_for('page.csv_upload'))
        assert response.status_code == 200

    # TODO: Test csv_upload_form
    # wayblazer/blueprints/page/views.py     25 - 34
    # Need to mock a CSV file to work

    # def test_csv_upload_form(self, client):
    #     csv = MockCSVFile
    #
    #     response = client.post(url_for('page.csv_upload'), data=csv,
    #                            follow_redirect=True)
    #     assert response.status_code == 200

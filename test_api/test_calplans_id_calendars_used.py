import pytest
import requests
import settings


class TestCalplansIdCalendarsUsed:
    uri = settings.SERVER_URI + '/calplans/{0}/calendars-used'

    @pytest.mark.parametrize(
        "calplanid,status_code,response_body,request_body",
        [
            ("as", 400, {'title': 'Wrong parameter', 'message': 'calplanId is not a number'}, ''),
            ("1", 200, {
                            'plan': {'calendarId': 2, 'title': 'Без выходных'},
                            'works': {'calendarId': 2, 'title': 'Без выходных'},
                            'worksSMR': {'calendarId': 2, 'title': 'Без выходных'}
            }, ''),
            ("", 400, {'title': 'Request is invalid', 'message': 'The request was not recognized'}, ''),
            ("1000", 404, {'title': 'Resources not found', 'message': 'Wrong calplanId'}, ''),
            ('1', 400, {'title': 'Request is invalid', 'message': 'The request was not recognized'}, {"calendarId": 2})

        ]
    )
    def test_get(self, calplanid, status_code, response_body, request_body):
        if request_body:
            response = requests.get(url=self.uri.format(calplanid), json=request_body)
        else:
            response = requests.get(url=self.uri.format(calplanid))

        assert response is not None
        assert response.status_code == status_code
        assert response.json() == response_body

    @pytest.mark.parametrize(
        "calplanid,status_code,request_body,params",
        [
            ('1', 200, {"calendarId": 2}, {"purpose": "works"})
        ]
    )
    def test_patch(self, calplanid, status_code, request_body, params):
        response = requests.patch(url=self.uri.format('1'), json=request_body, params=params)

        assert response is not None
        assert response.status_code == status_code
        assert response.content == b''

    def test_patch_id_1_correct_plan(self):
        body = {"calendarId": 2}
        param ={"purpose": "plan"}
        response = requests.request(method='patch', url=self.uri.format('1'), json=body, params=param)

        assert response.status_code == 200
        assert response is not None
        assert response.content == b''
        # print(response.content)

    def test_patch_id_1_correct_worksSMR(self):
        body = {"calendarId": 2}
        param ={"purpose": "worksSMR"}
        response = requests.request(method='patch', url=self.uri.format('1'), json=body, params=param)

        assert response.status_code == 200
        assert response is not None
        assert response.content == b''

    def test_patch_id_1_not_existing_calendarId(self):
        body = {"calendarId": 1000}
        param ={"purpose": "worksSMR"}
        response = requests.request(method='patch', url=self.uri.format('1'), json=body, params=param)

        assert response.status_code == 404
        assert response is not None
        assert response.json() == {'title': 'Calendar not found', 'message': 'Data with this calplanId and '
                                                                             'this calendarId not exists'}

    def test_patch_id_1_not_correct_calendarId(self):
        body = {"calendarId": "asd"}
        param ={"purpose": "worksSMR"}
        response = requests.request(method='patch', url=self.uri.format('1'), json=body, params=param)

        assert response.status_code == 400
        assert response is not None
        assert response.json() == {'title': 'Wrong parameter', 'message': 'Invalid calendarId'}

    def test_patch_id_1_dop_query_calendarId(self):
        body = {"calendarId": "1"}
        param ={"purpose": "worksSMR", "query": "15"}
        response = requests.request(method='patch', url=self.uri.format('1'), json=body, params=param)

        assert response.status_code == 400
        assert response is not None
        assert response.json() == {'title': 'Request is invalid', 'message': 'The request was not recognized'}

    def test_patch_id_1_incorrect_calendarId(self):
        body = {"calendarId": "1"}
        param ={"purpose": "worksSMR", "query": "15"}
        response = requests.request(method='patch', url=self.uri.format('1'), json=body, params=param)

        assert response.status_code == 400
        assert response is not None
        assert response.json() == {'title': 'Request is invalid', 'message': 'The request was not recognized'}
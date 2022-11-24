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
        "calplanid,status_code,request_body,params,response_body",
        [
            ('1', 200, {"calendarId": 2}, {"purpose": "works"}, b''),
            ('1', 200, {"calendarId": 2}, {"purpose": "plan"}, b''),
            ('1', 200, {"calendarId": 2}, {"purpose": "worksSMR"}, b''),
            ('1', 404, {"calendarId": 1000}, {"purpose": "worksSMR"}, {'title': 'Calendar not found', 'message':
                                                                                'Data with this calplanId and '
                                                                                'this calendarId not exists'}),
            ('1', 400, {"calendarId": "asd"}, {"purpose": "worksSMR"}, {'title': 'Wrong parameter', 'message':
                                                                              'Invalid calendarId'}),
            ('1', 400, {"calendarId": 1}, {"purpose": "worksSMR", "query": "15"}, {'title': 'Request is invalid',
                                                                                     'message':
                                                                                         'The request was not recognized'
                                                                                     }),
            ('1000', 404, {"calendarId": 1}, {"purpose": "worksSMR"}, {
                'title': 'Calendar not found',
                'message': 'Data with this calplanId and this calendarId not exists'
            }),
            ('1', 400, {"calendarId": 1}, {"purpose": "asd"}, {'title': 'Wrong data',
                                                                                     'message':
                                                                                         'Invalid purpose value'
                                                                                     }),
            ('1', 400, {"calendarId": ""}, {"purpose": "works"}, {'title': 'Wrong parameter',
                                                               'message':
                                                                   'Invalid calendarId'}),
            ('1', 400, {"calendarId": "1", "purpose": "works"}, {"purpose": "works"}, {'title': 'Wrong data',
                                                               'message':
                                                                   'Wrong number of json parameters'}),
            ('-1', 400, {"calendarId": 2}, {"purpose": "works"}, {'title': 'Wrong parameter',
                                                               'message':
                                                                   'Invalid calplanId'}),
            ('', 400, {"calendarId": 2}, {"purpose": "works"}, {'title': 'Request is invalid',
                                                               'message': 'The request was not recognized'}),
            ('1', 400, '', {"purpose": "works"}, {'title': 'Request is invalid',
                                                               'message': 'The request was not recognized'})
        ]
    )
    def test_patch(self, calplanid, status_code, request_body, params, response_body):
        if request_body:
            response = requests.patch(url=self.uri.format(calplanid), json=request_body, params=params)
        else:
            response = requests.patch(url=self.uri.format(calplanid), params=params)

        assert response is not None
        assert response.status_code == status_code

        if response_body:
            assert response.json() == response_body
        else:
            assert response.content == response_body


class TestCalplansIdCalendarsCreated:
    uri = settings.SERVER_URI + '/calplans/{0}/calendars-created'

    @pytest.mark.parametrize(
        "calplanid,status_code,response_body,request_body",
        [
                ("1", 200, {'title': 'Wrong parameter', 'message': 'calplanId is not a number'}, ''),
        ]
    )
    def test_get(self, calplanid, status_code, response_body, request_body):

        response = requests.get(url=self.uri.format(calplanid), data=request_body)

        assert response is not None
        assert response.status_code == status_code
        if status_code == 200:
            assert response.json().get('calendars') is not None

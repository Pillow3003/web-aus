import pytest
import requests
import settings


class TestCalplansIdCalendarsUsed:
    uri = settings.SERVER_URI + "/calplans/{0}/calendars-used"

    @pytest.mark.parametrize(
        "calplanid,status_code,response_body,request_body",
        [
            (
                "1",
                200,
                {
                    "plan": {"calendarId": 1, "title": "Стандартный"},
                    "works": {"calendarId": 1, "title": "Стандартный"},
                    "worksSMR": {"calendarId": 1, "title": "Стандартный"},
                },
                "",
            ),
            (
                "as",
                400,
                {
                    "message": "Validation failed: wrong value 'as'",
                    "title": "Wrong parameters",
                },
                "",
            ),
            (
                "",
                400,
                {
                    "title": "Request is invalid",
                    "message": "The request was not recognized",
                },
                "",
            ),
            (
                "1000",
                404,
                {"title": "Resources not found", "message": "Wrong calplanId"},
                "",
            ),
            (
                "1",
                400,
                {
                    "title": "Request is invalid",
                    "message": "The request was not recognized",
                },
                {"calendarId": 2},
            ),
        ],
    )
    def test_get(
        self,
        calplanid: str,
        status_code: int,
        response_body: dict,
        request_body: str,
        storage,
    ):
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
            ("1", 200, {"calendarId": 2}, {"purpose": "works"}, b""),
            ("1", 200, {"calendarId": 2}, {"purpose": "plan"}, b""),
            ("1", 200, {"calendarId": 2}, {"purpose": "worksSMR"}, b""),
            (
                "1",
                404,
                {"calendarId": 1000},
                {"purpose": "worksSMR"},
                {
                    "title": "Resouces not found",
                    "message": "data with calplanId '1' and calendarId '1000' not exists",
                },
            ),
            (
                "1",
                400,
                {"calendarId": "asd"},
                {"purpose": "worksSMR"},
                {
                    "title": "Wrong parameters",
                    "message": "Validation failed: wrong value '0'",
                },
            ),
            (
                "1",
                400,
                {"calendarId": 1},
                {"purpose": "worksSMR", "query": "15"},
                {
                    "title": "Request is invalid",
                    "message": "The request was not recognized",
                },
            ),
            (
                "1000",
                404,
                {"calendarId": 1},
                {"purpose": "worksSMR"},
                {
                    "title": "Resouces not found",
                    "message": "data with calplanId '1000' and calendarId '1' not exists",
                },
            ),
            (
                "1",
                400,
                {"calendarId": 1},
                {"purpose": "asd"},
                {"title": "Wrong data", "message": "Invalid purpose value"},
            ),
            (
                "1",
                400,
                {"calendarId": ""},
                {"purpose": "works"},
                {
                    "title": "Wrong parameters",
                    "message": "Validation failed: wrong value '0'",
                },
            ),
            (
                "1",
                400,
                {"calendarId": "1", "purpose": "works"},
                {"purpose": "works"},
                {
                    "title": "Wrong parameters",
                    "message": "Validation failed: wrong number of json parameters",
                },
            ),
            (
                "-1",
                400,
                {"calendarId": 1},
                {"purpose": "works"},
                {
                    "title": "Wrong parameters",
                    "message": "Validation failed: wrong value '-1'",
                },
            ),
            (
                "",
                400,
                {"calendarId": 1},
                {"purpose": "works"},
                {
                    "title": "Request is invalid",
                    "message": "The request was not recognized",
                },
            ),
            (
                "1",
                400,
                "",
                {"purpose": "works"},
                {
                    "title": "Request is invalid",
                    "message": "The request was not recognized",
                },
            ),
        ],
    )
    def test_patch(
        self, calplanid, status_code, request_body, params, response_body, storage
    ):
        if request_body:
            response = requests.patch(
                url=self.uri.format(calplanid), json=request_body, params=params
            )
        else:
            response = requests.patch(url=self.uri.format(calplanid), params=params)

        assert response is not None
        assert response.status_code == status_code

        if response_body:
            assert response.json() == response_body
        else:
            assert response.content == response_body

        data = storage.execute_sql("SELECT * FROM calplan_params WHERE calplan_id = 1")
        if status_code == 200:
            plan_id = (
                str(request_body["calendarId"]) if params["purpose"] == "plan" else "1"
            )
            works_id = (
                str(request_body["calendarId"]) if params["purpose"] == "works" else "1"
            )
            smr_id = (
                str(request_body["calendarId"])
                if params["purpose"] == "worksSMR"
                else "1"
            )
            assert {(1, 30, plan_id), (1, 32, smr_id), (1, 31, works_id)} == set(data)
        else:
            assert {(1, 30, "1"), (1, 32, "1"), (1, 31, "1")} == set(data)

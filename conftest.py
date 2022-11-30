import pytest

from framework.db import DataBase
from framework.models import (
    Calplan,
    CalplanCalendars,
    Calendars,
    CalplanParams,
    CalendarShifts,
)


@pytest.fixture(scope="function")
def storage() -> DataBase:
    calplan_1 = Calplan(id=1)

    calendar_1 = Calendars(
        id=1,
        title="Стандартный",
        order=1,
        type=0,
        is_default=True,
    )
    calendar_2 = Calendars(
        id=2,
        title="Без выходных>",
        order=2,
        type=0,
        is_default=True,
    )

    cal_calendars_1 = CalplanCalendars(calplan_id=1, calendar_id=1)
    cal_calendars_2 = CalplanCalendars(calplan_id=1, calendar_id=2)

    shift_1 = CalendarShifts(calendar_id=1, shift_id=1, hours=8)
    shift_2 = CalendarShifts(calendar_id=1, shift_id=2, hours=0)
    shift_3 = CalendarShifts(calendar_id=1, shift_id=3, hours=0)

    calplan_params_1 = CalplanParams(calplan_id=1, param_id=30, param_value=1)

    calplan_params_2 = CalplanParams(calplan_id=1, param_id=31, param_value=1)

    calplan_params_3 = CalplanParams(calplan_id=1, param_id=32, param_value=1)

    db = DataBase()

    session = db.session
    session.add(calplan_1)
    session.add_all([calendar_1, calendar_2])
    session.add_all([cal_calendars_1, cal_calendars_2])
    session.commit()
    session.add_all([shift_1, shift_2, shift_3])
    session.add_all([calplan_params_1, calplan_params_2, calplan_params_3])
    session.commit()

    yield db

    db.truncate_tables(
        tables=[
            "calendars",
            "calplans",
        ]
    )

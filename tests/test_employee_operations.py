from banking.employee_operations import get_salary, terminate
from banking.models import Employee
from sqlalchemy import and_, select

from . import Session


def test_get_salary(Session):
    actual_salary = get_salary.callback('Spencer Foobar', Session)
    assert actual_salary == 150


def test_terminate(Session):
    name = 'Garrett Foobar'
    terminate.callback(name, Session)
    with Session() as session:
        result = session.execute(
            select(Employee.is_active)
            .where(and_(
                Employee.firstname == name.split(" ")[0],
                Employee.lastname == name.split(" ")[1])))
        assert result.scalar_one() is False

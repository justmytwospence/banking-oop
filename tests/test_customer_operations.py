from banking.customer_operations import change_address, onboard
from banking.models import Customer
from sqlalchemy import and_, select

from . import Session


def test_onboard(Session):
    onboard.callback('Greg Foobar', 'USA', Session)
    with Session() as session:
        new_customer = session.execute(select(Customer).where(and_(
            Customer.firstname == 'Greg',
            Customer.lastname == 'Foobar')
        )).scalar_one()
    assert new_customer


def test_change_address(Session):
    new_address = 'Fairfax Avenue'
    change_address.callback('Spencer Foobar', new_address, Session)
    with Session() as session:
        actual_address = session.execute(select(Customer.address).where(and_(
            Customer.firstname == 'Spencer',
            Customer.lastname == 'Foobar')
        )).scalar_one()
    assert actual_address == new_address

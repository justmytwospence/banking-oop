import banking.models as models
import pytest
from banking.customer_operations import change_address, onboard
from sqlalchemy import and_, select

from . import Session


def test_onboard(Session):
    onboard.callback('Greg Boucher', 'Pond View Court', Session)
    with Session() as session:
        new_customer = session.execute(select(models.Customer).where(and_(
            models.Customer.firstname == 'Greg',
            models.Customer.lastname == 'Boucher')
        )).fetchall()
    assert new_customer

def test_change_address(Session):
    new_address = 'Fairfax Avenue'
    change_address.callback('Spencer Boucher', new_address, Session)
    with Session() as session:
        address = session.execute(select(models.Customer.address).where(and_(
            models.Customer.firstname == 'Spencer',
            models.Customer.lastname == 'Boucher')
        )).scalar_one()
    assert address == new_address
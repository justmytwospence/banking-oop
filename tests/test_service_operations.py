from banking.service_operations import open_checking
from banking.models import Account, Customer
from sqlalchemy import and_, select

from . import Session


def test_open_checking(Session):
    checking_id = open_checking.callback("Hilary Foobar", Session)
    assert checking_id

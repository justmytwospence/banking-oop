from banking.account_operations import open, add, get_customers
from banking.models import Account, Customer
from sqlalchemy import and_, select

from . import Session


def test_open(Session):
    name = "Spencer Foobar"
    new_account_id = open.callback(name, Session)
    with Session() as session:
        stmt = select(Account).where(Account.id == new_account_id)
        account = session.execute(stmt).scalar_one()
        assert name.split(" ")[0] in account.customers[0].firstname
        assert name.split(" ")[1] in account.customers[0].lastname


def test_add(Session):
    name = "Grace Foobar"
    new_account_id = add.callback("Garrett Foobar", name, Session)
    with Session() as session:
        stmt = select(Account).where(Account.id == new_account_id)
        account = session.execute(stmt).scalar_one()
        assert name.split(" ")[0] in [c.firstname for c in account.customers]
        assert name.split(" ")[1] in [c.lastname for c in account.customers]


def test_get_customers(Session):
    with Session() as session:
        account_id = session.execute(select(Account.id).limit(1)).scalar_one()
    customers = get_customers.callback(account_id, Session)
    assert customers

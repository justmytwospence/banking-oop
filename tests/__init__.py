import banking.models as models
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def seed_employees(Session):
    employees = [
        {"name": "Spencer Boucher", "address": "Nottingham Court", "salary": 150},
        {"name": "Hilary Boucher", "address": "Pond View Court", "salary": 100},
        {"name": "Greg Boucher", "address": "Pond view Court", "salary": 200},
        {"name": "Garrett Boucher", "address": "Nashville", "salary": 125},
    ]
    with Session() as session:
        for employee in employees:
            session.add(models.Employee(**employee))
        session.commit()


def seed_customer_accounts(Session):
    customers = [
        {"name": "Spencer Boucher", "address": "Nottingham Court"},
        {"name": "Hilary Boucher", "address": "Pond View Court"},
        {"name": "Garrett Boucher", "address": "Nashville"},
        {"name": "Grace Boucher", "address": "Nashville"},
    ]
    for customer in customers:
        with Session() as session:
            customer = models.Customer(**customer)
            session.add(customer)

            account = models.Account()
            session.add(account)
            account.customers.append(customer)
            session.commit()


@pytest.fixture()
def Session():
    # create mock database
    engine = create_engine(
        "postgresql+psycopg2://postgres@localhost:5432/banktesting")
    models.Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    # seed mock database with fake data
    seed_employees(Session)
    seed_customer_accounts(Session)

    # return Session handle to mock database
    yield Session

    # tear down database after tests
    models.Base.metadata.drop_all(engine)

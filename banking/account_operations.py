import logging

import click
from sqlalchemy import and_, select, update

from model import Account, Customer, Session

# logging
# INFO and above to file
# WARNING and above to console
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/bank.log")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s",
                                   datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
logger.addHandler(stream_handler)


@click.group(help="Account operations")
def account():
    pass


@account.command()
@click.option("--name",
              prompt="Customer name",
              help="The name of the customer for which to open an account")
def open(name):
    firstname, lastname = name.split(" ")
    with Session() as session:
        # get customer
        stmt = select(Customer).where(and_(
            Customer.firstname == firstname,
            Customer.lastname == lastname))
        customer = session.execute(stmt).scalar_one()

        # create new account
        new_account = Account()
        session.add(new_account)

        # link
        new_account.customers.append(customer)
        session.commit()


@account.command()
@click.option("--existing-account-customer", prompt="Name of current account holder")
@click.option("--new-account-customer", prompt="Name of new account holder")
def add(existing_account_customer, new_account_customer):
    with Session() as session:
        # get account
        firstname, lastname = existing_account_customer.split(" ")
        stmt = select(Account).join(Account.customers).where(and_(
            Customer.firstname == firstname,
            Customer.lastname == lastname
        ))
        account = session.execute(stmt).scalar_one()

        # get customer
        firstname, lastname = new_account_customer.split(" ")
        new_account_customer = session.execute(select(Customer).where(and_(
            Customer.firstname == firstname,
            Customer.lastname == lastname
        ))).scalar_one()

        # link
        account.customers.append(new_account_customer)
        session.commit()


@account.command()
@click.option("--uuid",
              prompt="Accout UUID",
              help="The name of the customer to add")
def get_customers(uuid):
    """Get the customers on an account"""
    with Session() as session:
        stmt = select(Account).where(Account.id == uuid)
        account = session.execute(stmt).scalar_one()
        logger.warning(account.customers)

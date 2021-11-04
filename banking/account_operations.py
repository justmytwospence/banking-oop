import logging

import click
import inquirer
from sqlalchemy import and_, select

from banking.models import Account, Customer, Session

logger = logging.getLogger(__name__)


@click.group(help="Account operations")
def account():
    pass


@account.command()
@click.option("--name",
              prompt="Customer name",
              help="The name of the customer for which to open an account")
def open(name):
    """Open a new account for a customer."""

    # get customer
    with Session() as session:
        firstname, lastname = name.split(" ")
        stmt = select(Customer).where(and_(
            Customer.firstname == firstname,
            Customer.lastname == lastname))
        logger.debug(f"Excecuting statement {stmt}")
        customer = session.execute(stmt).scalar_one()
        logger.info(f"Customer id is {customer.id}")

    # create new account
    with Session() as session:
        new_account = Account()
        session.add(new_account)
        session.commit()
        logger.info(f"New account's id is {new_account.id}")

        # link
        new_account.customers.append(customer)
        session.commit()


@account.command()
@click.option("--existing-account-customer", prompt="Name of current account holder")
@click.option("--new-account-customer", prompt="Name of new account holder")
def add(existing_account_customer, new_account_customer):
    """Add a second customer to the account of an existing customer."""

    # get account
    with Session() as session:
        firstname, lastname = existing_account_customer.split(" ")
        stmt = select(Account).join(Account.customers).where(and_(
            Customer.firstname == firstname,
            Customer.lastname == lastname
        ))
        accounts = session.execute(stmt)
        accounts = [inquirer.List('Account', message="Which account to use?",
                                  choices=[account[0] for account in accounts])]
        account = inquirer.prompt(accounts)['Account']

    # get customer
    with Session() as session:
        firstname, lastname = new_account_customer.split(" ")
        new_account_customer = session.execute(select(Customer).where(and_(
            Customer.firstname == firstname,
            Customer.lastname == lastname
        ))).scalar_one()
        logger.info("New account holder's id is {new_account_customer.id}")

        # link
        account.customers.append(new_account_customer)
        session.commit()


@account.command()
@click.option("--uuid",
              prompt="Accout UUID",
              help="The name of the customer to add")
def get_customers(uuid):
    """Get the customers on an account."""
    with Session() as session:
        stmt = select(Account).where(Account.id == uuid)
        logger.debug("Executing statement {stmt}")
        account = session.execute(stmt).scalar_one()
        click.echo([customer.firstname for customer in account.customers])

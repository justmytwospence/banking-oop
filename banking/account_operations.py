import logging

import click
import inquirer
from sqlalchemy import and_, exc, select

from banking.models import Account, Customer, Session
from banking.utils import split_name

logger = logging.getLogger(__name__)


@click.group(help="Account operations")
def account():
    pass


@account.command()
@click.option("--name",
              prompt="Customer name",
              help="The name of the customer for which to open an account")
def open(name, Session=Session):
    """Open a new account for a customer."""

    firstname, lastname = split_name(name)

    with Session() as session:
        # get customer
        stmt = select(Customer).where(and_(
            Customer.firstname == firstname,
            Customer.lastname == lastname))
        logger.debug(f"Excecuting statement {stmt}")
        customer = session.execute(stmt).scalar_one()
        logger.info(f"Customer id is {customer.id}")

        # create new account
        new_account = Account()
        session.add(new_account)
        session.commit()
        logger.info(f"New account's id is {new_account.id}")

        # link
        new_account.customers.append(customer)
        session.commit()

        return new_account.id


@account.command()
@click.option("--existing-account-customer", prompt="Name of current account holder")
@click.option("--new-account-customer", prompt="Name of new account holder")
def add(existing_account_customer, new_account_customer, Session):
    """Add a second customer to the account of an existing customer."""

    with Session() as session:
        # get existing account
        firstname, lastname = split_name(existing_account_customer)
        stmt = select(Account).join(Account.customers).where(and_(
            Customer.firstname == firstname,
            Customer.lastname == lastname
        ))
        accounts = session.execute(stmt).fetchall()
        if len(accounts) < 1:
            raise Exception(
                f"Customer {existing_account_customer} has no existing accounts.")
        elif len(accounts) == 1:
            account = accounts[0][0]
        else:
            accounts = [inquirer.List('Account', message="Which account to use?",
                                      choices=[account[0] for account in accounts])]
            account = inquirer.prompt(accounts)['Account']

        # get customer
        try:
            firstname, lastname = split_name(new_account_customer)
            new_account_customer = session.execute(select(Customer).where(and_(
                Customer.firstname == firstname,
                Customer.lastname == lastname
            ))).scalar_one()
            logger.info(
                f"New account holder's id is {new_account_customer.id}")
        except exc.SQLAlchemyError as e:
            logger.error(f"Failed to get customer {new_account_customer}: {e}")

        # link
        account.customers.append(new_account_customer)
        session.commit()

        return account.id


@account.command()
@click.option("--uuid",
              prompt="Accout UUID",
              help="The UUID of the account for which to get customers")
def get_customers(uuid, Session=Session):
    """Get the customers on an account."""

    with Session() as session:
        stmt = select(Account).where(Account.id == uuid)
        logger.debug("Executing statement {stmt}")
        account = session.execute(stmt).scalar_one()
        if len(account.customers) < 1:
            logger.warn(f"Account {uuid} has no associated customers.")
        click.echo([customer.firstname for customer in account.customers])
    return account.customers

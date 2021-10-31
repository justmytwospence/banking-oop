import click
import inquirer
from sqlalchemy import and_, select, update

from logging_utils import get_logger
from models import Account, Checking, Customer, Session

logger = get_logger()


@click.group(help="Account operations")
def checking():
    pass


@checking.command()
@click.argument("name")
def open(name):
    """Open checking account for customer"""
    firstname, lastname = name.split(" ")
    with Session() as session:
        stmt = select(Account).join(Account.customers)
        stmt = stmt.where(and_(
            Customer.firstname == firstname,
            Customer.lastname == lastname
        ))
        accounts = session.execute(stmt)
        accounts = [
          inquirer.List('Account',
                        message="Which account to use?",
                        choices=[account[0].id for account in accounts])]
        account_id = inquirer.prompt(accounts)

    new_checking = Checking(account_id=account_id)
    with Session() as session:
        session.add(new_checking)
        session.commit()


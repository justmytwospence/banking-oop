import logging

import click
import inquirer
from sqlalchemy import and_, select, update

from banking.models import Account, Checking, Customer, Session
from banking.utils import split_name

logger = logging.getLogger(__name__)


@click.group(help="Account operations")
def checking():
    pass


@checking.command()
@click.argument("name")
def open(name):
    """Open checking account for customer"""

    firstname, lastname = split_name(name)

    # get account
    try:
        with Session() as session:
            stmt = select(Account).join(Account.customers)
            stmt = stmt.where(and_(
                Customer.firstname == firstname,
                Customer.lastname == lastname
            ))
            logger.debug(f"Executing statement {stmt}")
            accounts = session.execute(stmt)
            accounts = [inquirer.List('Account', message="Which account to use?",
                                      choices=[account[0].id for account in accounts])]
            account_id = inquirer.prompt(accounts)['Account']
            logger.info(f"Using account_id {account_id}")
    except:
        logger.error(f"No existing accounts found for {name}.")

    # create checking
    try:
        with Session() as session:
            new_checking = Checking(account_id=account_id)
            session.add(new_checking)
            session.commit()
            logger.info(f"New checking account id is {new_checking.id}")
    except Exception as e:
        logger.error(
            f"Failed to create checking account for account {account_id}: {e}")

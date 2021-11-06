import logging

import click
import inquirer
from sqlalchemy import and_, select, update

from banking.models import Account, Checking, Customer, Session
from banking.utils import split_name

logger = logging.getLogger(__name__)


@click.group(help="Account operations")
def service():
    pass


@service.command()
@click.argument("name")
def open_checking(name, Session=Session):
    """Open checking account for customer"""

    firstname, lastname = split_name(name)

    # get account
    with Session() as session:
        stmt = select(Account).join(Account.customers)
        stmt = stmt.where(and_(
            Customer.firstname == firstname,
            Customer.lastname == lastname
        ))
        logger.debug(f"Executing statement {stmt}")
        accounts = session.execute(stmt).fetchall()

        if len(accounts) < 1:
            raise Exception(f"No accounts found")
        elif len(accounts) == 1:
            account_id = accounts[0][0].id
        else:
            accounts = [inquirer.List('Account', message="Which account to use?",
                                      choices=[account[0].id for account in accounts])]
            account_id = inquirer.prompt(accounts)['Account']
        logger.info(f"Using account_id {account_id}")

    # create checking
    try:
        with Session() as session:
            new_checking = Checking(account_id=account_id)
            session.add(new_checking)
            session.commit()
            logger.info(f"New checking account id is {new_checking.id}")
            return new_checking.id
    except Exception as e:
        logger.error(
            f"Failed to create checking account for account {account_id}: {e}")
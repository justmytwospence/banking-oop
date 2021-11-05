import logging

import click
from sqlalchemy import update, and_

from banking.models import Customer, Session

logger = logging.getLogger(__name__)


@click.group(help="Customer operations")
def customer():
    pass


@customer.command()
@click.option("--name", prompt="Customer name",
              help="The name of the customer to add")
@click.option("--address", prompt="Customer address",
              help="The address of the customer to add")
def onboard(name, address, Session=Session):
    """Add a customer."""

    with Session() as session:
        new_customer = Customer(name, address)
        logger.info(f"Adding new customer {new_customer}")
        session.add(new_customer)
        session.commit()
        logger.info(f"New customer id is {new_customer.id}")


@customer.command()
@click.option("--name", prompt="Customer name",
              help="The name of the customer to add")
@click.option("--address", prompt="Customer address",
              help="The address of the customer to add")
def change_address(name, address, Session):
    """Change a customer's address"""

    with Session() as session:
        firstname, lastname = name.split(" ")
        stmt = (
            update(Customer)
            .where(and_(
                Customer.firstname == firstname,
                Customer.lastname == lastname))
            .values(address=address))
        logger.debug(f"Executing statement {stmt}")
        session.execute(stmt)
        session.commit()

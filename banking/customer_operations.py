import logging

import click

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
def onboard(name, address):
    """Add a customer."""

    new_customer = Customer(name, address)
    logger.info(f"Adding new customer {new_customer}")
    with Session() as session:
        session.add(new_customer)
        session.commit()
        logger.info(f"New customer id is {new_customer.id}")

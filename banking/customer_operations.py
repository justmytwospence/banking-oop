import logging

import click

from logging_utils import get_logger
from models import Customer, Session

logger = get_logger()


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
        logger.info("Committing new customer...")
        session.commit()

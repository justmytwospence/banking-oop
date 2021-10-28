import logging

import click

from model import Account, Customer, Employee, Session

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


@click.command()
@click.option("--name", prompt="Customer name",
              help="The name of the customer to add")
@click.option("--address", prompt="Customer address",
              help="The address of the customer to add")
def add_customer(**kwargs):
    """Add a customer."""
    new_customer = Customer(**kwargs)
    logger.info(f"Adding new customer {new_customer}")
    with Session() as session:
        session.add(new_customer)
        logger.info("Committing new customer...")
        session.commit()


@click.group(help="Customer operations")
def customer():
    pass


customer.add_command(add_customer)

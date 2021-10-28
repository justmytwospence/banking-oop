import logging

import click

from customer_operations import customer
from employee_operations import employee

@click.group(help="CLI tool to manage your bank")
def cli():
    pass


cli.add_command(customer)
cli.add_command(employee)

if __name__ == "__main__":
    cli()

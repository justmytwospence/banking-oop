import click

from banking.account_operations import account
from banking.customer_operations import customer
from banking.employee_operations import employee
from banking.service_operations import checking


@click.group(help="CLI tool to manage your bank")
def cli():
    pass


cli.add_command(account)
cli.add_command(customer)
cli.add_command(employee)
cli.add_command(checking)

cli()

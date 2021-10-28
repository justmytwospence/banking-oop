import logging

import click
from sqlalchemy import and_, select, update

from model import Account, Customer, Employee, Session

# logging
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


@click.command()
@click.option("--name", prompt="Employee name",
              help="The name of the customer to add")
@click.option("--address", prompt="Employee address",
              help="The address of the employee")
@click.option("--salary", prompt="Employee salary",
              help="The salary of the employee")
@click.option("--manager", prompt="Manager id",
              help="The id of the employees manager")
@click.option("--is_active", default=True,
              prompt="Is the employee active (True/False)",
              help="Whether the employee is active.")
def add_employee(**kwargs):
    """Add an employee to the bank."""
    with Session() as session:
        new_employee = Employee(**kwargs)
        logger.info(f"Adding new employee {new_employee} to session")
        session.add(new_employee)
        logger.info("Committing new employee...")
        session.commit()


@click.command()
@click.option("--name",
              prompt="Employee name",
              help="The name of the employee")
def get_employee_salary(name):
    logger.info(f"Getting salary of employee {name}")
    names = name.split(" ")
    firstname, lastname = names[0], names[1]
    stmt = select(Employee).where(Employee.firstname == firstname)
    logger.info(f"Executing statement: {stmt}")
    with Session() as session:
        result = session.execute(stmt).scalar_one()
    click.echo(f"{name}'s salary is ${result.salary:0,.2f}")


@click.command()
@click.option("--name",
              prompt="Employee name",
              help="The name of the employee")
@click.option("--new-salary",
              prompt="New salary",
              help="The new salary of the employee")
def change_employee_salary(name, new_salary):
    logger.info(f"Changing salary of employee {name}")
    names = name.split(" ")
    firstname, lastname = names[0], names[1]
    stmt = update(Employee).where(Employee.firstname == firstname)
    stmt = stmt.values(salary=new_salary)
    logger.info(f"Executing statement: {stmt}")
    with Session() as session:
        session.execute(stmt)
        session.commit()


@click.command()
@click.option("--name",
              prompt="Employee name",
              help="The name of the employee to terminate")
def terminate_employee(name):
    logger.info(f"Terminating employee {name}")
    names = name.split(" ")
    firstname, lastname = names[0], names[1]
    stmt = update(Employee).where(and_(
        Employee.firstname == firstname,
        Employee.lastname == lastname))
    stmt = stmt.values(is_active=False)
    with Session() as session:
        session.execute(stmt)
        session.commit()


@click.group(help="CLI tool to manage manage your bank")
def cli():
    pass


cli.add_command(add_employee)
cli.add_command(add_customer)
cli.add_command(get_employee_salary)
cli.add_command(change_employee_salary)
cli.add_command(terminate_employee)

if __name__ == "__main__":
    cli()

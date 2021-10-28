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
@click.option("--name", prompt="Employee name",
              help="The name of the customer to add")
@click.option("--address", prompt="Employee address",
              help="The address of the employee")
@click.option("--salary", prompt="Employee salary",
              help="The salary of the employee")
@click.option("--manager-id", default="",
              prompt="Manager id",
              help="The id of the employees manager")
@click.option("--is_active", default=True,
              prompt="Is the employee active (True/False)",
              help="Whether the employee is active.")
def hire(**kwargs):
    """Add an employee to the bank."""
    with Session() as session:
        if kwargs["manager_id"] == "":
            kwargs["manager_id"] = None
        new_employee = Employee(**kwargs)
        logger.info(f"Adding new employee {new_employee} to session")
        session.add(new_employee)
        logger.info("Committing new employee...")
        session.commit()


@click.command()
@click.option("--name",
              prompt="Employee name",
              help="The name of the employee")
def get_salary(name):
    logger.info(f"Getting salary of employee {name}")
    names = name.split(" ")
    firstname, lastname = names[0], names[1]
    stmt = select(Employee).where(and_(
        Employee.firstname == firstname,
        Employee.lastname == lastname))
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
def change_salary(name, new_salary):
    logger.info(f"Changing salary of employee {name}")
    names = name.split(" ")
    firstname, lastname = names[0], names[1]
    stmt = update(Employee).where(and_(
        Employee.firstname == firstname,
        Employee.lastname == lastname))
    stmt = stmt.values(salary=new_salary)
    logger.info(f"Executing statement: {stmt}")
    with Session() as session:
        session.execute(stmt)
        session.commit()


@click.command()
@click.option("--name",
              prompt="Employee name",
              help="The name of the employee to terminate")
def terminate(name):
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


@click.command()
@click.option("--name",
              prompt="Manager name",
              help="The name of the manager of which to get reports")
def get_manager_reports(name):
    logger.info(f"Getting reports for {name}")
    names = name.split(" ")
    firstname, lastname = names[0], names[1]
    stmt = select(Employee).where(and_(
        Employee.firstname == firstname,
        Employee.lastname == lastname
    ))
    with Session() as session:
        manager = session.execute(stmt).scalar_one()
        click.echo(f"{name}'s reports are {Employee.reports}")


@click.group(help="Employee operations")
def employee():
    pass


employee.add_command(change_salary)
employee.add_command(get_manager_reports)
employee.add_command(get_salary)
employee.add_command(hire)
employee.add_command(terminate)

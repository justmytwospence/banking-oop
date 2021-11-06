import logging

import click
from sqlalchemy import and_, select, update

from banking.models import Employee, Session

logger = logging.getLogger(__name__)


@click.group(help="Employee operations")
def employee():
    pass


@employee.command()
@click.option("--name", prompt="Employee name",
              help="The name of the customer to add")
@click.option("--address", prompt="Employee address",
              help="The address of the employee")
@click.option("--salary", prompt="Employee salary",
              help="The salary of the employee")
@click.option("--manager", default="",
              prompt="Manager",
              help="The id of the employees manager")
@click.option("--is_active", is_flag=True, default=True,
              prompt="Is the employee active?")
def hire(name, address, salary, manager, is_active, Session=Session):
    """Add an employee to the bank."""

    if manager:
        with Session() as session:
            firstname, lastname = manager.split(" ")
            stmt = select(Employee).where(and_(
                Employee.firstname == firstname,
                Employee.lastname == lastname))
            logger.debug(f"Executing statement: {stmt}")
            manager = session.execute(stmt).scalar_one()
    manager_id = manager.id if manager else None
    logger.info(f"New hire's manager_id is {manager_id}")

    with Session() as session:
        new_employee = Employee(name, address, salary, manager_id, is_active)
        logger.debug(f"Adding new employee {new_employee}")
        session.add(new_employee)
        session.commit()
        logger.info(f"New hire's id is {new_employee.id}")

    return new_employee


@employee.command()
@click.option("--name",
              prompt="Employee name",
              help="The name of the employee")
def get_salary(name):
    """Get the salary of an employee by employee name."""

    names = name.split(" ")
    firstname, lastname = names[0], names[1]
    stmt = select(Employee).where(and_(
        Employee.firstname == firstname,
        Employee.lastname == lastname))

    logger.debug(f"Executing statement: {stmt}")
    with Session() as session:
        result = session.execute(stmt).scalar_one()
    logger.info(f"{name}'s employee_id is {result.id}")
    click.echo(f"{name}'s salary is ${result.salary:0,.2f}")
    return result.salary


@employee.command()
@click.option("--name",
              prompt="Employee name",
              help="The name of the employee")
@click.option("--new-salary",
              prompt="New salary",
              help="The new salary of the employee")
def change_salary(name, new_salary):
    """Change the salary of an employee"""

    names = name.split(" ")
    firstname, lastname = names[0], names[1]
    stmt = update(Employee).where(and_(
        Employee.firstname == firstname,
        Employee.lastname == lastname))
    stmt = stmt.values(salary=new_salary)

    logger.debug(f"Executing statement: {stmt}")
    with Session() as session:
        session.execute(stmt)
        session.commit()
    logger.info(f"Changed {name}'s salary to ${int(new_salary):0,.2f}")


@employee.command()
@click.option("--name",
              prompt="Employee name",
              help="The name of the employee to terminate")
def terminate(name):
    """Terminate an employee"""
    names = name.split(" ")
    firstname, lastname = names[0], names[1]
    stmt = update(Employee).where(and_(
        Employee.firstname == firstname,
        Employee.lastname == lastname))
    stmt = stmt.values(is_active=False)

    logger.debug(f"Executing statement: {stmt}")
    with Session() as session:
        session.execute(stmt)
        session.commit()


@employee.command()
@click.option("--name",
              prompt="Manager name",
              help="The name of the manager of which to get reports")
def get_manager_reports(name):
    """Get the employees that report to a manager."""

    names = name.split(" ")
    firstname, lastname = names[0], names[1]
    stmt = select(Employee).where(and_(
        Employee.firstname == firstname,
        Employee.lastname == lastname
    ))
    with Session() as session:
        logger.debug(f"Executing statement: {stmt}")
        manager = session.execute(stmt).scalar_one()
        logger.info(f"{name}'s id is {manager.id}")
        click.echo(f"{name}'s reports are {manager.reports}")
        logger.info(
            f"The ids of {name}'s reports are {[report.id for report in manager.reports]}")

import logging

import click
from sqlalchemy import and_, select, update

from models import Employee, Session
from logging_utils import get_logger

logger = get_logger()


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
def hire(name, address, salary, manager, is_active):
    """Add an employee to the bank."""
    firstname, lastname = manager.split(" ")
    with Session() as session:
        stmt = select(Employee).where(and_(
            Employee.firstname == firstname,
            Employee.lastname == lastname))
        manager = session.execute(stmt).scalar_one()
        new_employee = Employee(name, address, salary, manager.id, is_active)
        logger.info(f"Adding new employee {new_employee} to session")
        session.add(new_employee)
        logger.info("Committing new employee...")
        session.commit()


@employee.command()
@click.option("--name",
              prompt="Employee name",
              help="The name of the employee")
def get_salary(name):
    """Get the salary of an employee by employee name."""
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


@employee.command()
@click.option("--name",
              prompt="Employee name",
              help="The name of the employee")
@click.option("--new-salary",
              prompt="New salary",
              help="The new salary of the employee")
def change_salary(name, new_salary):
    """Change the salary of an employee"""
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


@employee.command()
@click.option("--name",
              prompt="Employee name",
              help="The name of the employee to terminate")
def terminate(name):
    """Terminate an employee"""
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


@employee.command()
@click.option("--name",
              prompt="Manager name",
              help="The name of the manager of which to get reports")
def get_manager_reports(name):
    """Get the employees that report to a manager."""
    logger.info(f"Getting reports for {name}")
    names = name.split(" ")
    firstname, lastname = names[0], names[1]
    stmt = select(Employee).where(and_(
        Employee.firstname == firstname,
        Employee.lastname == lastname
    ))
    with Session() as session:
        manager = session.execute(stmt).scalar_one()
        click.echo(f"{name}'s reports are {manager.reports}")

import logging
from datetime import datetime

import click
from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, create_engine, select)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

logging.basicConfig(filename='logs/bank.log', level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())

engine = create_engine("sqlite:///bank.db")
Base = declarative_base()


class Account(Base):
    __tablename__ = "Account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("Customer.id"))
    balance = Column(Float, default=0)

    def __init__(self, customer_ids):
        self.customer_idi


class Customer(Base):
    __tablename__ = "Customer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    account_id = Column(Integer, ForeignKey("Account.id"))

    def __init__(self, name, address):
        names = name.split(" ")
        if len(names) <= 2:
            self.firstname, self.lastname = names[0], names[1]
        else:
            raise Exception("Only first and last name supported")
        self.address = address


class Employee(Base):
    __tablename__ = "Employee"

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    salary = Column(Integer)
    manager_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    def __init__(self, name, address, salary, manager=None, is_active=True):
        names = name.split(" ")
        if len(names) == 2:
            self.firstname, self.lastname = names[0], names[1]
        else:
            raise Exception("Only single first and last name supported")
        self.address = address
        self.salary = salary
        self.manager = manager
        self.is_active = True

    def __repr__(self):
        return f"Employee(firstname={self.firstname}, lastname={self.lastname})"


Base.metadata.create_all(engine)  # create tables from classes


@click.command()
@click.option("--name", prompt="Customer name",
              help="The name of the customer to add")
@click.option("--address", prompt="Customer address",
              help="The address of the customer to add")
def add_customer(**kwargs):
    """Add a customer."""
    new_customer = Customer(**kwargs)
    with Session(engine) as session:
        session.add(new_customer)
        session.commit()


@click.command()
@click.option("--name", default="Spencer Boucher",
              prompt="Employee name",
              help="The name of the customer to add")
@click.option("--address", default="409 Pond View Court",
              prompt="Employee address",
              help="The address of the employee")
@click.option("--salary", default=100000,
              prompt="Employee salary",
              help="The salary of the employee")
@click.option("--manager", default=0,
              prompt="Manager id",
              help="The id of the employees manager")
@click.option("--is_active", default=True,
              prompt="Is the employee active (True/False)",
              help="Whether the employee is active.")
def add_employee(**kwargs):
    """Add an employee."""
    new_employee = Employee(**kwargs)
    print(new_employee)

    with Session(engine) as session:
        session.add(new_employee)
        logger.info("Comitting...")
        session.commit()


@click.command()
@click.option("--name")
def get_employee_salary(**kwargs):
    stmt = select([])


if __name__ == '__main__':
    add_employee()

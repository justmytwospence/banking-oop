import logging
from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, Table, create_engine, select, update)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs/bank.log")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                   datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)
logger.addHandler(stream_handler)

Base = declarative_base()

# Many to many relationship between Account and Customer
account_customer = Table("account_customer", Base.metadata,
                         Column("account_id", Integer(),
                                ForeignKey("Account.id")),
                         Column('customer_id',
                                Integer(), ForeignKey("Customer.id")))


class Account(Base):
    __tablename__ = "Account"

    # fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("Customer.id"))
    balance = Column(Float, default=0)

    def __init__(self, customer_ids):
        pass


class Customer(Base):
    __tablename__ = "Customer"

    # fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("Account.id"))
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)

    # relationships
    account = relationship("Account", secondary=account_customer)

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
    manager_id = Column(Integer, ForeignKey("Employee.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    salary = Column(Integer)
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


logger.info("Creating tables from classes")
engine = create_engine("sqlite:///bank.db")
Base.metadata.create_all(engine)
Session = sessionmaker(engine)

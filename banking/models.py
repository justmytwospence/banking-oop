import logging
import uuid
from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, Table, create_engine)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker

from logging_utils import get_logger

logger = get_logger()

Base = declarative_base()


class Account(Base):
    __tablename__ = "Account"

    # fields
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    balance = Column(Float, default=0)

    # relationships
    customers = relationship("Customer",
                             secondary="AccountCustomer",
                             back_populates="accounts")

    def __repr__(self):
        return f"Account(id={self.id})"


class Customer(Base):
    __tablename__ = "Customer"

    # fields
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)

    # relationships
    accounts = relationship("Account",
                            secondary="AccountCustomer",
                            back_populates="customers")

    def __init__(self, name, address):
        names = name.split(" ")
        if len(names) <= 2:
            self.firstname, self.lastname = names[0], names[1]
        else:
            raise Exception("Only first and last name supported")
        self.address = address


class AccountCustomer(Base):
    __tablename__ = "AccountCustomer"

    # fields
    account_id = Column(UUID(as_uuid=True),
                        ForeignKey("Account.id"),
                        primary_key=True)
    customer_id = Column(UUID(as_uuid=True),
                         ForeignKey("Customer.id"),
                         primary_key=True)


class Checking(Base):
    __tablename__ = "Checking"

    # fields
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("Account.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    balance = Column(Float, default=0)


class Saving(Base):
    __tablename__ = "Saving"

    # fields
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("Account.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    balance = Column(Float, default=0)


class Loan(Base):
    __tablename__ = "Loan"

    # fields
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("Account.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    balance = Column(Float, default=0)


class Credit(Base):
    __tablename__ = "Credit"

    # fields
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    account_id = Column(UUID(as_uuid=True), ForeignKey("Account.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    balance = Column(Float, default=0)


class Employee(Base):
    __tablename__ = "Employee"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    manager_id = Column(UUID(as_uuid=True),
                        ForeignKey("Employee.id"),
                        nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    firstname = Column(String)
    lastname = Column(String)
    address = Column(String)
    salary = Column(Integer)
    is_active = Column(Boolean, default=True)

    manager = relationship("Employee",
                           backref=backref('reports'),
                           remote_side=[id])

    def __init__(self, name, address, salary, manager_id=None, is_active=True):
        names = name.split(" ")
        if len(names) == 2:
            self.firstname, self.lastname = names[0], names[1]
        else:
            raise Exception("Only single first and last name supported")
        self.address = address
        self.salary = salary
        self.manager_id = manager_id
        self.is_active = is_active

    def __repr__(self):
        return f"Employee(firstname={self.firstname}, lastname={self.lastname})"


engine = create_engine(f"postgresql+psycopg2://postgres@localhost:5432/bank")
Session = sessionmaker(engine)
Base.metadata.create_all(engine)
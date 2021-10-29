A mock banking app.

## TODO

- [ ] Data model
- [ ] Functionality
- [ ] Organize
- [ ] Logging
- [ ] Documentation
- [ ] Testing

## Technologies

- [Python 3](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/) for data persistence
- [Click](https://click.palletsprojects.com/en/8.0.x/) for the command line interface
- [SQLAlchemy](https://www.sqlalchemy.org/) for object-relational mapping
- [pytest](https://docs.pytest.org/en/6.2.x/) for testing

## Data model

`Employee.manager_id` is a self-referential foreign key to `Employee.id`, to
model the relationship between managers and reports.

Because customers and accounts have a many to many relationship, they are
modeled with a join table `AccountCustomer`.

![ERD](images/erd.png)
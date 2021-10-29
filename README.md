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

### Customer

| field      | type    |
|------------|---------|
| id         | id      |
| first name | varchar |
| last name  | varchar |
| address    | varchar |

### Account

| field | type |
|-------|------|
| id    | id   |

### Employee

| field      | type    |
|------------|---------|
| id         | id      |
| first name | varchar |
| last name  | varchar |
| salary     | float   |
| manager    | id      |

### Checking

| field   | type |
|---------|------|
| id      | id   |
| account | id   |

### Saving

| field   | type |
|---------|------|
| id      | id   |
| account | id   |

### Loan

| field   | type  |
|---------|-------|
| id      | id    |
| account | id    |
| balance | float |
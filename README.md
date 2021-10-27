A mock banking app.

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

| field    | type |
|----------|------|
| id       | id   |
| account  | id   |

### Saving

| field    | type |
|----------|------|
| id       | id   |
| account  | id   |

### Loan

| field    | type  |
|----------|-------|
| id       | id    |
| account  | id    |
| balance  | float |
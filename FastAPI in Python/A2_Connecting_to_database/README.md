# Task API

A simple RESTful Task API built with **FastAPI**, **SQLModel**, and **SQLite**. The API supports creating, reading, updating, and deleting tasks (CRUD).

## Features

* Create a task
* View all tasks
* View a task by ID
* Update a task
* Delete a task
* Automatic database creation on startup

## Technologies Used

* Python 3.x
* FastAPI
* SQLModel
* SQLite
* Uvicorn

## Why SQLite?

SQLite was chosen because it is lightweight, serverless, and requires no installation or configuration. It stores all data in a single file, making it ideal for small projects, learning SQLModel, and local development.

## Database Location

The database is stored in the project directory as:

```text
tasks.db
```

The file is created automatically the first time the application starts.

## Project Structure

```text
.
├── main.py
├── tasks.db          # Created automatically
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://www.Backend-AI-Engineering/FastAPI in Python/A2_Connecting_to_database
cd <repository-folder>
```

Create a virtual environment (optional but recommended):

```bash
pipenv install
```

Activate it.

Windows:

```bash
pipenv shell
```

Linux/macOS:

```bash
pipenv shell
```

Install dependencies:

```bash
pipenv install -r requirements.txt
```

## Running the Project

Start the FastAPI server:

```bash
fastapi dev main.py
```

or

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Automatic Database Creation

No manual setup is required.

When the application starts, it automatically:

* Creates the SQLite database (`tasks.db`) if it does not exist.
* Creates the required tables.
* Inserts sample tasks if the database is empty.

## Example SQL Query

Example query executed in the SQLite database:

```sql
SELECT * FROM tasks;
```

Example result:

| id | title       | done |
| -- | ----------- | ---- |
| 1  | Wake Up     | 1    |
| 2  | Brush Teeth | 1    |
| 3  | Take Bath   | 0    |

## Database Screenshot

Insert a screenshot of your SQLite database viewer here.

Example:

```text
docs/database-viewer.png
```

Markdown:

```markdown
![SQLite Database](docs/database-viewer.png)
```

## API Endpoints

| Method | Endpoint      | Description      |
| ------ | ------------- | ---------------- |
| GET    | `/`           | API information  |
| GET    | `/tasks`      | Get all tasks    |
| GET    | `/tasks/{id}` | Get a task by ID |
| POST   | `/tasks`      | Create a task    |
| PUT    | `/tasks/{id}` | Update a task    |
| DELETE | `/tasks/{id}` | Delete a task    |

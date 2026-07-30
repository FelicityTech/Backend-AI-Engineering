from sqlmodel import Session, select

from .models import Task


class PostgresTaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.exec(select(Task)).all()

    def get_by_id(self, task_id: int):
        return self.session.get(Task, task_id)

    def create(self, title: str):
        task = Task(title=title, done=False)

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    def update(self, task_id: int, title: str):
        task = self.get_by_id(task_id)

        if task is None:
            return None

        task.title = title

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    def delete(self, task_id: int):
        task = self.get_by_id(task_id)

        if task is None:
            return False

        self.session.delete(task)
        self.session.commit()

        return True

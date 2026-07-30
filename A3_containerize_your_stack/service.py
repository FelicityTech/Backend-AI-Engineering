from .repository import PostgresTaskRepository


class TaskService:

    def __init__(self, repository: PostgresTaskRepository):
        self.repository = repository

    def get_tasks(self):
        return self.repository.get_all()

    def get_task(self, task_id):
        return self.repository.get_by_id(task_id)

    def create_task(self, title):
        return self.repository.create(title)

    def update_task(self, task_id, title):
        return self.repository.update(task_id, title)

    def delete_task(self, task_id):
        return self.repository.delete(task_id)

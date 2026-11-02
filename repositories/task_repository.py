
import sqlite3

from models.task_item import TaskItem


class TaskRepository:
    """
    Görevlerin veritabanı işlemlerini yöneten sınıf.
    """

    def __init__(self, database_helper):
        self.database_helper = database_helper

    # CREATE - Yeni görev ekleme
    def create_task(self, task: TaskItem):
        connection = self.database_helper.get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO tasks (
                    user_id,
                    title,
                    description,
                    priority,
                    status,
                    due_date
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    task.user_id,
                    task.title,
                    task.description,
                    task.priority,
                    task.status,
                    task.due_date
                )
            )

            connection.commit()

            return cursor.lastrowid

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()



    # READ - Arama ve filtreleme destekli görev listeleme
    def get_all_tasks(
        self,
        user_id: int,
        search_text: str = "",
        status: str = None,
        priority: str = None
    ):
        connection = self.database_helper.get_connection()

        try:
            # Temel sorgu: Sadece giriş yapan kullanıcının görevleri
            query = """
                SELECT * FROM tasks
                WHERE user_id = ?
            """

            parameters = [user_id]

            # Başlığa göre arama
            if search_text:
                query += " AND title LIKE ?"
                parameters.append(f"%{search_text.strip()}%")

            # Duruma göre filtreleme
            if status:
                query += " AND status = ?"
                parameters.append(status)

            # Önceliğe göre filtreleme
            if priority:
                query += " AND priority = ?"
                parameters.append(priority)

            # Görevleri sıralama
            query += " ORDER BY due_date ASC, id DESC"

            rows = connection.execute(
                query,
                parameters
            ).fetchall()

            tasks = []

            for row in rows:
                task = TaskItem(
                    task_id=row["id"],
                    user_id=row["user_id"],
                    title=row["title"],
                    description=row["description"],
                    priority=row["priority"],
                    status=row["status"],
                    due_date=row["due_date"],
                    created_at=row["created_at"]
                )

                tasks.append(task)

            return tasks

        finally:
            connection.close()


    # UPDATE - Görev güncelleme
    def update_task(self, task: TaskItem):
        connection = self.database_helper.get_connection()

        try:
            cursor = connection.execute(
                """
                UPDATE tasks
                SET
                    title = ?,
                    description = ?,
                    priority = ?,
                    status = ?,
                    due_date = ?
                WHERE id = ? AND user_id = ?
                """,
                (
                    task.title,
                    task.description,
                    task.priority,
                    task.status,
                    task.due_date,
                    task.id,
                    task.user_id
                )
            )

            connection.commit()

            return cursor.rowcount > 0

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()

    # DELETE - Görev silme
    def delete_task(self, task_id: int, user_id: int):
        connection = self.database_helper.get_connection()

        try:
            cursor = connection.execute(
                """
                DELETE FROM tasks
                WHERE id = ? AND user_id = ?
                """,
                (task_id, user_id)
            )

            connection.commit()

            return cursor.rowcount > 0

        except sqlite3.Error:
            connection.rollback()
            raise

        finally:
            connection.close()


from models.task_item import TaskItem


class TaskService:
    """
    Görev yönetimi işlemlerinin iş kurallarını yöneten sınıf.
    """

    def __init__(self, task_repository):
        self.task_repository = task_repository

    @staticmethod
    def validate_user_id(user_id):
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Geçerli bir kullanıcı bulunamadı.")

    # CREATE
    def add_task(
        self,
        user_id: int,
        title: str,
        description: str,
        priority: str,
        status: str,
        due_date: str
    ):
        self.validate_user_id(user_id)

        # TaskItem nesnesi oluşturulur.
        # Model içerisindeki kontroller otomatik çalışır.
        task = TaskItem(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            status=status,
            due_date=due_date
        )

        # Veritabanına kaydet
        task_id = self.task_repository.create_task(task)

        # Kaydedilen görevi ID bilgisiyle geri döndür
        return TaskItem(
            task_id=task_id,
            user_id=user_id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            status=task.status,
            due_date=task.due_date
        )



    # READ - Görevleri arama ve filtreleme
    def get_user_tasks(
        self,
        user_id: int,
        search_text: str = "",
        status: str = None,
        priority: str = None
    ):
        self.validate_user_id(user_id)

        # Arama metnini temizle
        search_text = search_text.strip() if search_text else ""

        # Durum kontrolü
        if status is not None and status not in TaskItem.VALID_STATUSES:
            raise ValueError("Geçersiz görev durumu.")

        # Öncelik kontrolü
        if priority is not None and priority not in TaskItem.VALID_PRIORITIES:
            raise ValueError("Geçersiz öncelik seviyesi.")

        return self.task_repository.get_all_tasks(
            user_id=user_id,
            search_text=search_text,
            status=status,
            priority=priority
        )


    # UPDATE
    def update_task(
        self,
        task_id: int,
        user_id: int,
        title: str,
        description: str,
        priority: str,
        status: str,
        due_date: str
    ):
        self.validate_user_id(user_id)

        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Geçersiz görev ID.")

        task = TaskItem(
            task_id=task_id,
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            status=status,
            due_date=due_date
        )

        success = self.task_repository.update_task(task)

        if not success:
            raise ValueError(
                "Görev bulunamadı veya bu görev size ait değil."
            )

        return task

    # DELETE
    def delete_task(self, task_id: int, user_id: int):
        self.validate_user_id(user_id)

        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Geçersiz görev ID.")

        success = self.task_repository.delete_task(
            task_id,
            user_id
        )

        if not success:
            raise ValueError(
                "Görev bulunamadı veya bu görev size ait değil."
            )

        return True

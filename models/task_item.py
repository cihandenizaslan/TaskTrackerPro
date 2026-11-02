
from datetime import datetime


class TaskItem:
    """
    Sistemdeki görevleri temsil eden sınıf.
    """

    VALID_PRIORITIES = ["Düşük", "Orta", "Yüksek"]

    VALID_STATUSES = [
        "Bekliyor",
        "Devam Ediyor",
        "Tamamlandı"
    ]

    def __init__(
        self,
        user_id: int,
        title: str,
        due_date: str,
        description: str = "",
        priority: str = "Orta",
        status: str = "Bekliyor",
        task_id: int = None,
        created_at: str = None
    ):
        self.__id = task_id
        self.__user_id = user_id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.__created_at = created_at

    # Görev ID
    @property
    def id(self):
        return self.__id

    # Kullanıcı ID
    @property
    def user_id(self):
        return self.__user_id

    # Görev başlığı
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Görev başlığı boş bırakılamaz.")

        self.__title = value.strip()

    # Görev açıklaması
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value or ""

    # Öncelik seviyesi
    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value):
        if value not in self.VALID_PRIORITIES:
            raise ValueError("Geçersiz öncelik seviyesi.")

        self.__priority = value

    # Görev durumu
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise ValueError("Geçersiz görev durumu.")

        self.__status = value

    # Son teslim tarihi
    @property
    def due_date(self):
        return self.__due_date

    @due_date.setter
    def due_date(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise ValueError("Tarih YYYY-AA-GG formatında olmalıdır.")

        self.__due_date = value

    # Görevin oluşturulma tarihi
    @property
    def created_at(self):
        return self.__created_at

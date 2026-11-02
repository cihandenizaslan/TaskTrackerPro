
import sys
import sqlite3

from PyQt6.QtWidgets import QApplication, QMessageBox

from database.database_helper import DatabaseHelper

from repositories.user_repository import UserRepository
from repositories.task_repository import TaskRepository

from services.auth_service import AuthService
from services.task_service import TaskService

from ui.login_window import LoginWindow
from ui.dashboard import DashboardWindow


class ApplicationController:
    """
    Uygulama ekranları arasındaki geçişleri yönetir.
    """

    def __init__(self, auth_service, task_service):

        self.auth_service = auth_service
        self.task_service = task_service

        self.dashboard_window = None

        # Login ekranını oluştur.
        self.login_window = LoginWindow(
            self.auth_service
        )

        # Başarılı giriş sinyalini dinle.
        self.login_window.login_success.connect(
            self.open_dashboard
        )

    def open_dashboard(self, user):
        """
        Başarılı giriş yapan kullanıcı için Dashboard açar.
        """

        self.login_window.hide()

        self.dashboard_window = DashboardWindow(
            user,
            self.task_service
        )

        self.dashboard_window.logout_requested.connect(
            self.handle_logout
        )

        self.dashboard_window.show()

    def handle_logout(self):
        """
        Dashboard ekranını kapatıp Login ekranına döner.
        """

        if self.dashboard_window is not None:

            self.dashboard_window.close()
            self.dashboard_window = None

        self.login_window.password_input.clear()
        self.login_window.show()

    def start(self):

        self.login_window.show()


def main():

    app = QApplication(sys.argv)

    app.setApplicationName("TaskTracker Pro")
    app.setStyle("Fusion")

    try:

        # Veritabanı
        database = DatabaseHelper()

        database.initialize_database()

        # Repository katmanı
        user_repository = UserRepository(database)
        task_repository = TaskRepository(database)

        # Service katmanı
        auth_service = AuthService(user_repository)
        task_service = TaskService(task_repository)

        # Uygulama yöneticisi
        controller = ApplicationController(
            auth_service,
            task_service
        )

        controller.start()

        sys.exit(app.exec())

    except (sqlite3.Error, OSError) as error:

        QMessageBox.critical(
            None,
            "Başlatma Hatası",
            f"Uygulama başlatılamadı:\n{error}"
        )


if __name__ == "__main__":
    main()

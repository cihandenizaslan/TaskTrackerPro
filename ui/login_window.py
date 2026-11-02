
import sqlite3

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QFrame
)

from ui.register_window import RegisterWindow


class LoginWindow(QMainWindow):
    """
    Kullanıcı giriş ekranı.
    """

    # Başarılı girişte User nesnesini dışarı aktarır.
    login_success = pyqtSignal(object)

    def __init__(self, auth_service):
        super().__init__()

        self.auth_service = auth_service

        self.setWindowTitle("TaskTracker Pro")
        self.setMinimumSize(850, 550)

        self.setStyleSheet("""
                QMainWindow {
                background-color: #111827;
                color: #F9FAFB;
            }
            
            QWidget#centralWidget {
                background-color: #111827;
            }
            
            QFrame#heroPanel {
                background-color: #1E3A8A;
                border-radius: 18px;
            }
            
            QFrame#loginPanel {
                background-color: #1F2937;
                border-radius: 18px;
            }
            
            QLabel {
                background-color: transparent;
                color: #F9FAFB;
                font-size: 13px;
            }

            QFrame#heroPanel {
                background-color: #1E3A8A;
                border-radius: 18px;
            }

            QFrame#loginPanel {
                background-color: #1F2937;
                border-radius: 18px;
            }

            QLabel {
                color: #F9FAFB;
                font-size: 13px;
            }

            QLineEdit {
                background-color: #111827;
                color: white;
                border: 1px solid #374151;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
            }

            QLineEdit:focus {
                border: 1px solid #3B82F6;
            }

            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 13px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
            }

            QPushButton#registerButton {
                background-color: transparent;
                border: 1px solid #4B5563;
                color: #D1D5DB;
            }

            QPushButton#registerButton:hover {
                background-color: #374151;
            }
        """)

        self.setup_ui()

    def setup_ui(self):

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # SOL PANEL
        hero_panel = QFrame()
        hero_panel.setObjectName("heroPanel")

        hero_layout = QVBoxLayout(hero_panel)

        hero_layout.setContentsMargins(35, 45, 35, 35)
        hero_layout.setSpacing(20)

        logo = QLabel("TASKTRACKER PRO")
        logo.setStyleSheet("""
            font-size: 23px;
            font-weight: bold;
            color: white;
        """)

        hero_layout.addWidget(logo)

        slogan = QLabel(
            "Görevlerini yönet,\n"
            "hedeflerine ulaş."
        )

        slogan.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: white;
        """)

        hero_layout.addWidget(slogan)

        description = QLabel(
            "Projelerini ve günlük görevlerini "
            "tek bir platform üzerinden düzenle."
        )

        description.setWordWrap(True)

        description.setStyleSheet("""
            font-size: 15px;
            color: #DBEAFE;
        """)

        hero_layout.addWidget(description)

        hero_layout.addStretch()

        features = QLabel(
            "✓  Görevlerini kolayca yönet\n\n"
            "✓  Önceliklerini belirle\n\n"
            "✓  İlerlemeni takip et"
        )

        features.setStyleSheet("""
            font-size: 14px;
            color: white;
        """)

        hero_layout.addWidget(features)

        # SAĞ PANEL
        login_panel = QFrame()
        login_panel.setObjectName("loginPanel")

        login_layout = QVBoxLayout(login_panel)

        login_layout.setContentsMargins(35, 50, 35, 35)
        login_layout.setSpacing(15)

        welcome = QLabel("Tekrar Hoş Geldin")

        welcome.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
        """)

        login_layout.addWidget(welcome)

        subtitle = QLabel("Devam etmek için hesabına giriş yap.")

        subtitle.setStyleSheet("color: #9CA3AF;")

        login_layout.addWidget(subtitle)

        login_layout.addSpacing(15)

        # Kullanıcı adı
        login_layout.addWidget(QLabel("Kullanıcı Adı"))

        self.username_input = QLineEdit()

        self.username_input.setPlaceholderText(
            "Kullanıcı adınızı girin"
        )

        login_layout.addWidget(self.username_input)

        # Şifre
        login_layout.addWidget(QLabel("Şifre"))

        self.password_input = QLineEdit()

        self.password_input.setPlaceholderText(
            "Şifrenizi girin"
        )

        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        login_layout.addWidget(self.password_input)

        login_layout.addSpacing(10)

        # Giriş butonu
        self.login_button = QPushButton("Giriş Yap")

        self.login_button.clicked.connect(self.handle_login)

        login_layout.addWidget(self.login_button)

        # Kayıt butonu
        self.register_button = QPushButton("Yeni Hesap Oluştur")

        self.register_button.setObjectName("registerButton")

        self.register_button.clicked.connect(
            self.open_register_window
        )

        login_layout.addWidget(self.register_button)

        login_layout.addStretch()

        footer = QLabel("TaskTracker Pro | Kişisel Görev Yönetimi")

        footer.setStyleSheet("""
            color: #6B7280;
            font-size: 11px;
        """)

        login_layout.addWidget(footer)

        main_layout.addWidget(hero_panel, 1)
        main_layout.addWidget(login_panel, 1)

        # Enter tuşuyla giriş
        self.username_input.returnPressed.connect(
            self.handle_login
        )

        self.password_input.returnPressed.connect(
            self.handle_login
        )


    def handle_login(self):

        username = self.username_input.text()
        password = self.password_input.text()

        try:

            user = self.auth_service.login_user(
                username=username,
                password=password
            )

            self.password_input.clear()

            QMessageBox.information(
                self,
                "Giriş Başarılı",
                f"Hoş geldin, {user.username}!"
            )

            # Başarılı girişten sonra Dashboard'a geç.
            self.login_success.emit(user)

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Giriş Hatası",
                str(error)
            )

        except sqlite3.Error:

            QMessageBox.critical(
                self,
                "Veritabanı Hatası",
                "Giriş sırasında veritabanı hatası oluştu."
            )


    def open_register_window(self):
        """
        Kayıt ekranını açar.
        """

        register_window = RegisterWindow(
            self.auth_service,
            self
        )

        result = register_window.exec()

        # Kayıt başarılıysa kullanıcı adını giriş alanına aktar.
        if result == RegisterWindow.DialogCode.Accepted:

            self.username_input.setText(
                register_window.registered_username
            )

            self.password_input.setFocus()

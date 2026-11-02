
import sqlite3

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox
)


class RegisterWindow(QDialog):
    """
    Yeni kullanıcı kayıt ekranı.
    """

    def __init__(self, auth_service, parent=None):
        super().__init__(parent)

        self.auth_service = auth_service
        self.registered_username = ""

        self.setWindowTitle("TaskTracker Pro - Kayıt Ol")
        self.setFixedSize(420, 520)

        self.setStyleSheet("""
            QDialog {
                background-color: #111827;
                color: #F9FAFB;
            }

            QLabel {
                color: #F9FAFB;
                font-size: 13px;
            }

            QLineEdit {
                background-color: #1F2937;
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
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
            }

            QPushButton#backButton {
                background-color: transparent;
                color: #9CA3AF;
                border: 1px solid #374151;
            }

            QPushButton#backButton:hover {
                background-color: #1F2937;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(12)

        title = QLabel("Hesap Oluştur")
        title.setStyleSheet("""
            font-size: 25px;
            font-weight: bold;
            color: white;
        """)

        description = QLabel(
            "TaskTracker Pro'ya katılmak için bilgilerini gir."
        )

        description.setStyleSheet("color: #9CA3AF;")

        # Kullanıcı adı
        layout.addWidget(QLabel("Kullanıcı Adı"))

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adınız")

        layout.addWidget(self.username_input)

        # E-posta
        layout.addWidget(QLabel("E-posta"))

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("ornek@mail.com")

        layout.addWidget(self.email_input)

        # Şifre
        layout.addWidget(QLabel("Şifre"))

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("En az 8 karakter")
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        layout.addWidget(self.password_input)

        # Şifre tekrar
        layout.addWidget(QLabel("Şifre Tekrar"))

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText(
            "Şifrenizi tekrar girin"
        )

        self.confirm_password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        layout.addWidget(self.confirm_password_input)

        # Kayıt butonu
        self.register_button = QPushButton("Hesap Oluştur")
        self.register_button.clicked.connect(self.handle_register)

        layout.addWidget(self.register_button)

        # Geri dön butonu
        self.back_button = QPushButton("Giriş Ekranına Dön")
        self.back_button.setObjectName("backButton")
        self.back_button.clicked.connect(self.reject)

        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def handle_register(self):
        """
        Kullanıcı kayıt işlemini gerçekleştirir.
        """

        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        try:

            user = self.auth_service.register_user(
                username=username,
                email=email,
                password=password,
                confirm_password=confirm_password
            )

            self.registered_username = user.username

            QMessageBox.information(
                self,
                "Kayıt Başarılı",
                "Hesabınız başarıyla oluşturuldu!"
            )

            self.accept()

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Kayıt Hatası",
                str(error)
            )

        except sqlite3.Error:

            QMessageBox.critical(
                self,
                "Veritabanı Hatası",
                "Kayıt sırasında veritabanı hatası oluştu."
            )

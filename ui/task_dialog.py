
import sqlite3

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QDateEdit,
    QPushButton,
    QMessageBox
)

from models.task_item import TaskItem


class TaskDialog(QDialog):
    """
    Yeni görev ekleme ve mevcut görevi düzenleme penceresi.
    """

    def __init__(
        self,
        task_service,
        user_id,
        task=None,
        parent=None
    ):
        super().__init__(parent)

        self.task_service = task_service
        self.user_id = user_id
        self.task = task

        if self.task is None:
            self.setWindowTitle("Yeni Görev Oluştur")
        else:
            self.setWindowTitle("Görevi Düzenle")

        self.setFixedSize(480, 530)

        self.setStyleSheet("""
            QDialog {
                background-color: #111827;
                color: white;
            }

            QLabel {
                color: #F9FAFB;
                font-size: 13px;
            }

            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                background-color: #1F2937;
                color: white;
                border: 1px solid #374151;
                border-radius: 7px;
                padding: 9px;
            }

            QComboBox QAbstractItemView {
                background-color: #1F2937;
                color: white;
                selection-background-color: #2563EB;
            }

            QPushButton {
                background-color: #2563EB;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 11px 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
            }

            QPushButton#cancelButton {
                background-color: #374151;
            }

            QPushButton#cancelButton:hover {
                background-color: #4B5563;
            }
        """)

        self.setup_ui()

        # Düzenleme yapılıyorsa mevcut bilgileri doldur.
        if self.task is not None:
            self.load_task_data()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)

        # Başlık
        title = QLabel(
            "Görev Bilgileri"
        )

        title.setStyleSheet("""
            font-size: 23px;
            font-weight: bold;
        """)

        main_layout.addWidget(title)

        description = QLabel(
            "Görev detaylarını aşağıdaki alanlara giriniz."
        )

        description.setStyleSheet("color: #9CA3AF;")

        main_layout.addWidget(description)

        # Form alanları
        form_layout = QFormLayout()

        form_layout.setSpacing(13)

        # Görev başlığı
        self.title_input = QLineEdit()

        self.title_input.setPlaceholderText(
            "Örn: Python projesini tamamla"
        )

        form_layout.addRow(
            "Görev Başlığı:",
            self.title_input
        )

        # Görev açıklaması
        self.description_input = QTextEdit()

        self.description_input.setPlaceholderText(
            "Görev hakkında açıklama yazınız..."
        )

        self.description_input.setFixedHeight(85)

        form_layout.addRow(
            "Açıklama:",
            self.description_input
        )

        # Öncelik
        self.priority_combo = QComboBox()

        self.priority_combo.addItems(
            TaskItem.VALID_PRIORITIES
        )

        self.priority_combo.setCurrentText("Orta")

        form_layout.addRow(
            "Öncelik:",
            self.priority_combo
        )

        # Durum
        self.status_combo = QComboBox()

        self.status_combo.addItems(
            TaskItem.VALID_STATUSES
        )

        self.status_combo.setCurrentText("Bekliyor")

        form_layout.addRow(
            "Görev Durumu:",
            self.status_combo
        )

        # Son teslim tarihi
        self.due_date_edit = QDateEdit()

        self.due_date_edit.setCalendarPopup(True)

        self.due_date_edit.setDisplayFormat(
            "dd.MM.yyyy"
        )

        self.due_date_edit.setDate(
            QDate.currentDate()
        )

        form_layout.addRow(
            "Son Teslim Tarihi:",
            self.due_date_edit
        )

        main_layout.addLayout(form_layout)

        main_layout.addStretch()

        # Butonlar
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Kaydet")

        self.cancel_button = QPushButton("İptal")

        self.cancel_button.setObjectName(
            "cancelButton"
        )

        self.save_button.clicked.connect(
            self.handle_save
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

        button_layout.addWidget(self.cancel_button)

        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

    def load_task_data(self):
        """
        Düzenlenecek görevin mevcut bilgilerini forma aktarır.
        """

        self.title_input.setText(
            self.task.title
        )

        self.description_input.setPlainText(
            self.task.description
        )

        self.priority_combo.setCurrentText(
            self.task.priority
        )

        self.status_combo.setCurrentText(
            self.task.status
        )

        task_date = QDate.fromString(
            self.task.due_date,
            "yyyy-MM-dd"
        )

        if task_date.isValid():
            self.due_date_edit.setDate(task_date)

    def handle_save(self):
        """
        Görev ekleme veya güncelleme işlemini gerçekleştirir.
        """

        title = self.title_input.text()

        description = self.description_input.toPlainText()

        priority = self.priority_combo.currentText()

        status = self.status_combo.currentText()

        due_date = self.due_date_edit.date().toString(
            "yyyy-MM-dd"
        )

        try:

            if self.task is None:

                # CREATE
                self.task_service.add_task(
                    user_id=self.user_id,
                    title=title,
                    description=description,
                    priority=priority,
                    status=status,
                    due_date=due_date
                )

                message = "Görev başarıyla oluşturuldu!"

            else:

                # UPDATE
                self.task_service.update_task(
                    task_id=self.task.id,
                    user_id=self.user_id,
                    title=title,
                    description=description,
                    priority=priority,
                    status=status,
                    due_date=due_date
                )

                message = "Görev başarıyla güncellendi!"

            QMessageBox.information(
                self,
                "İşlem Başarılı",
                message
            )

            self.accept()

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Geçersiz Bilgi",
                str(error)
            )

        except sqlite3.Error:

            QMessageBox.critical(
                self,
                "Veritabanı Hatası",
                "Görev kaydedilirken bir hata oluştu."
            )

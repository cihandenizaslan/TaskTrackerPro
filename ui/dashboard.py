
import sqlite3


from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from ui.task_dialog import TaskDialog
from PyQt6.QtWidgets import (
    QDialog,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
    QMessageBox,
    QAbstractItemView,
)


class DashboardWindow(QMainWindow):
    """
    Kullanıcının görevlerini yönettiği ana ekran.
    """

    logout_requested = pyqtSignal()

    def __init__(self, user, task_service):
        super().__init__()

        self.user = user
        self.task_service = task_service

        self.setWindowTitle("TaskTracker Pro - Dashboard")
        self.setMinimumSize(1050, 680)

        self.setStyleSheet("""
                QMainWindow {
                background-color: #111827;
                color: #F9FAFB;
            }
            
            QWidget#centralWidget {
                background-color: #111827;
                color: #F9FAFB;
            }
            
            QLabel {
                background-color: transparent;
                color: #F9FAFB;
            }

            QFrame#sidebar {
                background-color: #1F2937;
                border-radius: 12px;
            }

            QFrame#statCard {
                background-color: #1F2937;
                border-radius: 12px;
            }

            QLabel {
                color: #F9FAFB;
            }

            QLineEdit, QComboBox {
                background-color: #1F2937;
                color: white;
                border: 1px solid #374151;
                border-radius: 7px;
                padding: 10px;
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
                padding: 10px 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1D4ED8;
            }

            QPushButton#logoutButton {
                background-color: #374151;
            }

            QPushButton#logoutButton:hover {
                background-color: #4B5563;
            }

            QTableWidget {
                background-color: #1F2937;
                alternate-background-color: #263244;
                color: white;
                border: none;
                border-radius: 10px;
                gridline-color: #374151;
                selection-background-color: #1D4ED8;
            }

            QHeaderView::section {
                background-color: #374151;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 7px;
            }
        """)

        self.setup_ui()
        self.load_tasks()

    def setup_ui(self):

        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(18)

        # =====================================
        # SOL MENÜ
        # =====================================

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(210)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 25, 18, 20)
        sidebar_layout.setSpacing(18)

        logo = QLabel("TASKTRACKER\nPRO")

        logo.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #60A5FA;
        """)

        sidebar_layout.addWidget(logo)

        sidebar_layout.addSpacing(20)

        menu_title = QLabel("ANA MENÜ")
        menu_title.setStyleSheet("""
            color: #9CA3AF;
            font-size: 11px;
            font-weight: bold;
        """)

        sidebar_layout.addWidget(menu_title)

        dashboard_label = QLabel("▣  Genel Bakış")

        dashboard_label.setStyleSheet("""
            background-color: #374151;
            padding: 12px;
            border-radius: 7px;
            font-weight: bold;
        """)

        sidebar_layout.addWidget(dashboard_label)

        # Kullanıcı bilgisi
        sidebar_layout.addStretch()

        user_title = QLabel("OTURUM AÇAN KULLANICI")
        user_title.setStyleSheet("""
            color: #9CA3AF;
            font-size: 10px;
        """)

        sidebar_layout.addWidget(user_title)

        username_label = QLabel(self.user.username)

        username_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            color: #60A5FA;
        """)

        sidebar_layout.addWidget(username_label)

        self.logout_button = QPushButton("Çıkış Yap")
        self.logout_button.setObjectName("logoutButton")

        self.logout_button.clicked.connect(self.handle_logout)

        sidebar_layout.addWidget(self.logout_button)

        main_layout.addWidget(sidebar)

        # =====================================
        # ANA İÇERİK
        # =====================================

        content_widget = QWidget()

        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(5, 5, 5, 5)
        content_layout.setSpacing(18)

        main_layout.addWidget(content_widget, 1)

        # Üst başlık
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel("Genel Bakış")

        title.setStyleSheet("""
            font-size: 27px;
            font-weight: bold;
        """)

        subtitle = QLabel(
            f"Hoş geldin, {self.user.username}! "
            "Görevlerinin genel durumuna göz at."
        )

        subtitle.setStyleSheet("color: #9CA3AF;")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        content_layout.addLayout(header_layout)

        # =====================================
        # İSTATİSTİK KARTLARI
        # =====================================

        stats_layout = QGridLayout()
        stats_layout.setSpacing(12)

        self.total_value = self.create_stat_card(
            stats_layout,
            0,
            0,
            "TOPLAM GÖREV",
            "#60A5FA"
        )

        self.pending_value = self.create_stat_card(
            stats_layout,
            0,
            1,
            "BEKLEYEN",
            "#FBBF24"
        )

        self.progress_value = self.create_stat_card(
            stats_layout,
            0,
            2,
            "DEVAM EDEN",
            "#A78BFA"
        )

        self.completed_value = self.create_stat_card(
            stats_layout,
            0,
            3,
            "TAMAMLANAN",
            "#34D399"
        )

        content_layout.addLayout(stats_layout)

        # =====================================
        # ARAMA VE FİLTRELEME
        # =====================================

        filter_title = QLabel("Görevlerim")

        filter_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        content_layout.addWidget(filter_title)

        filter_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Görev başlığına göre ara..."
        )

        self.status_combo = QComboBox()

        self.status_combo.addItem("Tüm Durumlar", None)
        self.status_combo.addItem("Bekliyor", "Bekliyor")
        self.status_combo.addItem("Devam Ediyor", "Devam Ediyor")
        self.status_combo.addItem("Tamamlandı", "Tamamlandı")

        self.priority_combo = QComboBox()

        self.priority_combo.addItem("Tüm Öncelikler", None)
        self.priority_combo.addItem("Düşük", "Düşük")
        self.priority_combo.addItem("Orta", "Orta")
        self.priority_combo.addItem("Yüksek", "Yüksek")

        self.refresh_button = QPushButton("Yenile")

        filter_layout.addWidget(self.search_input, 2)
        filter_layout.addWidget(self.status_combo, 1)
        filter_layout.addWidget(self.priority_combo, 1)
        filter_layout.addWidget(self.refresh_button)

        content_layout.addLayout(filter_layout)


        # =====================================
        # GÖREV İŞLEM BUTONLARI
        # =====================================

        action_layout = QHBoxLayout()

        self.add_task_button = QPushButton("+ Yeni Görev")

        self.edit_task_button = QPushButton("Görevi Düzenle")

        self.delete_task_button = QPushButton("Görevi Sil")

        self.edit_task_button.setStyleSheet("""
            background-color: #7C3AED;
        """)

        self.delete_task_button.setStyleSheet("""
            background-color: #DC2626;
        """)

        # Buton bağlantıları
        self.add_task_button.clicked.connect(
            self.open_add_task_dialog
        )

        self.edit_task_button.clicked.connect(
            lambda: self.open_edit_task_dialog()
        )

        self.delete_task_button.clicked.connect(
            self.delete_selected_task
        )

        action_layout.addWidget(self.add_task_button)

        action_layout.addStretch()

        action_layout.addWidget(self.edit_task_button)

        action_layout.addWidget(self.delete_task_button)

        content_layout.addLayout(action_layout)


        # Filtre sinyalleri
        self.search_input.textChanged.connect(self.load_tasks)

        self.status_combo.currentIndexChanged.connect(
            self.load_tasks
        )

        self.priority_combo.currentIndexChanged.connect(
            self.load_tasks
        )

        self.refresh_button.clicked.connect(self.load_tasks)

        # =====================================
        # GÖREV TABLOSU
        # =====================================

        self.task_table = QTableWidget()

        self.task_table.setColumnCount(4)

        self.task_table.setHorizontalHeaderLabels([
            "Görev Başlığı",
            "Öncelik",
            "Durum",
            "Son Teslim Tarihi"
        ])

        self.task_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.task_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.task_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.task_table.setAlternatingRowColors(True)

        self.task_table.verticalHeader().setVisible(False)

        self.task_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.task_table.setMinimumHeight(300)

        content_layout.addWidget(self.task_table, 1)

        self.task_table.cellDoubleClicked.connect(
            self.open_edit_task_dialog
        )

        # Alt bilgi
        self.footer_label = QLabel("Görev listesi hazır.")

        self.footer_label.setStyleSheet("""
            color: #9CA3AF;
            font-size: 11px;
        """)

        content_layout.addWidget(self.footer_label)

    def create_stat_card(
        self,
        parent_layout,
        row,
        column,
        title,
        color
    ):
        """
        Dashboard istatistik kartı oluşturur.
        """

        card = QFrame()
        card.setObjectName("statCard")

        card_layout = QVBoxLayout(card)

        card_layout.setContentsMargins(18, 18, 18, 18)

        title_label = QLabel(title)

        title_label.setStyleSheet("""
            color: #9CA3AF;
            font-size: 11px;
            font-weight: bold;
        """)

        value_label = QLabel("0")

        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 29px;
            font-weight: bold;
        """)

        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)

        parent_layout.addWidget(card, row, column)

        return value_label

    def load_tasks(self):
        """
        Kullanıcının görevlerini ve istatistiklerini yükler.
        """

        try:

            # Önce kullanıcının bütün görevlerini getir.
            all_tasks = self.task_service.get_user_tasks(
                self.user.id
            )

            # İstatistikleri hesapla.
            total = len(all_tasks)

            pending = sum(
                task.status == "Bekliyor"
                for task in all_tasks
            )

            in_progress = sum(
                task.status == "Devam Ediyor"
                for task in all_tasks
            )

            completed = sum(
                task.status == "Tamamlandı"
                for task in all_tasks
            )

            self.total_value.setText(str(total))
            self.pending_value.setText(str(pending))
            self.progress_value.setText(str(in_progress))
            self.completed_value.setText(str(completed))

            # Filtre bilgilerini al.
            search_text = self.search_input.text()

            status = self.status_combo.currentData()

            priority = self.priority_combo.currentData()

            # Filtrelenmiş görevleri getir.
            filtered_tasks = self.task_service.get_user_tasks(
                user_id=self.user.id,
                search_text=search_text,
                status=status,
                priority=priority
            )

            # Tabloyu temizle.
            self.task_table.setRowCount(0)

            # Görevleri tabloya ekle.
            for task in filtered_tasks:

                row = self.task_table.rowCount()

                self.task_table.insertRow(row)

                values = [
                    task.title,
                    task.priority,
                    task.status,
                    task.due_date
                ]

                for column, value in enumerate(values):

                    item = QTableWidgetItem(str(value))

                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignVCenter |
                        Qt.AlignmentFlag.AlignLeft
                    )

                    if column == 0:
                        # Görev ID bilgisini tabloda gizli olarak tut.
                        item.setData(
                            Qt.ItemDataRole.UserRole,
                            task.id
                        )

                    self.task_table.setItem(
                        row,
                        column,
                        item
                    )

            self.footer_label.setText(
                f"{len(filtered_tasks)} görev listeleniyor."
            )

        except sqlite3.Error:

            QMessageBox.critical(
                self,
                "Veritabanı Hatası",
                "Görevler yüklenirken bir veritabanı hatası oluştu."
            )

        except ValueError as error:

            QMessageBox.warning(
                self,
                "İşlem Hatası",
                str(error)
            )

    def open_add_task_dialog(self):
        """
        Yeni görev oluşturma penceresini açar.
        """

        dialog = TaskDialog(
            task_service=self.task_service,
            user_id=self.user.id,
            parent=self
        )

        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.load_tasks()

    def get_selected_task_id(self):
        """
        Tabloda seçili olan görevin ID değerini getirir.
        """

        row = self.task_table.currentRow()

        if row < 0:
            QMessageBox.warning(
                self,
                "Görev Seçilmedi",
                "Lütfen işlem yapmak için bir görev seçiniz."
            )

            return None

        item = self.task_table.item(row, 0)

        if item is None:
            return None

        task_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        return task_id

    def open_edit_task_dialog(self, row=None, column=None):
        """
        Seçilen görevi düzenleme penceresinde açar.
        """

        if row is not None:
            self.task_table.selectRow(row)

        task_id = self.get_selected_task_id()

        if task_id is None:
            return

        try:

            # Görevi veritabanından getir.
            tasks = self.task_service.get_user_tasks(
                self.user.id
            )

            selected_task = next(
                (
                    task for task in tasks
                    if task.id == task_id
                ),
                None
            )

            if selected_task is None:

                QMessageBox.warning(
                    self,
                    "Görev Bulunamadı",
                    "Seçilen görev bulunamadı."
                )

                self.load_tasks()
                return

            # Düzenleme penceresi
            dialog = TaskDialog(
                task_service=self.task_service,
                user_id=self.user.id,
                task=selected_task,
                parent=self
            )

            result = dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                self.load_tasks()

        except sqlite3.Error:

            QMessageBox.critical(
                self,
                "Veritabanı Hatası",
                "Görev bilgileri alınamadı."
            )

        except ValueError as error:

            QMessageBox.warning(
                self,
                "İşlem Hatası",
                str(error)
            )

    def delete_selected_task(self):
        """
        Seçilen görevi veritabanından siler.
        """

        task_id = self.get_selected_task_id()

        if task_id is None:
            return

        result = QMessageBox.question(
            self,
            "Görevi Sil",
            "Seçilen görevi silmek istediğinize emin misiniz?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if result != QMessageBox.StandardButton.Yes:
            return

        try:

            self.task_service.delete_task(
                task_id=task_id,
                user_id=self.user.id
            )

            QMessageBox.information(
                self,
                "İşlem Başarılı",
                "Görev başarıyla silindi."
            )

            self.load_tasks()

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Silme Hatası",
                str(error)
            )

        except sqlite3.Error:

            QMessageBox.critical(
                self,
                "Veritabanı Hatası",
                "Görev silinirken bir hata oluştu."
            )


    def handle_logout(self):
        """
        Kullanıcı oturumunu kapatır.
        """

        result = QMessageBox.question(
            self,
            "Çıkış Yap",
            "Hesabınızdan çıkış yapmak istiyor musunuz?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if result == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()

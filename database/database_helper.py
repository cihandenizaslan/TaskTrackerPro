
import sqlite3
import os
import sys
from pathlib import Path


class DatabaseHelper:
    """
    SQLite veritabanı bağlantısını ve tablo oluşturma
    işlemlerini yöneten sınıf.
    """

    def __init__(self):

        if getattr(sys, "frozen", False):
            # Paketlenmiş Windows uygulaması
            base_dir = Path(
                os.getenv(
                    "LOCALAPPDATA",
                    str(Path.home() / "AppData" / "Local")
                )
            )

            app_dir = base_dir / "TaskTrackerPro"
            app_dir.mkdir(parents=True, exist_ok=True)

            self.db_path = app_dir / "tasks.db"

        else:
            # PyCharm üzerinden çalıştırılan geliştirme sürümü
            self.db_path = Path(__file__).resolve().parent / "tasks.db"

    def get_connection(self):
        """Veritabanına bağlantı oluşturur."""

        connection = sqlite3.connect(str(self.db_path))

        # Sorgu sonuçlarına sütun isimleriyle erişim sağlar.
        connection.row_factory = sqlite3.Row

        # Foreign Key kontrollerini etkinleştirir.
        connection.execute("PRAGMA foreign_keys = ON")

        return connection

    def initialize_database(self):
        """Gerekli veritabanı tablolarını oluşturur."""

        connection = self.get_connection()

        try:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    priority TEXT NOT NULL
                        CHECK(priority IN ('Düşük', 'Orta', 'Yüksek')),
                    status TEXT NOT NULL DEFAULT 'Bekliyor'
                        CHECK(status IN (
                            'Bekliyor',
                            'Devam Ediyor',
                            'Tamamlandı'
                        )),
                    due_date TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
                );

                CREATE INDEX IF NOT EXISTS idx_tasks_user_id
                ON tasks(user_id);

                CREATE INDEX IF NOT EXISTS idx_tasks_status
                ON tasks(user_id, status);
            """)

            connection.commit()
            print(f"Veritabanı hazır: {self.db_path}")

        except sqlite3.Error as error:
            connection.rollback()
            print(f"Veritabanı oluşturulurken hata oluştu: {error}")
            raise

        finally:
            connection.close()

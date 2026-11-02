
import sqlite3

from models.user import User


class UserRepository:
    """
    Kullanıcı veritabanı işlemlerini yöneten sınıf.
    """

    def __init__(self, database_helper):
        self.database_helper = database_helper

    def create_user(self, user: User):
        """
        Yeni kullanıcıyı veritabanına kaydeder.
        Kaydedilen kullanıcının ID değerini döndürür.
        """

        connection = self.database_helper.get_connection()

        try:
            cursor = connection.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (
                    user.username,
                    user.email,
                    user.password_hash
                )
            )

            connection.commit()

            return cursor.lastrowid

        except sqlite3.IntegrityError as error:
            connection.rollback()

            error_message = str(error).lower()

            if "users.username" in error_message:
                raise ValueError("Bu kullanıcı adı zaten kullanılıyor.")

            elif "users.email" in error_message:
                raise ValueError("Bu e-posta adresi zaten kullanılıyor.")

            raise ValueError("Kullanıcı kaydı gerçekleştirilemedi.")

        finally:
            connection.close()

    def username_exists(self, username: str):
        """
        Kullanıcı adının veritabanında bulunup bulunmadığını kontrol eder.
        """

        connection = self.database_helper.get_connection()

        try:
            result = connection.execute(
                "SELECT 1 FROM users WHERE username = ?",
                (username,)
            ).fetchone()

            return result is not None

        finally:
            connection.close()

    def email_exists(self, email: str):
        """
        E-posta adresinin veritabanında bulunup bulunmadığını kontrol eder.
        """

        connection = self.database_helper.get_connection()

        try:
            result = connection.execute(
                "SELECT 1 FROM users WHERE email = ?",
                (email,)
            ).fetchone()

            return result is not None

        finally:
            connection.close()

    def get_by_username(self, username: str):
        """
        Kullanıcı adına göre kullanıcı bilgilerini getirir.
        Login aşamasında kullanılacaktır.
        """

        connection = self.database_helper.get_connection()

        try:
            row = connection.execute(
                "SELECT * FROM users WHERE username = ?",
                (username,)
            ).fetchone()

            if row is None:
                return None

            return User(
                user_id=row["id"],
                username=row["username"],
                email=row["email"],
                password_hash=row["password_hash"],
                created_at=row["created_at"]
            )

        finally:
            connection.close()

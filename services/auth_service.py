
import re
import hashlib
import secrets
import hmac

from models.user import User


class AuthService:
    """
    Kullanıcı kayıt ve kimlik doğrulama işlemlerini yönetir.
    """

    ITERATIONS = 600_000

    def __init__(self, user_repository):
        self.user_repository = user_repository

    @staticmethod
    def hash_password(password: str):
        """
        Şifreyi PBKDF2-HMAC-SHA256 yöntemiyle hashler.
        Her şifre için rastgele salt üretir.
        """

        salt = secrets.token_bytes(16)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            AuthService.ITERATIONS
        )

        return (
            f"pbkdf2_sha256$"
            f"{AuthService.ITERATIONS}$"
            f"{salt.hex()}$"
            f"{password_hash.hex()}"
        )

    @staticmethod
    def verify_password(password: str, stored_hash: str):
        """
        Girilen şifrenin kayıtlı hash ile eşleşip eşleşmediğini kontrol eder.
        Login aşamasında da kullanılacaktır.
        """

        try:
            algorithm, iterations, salt_hex, expected_hash = (
                stored_hash.split("$")
            )

            if algorithm != "pbkdf2_sha256":
                return False

            calculated_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                bytes.fromhex(salt_hex),
                int(iterations)
            )

            return hmac.compare_digest(
                calculated_hash.hex(),
                expected_hash
            )

        except (ValueError, TypeError, AttributeError):
            return False

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        confirm_password: str
    ):
        """
        Yeni kullanıcı kaydını gerçekleştirir.
        """

        # Boş alan kontrolü
        username = username.strip() if username else ""
        email = email.strip().lower() if email else ""

        if not username or not email or not password or not confirm_password:
            raise ValueError("Bütün alanları doldurunuz.")

        # Kullanıcı adı kontrolü
        if len(username) < 3 or len(username) > 30:
            raise ValueError(
                "Kullanıcı adı 3-30 karakter arasında olmalıdır."
            )

        if not re.fullmatch(r"[A-Za-z0-9_.-]+", username):
            raise ValueError(
                "Kullanıcı adı harf, rakam, nokta, tire "
                "ve alt çizgi içerebilir."
            )

        # E-posta kontrolü
        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.fullmatch(email_pattern, email):
            raise ValueError("Geçerli bir e-posta adresi giriniz.")

        # Şifre kontrolü
        if len(password) < 8:
            raise ValueError("Şifre en az 8 karakter olmalıdır.")

        if password != confirm_password:
            raise ValueError("Girilen şifreler birbiriyle eşleşmiyor.")

        # Kullanıcı adı kontrolü
        if self.user_repository.username_exists(username):
            raise ValueError("Bu kullanıcı adı zaten kullanılıyor.")

        # E-posta kontrolü
        if self.user_repository.email_exists(email):
            raise ValueError("Bu e-posta adresi zaten kullanılıyor.")

        # Şifreyi hashleme
        password_hash = self.hash_password(password)

        # User nesnesini oluşturma
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )

        # Veritabanına kaydetme
        user_id = self.user_repository.create_user(user)

        # Kayıtlı kullanıcıyı geri döndürme
        return User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=password_hash
        )

    def login_user(self, username: str, password: str):
        """
        Kullanıcı giriş işlemini gerçekleştirir.
        Başarılı girişte User nesnesini döndürür.
        """

        username = username.strip() if username else ""

        # Boş alan kontrolü
        if not username or not password:
            raise ValueError("Kullanıcı adı ve şifre zorunludur.")

        # Kullanıcıyı veritabanında bul
        user = self.user_repository.get_by_username(username)

        # Kullanıcı bulunamadıysa veya şifre yanlışsa
        if user is None or not self.verify_password(
            password,
            user.password_hash
        ):
            raise ValueError("Kullanıcı adı veya şifre hatalı.")

        # Başarılı giriş
        return user


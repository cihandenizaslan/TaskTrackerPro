
class User:
    """
    Sistemdeki kullanıcıları temsil eden sınıf.
    """

    def __init__(
        self,
        username: str,
        email: str,
        password_hash: str,
        user_id: int = None,
        created_at: str = None
    ):
        self.__id = user_id
        self.__username = username
        self.__email = email
        self.__password_hash = password_hash
        self.__created_at = created_at

    # Kullanıcı ID bilgisi
    @property
    def id(self):
        return self.__id

    # Kullanıcı adı
    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if not value or not value.strip():
            raise ValueError("Kullanıcı adı boş bırakılamaz.")

        self.__username = value.strip()

    # E-posta
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not value or not value.strip():
            raise ValueError("E-posta boş bırakılamaz.")

        if "@" not in value:
            raise ValueError("Geçerli bir e-posta giriniz.")

        self.__email = value.strip()

    # Şifre hash bilgisi
    @property
    def password_hash(self):
        return self.__password_hash

    # Oluşturulma tarihi
    @property
    def created_at(self):
        return self.__created_at

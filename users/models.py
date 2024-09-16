from typing import Optional
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

from utils.validators import validate_latin_characters


class UserManager(BaseUserManager):
    """Custom manager for user DB"""

    def create_user(self, email: str, password: Optional[str] = None) -> "User":
        """
        Creates and saves a User with the given email and password.
        """

        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email: str, password: Optional[str] = None) -> "User":
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    

class User(AbstractUser):
    username = None
    first_name = models.CharField(
        max_length=50,
        blank=True,
        validators=[validate_latin_characters],
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        validators=[validate_latin_characters],
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,  # The field must be unique
    )
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD: str = "email"  # is used as the unique identifier
    EMAIL_FIELD: str = "email"
    REQUIRED_FIELDS = []

    objects: UserManager = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """
        Text representation of user.

        Display its first name and last name.
        """
        return self.get_full_name()
    
    # it is also possible to configure has_perm has_module_perms or any other @property

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin
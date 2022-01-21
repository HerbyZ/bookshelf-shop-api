from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

NEW_USER_BONUS_BALANCE = 10


class UserManager(BaseUserManager):
    def create_user(self, email, password, bonus_balance=NEW_USER_BONUS_BALANCE):
        user = self.model(
            email=self.normalize_email(email),
            bonus_balance=bonus_balance
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, bonus_balance=0):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            bonus_balance=bonus_balance
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField('email', max_length=255, unique=True)
    balance = models.PositiveIntegerField('balance', default=0)
    bonus_balance = models.PositiveIntegerField(
        'bonus balance', default=0)
    date_joined = models.DateTimeField('join date', auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        app_label = 'accounts'

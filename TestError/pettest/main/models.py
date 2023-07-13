from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

User = get_user_model()  # модель юзера


class Pet(models.Model):
    objects = ''
    vin = models.CharField(verbose_name="Vin", db_index=True, unique=True, max_length=64)
    color = models.CharField(verbose_name="Color", max_length=64)
    name = models.CharField(verbose_name="Name", max_length=64)
    age = models.IntegerField(verbose_name="Age")
    PET_BREED = (
        (1, 'Кошка'),
        (2, 'Собака'),
        (3, 'Попугай'),
        (4, 'Змея'),
        (5, 'Крыса'),
        (6, 'Ящерица'),
    )
    breed = models.IntegerField(verbose_name="Breed", choices=PET_BREED)
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)


class MyUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("Вы не ввели Email")
        if not username:
            raise ValueError("Вы не ввели Логин")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password):
        return self._create_user(email, username, password)

    def create_superuser(self, email, username, password):
        return self._create_user(email, username, password, is_staff=True, is_superuser=True)


class UserProfile(models.Model):
    objects = ''
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyUserManager()

    def __str__(self):
        return self.email


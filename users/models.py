from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, name, gender, age, introduction=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            gender=gender,
            age=age,
            introduction=introduction,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, name, gender, age, introduction=None, password=None
    ):
        user = self.create_user(
            email,
            password=password,
            name=name,
            gender=gender,
            age=age,
            introduction=introduction,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Meta:
        db_table = "user"

    email = models.EmailField(max_length=255, unique=True, verbose_name="이메일 주소")
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name="이름")
    gender_choice = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = models.CharField(
        max_length=1, choices=gender_choice, blank=True, null=True, verbose_name="성별"
    )
    age = models.SmallIntegerField(blank=True, null=True, verbose_name="나이")
    introduction = models.TextField(blank=True, null=True, verbose_name="자기소개")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
        "gender",
        "age",
    ]

    def __str__(self):
        return str(self.name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

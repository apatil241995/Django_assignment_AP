from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, mobile_no, password, date_of_birth, first_name, last_name):
        if not email:
            raise ValueError("user must have a email")
        if not mobile_no:
            raise ValueError("user must have mobile no")
        user = self.model(
            email=self.normalize_email(email),
            mobile_no=mobile_no,
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_manager(self, email, mobile_no, password, date_of_birth, first_name, last_name):
        if not email:
            raise ValueError("user must have a email")
        if not mobile_no:
            raise ValueError("user must have mobile no")

        user = self.model(
            email=self.normalize_email(email),
            mobile_no=mobile_no,
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.is_manager = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_employee(self, email, mobile_no, password, date_of_birth, first_name, last_name):
        if not email:
            raise ValueError("user must have a email")
        if not mobile_no:
            raise ValueError("user must have mobile no")

        user = self.model(
            email=self.normalize_email(email),
            mobile_no=mobile_no,
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.is_employee = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    mobile_no = models.CharField(max_length=10, unique=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_no', 'date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_manager,self.is_superuser

    def has_module_perm(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_manager,self.is_superuser

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, job_role, district, password=None, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        if not first_name or not last_name:
            raise ValueError('Users must have a name and a surname')
        if not district:
            raise ValueError('Users must belong to a district')
        if not job_role:
            raise ValueError('Users must specify their job')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.job_role = job_role
        user.district = district
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, job_role, district, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            job_role,
            district,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, job_role, district, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            job_role,
            district,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    JOB_ROLES = (
        ('F', 'Farmer'),
        ('A', 'Agronomist'),
        ('P', 'PolicyMaker'),
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    staff = models.BooleanField(default=False)  # an admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    job_role = models.CharField(max_length=1, choices=JOB_ROLES)
    district = models.CharField(max_length=100)
    objects = UserManager()
    # password field inherited by superclass

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'job_role', 'district']  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return ('[email: ' + self.email + ', first name: ' + self.first_name + ', last name: ' + self.last_name
                    + ', job: ' + self.job_role + ', district: ' + self.district + ']')

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

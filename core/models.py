from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class Users(AbstractUser):
    class Roles(models.TextChoices):
        MANAGER = "manager"
        FOREMAN = "foreman"

    first_name = models.CharField(
        max_length=100, null=False, blank=False
    )
    last_name = models.CharField(
        max_length=100, null=False, blank=False
    )
    role = models.CharField(
        choices=Roles, null=False,
        blank=False, default=Roles.FOREMAN
    )
    phone = models.CharField(
        max_length=100, null=False, blank=False
    )

    email = None
    is_staff = None
    date_joined = None
    groups = None
    user_permissions = None
    last_login = None

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        return super().save(*args, **kwargs)


# projects
class Projects(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "In_Progress"
        DONE = "Done"

    title = models.CharField(
        max_length=100, null=False,
        blank=False, unique=True
    )
    description = models.TextField(
        null=True, blank=True
    )
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, null=False, blank=False
    )
    status = models.CharField(
        max_length=100, choices=Status,
        default=Status.IN_PROGRESS, null=False, blank=False
    )
    deadline = models.DateField(
        null=False, blank=True
    )
    done_date = models.DateField(
        null=True, blank=True
    )

    class Meta:
        db_table = "Projects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        status = self.status
        if status == self.Status.DONE and self.done_date is None:
            self.done_date = timezone.now().date()

        return super().save(*args, **kwargs)


class Tasks(models.Model):
    class Status(models.TextChoices):
        PICKED = "picked"
        PENDING = "pending"

    class Levels(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    title = models.CharField(
        max_length=100, null=False, blank=False
    )
    project = models.ForeignKey(
        Projects, null=False, blank=False, on_delete=models.CASCADE
    )
    description = models.TextField(
        null=True, blank=True
    )
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, null=False, blank=False, related_name='user_task'
    )
    foreman = models.ForeignKey(
        Users, null=True, blank=True, on_delete=models.CASCADE
    )
    level = models.IntegerField(
        choices=Levels, null=False, blank=False
    )
    deadline = models.DateField(
        null=False, blank=False
    )
    status = models.CharField(
        choices=Status, null=False, blank=False, default=Status.PENDING
    )

    class Meta:
        db_table = "Tasks"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        user = self.user
        if user.role != Users.Roles.MANAGER:
            raise ValidationError(
                detail='نقض کاربر باید manager باشد ... !'
            )

        if self.foreman:
            if self.foreman.role != Users.Roles.FOREMAN:
                raise ValidationError(
                    detail='نقض کارمند باید foreman باشد ... !'
                )
            self.status = self.Status.PICKED

        return super().save(*args, **kwargs)

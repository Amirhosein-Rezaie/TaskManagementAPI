from django.db import models
from core.models import (Users, Tasks, Projects)
from django.utils import timezone


# tag on the tasks by users(foremans)
class Tags(models.Model):
    class Titles(models.TextChoices):
        TODO = "ToDo"
        INPROGRESS = "InProgress"
        DONE = "Done"

    user = models.ForeignKey(
        Users, null=False, blank=False, related_name='user_tag'
    )
    task = models.ForeignKey(
        Tasks, null=False, blank=False, related_name='tag_task'
    )
    title = models.CharField(
        choices=Titles, null=False, blank=False, default=Titles.TODO
    )
    date = models.DateField(
        auto_now_add=True
    )
    time = models.TimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "Tags"

    def __str__(self):
        return f"{self.user} -> {self.task}"


# set score for users(foreman)
class Scores(models.Model):
    score = models.IntegerField(
        choices=[n for n in range(1, 6)], null=False, blank=False
    )
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, null=False, blank=False
    )
    task = models.ForeignKey(
        Tasks, null=False, blank=False, on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'Scores'

    def __str__(self):
        return f"{self.user} -> {self.task} => {self.score}"


# members of every projects model
class ProjectMembers(models.Model):
    class Status(models.TextChoices):
        IN_PROJECT = "InProject"
        LEFT_PROJECT = "LeftProject"

    member = models.ForeignKey(
        Users, on_delete=models.CASCADE, null=False, blank=False
    )
    project = models.ForeignKey(
        Projects, on_delete=models.CASCADE, null=False, blank=False
    )
    join_date = models.DateField(
        auto_now_add=True
    )
    left_date = models.DateField(
        null=True, blank=True
    )
    status = models.CharField(
        max_length=100, choices=Status, default=Status.IN_PROJECT, null=False, blank=False
    )

    class Meta:
        db_table = "Project_Members"

    def __str__(self):
        return f"{self.member} -> {self.project}"

    def save(self, *args, **kwargs):
        if self.status == self.Status.LEFT_PROJECT and self.left_date in None:
            self.left_date = timezone.now().date()
        super().save(*args, **kwargs)

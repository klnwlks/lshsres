from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Includes additional fields for section and role information.
    """
    name = models.CharField(max_length=255)
    section = models.ForeignKey(
        'Section',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )
    isStudent = models.BooleanField(default=True)
    datemade = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Model for posts created by users.
    """
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    date_made = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.name} on {self.date_made}"

    class Meta:
        ordering = ['-date_made']

class Section(models.Model):
    """
    Model for sections that can contain an adviser and multiple students.
    """
    adviser = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='advised_sections'
    )
    students = ArrayField(
        models.IntegerField(),
        blank=True,
        null=True,
        help_text="IDs of enrolled students"
    )

    def __str__(self):
        return f"Section advised by {self.adviser.name if self.adviser else 'No adviser'}"
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True,  unique=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Department(models.Model):
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body


class Category(models.Model):
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body


class Annoucements(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True,  unique=True, editable=False)
    participants = models.ManyToManyField(
        User, related_name='participants', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title


class Employees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=200)
    second_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=200)
    designination = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True,  unique=True, editable=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.first_name


class Dayend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.ForeignKey(
        Employees, on_delete=models.CASCADE, null=True)
    checkout = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']


class Assests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=400)
    serial_no = models.CharField(max_length=400)
    employee = models.ForeignKey(
        Employees, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True,  unique=True, editable=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Faq(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True,  unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title


class Messages(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    annoucement = models.ForeignKey(
        Annoucements, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body

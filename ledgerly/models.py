from django.db import models

class User(models.Model):
    class Meta: db_table = "users"
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
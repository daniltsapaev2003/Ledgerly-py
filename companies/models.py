from django.db import models

class Company(models.Model):
    ticker = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    logo_color = models.CharField(max_length=7)
    logo_path = models.CharField(max_length=255, blank=True, null=True)
    tinkoff_uid = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

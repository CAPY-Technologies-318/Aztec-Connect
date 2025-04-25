from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.
class newSubmission(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    verification_code = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    race = models.CharField(max_length=100)
    sports = models.CharField(max_length=100)

    def generate_verification_code(self):
        self.verification_code = str(random.randint(100000, 999999))
        self.save()
    
    def __str__(self):
        return self.username







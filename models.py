from django.db import models
from accounts.models import newSubmission as User 
import random

class Club(models.Model):
    CATEGORY_CHOICES = [
        ('STEM', 'STEM'),
        ('SPORTS', 'Sports'),
        ('CULTURE', 'Culture'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='CULTURE')
    logo = models.ImageField(upload_to='club_logos/')
    banner = models.ImageField(upload_to='club_banners/')
    description = models.TextField()
    benefits = models.TextField()
    meeting_times = models.CharField(max_length=100)
    meeting_dates = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class UserClubInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)
    joined = models.BooleanField(default=False)
    

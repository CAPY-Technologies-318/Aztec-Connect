from django.db import models
from accounts.models import newSubmission as User 
import random

class Club(models.Model):
    CATEGORY_CHOICES = [
        ('Cultural', 'Cultural'),
        ('Social Sorority', 'Social Sorority'),
        ('Social Fraternity', 'Social Fraternity'),
        ('Academic Major Related', 'Academic Major Related'),
        ('Religious Based', 'Religious Based'),
        ('Service & Support', 'Service & Support'),
        ('Honor Society', 'Honor Society'),
        ('Greek Auxiliary Group', 'Greek Auxiliary Group'),
        ('Leadership', 'Leadership'),
        ('Political', 'Political'),
        ('Recreational', 'Recreational'),
        ('Imperial Valley Campus', 'Imperial Valley Campus'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='Other')
    logo = models.ImageField(upload_to='club_logos/', default='club_logos/default_logo.jpg', blank=True, null=True)
    banner = models.ImageField(upload_to='club_banners/', default='club_banners/default_banner.jpg', blank=True, null=True)
    description = models.TextField(blank=True)
    meeting_time = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True, null=True)
    meeting_location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
    
class UserClubInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)
    joined = models.BooleanField(default=False)
    

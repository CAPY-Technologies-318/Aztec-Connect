from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.
class newSubmission(models.Model):
    # Choices for dropdown menus
    MAJOR_CHOICES = [
        ('', 'Select Major'),  # Empty default option
        ('accounting', 'Accounting'),
        ('africana_studies', 'Africana Studies'),
        ('american_indian_studies', 'American Indian Studies'),
        ('anthropology', 'Anthropology'),
        ('art', 'Art'),
        ('astronomy', 'Astronomy'),
        ('aerospace_engineering', 'Aerospace Engineering'),
        ('biology', 'Biology'),
        ('brazilian_studies', 'Brazilian Studies'),
        ('chemical_physics', 'Chemical Physics'),
        ('chemistry', 'Chemistry'),
        ('child_development', 'Child Development'),
        ('civil_engineering', 'Civil Engineering'),
        ('classics', 'Classics'),
        ('communication', 'Communication'),
        ('comparative_international_studies', 'Comparative International Studies'),
        ('comparative_literature', 'Comparative Literature'),
        ('computer_engineering', 'Computer Engineering'),
        ('computer_science', 'Computer Science'),
        ('construction_engineering', 'Construction Engineering'),
        ('construction_management', 'Construction Management'),
        ('criminal_justice', 'Criminal Justice'),
        ('dance', 'Dance'),
        ('economics', 'Economics'),
        ('electrical_engineering', 'Electrical Engineering'),
        ('english_comparative_literature', 'English and Comparative Literature'),
        ('environmental_engineering', 'Environmental Engineering'),
        ('environmental_sciences', 'Environmental Sciences'),
        ('european_studies', 'European Studies'),
        ('finance', 'Finance'),
        ('financial_services', 'Financial Services'),
        ('foods_and_nutrition', 'Foods and Nutrition'),
        ('french', 'French'),
        ('geography', 'Geography'),
        ('geological_sciences', 'Geological Sciences'),
        ('german', 'German'),
        ('health_communication', 'Health Communication'),
        ('history', 'History'),
        ('hospitality_tourism_management', 'Hospitality and Tourism Management'),
        ('humanities', 'Humanities'),
        ('information_systems', 'Information Systems'),
        ('interdisciplinary_studies', 'Interdisciplinary Studies in Three Departments'),
        ('international_business', 'International Business'),
        ('international_security', 'International Security and Conflict Resolution'),
        ('islamic_arabic_studies', 'Islamic and Arabic Studies'),
        ('japanese', 'Japanese'),
        ('journalism', 'Journalism'),
        ('kinesiology', 'Kinesiology'),
        ('language_culture_society', 'Language, Culture, and Society'),
        ('latin_american_studies', 'Latin American Studies'),
        ('leadership_studies', 'Leadership Studies'),
        ('lgbtq_studies', 'Lesbian, Gay, Bisexual, Transgender, Queer, and Plus (LGBTQ+) Studies'),
        ('liberal_studies', 'Liberal Studies'),
        ('linguistics', 'Linguistics'),
        ('management', 'Management'),
        ('mathematics', 'Mathematics'),
        ('mechanical_engineering', 'Mechanical Engineering'),
        ('microbiology', 'Microbiology'),
        ('modern_jewish_studies', 'Modern Jewish Studies'),
        ('music', 'Music'),
        ('musical_theatre', 'Musical Theatre'),
        ('nursing', 'Nursing'),
        ('philosophy', 'Philosophy'),
        ('physical_science', 'Physical Science'),
        ('physics', 'Physics'),
        ('political_science', 'Political Science'),
        ('public_administration', 'Public Administration'),
        ('public_health', 'Public Health'),
        ('psychology', 'Psychology'),
        ('recreation_administration', 'Recreation Administration'),
        ('real_estate', 'Real Estate'),
        ('religious_studies', 'Religious Studies'),
        ('rhetoric_writing_studies', 'Rhetoric and Writing Studies'),
        ('russian', 'Russian'),
        ('russian_central_european_studies', 'Russian and Central European Studies'),
        ('social_science', 'Social Science'),
        ('social_work', 'Social Work'),
        ('sociology', 'Sociology'),
        ('spanish', 'Spanish'),
        ('speech_language_hearing', 'Speech, Language, and Hearing Sciences'),
        ('statistics', 'Statistics'),
        ('sustainability', 'Sustainability'),
        ('theatre_arts', 'Theatre Arts'),
        ('television_film_new_media', 'Television, Film and New Media'),
        ('urban_studies', 'Urban Studies'),
        ('womens_studies', 'Women\'s Studies'),
    ]

    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('non_binary', 'Non-binary'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    RACE_CHOICES = [
        ('', 'Select Race/Ethnicity'),
        ('asian', 'Asian'),
        ('black', 'Black or African American'),
        ('hispanic', 'Hispanic or Latino'),
        ('white', 'White'),
        ('native_american', 'Native American'),
        ('pacific_islander', 'Pacific Islander'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]

    SPORTS_CHOICES = [
        ('', 'Select Interest'),
        ('yes', 'Yes'),
        ('no', 'No'),
        ('maybe', 'Maybe'),
    ]

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    verification_code = models.CharField(max_length=6)
    name = models.CharField(max_length=100)
    major = models.CharField(max_length=100, choices=MAJOR_CHOICES, default='')
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default='')
    race = models.CharField(max_length=100, choices=RACE_CHOICES, default='')
    sports = models.CharField(max_length=100, choices=SPORTS_CHOICES, default='')

    def generate_verification_code(self):
        self.verification_code = str(random.randint(100000, 999999))
        self.save()
    
    def __str__(self):
        return self.username







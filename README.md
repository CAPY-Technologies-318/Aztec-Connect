# SDSU Club Discovery Platform

A Django-based web application designed to improve club discoverability at San Diego State University (SDSU). This platform provides personalized club recommendations based on student profiles, making it easier for students to find and connect with clubs and organizations that match their interests.

## 🎯 Project Overview

The goal of this project is to create a user-friendly platform that shows students a custom list of clubs and organizations from SDSU. Discoverability is the main focus of this project, addressing the previously lackluster and hard-to-navigate current options available to SDSU students.

## ✨ Features

- **Personalized Recommendations**: AI-powered club suggestions based on user major, interests, and preferences
- **User Profiles**: Comprehensive student profiles with academic and personal information
- **Club Management**: Detailed club pages with descriptions, meeting times, contact information, and media
- **Interactive Features**: Like, dislike, and join functionality for clubs
- **Search & Filter**: Browse clubs by category, major relevance, or search terms
- **Responsive Design**: Mobile-friendly interface for on-the-go access

## 🏗️ Tech Stack

- **Backend**: Django 5.2 (Python)
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS, JavaScript
- **File Storage**: Django's file handling for club logos and banners
- **Authentication**: Django's built-in user authentication system

## 📁 Project Structure

```
hackathon_426/
├── accounts/                 # User account management
│   ├── models.py            # User profile and submission models
│   ├── views.py             # Authentication and profile views
│   ├── forms.py             # User registration and profile forms
│   └── templates/           # Account-related templates
├── clubs/                   # Club management system
│   ├── models.py            # Club and interaction models
│   ├── views.py             # Club discovery and recommendation logic
│   ├── urls.py              # Club-related URL patterns
│   └── templates/           # Club-related templates
├── media/                   # User-uploaded files
│   ├── club_logos/          # Club logo images
│   ├── club_banners/        # Club banner images
│   └── profile_pictures/    # User profile pictures
├── staticfiles/             # Static CSS, JS, and images
├── manage.py                # Django management script
└── db.sqlite3              # Development database
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Django 5.2
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CAPY-Technologies-318/hackathon-426.git
   cd hackathon-426
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Navigate to project directory**
   ```bash
   cd hackathon_426
   ```

5. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

## 🎮 Usage

### For Students

1. **Create Account**: Register with your academic information including major, interests, and preferences
2. **Explore Clubs**: Browse through personalized club recommendations
3. **Interact**: Like, dislike, or join clubs that interest you
4. **Search**: Use filters to find specific types of clubs or organizations
5. **View Details**: Access detailed information about each club including meeting times and contact info

### For Administrators

1. **Club Management**: Add, edit, and manage club information through the Django admin panel
2. **User Oversight**: Monitor user registrations and interactions
3. **Content Moderation**: Manage club descriptions, images, and contact information

## 🔧 Key Components

### Models

- **newSubmission**: Extended user profile with academic and personal information
- **Club**: Club/organization information with categories, descriptions, and media
- **UserClubInteraction**: Tracks user interactions (likes, dislikes, joins) with clubs

### Recommendation System

The platform uses a sophisticated recommendation algorithm that considers:
- User's academic major and interests
- Previously liked/disliked clubs
- Popular clubs among similar users
- Club categories and activities

### Club Categories

- Cultural
- Social Sorority/Fraternity
- Academic Major Related
- Religious Based
- Service & Support
- Honor Society
- Greek Auxiliary Group
- Leadership
- Political
- Recreational
- Imperial Valley Campus
- Other

## 🎨 Customization

### Adding New Club Categories

Edit the `CATEGORY_CHOICES` in `clubs/models.py`:

```python
CATEGORY_CHOICES = [
    ('new_category', 'New Category Name'),
    # ... existing categories
]
```

### Modifying Recommendation Logic

The recommendation algorithm is located in `clubs/views.py` in the club discovery functions. You can adjust weights and criteria based on your institution's needs.

## 🐛 Troubleshooting

### Common Issues

1. **Static files not loading**: Run `python manage.py collectstatic`
2. **Database errors**: Ensure migrations are applied with `python manage.py migrate`
3. **Media files not displaying**: Check `MEDIA_URL` and `MEDIA_ROOT` settings in `settings.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of a hackathon submission. Please check with the repository maintainers for licensing information.

## 👥 Team

**CAPY Technologies 318**

## 📞 Support

For support and questions, please open an issue in the GitHub repository or contact the development team.

---

**Note**: This application was developed as part of a hackathon project to improve student life at SDSU through better club discoverability and engagement. 

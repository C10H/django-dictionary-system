# English-Chinese Dictionary System

A Django-based web application that provides English-Chinese translation services with automatic language detection, local database lookup, and Baidu Translation API integration.

## Features

- **Automatic Language Detection**: Automatically detects Chinese or English input
- **Dual Translation Source**: 
  - Primary: Local SQLite database lookup
  - Fallback: Baidu Translation API for missing words
- **Admin Management System**: 
  - User registration and authentication
  - Add, edit, and delete dictionary entries
  - Web-based admin interface
- **Real-time Translation**: Ajax-based translation without page refresh
- **Responsive Design**: Clean and user-friendly interface

## Technology Stack

- **Backend**: Django 4.2.23
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **API**: Baidu Translation API
- **Python**: 3.9+

## Installation

### Prerequisites

- Python 3.9+
- Conda (recommended) or pip
- Internet connection for Baidu Translation API

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd /path/to/dictionary_python
   ```

2. **Create virtual environment**
   ```bash
   conda create -n dictionary_env python=3.9 -y
   conda activate dictionary_env
   ```

3. **Install dependencies**
   ```bash
   pip install django requests
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create initial data**
   ```bash
   python initial_data.py
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver 8085
   ```

## Usage

### Accessing the Application

- **Home Page**: http://localhost:8085
  - Enter Chinese or English text for translation
  - Results show both translation and source (database/API)

- **Admin Login**: http://localhost:8085/login
  - Default credentials: `admin` / `password`
  - Manage dictionary entries after login

- **Registration**: http://localhost:8085/register
  - Create new admin accounts

### Translation Features

1. **Text Input**: Enter any Chinese or English text
2. **Auto-Detection**: System automatically detects language
3. **Smart Lookup**: 
   - First searches local database
   - Falls back to Baidu API if not found
4. **Source Indication**: Shows whether result came from database or API

### Admin Features

After logging in, administrators can:
- View all dictionary entries
- Add new word-translation pairs
- Update existing entries
- Delete entries
- Monitor entry creation/update timestamps

## API Configuration

The system uses Baidu Translation API with the following configuration:

- **App ID**: `20240531002066782`
- **Secret Key**: `2UYrEDwvtMgOShDLo3u8`

To change API credentials, update the `baidu_translate` function in `dictionary/views.py`.

## Project Structure

```
dictionary_python/
├── dictionary/                 # Main Django app
│   ├── templates/dictionary/   # HTML templates
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── urls.py                # URL patterns
│   └── admin.py               # Admin interface
├── dictionary_system/         # Django project settings
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL configuration
│   └── wsgi.py                # WSGI application
├── manage.py                  # Django management script
├── initial_data.py            # Initial data creation script
└── db.sqlite3                 # SQLite database
```

## Database Schema

### DictionaryEntry Model
- `id`: Primary key
- `word`: Unique word/phrase (CharField, max 200 chars)
- `translation`: Translation text (TextField)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### User Authentication
- Uses Django's built-in User model
- UserProfile model for extended user information

## Initial Data

The system comes with pre-populated data:

**Dictionary Entries**:
- hello → 你好
- test → 测试
- 时间 → time

**Admin User**:
- Username: `admin`
- Password: `password`

## Security Features

- CSRF protection on all forms
- User authentication required for admin functions
- Password validation
- SQL injection protection via Django ORM

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Try different port
   python manage.py runserver 8086
   ```

2. **Database Issues**
   ```bash
   # Reset database
   rm db.sqlite3
   python manage.py migrate
   python initial_data.py
   ```

3. **Translation API Errors**
   - Check internet connection
   - Verify API credentials
   - Check API quota limits

### Development Tips

- Use Django's built-in admin at `/admin/` for database management
- Check `django.log` for detailed error messages
- Use browser developer tools to debug Ajax requests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with Baidu Translation API terms of service.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Django documentation
3. Check Baidu Translation API documentation
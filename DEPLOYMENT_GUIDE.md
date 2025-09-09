# 🚀 PythonAnywhere Deployment Guide

Complete step-by-step guide to deploy your Django Movie Tracker on PythonAnywhere.

## 📋 Prerequisites

1. **PythonAnywhere Account**: Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **TMDB API Key**: Get one from [themoviedb.org](https://www.themoviedb.org/settings/api)

---

## 🔧 Step-by-Step Deployment

### Step 1: Set Up PythonAnywhere Console

1. **Log into PythonAnywhere**
2. **Open a Bash Console** (from Dashboard → Tasks → Consoles → Bash)
3. **Clone your repository**:
   ```bash
   git clone https://github.com/himanshuone/django-movie-tracker.git
   cd django-movie-tracker
   ```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3.10 -m venv movietracker-venv

# Activate virtual environment
source movietracker-venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables

1. **Create .env file**:
   ```bash
   cp .env.example .env
   nano .env
   ```

2. **Edit .env file with your settings**:
   ```env
   DEBUG=False
   SECRET_KEY=your-super-secret-production-key-change-this
   ALLOWED_HOSTS=yourusername.pythonanywhere.com
   TMDB_API_KEY=your-tmdb-api-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   ```

### Step 4: Collect Static Files

```bash
# Make sure you're in the project directory and virtual environment is activated
python manage.py collectstatic --noinput
```

### Step 5: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (use your preferred credentials)
python manage.py createsuperuser
```

### Step 6: Configure Web App on PythonAnywhere

1. **Go to Web tab** in PythonAnywhere dashboard
2. **Create a new web app**:
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select "Python 3.10"

3. **Configure Source Code**:
   - Source code: `/home/yourusername/django-movie-tracker`
   - Working directory: `/home/yourusername/django-movie-tracker`

4. **Configure Virtual Environment**:
   - Virtual env: `/home/yourusername/django-movie-tracker/movietracker-venv`

### Step 7: Configure WSGI File

1. **Edit the WSGI configuration file** (click on WSGI configuration file link)
2. **Replace the content** with:

   ```python
   import os
   import sys
   
   # Add your project directory to Python path
   path = '/home/yourusername/django-movie-tracker'
   if path not in sys.path:
       sys.path.append(path)
   
   # Set environment variables
   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movietracker.settings')
   
   # Import Django WSGI application
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

   **⚠️ Important**: Replace `yourusername` with your actual PythonAnywhere username!

### Step 8: Configure Static Files

1. **In the Web tab**, scroll to "Static files" section
2. **Add static file mapping**:
   - URL: `/static/`
   - Directory: `/home/yourusername/django-movie-tracker/staticfiles/`

3. **Add media file mapping**:
   - URL: `/media/`
   - Directory: `/home/yourusername/django-movie-tracker/media/`

### Step 9: Final Configuration

1. **Reload your web app** (big green "Reload" button in Web tab)
2. **Check error logs** if something goes wrong (Error log link in Web tab)

---

## 🎯 Post-Deployment Steps

### 1. Create Admin User
```bash
cd django-movie-tracker
source movietracker-venv/bin/activate
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('himanshu', 'himanshu@example.com', 'himanshu16664')
exit()
```

### 2. Test Your App

Visit your app at: `https://yourusername.pythonanywhere.com`

**Test these features**:
- ✅ Movie list displays correctly
- ✅ Login as admin works
- ✅ Add/Edit movies (admin only)
- ✅ Upload CSV (admin only)
- ✅ Non-admin users can view but not edit
- ✅ Poster images load correctly

---

## 🔧 Troubleshooting

### Common Issues:

1. **500 Internal Server Error**:
   - Check error logs in Web tab
   - Ensure virtual environment path is correct
   - Verify WSGI file is properly configured

2. **Static files not loading**:
   - Run `python manage.py collectstatic` again
   - Check static files mapping in Web tab

3. **Database issues**:
   - Run migrations: `python manage.py migrate`
   - Check if db.sqlite3 file exists

4. **Permission denied errors**:
   - Check file permissions
   - Ensure virtual environment is activated

### Useful Commands:

```bash
# Check if virtual environment is working
which python

# Restart web app (if you have a paid account)
# Free accounts need to use the Reload button in Web tab

# Check Django version
python -m django --version

# Test database connection
python manage.py check

# Check static files
python manage.py collectstatic --dry-run
```

---

## 🔄 Updating Your App

When you make changes to your code:

1. **Update code**:
   ```bash
   cd django-movie-tracker
   git pull origin main
   ```

2. **Update dependencies** (if requirements.txt changed):
   ```bash
   source movietracker-venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run migrations** (if models changed):
   ```bash
   python manage.py migrate
   ```

4. **Collect static files** (if CSS/JS changed):
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Reload web app** in PythonAnywhere Web tab

---

## 🎉 Success!

Your Django Movie Tracker should now be live at:
**https://yourusername.pythonanywhere.com**

### Admin Access:
- **Username**: `himanshu`
- **Password**: `himanshu16664`
- **Admin URL**: `https://yourusername.pythonanywhere.com/admin/`

### Features Available:
- 🎬 Beautiful movie cards with poster overlays
- 🔐 Admin-only movie management
- 📊 Statistics and export features
- 📱 Responsive design
- 🔍 Search and filtering
- 📤 CSV import/export

---

## 🆘 Need Help?

- Check PythonAnywhere help pages
- Review error logs in Web tab
- Ensure all file paths use your correct username
- Contact PythonAnywhere support if needed

**🚀 Happy deploying!**

# Movie Tracker - Django Application with Tailwind CSS

A personal movie tracking application built with Django and styled with Tailwind CSS, featuring a custom color palette.

![Movie Tracker](https://img.shields.io/badge/Django-4.2-green?style=flat-square)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=flat-square)

## 🎨 Color Palette

This application uses a carefully curated color palette:
- **text-gray-400** (#9ca3af) - Light gray for secondary text
- **text-gray-600** (#4b5563) - Medium gray for primary text  
- **text-orange-700** (#c2410c) - Dark orange for accents and danger actions
- **teal** (#14b8a6) - Primary brand color for buttons and highlights

## 🚀 Features

- Track your personal movie collection
- Add movies manually or via CSV upload
- Search and filter functionality
- Movie statistics and analytics
- Responsive design with mobile-first approach
- Modern UI with Tailwind CSS
- Clean, accessible design

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Node.js 14 or higher
- npm (comes with Node.js)
- Git

## 🛠️ Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd movie-tracker
```

### Step 2: Set Up Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\\Scripts\\activate
```

### Step 3: Install Python Dependencies
```bash
pip install django
pip install pillow  # for image handling
pip install python-decouple  # for environment variables (optional)
```

### Step 4: Install Tailwind CSS CLI
```bash
# Install Tailwind CLI globally
npm install -g @tailwindcss/cli

# Or install project dependencies (recommended)
npm install
```

### Step 5: Configure Tailwind CSS

The project already includes the following Tailwind configuration files:

#### `tailwind.config.js`
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './movies/**/*.html',
    './movietracker/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'gray': {
          400: '#9ca3af',
          600: '#4b5563',
        },
        'orange': {
          700: '#c2410c',
        },
        'teal': {
          DEFAULT: '#14b8a6',
          // ... extended teal palette
        },
      },
    },
  },
  plugins: [],
}
```

#### `static/css/input.css`
Contains Tailwind directives and custom component styles:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom components for movie cards, buttons, forms, etc. */
```

### Step 6: Build Tailwind CSS
```bash
# Build CSS for development (with watch mode)
npm run dev

# Or build for production (minified)
npm run build-css-prod
```

### Step 7: Django Setup
```bash
# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Step 8: Run the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see your movie tracker!

## 📁 Project Structure

```
movie-tracker/
├── README.md
├── manage.py
├── db.sqlite3
├── package.json                 # npm dependencies and scripts
├── tailwind.config.js          # Tailwind configuration
├── requirements.txt            # Python dependencies (create this)
├── venv/                       # Virtual environment
├── static/
│   ├── css/
│   │   ├── input.css          # Tailwind input file
│   │   └── output.css         # Generated CSS (don't edit)
│   └── js/
├── media/                      # Uploaded movie posters
├── templates/
│   ├── base.html              # Base template with Tailwind
│   └── movies/
│       └── movie_list.html
├── movies/                     # Django app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
└── movietracker/              # Django project
    ├── settings.py
    ├── urls.py
    └── ...
```

## 🎨 Customizing the Design

### Adding New Colors
1. Edit `tailwind.config.js` to add new colors:
```javascript
colors: {
  'custom-blue': '#3b82f6',
  'custom-green': '#10b981',
}
```

2. Rebuild the CSS:
```bash
npm run build-css-prod
```

### Custom Components
Add new component styles in `static/css/input.css`:
```css
@layer components {
  .my-custom-button {
    @apply bg-teal-500 hover:bg-teal-600 text-white px-4 py-2 rounded-lg;
  }
}
```

## 📦 NPM Scripts

The `package.json` includes these useful scripts:

```json
{
  "scripts": {
    "build-css": "tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch",
    "build-css-prod": "tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify",
    "dev": "tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch"
  }
}
```

- `npm run dev` - Build CSS with watch mode for development
- `npm run build-css-prod` - Build minified CSS for production

## 🚀 Deployment

### Preparing for Production

1. **Set DEBUG = False** in Django settings
2. **Configure ALLOWED_HOSTS** in settings.py
3. **Build production CSS**:
   ```bash
   npm run build-css-prod
   ```
4. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

### Environment Variables

Create a `.env` file for sensitive settings:
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

## 🔧 Development Workflow

### Making Style Changes

1. Edit `static/css/input.css` or `tailwind.config.js`
2. Run `npm run dev` to watch for changes
3. Refresh your browser to see updates

### Adding New Features

1. Create Django views, models, templates as usual
2. Use Tailwind classes in your templates
3. Add custom components to `input.css` if needed
4. Rebuild CSS with `npm run build-css-prod`

## 📖 Tailwind CSS Classes Used

### Color Classes (Your Custom Palette)
- `text-gray-400` - Light gray text
- `text-gray-600` - Medium gray text
- `text-orange-700` - Dark orange text
- `bg-teal-500` - Teal background
- `hover:bg-teal-600` - Darker teal on hover

### Layout Classes
- `max-w-7xl mx-auto` - Centered container
- `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4` - Responsive grid
- `flex items-center justify-between` - Flexbox layouts

### Component Classes (Custom)
- `movie-card` - Movie card styling
- `btn-primary` - Primary button style
- `search-form` - Search form container
- `stats-card` - Statistics card

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Build CSS: `npm run build-css-prod`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**CSS not loading:**
- Ensure `output.css` exists in `static/css/`
- Run `npm run build-css-prod`
- Check Django static files configuration

**Tailwind classes not working:**
- Verify content paths in `tailwind.config.js`
- Rebuild CSS after template changes
- Check for typos in class names

**Mobile menu not working:**
- Ensure JavaScript is loaded
- Check browser console for errors

### Getting Help

If you encounter issues:
1. Check the Django debug output
2. Verify all dependencies are installed
3. Ensure virtual environment is activated
4. Check that CSS has been built successfully

## 🔗 Useful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS CLI](https://tailwindcss.com/docs/installation)

---

**Happy Coding!** 🎬✨

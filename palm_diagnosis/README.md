# Palm Diagnosis Platform - منصة تشخيص النخيل

A Django web application for diagnosing palm tree health using AI technology.

## Project Structure

```
palm_diagnosis/
├── palm_diagnosis/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── palm_app/                # Main Django app
│   ├── views.py
│   ├── models.py
│   └── admin.py
├── templates/               # HTML templates
│   ├── index.html
│   └── analyze.html
├── static/                 # Static files
│   ├── css/
│   │   ├── style.css
│   │   └── analyze.css
│   ├── js/
│   │   └── analyze.js
│   └── images/
│       ├── background.png
│       ├── lightning.png
│       ├── pill.png
│       └── ...
├── manage.py
└── requirements.txt
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Features

- **AI-Powered Diagnosis**: Analyze palm tree health using advanced AI technology
- **Real-time Analysis**: Get instant diagnosis results within 3 seconds
- **Image Upload**: Upload images or capture photos directly from your device
- **Detailed Recommendations**: Receive practical treatment recommendations
- **Arabic Interface**: Fully localized Arabic interface

## Usage

1. Visit the homepage to learn about the platform
2. Click "ابدأ التشخيص الآن" (Start Diagnosis Now)
3. Choose to either:
   - Take a photo using your device camera
   - Upload an existing image
4. View the diagnosis results and recommendations

## Development

This project uses Django 4.2+ and follows Django best practices for static file management and template organization.


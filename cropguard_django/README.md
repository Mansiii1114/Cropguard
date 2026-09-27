# CropGuard — Django project (AML)

A Django version of the CropGuard crop-advisor site: real user accounts
(Django auth), a database-backed history, and the same crop-recommendation
and disease-check logic — now running server-side in Python instead of
client-side JavaScript.

## What it covers
- Classification: crop recommendation from soil/weather inputs (top 3 ranked matches) — advisor/crops_data.py
- Classification: symptom-based disease check (top 3 ranked matches) — advisor/disease_data.py
- Regression-style scoring: a 0-100 season risk score per crop
- Django's built-in auth (signup/login/logout) and a RecommendationHistory model

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser. Sign up for an account,
then use the sidebar to reach Crop Recommendation, Disease Check, History
and the Crop Library.

Optional — to view saved history in Django's admin panel:
```bash
python manage.py createsuperuser
```
then visit http://127.0.0.1:8000/admin/

## Project layout
```
cropguard_django/
├── manage.py
├── cropguard_django/       # project settings & urls
├── advisor/                # the app
│   ├── models.py           # RecommendationHistory
│   ├── forms.py            # signup, recommendation, disease forms
│   ├── views.py
│   ├── urls.py
│   ├── crops_data.py        # crop knowledge base + recommendation engine
│   ├── disease_data.py      # symptom rules + classifier
│   ├── templates/advisor/  # all page templates
│   └── static/advisor/     # style.css
└── requirements.txt
```

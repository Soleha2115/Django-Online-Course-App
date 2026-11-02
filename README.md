# Django Online Course App

A small Django application for managing courses and taking course assessments.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the course list and
`http://127.0.0.1:8000/admin/` to add courses, lessons, questions, and choices.

To take an exam, sign in using the **Log in** link, enroll in a course, and submit
answers from its detail page. Each question is all-or-nothing: every correct
choice and no incorrect choice must be selected. A score of 80% is a pass.

## Verify

```bash
python manage.py check
python manage.py test onlinecourse
```

See [SUBMISSION.md](SUBMISSION.md) for the GitHub links and screenshots to submit.
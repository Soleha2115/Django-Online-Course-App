# Project Submission Guide

## 1. Run and prepare the project

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/admin/`, sign in, and add:

1. A course with a name and description.
2. At least one lesson for that course.
3. Questions for that course. Set grades and add at least one correct choice and one incorrect choice to each question. Choices are managed from the question's admin page.

The admin home page should show the Authentication and Authorization and Onlinecourse sections. The exam workflow requires login: use the superuser above, open the course, enroll, submit answers, and review the result. A score of 80% or higher passes.

## 2. Capture screenshots

Save both screenshots in the repository root:

- `03-admin-site.png`: the admin home page showing Authentication and Authorization and Onlinecourse model lists.
- `07-final.png`: the completed exam result page. Select all correct answers and no incorrect answers to pass.

Screenshots are not generated automatically; capture them in your browser after adding the sample data.

## 3. Verify and push

Run the checks, then commit and push to the repository's `main` branch:

```bash
python manage.py check
python manage.py test onlinecourse
git add .gitignore README.md SUBMISSION.md requirements.txt manage.py courseproject onlinecourse
git commit -m "Add course assessment feature"
git push origin main
```

After capturing both screenshots, move them into the repository root, then run:

```bash
git add 03-admin-site.png 07-final.png
git commit -m "Add project submission screenshots"
git push origin main
```

Do not add `.venv/`, `db.sqlite3`, or `__pycache__/`.

## 4. Submit these items

Replace `<your-username>` with your GitHub account name and use the repository's `main` branch:

| Item | Submission |
| --- | --- |
| Task 1 | `https://github.com/<your-username>/Django-Online-Course-App/blob/main/onlinecourse/models.py` |
| Task 2 | `https://github.com/<your-username>/Django-Online-Course-App/blob/main/onlinecourse/admin.py` |
| Task 3 | Upload `03-admin-site.png` |
| Task 4 | `https://github.com/<your-username>/Django-Online-Course-App/blob/main/onlinecourse/templates/onlinecourse/course_detail_bootstrap.html` |
| Task 5 | `https://github.com/<your-username>/Django-Online-Course-App/blob/main/onlinecourse/views.py` |
| Task 6 | `https://github.com/<your-username>/Django-Online-Course-App/blob/main/onlinecourse/urls.py` |
| Task 7 | Upload `07-final.png` |

Also include `onlinecourse/templates/onlinecourse/exam_result_bootstrap.html` in the repository; it renders the Task 7 result screen.
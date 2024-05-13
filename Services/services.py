import random
import string

from flask import session, flash, make_response
from werkzeug.security import check_password_hash, generate_password_hash

from Repositories.repositories import PaperRepository, UserRepository

paper_repo = PaperRepository()
user_repo = UserRepository()


def check_session():
    user_id = session.get('user_id')
    user = user_repo.get_user_by_id(user_id) if user_id else None

    if user_id and user is None:  # End session if user does not exist (eg. deleted user while logged in)
        session.pop('user_id', None)
        user_id = None

    user_role = user.role if user else None
    user_name = user.name if user else None

    return user_id, user_role, user_name


def login_user(email, password):
    user = user_repo.get_user_by_email(email)

    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        return "success"
    else:
        flash('Invalid email or password. Please try again.')


def register_user(name, email, password, confirm_password, role):
    if not is_valid_password(password):
        flash('Password must be at least 8 characters long and contain at least one uppercase letter, '
              'one lowercase letter, one digit, and one special character.')
        return

    if password != confirm_password:
        flash('Passwords do not match. Please try again.')
        return

    if user_repo.get_user_by_email(email):
        flash('Email is already in use. Please use a different email.')
        return

    password_hash = generate_password_hash(password)

    user_repo.create_user(name, email, password_hash, role)
    return "success"


def submit_paper(title, abstract, keywords, is_pdf, file, author_id):
    if not is_pdf:
        flash('File must be a PDF.')
        return

    available_reviewers = user_repo.get_reviewers()
    reviewer = random.choice(available_reviewers) if available_reviewers else None

    if reviewer is None:
        flash('No reviewers available. Please try again later.')
        return

    paper_repo.create_paper(title, abstract, keywords, file, author_id, reviewer.id, None, None)

    flash('Paper uploaded successfully.')


def get_submitted_papers(user_id):
    return paper_repo.get_submitted_papers(user_id)


def get_assigned_papers(user_id):
    return paper_repo.get_assigned_papers(user_id)


def download_pdf_for_reviewer(paper_id):
    pdf_content = paper_repo.get_pdf_content_for_reviewer(paper_id)
    if pdf_content is None:
        flash('PDF not found.')
        return

    # Return PDF content as a downloadable attachment
    response = make_response(pdf_content)
    response.headers['Content-Disposition'] = 'attachment; filename=reviewer_dashboard.pdf'
    response.headers['Content-Type'] = 'application/pdf'
    return response


def get_paper_by_id(paper_id):
    return paper_repo.get_paper_by_id(paper_id)


def review_paper(paper_id, grade, feedback):
    paper_repo.review_paper(paper_id, grade, feedback)


def get_all_papers():
    return paper_repo.get_all_papers()


def get_all_users():
    return user_repo.get_all_users()


def is_valid_password(password):
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in string.punctuation for char in password):
        return False
    return True

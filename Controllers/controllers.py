from flask import Blueprint, request, redirect, url_for, flash, render_template, session

from Services.services import check_session, login_user, register_user, submit_paper, get_submitted_papers, \
    get_assigned_papers, get_paper_by_id, review_paper, download_pdf_for_reviewer, get_all_users, get_all_papers

bp = Blueprint('controllers', __name__)


@bp.route('/')
def home_page():
    user_id, user_role, user_name = check_session()

    return render_template('index.html', user_id=user_id, user_name=user_name, user_role=user_role)


@bp.route('/conferences')
def conference_page():
    user_id, user_role, user_name = check_session()

    return render_template('conferences.html', user_id=user_id, user_name=user_name, user_role=user_role)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    user_id, _, _ = check_session()
    status = None
    if user_id:  # Redirect to home page if user is already logged in
        return redirect(url_for('controllers.home_page'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        status = login_user(email, password)
    if status == "success":
        return redirect(url_for('controllers.home_page'))

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    user_id, _, _ = check_session()
    status = None
    if user_id:  # Redirect to home page if user is already logged in
        return redirect(url_for('controllers.home_page'))

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']

        status = register_user(name, email, password, confirm_password, role)
    if status == "success":
        return redirect(url_for('controllers.login'))

    return render_template('register.html')


@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('controllers.home_page'))


@bp.route('/author/dashboard', methods=['GET', 'POST'])
def author_dashboard():
    user_id, user_role, user_name = check_session()
    if user_role != 'author':  # Redirect to home page if user is not an author
        return redirect(url_for('controllers.home_page'))

    if request.method == 'POST':
        title = request.form['paper_title']
        abstract = request.form['paper_abstract']
        keywords = request.form['paper_keywords']
        is_pdf = request.files['paper_file'].filename.endswith('.pdf')
        file = request.files['paper_file'].read()
        author_id = session['user_id']

        submit_paper(title, abstract, keywords, is_pdf, file, author_id)

    submitted_papers = get_submitted_papers(user_id)

    return render_template('author_dashboard.html', user_name=user_name, submitted_papers=submitted_papers)


@bp.route('/reviewer/dashboard')
def reviewer_dashboard():
    user_id, user_role, user_name = check_session()
    if user_role != 'reviewer':  # Redirect to home page if user is not a reviewer
        return redirect(url_for('controllers.home_page'))

    assigned_papers = get_assigned_papers(user_id)

    return render_template('reviewer_dashboard.html', user_name=user_name, assigned_papers=assigned_papers)


@bp.route('/download_pdf/<int:paper_id>')
def download_pdf(paper_id):
    user_id, user_role, _ = check_session()
    if user_role != 'reviewer':  # Redirect to home page if user is not a reviewer
        return redirect(url_for('controllers.home_page'))

    assigned_papers = get_assigned_papers(user_id)

    if paper_id not in [paper.id for paper in assigned_papers]:  # Redirect to reviewer dashboard if paper is not
        # assigned to reviewer
        flash('You are not assigned to review this paper.')
        return redirect(url_for('controllers.reviewer_dashboard'))

    return download_pdf_for_reviewer(paper_id)


@bp.route('/feedback/<int:paper_id>', methods=['GET', 'POST'])
def feedback_popup(paper_id):
    _, user_role, _ = check_session()
    if user_role != 'reviewer':  # Redirect to home page if user is not a reviewer
        return redirect(url_for('controllers.home_page'))

    paper = get_paper_by_id(paper_id)
    if request.method == 'POST':
        grade = request.form.get('grade')
        feedback = request.form.get('feedback')

        review_paper(paper_id, grade, feedback)

    return render_template('feedback_popup.html', paper_id=paper.id, grade=paper.grade, feedback=paper.feedback)


@bp.route('/set_up_conference')
def conference_setup():
    user_id, user_role, user_name = check_session()
    if user_role != 'organizer':  # Redirect to home page if user is not an organizer
        return redirect(url_for('controllers.home_page'))

    return render_template('conference_setup.html', user_name=user_name, user_id=user_id, user_role=user_role)


@bp.route('/qr_attendee')
def qr_attendee():
    user_id, user_role, user_name = check_session()
    if user_role != 'attendee':
        return redirect(url_for('controllers.home_page'))

    return render_template('qr_attendee.html', user_name=user_name, user_id=user_id, user_role=user_role)


@bp.route('/review_conference')
def conference_review():
    user_id, user_role, user_name = check_session()
    if user_role != 'attendee':
        return redirect(url_for('controllers.home_page'))

    return render_template('conference_review.html', user_name=user_name, user_id=user_id, user_role=user_role)


@bp.route('/conference_register')
def conference_register():
    user_id, user_role, user_name = check_session()
    if user_role != 'attendee':
        return redirect(url_for('controllers.home_page'))

    return render_template('conference_register.html', user_name=user_name, user_id=user_id, user_role=user_role)


@bp.route('/admin')
def admin():
    users = get_all_users()
    papers = get_all_papers()

    return render_template('admin.html', users=users, papers=papers)

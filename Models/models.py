from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    abstract = db.Column(db.Text, nullable=True)
    keywords = db.Column(db.String(100), nullable=True)
    file = db.Column(db.LargeBinary, nullable=False)  # Store PDF data as binary
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grade = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Text, nullable=True)

    author = db.relationship('User', foreign_keys=[author_id],
                                  backref=db.backref('submitted_papers', lazy=True))
    reviewer = db.relationship('User', foreign_keys=[reviewer_id],
                                    backref=db.backref('reviewed_papers', lazy=True))

    def __init__(self, title, abstract, keywords, file, author_id, reviewer_id, grade, feedback):
        self.title = title
        self.abstract = abstract
        self.keywords = keywords
        self.file = file
        self.author_id = author_id
        self.reviewer_id = reviewer_id
        self.grade = grade
        self.feedback = feedback


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(50))  # Role of the user (e.g., 'author' or 'reviewer')

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        self.password_hash = password

    def check_password(self, password):
        return self.password_hash == password

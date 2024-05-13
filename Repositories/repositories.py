from Models.models import Paper, User, db
from Repositories.Irepositories import IPaperRepository, IUserRepository


class PaperRepository(IPaperRepository):
    def create_paper(self, title, abstract, keywords, file, author_id, reviewer_id, grade, feedback):
        paper = Paper(title=title,
                      abstract=abstract,
                      keywords=keywords,
                      file=file,
                      author_id=author_id,
                      reviewer_id=reviewer_id,
                      grade=grade,
                      feedback=feedback)
        db.session.add(paper)
        db.session.commit()
        return paper

    def get_paper_by_id(self, paper_id):
        return Paper.query.get(paper_id)

    def get_assigned_papers(self, reviewer_id):
        return Paper.query.filter_by(reviewer_id=reviewer_id).all()

    def get_submitted_papers(self, author_id):
        return Paper.query.filter_by(author_id=author_id).all()

    def get_pdf_content_for_reviewer(self, paper_id):
        paper = Paper.query.filter_by(id=paper_id).first()
        return paper.file

    def review_paper(self, paper_id, grade, feedback):
        paper = Paper.query.filter_by(id=paper_id).first()
        paper.grade = grade
        paper.feedback = feedback
        db.session.commit()

    def get_all_papers(self):
        return Paper.query.all()


class UserRepository(IUserRepository):
    def create_user(self, name, email, password, role):
        user = User(name=name, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

    def get_reviewers(self):
        return User.query.filter_by(role='reviewer').all()

    def get_all_users(self):
        return User.query.all()

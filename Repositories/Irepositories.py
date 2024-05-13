from abc import ABC, abstractmethod


class IPaperRepository(ABC):
    @abstractmethod
    def create_paper(self, title, abstract, keywords, file, author_id, reviewer_id, grade, feedback):
        pass

    @abstractmethod
    def get_paper_by_id(self, paper_id):
        pass

    @abstractmethod
    def get_assigned_papers(self, reviewer_id):
        pass

    def get_submitted_papers(self, author_id):
        pass

    @abstractmethod
    def get_pdf_content_for_reviewer(self, paper_id):
        pass

    @abstractmethod
    def review_paper(self, paper_id, grade, feedback):
        pass

    @abstractmethod
    def get_all_papers(self):
        pass


class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, name, email, password, role):
        pass

    @abstractmethod
    def get_user_by_email(self, email):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def get_reviewers(self):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

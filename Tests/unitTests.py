import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from werkzeug.security import generate_password_hash

from Services import services

app = Flask(__name__)


class TestServices(unittest.TestCase):

    @patch('Services.services.user_repo')
    def test_check_session(self, mock_user_repo):
        # Test when user_id is None
        services.session = {'user_id': None}
        self.assertEqual(services.check_session(), (None, None, None))

        # Test when user_id is not None but user does not exist
        mock_user_repo.get_user_by_id.return_value = None
        services.session = {'user_id': 1}
        self.assertEqual(services.check_session(), (None, None, None))

        # Test when user_id is not None and user exists
        mock_user = MagicMock()
        mock_user.role = 'test_role'
        mock_user.name = 'test_name'
        mock_user_repo.get_user_by_id.return_value = mock_user
        services.session = {'user_id': 1}
        self.assertEqual(services.check_session(), (1, 'test_role', 'test_name'))

    @patch('Services.services.user_repo')
    @patch('Services.services.flash')
    def test_login_user(self, mock_flash, mock_user_repo):
        # Test when user does not exist
        mock_user_repo.get_user_by_email.return_value = None
        self.assertEqual(services.login_user('test@test.com', 'password'), None)

        # Test when user exists but password is incorrect
        mock_user = MagicMock()
        mock_user.password_hash = 'incorrect_hash'
        mock_user_repo.get_user_by_email.return_value = mock_user
        self.assertEqual(services.login_user('test@test.com', 'password'), None)

        # Test when user exists and password is correct
        with app.test_request_context():
            mock_user.password_hash = generate_password_hash('password')
            mock_user.email = 'test@test.com'
            mock_user_repo.get_user_by_email.return_value = mock_user
            self.assertEqual(services.login_user('test@test.com', 'password'), 'success')

    @patch('Services.services.user_repo')
    @patch('Services.services.flash')
    def test_register_user(self, mock_flash, mock_user_repo):
        # Test when email is already in use
        mock_user_repo.get_user_by_email.return_value = MagicMock()
        self.assertEqual(services.register_user('test', 'test@test.com', 'Password1!', 'Password1!', 'role'), None)

        # Test when email is not in use
        mock_user_repo.get_user_by_email.return_value = None
        self.assertEqual(services.register_user('test', 'test@test.com', 'Password1!', 'Password1!', 'role'), 'success')

    @patch('Services.services.paper_repo')
    @patch('Services.services.user_repo')
    @patch('Services.services.flash')
    def test_submit_paper(self, mock_flash, mock_user_repo, mock_paper_repo):
        # Test when file is not a PDF
        self.assertEqual(services.submit_paper('title', 'abstract', 'keywords', False, 'file', 1), None)

        # Test when file is a PDF but no reviewers are available
        mock_user_repo.get_reviewers.return_value = []
        self.assertEqual(services.submit_paper('title', 'abstract', 'keywords', True, 'file', 1), None)

        # Test when file is a PDF and reviewers are available
        mock_user_repo.get_reviewers.return_value = [MagicMock()]
        self.assertEqual(services.submit_paper('title', 'abstract', 'keywords', True, 'file', 1), None)

    @patch('Services.services.paper_repo')
    def test_get_submitted_papers(self, mock_paper_repo):
        # Test when user has no assigned papers
        mock_paper_repo.get_assigned_papers.return_value = []
        self.assertEqual(services.get_assigned_papers(1), [])

        # Test when user has assigned papers
        mock_paper_repo.get_assigned_papers.return_value = [MagicMock()]
        self.assertEqual(len(services.get_assigned_papers(1)), 1)

    @patch('Services.services.paper_repo')
    def test_get_assigned_papers(self, mock_paper_repo):
        # Test when user has no assigned papers
        mock_paper_repo.get_assigned_papers.return_value = []
        self.assertEqual(services.get_assigned_papers(1), [])

        # Test when user has assigned papers
        mock_paper_repo.get_assigned_papers.return_value = [MagicMock()]
        self.assertEqual(len(services.get_assigned_papers(1)), 1)

    @patch('Services.services.flash')
    @patch('Services.services.paper_repo')
    def test_download_pdf_for_reviewer(self, mock_paper_repo, mock_flash):
        with app.test_request_context():
            # Test when PDF does not exist
            mock_paper_repo.get_pdf_content_for_reviewer.return_value = None
            self.assertEqual(services.download_pdf_for_reviewer(1), None)

            # Test when PDF exists
            mock_paper_repo.get_pdf_content_for_reviewer.return_value = b'pdf_content'
            self.assertEqual(services.download_pdf_for_reviewer(1).get_data(), b'pdf_content')

    @patch('Services.services.paper_repo')
    def test_get_paper_by_id(self, mock_paper_repo):
        # Test when paper does not exist
        mock_paper_repo.get_paper_by_id.return_value = None
        self.assertEqual(services.get_paper_by_id(1), None)

        # Test when paper exists
        mock_paper_repo.get_paper_by_id.return_value = MagicMock()
        self.assertIsNotNone(services.get_paper_by_id(1))

    @patch('Services.services.paper_repo')
    def test_review_paper(self, mock_paper_repo):
        # Test review_paper function (no return value to check)
        services.review_paper(1, 'grade', 'feedback')

    @patch('Services.services.paper_repo')
    def test_get_all_papers(self, mock_paper_repo):
        # Test when there are no papers
        mock_paper_repo.get_all_papers.return_value = []
        self.assertEqual(services.get_all_papers(), [])

        # Test when there are papers
        mock_paper_repo.get_all_papers.return_value = [MagicMock()]
        self.assertEqual(len(services.get_all_papers()), 1)

    @patch('Services.services.user_repo')
    def test_get_all_users(self, mock_user_repo):
        # Test when there are no users
        mock_user_repo.get_all_users.return_value = []
        self.assertEqual(services.get_all_users(), [])

        # Test when there are users
        mock_user_repo.get_all_users.return_value = [MagicMock()]
        self.assertEqual(len(services.get_all_users()), 1)

    def test_is_valid_password(self):
        # Test when password is not valid
        self.assertFalse(services.is_valid_password('password'))

        # Test when password is valid
        self.assertTrue(services.is_valid_password('Password1!'))


if __name__ == '__main__':
    unittest.main()

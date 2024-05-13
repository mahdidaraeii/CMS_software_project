# Conference Management System

This is a comprehensive Conference Management System designed to facilitate the organization of academic, professional, and corporate conferences. The system automates various aspects of conference management, from initial setup to post-event analysis.

## Features

- **User Registration and Management**: Supports multiple user roles with different access rights.
- **Conference Setup and Management**: Customizable details such as title, venue, dates, and schedules.
- **Call for Papers**: Online submission portal for authors including abstracts and file uploads.
- **Review and Selection Process**: Double-blind review system with automatic and manual paper assignments.
- **Program Scheduling**: Organize sessions based on themes, topics, or presentation types.
- **Registration and Payments**: Online registration and payment portal for attendees.
- **On-site Management**: Fast check-in process using QR codes or NFC technology.
- **Post-Conference Features**: Feedback collection, survey, and analytics for event assessment.

## Implemented Feature

- **Paper Submission and Review Assignment**: Users can submit papers, which are automatically assigned to reviewers for review.

## Project Structure

- **Controllers**: Contains the controllers for handling HTTP requests.
- **Models**: Defines the database models using SQLAlchemy.
- **Repositories**: Data access layer for interacting with the database.
- **Services**: Business logic layer for implementing the system's functionalities.
- **Tests**: Unit tests for ensuring code quality and reliability.
- **Instance**: Configuration files for development and production environments.
- **Static**: Static files such as CSS, JavaScript, and images.
- **Templates**: HTML templates for rendering views.
- **app.py**: Main entry point of the application.
- **requirements.txt**: List of dependencies for easy environment setup.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>

2. Navigate to the project directory:

   ```bash
   cd <directory_path>

3. Install dependencies:

   ```bash
   pip install -r requirements.txt

4. Run the application:

   ```bash
   python app.py


## Contributing

Contributions are welcome! If you have suggestions, feature requests, or bug reports, please open an issue or submit a pull request.

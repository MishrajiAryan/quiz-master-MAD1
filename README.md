# Quiz Quest MAD1 - Multi-User Exam Preparation Platform

## Summary
Quiz Quest is a comprehensive multi-user exam preparation application that enables administrators to create and manage quizzes while providing users with an intuitive platform to attempt quizzes and track their performance. Built with Flask, Jinja2, HTML, CSS, Bootstrap, and SQLite, it offers a complete solution for effective learning and assessment.

## Features
- **Admin Dashboard**: Complete quiz management system for administrators
- **User Management**: Multi-user support with secure authentication
- **Quiz Creation**: Intuitive interface for creating and editing quizzes
- **Quiz Participation**: User-friendly quiz-taking experience
- **Score Tracking**: Comprehensive scoring and performance analytics
- **Real-time Results**: Instant feedback and score calculation
- **Database Integration**: SQLite database for reliable data storage
- **Responsive Design**: Bootstrap-powered responsive UI
- **Template Engine**: Jinja2 templating for dynamic content
- **Session Management**: Secure user session handling

## Usage
1. **Admin Workflow**:
   - Register/login as an administrator
   - Access the admin dashboard
   - Create new quizzes with questions and answers
   - Manage user accounts and quiz settings
   - View analytics and user performance

2. **User Experience**:
   - Register/login to access the platform
   - Browse available quizzes
   - Attempt quizzes with timed sessions
   - View instant results and feedback
   - Track performance history

3. **Quiz Management**:
   - Create multiple-choice, true/false, or text-based questions
   - Set quiz parameters (time limits, attempts, difficulty)
   - Monitor user progress and generate reports

## Tech Stack
- **Backend Framework**: Flask (Python)
- **Template Engine**: Jinja2
- **Frontend**: HTML5, CSS3, Bootstrap
- **Database**: SQLite
- **Language**: Python (37.5%), HTML (62.5%)
- **Architecture**: MVC pattern with Flask
- **Development Tools**: VS Code configuration included

## Installation & Setup
```bash
# Clone the repository
git clone https://github.com/MishrajiAryan/quiz-master-MAD1.git

# Navigate to project directory
cd quiz-master-MAD1

# Navigate to code directory
cd code

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database (if needed)
python init_db.py

# Run the Flask application
python app.py
# OR
flask run

# Access the application at http://localhost:5000
```

## Project Structure
```
quiz-master-MAD1/
├── .vscode/                # VS Code configuration
├── __pycache__/            # Python cache files
├── code/                   # Main application code
│   ├── app.py              # Flask application entry point
│   ├── models.py           # Database models
│   ├── routes.py           # Application routes
│   ├── templates/          # Jinja2 templates
│   ├── static/             # CSS, JS, images
│   └── database.db         # SQLite database
├── MAD-1 Report (21f2000307).pdf  # Project documentation
└── README.md              # Project documentation
```

## Features in Detail

### Authentication & Authorization
- Secure user registration and login
- Role-based access control (Admin/User)
- Session management and security
- Password hashing and validation

### Quiz Management
- Create, edit, and delete quizzes
- Add multiple question types
- Set quiz parameters and constraints
- Bulk question import/export

### User Experience
- Responsive Bootstrap UI
- Real-time quiz timer
- Progress tracking during quizzes
- Immediate result feedback
- Personal performance dashboard

### Database Design
- SQLite database with optimized schema
- User, Quiz, Question, and Result tables
- Foreign key relationships for data integrity
- Efficient querying and indexing

## API Endpoints
(Flask routes)
- `GET /` - Home page
- `GET /login` - User login page
- `POST /login` - Process login
- `GET /register` - User registration
- `POST /register` - Process registration
- `GET /dashboard` - User dashboard
- `GET /quiz/<id>` - Quiz details
- `POST /quiz/<id>/submit` - Submit quiz answers
- `GET /admin` - Admin dashboard
- `POST /admin/quiz/create` - Create new quiz

## Requirements
- Python 3.7+
- Flask 2.0+
- SQLite3
- Bootstrap 4/5
- Modern web browser
- Jinja2 template engine

## Development Setup
1. Install Python dependencies from requirements.txt
2. Set up SQLite database with initial schema
3. Configure Flask environment variables
4. Run database migrations if needed
5. Start the Flask development server

## Testing
```bash
# Run unit tests (if available)
python -m pytest tests/

# Run with coverage
python -m pytest --cov=app tests/
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Documentation
Detailed project documentation is available in `MAD-1 Report (21f2000307).pdf` which includes:
- System architecture and design
- Database schema and relationships
- User interface mockups
- Implementation details
- Testing and deployment guide

## Screenshots
(Add screenshots of the application here)
- Login/Registration pages
- User dashboard
- Quiz interface
- Admin panel
- Results page

## License
This project is developed as part of academic coursework (MAD1 - Modern Application Development).

## Contact
**Developer**: Aryan Mishra  
**Student ID**: 21f2000307  
**GitHub**: [@MishrajiAryan](https://github.com/MishrajiAryan)  
**Repository**: [quiz-master-MAD1](https://github.com/MishrajiAryan/quiz-master-MAD1)

---
*Built with ❤️ using Flask, Jinja2, and Bootstrap as part of Modern Application Development (MAD1) coursework*

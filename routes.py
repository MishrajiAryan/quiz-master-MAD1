from app import app

from api import api_bp
from api.admin import admin_bp
from api.auth import auth_bp
from api.chapter import chapter_bp
from api.question import question_bp
from api.quiz import quiz_bp
from api.subject import subject_bp
from api.user import user_bp

# API blueprint
app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(chapter_bp, url_prefix="/api/chapter")
app.register_blueprint(question_bp, url_prefix="/api/question")
app.register_blueprint(quiz_bp, url_prefix="/api/quiz")
app.register_blueprint(subject_bp, url_prefix="/api/subject")
app.register_blueprint(user_bp, url_prefix="/api/user")
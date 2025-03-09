from app import app

from controllers.api.admin import admin_bp
from controllers.api.auth import auth_bp
from controllers.api.chapter import chapter_bp
from controllers.api.question import question_bp
from controllers.api.quiz import quiz_bp
from controllers.api.subject import subject_bp
from controllers.api.user import user_bp

# Register individual blueprints
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(auth_bp, url_prefix="/")
app.register_blueprint(chapter_bp, url_prefix="/chapter")
app.register_blueprint(question_bp, url_prefix="/question")
app.register_blueprint(quiz_bp, url_prefix="/quiz")
app.register_blueprint(subject_bp, url_prefix="/subject")
app.register_blueprint(user_bp, url_prefix="/user")

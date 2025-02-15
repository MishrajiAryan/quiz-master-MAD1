from flask import Blueprint

# Importing API Modules
from .admin import admin_bp
from .auth import auth_bp
from .chapter import chapter_bp
from .question import question_bp
from .quiz import quiz_bp
from .subject import subject_bp
from .user import user_bp

# Main Blueprint to group all API routes
api_bp = Blueprint("api", __name__) # Add __name__ for better blueprint handling

# Register individual blueprints ONLY with the main api_bp
api_bp.register_blueprint(admin_bp, url_prefix="/admin")
api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(chapter_bp, url_prefix="/chapter")
api_bp.register_blueprint(question_bp, url_prefix="/question")
api_bp.register_blueprint(quiz_bp, url_prefix="/quiz")
api_bp.register_blueprint(subject_bp, url_prefix="/subject")
api_bp.register_blueprint(user_bp, url_prefix="/user")



from .register import register_bp
from .login import login_bp
from .refresh import refresh_bp
from .logout import logout_bp
from .user import user_bp
from .forget_password import forget_password_bp
from .reset_password import reset_password_bp



def init_auth_blueprints(app):
    app.register_blueprint(register_bp, url_prefix="/auth")
    app.register_blueprint(login_bp, url_prefix="/auth")
    app.register_blueprint(refresh_bp, url_prefix="/auth")
    app.register_blueprint(logout_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/auth")
    app.register_blueprint(forget_password_bp, url_prefix='/auth')
    app.register_blueprint(reset_password_bp, url_prefix='/auth')

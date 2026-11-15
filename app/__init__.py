import os
import secrets
from datetime import date, time, timedelta
from flask import Flask, session, request, abort
from flask_login import LoginManager
from .models import db, User, Client, Service, Settings, Appointment


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or secrets.token_hex(32),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///beleza.sqlite3'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )
    if config:
        app.config.update(config)
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)
    login = LoginManager(app)
    login.login_view = 'main.login'
    login.login_message = 'Entre para acessar o sistema.'
    login.login_message_category = 'error'

    @login.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    def csrf_token():
        if '_csrf' not in session:
            session['_csrf'] = secrets.token_urlsafe(32)
        return session['_csrf']

    app.jinja_env.globals['csrf_token'] = csrf_token

    @app.before_request
    def protect():
        if request.method == 'POST' and not app.config.get('TESTING'):
            expected = session.get('_csrf', '')
            received = request.form.get('_csrf', '')
            if not expected or not secrets.compare_digest(expected, received):
                abort(400, description='Formulário expirado. Recarregue a página.')

    from .routes import main
    app.register_blueprint(main)

    @app.cli.command('init-db')
    def init_db():
        db.create_all()
        if not User.query.first():
            user = User(username=os.environ.get('DEMO_USERNAME', 'funcionario'))
            user.set_password(os.environ.get('DEMO_PASSWORD', 'beleza123'))
            db.session.add(user)
        if not Settings.query.first():
            db.session.add(Settings(opening=time(9), closing=time(18)))
        if not Service.query.first():
            db.session.add_all([Service(name='Corte Feminino', duration=60), Service(name='Escova', duration=45), Service(name='Manicure', duration=60)])
        if not Client.query.first():
            db.session.add_all([Client(name=n) for n in ['Ana Souza', 'Carla Mendes', 'Juliana Alves']])
        db.session.commit()
        if not Appointment.query.first():
            clients = Client.query.order_by(Client.id).all()
            services = Service.query.order_by(Service.id).all()
            if len(clients) >= 3 and len(services) >= 3:
                tomorrow = date.today() + timedelta(days=1)
                for c, s, h in zip(clients[:3], services[:3], [10, 13, 15]):
                    db.session.add(Appointment(client_id=c.id, service_id=s.id, date=tomorrow, start=time(h), duration=s.duration))
                db.session.commit()
        print('Banco inicializado. Dados demonstrativos disponíveis.')

    return app

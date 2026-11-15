from datetime import date, datetime, time, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from .models import db, User, Client, Service, Appointment, Settings
from .domain import overlap, within_hours, parse_date, parse_time

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username', '').strip()).first()
        if user and user.check_password(request.form.get('password', '')):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Usuário ou senha inválidos.', 'error')
    return render_template('login.html')

@main.post('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.get('/')
@login_required
def home():
    today = date.today()
    active = Appointment.query.filter(Appointment.status != 'Cancelado')
    count = active.filter_by(date=today).count()
    now = datetime.now()
    next_item = active.filter(or_(Appointment.date > today, (Appointment.date == today) & (Appointment.start >= now.time()))).order_by(Appointment.date, Appointment.start).first()
    return render_template('home.html', count=count, next_item=next_item)

@main.get('/agendamentos')
@login_required
def appointments():
    tab = request.args.get('tab', 'day')
    if tab not in ('day', 'next', 'cancelled'):
        tab = 'day'
    try:
        selected = parse_date(request.args.get('date', date.today().isoformat()))
    except ValueError:
        selected = date.today()
    search = request.args.get('q', '').strip()
    query = Appointment.query.join(Client).join(Service)
    if tab == 'cancelled':
        query = query.filter(Appointment.status == 'Cancelado')
    elif tab == 'next':
        query = query.filter(Appointment.status != 'Cancelado', Appointment.date >= date.today())
    else:
        query = query.filter(Appointment.status != 'Cancelado', Appointment.date == selected)
    if search:
        query = query.filter(or_(Client.name.contains(search, autoescape=True), Service.name.contains(search, autoescape=True)))
    items = query.order_by(Appointment.date, Appointment.start).all()
    return render_template('appointments.html', items=items, tab=tab, selected=selected, search=search)


def conflict(day, start, duration, exclude=None):
    query = Appointment.query.filter(Appointment.date == day, Appointment.status != 'Cancelado')
    if exclude:
        query = query.filter(Appointment.id != exclude)
    return any(overlap(start, duration, other.start, other.duration) for other in query.all())

@main.route('/agendamentos/novo', methods=['GET', 'POST'])
@main.route('/agendamentos/<int:item_id>/editar', methods=['GET', 'POST'])
@login_required
def appointment_form(item_id=None):
    item = db.get_or_404(Appointment, item_id) if item_id else None
    if item and item.status == 'Cancelado':
        flash('Agendamento cancelado não pode ser editado. Crie um novo.', 'error')
        return redirect(url_for('main.appointments', tab='cancelled'))
    settings = Settings.query.first()
    values = {'client_id': item.client_id if item else '', 'service_id': item.service_id if item else '', 'date': item.date.isoformat() if item else date.today().isoformat(), 'start': item.start.strftime('%H:%M') if item else '', 'notes': item.notes if item else ''}
    if request.method == 'POST':
        values.update(request.form.to_dict())
        try:
            client = db.session.get(Client, int(values['client_id']))
            service = db.session.get(Service, int(values['service_id']))
            day = parse_date(values['date'])
            start = parse_time(values['start'])
            if not client or not service:
                raise ValueError('Selecione cliente e serviço válidos.')
            if day < date.today():
                raise ValueError('Não é possível agendar em uma data passada.')
            if not settings or not within_hours(start, service.duration, settings.opening, settings.closing):
                raise ValueError('Horário fora do expediente do salão.')
            if conflict(day, start, service.duration, item_id):
                raise ValueError('Horário indisponível: existe outro atendimento nesse intervalo.')
            target = item or Appointment(status='Agendado')
            target.client_id, target.service_id = client.id, service.id
            target.date, target.start, target.duration = day, start, service.duration
            target.notes = values.get('notes', '').strip()[:1000]
            db.session.add(target)
            db.session.commit()
            flash(f'{"Agendamento atualizado" if item else "Agendamento realizado"} com sucesso! Cliente: {client.name} | Serviço: {service.name} | Data: {day:%d/%m/%Y} | Horário: {start:%H:%M}', 'success')
            return redirect(url_for('main.appointments', date=day.isoformat()))
        except (ValueError, KeyError, TypeError) as e:
            db.session.rollback()
            flash(str(e) if isinstance(e, ValueError) else 'Preencha os campos obrigatórios.', 'error')
    return render_template('appointment_form.html', item=item, values=values, clients=Client.query.order_by(Client.name).all(), services=Service.query.order_by(Service.name).all(), today=date.today().isoformat())

@main.get('/api/horarios')
@login_required
def slots():
    try:
        day = parse_date(request.args['date'])
        service = db.session.get(Service, int(request.args['service_id']))
        exclude = request.args.get('exclude', type=int)
        if not service or day < date.today():
            return jsonify([])
        settings = Settings.query.first()
        if not settings:
            return jsonify([])
        cursor = datetime.combine(day, settings.opening)
        end = datetime.combine(day, settings.closing)
        options = []
        while cursor + timedelta(minutes=service.duration) <= end:
            start = cursor.time()
            options.append({'time': start.strftime('%H:%M'), 'available': not conflict(day, start, service.duration, exclude)})
            cursor += timedelta(minutes=30)
        return jsonify(options)
    except (KeyError, ValueError, TypeError):
        return jsonify([]), 400

@main.post('/agendamentos/<int:item_id>/cancelar')
@login_required
def cancel(item_id):
    item = db.get_or_404(Appointment, item_id)
    item.status = 'Cancelado'
    db.session.commit()
    flash('Agendamento cancelado com sucesso.', 'success')
    return redirect(url_for('main.appointments', date=item.date.isoformat()))

@main.post('/agendamentos/<int:item_id>/confirmar')
@login_required
def confirm(item_id):
    item = db.get_or_404(Appointment, item_id)
    if item.status == 'Agendado':
        item.status = 'Confirmado'
        db.session.commit()
        flash('Atendimento confirmado.', 'success')
    return redirect(url_for('main.appointments', date=item.date.isoformat()))

@main.route('/clientes', methods=['GET', 'POST'])
@main.route('/clientes/<int:client_id>/editar', methods=['GET', 'POST'])
@login_required
def clients(client_id=None):
    client = db.get_or_404(Client, client_id) if client_id else None
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name or len(name) > 120:
            flash('Informe um nome válido (até 120 caracteres).', 'error')
        else:
            target = client or Client()
            target.name = name
            target.phone = request.form.get('phone', '').strip()[:30]
            target.email = request.form.get('email', '').strip()[:120]
            db.session.add(target)
            db.session.commit()
            flash('Cliente salvo com sucesso.', 'success')
            return redirect(url_for('main.clients'))
    return render_template('clients.html', client=client, clients=Client.query.order_by(Client.name).all())

@main.route('/configuracoes', methods=['GET', 'POST'])
@login_required
def settings():
    settings = Settings.query.first()
    if request.method == 'POST':
        try:
            if request.form.get('action') == 'hours':
                opening = parse_time(request.form['opening'])
                closing = parse_time(request.form['closing'])
                if opening >= closing:
                    raise ValueError('A abertura deve ser anterior ao fechamento.')
                target = settings or Settings()
                target.opening, target.closing = opening, closing
                db.session.add(target)
            else:
                name = request.form.get('name', '').strip()
                duration = int(request.form.get('duration', '0'))
                if not name or len(name) > 120 or not 5 <= duration <= 720:
                    raise ValueError('Informe nome e duração de 5 a 720 minutos.')
                db.session.add(Service(name=name, duration=duration))
            db.session.commit()
            flash('Configuração salva com sucesso.', 'success')
            return redirect(url_for('main.settings'))
        except (ValueError, KeyError, IntegrityError):
            db.session.rollback()
            flash('Dados inválidos ou serviço já cadastrado.', 'error')
    return render_template('settings.html', settings=settings, services=Service.query.order_by(Service.name).all())

from datetime import date, timedelta
import pytest

@pytest.fixture
def app():
    from app import create_app
    application = create_app({'TESTING':True, 'SECRET_KEY':'test-only', 'SQLALCHEMY_DATABASE_URI':'sqlite:///:memory:'})
    result = application.test_cli_runner().invoke(args=['init-db'])
    assert result.exit_code == 0, result.output
    yield application
    from app.models import db
    with application.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    c = app.test_client()
    c.post('/login', data={'username':'funcionario','password':'beleza123'})
    return c

def test_login_required(app):
    assert app.test_client().get('/agendamentos').status_code == 302

def test_login_invalid(app):
    response = app.test_client().post('/login', data={'username':'funcionario','password':'wrong'})
    assert 'inválidos' in response.get_data(as_text=True)

def test_crud_and_conflict(client, app):
    from app.models import Appointment
    day = (date.today()+timedelta(days=5)).isoformat()
    data = {'client_id':'1','service_id':'1','date':day,'start':'10:00','notes':'Teste'}
    result=client.post('/agendamentos/novo',data=data,follow_redirects=True)
    assert 'Agendamento realizado com sucesso' in result.get_data(as_text=True)
    response=client.post('/agendamentos/novo',data={**data,'start':'10:30'},follow_redirects=True)
    assert 'Horário indisponível' in response.get_data(as_text=True)
    with app.app_context():
        item=Appointment.query.filter_by(notes='Teste').first()
        item_id=item.id
    response=client.post(f'/agendamentos/{item_id}/editar',data={**data,'start':'11:00'},follow_redirects=True)
    assert 'Agendamento atualizado com sucesso' in response.get_data(as_text=True)
    assert client.post(f'/agendamentos/{item_id}/confirmar').status_code==302
    assert client.post(f'/agendamentos/{item_id}/cancelar').status_code==302
    with app.app_context():
        assert Appointment.query.filter_by(id=item_id).first().status=='Cancelado'
    assert 'Cancelado' in client.get('/agendamentos?tab=cancelled').get_data(as_text=True)
    assert client.post('/agendamentos/novo',data={**data,'start':'11:00'}).status_code==302

def test_client_registration(client):
    response=client.post('/clientes',data={'name':'Pessoa Teste','phone':'11999999999','email':'teste@example.com'},follow_redirects=True)
    assert 'Pessoa Teste' in response.get_data(as_text=True)

def test_slot_endpoint(client):
    tomorrow=(date.today()+timedelta(days=1)).isoformat()
    response=client.get(f'/api/horarios?date={tomorrow}&service_id=1')
    assert response.status_code==200
    assert any(s['time']=='10:00' and not s['available'] for s in response.json)

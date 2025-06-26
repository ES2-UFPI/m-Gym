import pytest
import base64
from fastapi.testclient import TestClient
from fastapi import status
from src.models.user import User
from src.auth import get_password_hash
from src.database import get_db
from src.auth import get_password_hash
from src.server import app
# Assumindo que a rota /login já esteja incluída no app principal
LOGIN_URL = "/login"
URL = "/usuarios"

# POST USUARIO
def test_register_user(client):
    response = client.post("/usuarios", json={
        "login": "usuario_teste",
        "email": "teste@example.com",
        "password": "senha123"
    })
    assert response.status_code == 201


def test_criar_usuario_sucesso(client, db_session):
    payload = {
        "login": "novousuario",
        "email": "novo@example.com",
        "password": "senha123",
        "photo": None
    }

    response = client.post(URL, json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data["message"] == "Usuário criado com sucesso!"
    assert data["usuario"]["email"] == "novo@example.com"
    assert data["usuario"]["login"] == "novousuario"
    assert "id" in data["usuario"]


def test_criar_usuario_email_duplicado(client, db_session):
    # Inserir manualmente usuário duplicado no banco
    usuario = User(
        login="repetido",
        email="repetido@example.com",
        password=get_password_hash("senha123"),
        photo=None
    )
    db_session.add(usuario)
    db_session.commit()

    payload = {
        "login": "repetido2",
        "email": "repetido@example.com",
        "password": "senha123",
        "photo": None
    }

    response = client.post(URL, json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "E-mail já cadastrado."


def test_criar_usuario_dados_invalidos(client):
    payload = {
        "login": "",
        "email": "email-invalido",
        "password": "123",
    }

    response = client.post(URL, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

# POST LOGIN
@pytest.fixture
def create_user(db_session):
    from src.models.user import User  # ajuste conforme seu projeto
    from src.auth import get_password_hash

    user = User(
        login="testuser",
        email="testuser@example.com",
        password=get_password_hash("strongpassword"),
        photo=None,
        bio="Test bio",
        pontuacao=42
    )
    db_session.add(user)
    db_session.commit()
    return user


def test_login_success(client, create_user):
    payload = {
        "email": "testuser@example.com",
        "password": "strongpassword"
    }

    response = client.post(LOGIN_URL, json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["usuario"]["email"] == "testuser@example.com"
    assert data["usuario"]["login"] == "testuser"
    assert data["usuario"]["pontuacao"] == 42
    assert data["usuario"]["photo"] is None


def test_login_invalid_credentials(client):
    payload = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = client.post(LOGIN_URL, json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Credenciais inválidas"


def test_login_missing_fields(client):
    # Missing password
    payload = {
        "email": "testuser@example.com"
    }

    response = client.post(LOGIN_URL, json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
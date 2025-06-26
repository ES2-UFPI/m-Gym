import pytest
from fastapi.testclient import TestClient
from datetime import date, timedelta
from sqlalchemy.orm import Session
from src.server import app
from src.models.user import User
from src.models.challenge import Challenge
from src.auth import create_access_token, get_password_hash
from src.database import get_db

client = TestClient(app)

# POST DESAFIOS
def criar_usuario_para_testes(db_session: Session):
    usuario = User(
        login="criador",
        email="criador@desafio.com",
        password=get_password_hash("senha123")
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario


def criar_token_para(usuario: User):
    return create_access_token({"sub": usuario.email})


@pytest.mark.parametrize("dias_inicio,dias_fim,pontos,esperado", [
    (1, 3, 50, 201),            # sucesso
    (5, 2, 50, 400),            # data início > fim
    (-1, 5, 50, 400),           # data início no passado
    (1, 5, -10, 422),           # pontos negativos
])
def test_criar_desafio_casos(client: TestClient, db_session: Session, dias_inicio, dias_fim, pontos, esperado):
    usuario = criar_usuario_para_testes(db_session)
    token = criar_token_para(usuario)

    payload = {
        "title": "Desafio Teste",
        "description": "Testando criação de desafio",
        "start_date": str(date.today() + timedelta(days=dias_inicio)),
        "end_date": str(date.today() + timedelta(days=dias_fim)),
        "points": pontos
    }

    response = client.post(
        "/desafios",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == esperado

    if esperado == 201:
        data = response.json()
        assert data["message"] == "Desafio criado com sucesso!"
        assert data["desafio"]["title"] == payload["title"]
        assert data["desafio"]["points"] == pontos


def test_criar_desafio_payload_invalido(client: TestClient, db_session: Session):
    usuario = criar_usuario_para_testes(db_session)
    token = criar_token_para(usuario)

    payload = {
        "title": "",  # Título vazio, inválido
        "description": "A" * 300,  # Muito longa
        "start_date": "2024-01-01",
        "end_date": "2024-01-02",
        "points": "não é inteiro"
    }

    response = client.post(
        "/desafios",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422  # erro de validação do Pydantic


def test_criar_desafio_sem_autenticacao(client: TestClient):
    payload = {
        "title": "Desafio sem auth",
        "description": "Descrição",
        "start_date": str(date.today() + timedelta(days=1)),
        "end_date": str(date.today() + timedelta(days=2)),
        "points": 10
    }

    response = client.post("/desafios", json=payload)
    assert response.status_code in (401, 403)
    assert "detail" in response.json()

# GET DESAFIO
def criar_usuario(db: Session, email="user@teste.com"):
    usuario = User(
        login="usuarioteste",
        email=email,
        password=get_password_hash("senha123")
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def criar_token(usuario: User):
    return create_access_token({"sub": usuario.email})

def criar_desafio(db: Session, usuario_id: int, titulo: str):
    desafio = Challenge(
        title=titulo,
        description="Descrição teste",
        start_date=date.today() + timedelta(days=1),
        end_date=date.today() + timedelta(days=5),
        points=100,
        creator_id=usuario_id
    )
    db.add(desafio)
    db.commit()
    db.refresh(desafio)
    return desafio

def test_listar_desafios_sucesso(client: TestClient, db_session: Session):
    usuario = criar_usuario(db_session)
    token = criar_token(usuario)

    desafio1 = criar_desafio(db_session, usuario.id, "Desafio A")
    desafio2 = criar_desafio(db_session, usuario.id, "Desafio B")

    response = client.get(
        "/desafios",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Pode haver outros desafios
    assert any(d["title"] == "Desafio A" for d in data)
    assert any(d["title"] == "Desafio B" for d in data)

def test_listar_desafios_vazio(client: TestClient, db_session: Session):
    usuario = criar_usuario(db_session)
    token = criar_token(usuario)

    response = client.get(
        "/desafios",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == []

def test_listar_desafios_sem_autenticacao(client: TestClient):
    response = client.get("/desafios")
    assert response.status_code in (401, 403)

def test_listar_desafios_token_invalido(client: TestClient):
    response = client.get(
        "/desafios",
        headers={"Authorization": "Bearer token_invalido"}
    )
    assert response.status_code in (401, 403)
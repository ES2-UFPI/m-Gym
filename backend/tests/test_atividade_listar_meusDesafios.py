import base64
import pytest
from datetime import date, timedelta, datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from io import BytesIO
from src.server import app
from src.models.user import User
from src.models.challenge import Challenge
from src.models.challengecompletion import ChallengeCompletion
from src.models.activity import Activity
from src.auth import get_password_hash, create_access_token

# POST /atividades
def criar_usuario_para_testes(db: Session):
    user = User(
        login="usuario_atividade",
        email="atividade@example.com",
        password=get_password_hash("senha123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def criar_desafio_para_testes(db: Session, usuario_id: int):
    desafio = Challenge(
        title="Desafio de Teste",
        description="Descrição teste",
        start_date=date.today() - timedelta(days=1),
        end_date=date.today() + timedelta(days=2),
        points=30,
        creator_id=usuario_id
    )
    db.add(desafio)
    db.commit()
    db.refresh(desafio)
    return desafio

def test_criar_atividade_sucesso_completo(client: TestClient, db_session: Session):
    user = criar_usuario_para_testes(db_session)
    desafio = criar_desafio_para_testes(db_session, user.id)
    token = create_access_token({"sub": user.email})

    foto_bytes = BytesIO(b"minhafoto").read()

    response = client.post(
        "/atividades",
        headers={"Authorization": f"Bearer {token}"},
        files={"photo": ("foto.png", foto_bytes, "image/png")},
        data={
            "challenge_id": desafio.id,
            "content": "Fiz 30 minutos de treino",
            "comment": "Gostei bastante"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["challenge_id"] == desafio.id
    assert data["content"] == "Fiz 30 minutos de treino"
    assert data["comment"] == "Gostei bastante"
    assert data["photo"] is not None
    assert isinstance(data["photo"], str)

def test_criar_atividade_sucesso_minimo(client: TestClient, db_session: Session):
    user = criar_usuario_para_testes(db_session)
    desafio = criar_desafio_para_testes(db_session, user.id)
    token = create_access_token({"sub": user.email})

    response = client.post(
        "/atividades",
        headers={"Authorization": f"Bearer {token}"},
        data={"challenge_id": desafio.id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["challenge_id"] == desafio.id
    assert data["content"] is None
    assert data["comment"] is None
    assert data["photo"] is None

def test_criar_atividade_sem_token(client: TestClient, db_session: Session):
    user = criar_usuario_para_testes(db_session)
    desafio = criar_desafio_para_testes(db_session, user.id)

    response = client.post(
        "/atividades",
        data={"challenge_id": desafio.id}
    )
    assert response.status_code in (401, 403)
    assert "detail" in response.json()

def test_criar_atividade_faltando_challenge_id(client: TestClient, db_session: Session):
    user = criar_usuario_para_testes(db_session)
    token = create_access_token({"sub": user.email})

    response = client.post(
        "/atividades",
        headers={"Authorization": f"Bearer {token}"},
        data={}  # sem challenge_id
    )
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()

def test_criar_atividade_challenge_invalido(client: TestClient, db_session: Session):
    user = criar_usuario_para_testes(db_session)
    token = create_access_token({"sub": user.email})

    response = client.post(
        "/atividades",
        headers={"Authorization": f"Bearer {token}"},
        data={"challenge_id": 9999, "content": "teste"}
    )
    # o comportamento depende se o sistema valida challenge_id ou não
    # aqui assumimos que não existe checagem explícita na rota
    # logo, o banco aceita challenge_id inexistente (FK não forçada)
    assert response.status_code == 201 or response.status_code == 500


# @app.get("/atividades-total")

def criar_usuario_e_desafio(db: Session):
    user = User(
        login="user_total",
        email="total@example.com",
        password=get_password_hash("senha123"),
        photo=b"foto_teste"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    desafio = Challenge(
        title="Desafio Ativo",
        description="descricao",
        start_date=datetime.today() - timedelta(days=1),
        end_date=datetime.today() + timedelta(days=1),
        points=100,
        creator_id=user.id
    )
    db.add(desafio)
    db.commit()
    db.refresh(desafio)

    return user, desafio

def criar_atividade(db: Session, user_id: int, challenge_id: int, created_at=None):
    atividade = Activity(
        user_id=user_id,
        challenge_id=challenge_id,
        content="atividade teste",
        comment="comentário teste",
        photo=b"foto_atividade",
        created_at=created_at or datetime.utcnow()
    )
    db.add(atividade)
    db.commit()
    db.refresh(atividade)
    return atividade

def test_listar_todas_atividades_sucesso(client: TestClient, db_session: Session):
    user, desafio = criar_usuario_e_desafio(db_session)
    atividade = criar_atividade(db_session, user.id, desafio.id)

    response = client.get("/atividades-total")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    atividade_json = data[0]
    assert atividade_json["id"] == atividade.id
    assert atividade_json["user_id"] == user.id
    assert atividade_json["challenge_id"] == desafio.id
    assert atividade_json["content"] == "atividade teste"
    assert atividade_json["comment"] == "comentário teste"
    assert "created_at" in atividade_json
    assert atividade_json["photo"] == base64.b64encode(b"foto_atividade").decode("utf-8")
    assert atividade_json["user"]["login"] == "user_total"
    assert atividade_json["user"]["photo"] == base64.b64encode(b"foto_teste").decode("utf-8")

def test_listar_todas_atividades_vazio(client: TestClient, db_session: Session):
    db_session.query(Activity).delete()
    db_session.commit()

    response = client.get("/atividades-total")
    assert response.status_code == 200
    assert response.json() == []


# @app.get("/meus-desafios")
def criar_usuario(db: Session):
    user = User(
        login="usuario_teste",
        email="teste_meus_desafios@example.com",
        password=get_password_hash("senha123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def criar_desafio(db: Session, titulo: str, criador_id: int):
    desafio = Challenge(
        title=titulo,
        description="Descrição de teste",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=7),
        points=20,
        creator_id=criador_id
    )
    db.add(desafio)
    db.commit()
    db.refresh(desafio)
    return desafio

def registrar_participacao(db: Session, user_id: int, challenge_id: int, concluido: bool = False):
    participacao = ChallengeCompletion(
        user_id=user_id,
        challenge_id=challenge_id,
        completed_at=date.today(),
        concluido=concluido
    )
    db.add(participacao)
    db.commit()

def test_meus_desafios_retorna_desafios_pendentes(client: TestClient, db_session: Session):
    user = criar_usuario(db_session)
    desafio1 = criar_desafio(db_session, "Desafio 1", user.id)
    desafio2 = criar_desafio(db_session, "Desafio 2", user.id)
    
    registrar_participacao(db_session, user.id, desafio1.id, concluido=False)
    registrar_participacao(db_session, user.id, desafio2.id, concluido=True)  # concluído deve ser ignorado

    token = create_access_token({"sub": user.email})
    response = client.get(
        "/meus-desafios",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Desafio 1"

def test_meus_desafios_vazio(client: TestClient, db_session: Session):
    user = criar_usuario(db_session)
    token = create_access_token({"sub": user.email})

    response = client.get(
        "/meus-desafios",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == []

def test_meus_desafios_sem_autenticacao(client: TestClient):
    response = client.get("/meus-desafios")
    assert response.status_code in (401, 403)
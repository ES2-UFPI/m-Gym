from datetime import datetime, date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.models.user import User
from src.models.challenge import Challenge
from src.models.challengecompletion import ChallengeCompletion
from src.models.activity import Activity
from src.auth import get_password_hash, create_access_token

def criar_usuario(db: Session, email="usuario_atividades@example.com"):
    user = User(
        login="usuario_atividades",
        email=email,
        password=get_password_hash("senha123")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def criar_atividade(db: Session, user_id: int, challenge_id: int = 1, content="Atividade Teste"):
    atividade = Activity(
        user_id=user_id,
        challenge_id=challenge_id,
        content=content,
        photo=None,
        comment="Comentário teste",
        created_at=datetime.utcnow()
    )
    db.add(atividade)
    db.commit()
    db.refresh(atividade)
    return atividade

def test_atividades_usuario_retorna_somente_do_usuario(client: TestClient, db_session: Session):
    user = criar_usuario(db_session)
    outro_usuario = criar_usuario(db_session, email="outro@example.com")

    criar_atividade(db_session, user_id=user.id)
    criar_atividade(db_session, user_id=outro_usuario.id)  # Atividade de outro usuário

    token = create_access_token({"sub": user.email})
    response = client.get(
        "/atividades-usuario",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["user_id"] == user.id
    assert data[0]["content"] == "Atividade Teste"

def test_atividades_usuario_nenhuma_registrada(client: TestClient, db_session: Session):
    user = criar_usuario(db_session)
    token = create_access_token({"sub": user.email})

    response = client.get(
        "/atividades-usuario",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == []
    
def test_atividades_usuario_sem_token(client: TestClient):
    response = client.get("/atividades-usuario")
    assert response.status_code in (401, 403)



# @app.post("/meus-desafios/{challenge_id}/concluir")
def criar_usuariopost(db: Session):
    user = User(
        login="teste_usuario_concluir",
        email="concluir@example.com",
        password=get_password_hash("senha123"),
        pontuacao=0
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def criar_desafio(db: Session, creator_id: int, pontos=30):
    desafio = Challenge(
        title="Desafio Concluir",
        description="Desafio de Teste",
        start_date=date.today(),
        end_date=date.today() + timedelta(days=5),
        points=pontos,
        creator_id=creator_id
    )
    db.add(desafio)
    db.commit()
    db.refresh(desafio)
    return desafio

def criar_participacao(db: Session, user_id: int, challenge_id: int):
    participacao = ChallengeCompletion(
        user_id=user_id,
        challenge_id=challenge_id,
        completed_at=date.today(),
        concluido=False
    )
    db.add(participacao)
    db.commit()
    return participacao

def test_concluir_desafio_com_sucesso(client: TestClient, db_session: Session):
    user = criar_usuariopost(db_session)
    desafio = criar_desafio(db_session, creator_id=user.id)
    criar_participacao(db_session, user_id=user.id, challenge_id=desafio.id)

    token = create_access_token({"sub": user.email})

    response = client.post(
        f"/meus-desafios/{desafio.id}/concluir",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Desafio concluído! Pontos adicionados."
    assert response.json()["pontos_ganhos"] == desafio.points

    db_session.refresh(user)
    assert user.pontuacao == desafio.points

def test_concluir_desafio_nao_inscrito(client: TestClient, db_session: Session):
    user = criar_usuariopost(db_session)
    desafio = criar_desafio(db_session, creator_id=user.id)  # Não se inscreveu
    token = create_access_token({"sub": user.email})

    response = client.post(
        f"/meus-desafios/{desafio.id}/concluir",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Você não está inscrito neste desafio."

def test_concluir_desafio_inexistente(client: TestClient, db_session: Session):
    user = criar_usuariopost(db_session)
    token = create_access_token({"sub": user.email})

    # Cria uma participação para um desafio inexistente
    participacao = ChallengeCompletion(
        user_id=user.id,
        challenge_id=9999,  # desafio inexistente
        completed_at=date.today(),
        concluido=False
    )
    db_session.add(participacao)
    db_session.commit()

    response = client.post(
        "/meus-desafios/9999/concluir",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Desafio não encontrado."

def test_concluir_desafio_sem_token(client: TestClient):
    response = client.post("/meus-desafios/1/concluir")
    assert response.status_code in (401, 403)

# GET /historico

def criar_usuario_historico(db: Session):
    user = User(
        login="user_historico",
        email="user@historico.com",
        password=get_password_hash("senha123"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def criar_desafio_historico(db: Session, creator_id: int):
    desafio = Challenge(
        title="Desafio Histórico",
        description="Desafio já concluído",
        start_date=date.today() - timedelta(days=10),
        end_date=date.today() - timedelta(days=1),
        points=20,
        creator_id=creator_id
    )
    db.add(desafio)
    db.commit()
    db.refresh(desafio)
    return desafio

def criar_conclusao_historico(db: Session, user_id: int, challenge_id: int):
    participacao = ChallengeCompletion(
        user_id=user_id,
        challenge_id=challenge_id,
        completed_at=date.today(),
        concluido=True
    )
    db.add(participacao)
    db.commit()

def test_listar_historico_usuario_com_sucesso(client: TestClient, db_session: Session):
    user = criar_usuario_historico(db_session)
    desafio = criar_desafio_historico(db_session, creator_id=user.id)
    criar_conclusao_historico(db_session, user_id=user.id, challenge_id=desafio.id)

    token = create_access_token({"sub": user.email})
    response = client.get("/historico", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    historico = response.json()
    assert isinstance(historico, list)
    assert len(historico) == 1
    assert historico[0]["title"] == desafio.title
    assert historico[0]["challenge_id"] == desafio.id
    
def test_listar_historico_usuario_vazio(client: TestClient, db_session: Session):
    user = criar_usuario_historico(db_session)
    token = create_access_token({"sub": user.email})

    response = client.get("/historico", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == []

def test_listar_historico_sem_autenticacao(client: TestClient):
    response = client.get("/historico")
    assert response.status_code in (401, 403)


import pytest

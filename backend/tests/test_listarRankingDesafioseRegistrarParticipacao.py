import pytest
import base64
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.models.user import User
from src.database import get_db
from src.models.challenge import Challenge
from src.auth import get_password_hash, create_access_token
from src.models.challengecompletion import ChallengeCompletion
# @app.get("/usuarios/ranking"
def criar_usuario_rank(db: Session, login, email, pontuacao, photo_bytes=None):
    user = User(
        login=login,
        email=email,
        password=get_password_hash("senha123"),
        photo=photo_bytes,
        pontuacao=pontuacao
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_ranking_ordenado_por_pontuacao(client: TestClient, db_session: Session):
    db_session.query(User).delete()
    db_session.commit()

    u1 = criar_usuario_rank(db_session, "usuario1", "u1@example.com", 50)
    u2 = criar_usuario_rank(db_session, "usuario2", "u2@example.com", 150)
    u3 = criar_usuario_rank(db_session, "usuario3", "u3@example.com", 100)

    response = client.get("/usuarios/ranking")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3

    # Verifica ordem correta
    assert data[0]["login"] == "usuario2"  # maior pontuação
    assert data[1]["login"] == "usuario3"
    assert data[2]["login"] == "usuario1"

    # Verifica campos presentes
    for user in data:
        assert "login" in user
        assert "email" in user
        assert "photo" in user
        assert "points" in user


def test_ranking_com_foto_base64(client: TestClient, db_session: Session):
    foto = b"imagem_testando"
    user = criar_usuario_rank(db_session, "comfoto", "foto@example.com", 99, photo_bytes=foto)

    response = client.get("/usuarios/ranking")
    assert response.status_code == 200

    data = response.json()
    usuario = next((u for u in data if u["login"] == "comfoto"), None)
    assert usuario is not None

    # Verifica se a foto está em base64 corretamente
    esperada = base64.b64encode(foto).decode("utf-8")
    assert usuario["photo"] == esperada


def test_ranking_vazio(client: TestClient, db_session: Session):
    db_session.query(User).delete()
    db_session.commit()

    response = client.get("/usuarios/ranking")
    assert response.status_code == 200
    assert response.json() == []

# @app.get("/desafios-ativos")
def criar_usuario_para_testes(db: Session):
    usuario = User(
        login="user_ativo",
        email="ativo@example.com",
        password=get_password_hash("senha123")
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def criar_desafio_com_datas(db: Session, titulo: str, dias_inicio: int, dias_fim: int, usuario_id: int):
    desafio = Challenge(
        title=titulo,
        description="desc",
        start_date=date.today() + timedelta(days=dias_inicio),
        end_date=date.today() + timedelta(days=dias_fim),
        points=10,
        creator_id=usuario_id
    )
    db.add(desafio)
    db.commit()
    db.refresh(desafio)
    return desafio


def test_listar_desafios_ativos_retorna_apenas_ativos(client: TestClient, db_session: Session):
    usuario = criar_usuario_para_testes(db_session)
    token = create_access_token({"sub": usuario.email})

    # Desafios com datas variadas
    criar_desafio_com_datas(db_session, "inativo_passado", -10, -5, usuario.id)
    criar_desafio_com_datas(db_session, "ativo", -1, 2, usuario.id)
    criar_desafio_com_datas(db_session, "inativo_futuro", 5, 10, usuario.id)

    response = client.get(
        "/desafios-ativos",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # Deve conter apenas o desafio ativo
    titulos = [d["title"] for d in data]
    assert "ativo" in titulos
    assert "inativo_passado" not in titulos
    assert "inativo_futuro" not in titulos


def test_listar_desafios_ativos_vazio(client: TestClient, db_session: Session):
    usuario = criar_usuario_para_testes(db_session)
    token = create_access_token({"sub": usuario.email})

    # Nenhum desafio criado
    response = client.get(
        "/desafios-ativos",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == []


def test_listar_desafios_ativos_sem_token(client: TestClient):
    response = client.get("/desafios-ativos")
    assert response.status_code in (401, 403)
    assert "detail" in response.json()

    
# @app.post("/desafios/{challenge_id}/participar")
def criar_usuario_para_testes(db: Session):
    usuario = User(
        login="participante",
        email="participante@example.com",
        password=get_password_hash("senha123")
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def criar_desafio(db: Session, titulo: str, usuario_id: int):
    desafio = Challenge(
        title=titulo,
        description="Desafio teste",
        start_date=date.today() - timedelta(days=1),
        end_date=date.today() + timedelta(days=3),
        points=10,
        creator_id=usuario_id
    )
    db.add(desafio)
    db.commit()
    db.refresh(desafio)
    return desafio


def test_participar_desafio_sucesso(client: TestClient, db_session: Session):
    usuario = criar_usuario_para_testes(db_session)
    desafio = criar_desafio(db_session, "Desafio A", usuario.id)
    token = create_access_token({"sub": usuario.email})

    response = client.post(
        f"/desafios/{desafio.id}/participar",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Participação registrada com sucesso!"


def test_participar_desafio_inexistente(client: TestClient, db_session: Session):
    usuario = criar_usuario_para_testes(db_session)
    token = create_access_token({"sub": usuario.email})

    response = client.post(
        f"/desafios/9999/participar",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Desafio não encontrado"


def test_participar_desafio_ja_concluido(client: TestClient, db_session: Session):
    usuario = criar_usuario_para_testes(db_session)
    desafio = criar_desafio(db_session, "Desafio B", usuario.id)
    token = create_access_token({"sub": usuario.email})

    participacao = ChallengeCompletion(
        user_id=usuario.id,
        challenge_id=desafio.id,
        completed_at=date.today(),
        concluido=True
    )
    db_session.add(participacao)
    db_session.commit()

    response = client.post(
        f"/desafios/{desafio.id}/participar",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Você já concluiu este desafio anteriormente."


def test_participar_desafio_ja_inscrito(client: TestClient, db_session: Session):
    usuario = criar_usuario_para_testes(db_session)
    desafio = criar_desafio(db_session, "Desafio C", usuario.id)
    token = create_access_token({"sub": usuario.email})

    participacao = ChallengeCompletion(
        user_id=usuario.id,
        challenge_id=desafio.id,
        completed_at=date.today(),
        concluido=False
    )
    db_session.add(participacao)
    db_session.commit()

    response = client.post(
        f"/desafios/{desafio.id}/participar",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Você já está inscrito neste desafio."


def test_participar_desafio_sem_token(client: TestClient, db_session: Session):
    usuario = criar_usuario_para_testes(db_session)
    desafio = criar_desafio(db_session, "Desafio D", usuario.id)

    response = client.post(f"/desafios/{desafio.id}/participar")
    assert response.status_code in (401, 403)
    assert "detail" in response.json()
import pytest
import base64
from fastapi.testclient import TestClient
from fastapi import status
from src.models.user import User
from src.auth import get_password_hash
from src.database import get_db
from src.auth import get_password_hash
from src.server import app
from src.auth import get_current_user, create_access_token, get_password_hash, verify_password
from sqlalchemy.orm import Session

# GET PERFIL
# Criação de um mock de usuário autenticado
@pytest.fixture
def usuario_falso(db_session):
    usuario = User(
        login="usuariofake",
        email="fake@example.com",
        password=get_password_hash("senha123"),
        photo=b"foto_fake_bytes",
        bio="Bio teste",
        pontuacao=42
    )
    db_session.add(usuario)
    db_session.commit()
    return usuario

@pytest.fixture
def client_override_auth(client, usuario_falso):
    # Sobrescrevendo get_current_user com fixture
    def override_get_current_user():
        return usuario_falso

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield client
    app.dependency_overrides.clear()

def test_get_perfil_sucesso(client_override_auth, usuario_falso):
    response = client_override_auth.get("/perfil")
    assert response.status_code == 200

    data = response.json()
    assert data["usuario"] == usuario_falso.login
    assert data["email"] == usuario_falso.email
    assert data["bio"] == usuario_falso.bio
    assert data["pontuacao"] == usuario_falso.pontuacao

    # Verifica se a foto foi codificada corretamente
    foto_base64_esperada = base64.b64encode(usuario_falso.photo).decode("utf-8")
    assert data["photo"] == foto_base64_esperada


def test_get_perfil_sem_autenticacao(client: TestClient):
    response = client.get("/perfil")
    assert response.status_code in (401, 403)  # depende do seu auth handler
    assert "detail" in response.json()


def test_get_perfil_token_invalido(client: TestClient):
    response = client.get(
        "/perfil", headers={"Authorization": "Bearer token_invalido"}
    )
    assert response.status_code in (401, 403)
    assert "detail" in response.json()


# PUT PERFIL
def test_atualiza_perfil_independente(client: TestClient, db_session: Session):
    # 1. Criar usuário diretamente no banco
    senha = get_password_hash("senha123")
    usuario = User(
        login="usuarioperfil",
        email="perfil@m.com",
        password=senha,
        photo=None,
        bio="Bio antiga"
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    # 2. Gerar token JWT manualmente
    token = create_access_token({"sub": usuario.email})

    # 3. Payload de atualização
    nova_bio = "Nova biografia"
    nova_foto_base64 = base64.b64encode(b"imagem-fake").decode("utf-8")

    payload = {
        "bio": nova_bio,
        "photo": nova_foto_base64
    }

    # 4. Requisição PUT /perfil com autenticação
    response = client.put(
        "/perfil",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["usuario"]["bio"] == nova_bio
    assert data["usuario"]["photo"] == nova_foto_base64
    assert data["usuario"]["email"] == usuario.email


def test_put_perfil_sem_autenticacao(client: TestClient):
    payload = {"bio": "Nova bio", "photo": None}
    response = client.put("/perfil", json=payload)
    assert response.status_code in (401, 403)


def test_put_perfil_usuario_nao_encontrado(client: TestClient, db_session: Session):
    # Cria um usuário, gera token, mas o deleta antes da chamada
    usuario = User(
        login="fantasma",
        email="semregistro@ghost.com",
        password=get_password_hash("senha123")
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    token = create_access_token({"sub": usuario.email})
    db_session.delete(usuario)
    db_session.commit()

    payload = {"bio": "Qualquer bio", "photo": None}
    response = client.put(
        "/perfil",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] in ["Não autenticado", "Not authenticated"]

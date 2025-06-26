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

# PUT ATUALIZALOGIN
def test_atualiza_login_independente(client: TestClient, db_session: Session):
    # 1. Criar usuário no banco
    senha = get_password_hash("senha123")
    usuario = User(
        login="login_antigo",
        email="loginteste@m.com",
        password=senha
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    # 2. Gerar token para esse usuário
    token = create_access_token({"sub": usuario.email})

    # 3. Payload com novo login
    payload = {
        "novo_login": "login_novo"
    }

    # 4. Enviar PUT /usuarios/atualizar-login com Authorization
    response = client.put(
        "/usuarios/atualizar-login",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    # 5. Verificações
    assert response.status_code == 200
    assert response.json()["message"] == "Login atualizado com sucesso."

    # 6. Verificar se foi atualizado no banco
    usuario_atualizado = db_session.query(User).filter(User.id == usuario.id).first()
    assert usuario_atualizado.login == "login_novo"

def criar_usuario(db: Session, login: str, email: str, senha: str = "senha123"):
    user = User(
        login=login,
        email=email,
        password=senha
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_atualizar_login_para_existente(client: TestClient, db_session: Session):
    # Cria dois usuários
    usuario1 = criar_usuario(db_session, "usuario1", "u1@email.com")
    usuario2 = criar_usuario(db_session, "usuario2", "u2@email.com")

    # Autentica como usuario1
    token = create_access_token({"sub": usuario1.email})

    # Tenta atualizar para login já existente (usuario2)
    response = client.put(
        "/usuarios/atualizar-login",
        json={"novo_login": "usuario2"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Login já está em uso."


def test_atualizar_login_sem_token(client: TestClient):
    response = client.put(
        "/usuarios/atualizar-login",
        json={"novo_login": "novo_login_sem_token"}
    )

    assert response.status_code == 401 or response.status_code == 403  # depende de como get_current_user está implementado


# def test_atualizar_login_payload_invalido(client: TestClient, db_session: Session):
#     usuario = criar_usuario(db_session, "original", "payload@email.com")
#     token = create_access_token({"sub": usuario.email})

#     # Envia login vazio
#     response = client.put(
#         "/usuarios/atualizar-login",
#         json={"novo_login": ""},
#         headers={"Authorization": f"Bearer {token}"}
#     )

#     assert response.status_code == 422  # erro de validação Pydantic

# PUT ATUALIZASENHA
def criar_usuario_para_teste(db_session):
    senha_hash = get_password_hash("senhaAntiga123")
    usuario = User(
        login="usuarioteste",
        email="senha@teste.com",
        password=senha_hash
    )
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)
    return usuario


def test_atualiza_senha_sucesso(client: TestClient, db_session: Session):
    usuario = criar_usuario_para_teste(db_session)
    token = create_access_token({"sub": usuario.email})

    payload = {
        "senha_antiga": "senhaAntiga123",
        "nova_senha": "novaSenha123"
    }

    response = client.put(
        "/usuarios/atualizar-senha",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Senha atualizada com sucesso."

    # Verifica se a senha realmente mudou no banco
    usuario_atualizado = db_session.query(User).filter(User.id == usuario.id).first()
    assert verify_password("novaSenha123", usuario_atualizado.password)


def test_atualiza_senha_falha_senha_antiga_incorreta(client: TestClient, db_session: Session):
    usuario = criar_usuario_para_teste(db_session)
    token = create_access_token({"sub": usuario.email})

    payload = {
        "senha_antiga": "senhaErrada",
        "nova_senha": "novaSenha123"
    }

    response = client.put(
        "/usuarios/atualizar-senha",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Senha antiga incorreta."


def test_atualiza_senha_falha_nova_senha_curta(client: TestClient, db_session: Session):
    usuario = criar_usuario_para_teste(db_session)
    token = create_access_token({"sub": usuario.email})

    payload = {
        "senha_antiga": "senhaAntiga123",
        "nova_senha": "123"
    }

    response = client.put(
        "/usuarios/atualizar-senha",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422  # erro de validação do Pydantic
    assert "nova_senha" in str(response.json())
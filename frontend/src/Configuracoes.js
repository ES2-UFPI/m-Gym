import React, { useState } from "react";

const Configuracoes = () => {
  const [novoLogin, setNovoLogin] = useState("");
  const [senhaAntiga, setSenhaAntiga] = useState("");
  const [novaSenha, setNovaSenha] = useState("");
  const [confirmarSenha, setConfirmarSenha] = useState("");

  const token = localStorage.getItem("access_token");

  const handleAtualizarLogin = async () => {
    if (!novoLogin.trim()) {
      alert("Por favor, insira um novo login.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/usuarios/atualizar-login", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ novo_login: novoLogin }),
      });

      if (!response.ok) throw new Error("Erro ao atualizar login");

      alert("Login atualizado com sucesso!");
      setNovoLogin("");
    } catch (error) {
      console.error(error);
      alert("Erro ao atualizar login.");
    }
  };

  const handleTrocarSenha = async () => {
    if (!senhaAntiga || !novaSenha || !confirmarSenha) {
      alert("Preencha todos os campos de senha.");
      return;
    }

    if (novaSenha !== confirmarSenha) {
      alert("A nova senha e a confirmação não coincidem.");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/usuarios/atualizar-senha", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          senha_antiga: senhaAntiga,
          nova_senha: novaSenha,
        }),
      });

      if (!response.ok) throw new Error("Erro ao atualizar senha");

      alert("Senha atualizada com sucesso!");
      setSenhaAntiga("");
      setNovaSenha("");
      setConfirmarSenha("");
    } catch (error) {
      console.error(error);
      alert("Erro ao atualizar senha.");
    }
  };

  return (
    <div
      style={{
        maxWidth: 700,
        margin: "0 auto",
        padding: 40,
        background: "#fff",
        borderRadius: 10,
        display: "flex",
        gap: 20,
        justifyContent: "center",
      }}
    >
      {/* Card para atualizar login */}
      <div
        style={{
          flex: 1,
          background: "#f9f9f9",
          padding: 20,
          borderRadius: 10,
          boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
        }}
      >
        <h2>Alterar Nome de Login</h2>
        <input
          type="text"
          placeholder="Novo nome de login"
          value={novoLogin}
          onChange={(e) => setNovoLogin(e.target.value)}
          style={{
            width: "100%",
            padding: 10,
            marginTop: 10,
            marginBottom: 20,
            borderRadius: 6,
            border: "1px solid #ccc",
          }}
        />
        <button
          onClick={handleAtualizarLogin}
          style={{
            backgroundColor: "#e53935",
            color: "#fff",
            padding: "10px 20px",
            border: "none",
            borderRadius: 6,
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          Atualizar Login
        </button>
      </div>

      {/* Card para trocar senha */}
      <div
        style={{
          flex: 1,
          background: "#f9f9f9",
          padding: 20,
          borderRadius: 10,
          boxShadow: "0 2px 8px rgba(0,0,0,0.05)",
        }}
      >
        <h2>Alterar Senha</h2>
        <input
          type="password"
          placeholder="Senha atual"
          value={senhaAntiga}
          onChange={(e) => setSenhaAntiga(e.target.value)}
          style={{
            width: "100%",
            padding: 10,
            marginTop: 10,
            borderRadius: 6,
            border: "1px solid #ccc",
          }}
        />
        <input
          type="password"
          placeholder="Nova senha"
          value={novaSenha}
          onChange={(e) => setNovaSenha(e.target.value)}
          style={{
            width: "100%",
            padding: 10,
            marginTop: 10,
            borderRadius: 6,
            border: "1px solid #ccc",
          }}
        />
        <input
          type="password"
          placeholder="Confirmar nova senha"
          value={confirmarSenha}
          onChange={(e) => setConfirmarSenha(e.target.value)}
          style={{
            width: "100%",
            padding: 10,
            marginTop: 10,
            marginBottom: 20,
            borderRadius: 6,
            border: "1px solid #ccc",
          }}
        />
        <button
          onClick={handleTrocarSenha}
          style={{
            backgroundColor: "#e53935",
            color: "#fff",
            padding: "10px 20px",
            border: "none",
            borderRadius: 6,
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          Atualizar Senha
        </button>
      </div>
    </div>
  );
};

export default Configuracoes;

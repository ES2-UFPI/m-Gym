import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Configuracoes() {
  const navigate = useNavigate();
  const usuario = JSON.parse(localStorage.getItem("usuario")) || {
    id: null,
    name: "",
    email: ""
  };

  const [name, setName] = useState(usuario.name);
  const [email, setEmail] = useState(usuario.email);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [mensagem, setMensagem] = useState('');
  const [excluindo, setExcluindo] = useState(false);

  const handleProfileSubmit = (e) => {
    e.preventDefault();
    // Atualiza apenas localmente (você pode adaptar para salvar no backend se quiser)
    const atualizado = { ...usuario, name, email };
    localStorage.setItem('usuario', JSON.stringify(atualizado));
    setMensagem('Perfil atualizado com sucesso!');
  };

  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setMensagem('As senhas não coincidem.');
      return;
    }

    // Aqui você poderia validar e enviar nova senha para o backend
    setMensagem('Senha atualizada com sucesso!');
    setCurrentPassword('');
    setNewPassword('');
    setConfirmPassword('');
  };

  const handleDeleteAccount = async () => {
  const confirmar = window.confirm("Tem certeza que deseja excluir sua conta?");
  if (!confirmar) return;

  setExcluindo(true);

  try {
    const token = localStorage.getItem("token");

    const response = await fetch(`http://localhost:8000/usuarios/${usuario.id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`, 
      }
    });

    if (!response.ok) {
      const data = await response.json();
      setMensagem(data.detail || 'Erro ao excluir a conta.');
      setExcluindo(false);
      return;
    }

    setMensagem('Conta excluída com sucesso!');
    localStorage.clear();
    setTimeout(() => navigate("/"), 1500);

  } catch (error) {
    console.error("Erro ao excluir conta:", error);
    setMensagem('Erro ao conectar com o servidor.');
    setExcluindo(false);
  }
};


  return (
    <div style={{ maxWidth: '600px', margin: '2rem auto', padding: '1rem' }}>
      <h1>Configurações</h1>
      <p>Gerencie suas configurações de conta e preferências.</p>

      {mensagem && <p style={{ color: 'green' }}>{mensagem}</p>}

      <hr />

      <h2>Perfil</h2>
      <form onSubmit={handleProfileSubmit}>
        <div>
          <label>Nome:</label><br />
          <input value={name} onChange={e => setName(e.target.value)} required />
        </div>
        <div>
          <label>Email:</label><br />
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        </div>
        <button type="submit">Salvar Alterações</button>
      </form>

      <hr />

      <h2>Alterar Senha</h2>
      <form onSubmit={handlePasswordSubmit}>
        <div>
          <label>Senha Atual:</label><br />
          <input type="password" value={currentPassword} onChange={e => setCurrentPassword(e.target.value)} required />
        </div>
        <div>
          <label>Nova Senha:</label><br />
          <input type="password" value={newPassword} onChange={e => setNewPassword(e.target.value)} required />
        </div>
        <div>
          <label>Confirmar Nova Senha:</label><br />
          <input type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required />
        </div>
        <button type="submit">Alterar Senha</button>
      </form>

      <hr />

      <h2>Excluir Conta</h2>
      <p style={{ color: 'red' }}>Ao excluir sua conta, todos os seus dados serão removidos. Esta ação é irreversível.</p>
      <button onClick={handleDeleteAccount} style={{ backgroundColor: 'red', color: 'white' }}>
        {excluindo ? "Excluindo..." : "Excluir Conta" }
      </button>
    </div>
  );
}

export default Configuracoes;
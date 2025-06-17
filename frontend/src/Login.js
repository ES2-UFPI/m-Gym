import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [mensagem, setMensagem] = useState('');

  const handleLogin = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch(`${process.env.REACT_APP_API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      if (Array.isArray(data.detail)) {
        // Concatena as mensagens de erro do FastAPI
        const mensagensErro = data.detail.map((err) => err.msg).join(', ');
        setMensagem(mensagensErro);
      } else {
        setMensagem(data.detail || 'Erro no login');
      }
      return;
    }


    localStorage.setItem("access_token", data.access_token);
    
    localStorage.setItem("usuario", JSON.stringify(data.usuario));

    navigate('/inicio');
  } catch (error) {
    setMensagem("Erro ao conectar com o servidor.");
  }
};

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Bem Vindo ao m-GYM</h2>
        <form onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="E-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={styles.input}
          />
          <input
            type="password"
            placeholder="Senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={styles.input}
          />
          <button type="submit" style={styles.button}>Entrar</button>
        </form>
        <button onClick={() => navigate('/cadastro')} style={styles.linkButton}>
          Criar Conta
        </button>
        {mensagem && <p style={styles.message}>{mensagem}</p>}
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    background: '#f0f2f5',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
  },
  card: {
    width: 320,
    padding: 30,
    borderRadius: 10,
    backgroundColor: '#ffffff',
    boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
  },
  title: {
    marginBottom: 20,
    textAlign: 'center',
    color: '#333',
  },
  input: {
    width: '100%',
    padding: 12,
    margin: '10px 0',
    borderRadius: 5,
    border: '1px solid #ccc',
    fontSize: 14,
  },
  button: {
    width: '100%',
    padding: 12,
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: 5,
    fontSize: 16,
    cursor: 'pointer',
    marginTop: 10,
  },
  linkButton: {
    width: '100%',
    padding: 10,
    backgroundColor: '#2196F3',
    color: 'white',
    border: 'none',
    borderRadius: 5,
    fontSize: 14,
    cursor: 'pointer',
    marginTop: 10,
  },
  message: {
    marginTop: 15,
    textAlign: 'center',
    color: '#666',
  },
};

export default Login;
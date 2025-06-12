// src/Register.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [login, setLogin] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [mensagem, setMensagem] = useState("");
  const navigate = useNavigate();

 const handleSubmit = async (e) => {
  e.preventDefault();
  setMensagem('');

  try {
    const response = await fetch('https://m-gym-ag38.onrender.com/usuarios', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ login, email, password }),  // ajuste dos campos
    });

    const data = await response.json();

    if (!response.ok) {
      if (Array.isArray(data.detail)) {
        const erros = data.detail.map((err) => err.msg).join(" | ");
        setMensagem(erros);
      } else if (typeof data.detail === 'string') {
        setMensagem(data.detail);
      } else {
        setMensagem("Erro ao cadastrar.");
      }
      return;
    }

    setMensagem(data.message);
    setTimeout(() => navigate('/'), 2000);
  } catch (error) {
    setMensagem('Erro de conexão com o servidor.');
  }
};

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Cadastro</h2>
        <form onSubmit={handleSubmit}>
          <input type="text" style={styles.text}
            value={login}
            onChange={(e) => setLogin(e.target.value)}
            required
            placeholder="Login"
          />

            <input type="email" style={styles.text}
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Email"
            />
            <input type="password" style={styles.text}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="Senha"
            />
          <button type="submit" style={styles.button}>Cadastrar</button>
        </form>
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
  password: {
    width: '100%',
    padding: 12,
    margin: '10px 0',
    borderRadius: 5,
    border: '1px solid #ccc',
    fontSize: 14,
  },
  email: {
    width: '100%',
    padding: 12,
    margin: '10px 0',
    borderRadius: 5,
    border: '1px solid #ccc',
    fontSize: 14,
  },
  text: {
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
    backgroundColor: '#673AB7',  // Mesma cor roxa do login
    color: 'white',
    border: 'none',
    borderRadius: 5,
    fontSize: 16,
    cursor: 'pointer',
    marginTop: 10,
  },
  message: {
    marginTop: 15,
    textAlign: 'center',
    color: '#444',
  },
};

export default Register;
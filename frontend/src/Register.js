// src/Register.js
import React, { useState } from 'react';

function Register() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log({ nome, email, senha }); // Futuramente: enviar para API
    alert('Cadastro enviado (ainda não integrado)');
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Cadastro</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Nome de usuário"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            required
            style={styles.input}
          />
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
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            required
            style={styles.input}
          />
          <button type="submit" style={styles.button}>Cadastrar</button>
        </form>
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
    backgroundColor: '#673AB7',
    color: 'white',
    border: 'none',
    borderRadius: 5,
    fontSize: 16,
    cursor: 'pointer',
    marginTop: 10,
  },
};

export default Register;

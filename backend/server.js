
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const PORT = 3001;

app.use(cors());
app.use(bodyParser.json());

// Simulação de login com credenciais fixas
const user = {
  email: 'usuario@example.com',
  password: '123456'
};

app.post('/login', (req, res) => {
  const { email, password } = req.body;
  if (email === user.email && password === user.password) {
    return res.status(200).json({ message: 'Login bem-sucedido' });
  } else {
    return res.status(401).json({ message: 'Credenciais inválidas' });
  }
});

app.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});
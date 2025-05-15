import React from 'react';

function Inicio() {
  const usuario = JSON.parse(localStorage.getItem("usuario"));

  return (
    <div style={{ textAlign: 'center', marginTop: '20%' }}>
      <h1>Bem-vindo(a), {usuario?.login || 'usuário'}!</h1>
      <p>Você está logado com o e-mail: {usuario?.email}</p>
    </div>
  );
}

export default Inicio;
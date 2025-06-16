import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import Inicio from './Inicio';
import Configuracoes from './Configuracoes'; 
import EditarPerfil from './EditarPerfil';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/cadastro" element={<Register />} />
        <Route path="/inicio" element={<Inicio />} />
        <Route path="/configuracoes" element={<Configuracoes />} /> 
        <Route path="/editar" element={<EditarPerfil/>}/>
      </Routes>
    </Router>
  );
}

export default App;
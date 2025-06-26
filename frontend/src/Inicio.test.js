// src/Inicio.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import Inicio from './Inicio';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn(),
}));


describe('Componente Inicio', () => {
  test('exibe saudação com usuário padrão', () => {
    render(<Inicio />);
    expect(screen.getByText(/bem-vindo/i)).toBeInTheDocument();
  });
});

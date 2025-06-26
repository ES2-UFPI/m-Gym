// src/Login.test.js
import React from 'react';
import { render, screen } from '@testing-library/react';
import Login from './Login';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => jest.fn(),
}));


describe('Componente Login', () => {
  test('renderiza título "Entrar"', () => {
    render(<Login />);
    expect(screen.getByText(/entrar/i)).toBeInTheDocument();
  });

  test('renderiza campos de email e senha', () => {
    render(<Login />);
    expect(screen.getByPlaceholderText(/email/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/senha/i)).toBeInTheDocument();
  });

  test('renderiza botão de login', () => {
    render(<Login />);
    expect(screen.getByRole('button', { name: /entrar/i })).toBeInTheDocument();
  });
});

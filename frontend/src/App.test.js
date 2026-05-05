import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';
import '@testing-library/jest-dom';

// Mock do window.location
delete window.location;
window.location = { href: '', pathname: '/' };

beforeEach(() => {
  window.location.href = '';
  window.location.pathname = '/';
});

describe('App Component - Integração', () => {
  test('renderiza componente Login por padrão', () => {
    render(<App />);
    
    // Verifica se está mostrando o componente Login
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  test('renderiza componente SuccessPage quando pathname é /success', () => {
    // Mock do window.location para página de sucesso
    Object.defineProperty(window, 'location', {
      value: { 
        pathname: '/success',
        href: '/success'
      },
      writable: true
    });

    render(<App />);

    // Verifica se está mostrando o componente SuccessPage
    expect(screen.getByRole('heading', { name: /welcome/i })).toBeInTheDocument();
    expect(screen.getByText(/registration successful/i)).toBeInTheDocument();
  });

  test('alterna entre Login e Register', () => {
    render(<App />);
    
    // Verifica se começa com Login
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();

    // Clica no link para Register
    fireEvent.click(screen.getByRole('link', { name: /register/i }));
    
    // Verifica se mudou para Register
    expect(screen.getByRole('heading', { name: /register/i })).toBeInTheDocument();

    // Clica no link para Login
    fireEvent.click(screen.getByRole('link', { name: /login/i }));
    
    // Verifica se voltou para Login
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
  });

  test('estado inicial isLogin é true', () => {
    render(<App />);
    
    // Componente Login deve estar visível
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
    expect(screen.queryByRole('heading', { name: /register/i })).not.toBeInTheDocument();
  });

  test('roteamento baseado em pathname funciona corretamente', () => {
    // Testar pathname raiz
    Object.defineProperty(window, 'location', {
      value: { pathname: '/' },
      writable: true
    });

    const { rerender } = render(<App />);
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();

    // Testar pathname /success
    Object.defineProperty(window, 'location', {
      value: { pathname: '/success' },
      writable: true
    });

    rerender(<App />);
    expect(screen.getByRole('heading', { name: /welcome/i })).toBeInTheDocument();
  });

  test('callbacks são passados corretamente para componentes filhos', () => {
    render(<App />);
    
    // Verifica se os callbacks existem (não podemos testar diretamente, 
    // mas podemos verificar que os componentes filhos estão renderizados)
    expect(screen.getByRole('link', { name: /register/i })).toBeInTheDocument();
    
    // Clicar no link deve funcionar (o que indica que o callback foi passado)
    fireEvent.click(screen.getByRole('link', { name: /register/i }));
    expect(screen.getByRole('heading', { name: /register/i })).toBeInTheDocument();
  });
});
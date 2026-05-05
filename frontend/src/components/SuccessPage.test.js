import { render, screen, fireEvent } from '@testing-library/react';
import SuccessPage from './SuccessPage';
import '@testing-library/jest-dom';

// Mock do localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

// Mock do window.location
delete window.location;
window.location = { href: '', pathname: '/success' };

beforeEach(() => {
  localStorageMock.getItem.mockClear();
  localStorageMock.clear.mockClear();
  window.location.href = '';
});

describe('SuccessPage Component', () => {
  test('renderiza página de sucesso com usuário', async () => {
    // Mock do localStorage para retornar usuário
    localStorageMock.getItem.mockImplementation((key) => {
      if (key === 'user') return 'testuser';
      return null;
    });

    render(<SuccessPage />);

    // Esperar carregamento e verificar elementos
    await screen.findByRole('heading', { name: /welcome/i });
    expect(screen.getByText(/registration successful/i)).toBeInTheDocument();
    expect(screen.getByText(/welcome, testuser/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument();
  });

  test('renderiza página de sucesso sem usuário', async () => {
    // Mock do localStorage para não retornar usuário
    localStorageMock.getItem.mockImplementation(() => null);

    render(<SuccessPage />);

    // Esperar carregamento e verificar elementos
    await screen.findByRole('heading', { name: /welcome/i });
    expect(screen.getByText(/welcome, user/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument();
  });

  test('mostra loading enquanto carrega', () => {
    // Mock do localStorage para demorar
    localStorageMock.getItem.mockImplementation(() => {
      // Simular demora
      return null;
    });

    render(<SuccessPage />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test('faz logout corretamente', async () => {
    // Mock do localStorage para retornar usuário
    localStorageMock.getItem.mockImplementation((key) => {
      if (key === 'user') return 'testuser';
      return null;
    });

    render(<SuccessPage />);

    // Esperar carregamento
    await screen.findByRole('button', { name: /logout/i });

    // Clicar em logout
    fireEvent.click(screen.getByRole('button', { name: /logout/i }));

    // Verificar se localStorage foi limpo
    expect(localStorageMock.clear).toHaveBeenCalled();
    
    // Verificar se redirecionou para página inicial
    expect(window.location.href).toBe('/');
  });

  test('chama localStorage.getItem com chave correta', () => {
    localStorageMock.getItem.mockImplementation((key) => {
      if (key === 'user') return 'testuser';
      return null;
    });

    render(<SuccessPage />);

    // Verificar se getItem foi chamado com 'user'
    expect(localStorageMock.getItem).toHaveBeenCalledWith('user');
  });

  test('estilização do botão de logout', async () => {
    localStorageMock.getItem.mockImplementation((key) => {
      if (key === 'user') return 'testuser';
      return null;
    });

    render(<SuccessPage />);

    const logoutButton = await screen.findByRole('button', { name: /logout/i });
    
    // Verificar estilos do botão
    expect(logoutButton).toHaveStyle({
      maxWidth: '200px',
      padding: '0.75rem 1.5rem',
      backgroundColor: '#e74c3c',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer'
    });
  });
});

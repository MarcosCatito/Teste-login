import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SuccessPage from './SuccessPage';
import '@testing-library/jest-dom';

// Mock do localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};

// Limpar localStorage real e substituir com mock
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
  writable: true
});

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

  
  test('faz logout corretamente', async () => {
    // Mock do localStorage para retornar usuário
    localStorageMock.getItem.mockReturnValue('testuser');

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

  test('chama localStorage.getItem com chave correta', async () => {
    localStorageMock.getItem.mockReturnValue('testuser');

    render(<SuccessPage />);

    // Esperar o useEffect ser executado
    await waitFor(() => {
      expect(localStorageMock.getItem).toHaveBeenCalledWith('user');
    });
  });

  test('botão de logout está presente e clicável', async () => {
    localStorageMock.getItem.mockImplementation((key) => {
      if (key === 'user') return 'testuser';
      return null;
    });

    render(<SuccessPage />);

    const logoutButton = await screen.findByRole('button', { name: /logout/i });
    
    // Verificar se o botão existe e está visível
    expect(logoutButton).toBeInTheDocument();
    expect(logoutButton).toBeVisible();
    expect(logoutButton).toBeEnabled();
  });
});

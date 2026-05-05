import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Login from './Login';
import '@testing-library/jest-dom';

// Mock do fetch global
global.fetch = jest.fn();

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
window.location = { href: '', pathname: '/' };

beforeEach(() => {
  fetch.mockClear();
  localStorageMock.getItem.mockClear();
  localStorageMock.setItem.mockClear();
  localStorageMock.clear.mockClear();
});

describe('Login Component', () => {
  test('renderiza formulário de login corretamente', () => {
    render(<Login />);
    
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /register/i })).toBeInTheDocument();
  });

  test('preenche formulário e submete com sucesso', async () => {
    const mockOnLoginSuccess = jest.fn();
    
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        message: 'Login successful',
        token: 'fake-token',
        user: 'testuser'
      })
    });

    render(<Login onLoginSuccess={mockOnLoginSuccess} />);

    // Preencher formulário
    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'testuser' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });

    // Submeter
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    // Verificar sucesso
    await waitFor(() => {
      expect(screen.getByText(/login successful/i)).toBeInTheDocument();
    });

    // Verificar se localStorage foi chamado
    expect(localStorageMock.setItem).toHaveBeenCalledWith('token', 'fake-token');
    expect(localStorageMock.setItem).toHaveBeenCalledWith('user', 'testuser');
    
    // Verificar se callback foi chamado
    expect(mockOnLoginSuccess).toHaveBeenCalledWith({
      message: 'Login successful',
      token: 'fake-token',
      user: 'testuser'
    });
  });

  test('mostra erro de credenciais inválidas', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ error: 'Invalid credentials' })
    });

    render(<Login />);

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'wronguser' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'wrongpass' }
    });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });

    expect(localStorageMock.setItem).not.toHaveBeenCalled();
  });

  test('mostra erro de conexão', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));

    render(<Login />);

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'testuser' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText(/connection error/i)).toBeInTheDocument();
    });
  });

  test('chama onToggleForm ao clicar em Register', () => {
    const mockOnToggleForm = jest.fn();
    render(<Login onToggleForm={mockOnToggleForm} />);

    fireEvent.click(screen.getByRole('link', { name: /register/i }));
    expect(mockOnToggleForm).toHaveBeenCalledTimes(1);
  });

  test('desabilita botão durante carregamento', async () => {
    fetch.mockImplementation(() => new Promise(resolve => 
      setTimeout(() => resolve({
        ok: true,
        json: async () => ({ message: 'Login successful' })
      }), 100)
    ));

    render(<Login />);

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'testuser' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });

    const button = screen.getByRole('button', { name: /login/i });
    fireEvent.click(button);

    // Verificar se botão está desabilitado e com texto de carregamento
    expect(button).toBeDisabled();
    expect(button).toHaveTextContent('Logging in...');
  });
});

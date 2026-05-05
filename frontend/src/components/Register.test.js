import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Register from './Register';
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

describe('Register Component', () => {
  test('renderiza formulário de registro corretamente', () => {
    render(<Register />);
    
    expect(screen.getByRole('heading', { name: /register/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /register/i })).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /login/i })).toBeInTheDocument();
  });

  test('preenche formulário e submete com sucesso', async () => {
    const mockOnRegisterSuccess = jest.fn();
    jest.useFakeTimers();
    
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        message: 'Registration successful',
        token: 'fake-token',
        user: 'newuser'
      })
    });

    render(<Register onRegisterSuccess={mockOnRegisterSuccess} />);

    // Preencher formulário
    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'newuser' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });

    // Submeter
    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    // Verificar sucesso
    await waitFor(() => {
      expect(screen.getByText(/registration successful/i)).toBeInTheDocument();
    });

    // Verificar se localStorage foi chamado
    expect(localStorageMock.setItem).toHaveBeenCalledWith('token', 'fake-token');
    expect(localStorageMock.setItem).toHaveBeenCalledWith('user', 'newuser');
    
    // Verificar se callback foi chamado
    expect(mockOnRegisterSuccess).toHaveBeenCalledWith({
      message: 'Registration successful',
      token: 'fake-token',
      user: 'newuser'
    });

    // Simular setTimeout e verificar redirect
    jest.advanceTimersByTime(1000);
    expect(window.location.href).toBe('/success');

    jest.useRealTimers();
  });

  test('mostra erro de usuário já existente', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ error: 'Username already exists' })
    });

    render(<Register />);

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'existinguser' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    await waitFor(() => {
      expect(screen.getByText(/username already exists/i)).toBeInTheDocument();
    });

    expect(localStorageMock.setItem).not.toHaveBeenCalled();
  });

  test('mostra erro de conexão', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));

    render(<Register />);

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'newuser' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });
    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    await waitFor(() => {
      expect(screen.getByText(/connection error/i)).toBeInTheDocument();
    });
  });

  test('chama onToggleForm ao clicar em Login', () => {
    const mockOnToggleForm = jest.fn();
    render(<Register onToggleForm={mockOnToggleForm} />);

    fireEvent.click(screen.getByRole('link', { name: /login/i }));
    expect(mockOnToggleForm).toHaveBeenCalledTimes(1);
  });

  test('desabilita botão durante carregamento', async () => {
    fetch.mockImplementation(() => new Promise(resolve => 
      setTimeout(() => resolve({
        ok: true,
        json: async () => ({ message: 'Registration successful' })
      }), 100)
    ));

    render(<Register />);

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: 'newuser' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });

    const button = screen.getByRole('button', { name: /register/i });
    fireEvent.click(button);

    // Verificar se botão está desabilitado e com texto de carregamento
    expect(button).toBeDisabled();
    expect(button).toHaveTextContent('Registering...');
  });

  test('valida campos obrigatórios', async () => {
    render(<Register />);

    // Tentar submeter formulário vazio
    const button = screen.getByRole('button', { name: /register/i });
    fireEvent.click(button);

    // Verificar se inputs estão marcados como required
    expect(screen.getByLabelText(/username/i)).toBeRequired();
    expect(screen.getByLabelText(/password/i)).toBeRequired();
  });
});

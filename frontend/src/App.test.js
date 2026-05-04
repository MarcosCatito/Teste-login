import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from './App';


global.fetch = jest.fn();

beforeEach(() => {
  fetch.mockClear();
  localStorage.clear();
});

test('renderiza formulário de login por defeito', () => {
  render(<App />);
  
  expect(screen.getByText(/login/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
});

test('alterna entre login e register', () => {
  render(<App />);
  
  fireEvent.click(screen.getByText(/register/i));
  expect(screen.getByText(/register/i)).toBeInTheDocument();

  fireEvent.click(screen.getByText(/login/i));
  expect(screen.getByText(/login/i)).toBeInTheDocument();
});

test('submete login com sucesso', async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({ message: 'Login successful' })
  });

  render(<App />);

  fireEvent.change(screen.getByLabelText(/username/i), {
    target: { value: 'testuser' }
  });

  fireEvent.change(screen.getByLabelText(/password/i), {
    target: { value: 'password123' }
  });

  fireEvent.click(screen.getByRole('button'));

  await waitFor(() => {
    expect(screen.getByText(/login successful/i)).toBeInTheDocument();
  });
});

test('submete register com sucesso e guarda dados', async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({
      message: 'Registered',
      token: '123',
      user: 'testuser'
    })
  });

  render(<App />);

  fireEvent.click(screen.getByText(/register/i));

  fireEvent.change(screen.getByLabelText(/username/i), {
    target: { value: 'testuser' }
  });

  fireEvent.change(screen.getByLabelText(/password/i), {
    target: { value: 'password123' }
  });

  fireEvent.click(screen.getByRole('button'));

  await waitFor(() => {
    expect(screen.getByText(/registered/i)).toBeInTheDocument();
  });

  expect(localStorage.getItem('token')).toBe('123');
  expect(localStorage.getItem('user')).toBe('testuser');
});
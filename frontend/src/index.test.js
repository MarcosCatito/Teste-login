import React from 'react';
import ReactDOM from 'react-dom/client';
import { act } from 'react-dom/test-utils';

// Mock do App (para não testar o App aqui)
jest.mock('./App', () => () => <div>Mocked App</div>);

describe('index.js', () => {
  let container;

  beforeEach(() => {
    container = document.createElement('div');
    container.id = 'root';
    document.body.appendChild(container);
  });

  afterEach(() => {
    document.body.removeChild(container);
    container = null;
    jest.resetModules(); // importante para reimportar o index
  });

  test('renders App into root div', async () => {
    await act(async () => {
      require('./index'); // importa o ficheiro que executa o render
    });

    expect(container.innerHTML).toContain('Mocked App');
  });
});
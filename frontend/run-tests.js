const { execSync } = require('child_process');

try {
  console.log('Executando testes unitários...');
  const output = execSync('npm test -- --watchAll=false --verbose', { 
    encoding: 'utf8',
    stdio: 'pipe'
  });
  console.log('Saída dos testes:');
  console.log(output);
} catch (error) {
  console.log('Erro durante a execução dos testes:');
  console.log(error.stdout);
  console.log(error.stderr);
  process.exit(1);
}

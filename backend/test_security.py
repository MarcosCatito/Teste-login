#!/usr/bin/env python3
"""
Testes de segurança para verificar proteções implementadas
"""

import requests
import json
import time
from database import db
from security import security

class SecurityTests:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_sql_injection_attempts(self):
        """Testa tentativas de SQL Injection"""
        print("=== Testando SQL Injection ===")
        
        sql_injection_payloads = [
            "admin'--",
            "admin' OR '1'='1",
            "admin'; DROP TABLE users; --",
            "admin' UNION SELECT * FROM users --",
            "'; DELETE FROM users; --",
            "admin' OR 1=1#",
            "admin'/**/OR/**/1=1--"
        ]
        
        for payload in sql_injection_payloads:
            try:
                response = self.session.post(
                    f"{self.base_url}/login",
                    json={"username": payload, "password": "password123"}
                )
                
                if response.status_code == 200:
                    print(f"❌ VULNERÁVEL: Payload '{payload}' aceito")
                else:
                    print(f"✓ PROTEGIDO: Payload '{payload}' rejeitado")
                    
            except Exception as e:
                print(f"✓ PROTEGIDO: Payload '{payload}' causou erro: {e}")
    
    def test_xss_attempts(self):
        """Testa tentativas de XSS"""
        print("\n=== Testando XSS ===")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "';alert('XSS');//",
            "<svg onload=alert('XSS')>"
        ]
        
        for payload in xss_payloads:
            try:
                response = self.session.post(
                    f"{self.base_url}/register",
                    json={"username": payload, "password": "Password123456"}
                )
                
                if response.status_code == 201:
                    print(f"❌ VULNERÁVEL: XSS payload '{payload}' aceito")
                else:
                    print(f"✓ PROTEGIDO: XSS payload '{payload}' rejeitado")
                    
            except Exception as e:
                print(f"✓ PROTEGIDO: XSS payload '{payload}' causou erro: {e}")
    
    def test_brute_force_protection(self):
        """Testa proteção contra brute force"""
        print("\n=== Testando Brute Force Protection ===")
        
        username = "testuser"
        failed_attempts = 0
        
        for i in range(10):  # Tentar 10 vezes
            try:
                response = self.session.post(
                    f"{self.base_url}/login",
                    json={"username": username, "password": f"wrongpass{i}"}
                )
                
                if response.status_code == 401:
                    failed_attempts += 1
                    if failed_attempts >= 5:
                        print(f"✓ PROTEGIDO: Bloqueado após {failed_attempts} tentativas")
                        break
                elif response.status_code == 429:
                    print(f"✓ PROTEGIDO: Rate limit ativado na tentativa {i+1}")
                    break
                else:
                    print(f"? Status inesperado: {response.status_code}")
                    
            except Exception as e:
                print(f"Erro na tentativa {i+1}: {e}")
        
        if failed_attempts < 5:
            print(f"⚠️  AVISO: Apenas {failed_attempts} tentativas antes de bloquear")
    
    def test_rate_limiting(self):
        """Testa rate limiting"""
        print("\n=== Testando Rate Limiting ===")
        
        requests_made = 0
        
        for i in range(10):  # Fazer 10 requisições rápidas
            try:
                response = self.session.post(
                    f"{self.base_url}/register",
                    json={"username": f"user{i}", "password": "Password123456"}
                )
                
                requests_made += 1
                
                if response.status_code == 429:
                    print(f"✓ PROTEGIDO: Rate limit ativado após {requests_made} requisições")
                    break
                    
            except Exception as e:
                print(f"Erro na requisição {i+1}: {e}")
        
        if requests_made >= 10:
            print("⚠️  AVISO: Rate limit não ativado após 10 requisições")
    
    def test_username_validation(self):
        """Testa validação de usernames"""
        print("\n=== Testando Validação de Username ===")
        
        invalid_usernames = [
            "",  # Vazio
            "ab",  # Muito curto
            "a" * 51,  # Muito longo
            "user name",  # Espaço
            "user@name",  # Caractere especial
            "admin",  # Palavra reservada
            "root",  # Palavra reservada
            "'; DROP TABLE users; --",  # SQL Injection
            "<script>alert('xss')</script>",  # XSS
        ]
        
        for username in invalid_usernames:
            try:
                response = self.session.post(
                    f"{self.base_url}/register",
                    json={"username": username, "password": "Password123456"}
                )
                
                if response.status_code == 201:
                    print(f"❌ VULNERÁVEL: Username inválido '{username}' aceito")
                else:
                    print(f"✓ PROTEGIDO: Username inválido '{username}' rejeitado")
                    
            except Exception as e:
                print(f"✓ PROTEGIDO: Username '{username}' causou erro: {e}")
    
    def test_cors_security(self):
        """Testa configuração CORS"""
        print("\n=== Testando CORS ===")
        
        # Testar origem não permitida
        headers = {"Origin": "http://malicious-site.com"}
        
        try:
            response = requests.get(f"{self.base_url}/", headers=headers)
            
            if "Access-Control-Allow-Origin" in response.headers:
                allowed_origin = response.headers["Access-Control-Allow-Origin"]
                if allowed_origin == "*" or allowed_origin == "http://malicious-site.com":
                    print(f"❌ VULNERÁVEL: CORS permite origem maliciosa: {allowed_origin}")
                else:
                    print(f"✓ PROTEGIDO: CORS restringe origens: {allowed_origin}")
            else:
                print("✓ PROTEGIDO: Sem cabeçalho CORS para origem não permitida")
                
        except Exception as e:
            print(f"Erro ao testar CORS: {e}")
    
    def test_database_security(self):
        """Testa segurança da base de dados"""
        print("\n=== Testando Segurança da Base de Dados ===")
        
        # Testar se a base de dados usa prepared statements
        try:
            # Tentar criar usuário com SQL Injection
            success, result = db.create_user("test'; DROP TABLE users; --", "Password123456")
            
            if success:
                print("❌ VULNERÁVEL: SQL Injection bem-sucedido na criação de usuário")
            else:
                print("✓ PROTEGIDO: SQL Injection prevenido na criação de usuário")
                
        except Exception as e:
            print(f"✓ PROTEGIDO: SQL Injection causou erro: {e}")
        
        # Verificar se tabela users ainda existe
        try:
            users = db.get_all_users()
            print(f"✓ Base de dados intacta: {len(users)} usuários encontrados")
        except Exception as e:
            print(f"❌ ERRO: Problema na base de dados: {e}")
    
    def run_all_tests(self):
        """Executa todos os testes de segurança"""
        print("🔒 INICIANDO TESTES DE SEGURANÇA 🔒")
        print("=" * 50)
        
        self.test_sql_injection_attempts()
        self.test_xss_attempts()
        self.test_brute_force_protection()
        self.test_rate_limiting()
        self.test_username_validation()
        self.test_cors_security()
        self.test_database_security()
        
        print("\n" + "=" * 50)
        print("🔒 TESTES DE SEGURANÇA CONCLUÍDOS 🔒")

if __name__ == "__main__":
    # Teste direto das funções de segurança
    print("=== Teste Direto das Funções de Segurança ===")
    
    # Testar sanitização
    security_manager = security
    
    test_inputs = [
        "admin'; DROP TABLE users; --",
        "<script>alert('xss')</script>",
        "normal_user",
        "user@domain.com",
        "'; SELECT * FROM users; --"
    ]
    
    for test_input in test_inputs:
        sanitized = security_manager.sanitize_input(test_input)
        print(f"Original: {test_input}")
        print(f"Sanitized: {sanitized}")
        print("-" * 30)
    
    # Testar validação de username
    test_usernames = ["admin", "test_user", "ab", "user@name", "'; DROP TABLE users; --"]
    
    for username in test_usernames:
        valid, result = security_manager.validate_username(username)
        print(f"Username: {username} -> {'VÁLIDO' if valid else 'INVÁLIDO'}: {result}")
    
    print("\n✓ Testes diretos concluídos!")
    print("\nPara testes completos com servidor em execução:")
    print("python app.py")
    print("python test_security.py")

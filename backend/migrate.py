#!/usr/bin/env python3
from database import db
import os

def migrate_data():
    print("=== Migração para Base de Dados SQL ===")
    
    # Criar utilizador admin
    success, result = db.create_user("admin", "Admin123456", "admin@example.com")
    if success:
        print(f"✓ Admin criado: {result}")
    
    # Criar utilizadores de exemplo
    sample_users = [
        ("joao", "Joao123456", "joao@example.com"),
        ("maria", "Maria123456", "maria@example.com"),
        ("pedro", "Pedro123456", "pedro@example.com")
    ]
    
    for username, password, email in sample_users:
        success, result = db.create_user(username, password, email)
        if success:
            print(f"✓ Criado: {username}")
        else:
            print(f"✗ Falha: {username}")

def test_operations():
    print("\n=== Testando Operações SQL ===")
    
    # Testar CREATE
    success, result = db.create_user("test", "Test123456", "test@example.com")
    assert success, "CREATE failed"
    print("✓ CREATE funcionando")
    
    # Testar SELECT
    user = db.get_user_by_username("test")
    assert user is not None, "SELECT failed"
    print("✓ SELECT funcionando")
    
    # Testar VERIFY
    verified = db.verify_user("test", "Test123456")
    assert verified is not None, "VERIFY failed"
    print("✓ VERIFY funcionando")
    
    # Testar UPDATE
    success, result = db.update_user(user['id'], email="updated@example.com")
    assert success, "UPDATE failed"
    print("✓ UPDATE funcionando")
    
    # Testar DELETE
    success = db.delete_user(user['id'])
    assert success, "DELETE failed"
    print("✓ DELETE funcionando")
    
    # Testar STATS
    stats = db.get_user_stats()
    assert 'total_users' in stats, "STATS failed"
    print(f"✓ STATS: {stats}")

def show_info():
    print("\n=== Informações da Base de Dados ===")
    
    if os.path.exists(db.db_path):
        size = os.path.getsize(db.db_path)
        print(f"Arquivo: {db.db_path} ({size} bytes)")
        
        stats = db.get_user_stats()
        print(f"Total utilizadores: {stats.get('total_users', 0)}")
        
        users = db.get_all_users()
        print(f"Utilizadores ativos: {len(users)}")
        for user in users[:3]:
            print(f"  - {user['username']}")
    else:
        print("Base de dados não encontrada")

if __name__ == "__main__":
    try:
        migrate_data()
        test_operations()
        show_info()
        print("\n✓ Migração concluída com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")

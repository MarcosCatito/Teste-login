#!/usr/bin/env python3
from database import db
import sqlite3

def view_database():
    print("=== VISUALIZAR BASE DE DADOS ===\n")
    
    # Verificar se arquivo existe
    import os
    if not os.path.exists('users.db'):
        print(" Base de dados não encontrada. Execute primeiro:")
        print("   python migrate_optimized.py")
        return
    
    # Conectar diretamente ao SQLite
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Mostrar tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"Tabelas encontradas: {[t[0] for t in tables]}\n")
    
    # Mostrar dados da tabela users
    if 'users' in [t[0] for t in tables]:
        print("📋 TABELA USERS:")
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        if users:
            # Mostrar colunas
            cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]
            print(f"Colunas: {columns}")
            print()
            
            # Mostrar dados
            for user in users:
                print(f"ID: {user[0]}")
                print(f"Username: {user[1]}")
                print(f"Email: {user[3]}")
                print(f"Criado em: {user[4]}")
                print(f"Último login: {user[5]}")
                print(f"Ativo: {user[6]}")
                print("-" * 40)
        else:
            print("Nenhum utilizador encontrado")
    
    conn.close()
    
    # Usar funções do database
    print("\n📊 ESTATÍSTICAS:")
    stats = db.get_user_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\n👥 UTILIZADORES ATIVOS:")
    users = db.get_all_users()
    for user in users:
        print(f"- {user['username']} ({user['email']})")

if __name__ == "__main__":
    view_database()

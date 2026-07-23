def test_db():
    print("Test de connexion à la base de données...")
    
    try:
        import sqlite3
        print("1. Module sqlite3 importé avec succès")
        
        conn = sqlite3.connect('data.db')
        print("2. Connexion à la base de données établie")
        
        cursor = conn.cursor()
        print("3. Curseur créé")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"4. Tables trouvées: {tables}")
        
        conn.close()
        print("Test terminé avec succès!")
        
    except Exception as e:
        print(f"ERREUR: {str(e)}")

if __name__ == "__main__":
    test_db()

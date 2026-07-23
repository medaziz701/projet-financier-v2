import sys
import os

def check_environment():
    print("=== Vérification de l'environnement ===")
    print(f"Python version: {sys.version}")
    print(f"Répertoire de travail: {os.getcwd()}")
    print(f"Chemin Python: {sys.executable}")
    
    # Vérifier l'accès au fichier
    db_path = 'data.db'
    print(f"\n=== Vérification de l'accès à {db_path} ===")
    if os.path.exists(db_path):
        print(f"- Le fichier existe. Taille: {os.path.getsize(db_path)} octets")
        print(f"- Dernière modification: {os.path.getmtime(db_path)}")
        print(f"- Droits d'accès: {os.access(db_path, os.R_OK) and 'Lecture' or 'Pas de lecture'}, "
              f"{os.access(db_path, os.W_OK) and 'Écriture' or 'Pas d\'écriture'}")
    else:
        print(f"- ERREUR: Le fichier {db_path} n'existe pas dans le répertoire courant.")
    
    # Vérifier le contenu du répertoire
    print("\n=== Contenu du répertoire ===")
    files = os.listdir()
    print(f"Nombre de fichiers: {len(files)}")
    print("Fichiers .db dans le répertoire:", 
          [f for f in files if f.endswith('.db')])
    
    # Vérifier les modules installés
    try:
        import sqlite3
        print("\n=== Module SQLite3 ===")
        print(f"Version SQLite: {sqlite3.sqlite_version}")
        print("Le module SQLite3 est correctement importé.")
    except ImportError as e:
        print(f"ERREUR: Impossible d'importer le module SQLite3: {e}")

if __name__ == "__main__":
    check_environment()

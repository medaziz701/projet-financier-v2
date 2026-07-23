import os
import shutil
from datetime import datetime

def restore_latest_backup():
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
    db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.db')
    
    # Vérifier si le dossier de sauvegarde existe
    if not os.path.exists(backup_dir):
        print("ERREUR: Le dossier de sauvegarde n'existe pas.")
        return False
    
    # Trouver tous les fichiers de sauvegarde
    backups = []
    for file in os.listdir(backup_dir):
        if file.endswith(('.db', '.backup')) and 'data' in file.lower():
            file_path = os.path.join(backup_dir, file)
            mtime = os.path.getmtime(file_path)
            backups.append((mtime, file, file_path))
    
    if not backups:
        print("Aucune sauvegarde trouvée dans le dossier 'backups'.")
        return False
    
    # Trier par date de modification (du plus récent au plus ancien)
    backups.sort(reverse=True, key=lambda x: x[0])
    
    # Afficher les sauvegardes disponibles
    print("Sauvegardes disponibles (du plus récent au plus ancien) :")
    for i, (mtime, file, _) in enumerate(backups, 1):
        print(f"{i}. {file} - {datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Demander à l'utilisateur quelle sauvegarde restaurer
    while True:
        try:
            choice = input("\nEntrez le numéro de la sauvegarde à restaurer (ou 'q' pour quitter) : ")
            if choice.lower() == 'q':
                return False
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(backups):
                selected_backup = backups[choice_idx]
                break
            print("Numéro invalide. Veuillez réessayer.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")
    
    # Sauvegarder l'ancien fichier s'il existe
    if os.path.exists(db_file):
        backup_name = f"data.backup_before_restore_{int(datetime.now().timestamp())}.db"
        shutil.copy2(db_file, os.path.join(os.path.dirname(db_file), backup_name))
        print(f"\nAncien fichier sauvegardé sous : {backup_name}")
    
    # Restaurer la sauvegarde
    try:
        shutil.copy2(selected_backup[2], db_file)
        print(f"\nSauvegarde restaurée avec succès : {selected_backup[1]}")
        print(f"Base de données mise à jour : {db_file}")
        return True
    except Exception as e:
        print(f"\nERREUR lors de la restauration : {e}")
        return False

if __name__ == "__main__":
    print("=== RESTAURATION DE SAUVEGARDE DE LA BASE DE DONNÉES ===\n")
    restore_latest_backup()

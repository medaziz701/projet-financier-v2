import os
import shutil
from datetime import datetime

def restore_backup():
    # Chemin du dossier de sauvegarde
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
    
    # Vérifier si le dossier de sauvegarde existe
    if not os.path.exists(backup_dir):
        print("ERREUR: Le dossier de sauvegarde n'existe pas.")
        return False
    
    # Lister les fichiers de sauvegarde
    try:
        backup_files = [f for f in os.listdir(backup_dir) 
                       if f.lower().endswith(('.db', '.backup')) 
                       and 'data' in f.lower()]
        
        if not backup_files:
            print("Aucun fichier de sauvegarde trouvé dans le dossier 'backups'.")
            return False
            
        # Trier les fichiers par date de modification (du plus récent au plus ancien)
        backup_files.sort(key=lambda x: os.path.getmtime(os.path.join(backup_dir, x)), reverse=True)
        
        # Afficher les sauvegardes disponibles
        print("Sauvegardes disponibles (du plus récent au plus ancien):")
        for i, file in enumerate(backup_files, 1):
            mtime = os.path.getmtime(os.path.join(backup_dir, file))
            print(f"{i}. {file} - {datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Demander à l'utilisateur de choisir une sauvegarde
        while True:
            try:
                choice = input("\nEntrez le numéro de la sauvegarde à restaurer (ou 'q' pour quitter): ").strip()
                if choice.lower() == 'q':
                    return False
                
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(backup_files):
                    selected_backup = backup_files[choice_idx]
                    break
                print("Numéro invalide. Veuillez réessayer.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")
        
        # Chemin de la sauvegarde sélectionnée et de la base de données
        backup_path = os.path.join(backup_dir, selected_backup)
        db_path = os.path.join(os.path.dirname(backup_dir), 'data.db')
        
        # Sauvegarder l'ancien fichier s'il existe
        if os.path.exists(db_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"data.bak_{timestamp}.db"
            shutil.copy2(db_path, os.path.join(os.path.dirname(db_path), backup_name))
            print(f"\nAncien fichier sauvegardé sous : {backup_name}")
        
        # Copier la sauvegarde
        shutil.copy2(backup_path, db_path)
        print(f"\nSauvegarde restaurée avec succès : {selected_backup}")
        print(f"Base de données mise à jour : {db_path}")
        
        # Vérifier la taille du fichier restauré
        if os.path.exists(db_path):
            print(f"Taille du fichier restauré : {os.path.getsize(db_path) / (1024*1024):.2f} Mo")
        
        return True
        
    except Exception as e:
        print(f"\nERREUR lors de la restauration : {str(e)}")
        return False

if __name__ == "__main__":
    print("=== RESTAURATION DE SAUVEGARDE DE LA BASE DE DONNÉES ===\n")
    restore_backup()

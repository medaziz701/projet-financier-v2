import os
import shutil

def copy_latest_backup():
    try:
        # Chemin du dossier de sauvegarde
        backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
        
        # Vérifier si le dossier de sauvegarde existe
        if not os.path.exists(backup_dir):
            print("ERREUR: Le dossier de sauvegarde n'existe pas.")
            return False
            
        # Trouver le fichier de sauvegarde le plus récent
        backup_files = []
        for file in os.listdir(backup_dir):
            if file.startswith('data-backup') and file.endswith('.db'):
                file_path = os.path.join(backup_dir, file)
                mtime = os.path.getmtime(file_path)
                backup_files.append((mtime, file_path))
        
        if not backup_files:
            print("Aucun fichier de sauvegarde trouvé.")
            return False
            
        # Trier par date de modification (du plus récent au plus ancien)
        backup_files.sort(reverse=True)
        latest_backup = backup_files[0][1]
        
        # Chemin de destination
        dest_path = os.path.join(os.path.dirname(latest_backup), '..', 'data.db')
        
        # Copier le fichier
        shutil.copy2(latest_backup, dest_path)
        
        print(f"Sauvegarde restaurée avec succès : {os.path.basename(latest_backup)}")
        print(f"Vers : {dest_path}")
        print(f"Taille : {os.path.getsize(dest_path) / (1024*1024):.2f} Mo")
        
        return True
        
    except Exception as e:
        print(f"ERREUR : {str(e)}")
        return False

if __name__ == "__main__":
    print("Restauration de la dernière sauvegarde...\n")
    copy_latest_backup()
    

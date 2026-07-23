import os
import shutil
import sqlite3
from datetime import datetime

DB_PATH = "data.db"


def backup_database(db_path: str) -> str:
    """Create a timestamped backup copy of the database next to the original.

    Returns the backup file path.
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Base de données introuvable: {db_path}")

    backup_dir = os.path.join(os.path.dirname(db_path) or ".", "backups")
    os.makedirs(backup_dir, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = os.path.splitext(os.path.basename(db_path))[0]
    backup_path = os.path.join(backup_dir, f"{base}-backup-{ts}.db")

    shutil.copy2(db_path, backup_path)
    return backup_path


def reset_all_tables(db_path: str) -> None:
    """Delete all rows from all non-system tables and reset sequences.

    - Disables foreign keys for the purge, re-enables afterwards
    - Resets AUTOINCREMENT counters (sqlite_sequence)
    - VACUUM to reclaim space
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Disable FKs to avoid delete-order issues
    cur.execute("PRAGMA foreign_keys = OFF")

    # Fetch all user tables (exclude internal sqlite_* tables)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cur.fetchall()]

    # Purge data from each table
    for tbl in tables:
        try:
            cur.execute(f"DELETE FROM {tbl}")
        except sqlite3.Error as e:
            print(f"[AVERTISSEMENT] Échec suppression table '{tbl}': {e}")

    # Reset AUTOINCREMENT counters if the meta-table exists
    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sqlite_sequence';")
        if cur.fetchone():
            cur.execute("DELETE FROM sqlite_sequence")
    except sqlite3.Error as e:
        print(f"[INFO] Impossible de réinitialiser sqlite_sequence: {e}")

    # Re-enable FKs and commit
    cur.execute("PRAGMA foreign_keys = ON")
    conn.commit()

    # VACUUM outside of a transaction for file compaction
    try:
        cur.execute("VACUUM")
    except sqlite3.Error as e:
        print(f"[INFO] VACUUM non exécuté: {e}")

    conn.close()


def main():
    print("=== Réinitialisation des tables de la base ===")

    try:
        backup_path = backup_database(DB_PATH)
        print(f"Sauvegarde créée: {backup_path}")
    except Exception as e:
        print(f"[ATTENTION] Sauvegarde non réalisée: {e}")
        print("Poursuite de la réinitialisation sans sauvegarde…")

    try:
        reset_all_tables(DB_PATH)
        print("Réinitialisation terminée avec succès.")
    except Exception as e:
        print(f"Échec de la réinitialisation: {e}")


if __name__ == "__main__":
    main()

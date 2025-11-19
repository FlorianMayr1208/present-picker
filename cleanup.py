#!/usr/bin/env python3
"""
Cleanup Script - Entfernt alle überflüssigen Dateien der Datenbank-Version
"""
import os
import shutil

# Dateien zum Löschen
FILES_TO_DELETE = [
    'run.py',
    'init_db.py',
    'migrate_to_postgres.py',
    'setup_supabase.py',
    'VERCEL_DEPLOYMENT.md',
    'SUPABASE_SETUP.md',
    'requirements.md',
    'app/app.py',
    'app/config.py',
    'app/templates/admin.html',
    'app/templates/admin_destination_form.html',
    'app/templates/admin_activities.html',
    'app/templates/admin_activity_form.html',
    'app/templates/admin_import.html',
]

# Ordner zum Löschen
FOLDERS_TO_DELETE = [
    'app/models',
    'app/__pycache__',
]

def cleanup():
    """Führe Cleanup durch"""
    print("🧹 Starte Cleanup...\n")

    deleted_files = 0
    deleted_folders = 0

    # Lösche Dateien
    for file_path in FILES_TO_DELETE:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✓ Gelöscht: {file_path}")
                deleted_files += 1
            except Exception as e:
                print(f"✗ Fehler bei {file_path}: {e}")
        else:
            print(f"⊘ Nicht gefunden: {file_path}")

    print()

    # Lösche Ordner
    for folder_path in FOLDERS_TO_DELETE:
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"✓ Gelöscht: {folder_path}/")
                deleted_folders += 1
            except Exception as e:
                print(f"✗ Fehler bei {folder_path}: {e}")
        else:
            print(f"⊘ Nicht gefunden: {folder_path}/")

    # Lösche .DS_Store Files (macOS)
    print("\n🍎 Entferne .DS_Store Files...")
    ds_store_count = 0
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == '.DS_Store':
                try:
                    os.remove(os.path.join(root, file))
                    ds_store_count += 1
                except:
                    pass

    if ds_store_count > 0:
        print(f"✓ {ds_store_count} .DS_Store Files gelöscht")

    print("\n" + "="*60)
    print(f"  Cleanup abgeschlossen!")
    print(f"  {deleted_files} Dateien gelöscht")
    print(f"  {deleted_folders} Ordner gelöscht")
    print("="*60)
    print("\n✨ Dein Projekt ist jetzt aufgeräumt!")
    print("📝 Starte die App mit: python app_simple.py")

if __name__ == '__main__':
    response = input("⚠️  Möchtest du wirklich alle überflüssigen Dateien löschen? (ja/nein): ")
    if response.lower() in ['ja', 'j', 'yes', 'y']:
        cleanup()
    else:
        print("Abgebrochen.")



@echo off
setlocal

REM Dossier du projet (où se trouve ce .bat)
set "PROJECT_DIR=%~dp0"

REM Aller dans le dossier du projet
pushd "%PROJECT_DIR%"

REM Créer l'environnement virtuel s'il n'existe pas
if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creation de l'environnement virtuel...
    py -3 -m venv .venv
)

REM Activer l'environnement virtuel
call ".venv\Scripts\activate.bat"

REM Dossier des logs
if not exist logs mkdir logs

REM Installer les dependances si requirements.txt existe
if exist requirements.txt (
    echo [INFO] Installation des dependances depuis requirements.txt...
    pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt
)

REM Vérifier et installer les paquets requis si absents
python -c "import ttkthemes" 1>nul 2>nul
if errorlevel 1 (
    echo [INFO] Installation du paquet manquant: ttkthemes
    pip install ttkthemes
)
python -c "import matplotlib" 1>nul 2>nul
if errorlevel 1 (
    echo [INFO] Installation du paquet manquant: matplotlib
    pip install matplotlib
)
python -c "import PIL" 1>nul 2>nul
if errorlevel 1 (
    echo [INFO] Installation du paquet manquant: Pillow
    pip install Pillow
)

REM Lancer l'application
echo [INFO] Demarrage de l'application...
python "%PROJECT_DIR%main.py" 1> "logs/run.log" 2> "logs/error.log"
set "ERR=%ERRORLEVEL%"
if not "%ERR%"=="0" (
    echo.
    echo [ERREUR] L'application s'est arretee avec le code %ERR%.
    echo Consultez logs\error.log pour le detail. Apercu:
    echo --------------------
    type "logs/error.log"
    echo --------------------
    echo.
    pause
)

REM Revenir au dossier precedent
popd

endlocal

@echo off
setlocal enabledelayedexpansion

REM Chemin vers le répertoire contenant les fichiers CNF
set "cnf_dir=D:\RCR_TP\Benchmark\uf20-91"

REM Chemin vers l'exécutable ubcsat
set "ubcsat_path=D:\RCR_TP\RCR\ubcsat.exe"

REM Parcourir tous les fichiers CNF dans le répertoire
for %%f in ("%cnf_dir%\*.cnf") do (
    echo Traitement de %%f...
    "%ubcsat_path%" -alg saps -i "%%f" -solve
    echo.
)

echo Tous les fichiers ont été traités.
pause
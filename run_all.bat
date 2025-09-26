@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Cek apakah ada argumen file
if "%~1"=="" (
    echo Pemakaian: run_all.bat namafile.xlsx
    exit /b 1
)

:: Simpan path file input
set "INPUT_FILE=%~1"

:: Ambil nama file dasar (tanpa ekstensi)
for %%F in ("%INPUT_FILE%") do (
    set "BASENAME=%%~nF"
    set "DIRNAME=%%~dpF"
)

:: Log file
set "LOGFILE=%DIRNAME%%BASENAME%_run_all.log"

echo === Proses dimulai: %DATE% %TIME% === > "%LOGFILE%"
echo === Proses dimulai: %DATE% %TIME% ===

:: Aktifkan venv
call venv\Scripts\activate

:: Step 1
echo === Step 1: Proses app.py === | tee -a "%LOGFILE%"
echo === Step 1: Proses app.py === >> "%LOGFILE%"
python app.py --file "%INPUT_FILE%" >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo Gagal di step 1 (app.py). Stop.
    exit /b 1
)

set "UND_FILE=%DIRNAME%%BASENAME%_undian.xlsx"
if not exist "%UND_FILE%" (
    echo File %UND_FILE% tidak ditemukan. Stop.
    exit /b 1
)

:: Step 2
echo === Step 2: Proses transform.py ===
echo === Step 2: Proses transform.py === >> "%LOGFILE%"
python transform.py --file "%UND_FILE%" >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo Gagal di step 2 (transform.py). Stop.
    exit /b 1
)

set "TRANS_FILE=%DIRNAME%%BASENAME%_undian_transform.xlsx"
if not exist "%TRANS_FILE%" (
    echo File %TRANS_FILE% tidak ditemukan. Stop.
    exit /b 1
)

:: Step 3
echo === Step 3: Proses takeout.py ===
echo === Step 3: Proses takeout.py === >> "%LOGFILE%"
python takeout.py --file "%TRANS_FILE%" >> "%LOGFILE%" 2>&1
if errorlevel 1 (
    echo Gagal di step 3 (takeout.py). Stop.
    exit /b 1
)

echo === Semua proses selesai ===
echo === Semua proses selesai === >> "%LOGFILE%"
echo Hasil akhir: %DIRNAME%%BASENAME%_undian_transform_takeout.xlsx
echo Hasil akhir: %DIRNAME%%BASENAME%_undian_transform_takeout.xlsx >> "%LOGFILE%"

pause

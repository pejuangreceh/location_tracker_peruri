@echo off
SETLOCAL

:: Cek apakah ada argumen file
if "%~1"=="" (
    echo Pemakaian: run_all.bat namafile.xlsx
    exit /b 1
)

set FILE=%~1

:: Aktifkan venv
call venv\Scripts\activate

echo === Step 1: Proses app.py ===
python app.py --file "%FILE%"

:: Hasil step 1 = namafile_processed.xlsx + namafile_undian.xlsx
set BASE=%~dpn1
set UND_FILE=%BASE%_undian.xlsx

echo === Step 2: Proses transform.py (pakai file _undian) ===
python transform.py --file "%UND_FILE%"

:: Hasil step 2 = namafile_undian_transform.xlsx
set TRANS_FILE=%BASE%_undian_transform.xlsx

echo === Step 3: Proses takeout.py (pakai file _undian_transform) ===
python takeout.py --file "%TRANS_FILE%"

:: Hasil step 3 = namafile_undian_transform_takeout.xlsx

echo.
echo === Semua proses selesai ===
echo Hasil akhir: %BASE%_undian_transform_takeout.xlsx
pause

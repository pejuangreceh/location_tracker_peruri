@echo off
echo === Aktifkan Virtual Environment ===
call venv\Scripts\activate

echo === Jalankan Aplikasi ===
python app.py --file "Form_Reg_HUT_Peruri_20252025-09-25_07_02_54.xlsx"

echo.
echo === Program Selesai ===
pause

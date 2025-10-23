@echo off
echo [%date% %time%] Restart cycle >> "D:\JavaService\logs\JavaService.log"
tasklist /FI "IMAGENAME eq OtohitsApp.exe" | findstr /I "OtohitsApp.exe" >nul
if %ERRORLEVEL%==0 (
    echo [%date% %time%] Menghentikan OtohitsApp.exe >> "D:\JavaService\logs\JavaService.log"
    taskkill /F /IM OtohitsApp.exe >> "D:\JavaService\logs\JavaService.log" 2>&1
)
timeout /t 10 /nobreak >nul
echo [%date% %time%] Menjalankan OtohitsApp.exe >> "D:\JavaService\logs\JavaService.log"
start "" "D:\JavaService\OtohitsApp.exe" >> "D:\JavaService\logs\JavaService.log" 2>&1

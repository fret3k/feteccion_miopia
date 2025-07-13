@echo off
echo ========================================
echo    MyopiaAI - Iniciando Aplicación
echo ========================================
echo.

echo Iniciando Backend en nueva ventana...
start "MyopiaAI Backend" cmd /k "cd /d %~dp0 && start_backend.bat"

echo Esperando 5 segundos para que el backend inicie...
timeout /t 5 /nobreak >nul

echo Iniciando Frontend en nueva ventana...
start "MyopiaAI Frontend" cmd /k "cd /d %~dp0 && start_frontend.bat"

echo.
echo ========================================
echo    Aplicación iniciada correctamente
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul 
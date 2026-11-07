@echo off
chcp 65001 > nul
echo ============================================================
echo   Galaxy To-Do Sync: Google 계정 1회 인증 (OAuth 2.0)
echo ============================================================
echo.
echo 잠시 후 기본 웹 브라우저가 열립니다.
echo kiho.kil@gmail.com 계정으로 로그인 후 [허용]을 눌러주세요.
echo.
python "%~dp0galaxy_todo_sync.py" auth
echo.
pause


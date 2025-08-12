@echo off
setlocal
for /f "delims=" %%I in ('wsl wslpath -a "%~dp0check_qdrant.sh"') do set WSL_PATH=%%I
wsl bash -lc "bash -x '%WSL_PATH%'"
endlocal

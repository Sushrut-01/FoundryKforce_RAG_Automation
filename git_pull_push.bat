@echo off
REM Git pull and push with conflict resolution

setlocal enabledelayedexpansion

cd /d c:\Users\SushrutNistane\foundry-playready-rag-testing

set GIT_PATH=C:\Users\SushrutNistane\AppData\Local\Programs\Git\cmd\git.exe

echo.
echo ======================================================================
echo GIT PULL AND PUSH
echo ======================================================================
echo.

echo [1/3] Pulling latest changes from remote...
"%GIT_PATH%" pull origin main --no-edit
echo.

if !errorlevel! equ 0 (
    echo [2/3] Push attempt...
    "%GIT_PATH%" push origin main
    
    if !errorlevel! equ 0 (
        echo.
        echo ======================================================================
        echo SUCCESS! All changes pushed!
        echo ======================================================================
        echo.
        echo Repository: https://github.com/Sushrut-01/FoundryKforce_RAG_Automation
        echo.
        echo Recent commits:
        "%GIT_PATH%" log --oneline -5
    ) else (
        echo Push failed. Retrying with force pull...
        "%GIT_PATH%" fetch origin
        "%GIT_PATH%" rebase origin/main 2>nul
        "%GIT_PATH%" push origin main
    )
) else (
    echo Pull encountered issues. Checking status...
    "%GIT_PATH%" status
)

echo.
pause

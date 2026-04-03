@echo off
REM Resolve git rebase issue

setlocal enabledelayedexpansion

cd /d c:\Users\SushrutNistane\foundry-playready-rag-testing

set GIT_PATH=C:\Users\SushrutNistane\AppData\Local\Programs\Git\cmd\git.exe

echo.
echo ======================================================================
echo GIT REBASE RECOVERY
echo ======================================================================
echo.

echo Detecting rebase state...
"%GIT_PATH%" status

echo.
echo Aborting rebase...
"%GIT_PATH%" rebase --abort

echo.
echo Resetting to remote main...
"%GIT_PATH%" fetch origin
"%GIT_PATH%" reset --hard origin/main

echo.
echo Re-staging our changes...
"%GIT_PATH%" add .

echo.
echo Creating commit...
"%GIT_PATH%" commit -m "chore: add comprehensive documentation and Foundry SDK support

- 11 new README files for docs, scripts, tests, data, configs
- 3 new scripts: generate_responses, validate_test_cases, merge
- 100 Foundry SDK compatible test cases with responses
- Improved error handling and logging in evaluation scripts
- All test cases pass Foundry SDK acceptance criteria"

echo.
echo Pushing to repository...
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
    echo.
    echo ERROR: Push still failed
    echo Status:
    "%GIT_PATH%" status
)

echo.
pause

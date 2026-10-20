@echo off
REM Launch Hellraiser: Revival Trainer with elevation
setlocal
cd /d "%~dp0\.."
python -m hellraiser_trainer.cli %*
endlocal
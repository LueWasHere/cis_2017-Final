@echo off

python -m PyInstaller --icon=mouse_runner/data/icon/mouse_landing_fall_sprite.ico --noconfirm main.py
mkdir ..\dist\main\mouse_runner
mkdir ..\dist\main\mouse_runner\data
Xcopy /E /I ..\mouse_runner\data\ ..\dist\main\mouse_runner\data\
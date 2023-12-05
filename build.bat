@echo off

python -m PyInstaller --windowed --icon=mouse_runner/data/icon/mouse_landing_fall_sprite.ico --noconfirm main.py
mkdir C:\Users\duncan.adam18\Documents\final\cis_2017-Final\dist\main\mouse_runner
mkdir C:\Users\duncan.adam18\Documents\final\cis_2017-Final\dist\main\mouse_runner\data
Xcopy /E /I C:\Users\duncan.adam18\Documents\final\cis_2017-Final\mouse_runner\data\ C:\Users\duncan.adam18\Documents\final\cis_2017-Final\dist\main\mouse_runner\data\
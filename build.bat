@echo off
echo Instalando dependencias necessarias...
pip install pyinstaller pandas ttkthemes openpyxl

echo Criando executavel...
pyinstaller --noconfirm --onefile --windowed --name "Gerador_de_Contas_Bancarias" --clean ^
  --add-data "C:\Users\maxwi\anaconda3\Lib\site-packages/ttkthemes;ttkthemes/" ^
  app_tkinter.py

echo Executable criado com sucesso na pasta 'dist'!
pause
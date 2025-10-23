import PyInstaller.__main__

PyInstaller.__main__.run([
    'app_tkinter.py',
    '--onefile',
    '--windowed',
    '--name=Gerador_de_Contas_Bancarias',
    '--add-data=LICENSE.txt;.',
    '--icon=bank.ico',
    '--noconsole'
])
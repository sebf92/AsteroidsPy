pip install -r requirements.txt
pyinstaller --onefile main.py
cd dist
del asteropy.exe
rename main.exe asteropy.exe
cd ..
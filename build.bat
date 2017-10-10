
@set BUILD_FILE_NAME=main
@set PYINSTALLER_ROOT="C:\Python27\Scripts"
@set UPX_ROOT="D:\Program Files\upx391w"


%PYINSTALLER_ROOT%\pyinstaller.exe --name PmSnapshot.exe --noupx --noconfirm --onefile --clean %BUILD_FILE_NAME%.py

@Pause

@ECHO OFF

CD /D "%~dp0"

rd /s /q .\pyrit-packages

REM Set PATH="C:\OpenTwin\Deployment\Python";%PATH%
Set base=%OPENTWIN_DEV_ROOT%\Deployment
Set PYTHONPATH=%base%\Python;%base%\Python\DLLs;%base%\Python\Lib;%base%\Python\Lib\site-packages

"%base%\Python.exe" -m pip install --target .\pyrit-packages .\Distribution\.



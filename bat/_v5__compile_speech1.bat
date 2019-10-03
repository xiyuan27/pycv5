@echo off
cd "C:\Users\kondou\Documents\GitHub\pycv5"

rd build /s /q
rd dist /s /q
pause

set pyname=_v5_proc_adintool
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5_proc_voice2wav
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5_proc_txtreader
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

set pyname=_v5_proc_playvoice
    echo;
    echo %pyname%.py
    pyinstaller %pyname%.py  --onefile
    copy "C:\Users\kondou\Documents\GitHub\pycv5\dist\%pyname%.exe"   "%pyname%.exe"
    del  "%pyname%.spec"

rd build /s /q
rd dist /s /q
pause


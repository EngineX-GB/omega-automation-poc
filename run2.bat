@echo off
call setenv.bat
title %1
%PYTHON_HOME%\python.exe streamhandler_v4.py %1
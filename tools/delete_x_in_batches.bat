@echo off
Setlocal Enabledelayedexpansion
set "str=_"
for /f "delims=" %%i in ('dir /b *.*') do (
set "var=%%i" & ren "%%i" "!var:%str%=!")
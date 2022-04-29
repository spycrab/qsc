@echo off
REM QSC (Qt SDK Creator) - A tool for automatically downloading, building and stripping down Qt
REM Copyright (C) 2020 spycrab0
REM
REM This program is free software: you can redistribute it and/or modify
REM it under the terms of the GNU General Public License as published by
REM the Free Software Foundation, either version 3 of the License, or
REM (at your option) any later version.
REM
REM This program is distributed in the hope that it will be useful,
REM but WITHOUT ANY WARRANTY; without even the implied warranty of
REM MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
REM GNU General Public License for more details.
REM
REM You should have received a copy of the GNU General Public License
REM along with this program.  If not, see <http://www.gnu.org/licenses/>.


IF "%USE_VS%"=="1" ( 
     if "%VCVARSALL%"=="" (
          call "%PROGRAMFILES%\Microsoft Visual Studio\%VS_VERSION%\%VS_EDITION%\Common7\Tools\VsDevCmd.bat"
     ) else (
          call "%PROGRAMFILES%\Microsoft Visual Studio\%VS_VERSION%\%VS_EDITION%\VC\Auxiliary\Build\vcvarsall.bat" %VCVARSALL%
     )
)


:configure
set DETERMINISM_COMPILE="/experimental:deterministic"
rem incremental:no only really needed for debug target, which defaults it on
set DETERMINISM_LINK="/experimental:deterministic /INCREMENTAL:NO"

rem msvc_obj_debug_info gets Qt's cmake to replace /Zi with /Z7

call ..\qt-everywhere-src-%RELEASE%\configure.bat ^
 -opensource -confirm-license ^
 %QT_CONFIGURE_OPTIONS% ^
 -prefix %OUTNAME% ^
 %QT_PLATFORM% ^
 %QT_HOST_PATH% ^
 -- -DCMAKE_ASM_FLAGS=%DETERMINISM_COMPILE% ^
 -DCMAKE_C_FLAGS=%DETERMINISM_COMPILE% ^
 -DCMAKE_CXX_FLAGS=%DETERMINISM_COMPILE% ^
 -DCMAKE_EXE_LINKER_FLAGS=%DETERMINISM_LINK% ^
 -DCMAKE_MODULE_LINKER_FLAGS=%DETERMINISM_LINK% ^
 -DCMAKE_SHARED_LINKER_FLAGS=%DETERMINISM_LINK% ^
 -DCMAKE_STATIC_LINKER_FLAGS="/experimental:deterministic" ^
 -DFEATURE_msvc_obj_debug_info=ON

IF NOT "%ERRORLEVEL%"=="0" (
     echo An error occured while configuring! Exit code is %ERRORLEVEL%
     exit 1
)

:compile
title Compiling...
echo Compiling...
cmake --build . --parallel

IF NOT "%ERRORLEVEL%"=="0" (
     echo An error occured while compiling! Exit code is %ERRORLEVEL%
     exit 1
)

:install
title Installing...
echo Installing...
ninja install

IF NOT "%ERRORLEVEL%"=="0" (
     echo An error occured while installing! Exit code is %ERRORLEVEL%
     exit 1
)

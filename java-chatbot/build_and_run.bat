@echo off
setlocal

set SRC_DIR=src
set OUT_DIR=out

if not exist %OUT_DIR% mkdir %OUT_DIR%

javac -d %OUT_DIR% %SRC_DIR%\*.java

java -cp %OUT_DIR% ChatbotGUI

endlocal


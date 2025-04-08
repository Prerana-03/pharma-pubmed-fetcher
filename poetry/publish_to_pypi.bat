@echo off
echo Building package...
poetry build

echo Publishing to PyPI...
poetry publish

echo Done! Package published to PyPI.
pause 
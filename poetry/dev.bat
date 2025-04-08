@echo off
REM Development tasks for PubMed Fetcher

if "%1"=="" goto help
if "%1"=="install" goto install
if "%1"=="test" goto test
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="clean" goto clean
if "%1"=="build" goto build
if "%1"=="publish-test" goto publish-test
if "%1"=="all" goto all
goto help

:install
poetry install
goto end

:test
poetry run pytest
goto end

:lint
poetry run flake8 pubmed_fetcher tests
poetry run mypy pubmed_fetcher
goto end

:format
poetry run black pubmed_fetcher tests
poetry run isort pubmed_fetcher tests
goto end

:clean
if exist build\ rmdir /s /q build
if exist dist\ rmdir /s /q dist
if exist *.egg-info rmdir /s /q *.egg-info
if exist .coverage del .coverage
if exist htmlcov\ rmdir /s /q htmlcov
if exist .pytest_cache\ rmdir /s /q .pytest_cache
if exist .mypy_cache\ rmdir /s /q .mypy_cache
goto end

:build
poetry build
goto end

:publish-test
poetry publish -r testpypi
goto end

:all
call :install
call :lint
call :test
call :format
goto end

:help
echo Usage: dev.bat [command]
echo.
echo Commands:
echo   install      Install dependencies
echo   test         Run tests
echo   lint         Run linters
echo   format       Format code
echo   clean        Clean build artifacts
echo   build        Build package
echo   publish-test Publish to Test-PyPI
echo   all          Run install, lint, test, and format
goto end

:end 
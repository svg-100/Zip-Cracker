@echo off

for /r %%f in (*.py) do (
    python "%%f"
)
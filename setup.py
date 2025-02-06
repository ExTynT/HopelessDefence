import sys
import os
from cx_Freeze import setup, Executable

def get_files_in_directory(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append((os.path.join(root, filename), os.path.join(root, filename)))
    return files

# Resource files
resource_files = []
resource_files.extend(get_files_in_directory("fonts"))
resource_files.extend(get_files_in_directory("music"))
resource_files.extend(get_files_in_directory("sprites"))

# Dependencies
build_exe_options = {
    "packages": ["pygame", "sys", "os", "random", "math", "time"],
    "includes": [
        "Tower",
        "Enemy",
        "Map",
        "Wave",
        "Shop",
        "Menus",
        "Economy"
    ],
    "include_files": resource_files,
    "excludes": [],
    "include_msvcr": True
}

setup(
    name="HopelessDefence",
    version="1.0",
    description="Tower Defense Game",
    options={"build_exe": build_exe_options},
    executables=[Executable(
        "main.py",
        base="Win32GUI" if sys.platform == "win32" else None,
        target_name="HopelessDefence.exe"
    )]
) 
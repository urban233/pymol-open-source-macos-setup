import sys
import pathlib

import toml
from cx_Freeze import setup

# <editor-fold desc="Module constants">
tmp_pyproject_toml = toml.load("../pyproject.toml")
PROJECT_NAME = tmp_pyproject_toml["project"]["name"]
PROJECT_VERSION = tmp_pyproject_toml["project"]["version"]

PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
SHARED_SUFFIX = f".cpython-{PYTHON_VERSION.replace('.', '')}-darwin.so"

PROJECT_ROOT_DIR = pathlib.Path(__file__).parent.parent
# </editor-fold>


build_exe_options = {
  "excludes": ["tkinter", "unittest"],
  "includes": ["copy", "encodings", "PyQt5.uic", "pymol.povray", "pymol.parser", "uuid"],
  "include_files": [
    (
      pathlib.Path(PROJECT_ROOT_DIR / f".venv/lib/python{PYTHON_VERSION}/site-packages/pymol" / f"_cmd{SHARED_SUFFIX}"),
      f"./lib/pymol/_cmd{SHARED_SUFFIX}"
     )
  ]
}

bdist_mac_options = {
  "custom_info_plist": pathlib.Path(PROJECT_ROOT_DIR / "Info.plist")
}

setup(
  name="Open-Source-PyMOL",
  version=PROJECT_VERSION,
  options={
    "build_exe": build_exe_options,
    "bdist_mac": bdist_mac_options
  },
  executables=[
    {
      "target_name": "PyMOL",
      "script": pathlib.Path(PROJECT_ROOT_DIR / "pymol/pymol/startup_wrapper.py"),
      "base": "gui",
      "icon": pathlib.Path(PROJECT_ROOT_DIR / "alternative_design/icon.icns"),
    }
  ],
)

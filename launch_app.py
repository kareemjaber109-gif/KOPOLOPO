"""Launcher for the Streamlit dashboard.

Sets HOME / USERPROFILE / STREAMLIT_CONFIG_DIR to writable paths inside
the project root so Streamlit never hits Windows permission errors on
%USERPROFILE%\\.streamlit .

Run:
  python launch_app.py
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Writable folders inside the project
HOME_DIR = ROOT / "_userhome"
CFG_DIR  = ROOT / ".streamlit"
HOME_DIR.mkdir(exist_ok=True)
CFG_DIR.mkdir(exist_ok=True)

# Redirect everything before importing / launching anything
os.environ["HOME"]                = str(HOME_DIR)
os.environ["USERPROFILE"]         = str(HOME_DIR)
os.environ["APPDATA"]             = str(HOME_DIR)
os.environ["LOCALAPPDATA"]        = str(HOME_DIR)
os.environ["STREAMLIT_CONFIG_DIR"]= str(CFG_DIR)
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

print("[launcher] Project root  :", ROOT)
print("[launcher] HOME          :", os.environ["HOME"])
print("[launcher] STREAMLIT_CFG:", os.environ["STREAMLIT_CONFIG_DIR"])

from streamlit.web import cli as stcli

# Emulate:  streamlit run app.py --server.headless true --server.port 8501 ...
sys.argv = [
    "streamlit", "run", str(ROOT / "app.py"),
    "--server.headless", "true",
    "--server.port", "8501",
    "--server.address", "127.0.0.1",
    "--browser.gatherUsageStats", "false",
]

sys.exit(stcli.main())

import os
from pathlib import Path

MPL_CONFIG = Path(__file__).resolve().parents[1] / ".mplconfig"
MPL_CONFIG.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPL_CONFIG))

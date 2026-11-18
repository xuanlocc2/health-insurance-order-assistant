import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = ""  # test không bao giờ ghi vào database thật trong .env

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))  # để "from src import ..." chạy được với lệnh pytest trần

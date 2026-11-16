"""Log xác nhận: JSONL, chỉ ghi thêm (spec mục 9)."""
import json
from pathlib import Path


def append(rows, path="logs/xac-nhan.jsonl"):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    # một lần write cho cả lô để các dòng không bị xen kẽ; default=str cho date của YAML
    data = "".join(json.dumps(r, ensure_ascii=False, default=str) + "\n" for r in rows)
    with p.open("a", encoding="utf-8", newline="\n") as f:
        f.write(data)

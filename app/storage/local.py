from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4


class LocalStorage:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, src: Path, subdir: str, suffix: str) -> Path:
        # 하위 디렉터리에 UUID 파일명으로 저장하고 경로를 반환
        dest_dir = self.base_path / subdir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / f"{uuid4().hex}{suffix}"
        shutil.copy2(src, dest)
        return dest

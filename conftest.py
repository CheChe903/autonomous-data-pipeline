import sys
from pathlib import Path

# 프로젝트 루트를 모듈 검색 경로에 추가해 'app' 패키지를 인식시키기 위함
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

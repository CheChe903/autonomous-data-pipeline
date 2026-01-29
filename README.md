# Autonomous Data Pipeline

자율주행 학습 데이터 관리 시스템을 구축하는 프로젝트입니다. 대규모 주행 데이터의 수집·전처리·검증·서빙 파이프라인을 목표로 합니다. (현재 단계: 라벨 포함 공개 데이터셋 수집/전처리·품질 검증에 집중, 모델 추론은 제외)

## 목표
- KITTI 또는 nuScenes 데이터셋을 자동으로 다운로드하고 저장소(MinIO 또는 로컬)에 적재
- 이미지/영상 전처리(리사이징, 정규화) 및 시간대·날씨·도로 유형별 자동 분류
- YOLOv8 기반 객체 탐지 후 바운딩 박스/클래스/신뢰도를 PostgreSQL에 기록
- 기존 어노테이션 대비 품질 검증 및 저품질 데이터(블러, 가림 등) 자동 필터링
- FastAPI로 업로드/조회/다운로드/통계 API 제공
- Docker Compose 한 번으로 전체 시스템 실행

## 요구사항
1) 데이터 수집 및 전처리  
   - KITTI 또는 nuScenes 데이터셋 다운로드·로드  
   - 리사이징·정규화 등 자동 전처리  
   - 시간대/날씨/도로 유형별 자동 분류  
   - MinIO 또는 로컬 스토리지에 원본 보관  

2) 객체 탐지 및 어노테이션 관리  
   - (추후) YOLO(ultralytics)로 차량/보행자/신호등 탐지  
   - 기존 라벨(JSON/XML/txt) 파싱 후 PostgreSQL 저장  
   - 기존 어노테이션과 비교해 품질 검증  
   - 저품질(블러, 가림 등) 자동 필터링  

3) FastAPI 백엔드  
   - `POST /upload` : 새 주행 영상 업로드(옵션 라벨 파일) → 전처리 후 저장·DB 기록  
   - `GET /images` : 라벨/품질(블러) 필터 + 페이징 조회  
   - `GET /images/{id}` : 특정 이미지 메타/라벨 상세  
   - `GET /download/dataset` : 조건 기반 서브셋 ZIP 다운로드(로컬 스토리지 지원)  
   - `GET /stats` : 객체별 분포, 블러 통계  

4) 데이터베이스 스키마  
   - `images`: 경로, 크기, 촬영시간, 품질점수 등 메타데이터  
   - `detections`: 탐지 결과 기록  
   - `datasets`: 생성된 학습 데이터셋 버전 관리  

5) 선택: Streamlit 대시보드  
   - 데이터 조회/필터, 이미지 뷰어, 바운딩 박스 시각화  

## 기술 스택
- Python, FastAPI
- PostgreSQL (메타데이터)
- MinIO 또는 로컬 파일시스템 (이미지 저장) — 기본은 로컬
- OpenCV, Pillow (이미지 처리)
- (추후) YOLOv8 / ultralytics (객체 탐지)
- Docker, Docker Compose

## 성공 기준
- 1000개 이상의 이미지 처리 가능
- API 평균 응답 시간 < 500ms
- 데이터 품질 검증 자동화
- `docker compose up` 한 번으로 전체 시스템 실행
- README에 명확한 사용법 문서화

## 진행 순서 (마일스톤)
1. 프로젝트 구조 설계 및 환경 설정  
2. 데이터셋 다운로드 및 탐색  
3. 데이터베이스 스키마 설계  
4. 이미지 전처리 파이프라인 구현  
5. 객체 탐지 및 DB 저장 로직  
6. FastAPI 엔드포인트 구현  
7. Docker Compose로 통합  
8. 테스트 및 문서화  

## 초기 세팅 상태
- `git init` 완료 (초기 브랜치: master)  
- 추후 GitHub 원격 저장소 연결 예정 (`git remote add origin <url>`)  

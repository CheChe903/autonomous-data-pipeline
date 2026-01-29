from pathlib import Path
import numpy as np
import cv2

from app.pipeline.preprocess import preprocess_image


def test_preprocess_image(tmp_path: Path):
    # 검사용 더미 이미지를 생성
    img = np.zeros((100, 200, 3), dtype=np.uint8)
    cv2.rectangle(img, (10, 10), (190, 90), (255, 255, 255), 2)
    src = tmp_path / "src.jpg"
    cv2.imwrite(str(src), img)

    # 전처리 실행 후 메타데이터 검증
    out_path, meta = preprocess_image(
        input_path=src,
        output_path=tmp_path / "out",
        size=(64, 64),
        image_format="jpeg",
        jpeg_quality=90,
    )

    assert out_path.exists()
    assert meta["width"] == 64
    assert meta["height"] == 64
    assert meta["blur_score"] >= 0.0
